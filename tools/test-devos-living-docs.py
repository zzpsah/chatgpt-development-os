#!/usr/bin/env python3
"""Read-only verification of the DevOS living documentation surface."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "master_map": ROOT / "docs/DEVOS-MASTER-ENGINEERING-MAP.md",
    "evolution_contract": ROOT / "core/devos-living-state-and-evolution.md",
    "experiment_ledger": ROOT / "docs/DEVOS-INTERPRETER-EXPERIMENT-LEDGER.md",
    "handoff": ROOT / "docs/handoff/README.md",
    "current_state": ROOT / ".ai/CURRENT-STATE.md",
    "tasks": ROOT / ".ai/TASKS.md",
    "decisions": ROOT / ".ai/DECISIONS.md",
}
MARKERS = {
    "master_map": ["# DevOS Master Engineering Map", "IMPLEMENTED + VERIFIED + DOCUMENTED", "INTERPRETATION != AUTHORIZATION", "Human Language Interpreter: evolution target", "Self-maintaining repository model"],
    "evolution_contract": ["# DevOS Living State & Evolution Contract", "Source-of-truth precedence", "Automatic vs semantic documentation", "Experiment loop", "LEARNING != AUTHORIZATION"],
    "experiment_ledger": ["# DevOS Interpreter Experiment Ledger", "experiment_id", "ADOPT|REJECT|DEFER", "INTERPRETATION != AUTHORIZATION"],
    "handoff": ["DevOS AI handoff index", "Master Engineering Map", "Interpreter Experiment Ledger"],
    "current_state": ["# Current State", "Canonical governed path"],
    "tasks": ["# DevOS Tasks", "Core safety invariants"],
    "decisions": ["# DevOS Decisions", "P15 Human Language Interpretation"],
}

def main() -> int:
    failures = []
    for name, path in REQUIRED.items():
        if not path.exists():
            failures.append(f"{name}: missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in MARKERS[name]:
            if marker not in text:
                failures.append(f"{name}: missing marker {marker!r}")
    if failures:
        print("LIVING-DOCS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("LIVING-DOCS: PASS")
    print("Canonical master map, evolution contract, experiment ledger, handoff links, and durable-state markers are present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
