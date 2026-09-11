#!/usr/bin/env python3
"""Verify the automatic DevOS project identity discovery contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "discover-project-identity.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), "project identity discovery tool is missing")
    text = TOOL.read_text(encoding="utf-8")
    for needle in (
        "remote.origin.url",
        "GITHUB_REPOSITORY",
        ".ai/manifest.yaml",
        "project_id",
        "identity_source",
        "confidence",
        '"UNKNOWN"',
        "DEVOS_WRITE_IDENTITY",
        "non-destructive",
        "application source",
    ):
        require(needle in text, f"identity discovery contract missing {needle!r}")
    require("manifest" in text and "github-ci" in text and "git-remote" in text, "identity source precedence must be explicit")
    print("PASS: automatic DevOS project identity discovery contract is structurally valid")
    print("NOTE: identity discovery reports ambiguity instead of guessing and is non-destructive by default")


if __name__ == "__main__":
    main()
