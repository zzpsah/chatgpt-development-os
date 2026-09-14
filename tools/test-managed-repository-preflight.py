#!/usr/bin/env python3
"""Regression corpus for read-only managed-repository delivery preflight."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("managed_preflight", ROOT / "tools" / "managed-repository-preflight.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def run(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def fixture(root: Path) -> Path:
    repo = root / "managed"
    repo.mkdir()
    run(repo, "init", "-q")
    run(repo, "config", "user.email", "preflight@example.invalid")
    run(repo, "config", "user.name", "Preflight")
    (repo / "docs").mkdir()
    (repo / "docs" / "note.md").write_text("before\n", encoding="utf-8")
    run(repo, "add", ".")
    run(repo, "commit", "-qm", "fixture")
    return repo


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        repo = fixture(root)
        before = (repo / "docs" / "note.md").read_text(encoding="utf-8")
        output = root / "evidence" / "preflight.json"
        result = mod.preflight(repo, "Inspect current repository state then update docs note", ["docs/note.md"], "managed-fixture")
        assert result["status"] == "HOLD", result
        assert {"READ_ONLY_PREFLIGHT_COMPLETE", "EXPLICIT_STEP_SCOPED_APPROVAL_REQUIRED"}.issubset(result["reasons"]), result
        assert result["approval_request"]["repository_head"] == subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(), result
        assert result["approval_request"]["targets"] == ["docs/note.md"], result
        assert result["approval_request"]["allowed_operations"] == ["file.create", "file.update"], result
        assert result["execution"] == "NONE" and result["mutation"] == "NONE" and result["production_ready"] is False, result
        assert (repo / "docs" / "note.md").read_text(encoding="utf-8") == before, "preflight edited repository"
        assert subprocess.check_output(["git", "status", "--porcelain"], cwd=repo, text=True) == "", "preflight changed git state"
        mod.persist_external(result, output, repo)
        persisted = json.loads(output.read_text(encoding="utf-8"))
        assert persisted["evidence_id"] == result["evidence_id"], persisted
        try:
            mod.persist_external(result, repo / ".ai" / "preflight.json", repo)
        except ValueError as error:
            assert str(error) == "EVIDENCE_OUTPUT_MUST_BE_OUTSIDE_INSPECTED_REPOSITORY"
        else:
            raise AssertionError("repository-local evidence write was accepted")
        (repo / "untracked.txt").write_text("conflict\n", encoding="utf-8")
        dirty = mod.preflight(repo, "Inspect current repository state then update docs note", ["docs/note.md"])
        assert dirty["status"] == "HOLD" and "WORKTREE_NOT_CLEAN" in dirty["reasons"], dirty
        invalid = mod.preflight(repo, "Inspect current repository state then update docs note", ["../escape"])
        assert invalid["status"] == "HOLD" and "ALLOWED_PATHS_INVALID" in invalid["reasons"], invalid
    print("PASS: managed repository preflight builds exact scoped approval evidence and holds without repository mutation")


if __name__ == "__main__":
    main()
