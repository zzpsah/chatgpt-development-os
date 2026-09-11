#!/usr/bin/env python3
"""Deterministic P12 operational intelligence for task graphs."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any


TERMINAL = {"COMPLETE"}
BLOCKED = {"BLOCKED", "FAILED", "ESCALATED"}
UNAUTHORIZED = {"NEEDS_APPROVAL"}
VALID_CHECKPOINT_EVENTS = {
    "REPOSITORY_CHANGE", "WORK_UNIT_COMPLETE", "WORK_UNIT_FAILED",
    "BLOCKED_TRANSITION", "AUTHORIZATION_CHANGE", "VERIFICATION_RESULT",
    "SECURITY_RESULT", "SESSION_BOUNDARY", "HANDOFF_BOUNDARY",
}
FAILURE_CLASSES = {
    "CAPABILITY_MISSING", "AUTHORIZATION_REQUIRED", "DEPENDENCY_BLOCKED",
    "VERIFICATION_FAILED", "SECURITY_BLOCKED", "PROVIDER_FAILURE",
    "REPOSITORY_DRIFT", "INPUT_AMBIGUOUS", "UNKNOWN",
}
EXECUTION_EVIDENCE_SOURCES = {"repository", "git", "runtime", "test", "security", "provider"}


@dataclass(frozen=True)
class Node:
    id: str
    status: str
    dependencies: tuple[str, ...]
    priority: int
    effort: int = 0
    age_days: int = 0
    deadline_days: int | None = None


def build_graph(tasks: list[dict[str, Any]]) -> dict[str, Node]:
    graph: dict[str, Node] = {}
    for raw in tasks:
        task_id = str(raw["id"])
        if task_id in graph:
            raise ValueError(f"duplicate task id: {task_id}")
        deps = tuple(str(x) for x in raw.get("dependencies", []))
        deadline = raw.get("deadline_days")
        graph[task_id] = Node(task_id, str(raw.get("status", "PLANNED")), deps,
                              int(raw.get("priority", 0)), max(0, int(raw.get("effort", 0))),
                              max(0, int(raw.get("age_days", 0))),
                              None if deadline is None else int(deadline))
    missing = sorted({d for n in graph.values() for d in n.dependencies if d not in graph})
    if missing:
        raise ValueError("missing dependency references: " + ", ".join(missing))
    return graph


def has_cycle(graph: dict[str, Node]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        if any(visit(dep) for dep in graph[node_id].dependencies):
            return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False
    return any(visit(node_id) for node_id in sorted(graph))


def readiness(graph: dict[str, Node]) -> list[dict[str, Any]]:
    if has_cycle(graph):
        return [{"id": n.id, "readiness": "BLOCKED", "reason": "DEPENDENCY_CYCLE", "priority": n.priority}
                for n in sorted(graph.values(), key=lambda x: x.id)]
    result = []
    for node in graph.values():
        if node.status in TERMINAL:
            state, reason = "COMPLETE", "TASK_COMPLETE"
        elif node.status in BLOCKED:
            state, reason = "BLOCKED", node.status
        elif node.status in UNAUTHORIZED:
            state, reason = "UNAUTHORIZED", "AUTHORIZATION_REQUIRED"
        elif any(graph[d].status not in TERMINAL for d in node.dependencies):
            state, reason = "WAITING", "DEPENDENCIES_UNSATISFIED"
        else:
            state, reason = "READY", "DEPENDENCIES_SATISFIED"
        result.append({"id": node.id, "readiness": state, "reason": reason, "priority": node.priority})
    return sorted(result, key=lambda x: (-x["priority"], x["id"]))


def priority_analysis(graph: dict[str, Node]) -> list[dict[str, Any]]:
    dependents = {node_id: 0 for node_id in graph}
    for node in graph.values():
        for dep in node.dependencies:
            dependents[dep] += 1
    rows = []
    for node in graph.values():
        if node.status in TERMINAL:
            continue
        score = node.priority * 100
        reasons = [f"explicit_priority={node.priority}"]
        if dependents[node.id]:
            score += dependents[node.id] * 20
            reasons.append(f"dependent_count={dependents[node.id]}")
        if node.status in BLOCKED:
            score -= 50
            reasons.append(f"status_penalty={node.status}")
        if node.age_days:
            score += min(node.age_days, 30)
            reasons.append(f"age_days={node.age_days}")
        if node.deadline_days is not None:
            if node.deadline_days <= 0:
                score += 100
                reasons.append("deadline_due_or_overdue")
            else:
                score += max(0, 30 - node.deadline_days)
                reasons.append(f"deadline_days={node.deadline_days}")
        if node.effort:
            score -= min(node.effort, 50)
            reasons.append(f"effort_penalty={node.effort}")
        rows.append({"id": node.id, "score": score, "reasons": reasons})
    return sorted(rows, key=lambda x: (-x["score"], x["id"]))


def checkpoint_signals(events: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    signals = []
    for event in events or []:
        kind = str(event.get("type", ""))
        signals.append({"checkpoint": kind in VALID_CHECKPOINT_EVENTS,
                        "reason": kind if kind in VALID_CHECKPOINT_EVENTS else "UNRECOGNIZED_EVENT",
                        "event": kind})
    return signals


def classify_failure(failure: dict[str, Any]) -> dict[str, Any]:
    """Classify explicit machine-readable hints; preserve raw evidence unchanged."""
    raw_class = failure.get("class") or failure.get("failure_class")
    status = str(failure.get("status", ""))
    mapping = {"capability": "CAPABILITY_MISSING", "authorization": "AUTHORIZATION_REQUIRED",
               "dependency": "DEPENDENCY_BLOCKED", "verification": "VERIFICATION_FAILED",
               "security": "SECURITY_BLOCKED", "provider": "PROVIDER_FAILURE",
               "repository": "REPOSITORY_DRIFT", "input": "INPUT_AMBIGUOUS"}
    candidate = str(raw_class).upper() if raw_class else mapping.get(status.lower(), "UNKNOWN")
    classification = candidate if candidate in FAILURE_CLASSES else "UNKNOWN"
    confidence = "explicit" if raw_class and classification != "UNKNOWN" else ("status" if classification != "UNKNOWN" else "low")
    return {"class": classification, "confidence": confidence, "raw_evidence": dict(failure)}


def evidence_records(evidence: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Normalize provenance/freshness; assertions are never execution evidence."""
    records = []
    for item in evidence or []:
        record = dict(item)
        source = str(record.get("source", "UNKNOWN"))
        record["source"] = source
        record["execution_evidence"] = source in EXECUTION_EVIDENCE_SOURCES
        record["freshness"] = record.get("freshness", "UNSPECIFIED")
        records.append(record)
    return records


def analyze(tasks: list[dict[str, Any]], events: list[dict[str, Any]] | None = None,
            failures: list[dict[str, Any]] | None = None,
            evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    graph = build_graph(tasks)
    return {"protocol_version": "P12-OI-v3", "task_count": len(graph),
            "cycle_detected": has_cycle(graph),
            "nodes": [{"id": n.id, "status": n.status, "dependencies": list(n.dependencies),
                       "priority": n.priority, "effort": n.effort, "age_days": n.age_days,
                       "deadline_days": n.deadline_days} for n in graph.values()],
            "readiness": readiness(graph), "priority": priority_analysis(graph),
            "checkpoints": checkpoint_signals(events),
            "failures": [classify_failure(x) for x in failures or []],
            "evidence": evidence_records(evidence)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file containing tasks and optional events/failures/evidence")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    payload_in = json.loads(open(args.input, encoding="utf-8").read())
    if isinstance(payload_in, dict):
        tasks, events = payload_in.get("tasks", []), payload_in.get("events", [])
        failures, evidence = payload_in.get("failures", []), payload_in.get("evidence", [])
    else:
        tasks, events, failures, evidence = payload_in, [], [], []
    payload = json.dumps(analyze(tasks, events, failures, evidence), indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
