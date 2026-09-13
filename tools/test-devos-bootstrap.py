#!/usr/bin/env python3
"""Regression tests for the read-only DevOS foundation bootstrap checker."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tempfile

MODULE_PATH = Path(__file__).with_name("devos-bootstrap.py")
spec = spec_from_file_location("devos_bootstrap", MODULE_PATH)
assert spec and spec.loader
module = module_from_spec(spec)
spec.loader.exec_module(module)
devos_bootstrap = module


def test_repository_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    ok, results = devos_bootstrap.check(root)
    assert ok, results
    assert all(status == "PASS" for _, status in results), results


def test_missing_required_file_holds() -> None:
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in devos_bootstrap.REQUIRED_FILES:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((source / rel).read_text(encoding="utf-8"), encoding="utf-8")
        (root / "AGENTS.md").unlink()
        ok, results = devos_bootstrap.check(root)
        assert not ok
        assert ("required:AGENTS.md", "HOLD") in results


def test_identity_conflict_holds() -> None:
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in devos_bootstrap.REQUIRED_FILES:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((source / rel).read_text(encoding="utf-8"), encoding="utf-8")
        manifest = root / ".ai/manifest.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "canonical_repository: zzpsah/chatgpt-development-os",
                "canonical_repository: attacker/not-devos",
            ),
            encoding="utf-8",
        )
        ok, results = devos_bootstrap.check(root)
        assert not ok
        assert ("canonical-identity", "HOLD") in results


if __name__ == "__main__":
    test_repository_passes()
    test_missing_required_file_holds()
    test_identity_conflict_holds()
    print("DevOS bootstrap tests: PASS")
