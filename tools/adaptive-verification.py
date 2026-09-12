#!/usr/bin/env python3
"""P14 deterministic adaptive verification and bounded self-healing policy engine."""
from __future__ import annotations

import argparse
import json
from pathlib import PurePosixPath
from typing import Any

LEVEL_ORDER = ["STATIC", "UNIT", "INTEGRATION", "E2E", "RUNTIME", "DEPLOYMENT", "SECURITY"]
DERIVED_CONTEXT = {"STATE-INDEX.md", "CHANGELOG.md", "PROJECT-IDENTITY.json"}
SEMANTIC_CONTEXT = {"PROJECT.md", "DECISIONS.md", "TASKS.md", "CURRENT-STATE.md", "ARCHITECTURE.md"}
RISK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}


def normalize_paths(paths: Any) -> list[str]:
    if not isinstance(paths, list):
        return []
    return sorted({str(path).strip().replace("\\", "/") for path in paths if str(path).strip()})


def infer_required_levels(change: dict[str, Any]) -> list[str]:
    paths = normalize_paths(change.get("paths"))
    boundaries = {str(item).upper() for item in change.get("boundaries", []) if str(item).strip()}
    risk = str(change.get("risk", "LOW")).upper()
    required = {"STATIC"}

    code_ext = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cs", ".cpp", ".c", ".rb", ".php"}
    if any(PurePosixPath(path).suffix.lower() in code_ext for path in paths):
        required.add("UNIT")
    if boundaries & {"API", "DATABASE", "AUTH", "QUEUE", "EXTERNAL", "INTEGRATION"}:
        required.add("INTEGRATION")
    if boundaries & {"UI", "USER_FLOW", "E2E"}:
        required.add("E2E")
    if boundaries & {"RUNTIME", "SERVICE", "PROCESS"}:
        required.add("RUNTIME")
    if boundaries & {"DEPLOYMENT", "INFRASTRUCTURE"}:
        required.add("DEPLOYMENT")
    if boundaries & {"AUTH", "AUTHZ", "SECRETS", "SECURITY"}:
        required.add("SECURITY")

    if RISK.get(risk, 0) >= RISK["HIGH"]:
        required.add("INTEGRATION")
    if risk == "CRITICAL":
        required.update({"RUNTIME", "SECURITY"})

    return [level for level in LEVEL_ORDER if level in required]


def verification_status(required: list[str], evidence: Any) -> tuple[str, list[str], list[str]]:
    rows = evidence if isinstance(evidence, list) else []
    by_level: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        level = str(row.get("level", "")).upper()
        if level:
            by_level.setdefault(level, []).append(row)

    failed: list[str] = []
    missing: list[str] = []
    passed = 0
    for level in required:
        observations = by_level.get(level, [])
        if any(str(item.get("result", "")).upper() == "FAIL" for item in observations):
            failed.append(level)
            continue
        fresh_pass = any(
            str(item.get("result", "")).upper() == "PASS"
            and item.get("observed", True) is True
            and item.get("fresh", True) is True
            for item in observations
        )
        if fresh_pass:
            passed += 1
        else:
            missing.append(level)

    if failed:
        return "FAILED", failed, missing
    if not required or passed == len(required):
        return "VERIFIED", failed, missing
    if passed:
        return "PARTIAL", failed, missing
    return "UNVERIFIED", failed, missing


def healing_decision(payload: dict[str, Any], status: str) -> dict[str, Any]:
    repair = payload.get("repair") if isinstance(payload.get("repair"), dict) else {}
    kind = str(repair.get("kind", "NONE")).upper()
    target = str(repair.get("target", "")).replace("\\", "/")
    attempts = int(repair.get("attempts", 0) or 0)
    max_attempts = int(repair.get("max_attempts", 2) or 2)
    basename = PurePosixPath(target).name if target else ""

    base = {
        "authority": "UNCHANGED",
        "execution": "NONE",
        "attempts": attempts,
        "max_attempts": max_attempts,
        "target": target or None,
    }
    if status != "FAILED":
        return base | {"decision": "NO_HEAL", "reason": "VERIFICATION_NOT_FAILED"}
    if attempts >= max_attempts:
        return base | {"decision": "HOLD", "reason": "REPAIR_BUDGET_EXHAUSTED"}
    if basename in SEMANTIC_CONTEXT or kind in {"CODE", "CONFIG", "DATABASE", "DEPLOYMENT", "INFRASTRUCTURE", "SECURITY"}:
        return base | {"decision": "PROPOSE_ONLY", "reason": "SEMANTIC_OR_HIGHER_IMPACT_REPAIR_REQUIRES_CONTROLLER_GATE"}
    if kind == "DERIVED_CONTEXT" and basename in DERIVED_CONTEXT:
        return base | {
            "decision": "AUTO_ELIGIBLE",
            "reason": "DETERMINISTIC_DERIVED_CONTEXT_WITHIN_EXISTING_SELF_HEAL_BOUNDARY",
            "allowed_tool": "tools/self-heal-derived-context.py",
        }
    return base | {"decision": "HOLD", "reason": "REPAIR_NOT_IN_SAFE_AUTO_HEAL_ALLOWLIST"}


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    change = payload.get("change") if isinstance(payload.get("change"), dict) else {}
    required = infer_required_levels(change)
    status, failed, missing = verification_status(required, payload.get("evidence"))
    healing = healing_decision(payload, status)
    return {
        "protocol": "P14-ADAPTIVE-VERIFICATION-v1",
        "verification": {
            "status": status,
            "required_levels": required,
            "failed_levels": failed,
            "missing_levels": missing,
            "escalation": "REVERIFY_AFTER_REPAIR" if status == "FAILED" else ("GATHER_MISSING_EVIDENCE" if missing else "NONE"),
        },
        "healing": healing,
        "authority": "UNCHANGED",
        "execution": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", nargs="?", help="JSON payload; reads stdin when omitted")
    args = parser.parse_args()
    raw = args.payload if args.payload is not None else __import__("sys").stdin.read()
    payload = json.loads(raw or "{}")
    print(json.dumps(evaluate(payload), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
