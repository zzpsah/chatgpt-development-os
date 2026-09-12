#!/usr/bin/env python3
"""Execute only P14 AUTO_ELIGIBLE deterministic derived-context healing."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_policy() -> Any:
    spec = importlib.util.spec_from_file_location("adaptive_verification", ROOT / "tools" / "adaptive-verification.py")
    if spec is None or spec.loader is None:
        raise ImportError("could not load adaptive-verification.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["adaptive_verification"] = module
    spec.loader.exec_module(module)
    return module


def execute(project_root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    policy = load_policy()
    decision = policy.evaluate(payload)
    healing = decision["healing"]
    if healing["decision"] != "AUTO_ELIGIBLE":
        return {
            "protocol": "P14-ADAPTIVE-SELF-HEAL-v1",
            "status": "NOT_EXECUTED",
            "reason": healing["reason"],
            "policy": decision,
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    target = Path(str(healing.get("target") or ""))
    basename = target.name
    if basename not in policy.DERIVED_CONTEXT:
        raise AssertionError("policy/executor allowlist mismatch")
    if not (project_root / ".git").exists():
        return {
            "protocol": "P14-ADAPTIVE-SELF-HEAL-v1",
            "status": "BLOCKED",
            "reason": "PROJECT_ROOT_IS_NOT_A_GIT_WORKTREE",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    env = os.environ.copy()
    env["DEVOS_SELF_HEAL_FILES"] = basename
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "self-heal-derived-context.py")],
        cwd=project_root,
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return {
            "protocol": "P14-ADAPTIVE-SELF-HEAL-v1",
            "status": "FAILED",
            "reason": "DERIVED_CONTEXT_HEAL_COMMAND_FAILED",
            "exit_status": result.returncode,
            "stderr": result.stderr.strip(),
            "authority": "UNCHANGED",
            "execution": "FAILED",
            "reverification_required": True,
        }
    return {
        "protocol": "P14-ADAPTIVE-SELF-HEAL-v1",
        "status": "HEALED_PENDING_REVERIFY",
        "target": str(healing["target"]),
        "tool": healing["allowed_tool"],
        "stdout": result.stdout.strip(),
        "authority": "UNCHANGED",
        "execution": "COMPLETED",
        "reverification_required": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--payload", required=True, help="JSON P14 policy payload")
    args = parser.parse_args()
    output = execute(Path(args.project_root).resolve(), json.loads(args.payload))
    print(json.dumps(output, sort_keys=True))
    return 0 if output["status"] in {"HEALED_PENDING_REVERIFY", "NOT_EXECUTED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
