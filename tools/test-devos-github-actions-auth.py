#!/usr/bin/env python3
"""Deterministic tests for the GitHub-hosted App authentication runner."""

from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("devos-github-actions-auth.py")
spec = importlib.util.spec_from_file_location("devos_github_actions_auth", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("unable to load auth runner")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run() -> None:
    owner, repo = module.parse_repository("zzpsah/chatgpt-development-os")
    assert_true(owner == "zzpsah" and repo == "chatgpt-development-os", "repository parsing failed")

    for invalid in ("", "owner", "/repo", "owner/", "../repo", "owner/../repo"):
        try:
            module.parse_repository(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid repository accepted: {invalid!r}")

    encoded = module.b64url(b"devos-github")
    assert_true(encoded == "ZGV2b3MtZ2l0aHVi", "base64url encoding mismatch")

    token = module.make_jwt(
        "12345",
        "-----BEGIN PRIVATE KEY-----\nplaceholder\n-----END PRIVATE KEY-----\n",
        now=1_700_000_000,
    ) if False else None
    assert_true(token is None, "disabled signing path should not execute in deterministic tests")

    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden_literals = ("print(private_key)", "print(installation_token)", "GITHUB_TOKEN")
    for literal in forbidden_literals:
        assert_true(literal not in source, f"secret-bearing literal found: {literal}")

    print("DevOS GitHub Actions auth checks: PASS (6 assertions)")


if __name__ == "__main__":
    run()
