#!/usr/bin/env python3
"""Verify the versioned Development OS project-context manifest contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".ai" / "manifest.yaml"
REQUIRED_KEYS = {
    "context_version:",
    "specification:",
    "project_id:",
    "name:",
    "managed_by:",
    "context_directory:",
    "read_first:",
    "recommended:",
    "state_index:",
    "session_records:",
    "secrets_policy:",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(MANIFEST.is_file(), ".ai/manifest.yaml is missing")
    text = MANIFEST.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]

    for key in REQUIRED_KEYS:
        require(any(line.startswith(key) for line in lines), f"manifest key missing: {key}")

    context_version = next(line.split(":", 1)[1].strip() for line in lines if line.startswith("context_version:"))
    require(context_version.isdigit() and int(context_version) >= 1, "context_version must be a positive integer")

    require(any(line == "specification: portable-project-context" for line in lines), "unsupported manifest specification")
    require(any(line == "managed_by: development-os" for line in lines), "manifest must identify Development OS as manager")
    require(any(line == "context_directory: .ai" for line in lines), "context_directory must be .ai")
    require(any(line == "authority: repository-evidence-only" for line in lines), "state_index authority must be repository-evidence-only")
    require(any(line == "directory: SESSIONS" for line in lines), "session_records directory must be SESSIONS")
    require(any(line == "format: session-template.md" for line in lines), "session_records format must be declared")
    require(any(line == "secrets_policy: never-store-secrets" for line in lines), "manifest must declare the no-secrets policy")

    read_first = text.split("read_first:", 1)[1].split("recommended:", 1)[0]
    for required in ("STATE-INDEX.md", "PROJECT.md", "CURRENT-STATE.md"):
        require(required in read_first, f"read_first must include {required}")

    print("PASS: versioned DevOS project manifest contract is valid")


if __name__ == "__main__":
    main()
