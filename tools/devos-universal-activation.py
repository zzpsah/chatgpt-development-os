#!/usr/bin/env python3
"""Resolve a DevOS stance invocation into an evidence-backed bootstrap request.

This reference tool is intentionally read-only. A host may use it after a user
writes ``DEVOS`` or ``DEVOS::<STANCE>`` to decide whether DevOS can actually be
loaded from a repository available to that host. It never treats chat memory,
a provider credential, or the stance itself as repository or execution proof.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BOOTSTRAP_FILES = (
    "AGENTS.md",
    ".ai/manifest.yaml",
    ".ai/CURRENT-STATE.md",
    ".ai/TASKS.md",
    ".ai/DECISIONS.md",
)


def _load_stance_parser() -> Any:
    path = ROOT / "tools" / "parse-devos-stance.py"
    spec = importlib.util.spec_from_file_location("devos_stance_parser", path)
    if spec is None or spec.loader is None:
        raise ImportError("DevOS stance parser is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _base(status: str, invocation: str) -> dict[str, Any]:
    return {
        "protocol": "DEVOS-UNIVERSAL-ACTIVATION-v1",
        "status": status,
        "invocation": invocation,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
    }


def _looks_like_devos_invocation(value: str, registry: dict[str, Any]) -> bool:
    normalized = value.strip().lower()
    return normalized == "devos" or normalized.startswith("devos::") or normalized in registry.get("aliases", {})


def _find_repository_root(start: Path) -> Path | None:
    """Find the nearest repository-local DevOS bootstrap surface without writing."""
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / ".ai" / "manifest.yaml").is_file():
            return candidate
    return None


def activate(payload: dict[str, Any]) -> dict[str, Any]:
    invocation = str(payload.get("invocation", "")).strip()
    parser = _load_stance_parser()
    registry = parser.load_registry()

    if not _looks_like_devos_invocation(invocation, registry):
        result = _base("NOT_INVOKED", invocation)
        result["reason"] = "No canonical DevOS stance or registered DevOS alias was supplied."
        return result

    try:
        stance = parser.parse(invocation, registry)
    except ValueError as exc:
        result = _base("INVALID_INVOCATION", invocation)
        result["reason"] = str(exc)
        result["accepted_syntax"] = "DEVOS, DEVOS::<STANCE>, or DEVOS::<STANCE>::<STYLE>"
        return result

    root_value = payload.get("repository_root")
    if not isinstance(root_value, str) or not root_value.strip():
        result = _base("DEVOS_NOT_AVAILABLE", invocation)
        result.update({
            "stance": stance,
            "reason": "REPOSITORY_ROOT_REQUIRED",
            "next_action": "The host must provide a local managed-project or DevOS repository root before bootstrap.",
        })
        return result

    start = Path(root_value).expanduser().resolve()
    if not start.is_dir():
        result = _base("DEVOS_NOT_AVAILABLE", invocation)
        result.update({
            "stance": stance,
            "reason": "REPOSITORY_ROOT_NOT_FOUND",
            "repository_root": str(start),
        })
        return result

    root = _find_repository_root(start)
    if root is None:
        result = _base("DEVOS_NOT_AVAILABLE", invocation)
        result.update({
            "stance": stance,
            "reason": "DEVOS_BOOTSTRAP_FILES_NOT_FOUND",
            "repository_root": str(start),
            "required_files": list(REQUIRED_BOOTSTRAP_FILES),
        })
        return result

    missing = [relative for relative in REQUIRED_BOOTSTRAP_FILES if not (root / relative).is_file()]
    if missing:
        result = _base("PROJECT_UNKNOWN", invocation)
        result.update({
            "stance": stance,
            "repository_root": str(root),
            "reason": "INCOMPLETE_DEVOS_BOOTSTRAP_SURFACE",
            "missing": missing,
        })
        return result

    result = _base("READY_FOR_BOOTSTRAP", invocation)
    result.update({
        "stance": stance,
        "repository_root": str(root),
        "required_next_actions": [
            "Read AGENTS.md and the applicable DevOS bootstrap protocol.",
            "Recover CURRENT-STATE.md, TASKS.md, DECISIONS.md, and relevant session provenance.",
            "Inspect current source tree, Git state, tests, configuration, and applicable CI evidence.",
            "Only then interpret, plan, assess readiness, and continue through the governed workflow.",
        ],
        "authority_boundary": "The stance permits only the routine authority already granted by the user and project policy. It does not grant approval or execution.",
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only DevOS universal activation resolver")
    parser.add_argument("--input", help="JSON payload; stdin is used when omitted")
    args = parser.parse_args()
    raw = args.input if args.input is not None else __import__("sys").stdin.read()
    print(json.dumps(activate(json.loads(raw)), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
