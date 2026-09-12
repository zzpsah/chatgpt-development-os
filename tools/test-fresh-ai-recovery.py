#!/usr/bin/env python3
"""Simulate first contact by an AI with no prior chat/account memory."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"
CANONICAL_URL = "https://github.com/zzpsah/chatgpt-development-os"

REQUIRED = [
    Path("AGENTS.md"),
    Path(".ai/manifest.yaml"),
    Path(".ai/CURRENT-STATE.md"),
    Path(".ai/TASKS.md"),
    Path(".ai/DECISIONS.md"),
    Path("core/ai-bootstrap-protocol.md"),
    Path("core/project-router.md"),
    Path("projects/registry.md"),
    Path("docs/DEVOS-STANCE-CODES.md"),
    Path("docs/CROSS-AI-HANDSHAKE.md"),
    Path("docs/P11-FEDERATION-SELF-HEALING.md"),
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
    router = text(Path("core/project-router.md"))
    registry = text(Path("projects/registry.md"))
    stance = text(Path("docs/DEVOS-STANCE-CODES.md"))
    federation = text(Path("docs/P11-FEDERATION-SELF-HEALING.md"))

    require("source tree + Git" in current or "Git" in current, "current-state must identify implementation authority")
    require("ChatGPT Memory" in current or "chat history" in current, "current-state must preserve account-memory boundary")
    require("P11" in current and "P11" in tasks, "fresh AI must be able to recover current milestone")
    require("## Active" in tasks, "fresh AI must recover active work")
    require("revalidation" in stance.lower(), "stance contract must require repository revalidation")
    require("repository revalidation" in federation.lower(), "fresh AI recovery must explicitly require repository revalidation")
    require("current source tree and Git" in federation, "repository revalidation must target current source tree and Git")
    require("Recovery precedence" in federation, "P11 must define recovery precedence")

    manifest_project = re.search(r"^project_id:\s*(.+)$", manifest, flags=re.MULTILINE)
    manifest_name = re.search(r"^name:\s*(.+)$", manifest, flags=re.MULTILINE)
    require(manifest_project is not None, "manifest project_id is missing")
    require(manifest_name is not None, "manifest name is missing")
    require(f"canonical_repository: {CANONICAL_REPOSITORY}" in manifest, "fresh AI must recover exact canonical DevOS repository from manifest")
    require(f"canonical_url: {CANONICAL_URL}" in manifest, "fresh AI must recover canonical DevOS URL from manifest")
    require("canonical_alias: DEVOS" in manifest, "fresh AI must recover DEVOS alias from manifest")
    require("DevOS / Development OS" in registry and CANONICAL_REPOSITORY in registry, "project registry must map DevOS alias to exact canonical repository")
    require("DEVOS" in router and CANONICAL_REPOSITORY in router, "Project Router must contain explicit DevOS canonical routing example")
    require(CANONICAL_REPOSITORY in agents, "AGENTS bootstrap must state exact canonical DevOS repository")
    require("name-only" in agents.lower() or "similar" in agents.lower(), "AGENTS bootstrap must reject name-only repository substitution")
    require("P9" in decisions and "P10" in decisions, "decision history must preserve prior milestone context")
    require(git_head(), "Git HEAD must be recoverable")
    require("DEVOS::GOD" in agents and "DEVOS::GOD::DESI" in stance, "preferred DevOS stance must be discoverable")

    print("PASS: fresh-AI recovery sources are present")
    print("PASS: DEVOS alias resolves to exact canonical repository from repository evidence alone")
    print("PASS: project identity and current milestone are recoverable")
    print("PASS: active work and decision history are recoverable")
    print("PASS: account-memory/chat-history boundary is explicit")
    print("PASS: repository revalidation against current source tree and Git is explicit")
    print("PASS: preferred GOD+DESI stance is discoverable")
    print("PASS: recovery can begin from repository evidence alone")


if __name__ == "__main__":
    main()
