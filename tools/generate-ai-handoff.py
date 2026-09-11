#!/usr/bin/env python3
"""Generate a vendor-neutral, provenance-aware DevOS AI handoff packet."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / ".ai"
OUT = CONTEXT / "AI-HANDOFF.json"


def extract_section(text: str, heading: str) -> list[str]:
    marker = f"## {heading}"
    if marker not in text:
        return []
    chunk = text.split(marker, 1)[1]
    chunk = chunk.split("\n## ", 1)[0]
    return [line[2:].strip() for line in chunk.splitlines() if line.startswith("- ") and line[2:].strip()]


def scalar_manifest(key: str) -> str:
    manifest = CONTEXT / "manifest.yaml"
    if not manifest.exists():
        return "UNKNOWN"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith(key + ":"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return "UNKNOWN"


def git_value(*args: str) -> str:
    # Git provenance is validated with: git rev-parse HEAD
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip() or "UNKNOWN"
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def main() -> None:
    current = (CONTEXT / "CURRENT-STATE.md").read_text(encoding="utf-8") if (CONTEXT / "CURRENT-STATE.md").exists() else ""
    tasks = (CONTEXT / "TASKS.md").read_text(encoding="utf-8") if (CONTEXT / "TASKS.md").exists() else ""
    decisions = (CONTEXT / "DECISIONS.md").read_text(encoding="utf-8") if (CONTEXT / "DECISIONS.md").exists() else ""

    evidence_refs = [
        "AGENTS.md",
        ".ai/manifest.yaml",
        ".ai/CURRENT-STATE.md",
        ".ai/TASKS.md",
        ".ai/DECISIONS.md",
        ".ai/STATE-INDEX.md",
        ".ai/SESSIONS/",
    ]

    payload = {
        "protocol_version": 1,
        "project_id": scalar_manifest("project_id"),
        "project_name": scalar_manifest("name"),
        "repository": scalar_manifest("repository"),
        "devos_context_version": scalar_manifest("context_version"),
        "current_objective": extract_section(current, "P11 status") or extract_section(current, "Snapshot"),
        "verified_state": [line for line in extract_section(current, "P10 status") + extract_section(current, "P9 status") if line],
        "active_work": extract_section(tasks, "Active"),
        "blocked_work": extract_section(tasks, "Blocked"),
        "recent_work": extract_section(tasks, "Completed recently")[-10:],
        "recommended_next_action": extract_section(current, "Immediate remaining focus")[-1:] or extract_section(tasks, "Active")[:1] or ["Read TASKS.md and inspect source/Git evidence before proceeding."],
        "evidence_refs": evidence_refs,
        "confidence": "high" if (CONTEXT / "manifest.yaml").exists() and (CONTEXT / "CURRENT-STATE.md").exists() else "low",
        "unknowns": ["Receiving AI must validate semantic conclusions against current source/Git."],
        "decision_context_available": bool(decisions),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_value("rev-parse", "HEAD"),
        "git_branch": git_value("branch", "--show-current"),
        "git_status": "clean" if git_value("status", "--porcelain") == "" else "dirty",
        "generated_from": {
            "manifest": ".ai/manifest.yaml",
            "current_state": ".ai/CURRENT-STATE.md",
            "tasks": ".ai/TASKS.md",
            "decisions": ".ai/DECISIONS.md",
            "git_commit": git_value("rev-parse", "HEAD"),
        },
        "revalidation": {
            "required_when": [
                "handoff git_commit differs from current HEAD",
                "confidence is not high",
                "semantic decisions changed",
            ],
            "instruction": "Validate material conclusions against current source and Git before acting.",
        },
    }

    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT}")
    print("HANDSHAKE: READY" if payload["confidence"] == "high" else "HANDSHAKE: NEEDS_REVIEW")


if __name__ == "__main__":
    main()
