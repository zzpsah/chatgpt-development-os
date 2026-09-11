#!/usr/bin/env python3
"""Verify the DevOS stance-code and communication-style contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "DEVOS-STANCE-CODES.md"
STYLE = ROOT / "docs" / "DEVOS-CHATGPT-DESI-STYLE.md"
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
    require(STYLE.is_file(), "DESI communication profile is missing")
    require(AGENTS.is_file(), "AGENTS.md is missing")
    text = DOC.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    require("DEVOS::<STANCE>" in text, "canonical stance syntax missing")
    require("DEVOS::<STANCE>::<STYLE>" in text, "composable stance/style syntax missing")
    for code, marker in REQUIRED.items():
        require(code in text, f"canonical stance missing: {code}")
        require(marker in text.lower(), f"stance document missing semantic marker for {code}")

    for alias in ("god mode", "devil mode", "fuck mode", "desi mode"):
        require(alias in text.lower(), f"human alias missing: {alias}")

    # Validate semantic safety requirements without depending on one exact sentence.
    safety_terms = text.lower()
    require("permission" in safety_terms and "authorization" in safety_terms,
            "stance safety contract must discuss permission and authorization")
    require("safety" in safety_terms,
            "stance safety contract must discuss safety")
    require("does not replace project context" in safety_terms or
            "not a substitute for project context" in safety_terms,
            "stance contract must preserve project-context recovery")
    require("semantic" in safety_terms,
            "stance contract must preserve semantic interpretation")

    for phrase in (
        "natural Hinglish",
        "engineering mate",
        "college-style",
        "profanity",
        "technical precision",
        "presentation layer",
    ):
        require(phrase.lower() in style.lower(), f"DESI profile missing: {phrase}")

    require("docs/DEVOS-STANCE-CODES.md" in agents, "AGENTS.md must route to stance-code contract")
    require("DEVOS::GOD" in agents, "AGENTS.md must expose canonical GOD stance")
    require("DESI" in agents, "AGENTS.md must expose DESI style")
    require("docs/DEVOS-CHATGPT-DESI-STYLE.md" in agents, "AGENTS.md must route to DESI profile")

    print("PASS: DevOS stance-code contract is present")
    print("PASS: canonical stances and human aliases are documented")
    print("PASS: DESI communication profile is present")
    print("PASS: safety/authorization invariants are documented")
    print("PASS: AGENTS.md routes to stance and style contracts")


if __name__ == "__main__":
    main()
