#!/usr/bin/env python3
"""Read-only verification of the DevOS living documentation surface."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_MASTER_MAP = ROOT / "docs/DEVOS-MASTER-ENGINEERING-MAP.md"
LEGACY_MASTER_MAPS = [
    ROOT / "docs/DEVOS-MASTER-ENGINEERING-MAP-v2.md",
]
REQUIRED = {
    "master_map": CANONICAL_MASTER_MAP,
    "roadmap": ROOT / "docs/ROADMAP.md",
    "evolution_contract": ROOT / "core/devos-living-state-and-evolution.md",
    "experiment_ledger": ROOT / "docs/DEVOS-INTERPRETER-EXPERIMENT-LEDGER.md",
    "handoff": ROOT / "docs/handoff/README.md",
    "current_state": ROOT / ".ai/CURRENT-STATE.md",
    "tasks": ROOT / ".ai/TASKS.md",
    "decisions": ROOT / ".ai/DECISIONS.md",
}
MARKERS = {
    "master_map": [
        "# DevOS Master Engineering Map",
        "What is not written was never done.",
        "IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE",
        "Human Language Interpreter evolution",
        "Self-maintaining knowledge model",
        "Every-AI maintenance contract",
    ],
    "roadmap": [
        "# Development OS Roadmap",
        "### P14 — Adaptive Verification & Self-Healing — COMPLETE",
        "### P15 — Human Language Interpretation v2 — COMPLETE",
        "### P16 — Semantic Goal-to-Plan Compiler — COMPLETE",
        "### P17 — Step Readiness & Authorization Orchestrator — COMPLETE",
        "No numbered feature milestone is currently active.",
        "production_ready = false",
    ],
    "evolution_contract": [
        "# DevOS Living State & Evolution Contract",
        "core/documentation-integrity.md",
        "does not redefine, replace, weaken, or independently compete",
        "What is not written was never done.",
        "Source-of-truth precedence",
        "Automatic vs semantic documentation",
        "Human Language Interpreter evolution",
        "LEARNING != AUTHORIZATION",
    ],
    "experiment_ledger": [
        "# DevOS Interpreter Experiment Ledger",
        "experiment_id",
        "ADOPT|REJECT|DEFER",
        "INTERPRETATION != AUTHORIZATION",
    ],
    "handoff": ["DevOS AI handoff index", "Master Engineering Map", "Interpreter Experiment Ledger"],
    "current_state": ["# Current State", "Core documentation law", "Canonical governed path"],
    "tasks": ["# DevOS Tasks", "What is not written was never done.", "Core safety invariants"],
    "decisions": ["# DevOS Decisions", "What is not written was never done.", "P15 Human Language Interpretation"],
}
FORBIDDEN_MARKERS = {
    "roadmap": [
        "### P14 — Adaptive Verification & Self-Healing — PLANNED",
        "P14 starts from the verified P13 execution-feedback boundary.",
    ],
}


def main() -> int:
    failures = []

    for legacy in LEGACY_MASTER_MAPS:
        if legacy.exists():
            failures.append(
                "duplicate canonical master-map surface: "
                f"{legacy.relative_to(ROOT)} exists alongside {CANONICAL_MASTER_MAP.relative_to(ROOT)}"
            )

    for name, path in REQUIRED.items():
        if not path.exists():
            failures.append(f"{name}: missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in MARKERS[name]:
            if marker not in text:
                failures.append(f"{name}: missing marker {marker!r}")
        for marker in FORBIDDEN_MARKERS.get(name, []):
            if marker in text:
                failures.append(f"{name}: stale/forbidden marker present {marker!r}")

    if failures:
        print("LIVING-DOCS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("LIVING-DOCS: PASS")
    print(
        "Exactly one canonical master map is present; roadmap stage status, living-state delegation, "
        "interpreter experiments, handoff links, and durable-state documentation law are present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
