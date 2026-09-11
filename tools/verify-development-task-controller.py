#!/usr/bin/env python3
"""Static contract verification for the P9 Development Task Controller."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, needles: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {path}"


require("core/development-task-controller.md", [
    "Development Task Controller v1",
    "User request",
    "Project + intent resolution",
    "Durable state resolution",
    "Orchestration / work units",
    "Capability + authorization checks",
    "Bounded execution",
    "Verification",
    "Security review",
    "Durable state persistence",
    "Final evidence-backed outcome",
    "P11 repository-first recovery",
    "P11 derived-context self-healing",
    "provenance-aware handoff",
    "repository revalidation",
    "COMPLETE",
    "BLOCKED",
    "ESCALATED",
    "actual execution",
    "Remote Mutation Controls",
])

require("workflows/development-task.md", [
    "Development Task Workflow v1",
    "Normalize the user's request",
    "Load durable context",
    "P11 repository-first recovery",
    "context freshness/integrity",
    "acceptance criteria",
    "execution budget",
    "capability and authorization",
    "actual changes and evidence",
    "P11 self-healing",
    "repository revalidation",
    "Run applicable verification",
    "Security Gate",
    "COMPLETE",
    "BLOCKED",
    "FAILED",
    "ESCALATED",
])

print("Development Task Controller v1 contract: PASS")
print("P11 recovery/self-healing lifecycle integration: PASS")
