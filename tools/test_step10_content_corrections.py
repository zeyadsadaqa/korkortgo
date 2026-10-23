"""Correction staging must never manufacture renewed release acceptance."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import stage_step10_corrections as correction
from compile_curriculum import ContentError, Validator


class Step10CorrectionTest(unittest.TestCase):
    def test_reviewed_metadata_preserves_every_url_publisher_and_evidence_date(self):
        amendments, base, data, changed = correction.build()
        for source in ('content/sources.json', 'content/package-sources.json'):
            original = {r['id']: r for r in base['files'][source]['references']}
            after = {r['id']: r for r in data[source]['references']}
            self.assertEqual(set(original), set(after))
            amended = {r['reference_id'] for r in amendments['classifications']}
            self.assertEqual(6, len(amended))
            for key, row in after.items():
                if key in amended:
                    self.assertEqual({'classifications', 'classification_note'}, {k for k in row if row[k] != original[key][k]})
                    self.assertNotEqual(['foreign_public_authority'], row['classifications'])
                else:
                    self.assertEqual(original[key], row)

    def test_seven_changed_descriptions_are_held_and_keys_and_other_questions_unchanged(self):
        _, base, data, changed = correction.build()
        self.assertEqual(7, len(changed))
        original = {q['key']['question_id']: q for q in base['files']['content/accepted-assessment-questions.json']['questions']}
        for q in data['content/accepted-assessment-questions.json']['questions']:
            before = original[q['key']['question_id']]
            self.assertEqual(before['feedback'], q['feedback'])
            if q['key']['question_id'] in changed:
                self.assertNotEqual(before['key']['revision'], q['key']['revision'])
                self.assertEqual('held', q['acceptance']['eligibility'])
                self.assertTrue(q['acceptance']['open_holds'])
                self.assertEqual([], q['acceptance']['delivery_proof'])
            else:
                self.assertEqual(before, q)

    def test_staged_candidate_passes_fixture_validation_but_cannot_be_released(self):
        manifest = correction.load(correction.OUT / 'candidate-manifest.json')
        payloads = {r['kind']: correction.load(Path(r['file']['path'])) for r in manifest['payloads'] if r['kind'] != 'asset'}
        validator = Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json')
        self.assertEqual(1000, validator.package(payloads, manifest, 'fixture')['questions'])
        with self.assertRaisesRegex(ContentError, 'unaccepted/retired questions'):
            Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json').package(payloads, manifest, 'release')

    def test_stale_base_or_wrong_before_description_refuses_generation(self):
        read = correction.load
        for field in ('base', 'description'):
            spec = copy.deepcopy(read(correction.AUTHOR))
            if field == 'base':
                spec['base_release']['sha256'] = '0' * 64
            else:
                spec['descriptions']['X9']['before'] = 'Unreviewed replacement baseline'
            with patch.object(correction, 'load', side_effect=lambda p: spec if p == correction.AUTHOR else read(p)):
                with self.assertRaises(AssertionError):
                    correction.build()


if __name__ == '__main__':
    unittest.main()
