#!/usr/bin/env python3
"""Verify the vendor-neutral DevOS AI handoff and provenance contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "generate-ai-handoff.py"
SPEC = ROOT / "docs" / "CROSS-AI-HANDSHAKE.md"
PROVENANCE = ROOT / "core" / "ai-handoff-provenance.md"
REQUIRED_FIELDS = (
    'protocol_version', 'project_id', 'project_name', 'repository',
    'devos_context_version', 'current_objective', 'verified_state',
    'active_work', 'blocked_work', 'recent_work', 'recommended_next_action',
    'evidence_refs', 'confidence', 'unknowns', 'generated_at', 'git_commit',
    'git_branch', 'git_status', 'generated_from', 'revalidation'
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), 'AI handoff generator is missing')
    require(SPEC.is_file(), 'cross-AI handshake specification is missing')
    require(PROVENANCE.is_file(), 'handoff provenance contract is missing')
    tool = TOOL.read_text(encoding='utf-8')
    spec = SPEC.read_text(encoding='utf-8')
    provenance = PROVENANCE.read_text(encoding='utf-8')

    for field in REQUIRED_FIELDS:
        require(field in tool, f'generator missing handoff field: {field}')
    for field in ('protocol_version', 'project_id', 'repository', 'evidence_refs', 'confidence'):
        require(field in spec, f'handshake spec missing field: {field}')
    for term in ('HANDSHAKE: READY', 'HANDSHAKE: NEEDS_REVIEW', 'vendor-neutral', 'source/Git'):
        require(term in tool or term in spec, f'handshake behavior missing: {term}')
    for term in ('git_commit', 'generated_from', 'revalidation', 'current HEAD'):
        require(term in provenance, f'provenance requirement missing: {term}')

    require('.ai/manifest.yaml' in tool, 'handoff must include manifest provenance')
    require('.ai/CURRENT-STATE.md' in tool and '.ai/TASKS.md' in tool, 'handoff must include durable state provenance')
    require('DECISIONS.md' in tool, 'handoff must include decision provenance')
    require('git rev-parse' in tool, 'handoff must capture Git commit provenance')
    require('status --porcelain' in tool, 'handoff must capture Git cleanliness')
    require('Validate material conclusions against current source and Git before acting.' in tool, 'handoff must require revalidation')
    print('PASS: vendor-neutral AI handoff contract is structurally valid')
    print('PASS: handoff provenance and revalidation contract is present')


if __name__ == '__main__':
    main()
