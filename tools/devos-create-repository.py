#!/usr/bin/env python3
"""Provider-neutral repository creation adapter with GitHub REST support.

Default mode is plan-only. Live creation requires --apply and DEVOS_ALLOW_REPO_CREATE=1.
Credentials are read only from environment/configured client code and are never printed.

Repository creation is only the provider-resource step. A created repository must
still pass fresh readback plus the Managed Project Lifecycle gate before DevOS
may continue application development.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

PROTOCOL = "DEVOS-REPOSITORY-CREATE-v1"
CAPABILITY = "repository.create"
LIFECYCLE_POSTCONDITION = {
    "managed_project_required": True,
    "required_next_capability": "project.onboard",
    "lifecycle_protocol": "DEVOS-MANAGED-PROJECT-LIFECYCLE-v1",
    "fresh_repository_readback_required": True,
    "development_continuation_allowed": False,
}


def validate_name(name: str) -> str | None:
    if not isinstance(name, str) or not name.strip():
        return "repository name is required"
    if len(name.strip()) > 100:
        return "repository name is too long"
    return None


def plan(owner: str, name: str, private: bool, description: str = "") -> dict:
    reason = validate_name(name)
    if not owner.strip():
        reason = reason or "repository owner/namespace is required"
    if reason:
        return {
            "protocol": PROTOCOL, "capability": CAPABILITY, "status": "BLOCKED",
            "reason": reason, "authority": "UNCHANGED", "authorization": "UNCHANGED",
            "execution": "NONE", "mutation": "NONE",
            "lifecycle_postcondition": dict(LIFECYCLE_POSTCONDITION),
        }
    return {
        "protocol": PROTOCOL, "capability": CAPABILITY, "status": "READY",
        "owner": owner.strip(), "name": name.strip(), "private": bool(private),
        "description": description, "provider": "github", "authority": "UNCHANGED",
        "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE",
        "verification_required": True,
        "lifecycle_postcondition": dict(LIFECYCLE_POSTCONDITION),
    }


def github_create(owner: str, name: str, private: bool, description: str, token: str) -> dict:
    """Create one repository via GitHub REST.

    This function intentionally performs a single POST. Caller must reconcile
    the returned state before claiming verified completion.
    """
    if not token:
        return {"status": "BLOCKED", "reason": "GitHub token unavailable"}
    payload = json.dumps({
        "name": name,
        "description": description,
        "private": private,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": False,
        "auto_init": False,
    }).encode("utf-8")

    if owner == "@me":
        url = "https://api.github.com/user/repos"
    else:
        url = f"https://api.github.com/orgs/{urllib.parse.quote(owner, safe='')}/repos"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "devos-repository-create-v1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
            return {"status": "ATTEMPTED", "provider": "github", "http_status": response.status,
                    "repository": data.get("full_name"), "html_url": data.get("html_url"),
                    "default_branch": data.get("default_branch")}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"status": "FAILED", "provider": "github", "http_status": exc.code,
                "error": body[:1000]}
    except urllib.error.URLError as exc:
        return {"status": "UNCERTAIN", "provider": "github", "error": str(exc.reason)}
    except TimeoutError:
        return {"status": "UNCERTAIN", "provider": "github", "error": "request timeout"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Governed DevOS repository creation")
    parser.add_argument("--owner", required=True, help="GitHub owner/org; use @me for the authenticated user")
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--apply", action="store_true", help="perform one live repository-create request")
    parser.add_argument("--authorization", choices=["EXPLICIT"], help="externally supplied authorization signal")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = plan(args.owner, args.name, args.private, args.description)
    report["mode"] = "apply" if args.apply else "plan"

    if report["status"] != "READY":
        code = 2
    elif not args.apply:
        code = 0
        report["status"] = "READY"
        report["next"] = "After provider creation and fresh readback, run the managed-project lifecycle gate and onboard before development continuation."
    elif args.authorization != "EXPLICIT":
        code = 2
        report["status"] = "NEEDS_APPROVAL"
        report["reason"] = "explicit repository-create authorization is required"
    elif os.environ.get("DEVOS_ALLOW_REPO_CREATE") != "1":
        code = 2
        report["status"] = "BLOCKED"
        report["reason"] = "provider-side repository creation is disabled by local safety gate"
    else:
        token = os.environ.get("GITHUB_TOKEN", "")
        result = github_create(args.owner.strip(), args.name.strip(), args.private, args.description, token)
        report["provider_result"] = result
        report["execution"] = "ONE_REQUEST"
        report["mutation"] = "attempted"
        if result.get("status") == "UNCERTAIN":
            report["status"] = "HOLD"
            report["replay"] = "FORBIDDEN"
        elif result.get("status") == "ATTEMPTED":
            report["status"] = "NEEDS_READBACK"
            report["replay"] = "NOT_NEEDED_YET"
            report["next"] = "Fresh provider readback, then Managed Project Lifecycle check/onboarding. Development continuation remains HOLD until MANAGED."
        else:
            report["status"] = "HOLD"
            report["replay"] = "FORBIDDEN"
        code = 0 if report["status"] in {"NEEDS_READBACK", "HOLD"} else 2

    report["authority"] = "UNCHANGED"
    report["authorization"] = "UNCHANGED"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("DEVOS REPOSITORY CREATION v1")
        print(f"Target: {report.get('owner', '?')}/{report.get('name', '?')}")
        print(f"Mode: {'APPLY' if args.apply else 'PLAN'}")
        print(f"Status: {report.get('status')}")
        if report.get("reason"):
            print(f"Reason: {report['reason']}")
        print("Managed-project postcondition: REQUIRED")
        print("Development continuation: HOLD until lifecycle state MANAGED")
        print("Authority: UNCHANGED")
        print("Authorization: UNCHANGED")
        if report.get("execution") == "ONE_REQUEST":
            print("Execution: ONE_REQUEST")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
