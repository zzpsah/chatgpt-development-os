#!/usr/bin/env python3
"""Adversarial claim/provenance regressions for the read-only readiness ledger."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("readiness_evidence", ROOT / "tools/verify-readiness-evidence.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReadinessEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = mod.read_json(ROOT / "config/readiness-evidence.json")

    def reject(self, expected):
        errors = mod.validate(self.data)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_checked_in_matrix_valid(self):
        self.assertEqual(mod.validate(self.data), [])

    def test_cannot_promote_production(self):
        self.data['production_ready'] = True
        self.reject('production_ready')

    def test_boolean_not_integer(self):
        self.data['production_ready'] = 0
        self.reject('production_ready')

    def test_no_authority_from_matrix(self):
        self.data['authorization'] = 'ALREADY_GRANTED'
        self.reject('authorization')

    def test_missing_family(self):
        self.data['capabilities'].pop()
        self.reject('missing capability')

    def test_duplicate_family(self):
        self.data['capabilities'].append(copy.deepcopy(self.data['capabilities'][0]))
        self.reject('duplicate capability')

    def test_missing_limitations(self):
        self.data['capabilities'][0]['limitations'] = []
        self.reject('limitations')

    def test_missing_boundary(self):
        self.data['capabilities'][0]['security_boundary'] = ''
        self.reject('security_boundary')

    def test_archive_tamper(self):
        self.data['archive_sha256'] = '0' * 64
        self.reject('archive hash')

    def test_snapshot_drift(self):
        self.data['snapshot_head'] = 'f' * 40
        self.reject('snapshot head')

    def test_path_escape(self):
        self.data['archive'] = '../secret.json'
        self.reject('escapes')

    def test_no_current_claim_from_old_run(self):
        self.data['capabilities'][0]['evidence'][0]['freshness'] = 'current'
        self.reject('historical')

    def test_wrong_ci_head(self):
        self.data['capabilities'][1]['evidence'][0]['source_head'] = 'f' * 40
        self.reject('CI run success/head')

    def test_invented_ci_run(self):
        self.data['capabilities'][1]['evidence'][0]['run_id'] = 1
        self.reject('CI run success/head')

    def test_unexecuted_local_corpus(self):
        self.data['capabilities'][0]['evidence'][0]['test'] = 'tools/test-foundation-value-audit.py'
        self.reject('successful archived local check')

    def test_fake_live_evidence(self):
        row = self.data['capabilities'][-2]
        row['evidence'][0]['level'] = 'live_provider'
        row['verification_levels'] = ['live_provider']
        self.reject('unsupported evidence level')

    def test_simulation_cannot_be_real(self):
        row = self.data['capabilities'][-2]
        row['evidence'][0]['level'] = 'real_read_only'
        row['verification_levels'] = ['real_read_only']
        self.reject('cannot establish external')

    def test_live_mutation_flag_blocked(self):
        self.data['capabilities'][-2]['live_mutation_proven'] = True
        self.reject('promotion')

    def test_planned_cannot_have_proof(self):
        self.data['capabilities'][0]['implementation'] = 'planned'
        self.reject('cannot claim proof')

    def test_declared_levels_need_evidence(self):
        self.data['capabilities'][0]['verification_levels'].append('integrated')
        self.reject('exactly match')

    def test_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('{"production_ready":false,"production_ready":true}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'duplicate JSON'):
                mod.read_json(path)

    def test_missing_source_rejected(self):
        self.data['capabilities'][0]['implementation_refs'] = ['tools/not-present.py']
        self.reject('missing or escaping')

    def test_unknown_claim_field(self):
        self.data['capabilities'][0]['production_certified'] = True
        self.reject('unknown capability fields')

    def test_wrong_workflow(self):
        self.data['capabilities'][1]['evidence'][0]['workflow'] = '.github/workflows/context-sync.yml'
        self.reject('not covered')

    def test_changed_test_cannot_reuse_evidence(self):
        original = mod.file_in_root
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / 'test-devos-bootstrap.py'
            changed.write_text('print("unverified replacement")\n',encoding='utf-8')
            def resolve(root, value):
                if value == 'tools/test-devos-bootstrap.py':
                    return changed
                return original(root, value)
            with patch.object(mod, 'file_in_root', side_effect=resolve):
                self.reject('test differs from archived source')


if __name__ == '__main__':
    unittest.main()
