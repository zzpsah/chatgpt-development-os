#!/usr/bin/env python3
"""Exercise deterministic derived-context self-healing in an isolated Git repo."""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "self-heal-derived-context.py"


def run(cwd: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(["python", *args], cwd=cwd, text=True, capture_output=True, env=merged, check=False)


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        context = project / ".ai"
        context.mkdir(parents=True)
        (project / "AGENTS.md").write_text("# Agent Contract\n", encoding="utf-8")
        (context / "manifest.yaml").write_text(
            "project_id: test-project\nname: Test Project\ncontext_version: 1\n", encoding="utf-8"
        )
        semantic = context / "DECISIONS.md"
        semantic_text = "# Decision\nNever overwrite this semantic state.\n"
        semantic.write_text(semantic_text, encoding="utf-8")
        (context / "PROJECT.md").write_text("# Project\n", encoding="utf-8")
        (context / "CURRENT-STATE.md").write_text("# State\n", encoding="utf-8")
        (context / "TASKS.md").write_text("# Tasks\n", encoding="utf-8")
        git(project, "init")
        git(project, "config", "user.name", "DevOS Test")
        git(project, "config", "user.email", "devos-test@example.invalid")
        git(project, "add", ".")
        git(project, "commit", "-m", "test: seed isolated project")

        env = {
            "DEVOS_SELF_HEAL_FILES": "STATE-INDEX.md,PROJECT-IDENTITY.json,CHANGELOG.md",
        }
        healed = run(project, str(TOOL), env=env)
        assert healed.returncode == 0, healed.stderr
        assert "HEALED:" in healed.stdout
        assert "BOUNDARY: semantic project state unchanged" in healed.stdout
        assert (context / "STATE-INDEX.md").is_file()
        assert (context / "PROJECT-IDENTITY.json").is_file()
        assert (context / "CHANGELOG.md").is_file()
        assert semantic.read_text(encoding="utf-8") == semantic_text

        blocked = run(project, str(TOOL), env={"DEVOS_SELF_HEAL_FILES": "DECISIONS.md"})
        assert blocked.returncode != 0
        assert "BLOCKED:" in blocked.stderr or "BLOCKED:" in blocked.stdout
        assert semantic.read_text(encoding="utf-8") == semantic_text

        (context / "STATE-INDEX.md").unlink()
        healed_again = run(project, str(TOOL), env={"DEVOS_SELF_HEAL_FILES": "STATE-INDEX.md"})
        assert healed_again.returncode == 0, healed_again.stderr
        assert (context / "STATE-INDEX.md").is_file()

    print("PASS: missing derived context is deterministically self-healed")
    print("PASS: semantic project state remains unchanged")
    print("PASS: unsafe semantic-file requests are blocked")
    print("PASS: recreated index is based on actual Git evidence")


if __name__ == "__main__":
    main()
