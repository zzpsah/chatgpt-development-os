#!/usr/bin/env python3
"""Static contract checks for Executable Development Runtime v1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

core = read("core/execution-runtime.md")
workflow = read("workflows/execution-runtime.md")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

require(core, [
    "decision", "execution", "evidence",
    "PLANNED", "READY", "IN_PROGRESS", "BLOCKED", "COMPLETE", "FAILED", "CANCELLED",
    "AVAILABLE | DELEGATABLE | MISSING",
    "pre-action checkpoint", "post-action checkpoint",
    "never fabricate command output",
    "No authorization is created by the runtime",
    "Production, destructive, irreversible, security-sensitive, and data-affecting",
    "never blindly replay",
], "core/execution-runtime.md")

require(workflow, [
    "authorized work unit", "required capabilities", "pre-action checkpoint",
    "actual execution evidence", "post-action checkpoint", "verification",
    "Never blindly replay", "STOP/ESCALATE",
], "workflows/execution-runtime.md")

require(roadmap, [
    "P5 — Executable Development Runtime",
    "[x] Runtime execution contract",
    "[x] Work-unit execution and capability registry",
    "[x] Checkpoint and resume contract",
    "[x] Evidence capture and safety boundaries",
    "[x] Runtime workflow and verification harness",
], "docs/ROADMAP.md")

require(architecture, ["Executable Development Runtime", "checkpoint", "capability", "evidence"], "docs/ARCHITECTURE.md")

print("Executable Development Runtime v1 contract checks passed.")
