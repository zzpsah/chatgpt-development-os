#!/usr/bin/env python3
"""Simulate first contact by an AI with no prior chat/account memory."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    Path("AGENTS.md"),
    Path(".ai/manifest.yaml"),
    Path(".ai/CURRENT-STATE.md"),
    Path(".ai/TASKS.md"),
    Path(".ai/DECISIONS.md"),
    Path("core/ai-bootstrap-protocol.md"),
    Path("docs/DEVOS-STANCE-CODES.md"),
    Path("docs/CROSS-AI-HANDSHAKE.md"),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def main() -> None:
    for path in REQUIRED:
        require((ROOT / path).is_file(), f"missing recovery source: {path}")

    agents = text(Path("AGENTS.md"))
    current = text(Path(".ai/CURRENT-STATE.md"))
    tasks = text(Path(".ai/TASKS.md"))
    decisions = text(Path(".ai/DECISIONS.md"))
    manifest = text(Path(".ai/manifest.yaml"))
    stance = text(Path("docs/DEVOS-STANCE-CODES.md"))

    require("source tree + Git" in current or "Git" in current, "current-state must identify implementation authority")
    require("ChatGPT Memory" in current or "chat history" in current, "current-state must preserve account-memory boundary")
    require("P11" in current and "P11" in tasks, "fresh AI must be able to recover current milestone")
    require("## Active" in tasks, "fresh AI must recover active work")
    require("revalidation" in stance.lower(), "stance contract must require repository revalidation")
    require("Recovery precedence" in text(Path("docs/P11-FEDERATION-SELF-HEALING.md")), "P11 must define recovery precedence")

    manifest_project = re.search(r"^project_id:\s*(.+)$", manifest, flags=re.MULTILINE)
    manifest_name = re.search(r"^name:\s*(.+)$", manifest, flags=re.MULTILINE)
    require(manifest_project is not None, "manifest project_id is missing")
    require(manifest_name is not None, "manifest name is missing")
    require("P9" in decisions and "P10" in decisions, "decision history must preserve prior milestone context")
    require(git_head(), "Git HEAD must be recoverable")
    require("DEVOS::GOD" in agents and "DEVOS::GOD::DESI" in stance, "preferred DevOS stance must be discoverable")

    print("PASS: fresh-AI recovery sources are present")
    print("PASS: project identity and current milestone are recoverable")
    print("PASS: active work and decision history are recoverable")
    print("PASS: account-memory/chat-history boundary is explicit")
    print("PASS: preferred GOD+DESI stance is discoverable")
    print("PASS: recovery can begin from repository evidence alone")


if __name__ == "__main__":
    main()
