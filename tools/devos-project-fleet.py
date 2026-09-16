#!/usr/bin/env python3
"""Read-only DevOS Project Fleet Watch v1.

Aggregates repository observations through Managed Project Lifecycle v1 so a
new/unmanaged repository cannot disappear inside a list of accessible projects.
The engine can assess deterministic snapshot files or perform bounded read-only
GitHub discovery. It never onboards, mutates, deploys, or creates authorization.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE_PATH = ROOT / "tools" / "devos-project-lifecycle.py"
spec = importlib.util.spec_from_file_location("devos_project_lifecycle", LIFECYCLE_PATH)
assert spec and spec.loader
lifecycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lifecycle)

PROTOCOL = "DEVOS-PROJECT-FLEET-WATCH-v1"
SNAPSHOT_PROTOCOL = "DEVOS-PROJECT-FLEET-SNAPSHOT-v1"
PROVIDER = "github"
MAX_REPOSITORIES = 200

BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "external_mutation": "NONE",
    "production_ready": False,
    "publication_authorized": False,
    "deployment_authorized": False,
}


def _iso_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _manifest_from_text(text: str) -> dict[str, str]:
    """Parse only the top-level scalar identity fields used by lifecycle v1."""
    data: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def _blocked(reason: str) -> dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "fleet_status": "BLOCKED",
        "reason": reason,
        "repository_count": 0,
        "repositories": [],
        "summary": {
            "managed": 0,
            "onboarding_required": 0,
            "hold": 0,
            "blocked": 0,
            "archived": 0,
        },
        "fleet_clean": False,
        "next_actions": [],
        "drift": None,
        "execution": "NONE",
        "mutation": "NONE",
        **BOUNDARIES,
    }


def validate_snapshot(payload: Any) -> tuple[bool, str | None]:
    if not isinstance(payload, dict):
        return False, "snapshot must be a JSON object"
    allowed = {"protocol", "provider", "observed_at", "repositories"}
    if set(payload) != allowed:
        return False, "snapshot fields are invalid"
    if payload.get("protocol") != SNAPSHOT_PROTOCOL:
        return False, "snapshot protocol is invalid"
    if not isinstance(payload.get("provider"), str) or not payload["provider"].strip():
        return False, "snapshot provider is required"
    if not _iso_timestamp(payload.get("observed_at")):
        return False, "snapshot observed_at must be timezone-aware ISO-8601"
    repos = payload.get("repositories")
    if not isinstance(repos, list):
        return False, "repositories must be a list"
    if len(repos) > MAX_REPOSITORIES:
        return False, f"repository count exceeds {MAX_REPOSITORIES}"

    seen: set[str] = set()
    entry_fields = {"repository", "default_branch", "observed_head", "archived", "files", "manifest"}
    for entry in repos:
        if not isinstance(entry, dict) or set(entry) != entry_fields:
            return False, "repository entry fields are invalid"
        repository = entry.get("repository")
        if not isinstance(repository, str) or "/" not in repository or not repository.strip():
            return False, "repository identity is invalid"
        if repository in seen:
            return False, f"duplicate repository: {repository}"
        seen.add(repository)
        if entry.get("default_branch") is not None and not isinstance(entry.get("default_branch"), str):
            return False, f"default_branch is invalid for {repository}"
        if not isinstance(entry.get("archived"), bool):
            return False, f"archived must be boolean for {repository}"
        files = entry.get("files")
        if not isinstance(files, list) or any(not isinstance(item, str) or not item for item in files):
            return False, f"files are invalid for {repository}"
        if len(set(files)) != len(files):
            return False, f"files contain duplicates for {repository}"
        manifest = entry.get("manifest")
        if manifest is not None and not isinstance(manifest, dict):
            return False, f"manifest is invalid for {repository}"
        head = entry.get("observed_head")
        if head is not None and (not isinstance(head, str) or not lifecycle.SHA40.fullmatch(head)):
            return False, f"observed_head is invalid for {repository}"
    return True, None


def _fleet_entry(entry: dict[str, Any]) -> dict[str, Any]:
    if entry["archived"]:
        return {
            "repository": entry["repository"],
            "fleet_state": "ARCHIVED",
            "managed": None,
            "development_continuation_allowed": False,
            "next_action": "NONE",
            "observed_head": entry["observed_head"],
            "default_branch": entry["default_branch"],
            "archived": True,
        }

    report = lifecycle.classify_observation(
        repository=entry["repository"],
        files=set(entry["files"]),
        manifest=entry["manifest"],
        observed_head=entry["observed_head"],
    )
    return {
        "repository": entry["repository"],
        "fleet_state": report["status"],
        "management_state": report.get("management_state"),
        "managed": report.get("managed", False),
        "development_continuation_allowed": report.get("development_continuation_allowed", False),
        "next_action": report.get("next_action", "HOLD"),
        "reason": report.get("reason"),
        "missing_files": report.get("missing_files", []),
        "observed_head": entry["observed_head"],
        "default_branch": entry["default_branch"],
        "archived": False,
    }


def _state_map(assessment: dict[str, Any]) -> dict[str, str]:
    return {item["repository"]: item["fleet_state"] for item in assessment.get("repositories", [])}


def compute_drift(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, list[str]]:
    old = _state_map(previous)
    new = _state_map(current)
    old_names, new_names = set(old), set(new)
    new_repositories = sorted(new_names - old_names)
    removed_repositories = sorted(old_names - new_names)
    new_unmanaged = sorted(
        name for name in new_repositories if new[name] not in {"MANAGED", "ARCHIVED"}
    )
    newly_managed = sorted(
        name for name in old_names & new_names if old[name] != "MANAGED" and new[name] == "MANAGED"
    )
    management_regressions = sorted(
        name for name in old_names & new_names if old[name] == "MANAGED" and new[name] != "MANAGED"
    )
    newly_attention_required = sorted(
        name
        for name in new_names
        if new[name] not in {"MANAGED", "ARCHIVED"}
        and (name not in old or old[name] in {"MANAGED", "ARCHIVED"})
    )
    return {
        "new_repositories": new_repositories,
        "removed_repositories": removed_repositories,
        "new_unmanaged": new_unmanaged,
        "newly_managed": newly_managed,
        "management_regressions": management_regressions,
        "newly_attention_required": newly_attention_required,
    }


def assess_snapshot(payload: Any, previous_payload: Any | None = None) -> dict[str, Any]:
    valid, reason = validate_snapshot(payload)
    if not valid:
        return _blocked(reason or "snapshot invalid")

    entries = [_fleet_entry(item) for item in payload["repositories"]]
    summary = {
        "managed": sum(item["fleet_state"] == "MANAGED" for item in entries),
        "onboarding_required": sum(item["fleet_state"] == "ONBOARDING_REQUIRED" for item in entries),
        "hold": sum(item["fleet_state"] == "HOLD" for item in entries),
        "blocked": sum(item["fleet_state"] == "BLOCKED" for item in entries),
        "archived": sum(item["fleet_state"] == "ARCHIVED" for item in entries),
    }
    active_count = len(entries) - summary["archived"]
    if summary["blocked"] or summary["hold"]:
        fleet_status = "HOLD"
    elif summary["onboarding_required"]:
        fleet_status = "ATTENTION"
    elif active_count == 0:
        fleet_status = "EMPTY"
    else:
        fleet_status = "HEALTHY"

    next_actions = [
        {"repository": item["repository"], "action": item["next_action"]}
        for item in entries
        if item["fleet_state"] not in {"MANAGED", "ARCHIVED"}
    ]
    result: dict[str, Any] = {
        "protocol": PROTOCOL,
        "fleet_status": fleet_status,
        "repository_count": len(entries),
        "active_repository_count": active_count,
        "provider": payload["provider"],
        "observed_at": payload["observed_at"],
        "repositories": sorted(entries, key=lambda item: item["repository"].lower()),
        "summary": summary,
        "fleet_clean": fleet_status == "HEALTHY",
        "next_actions": next_actions,
        "drift": None,
        "execution": "NONE",
        "mutation": "NONE",
        **BOUNDARIES,
    }

    if previous_payload is not None:
        previous = assess_snapshot(previous_payload)
        if previous["fleet_status"] == "BLOCKED":
            result["fleet_status"] = "BLOCKED"
            result["fleet_clean"] = False
            result["reason"] = f"previous snapshot invalid: {previous.get('reason', 'unknown')}"
        else:
            result["drift"] = compute_drift(previous, result)
            if result["drift"]["management_regressions"]:
                result["fleet_status"] = "HOLD"
                result["fleet_clean"] = False
            elif result["drift"]["new_unmanaged"] and result["fleet_status"] == "HEALTHY":
                # Defensive; normally an unmanaged repo already yields ATTENTION/HOLD.
                result["fleet_status"] = "ATTENTION"
                result["fleet_clean"] = False
    return result


def load_snapshot(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _request_json(url: str, token: str | None, *, allow_404: bool = False) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "devos-project-fleet-watch-v1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if allow_404 and exc.code == 404:
            return None
        # Do not include headers/tokens or provider response bodies in errors.
        raise RuntimeError(f"GitHub read failed with HTTP {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError("GitHub read failed or timed out") from exc


def _repo_listing_url(owner: str, page: int) -> str:
    if owner == "@me":
        return (
            "https://api.github.com/user/repos?per_page=100"
            f"&page={page}&sort=full_name&direction=asc&affiliation=owner,collaborator,organization_member"
        )
    escaped = urllib.parse.quote(owner, safe="")
    return f"https://api.github.com/users/{escaped}/repos?per_page=100&page={page}&sort=full_name&direction=asc"


def discover_github(
    owner: str,
    token: str | None,
    *,
    limit: int = 100,
    fetch_json: Callable[..., Any] = _request_json,
) -> dict[str, Any]:
    if not owner.strip():
        raise ValueError("GitHub owner is required")
    if owner == "@me" and not token:
        raise ValueError("GITHUB_TOKEN is required for @me discovery")
    if limit < 1 or limit > MAX_REPOSITORIES:
        raise ValueError(f"limit must be between 1 and {MAX_REPOSITORIES}")

    repos: list[dict[str, Any]] = []
    page = 1
    while len(repos) < limit:
        listing = fetch_json(_repo_listing_url(owner, page), token)
        if not isinstance(listing, list):
            raise RuntimeError("GitHub repository listing response is invalid")
        if not listing:
            break
        repos.extend(item for item in listing if isinstance(item, dict))
        if len(listing) < 100:
            break
        page += 1
    repos = repos[:limit]

    observations: list[dict[str, Any]] = []
    for repo in repos:
        full_name = repo.get("full_name")
        if not isinstance(full_name, str) or "/" not in full_name:
            continue
        archived = bool(repo.get("archived", False))
        default_branch = repo.get("default_branch") if isinstance(repo.get("default_branch"), str) else None
        observed_head: str | None = None
        files: list[str] = []
        manifest: dict[str, str] | None = None

        if default_branch:
            escaped_repo = "/".join(urllib.parse.quote(part, safe="") for part in full_name.split("/", 1))
            branch_url = (
                f"https://api.github.com/repos/{escaped_repo}/branches/"
                f"{urllib.parse.quote(default_branch, safe='')}"
            )
            branch = fetch_json(branch_url, token, allow_404=True)
            if isinstance(branch, dict):
                commit = branch.get("commit") if isinstance(branch.get("commit"), dict) else {}
                sha = commit.get("sha")
                if isinstance(sha, str) and lifecycle.SHA40.fullmatch(sha):
                    observed_head = sha
                commit_detail = commit.get("commit") if isinstance(commit.get("commit"), dict) else {}
                tree = commit_detail.get("tree") if isinstance(commit_detail.get("tree"), dict) else {}
                tree_sha = tree.get("sha")
                if isinstance(tree_sha, str) and lifecycle.SHA40.fullmatch(tree_sha):
                    tree_url = f"https://api.github.com/repos/{escaped_repo}/git/trees/{tree_sha}?recursive=1"
                    tree_payload = fetch_json(tree_url, token, allow_404=True)
                    if isinstance(tree_payload, dict) and isinstance(tree_payload.get("tree"), list):
                        files = sorted(
                            item["path"]
                            for item in tree_payload["tree"]
                            if isinstance(item, dict)
                            and item.get("type") == "blob"
                            and isinstance(item.get("path"), str)
                        )

            manifest_url = f"https://api.github.com/repos/{escaped_repo}/contents/.ai/manifest.yaml"
            manifest_payload = fetch_json(manifest_url, token, allow_404=True)
            if isinstance(manifest_payload, dict) and isinstance(manifest_payload.get("content"), str):
                try:
                    text = base64.b64decode(manifest_payload["content"], validate=False).decode("utf-8")
                    manifest = _manifest_from_text(text)
                except (ValueError, UnicodeDecodeError):
                    manifest = {"managed_by": "INVALID_MANIFEST_ENCODING"}

        observations.append(
            {
                "repository": full_name,
                "default_branch": default_branch,
                "observed_head": observed_head,
                "archived": archived,
                "files": files,
                "manifest": manifest,
            }
        )

    return {
        "protocol": SNAPSHOT_PROTOCOL,
        "provider": PROVIDER,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "repositories": observations,
    }


def _print_text(report: dict[str, Any]) -> None:
    print("DEVOS PROJECT FLEET WATCH v1")
    print(f"Fleet status: {report.get('fleet_status')}")
    print(f"Repositories: {report.get('repository_count', 0)}")
    summary = report.get("summary", {})
    print(
        "Managed: {managed} | Onboarding: {onboarding_required} | Hold: {hold} | "
        "Blocked: {blocked} | Archived: {archived}".format(
            managed=summary.get("managed", 0),
            onboarding_required=summary.get("onboarding_required", 0),
            hold=summary.get("hold", 0),
            blocked=summary.get("blocked", 0),
            archived=summary.get("archived", 0),
        )
    )
    for item in report.get("repositories", []):
        print(f"- {item['repository']}: {item['fleet_state']} → {item['next_action']}")
    drift = report.get("drift")
    if drift:
        print(f"New unmanaged: {', '.join(drift['new_unmanaged']) or 'none'}")
        print(f"Management regressions: {', '.join(drift['management_regressions']) or 'none'}")
    print("Authority: UNCHANGED")
    print("External mutation: NONE")
    print("production_ready=false")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only DevOS Project Fleet Watch v1")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--snapshot", help="current fleet snapshot JSON")
    source.add_argument("--github-owner", help="read-only GitHub discovery; use @me for authenticated accessible repos")
    parser.add_argument("--previous", help="previous fleet snapshot JSON for drift detection")
    parser.add_argument("--limit", type=int, default=100, help=f"repository discovery cap (1-{MAX_REPOSITORIES})")
    parser.add_argument("--require-clean", action="store_true", help="exit non-zero unless every active repository is MANAGED")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    previous_payload = None
    if args.previous:
        try:
            previous_payload = load_snapshot(Path(args.previous))
        except (OSError, json.JSONDecodeError) as exc:
            report = _blocked(f"previous snapshot load failed: {exc}")
            print(json.dumps(report, indent=2, sort_keys=True) if args.json else report["reason"])
            return 2

    execution = "NONE"
    try:
        if args.snapshot:
            payload = load_snapshot(Path(args.snapshot))
        else:
            token = os.environ.get("GITHUB_TOKEN")
            payload = discover_github(args.github_owner, token, limit=args.limit)
            execution = "READ_ONLY_PROVIDER"
        report = assess_snapshot(payload, previous_payload)
    except (OSError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        report = _blocked(str(exc))

    report["execution"] = execution
    report["mutation"] = "NONE"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_text(report)

    if args.require_clean and report.get("fleet_status") != "HEALTHY":
        return 2
    return 2 if report.get("fleet_status") in {"BLOCKED", "HOLD"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
