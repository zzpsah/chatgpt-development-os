#!/usr/bin/env python3
"""Regression tests for the read-only Trust-First DevOS audit."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-audit.py"
spec = importlib.util.spec_from_file_location("devos_audit", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def copy_manifest(source: Path, target: Path) -> None:
    for rel in mod.manifest():
        src = source / rel
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def test_repository_dependency_closure() -> None:
    report = mod.audit(ROOT, run_checks=False)
    assert report["bundle"]["dependency_closed"] is True, report
    assert report["bundle"]["classification"] == "COMPLETE_FOR_ADVERTISED_CHECKS"
    assert report["identity"]["result"] == "PASS"
    checks = {row["name"]: row for row in report["checks"]}
    assert checks["interpretation"]["result"] == "PASS", checks["interpretation"]
    assert checks["evidence_ledger"]["result"] == "PASS", checks["evidence_ledger"]
    assert all(row["result"] == "PASS" for row in report["checks"]), report
    assert report["mutation"] == "NONE"
    assert report["execution"] == "NONE"


def test_missing_runtime_bridge_is_packaging_gap() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_manifest(ROOT, pack)
        (pack / "tools/runtime-adapter-bridge.py").unlink()
        report = mod.audit(pack, run_checks=False)
        controlled = next(row for row in report["checks"] if row["name"] == "controlled_mutation")
        assert controlled["result"] == "UNKNOWN", controlled
        assert controlled["evidence"] == "PACK_INCOMPLETE"
        assert "tools/runtime-adapter-bridge.py" in controlled["missing"]
        assert report["overall"] == "UNKNOWN"


def test_missing_security_dependencies_is_packaging_gap() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_manifest(ROOT, pack)
        (pack / "rules/security.md").unlink()
        (pack / "workflows/security.md").unlink()
        report = mod.audit(pack, run_checks=False)
        security = next(row for row in report["checks"] if row["name"] == "security_gate")
        assert security["result"] == "UNKNOWN", security
        assert security["evidence"] == "PACK_INCOMPLETE"
        assert set(security["missing"]) == {"rules/security.md", "workflows/security.md"}
        assert report["overall"] == "UNKNOWN"


def test_missing_interpreter_dependency_is_packaging_gap() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_manifest(ROOT, pack)
        (pack / "tools/human-language-interpreter.py").unlink()
        report = mod.audit(pack, run_checks=False)
        interpretation = next(row for row in report["checks"] if row["name"] == "interpretation")
        assert interpretation["result"] == "UNKNOWN", interpretation
        assert interpretation["evidence"] == "PACK_INCOMPLETE"
        assert "tools/human-language-interpreter.py" in interpretation["missing"]
        assert report["overall"] == "UNKNOWN"


def test_missing_ledger_dependency_is_packaging_gap() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_manifest(ROOT, pack)
        (pack / "config/readiness-evidence.json").unlink()
        report = mod.audit(pack, run_checks=False)
        ledger = next(row for row in report["checks"] if row["name"] == "evidence_ledger")
        assert ledger["result"] == "UNKNOWN", ledger
        assert ledger["evidence"] == "PACK_INCOMPLETE"
        assert "config/readiness-evidence.json" in ledger["missing"]
        assert report["overall"] == "UNKNOWN"


def test_wrong_identity_blocks_instead_of_guessing() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_manifest(ROOT, pack)
        manifest = pack / ".ai/manifest.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "canonical_repository: zzpsah/chatgpt-development-os",
                "canonical_repository: attacker/not-devos",
            ),
            encoding="utf-8",
        )
        report = mod.audit(pack, run_checks=False)
        assert report["identity"]["result"] == "FAIL", report
        assert report["identity"]["evidence"] == "BLOCKED"
        assert report["overall"] == "BLOCKED"


def main() -> None:
    test_repository_dependency_closure()
    test_missing_runtime_bridge_is_packaging_gap()
    test_missing_security_dependencies_is_packaging_gap()
    test_missing_interpreter_dependency_is_packaging_gap()
    test_missing_ledger_dependency_is_packaging_gap()
    test_wrong_identity_blocks_instead_of_guessing()
    print("PASS: Trust-First DevOS audit / audit-pack reproducibility corpus")


if __name__ == "__main__":
    main()
