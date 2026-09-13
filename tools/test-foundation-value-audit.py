#!/usr/bin/env python3
"""Regression guard for the P0–P15 foundation value audit."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "P0-P15-FOUNDATION-VALUE-AUDIT.md"

required_phases = [f"P{i}" for i in range(16)]
required_sections = [
    "## P0–P7 — Foundational layer",
    "## P8–P12 — Operational control layer",
    "## P13–P15 — Integration and human interface layer",
    "## Cross-phase findings",
    "## Remediation completed by this audit",
    "## Next engineering gate",
]
allowed_dispositions = {
    "RETAIN",
    "RETAIN + CONSOLIDATE",
    "RETAIN + HARDEN",
    "RETAIN — CORE",
    "RETAIN + E2E HARDEN",
    "DEPRECATE",
}

text = AUDIT.read_text(encoding="utf-8")

for phase in required_phases:
    assert f"| {phase} |" in text, f"missing phase row: {phase}"
for section in required_sections:
    assert section in text, f"missing audit section: {section}"

rows = [line for line in text.splitlines() if line.startswith("| P")]
assert len(rows) == 16, f"expected 16 phase rows, found {len(rows)}"

for row in rows:
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    assert len(cells) == 5, f"malformed phase row: {row}"
    disposition = cells[4]
    assert disposition in allowed_dispositions, f"unknown disposition: {disposition}"

assert "DEPRECATE" not in "\n".join(rows), "deprecation must not be asserted without evidence"
assert "E2E HARDEN" in text, "audit must preserve the E2E maturity gap"
assert "Production E2E Harness" in text, "next engineering gate must include E2E harness"
assert "P16 final verification" in text and "P17 revalidation" in text

print("P0–P15 foundation value audit regression guard: PASS")
