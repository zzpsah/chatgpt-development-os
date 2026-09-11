#!/usr/bin/env python3
"""Verify the vendor-neutral DevOS AI handoff generator contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "generate-ai-handoff.py"
SPEC = ROOT / "docs" / "CROSS-AI-HANDSHAKE.md"
REQUIRED_FIELDS = (
    'protocol_version', 'project_id', 'project_name', 'repository',
    'devos_context_version', 'current_objective', 'verified_state',
    'active_work', 'blocked_work', 'recent_work', 'recommended_next_action',
    'evidence_refs', 'confidence', 'unknowns', 'generated_at'
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), 'AI handoff generator is missing')
    require(SPEC.is_file(), 'cross-AI handshake specification is missing')
    tool = TOOL.read_text(encoding='utf-8')
    spec = SPEC.read_text(encoding='utf-8')
    for field in REQUIRED_FIELDS:
        require(field in tool, f'generator missing handoff field: {field}')
        require(field in spec, f'handshake spec missing field: {field}')
    for term in ('HANDSHAKE: READY', 'HANDSHAKE: NEEDS_REVIEW', 'vendor-neutral', 'source/Git'):
        require(term in tool or term in spec, f'handshake behavior missing: {term}')
    require('.ai/manifest.yaml' in tool, 'handoff must include manifest provenance')
    require('CURRENT-STATE.md' in tool and 'TASKS.md' in tool, 'handoff must include durable state provenance')
    print('PASS: vendor-neutral AI handoff contract is structurally valid')


if __name__ == '__main__':
    main()
