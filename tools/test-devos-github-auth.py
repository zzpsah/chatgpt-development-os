#!/usr/bin/env python3
"""Deterministic regression tests for DevOS GitHub auth control-plane primitives."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "devos-github-auth.py"
SPEC = importlib.util.spec_from_file_location("devos_github_auth", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load devos-github-auth.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def expect_error(fn, code: str) -> None:
    try:
        fn()
    except MODULE.GitHubAuthError as exc:
        assert str(exc).startswith(code), (str(exc), code)
    else:
        raise AssertionError(f"expected {code}")


def main() -> None:
    now = datetime(2026, 9, 14, 0, 0, tzinfo=timezone.utc)
    tx = MODULE.create_oauth_transaction("client", "https://example.test/callback", now=now)
    assert tx.client_id == "client"
    assert tx.redirect_uri.startswith("https://")
    assert len(tx.state) >= 32

    url = MODULE.build_github_authorize_url(tx)
    assert "client_id=client" in url
    assert "state=" in url
    assert "redirect_uri=https%3A%2F%2Fexample.test%2Fcallback" in url

    assert MODULE.validate_oauth_callback(tx.state, tx.state, "code-1") == "code-1"
    expect_error(lambda: MODULE.validate_oauth_callback(tx.state, "wrong", "code-1"), "AUTH_STATE_MISMATCH")

    binding = MODULE.build_identity_binding(
        {
            "project_id": "demo-project",
            "provider": "github",
            "login": "example",
            "account_id": 42,
            "auth_mode": "github_app_installation",
            "installation_id": 1001,
            "repositories": ["example/repo"],
            "permissions": {"contents": "write", "pull_requests": "write", "workflows": "write"},
            "expires_at": "2026-09-14T01:00:00Z",
        }
    )
    assert binding.repository_scope == ("example/repo",)
    assert MODULE.is_expired(binding, now=now) is False
    assert MODULE.is_expired(binding, now=datetime(2026, 9, 14, 1, 0, tzinfo=timezone.utc), skew_seconds=0) is True

    evidence = MODULE.safe_evidence_metadata(binding)
    assert evidence["credential_material"] == "NOT_INCLUDED"
    assert "token" not in str(evidence).lower()

    expect_error(
        lambda: MODULE.build_identity_binding(
            {
                "project_id": "demo-project",
                "provider": "github",
                "login": "example",
                "auth_mode": "github_app_installation",
            }
        ),
        "GITHUB_INSTALLATION_UNCONFIRMED",
    )
    assert MODULE.redact_secret("super-secret") != "super-secret"

    print("DevOS GitHub auth checks: PASS (10 assertions)")


if __name__ == "__main__":
    main()
