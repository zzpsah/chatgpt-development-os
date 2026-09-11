#!/usr/bin/env python3
"""Static contract checks for Agent Orchestration v1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, path):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {path}"

core = read("core/agent-orchestration.md")
workflow = read("workflows/orchestration.md")
roles = read("agents/roles.md")
arch = read("docs/ARCHITECTURE.md")
roadmap = read("docs/ROADMAP.md")

require(core, [
    "User intent", "Work decomposition", "Role selection", "Evidence handoff",
    "PLANNED | READY | IN_PROGRESS | BLOCKED | COMPLETE | FAILED",
    "Observed / Likely / Unknown", "production-impacting, destructive, irreversible",
    "Emotional urgency, profanity, or praise never grants authorization",
    "Verification / Test Engine remains authoritative",
    "Security Gate remains authoritative",
    "small recoverable failure",
], "core/agent-orchestration.md")

require(workflow, [
    "Project Router", "Human Language Execution Engine", "durable `.ai` context",
    "decompose the objective", "Parallelize read-only", "Serialize operations",
    "evidence packet", "Do not hide failed units", "COMPLETE",
], "workflows/orchestration.md")

require(roles, ["Planner", "Architect", "Developer", "Tester", "Security Reviewer", "Code Reviewer"], "agents/roles.md")
require(arch, ["Agent Orchestration", "coordinates work", "does not replace the existing safety"], "docs/ARCHITECTURE.md")
require(roadmap, ["### P3 — Agent Orchestration", "[x] Orchestration contract", "[x] Dependency and parallelism rules", "[x] Evidence handoff and failure recovery", "[x] Verification harness and CI integration"], "docs/ROADMAP.md")

print("Agent Orchestration v1 contract checks passed.")
