#!/usr/bin/env python3
"""Deterministic P12 task-graph and readiness analysis."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any


TERMINAL = {"COMPLETE"}
BLOCKED = {"BLOCKED", "FAILED", "ESCALATED", "NEEDS_APPROVAL"}


@dataclass(frozen=True)
class Node:
    id: str
    status: str
    dependencies: tuple[str, ...]
    priority: int


def build_graph(tasks: list[dict[str, Any]]) -> dict[str, Node]:
    graph: dict[str, Node] = {}
    for raw in tasks:
        task_id = str(raw["id"])
        if task_id in graph:
            raise ValueError(f"duplicate task id: {task_id}")
        deps = tuple(str(x) for x in raw.get("dependencies", []))
        graph[task_id] = Node(
            id=task_id,
            status=str(raw.get("status", "PLANNED")),
            dependencies=deps,
            priority=int(raw.get("priority", 0)),
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

    return any(visit(node_id) for node_id in graph)


def readiness(graph: dict[str, Node]) -> list[dict[str, Any]]:
    if has_cycle(graph):
        return [{"id": node.id, "readiness": "BLOCKED", "reason": "DEPENDENCY_CYCLE"} for node in graph.values()]
    result = []
    for node in graph.values():
        if node.status in TERMINAL:
            state, reason = "COMPLETE", "TASK_COMPLETE"
        elif node.status in BLOCKED:
            state, reason = "BLOCKED", node.status
        else:
            unfinished = [d for d in node.dependencies if graph[d].status not in TERMINAL]
            if unfinished:
                state, reason = "WAITING", "DEPENDENCIES_UNSATISFIED"
            else:
                state, reason = "READY", "DEPENDENCIES_SATISFIED"
        result.append({"id": node.id, "readiness": state, "reason": reason, "priority": node.priority})
    return sorted(result, key=lambda x: (-x.get("priority", 0), x["id"]))


def analyze(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    graph = build_graph(tasks)
    return {
        "protocol_version": "P12-OI-v1",
        "task_count": len(graph),
        "cycle_detected": has_cycle(graph),
        "nodes": [
            {
                "id": n.id,
                "status": n.status,
                "dependencies": list(n.dependencies),
                "priority": n.priority,
            }
            for n in graph.values()
        ],
        "readiness": readiness(graph),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file containing a list of task objects")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    tasks = json.loads(open(args.input, encoding="utf-8").read())
    result = analyze(tasks)
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
