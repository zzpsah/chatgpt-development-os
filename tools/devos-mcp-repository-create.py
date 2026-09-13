#!/usr/bin/env python3
"""Host-neutral DevOS MCP/App adapter for governed repository creation.

This module does not contact a provider. It validates a bounded tool request and
combines DevOS authorization, provider-capability, attempt, and fresh-readback
evidence. The provider adapter remains a separate boundary.
"""
from __future__ import annotations

import argparse
import json
import re
from typing import Any

PROTOCOL = "DEVOS-MCP-REPOSITORY-CREATE-v1"
TOOL = "devos.create_repository"
CAPABILITY = "repository.create"
ALLOWED_REQUEST_KEYS = {
    "provider", "owner", "repository", "visibility", "description",
    "initialization_policy", "default_branch", "project_identity",
}
SECRET_KEYS = {
    "token", "password", "secret", "credential", "credentials", "api_key",
    "authorization_header", "private_key",
}
NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
OWNER_RE = re.compile(r"^(?:@me|[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))$")
STATUSES = {
    "READY", "NEEDS_APPROVAL", "CAPABILITY_UNAVAILABLE", "BLOCKED", "HOLD",
    "CREATION_ATTEMPTED", "VERIFIED", "NEEDS_EXTERNAL_REPO_CREATION",
}


def _base(status: str, reason: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {
        "protocol": PROTOCOL,
        "tool": TOOL,
        "capability": CAPABILITY,
        "status": status,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation_requests": 0,
        "live_provider_proven": False,
        "production_proven": False,
        "evidence_level": "COMPONENT_TEST_VERIFIED",
    }
    if reason:
        out["reason"] = reason
    return out


def _contains_secret(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in SECRET_KEYS or _contains_secret(item):
                return True
    elif isinstance(value, list):
        return any(_contains_secret(item) for item in value)
    return False


def validate_request(request: Any) -> str | None:
    if not isinstance(request, dict):
        return "request must be an object"
    if _contains_secret(request):
        return "credential material is forbidden in the MCP/App request"
    unknown = set(request) - ALLOWED_REQUEST_KEYS
    if unknown:
        return "unknown request fields: " + ", ".join(sorted(unknown))
    required = {"provider", "owner", "repository", "visibility", "initialization_policy", "project_identity"}
    missing = [name for name in sorted(required) if not isinstance(request.get(name), str) or not request[name].strip()]
    if missing:
        return "missing required fields: " + ", ".join(missing)
    if request["provider"] not in {"github", "gitlab", "bitbucket"}:
        return "unsupported provider"
    if not OWNER_RE.fullmatch(request["owner"]):
        return "invalid owner/namespace"
    if not NAME_RE.fullmatch(request["repository"]):
        return "invalid repository name"
    if request["visibility"] not in {"public", "private"}:
        return "invalid visibility"
    if request["initialization_policy"] not in {"empty"}:
        return "unsupported initialization policy"
    default_branch = request.get("default_branch")
    if default_branch is not None and (not isinstance(default_branch, str) or not NAME_RE.fullmatch(default_branch)):
        return "invalid default branch"
    description = request.get("description", "")
    if not isinstance(description, str) or len(description) > 500:
        return "invalid description"
    return None


def _capability_names(provider_capabilities: Any) -> set[str]:
    if not isinstance(provider_capabilities, list) or not all(isinstance(x, str) for x in provider_capabilities):
        return set()
    return set(provider_capabilities)


def _authorization_matches(request: dict[str, Any], authorization: Any) -> bool:
    if not isinstance(authorization, dict):
        return False
    expected = {
        "status": "GRANTED",
        "capability": CAPABILITY,
        "provider": request["provider"],
        "owner": request["owner"],
        "repository": request["repository"],
        "project_identity": request["project_identity"],
    }
    return all(authorization.get(key) == value for key, value in expected.items())


def _fresh_target_is_safe(request: dict[str, Any], target_state: Any) -> bool:
    return (
        isinstance(target_state, dict)
        and target_state.get("fresh") is True
        and target_state.get("provider") == request["provider"]
        and target_state.get("owner") == request["owner"]
        and target_state.get("repository") == request["repository"]
        and target_state.get("exists") is False
    )


def _readback_matches(request: dict[str, Any], readback: Any) -> tuple[bool, str | None]:
    if not isinstance(readback, dict) or readback.get("fresh") is not True:
        return False, "fresh post-create readback is required"
    checks = {
        "provider": request["provider"],
        "owner": request["owner"],
        "repository": request["repository"],
        "exists": True,
    }
    for key, expected in checks.items():
        if readback.get(key) != expected:
            return False, f"post-create target mismatch: {key}"
    observed_visibility = readback.get("visibility")
    if observed_visibility is not None and observed_visibility != request["visibility"]:
        return False, "post-create visibility mismatch"
    intended_branch = request.get("default_branch")
    observed_branch = readback.get("default_branch")
    if intended_branch and observed_branch is not None and observed_branch != intended_branch:
        return False, "post-create default branch mismatch"
    return True, None


def evaluate(
    request: Any,
    provider_capabilities: Any,
    authorization: Any = None,
    target_state: Any = None,
    provider_result: Any = None,
    readback: Any = None,
) -> dict[str, Any]:
    """Evaluate one governed MCP/App repository-create operation.

    provider_result/readback are evidence supplied by the provider boundary. This
    function never issues a provider mutation and never retries one.
    """
    reason = validate_request(request)
    if reason:
        return _base("BLOCKED", reason)
    assert isinstance(request, dict)

    capabilities = _capability_names(provider_capabilities)
    create_cap = f"{request['provider']}.repository.create"
    inspect_cap = f"{request['provider']}.repository.inspect"
    if create_cap not in capabilities:
        out = _base("NEEDS_EXTERNAL_REPO_CREATION", "repository.create capability unavailable")
        out["provider_capability"] = create_cap
        return out
    if inspect_cap not in capabilities:
        return _base("CAPABILITY_UNAVAILABLE", "post-create repository inspection capability unavailable")

    if authorization is None:
        return _base("NEEDS_APPROVAL", "exact repository.create authorization is required")
    if _contains_secret(authorization):
        return _base("BLOCKED", "credential material must not be carried as DevOS authorization")
    if not _authorization_matches(request, authorization):
        return _base("BLOCKED", "authorization is not bound to the exact repository target")
    if not _fresh_target_is_safe(request, target_state):
        return _base("HOLD", "fresh target evidence is missing, stale, or conflicting")

    if provider_result is None:
        out = _base("READY")
        out["next"] = "provider adapter may perform at most one governed create request"
        return out
    if _contains_secret(provider_result) or _contains_secret(readback):
        return _base("BLOCKED", "provider evidence contains forbidden credential material")
    if not isinstance(provider_result, dict):
        return _base("BLOCKED", "provider result must be an object")

    attempt_count = provider_result.get("mutation_requests")
    if attempt_count != 1:
        return _base("BLOCKED", "provider evidence must describe exactly one mutation request")

    provider_status = provider_result.get("status")
    if provider_status in {"TIMEOUT", "UNCERTAIN", "CONNECTION_ERROR", "UNKNOWN"}:
        out = _base("HOLD", "provider completion state is uncertain; reconcile without replay")
        out["execution"] = "ONE_REQUEST"
        out["mutation_requests"] = 1
        out["replay"] = "FORBIDDEN"
        return out
    if provider_status not in {"ATTEMPTED", "CREATED"}:
        out = _base("HOLD", "provider did not produce acceptable creation-attempt evidence")
        out["execution"] = "ONE_REQUEST"
        out["mutation_requests"] = 1
        out["replay"] = "FORBIDDEN"
        return out

    out = _base("CREATION_ATTEMPTED")
    out["execution"] = "ONE_REQUEST"
    out["mutation_requests"] = 1
    out["replay"] = "FORBIDDEN"
    if readback is None:
        out["reason"] = "fresh post-create readback required before VERIFIED"
        return out
    matches, mismatch = _readback_matches(request, readback)
    if not matches:
        out["status"] = "HOLD"
        out["reason"] = mismatch
        return out
    out["status"] = "VERIFIED"
    out["verification"] = "FRESH_PROVIDER_READBACK_MATCHED"
    out["onboarding_handoff"] = {
        "eligible": True,
        "capability": "universal.onboard",
        "project_identity": request["project_identity"],
        "target": f"{request['owner']}/{request['repository']}",
    }
    # Deterministic tests can prove semantics only; live-provider level must be
    # established separately from real request/readback provenance.
    out["evidence_level"] = "PROVIDER_SIMULATED_VERIFIED"
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-json", required=True)
    parser.add_argument("--capabilities-json", required=True)
    parser.add_argument("--authorization-json")
    parser.add_argument("--target-state-json")
    parser.add_argument("--provider-result-json")
    parser.add_argument("--readback-json")
    args = parser.parse_args()

    def load(value: str | None) -> Any:
        return None if value is None else json.loads(value)

    try:
        result = evaluate(
            load(args.request_json), load(args.capabilities_json),
            load(args.authorization_json), load(args.target_state_json),
            load(args.provider_result_json), load(args.readback_json),
        )
    except (json.JSONDecodeError, TypeError) as exc:
        result = _base("BLOCKED", f"malformed MCP/App input: {exc}")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"READY", "CREATION_ATTEMPTED", "VERIFIED", "NEEDS_EXTERNAL_REPO_CREATION"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
