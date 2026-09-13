#!/usr/bin/env python3
"""Side-effect-free GitHub identity/token control-plane primitives for DevOS.

This module deliberately does not perform network calls, token exchange, secret
storage, or GitHub mutations. It validates bounded authentication metadata and
builds non-secret inputs for a real provider adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import secrets
from typing import Any, Mapping
from urllib.parse import urlencode

AUTH_MODES = {"github_app_user", "github_app_installation"}


class GitHubAuthError(ValueError):
    """Raised when authentication metadata is invalid or unsafe."""


@dataclass(frozen=True)
class OAuthTransaction:
    client_id: str
    redirect_uri: str
    state: str
    issued_at: datetime


@dataclass(frozen=True)
class GitHubIdentityBinding:
    project_id: str
    provider: str
    login: str
    account_id: int | None
    auth_mode: str
    installation_id: int | None
    repository_scope: tuple[str, ...]
    permissions: tuple[tuple[str, str], ...]
    expires_at: datetime | None


def create_oauth_transaction(client_id: str, redirect_uri: str, *, now: datetime | None = None) -> OAuthTransaction:
    if not client_id.strip():
        raise GitHubAuthError("AUTH_CONFIG_INVALID: client_id required")
    if not redirect_uri.startswith("https://"):
        raise GitHubAuthError("AUTH_CONFIG_INVALID: HTTPS redirect_uri required")
    moment = now or datetime.now(timezone.utc)
    return OAuthTransaction(client_id, redirect_uri, secrets.token_urlsafe(32), moment)


def build_github_authorize_url(transaction: OAuthTransaction, *, allow_signup: bool = False) -> str:
    params = {"client_id": transaction.client_id, "redirect_uri": transaction.redirect_uri, "state": transaction.state}
    if allow_signup:
        params["allow_signup"] = "true"
    return "https://github.com/login/oauth/authorize?" + urlencode(params)


def validate_oauth_callback(expected_state: str, returned_state: str, code: str) -> str:
    if not expected_state or not returned_state or not hmac.compare_digest(expected_state, returned_state):
        raise GitHubAuthError("AUTH_STATE_MISMATCH")
    if not code or len(code) > 4096:
        raise GitHubAuthError("AUTHORIZATION_HOLD: invalid callback code")
    return code


def _parse_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GitHubAuthError("AUTH_TOKEN_SCOPE_UNKNOWN: invalid expiry timestamp") from exc
    return (parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)


def normalize_permissions(raw: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    normalized: list[tuple[str, str]] = []
    for name, level in raw.items():
        if not isinstance(name, str) or not isinstance(level, str):
            raise GitHubAuthError("GITHUB_CAPABILITY_UNCONFIRMED")
        normalized.append((name, level))
    return tuple(sorted(normalized))


def build_identity_binding(payload: Mapping[str, Any]) -> GitHubIdentityBinding:
    project_id = payload.get("project_id")
    provider = payload.get("provider")
    login = payload.get("login")
    auth_mode = payload.get("auth_mode")
    if not all(isinstance(v, str) and v.strip() for v in (project_id, provider, login)):
        raise GitHubAuthError("PROJECT_PROVIDER_BINDING_INVALID")
    if provider != "github":
        raise GitHubAuthError("PROJECT_PROVIDER_BINDING_INVALID")
    if auth_mode not in AUTH_MODES:
        raise GitHubAuthError("AUTH_CONFIG_INVALID: unsupported auth_mode")

    account_id = payload.get("account_id")
    if account_id is not None and (not isinstance(account_id, int) or isinstance(account_id, bool) or account_id <= 0):
        raise GitHubAuthError("GITHUB_IDENTITY_UNCONFIRMED")

    installation_id = payload.get("installation_id")
    if auth_mode == "github_app_installation":
        if not isinstance(installation_id, int) or isinstance(installation_id, bool) or installation_id <= 0:
            raise GitHubAuthError("GITHUB_INSTALLATION_UNCONFIRMED")
    elif installation_id is not None:
        raise GitHubAuthError("PROJECT_PROVIDER_BINDING_INVALID")

    repositories = payload.get("repositories", ())
    if isinstance(repositories, str) or not isinstance(repositories, (list, tuple)):
        raise GitHubAuthError("GITHUB_CAPABILITY_UNCONFIRMED")
    repo_scope = tuple(sorted({repo.strip() for repo in repositories if isinstance(repo, str) and repo.strip()}))

    permissions = payload.get("permissions", {})
    if not isinstance(permissions, Mapping):
        raise GitHubAuthError("GITHUB_CAPABILITY_UNCONFIRMED")

    return GitHubIdentityBinding(
        project_id=project_id,
        provider=provider,
        login=login,
        account_id=account_id,
        auth_mode=auth_mode,
        installation_id=installation_id,
        repository_scope=repo_scope,
        permissions=normalize_permissions(permissions),
        expires_at=_parse_time(payload.get("expires_at")),
    )


def redact_secret(value: str) -> str:
    """Return a non-secret fingerprint safe for evidence/audit metadata."""
    if not value:
        raise GitHubAuthError("AUTH_CONFIG_INVALID: empty secret material")
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:16]}"


def is_expired(binding: GitHubIdentityBinding, *, now: datetime | None = None, skew_seconds: int = 60) -> bool:
    if binding.expires_at is None:
        return False
    if skew_seconds < 0:
        raise GitHubAuthError("AUTH_CONFIG_INVALID: negative expiry skew")
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return moment.timestamp() >= binding.expires_at.timestamp() - skew_seconds


def safe_evidence_metadata(binding: GitHubIdentityBinding) -> dict[str, Any]:
    """Return provider identity/capability metadata with no credential material."""
    return {
        "provider": binding.provider,
        "project_id": binding.project_id,
        "login": binding.login,
        "account_id": binding.account_id,
        "auth_mode": binding.auth_mode,
        "installation_id": binding.installation_id,
        "repository_scope": list(binding.repository_scope),
        "permissions": dict(binding.permissions),
        "expires_at": binding.expires_at.isoformat() if binding.expires_at else None,
        "credential_material": "NOT_INCLUDED",
    }


if __name__ == "__main__":
    transaction = create_oauth_transaction("github-client-id", "https://example.test/github/callback")
    print(build_github_authorize_url(transaction))
