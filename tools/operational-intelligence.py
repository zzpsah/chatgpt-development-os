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
    "REPOSITORY_CHANGE",
    "WORK_UNIT_COMPLETE",
    "WORK_UNIT_FAILED",
    "BLOCKED_TRANSITION",
    "AUTHORIZATION_CHANGE",
    "VERIFICATION_RESULT",
    "SECURITY_RESULT",
    "SESSION_BOUNDARY",
    "HANDOFF_BOUNDARY",
}


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
        graph[task_id] = Node(
            id=task_id,
            status=str(raw.get("status", "PLANNED")),
            dependencies=deps,
            priority=int(raw.get("priority", 0)),
            effort=max(0, int(raw.get("effort", 0))),
            age_days=max(0, int(raw.get("age_days", 0))),
            deadline_days=None if deadline is None else int(deadline),
        )
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
        for dep in graph[node_id].dependencies:
            if visit(dep):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node_id) for node_id in sorted(graph))


def readiness(graph: dict[str, Node]) -> list[dict[str, Any]]:
    if has_cycle(graph):
        return [
            {"id": node.id, "readiness": "BLOCKED", "reason": "DEPENDENCY_CYCLE", "priority": node.priority}
            for node in sorted(graph.values(), key=lambda n: n.id)
        ]
    result = []
    for node in graph.values():
        if node.status in TERMINAL:
            state, reason = "COMPLETE", "TASK_COMPLETE"
        elif node.status in BLOCKED:
            state, reason = "BLOCKED", node.status
        elif node.status in UNAUTHORIZED:
            state, reason = "UNAUTHORIZED", "AUTHORIZATION_REQUIRED"
        else:
            unfinished = [d for d in node.dependencies if graph[d].status not in TERMINAL]
            if unfinished:
                state, reason = "WAITING", "DEPENDENCIES_UNSATISFIED"
            else:
                state, reason = "READY", "DEPENDENCIES_SATISFIED"
        result.append({"id": node.id, "readiness": state, "reason": reason, "priority": node.priority})
    return sorted(result, key=lambda x: (-x.get("priority", 0), x["id"]))


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
        criticality = dependents[node.id]
        if criticality:
            score += criticality * 20
            reasons.append(f"dependent_count={criticality}")
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
        if kind not in VALID_CHECKPOINT_EVENTS:
            signals.append({"checkpoint": False, "reason": "UNRECOGNIZED_EVENT", "event": kind})
            continue
        signals.append({"checkpoint": True, "reason": kind, "event": kind})
    return signals


def analyze(tasks: list[dict[str, Any]], events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    graph = build_graph(tasks)
    return {
        "protocol_version": "P12-OI-v2",
        "task_count": len(graph),
        "cycle_detected": has_cycle(graph),
        "nodes": [
            {
                "id": n.id,
                "status": n.status,
                "dependencies": list(n.dependencies),
                "priority": n.priority,
                "effort": n.effort,
                "age_days": n.age_days,
                "deadline_days": n.deadline_days,
            }
            for n in graph.values()
        ],
        "readiness": readiness(graph),
        "priority": priority_analysis(graph),
        "checkpoints": checkpoint_signals(events),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file containing a list of task objects")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    payload_in = json.loads(open(args.input, encoding="utf-8").read())
    tasks = payload_in.get("tasks", payload_in) if isinstance(payload_in, (dict, list)) else []
    events = payload_in.get("events", []) if isinstance(payload_in, dict) else []
    payload = json.dumps(analyze(tasks, events), indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
