#!/usr/bin/env python3
"""Resolve DevOS recovery precedence without treating AI memory as authority."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / ".ai"

@dataclass(frozen=True)
class Evidence:
    source: str
    available: bool
    authority: str
    notes: str

PRECEDENCE = (
    ("source+git", "implementation", "authoritative for exact implementation state"),
    ("requirements+decisions", "intent", "authoritative for intentional project requirements/decisions"),
    ("ai-state", "context", "durable project context and handoff"),
    ("generated-index", "navigation", "derived evidence/navigation only"),
    ("ai-memory", "supplementary", "never authoritative; must be revalidated"),
)


def collect() -> list[Evidence]:
    return [
        Evidence("source+git", (ROOT / ".git").exists(), "implementation", "inspect actual tree and Git history"),
        Evidence("requirements+decisions", (CONTEXT / "DECISIONS.md").exists(), "intent", "use explicit decisions/requirements"),
        Evidence("ai-state", (CONTEXT / "CURRENT-STATE.md").exists() and (CONTEXT / "TASKS.md").exists(), "context", "durable project state"),
        Evidence("generated-index", (CONTEXT / "STATE-INDEX.md").exists(), "navigation", "derived and re-creatable"),
        Evidence("ai-memory", False, "supplementary", "account/chat memory is not repository evidence"),
    ]


def resolve() -> dict:
    evidence = collect()
    conflicts: list[str] = []
    for item in evidence:
        if item.source == "ai-memory":
            continue
        if item.available:
            continue
    if not evidence[0].available:
        conflicts.append("implementation source/Git evidence is unavailable")
    if evidence[3].available and not evidence[2].available:
        conflicts.append("generated index exists without durable semantic AI state")
    return {
        "precedence": [name for name, _, _ in PRECEDENCE],
        "evidence": [item.__dict__ for item in evidence],
        "conflicts": conflicts,
        "action": "PROCEED_WITH_SOURCE_AND_GIT" if not conflicts else "ESCALATE_REVIEW",
    }


def main() -> None:
    result = resolve()
    print("RECOVERY PRECEDENCE")
    for idx, (name, authority, note) in enumerate(PRECEDENCE, 1):
        print(f"{idx}. {name} [{authority}] — {note}")
    print(f"ACTION: {result['action']}")
    if result["conflicts"]:
        for conflict in result["conflicts"]:
            print(f"CONFLICT: {conflict}")


if __name__ == "__main__":
    main()
