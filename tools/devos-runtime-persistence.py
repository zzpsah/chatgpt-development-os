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
_CHECKPOINT_FIELDS = {
    "id": str,
    "runtime_version": str,
    "objective": str,
    "iteration": int,
    "work_unit": str,
    "repository_head": str,
    "status": str,
    "changes": list,
    "evidence": list,
    "verification": str,
    "blockers": list,
    "next_action": str,
}


def _validate_checkpoint(checkpoint: Any) -> None:
    if checkpoint is None:
        return
    if not isinstance(checkpoint, dict):
        raise ValueError("checkpoint must be an object or null")
    for field, expected in _CHECKPOINT_FIELDS.items():
        if field not in checkpoint or not isinstance(checkpoint[field], expected):
            raise ValueError(f"invalid checkpoint field: {field}")
    if isinstance(checkpoint["iteration"], bool) or checkpoint["iteration"] < 1:
        raise ValueError("checkpoint iteration must be a positive integer")
    if checkpoint["status"] not in {"IN_PROGRESS", "COMPLETE", "FAILED", "BLOCKED", "CANCELLED"}:
        raise ValueError("invalid checkpoint status")
    if not checkpoint["id"] or not checkpoint["runtime_version"] or not checkpoint["objective"] or not checkpoint["work_unit"]:
        raise ValueError("checkpoint identity fields must be non-empty")
    if checkpoint["repository_head"] != "UNKNOWN" and len(checkpoint["repository_head"]) != 40:
        raise ValueError("checkpoint repository_head must be a 40-character SHA or UNKNOWN")


def _validate_record(record: Any) -> None:
    if not isinstance(record, dict):
        raise ValueError("runtime record must be an object")
    for field in ("task_id", "objective", "status", "evidence"):
        if field not in record:
            raise ValueError(f"runtime record missing field: {field}")
    if not isinstance(record["task_id"], str) or not record["task_id"]:
        raise ValueError("runtime record task_id must be non-empty text")
    if not isinstance(record["objective"], str) or not record["objective"]:
        raise ValueError("runtime record objective must be non-empty text")
    if record["status"] not in {"COMPLETE", "FAILED", "BLOCKED", "CANCELLED"}:
        raise ValueError("invalid runtime outcome")
    if not isinstance(record["evidence"], list) or not record["evidence"]:
        raise ValueError("RAW_EXECUTION_EVIDENCE_REQUIRED")
    _validate_checkpoint(record.get("checkpoint"))


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"state_version": STATE_VERSION, "latest": None, "history": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("state_version") != STATE_VERSION:
        raise ValueError("unsupported runtime state")
    history = data.get("history", [])
    if not isinstance(history, list):
        raise ValueError("runtime history must be a list")
    latest = data.get("latest")
    if latest is not None:
        _validate_record(latest)
    for record in history:
        _validate_record(record)
    return data


def persist(path: Path, runtime_result: dict[str, Any], task_id: str, objective: str) -> dict[str, Any]:
    """Persist one verified-or-failed runtime outcome atomically."""
    if not isinstance(runtime_result, dict):
        raise ValueError("runtime result must be an object")
    evidence = runtime_result.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("RAW_EXECUTION_EVIDENCE_REQUIRED")
    status = runtime_result.get("status")
    if status not in {"COMPLETE", "FAILED", "BLOCKED", "CANCELLED"}:
        raise ValueError("invalid runtime outcome")
    if not isinstance(task_id, str) or not task_id or not isinstance(objective, str) or not objective:
        raise ValueError("task identity must be non-empty text")

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
    _validate_record(record)
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
    latest = _load(path).get("latest")
    if latest is not None:
        _validate_record(latest)
    return latest
