#!/usr/bin/env python3
"""Exercise safe reconciliation behavior in an isolated temporary project."""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "reconcile-derived-context.py"


def run(env: dict[str, str], cwd: Path) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    merged.update(env)
    return subprocess.run(
        ["python", str(TOOL)], cwd=cwd, text=True, capture_output=True, env=merged, check=False
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        context = project / ".ai"
        context.mkdir()
        semantic = context / "DECISIONS.md"
        semantic.write_text("# Intent\nKeep this decision unchanged.\n", encoding="utf-8")

        blocked = run({"DEVOS_RECONCILE_FILES": "DECISIONS.md"}, project)
        assert blocked.returncode != 0, "semantic file must be blocked"
        assert "BLOCKED:" in blocked.stderr or "BLOCKED:" in blocked.stdout, "missing BLOCKED signal"
        assert semantic.read_text(encoding="utf-8") == "# Intent\nKeep this decision unchanged.\n"

        repair = run({"DEVOS_RECONCILE_FILES": "STATE-INDEX.md"}, project)
        assert repair.returncode == 0, repair.stderr
        assert "REPAIR_REQUIRED:" in repair.stdout, "missing derived file must request repair"

        (context / "STATE-INDEX.md").write_text("stale", encoding="utf-8")
        safe = run({"DEVOS_RECONCILE_FILES": "STATE-INDEX.md"}, project)
        assert safe.returncode == 0, safe.stderr
        assert "SAFE:" in safe.stdout and "NOOP:" in safe.stdout, "existing derived file must be safe no-op"
        assert (context / "STATE-INDEX.md").read_text(encoding="utf-8") == "stale"

    print("PASS: semantic files are blocked from auto-reconciliation")
    print("PASS: missing derived files request deterministic repair")
    print("PASS: existing derived files remain non-destructive no-ops")


if __name__ == "__main__":
    main()
