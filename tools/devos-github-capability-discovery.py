#!/usr/bin/env python3
"""Side-effect-free GitHub capability discovery/evaluation primitives for DevOS.

This module consumes provider-reported, non-secret permission metadata. It never
contacts GitHub, reads credentials, or authorizes a mutation by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

CAPABILITIES = {
    "repository.create",
    "repository.delete",
    "branch.create",
    "branch.update",
    "branch.force_update",
    "branch.delete",
    "file.create",
    "file.update",
    "file.delete",
    "pr.merge",
}

EXISTING_REPOSITORY_CAPABILITIES = CAPABILITIES - {"repository.create"}
PERMISSION_LEVEL_ORDER = {"read": 1, "write": 2}


class CapabilityDiscoveryError(ValueError):
    """Raised when provider capability metadata cannot be trusted."""


@dataclass(frozen=True)
class CapabilityResult:
    capability: str
    status: str
    reason: str


def _normalize_repository(value: str) -> str:
    normalized = value.strip()
    parts = normalized.split("/")
    if len(parts) != 2 or not all(parts) or any(part in {".", ".."} for part in parts):
        raise CapabilityDiscoveryError("GITHUB_CAPABILITY_UNCONFIRMED: invalid repository scope")
    return f"{parts[0]}/{parts[1]}"


def normalize_provider_permissions(raw: Mapping[str, str]) -> tuple[tuple[str, str], ...]:
    if not isinstance(raw, Mapping):
        raise CapabilityDiscoveryError("GITHUB_CAPABILITY_UNCONFIRMED")
    normalized: list[tuple[str, str]] = []
    for name, level in raw.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(level, str) or not level.strip():
            raise CapabilityDiscoveryError("GITHUB_CAPABILITY_UNCONFIRMED")
        normalized.append((name.strip(), level.strip().lower()))
    return tuple(sorted(normalized))


def normalize_repository_scope(scope: Sequence[str]) -> tuple[str, ...]:
    if isinstance(scope, str):
        raise CapabilityDiscoveryError("GITHUB_CAPABILITY_UNCONFIRMED: repository_scope must be a sequence")
    return tuple(sorted({_normalize_repository(repo) for repo in scope}))


def evaluate_capability(
    capability: str,
    *,
    provider_permissions: Mapping[str, str],
    required_permissions: Mapping[str, Mapping[str, str]],
    target_repository: str | None = None,
    repository_scope: Sequence[str] = (),
) -> CapabilityResult:
    if capability not in CAPABILITIES:
        raise CapabilityDiscoveryError(f"UNSUPPORTED_DEVOS_CAPABILITY:{capability}")

    permissions = dict(normalize_provider_permissions(provider_permissions))

    if capability in EXISTING_REPOSITORY_CAPABILITIES:
        if not target_repository:
            return CapabilityResult(capability, "UNCONFIRMED", "TARGET_REPOSITORY_REQUIRED")
        target = _normalize_repository(target_repository)
        allowed_repositories = set(normalize_repository_scope(repository_scope))
        if target not in allowed_repositories:
            return CapabilityResult(capability, "UNAVAILABLE", "TARGET_REPOSITORY_OUTSIDE_SCOPE")

    required = required_permissions.get(capability)
    if required is None:
        return CapabilityResult(capability, "UNCONFIRMED", "PROVIDER_MAPPING_REQUIRED")
    if not isinstance(required, Mapping) or not required:
        return CapabilityResult(capability, "UNCONFIRMED", "PROVIDER_MAPPING_INVALID")

    for name, required_level in sorted(required.items()):
        if not isinstance(name, str) or not name.strip() or not isinstance(required_level, str) or not required_level.strip():
            return CapabilityResult(capability, "UNCONFIRMED", "PROVIDER_MAPPING_INVALID")
        permission_name = name.strip()
        minimum_level = required_level.strip().lower()
        actual_level = permissions.get(permission_name)
        if actual_level is None:
            return CapabilityResult(capability, "UNAVAILABLE", f"MISSING_PROVIDER_PERMISSION:{permission_name}")
        if minimum_level not in PERMISSION_LEVEL_ORDER or actual_level not in PERMISSION_LEVEL_ORDER:
            return CapabilityResult(capability, "UNCONFIRMED", f"PERMISSION_LEVEL_UNCONFIRMED:{permission_name}")
        if PERMISSION_LEVEL_ORDER[actual_level] < PERMISSION_LEVEL_ORDER[minimum_level]:
            return CapabilityResult(
                capability,
                "UNAVAILABLE",
                f"INSUFFICIENT_PROVIDER_PERMISSION_LEVEL:{permission_name}:{actual_level}<{minimum_level}",
            )

    return CapabilityResult(capability, "AVAILABLE", "PROVIDER_PERMISSIONS_AND_SCOPE_SATISFY_MAPPING")


def evaluate_capabilities(
    capabilities: Sequence[str],
    *,
    provider_permissions: Mapping[str, str],
    required_permissions: Mapping[str, Mapping[str, str]],
    target_repository: str | None = None,
    repository_scope: Sequence[str] = (),
) -> tuple[CapabilityResult, ...]:
    return tuple(
        evaluate_capability(
            capability,
            provider_permissions=provider_permissions,
            required_permissions=required_permissions,
            target_repository=target_repository,
            repository_scope=repository_scope,
        )
        for capability in capabilities
    )


def safe_capability_metadata(
    *,
    provider: str,
    identity: str,
    permissions: Mapping[str, str],
    results: Sequence[CapabilityResult],
    target_repository: str | None = None,
    repository_scope: Sequence[str] = (),
) -> dict[str, object]:
    """Return durable capability metadata with no credential material."""
    return {
        "provider": provider,
        "identity": identity,
        "target_repository": _normalize_repository(target_repository) if target_repository else None,
        "repository_scope": list(normalize_repository_scope(repository_scope)),
        "provider_permissions": dict(normalize_provider_permissions(permissions)),
        "capabilities": [
            {"capability": result.capability, "status": result.status, "reason": result.reason}
            for result in results
        ],
        "credential_material": "NOT_INCLUDED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
    }


if __name__ == "__main__":
    sample = evaluate_capability(
        "file.update",
        provider_permissions={"contents": "write"},
        required_permissions={"file.update": {"contents": "write"}},
        target_repository="example/repo",
        repository_scope=("example/repo",),
    )
    print(sample)