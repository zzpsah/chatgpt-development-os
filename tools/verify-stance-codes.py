#!/usr/bin/env python3
"""Verify the DevOS stance-code contract and safety invariants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "DEVOS-STANCE-CODES.md"
AGENTS = ROOT / "AGENTS.md"
REQUIRED = {
    "DEVOS::RECOVER": "recover",
    "DEVOS::CONTINUE": "continue",
    "DEVOS::GOD": "maximum",
    "DEVOS::BUILD": "implementation",
    "DEVOS::FIX": "fix",
    "DEVOS::DEBUG": "investigate",
    "DEVOS::DEVIL": "adversarial",
    "DEVOS::TEACH": "teaching",
    "DEVOS::DESIGN": "architecture",
    "DEVOS::AUDIT": "review",
    "DEVOS::FUCK": "high-intensity",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(DOC.is_file(), "stance-code document is missing")
    require(AGENTS.is_file(), "AGENTS.md is missing")
    text = DOC.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    require("DEVOS::<STANCE>" in text, "canonical stance syntax missing")
    for code, marker in REQUIRED.items():
        require(code in text, f"canonical stance missing: {code}")
        require(marker in text.lower(), f"stance document missing semantic marker for {code}")

    for alias in ("god mode", "devil mode", "fuck mode"):
        require(alias in text.lower(), f"human alias missing: {alias}")

    for invariant in (
        "does not replace project recovery",
        "never grants permission",
        "safety",
        "authorization",
        "semantic",
    ):
        require(invariant in text.lower(), f"safety invariant missing: {invariant}")

    require("docs/DEVOS-STANCE-CODES.md" in agents, "AGENTS.md must route to stance-code contract")
    require("DEVOS::GOD" in agents, "AGENTS.md must expose canonical GOD stance")

    print("PASS: DevOS stance-code contract is present")
    print("PASS: canonical stances and human aliases are documented")
    print("PASS: safety/authorization invariants are documented")
    print("PASS: AGENTS.md references the stance-code entry point")


if __name__ == "__main__":
    main()
