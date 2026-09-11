#!/usr/bin/env python3
"""Verify the Development OS auto-onboarding contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    p = ROOT / path
    assert p.exists(), f"missing required file: {path}"
    return p.read_text(encoding="utf-8")


def require(text: str, needle: str, source: str) -> None:
    assert needle in text, f"missing {needle!r} in {source}"


def main() -> None:
    docs = read("docs/AUTO-ONBOARDING.md")
    onboarding = read("tools/onboard-project.ps1")
    initializer = read("tools/init-project.ps1")
    health = read("tools/check-project.ps1")
    detection = read("automation/detection-policy.md")
    bootstrap = read("core/ai-bootstrap-protocol.md")
    roadmap = read("docs/ROADMAP.md")

    for term in [
        "Existing-repository flow",
        "Preservation rule",
        "Context generation boundary",
        "GitHub-side versus local automation",
        "Completion criterion",
    ]:
        require(docs, term, "docs/AUTO-ONBOARDING.md")

    for term in [
        "DryRun", "init-project.ps1", "context-sync.yml",
        "Existing caller preserved.", "Existing .ai files were preserved.",
    ]:
        require(onboarding, term, "tools/onboard-project.ps1")

    for term in [
        "Write-IfMissing", "AGENTS.md", ".ai/manifest.yaml",
        ".ai/STATE-INDEX.md", ".ai/PROJECT.md", ".ai/CURRENT-STATE.md",
        ".ai/DECISIONS.md", ".ai/TASKS.md",
    ]:
        require(initializer, term, "tools/init-project.ps1")

    for term in [
        "AGENTS.md", ".ai\\manifest.yaml", ".ai\\STATE-INDEX.md",
        ".ai\\PROJECT.md", ".ai\\CURRENT-STATE.md", ".github\\workflows\\context-sync.yml",
    ]:
        require(health, term, "tools/check-project.ps1")

    for term in [
        "configured project root", "Existing project files and existing `.ai/` content are preserved",
        "Never overwrite existing project context automatically", "Never modify application source",
    ]:
        require(detection, term, "automation/detection-policy.md")

    require(bootstrap, "Vendor independence", "core/ai-bootstrap-protocol.md")
    require(bootstrap, "Missing or incomplete context", "core/ai-bootstrap-protocol.md")

    for item in [
        "[x] Existing-repository onboarding flow",
        "[x] Onboarding script/workflow",
        "[x] Context validation",
        "[x] Preserve existing context; no destructive overwrite",
        "[x] GitHub-side versus local automation boundaries",
    ]:
        require(roadmap, item, "docs/ROADMAP.md")

    print("Auto-onboarding contract checks passed.")


if __name__ == "__main__":
    main()
