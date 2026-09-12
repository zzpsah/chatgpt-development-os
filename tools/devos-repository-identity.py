#!/usr/bin/env python3
"""Validate the canonical DevOS repository identity without network access."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / ".ai" / "repository-identity.json"
EXPECTED = {
    "project_id": "chatgpt-development-os",
    "name": "ChatGPT Development OS",
    "canonical_repository": "zzpsah/chatgpt-development-os",
    "owner": "zzpsah",
    "default_branch": "main",
    "visibility": "public",
}


def validate(data: object) -> None:
    if not isinstance(data, dict):
        raise ValueError("repository identity must be an object")
    for key, expected in EXPECTED.items():
        actual = data.get(key)
        if actual != expected:
            raise ValueError(f"repository identity mismatch for {key}: expected {expected!r}, got {actual!r}")
    aliases = data.get("aliases")
    if not isinstance(aliases, list) or "DEVOS" not in aliases:
        raise ValueError("DEVOS alias is missing")
    if data.get("identity_status") != "CANONICAL":
        raise ValueError("repository identity is not canonical")


def load_and_validate(path: Path = IDENTITY) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate(data)
    return data


def main() -> int:
    data = load_and_validate()
    print("DevOS repository identity validation: PASS")
    print(f"Canonical repository: {data['canonical_repository']}")
    print(f"Default branch: {data['default_branch']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
