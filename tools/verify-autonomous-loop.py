#!/usr/bin/env python3
"""Static contract checks for Autonomous Development Loop v1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def require(text: str, needle: str, source: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {needle!r} in {source}")

core = read("core/autonomous-development-loop.md")
workflow = read("workflows/autonomous-loop.md")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

for needle in [
    "bounded, evidence-driven, checkpointed, and stoppable",
    "Objective",
    "State resolution",
    "Plan / orchestrate",
    "Capability check",
    "Authorization check",
    "Checkpoint",
    "CONTINUE | STOP | ESCALATE",
    "AVAILABLE",
    "DELEGATABLE",
    "MISSING",
    "maximum iteration count",
    "Production-impacting, destructive, irreversible, security-sensitive, or data-affecting",
    "ESCALATE",
    "checkpoint",
    "Observed",
    "Likely",
    "Unknown",
    "VERIFIED",
    "PARTIAL",
    "UNVERIFIED",
    "FAILED",
    "never blindly replay",
    "never automatically repeated",
    "does not provide unrestricted autonomous software development",
]:
    require(core, needle, "core/autonomous-development-loop.md")

for needle in [
    "AI State Resolver",
    "Agent Orchestration",
    "capabilities",
    "authorization",
    "checkpoint",
    "Verification",
    "Security Gate",
    "CONTINUE",
    "STOP",
    "ESCALATE",
    "never blindly replay",
]:
    require(workflow, needle, "workflows/autonomous-loop.md")

for needle in [
    "P4 — Autonomous Development Loop",
    "[x] Define autonomous-loop lifecycle and bounded iteration",
    "[x] Define stop/continue/escalation conditions",
    "[x] Connect orchestration outputs to executable workflow steps",
    "[x] Define capability checks and honest delegation when a host lacks tools",
    "[x] Define checkpointing and resumability between iterations",
    "[x] Define approval gates for high-risk actions",
    "[x] Define end-to-end evidence aggregation",
    "[x] Build contract verification harness and CI integration",
]:
    require(roadmap, needle, "docs/ROADMAP.md")

require(architecture, "Autonomous Development Loop", "docs/ARCHITECTURE.md")
require(architecture, "bounded", "docs/ARCHITECTURE.md")
require(architecture, "CONTINUE", "docs/ARCHITECTURE.md")
require(architecture, "STOP", "docs/ARCHITECTURE.md")
require(architecture, "ESCALATE", "docs/ARCHITECTURE.md")
require(architecture, "capability", "docs/ARCHITECTURE.md")
require(architecture, "checkpoint", "docs/ARCHITECTURE.md")

print("Autonomous Development Loop v1 contract checks passed.")
