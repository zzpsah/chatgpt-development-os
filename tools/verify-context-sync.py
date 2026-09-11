#!/usr/bin/env python3
"""Verify the Development OS durable-context synchronization contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "context-sync.yml"
CALLER = ROOT / "templates" / "project" / ".github" / "workflows" / "context-sync.yml"
SYNC_TOOL = ROOT / "tools" / "context-sync.py"
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
    require(SYNC_TOOL.is_file(), "portable context-sync tool is missing")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    caller = CALLER.read_text(encoding="utf-8")
    tool = SYNC_TOOL.read_text(encoding="utf-8")

    require("workflow_call:" in workflow, "context-sync must be reusable via workflow_call")
    require("contents: write" in workflow, "context-sync job must request contents write permission")
    require("actions/checkout@v4" in workflow, "context-sync must inspect repositories")
    require("fetch-depth: 0" in workflow, "context-sync must fetch full project Git history")
    require("repository: zzpsah/chatgpt-development-os" in workflow, "workflow must fetch the pinned DevOS tooling repository")
    require("path: .devos" in workflow, "DevOS tooling checkout path must be isolated")
    require("tools/context-sync.py" in workflow, "workflow must execute the portable context-sync tool")
    require("DEVOS_CONTEXT_DIRECTORY" in workflow, "context directory input must be passed to the tool")
    require("DEVOS_BEFORE_SHA" in workflow, "before SHA input must be passed to the tool")
    require("DEVOS_MEANINGFUL_PATTERNS" in workflow, "meaningful path configuration must be passed to the tool")

    require('git("diff", "--name-only"' in tool, "sync tool must derive changes from Git")
    require("DEVOS_MEANINGFUL_PATTERNS" in tool, "sync tool must support configured meaningful patterns")
    require("fnmatch.fnmatchcase" in tool, "sync tool must classify meaningful paths")
    require("STATE-INDEX.md" in tool, "sync tool must generate STATE-INDEX.md")
    require("CHANGELOG.md" in tool, "sync tool must generate CHANGELOG.md")
    require("CURRENT-STATE.md" in tool, "sync tool must update meaningful current state")
    require("development-os[bot]" in tool, "sync tool must use a dedicated bot identity")
    require("chore: sync project AI context [devos-context-sync]" in tool, "sync tool must use a recursion-identifying commit message")
    require("git push" in tool, "sync tool must persist generated context")

    require("zzpsah/chatgpt-development-os/.github/workflows/context-sync.yml@main" in caller, "project caller must use the reusable DevOS workflow")
    require("contents: write" in caller, "project caller must grant the reusable workflow write permission")

    template = ROOT / "templates" / "project"
    require((template / "AGENTS.md").is_file(), "project template AGENTS.md is missing")
    for name in REQUIRED_CONTEXT_FILES:
        require((template / ".ai" / name).is_file(), f"project template .ai/{name} is missing")

    print("PASS: durable context-sync workflow contract is structurally valid")
    print("PASS: portable context-sync tool contract is structurally valid")
    print("PASS: project template contains required durable context files")
    print("NOTE: this verifier does not execute GitHub Actions or project tests")


if __name__ == "__main__":
    main()
