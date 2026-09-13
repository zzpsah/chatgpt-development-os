#!/usr/bin/env python3
"""Regression corpus for the read-only DevOS universal activation resolver."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVATION_CARD = ROOT / "DEVOS-ACTIVATE.md"
spec = importlib.util.spec_from_file_location("devos_universal_activation", ROOT / "tools" / "devos-universal-activation.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def check(payload: dict, expected: str) -> dict:
    result = module.activate(payload)
    assert result["status"] == expected, result
    assert result["authority"] == "UNCHANGED", result
    assert result["authorization"] == "UNCHANGED", result
    assert result["execution"] == "NONE", result
    assert result["mutation"] == "NONE", result
    return result


check({"invocation": "hello", "repository_root": str(ROOT)}, "NOT_INVOKED")
check({"invocation": "DEVOS::DOD", "repository_root": str(ROOT)}, "INVALID_INVOCATION")
check({"invocation": "DEVOS::GOD"}, "DEVOS_NOT_AVAILABLE")
check({"invocation": "DEVOS::GOD", "repository_root": str(ROOT / "missing")}, "DEVOS_NOT_AVAILABLE")

with tempfile.TemporaryDirectory() as temporary:
    empty_root = Path(temporary)
    check({"invocation": "DEVOS::GOD", "repository_root": str(empty_root)}, "DEVOS_NOT_AVAILABLE")

with tempfile.TemporaryDirectory() as temporary:
    partial_root = Path(temporary)
    (partial_root / "AGENTS.md").write_text("# Managed project\n", encoding="utf-8")
    (partial_root / ".ai").mkdir()
    (partial_root / ".ai" / "manifest.yaml").write_text("project_id: partial\n", encoding="utf-8")
    partial = check({"invocation": "DEVOS::GOD", "repository_root": str(partial_root)}, "PROJECT_UNKNOWN")
    assert ".ai/CURRENT-STATE.md" in partial["missing"], partial

ready = check({"invocation": "DEVOS::GOD::DESI", "repository_root": str(ROOT / "tools")}, "READY_FOR_BOOTSTRAP")
assert ready["stance"]["canonical"] == "DEVOS::GOD::DESI", ready
assert Path(ready["repository_root"]) == ROOT, ready
assert len(ready["required_next_actions"]) == 4, ready
assert "does not grant approval" in ready["authority_boundary"], ready

default = check({"invocation": "DEVOS", "repository_root": str(ROOT)}, "READY_FOR_BOOTSTRAP")
assert default["stance"]["canonical"] == "DEVOS::CONTINUE::DESI", default

card = ACTIVATION_CARD.read_text(encoding="utf-8")
for marker in (
    "# DevOS Activation Card — Any AI, Any Account, Any Plan",
    "requires no API key, paid plan, plugin, MCP server",
    "DEVOS_NOT_AVAILABLE",
    "COPIED ACTIVATION CARD != REPOSITORY ACCESS",
):
    assert marker in card, marker

print("PASS: universal activation recognizes only explicit DevOS invocations")
print("PASS: unavailable or incomplete repository context never becomes bootstrap-ready")
print("PASS: DEVOS::GOD resolves to repository-backed bootstrap, not execution authority")
print("PASS: free-model activation card preserves the repository-access boundary")
