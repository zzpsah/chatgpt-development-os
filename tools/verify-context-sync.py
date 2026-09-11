#!/usr/bin/env python3
"""Verify the Development OS durable-context synchronization contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "context-sync.yml"
CALLER = ROOT / "templates" / "project" / ".github" / "workflows" / "context-sync.yml"
REQUIRED_CONTEXT_FILES = [
    "manifest.yaml", "PROJECT.md", "CURRENT-STATE.md", "ARCHITECTURE.md",
    "DECISIONS.md", "TASKS.md", "STATE-INDEX.md", "CHANGELOG.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(WORKFLOW.is_file(), "reusable context-sync workflow is missing")
    require(CALLER.is_file(), "project caller template is missing")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    caller = CALLER.read_text(encoding="utf-8")

    require("workflow_call:" in workflow, "context-sync must be reusable via workflow_call")
    require("contents: write" in workflow, "context-sync must request contents write permission")
    require("actions/checkout@v4" in workflow, "context-sync must inspect repository history")
    require("fetch-depth: 0" in workflow, "context-sync must fetch full Git history")
    require("[devos-context-sync]" in workflow, "context-sync must prevent recursive synchronization")
    require("STATE-INDEX.md" in workflow, "context-sync must generate STATE-INDEX.md")
    require("CHANGELOG.md" in workflow, "context-sync must maintain CHANGELOG.md")
    require("CURRENT-STATE.md" in workflow, "context-sync must update meaningful current-state facts")
    require("git diff --name-only" in workflow, "context-sync must derive changed paths from Git")
    require("git push" in workflow, "context-sync must persist generated context")
    require("MEANINGFUL_PATTERNS" in workflow, "meaningful path input must be wired into the workflow")
    require("case \"$file\" in" not in workflow, "meaningful path classification must not silently ignore its configured input")
    require("zzpsah/chatgpt-development-os/.github/workflows/context-sync.yml@main" in caller, "project caller must use the reusable DevOS workflow")
    require("contents: write" in caller, "project caller must grant the reusable workflow write permission")

    template = ROOT / "templates" / "project"
    require((template / "AGENTS.md").is_file(), "project template AGENTS.md is missing")
    for name in REQUIRED_CONTEXT_FILES:
        require((template / ".ai" / name).is_file(), f"project template .ai/{name} is missing")

    print("PASS: durable context-sync contract is structurally valid")
    print("PASS: project template contains required durable context files")
    print("NOTE: this verifier does not execute GitHub Actions or project tests")


if __name__ == "__main__":
    main()
