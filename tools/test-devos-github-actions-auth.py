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
    assertions = 0

    owner, repo = module.parse_repository("zzpsah/chatgpt-development-os")
    assert_true(owner == "zzpsah" and repo == "chatgpt-development-os", "repository parsing failed")
    assertions += 1

    for invalid in ("", "owner", "/repo", "owner/", "../repo", "owner/../repo"):
        try:
            module.parse_repository(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid repository accepted: {invalid!r}")
        assertions += 1

    encoded = module.b64url(b"devos-github")
    assert_true(encoded == "ZGV2b3MtZ2l0aHVi", "base64url encoding mismatch")
    assertions += 1

    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden_literals = ("print(private_key)", "print(installation_token)", "os.environ['DEVOS_GITHUB_APP_PRIVATE_KEY']")
    for literal in forbidden_literals:
        assert_true(literal not in source, f"unsafe secret-access pattern found: {literal}")
        assertions += 1

    assert_true('"credential_material": "NOT_INCLUDED"' in source, "credential redaction evidence missing")
    assertions += 1
    assert_true('"mutation": "NONE"' in source, "mutation boundary missing")
    assertions += 1
    assert_true('"execution": "NONE"' in source, "execution boundary missing")
    assertions += 1

    print(f"DevOS GitHub Actions auth checks: PASS ({assertions} assertions)")


if __name__ == "__main__":
    run()
