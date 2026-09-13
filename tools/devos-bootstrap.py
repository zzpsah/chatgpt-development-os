#!/usr/bin/env python3
"""Deterministic, read-only DevOS foundation bootstrap check."""

from __future__ import annotations

import argparse
from pathlib import Path

CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"
REQUIRED_FILES = (
    "AGENTS.md",
    ".ai/manifest.yaml",
    ".ai/CURRENT-STATE.md",
    "core/ai-bootstrap-protocol.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check(root: Path) -> tuple[bool, list[tuple[str, str]]]:
    results: list[tuple[str, str]] = []
    ok = True

    for rel in REQUIRED_FILES:
        exists = (root / rel).is_file()
        results.append((f"required:{rel}", "PASS" if exists else "HOLD"))
        ok &= exists

    if not ok:
        return False, results

    manifest = read(root / ".ai/manifest.yaml")
    identity_ok = (
        "project_id: chatgpt-development-os" in manifest
        and "canonical_repository: zzpsah/chatgpt-development-os" in manifest
        and "canonical_alias: DEVOS" in manifest
    )
    results.append(("canonical-identity", "PASS" if identity_ok else "HOLD"))
    ok &= identity_ok

    agents = read(root / "AGENTS.md")
    agents_ok = (
        "zzpsah/chatgpt-development-os" in agents
        and "core/ai-bootstrap-protocol.md" in agents
    )
    results.append(("agents-bootstrap-link", "PASS" if agents_ok else "HOLD"))
    ok &= agents_ok

    protocol = read(root / "core/ai-bootstrap-protocol.md")
    protocol_ok = (
        "project-portable continuity" in protocol
        and "repository evidence" in protocol.lower()
        and "Completion standard" in protocol
    )
    results.append(("bootstrap-protocol", "PASS" if protocol_ok else "HOLD"))
    ok &= protocol_ok

    state = read(root / ".ai/CURRENT-STATE.md")
    state_ok = "# Current State" in state and "Canonical governed path" in state
    results.append(("current-state", "PASS" if state_ok else "HOLD"))
    ok &= state_ok

    return ok, results


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only DevOS foundation bootstrap check")
    parser.add_argument("--root", default=".", help="DevOS repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    print("DEVOS FOUNDATION BOOTSTRAP v1")
    print(f"Repository root: {root}")
    print(f"Canonical repository: {CANONICAL_REPOSITORY}")
    print("--------------------------------")

    ok, results = check(root)
    for name, status in results:
        print(f"{status:5} {name}")

    print("--------------------------------")
    print(f"BOOTSTRAP STATUS: {'READY' if ok else 'HOLD'}")
    print("Execution authority: UNCHANGED")
    print("Mutation performed: NONE")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
