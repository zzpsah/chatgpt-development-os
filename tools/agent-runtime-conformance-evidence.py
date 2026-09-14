#!/usr/bin/env python3
"""Deterministic intake for agent-runtime conformance evidence.

This tool creates a challenge bound to one runtime/head/nonce and validates a
returned evidence packet. A valid packet is still only candidate evidence: this
tool never invokes a runtime, upgrades a registry entry, grants authorization,
mutates a repository, or changes production readiness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

CHALLENGE_PROTOCOL = "DEVOS-AGENT-RUNTIME-CONFORMANCE-CHALLENGE-v1"
EVIDENCE_PROTOCOL = "DEVOS-AGENT-RUNTIME-CONFORMANCE-EVIDENCE-v1"
VERDICT_PROTOCOL = "DEVOS-AGENT-RUNTIME-CONFORMANCE-VERDICT-v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_CAPABILITIES = {
    "filesystem.read",
    "filesystem.write_scoped",
    "git.inspect",
    "verification.run",
}
BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "production_ready": False,
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _blocked(reasons: list[str], challenge_id: str | None = None) -> dict[str, Any]:
    return {
        "protocol": VERDICT_PROTOCOL,
        "status": "BLOCKED",
        "reasons": sorted(set(reasons)),
        "challenge_id": challenge_id,
        "registry_promotion_allowed": False,
        "direct_runtime_verified": False,
        **BOUNDARIES,
    }


def create_challenge(runtime_id: Any, adapter_version: Any, repository_head: Any, nonce: Any) -> dict[str, Any]:
    reasons: list[str] = []
    if not _text(runtime_id):
        reasons.append("RUNTIME_ID_INVALID")
    if not _text(adapter_version):
        reasons.append("ADAPTER_VERSION_INVALID")
    if not _text(repository_head) or not SHA40.fullmatch(str(repository_head)):
        reasons.append("REPOSITORY_HEAD_INVALID")
    if not _text(nonce):
        reasons.append("NONCE_INVALID")
    if reasons:
        return {
            "protocol": CHALLENGE_PROTOCOL,
            "status": "BLOCKED",
            "reasons": sorted(set(reasons)),
            "challenge_id": None,
            "challenge": None,
            **BOUNDARIES,
        }

    challenge = {
        "protocol": CHALLENGE_PROTOCOL,
        "runtime_id": str(runtime_id).strip(),
        "adapter_version": str(adapter_version).strip(),
        "repository_head": str(repository_head),
        "nonce": str(nonce).strip(),
        "required_capabilities": sorted(REQUIRED_CAPABILITIES),
    }
    challenge_id = _digest(challenge)
    return {
        "protocol": CHALLENGE_PROTOCOL,
        "status": "CHALLENGE_READY",
        "reasons": ["EXACT_RUNTIME_HEAD_NONCE_CHALLENGE_BOUND"],
        "challenge_id": challenge_id,
        "challenge": challenge,
        **BOUNDARIES,
    }


def _validate_challenge_bundle(bundle: Any) -> tuple[list[str], dict[str, Any] | None, str | None]:
    if not isinstance(bundle, dict):
        return ["CHALLENGE_BUNDLE_NOT_OBJECT"], None, None
    allowed = {
        "protocol", "status", "reasons", "challenge_id", "challenge",
        "authority", "authorization", "execution", "mutation", "production_ready",
    }
    reasons: list[str] = []
    if set(bundle) != allowed:
        reasons.append("CHALLENGE_BUNDLE_FIELDS_INVALID")
    if bundle.get("protocol") != CHALLENGE_PROTOCOL:
        reasons.append("CHALLENGE_BUNDLE_PROTOCOL_INVALID")
    if bundle.get("status") != "CHALLENGE_READY":
        reasons.append("CHALLENGE_NOT_READY")
    if any(bundle.get(key) != value for key, value in BOUNDARIES.items()):
        reasons.append("CHALLENGE_BOUNDARY_CHANGED")
    challenge = bundle.get("challenge")
    challenge_id = bundle.get("challenge_id")
    if not isinstance(challenge, dict):
        reasons.append("CHALLENGE_NOT_OBJECT")
        return reasons, None, challenge_id if isinstance(challenge_id, str) else None
    expected_fields = {
        "protocol", "runtime_id", "adapter_version", "repository_head", "nonce", "required_capabilities"
    }
    if set(challenge) != expected_fields:
        reasons.append("CHALLENGE_FIELDS_INVALID")
    if challenge.get("protocol") != CHALLENGE_PROTOCOL:
        reasons.append("CHALLENGE_PROTOCOL_INVALID")
    if not _text(challenge.get("runtime_id")):
        reasons.append("CHALLENGE_RUNTIME_ID_INVALID")
    if not _text(challenge.get("adapter_version")):
        reasons.append("CHALLENGE_ADAPTER_VERSION_INVALID")
    if not _text(challenge.get("repository_head")) or not SHA40.fullmatch(challenge.get("repository_head", "")):
        reasons.append("CHALLENGE_REPOSITORY_HEAD_INVALID")
    if not _text(challenge.get("nonce")):
        reasons.append("CHALLENGE_NONCE_INVALID")
    if challenge.get("required_capabilities") != sorted(REQUIRED_CAPABILITIES):
        reasons.append("CHALLENGE_CAPABILITY_SET_INVALID")
    if not isinstance(challenge_id, str) or not SHA256.fullmatch(challenge_id):
        reasons.append("CHALLENGE_ID_INVALID")
    elif _digest(challenge) != challenge_id:
        reasons.append("CHALLENGE_INTEGRITY_INVALID")
    return reasons, challenge, challenge_id if isinstance(challenge_id, str) else None


def evaluate_evidence(challenge_bundle: Any, evidence: Any) -> dict[str, Any]:
    reasons, challenge, challenge_id = _validate_challenge_bundle(challenge_bundle)
    if reasons or challenge is None:
        return _blocked(reasons or ["CHALLENGE_INVALID"], challenge_id)
    if not isinstance(evidence, dict):
        return _blocked(["EVIDENCE_NOT_OBJECT"], challenge_id)

    allowed_fields = {
        "protocol", "challenge_id", "runtime_id", "adapter_version", "repository_head", "nonce",
        "invocation_provenance", "capabilities", "limitations",
    }
    if set(evidence) != allowed_fields:
        reasons.append("EVIDENCE_FIELDS_INVALID")
    if evidence.get("protocol") != EVIDENCE_PROTOCOL:
        reasons.append("EVIDENCE_PROTOCOL_INVALID")
    for field in ("challenge_id", "runtime_id", "adapter_version", "repository_head", "nonce"):
        expected = challenge_id if field == "challenge_id" else challenge[field]
        if evidence.get(field) != expected:
            reasons.append("EVIDENCE_" + field.upper() + "_MISMATCH")

    provenance = evidence.get("invocation_provenance")
    if not isinstance(provenance, dict) or set(provenance) != {"kind", "ref", "observed_by"}:
        reasons.append("INVOCATION_PROVENANCE_INVALID")
    elif any(not _text(provenance.get(field)) for field in ("kind", "ref", "observed_by")):
        reasons.append("INVOCATION_PROVENANCE_INVALID")

    caps = evidence.get("capabilities")
    failed_caps: list[str] = []
    if not isinstance(caps, dict):
        reasons.append("CAPABILITIES_INVALID")
    else:
        if set(caps) != REQUIRED_CAPABILITIES:
            reasons.append("CAPABILITY_SET_INVALID")
        for name in sorted(REQUIRED_CAPABILITIES):
            item = caps.get(name)
            if not isinstance(item, dict) or set(item) != {"status", "ref", "scope", "digest"}:
                reasons.append("CAPABILITY_EVIDENCE_INVALID=" + name)
                continue
            if item.get("status") not in {"PASS", "FAIL"}:
                reasons.append("CAPABILITY_STATUS_INVALID=" + name)
            elif item["status"] != "PASS":
                failed_caps.append(name)
            if not _text(item.get("ref")) or not _text(item.get("scope")):
                reasons.append("CAPABILITY_REFERENCE_INVALID=" + name)
            digest = item.get("digest")
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                reasons.append("CAPABILITY_DIGEST_INVALID=" + name)

    limitations = evidence.get("limitations")
    if not isinstance(limitations, list) or not limitations or any(not _text(item) for item in limitations):
        reasons.append("LIMITATIONS_INVALID")

    if reasons:
        return _blocked(reasons, challenge_id)
    if failed_caps:
        return {
            "protocol": VERDICT_PROTOCOL,
            "status": "HOLD",
            "reasons": ["CAPABILITY_PROBE_FAILED=" + ",".join(sorted(failed_caps))],
            "challenge_id": challenge_id,
            "evidence_digest": _digest(evidence),
            "registry_promotion_allowed": False,
            "direct_runtime_verified": False,
            **BOUNDARIES,
        }

    return {
        "protocol": VERDICT_PROTOCOL,
        "status": "EVIDENCE_PACKET_VALID",
        "reasons": [
            "CHALLENGE_BOUND_CAPABILITY_PACKET_VALID",
            "DIRECT_INVOCATION_ATTESTATION_AND_SEMANTIC_REVIEW_STILL_REQUIRED",
        ],
        "challenge_id": challenge_id,
        "evidence_digest": _digest(evidence),
        "runtime_id": challenge["runtime_id"],
        "capabilities": sorted(REQUIRED_CAPABILITIES),
        "registry_promotion_allowed": False,
        "direct_runtime_verified": False,
        **BOUNDARIES,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    challenge_parser = sub.add_parser("challenge")
    challenge_parser.add_argument("--runtime-id", required=True)
    challenge_parser.add_argument("--adapter-version", required=True)
    challenge_parser.add_argument("--repository-head", required=True)
    challenge_parser.add_argument("--nonce", required=True)

    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("challenge")
    verify_parser.add_argument("evidence")

    args = parser.parse_args()
    if args.command == "challenge":
        result = create_challenge(args.runtime_id, args.adapter_version, args.repository_head, args.nonce)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "CHALLENGE_READY" else 2

    challenge_bundle = json.loads(Path(args.challenge).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    verdict = evaluate_evidence(challenge_bundle, evidence)
    print(json.dumps(verdict, indent=2, sort_keys=True))
    return 0 if verdict["status"] == "EVIDENCE_PACKET_VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
