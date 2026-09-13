#!/usr/bin/env python3
"""Deterministic regression checks for remote resource permission governance."""
from pathlib import Path

CONTRACT = Path(__file__).with_name("../core/remote-resource-permission-governance.md")


def main() -> None:
    text = CONTRACT.resolve().read_text(encoding="utf-8")
    required = [
        "repository.create",
        "repository.delete",
        "branch.create",
        "branch.update",
        "branch.force_update",
        "branch.delete",
        "FULL APPROVAL",
        "CONTINUE",
        "NEEDS_EXTERNAL_REPO_CREATION",
        "do not blindly replay",
        "CHAT MEMORY != SOURCE OF TRUTH",
        "PROVIDER CREDENTIAL != DEVOS AUTHORIZATION",
    ]
    for marker in required:
        assert marker in text, marker

    # Capability separation must be explicit.
    assert "REPOSITORY DELETE != REPOSITORY CREATE" in text
    assert "BRANCH DELETE != BRANCH CREATE" in text
    assert "NORMAL BRANCH UPDATE != FORCE UPDATE" in text

    # Multi-project isolation must be represented.
    assert "PROJECT A state != PROJECT B state" in text
    assert "PROJECT A approval != PROJECT B approval" in text

    # Destructive operations must not inherit lower-risk approval.
    assert "Branch deletion must never be inferred from repository deletion approval." in text
    assert "A normal approval for `branch.update` must not authorize a force update." in text

    print("PASS: remote resource permission governance regression corpus")


if __name__ == "__main__":
    main()
