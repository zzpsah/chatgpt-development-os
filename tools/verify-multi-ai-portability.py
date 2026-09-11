#!/usr/bin/env python3
"""Verify the Development OS multi-AI portability contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    p = ROOT / path
    assert p.exists(), f"missing required file: {path}"
    return p.read_text(encoding="utf-8")


def require(text: str, needle: str, source: str) -> None:
    assert needle in text, f"missing {needle!r} in {source}"


def main() -> None:
    contract = read("adapters/adapter-contract.md")
    portability = read("docs/MULTI-AI-PORTABILITY.md")
    bootstrap = read("core/ai-bootstrap-protocol.md")
    chatgpt = read("adapters/chatgpt.md")
    codex = read("adapters/codex.md")

    for name in ["AGENTS.md", ".ai/manifest.yaml", ".ai/STATE-INDEX.md", ".ai/PROJECT.md", ".ai/CURRENT-STATE.md"]:
        require(contract, name, "adapters/adapter-contract.md")
        require(portability, name, "docs/MULTI-AI-PORTABILITY.md")

    for term in [
        "Project discovery", "Bootstrap", "Inspection", "Intent routing",
        "State resolution", "Execution", "Verification", "Persistence",
        "Observed / Likely / Unknown", "VERIFIED / PARTIAL / UNVERIFIED / FAILED",
        "authorization", "Security Gate", "secrets", "previous AI",
    ]:
        require(contract, term, "adapters/adapter-contract.md")

    require(contract, "project must remain understandable and recoverable from the repository", "adapters/adapter-contract.md")
    for term in ["Repository-only recovery", "Vendor/account independence", "Adapter boundary", "Portability test"]:
        require(portability, term, "docs/MULTI-AI-PORTABILITY.md")

    for term in ["Vendor independence", "Bootstrap sequence", "State authority", "Evidence discipline", "Persistence contract"]:
        require(bootstrap, term, "core/ai-bootstrap-protocol.md")

    require(chatgpt, "durable project state in the project repository", "adapters/chatgpt.md")
    require(codex, "same project-level `AGENTS.md`, `.ai/` context, decisions, tasks, and workflow artifacts", "adapters/codex.md")
    require(codex, "repository remains the durable source of project context and implementation history", "adapters/codex.md")

    print("Multi-AI portability contract checks passed.")


if __name__ == "__main__":
    main()
