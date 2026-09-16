#!/usr/bin/env python3
"""Small cross-platform DevOS command entry point.

The dispatcher uses explicit argv and delegates to existing tools. It creates no
new authorization or execution semantics; each delegated tool keeps its own gate.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
COMMANDS = {
    "doctor": ROOT / "tools" / "devos-doctor.py",
    "health": ROOT / "tools" / "devos-health.py",
    "bootstrap": ROOT / "tools" / "devos-bootstrap.py",
    "release-check": ROOT / "tools" / "devos-release-check.py",
    "project-lifecycle": ROOT / "tools" / "devos-project-lifecycle.py",
    "project-fleet": ROOT / "tools" / "devos-project-fleet.py",
    "project-remediation": ROOT / "tools" / "devos-project-remediation.py",
    "production-readiness": ROOT / "tools" / "verify-production-readiness-v2.py",
    "production-target-evidence": ROOT / "tools" / "production-target-evidence.py",
}


def version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def run_tool(command: str, argv: list[str]) -> int:
    script = COMMANDS[command]
    proc = subprocess.run([sys.executable, str(script), *argv], cwd=ROOT, check=False)
    return int(proc.returncode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="devos",
        description="DevOS repository CLI (safe dispatcher; delegated tools retain their own authority boundaries).",
    )
    parser.add_argument("--version", action="store_true", help="Print the canonical DevOS version.")
    parser.add_argument("command", nargs="?", choices=["version", *COMMANDS.keys()])
    parser.add_argument("args", nargs=argparse.REMAINDER)
    ns = parser.parse_args(argv)

    if ns.version or ns.command == "version":
        print(version())
        return 0
    if ns.command is None:
        parser.print_help()
        return 0
    return run_tool(ns.command, ns.args)


if __name__ == "__main__":
    raise SystemExit(main())
