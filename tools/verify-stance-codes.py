#!/usr/bin/env python3
"""Verify the DevOS stance-code and communication-style contract."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "DEVOS-STANCE-CODES.md"
STYLE = ROOT / "docs" / "DEVOS-CHATGPT-DESI-STYLE.md"
AGENTS = ROOT / "AGENTS.md"
REGISTRY = ROOT / "config" / "devos-stance-registry.yaml"
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
    for path, label in ((DOC, "stance-code document"), (STYLE, "DESI communication profile"), (AGENTS, "AGENTS.md"), (REGISTRY, "stance registry")):
        require(path.is_file(), f"{label} is missing")

    text = DOC.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    require(isinstance(registry, dict), "stance registry is not a mapping")

    require("DEVOS::<STANCE>" in text, "canonical stance syntax missing")
    require("DEVOS::<STANCE>::<STYLE>" in text, "composable stance/style syntax missing")
    executions = registry.get("executions", {})
    styles = registry.get("styles", {})
    aliases = registry.get("aliases", {})
    require(registry.get("default_execution") in executions, "default execution is not registered")
    require(registry.get("default_style") in styles, "default style is not registered")

    for code, marker in REQUIRED.items():
        stance = code.split("::", 1)[1]
        require(stance in executions, f"registry execution missing: {stance}")
        require(code in text, f"canonical stance missing: {code}")
        require(marker in str(executions[stance].get("purpose", "")).lower(), f"registry purpose missing semantic marker for {code}")

    require(aliases.get("god mode") == "DEVOS::GOD", "god mode alias must resolve canonically")
    require(aliases.get("devil mode") == "DEVOS::DEVIL", "devil mode alias must resolve canonically")
    require(aliases.get("fuck mode") == "DEVOS::FUCK", "fuck mode alias must resolve canonically")
    require(aliases.get("desi mode") == "DEVOS::CONTINUE::DESI", "desi mode alias must resolve to CONTINUE + DESI")

    # Safety is a semantic contract: check the registry model rather than one exact prose sentence.
    god = executions["GOD"]
    require(god.get("write_allowed_by_stance") is True, "GOD must permit routine authorized writes")
    for required_escalation in ("destructive", "irreversible", "production-impacting", "security-sensitive", "ambiguous"):
        require(required_escalation in god.get("escalation_required_for", []), f"GOD escalation guard missing: {required_escalation}")
    desi = styles["DESI"]
    require(desi.get("profanity") == "allowed_when_natural_and_user_invited", "DESI profanity behavior must remain explicit")
    require("authorization" in str(desi.get("technical_invariant", "")).lower(), "DESI technical invariant must preserve authorization")
    require("verification" in str(desi.get("technical_invariant", "")).lower(), "DESI technical invariant must preserve verification")

    for phrase in ("natural Hinglish", "engineering mate", "college-style", "profanity", "technical precision", "presentation layer"):
        require(phrase.lower() in style.lower(), f"DESI profile missing: {phrase}")

    require("docs/DEVOS-STANCE-CODES.md" in agents, "AGENTS.md must route to stance-code contract")
    require("DEVOS::GOD" in agents, "AGENTS.md must expose canonical GOD stance")
    require("DESI" in agents, "AGENTS.md must expose DESI style")
    require("docs/DEVOS-CHATGPT-DESI-STYLE.md" in agents, "AGENTS.md must route to DESI profile")

    print("PASS: DevOS stance/style registry is valid")
    print("PASS: canonical stances and aliases resolve from the registry")
    print("PASS: GOD safety/authorization escalation guards are present")
    print("PASS: DESI communication profile is present")
    print("PASS: AGENTS.md routes to stance and style contracts")


if __name__ == "__main__":
    main()
