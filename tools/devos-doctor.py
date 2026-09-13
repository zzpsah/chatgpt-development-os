#!/usr/bin/env python3
"""Human-readable read-only presentation layer for DevOS foundation health.

Truth remains in the Trust-First audit and readiness evidence ledger. This tool
only renders machine-derived health and never grants authority or mutates state.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEALTH = ROOT / "tools" / "devos-health.py"


def _load_health():
    spec = importlib.util.spec_from_file_location("devos_health_doctor", HEALTH)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load tools/devos-health.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render(report: dict) -> str:
    lines = [
        f"DEVOS DOCTOR: {report.get('overall', 'UNKNOWN')}",
        f"Repository: {report.get('repository', 'UNKNOWN')}",
        "Mode: READ_ONLY | authority=UNCHANGED | authorization=UNCHANGED | execution=NONE | mutation=NONE",
        "",
        "Checks:",
    ]
    for row in report.get("checks", []):
        lines.append(f"- [{row.get('status', 'UNKNOWN')}] {row.get('name', 'unknown')}: {row.get('reason', '')}")
        evidence = row.get("evidence")
        if evidence:
            lines.append(f"  evidence: {evidence}")
    lines.extend([
        "",
        f"production_ready: {str(report.get('production_ready', False)).lower()}",
        f"live_mutation_proven: {str(report.get('live_mutation_proven', False)).lower()}",
    ])
    drift = report.get("historical_source_drift", [])
    if drift:
        lines.append("historical_source_drift:")
        lines.extend(f"  - {item}" for item in drift)
    lines.append("")
    lines.append("Safety invariants:")
    lines.extend(f"- {item}" for item in report.get("invariants", []))
    lines.append("")
    lines.append("Universal goal:")
    lines.append(report.get("universal_product_goal", "UNKNOWN"))
    limitations = report.get("limitations", [])
    if limitations:
        lines.append("")
        lines.append("Limitations:")
        lines.extend(f"- {item}" for item in limitations)
    lines.append("")
    lines.append("Rule: WARN and UNKNOWN are not PASS.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--no-run-checks", action="store_true")
    args = parser.parse_args()
    health = _load_health()
    report = health.derive_health(Path(args.root), run_checks=not args.no_run_checks)
    print(render(report))
    return 0 if report.get("overall") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
