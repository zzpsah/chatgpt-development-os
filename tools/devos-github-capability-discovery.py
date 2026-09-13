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


class CapabilityDiscoveryError(ValueError):
    """Raised when provider capability metadata cannot be trusted."""


@dataclass(frozen=True)
class CapabilityResult:
    capability: str
    status: str
    reason: str


def normalize_provider_permissions(raw: Mapping[str, str]) -> tuple[tuple[str, str], ...]:
    if not isinstance(raw, Mapping):
        raise CapabilityDiscoveryError("GITHUB_CAPABILITY_UNCONFIRMED")
    normalized: list[tuple[str, str]] = []
    for name, level in raw.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(level, str):
            raise CapabilityDiscoveryError("GITHUB_CAPABILITY_UNCONFIRMED")
        normalized.append((name.strip(), level.strip()))
    return tuple(sorted(normalized))


def evaluate_capability(
    capability: str,
    *,
    provider_permissions: Mapping[str, str],
    required_permissions: Mapping[str, Sequence[str]],
) -> CapabilityResult:
    if capability not in CAPABILITIES:
        raise CapabilityDiscoveryError(f"UNSUPPORTED_DEVOS_CAPABILITY:{capability}")

    permissions = dict(normalize_provider_permissions(provider_permissions))
    required = required_permissions.get(capability)
    if required is None:
        return CapabilityResult(capability, "UNCONFIRMED", "PROVIDER_MAPPING_REQUIRED")

    missing = [name for name in required if name not in permissions]
    if missing:
        return CapabilityResult(capability, "UNAVAILABLE", "MISSING_PROVIDER_PERMISSIONS:" + ",".join(sorted(missing)))

    return CapabilityResult(capability, "AVAILABLE", "PROVIDER_PERMISSIONS_SATISFY_MAPPING")


def evaluate_capabilities(
    capabilities: Sequence[str],
    *,
    provider_permissions: Mapping[str, str],
    required_permissions: Mapping[str, Sequence[str]],
) -> tuple[CapabilityResult, ...]:
    return tuple(
        evaluate_capability(
            capability,
            provider_permissions=provider_permissions,
            required_permissions=required_permissions,
        )
        for capability in capabilities
    )


def safe_capability_metadata(
    *,
    provider: str,
    identity: str,
    permissions: Mapping[str, str],
    results: Sequence[CapabilityResult],
) -> dict[str, object]:
    """Return durable capability metadata with no credential material."""
    return {
        "provider": provider,
        "identity": identity,
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
        required_permissions={"file.update": ("contents",)},
    )
    print(sample)
