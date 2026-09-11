#!/usr/bin/env python3
"""Exercise recovery precedence decisions without accessing AI-account memory."""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "resolve-recovery-precedence.py"


def run(cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python", str(TOOL)], cwd=cwd, text=True, capture_output=True, env=os.environ.copy(), check=False)


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".ai").mkdir()
        git(project, "init")
        git(project, "config", "user.name", "DevOS Test")
        git(project, "config", "user.email", "devos-test@example.invalid")
        (project / "app.py").write_text("print('source')\n", encoding="utf-8")
        git(project, "add", ".")
        git(project, "commit", "-m", "test: seed precedence project")

        healthy = run(project)
        assert healthy.returncode == 0
        assert "ACTION: PROCEED_WITH_SOURCE_AND_GIT" in healthy.stdout
        assert "source+git" in healthy.stdout
        assert "ai-memory" in healthy.stdout

        (project / ".ai" / "CURRENT-STATE.md").write_text("old state\n", encoding="utf-8")
        (project / ".ai" / "TASKS.md").write_text("old task\n", encoding="utf-8")
        conflicted = run(project)
        assert conflicted.returncode == 0
        assert "PROCEED_WITH_SOURCE_AND_GIT" in conflicted.stdout
        assert "source+git" in conflicted.stdout

        (project / ".ai" / "CURRENT-STATE.md").unlink()
        (project / ".ai" / "TASKS.md").unlink()
        (project / ".ai" / "STATE-INDEX.md").write_text("generated only\n", encoding="utf-8")
        generated_only = run(project)
        assert generated_only.returncode == 0
        assert "CONFLICT: generated index exists without durable semantic AI state" in generated_only.stdout
        assert "ACTION: ESCALATE_REVIEW" in generated_only.stdout

    print("PASS: source/Git remains first implementation authority")
    print("PASS: AI memory is never consulted as authoritative evidence")
    print("PASS: generated-only context without durable semantic state escalates")
    print("PASS: recovery precedence is deterministic")


if __name__ == "__main__":
    main()
