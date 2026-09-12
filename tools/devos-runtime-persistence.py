#!/usr/bin/env python3
"""Bounded durable persistence for DevOS runtime outcomes.

Persistence records factual runtime evidence and checkpoint state. It never
creates authority, executes work, or treats an assertion as evidence.
"""
from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

STATE_VERSION = "P12-PERSISTENCE-v1"
MAX_HISTORY = 100


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"state_version": STATE_VERSION, "latest": None, "history": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("state_version") != STATE_VERSION:
        raise ValueError("unsupported runtime state")
    latest = data.get("latest")
    if latest is not None and not isinstance(latest, dict):
        raise ValueError("runtime latest record must be an object or null")
    history = data.get("history", [])
    if not isinstance(history, list):
        raise ValueError("runtime history must be a list")
    if len(history) > MAX_HISTORY:
        raise ValueError("runtime history exceeds bounded size")
    if any(not isinstance(record, dict) for record in history):
        raise ValueError("runtime history records must be objects")
    if latest is not None and history and history[-1] != latest:
        raise ValueError("runtime latest record must match final history record")
    if latest is not None and not history:
        raise ValueError("runtime latest record requires history")
    return data


def persist(path: Path, runtime_result: dict[str, Any], task_id: str, objective: str) -> dict[str, Any]:
    """Persist one verified-or-failed runtime outcome atomically."""
    evidence = runtime_result.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("RAW_EXECUTION_EVIDENCE_REQUIRED")
    status = runtime_result.get("status")
    if status not in {"COMPLETE", "FAILED", "BLOCKED", "CANCELLED"}:
        raise ValueError("invalid runtime outcome")

    path = path.resolve()
    state = _load(path)
    record = {
        "recorded_at": int(time.time()),
        "task_id": task_id,
        "objective": objective,
        "status": status,
        "verification": runtime_result.get("verification", "UNVERIFIED"),
        "security": runtime_result.get("security", "UNVERIFIED"),
        "evidence": evidence,
        "checkpoint": runtime_result.get("checkpoint"),
    }
    history = list(state.get("history", []))
    history.append(record)
    state = {"state_version": STATE_VERSION, "latest": record, "history": history[-MAX_HISTORY:]}

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return record


def load_latest(path: Path) -> dict[str, Any] | None:
    return _load(path).get("latest")
