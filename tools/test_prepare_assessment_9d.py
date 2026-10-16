"""Independent coverage/identity checks for the reviewed 9D deliverables."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import prepare_assessment_9d as assessment


class AssessmentPreparationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = assessment.outputs()
        cls.actions = assessment.read(assessment.ACTIONS)['questions']
        cls.batches = [b for b in assessment.read(assessment.BACKLOG)['execution_batches'] if b['work_item_id'] == '9D']

    def test_exact_batches_cover_616_questions_once(self):
        actual = []
        for batch in self.batches:
            path = assessment.BASE/f"9D{batch['batch']+2}/description-acceptance.json"
            record = self.files[path]
            self.assertEqual(batch['question_ids'], [q['question_id'] for q in record['questions']])
            self.assertLessEqual(record['question_count'], 50)
            actual.extend(q['question_id'] for q in record['questions'])
        expected = {q['question_id'] for q in self.actions if q['question_id'].startswith('sign-')}
        self.assertEqual(616, len(actual))
        self.assertEqual(expected, set(actual))

    def test_all_original_keys_and_sign_authored_ids_survive(self):
        records = self.files[assessment.BASE/'9D1/authored-identities.json']['questions']
        self.assertEqual(len(self.actions), len(records))
        for action, record in zip(self.actions, records):
            self.assertEqual(action['question_id'], record['question_id'])
            self.assertEqual(record['option_ids_in_authored_order'][action['original']['correct']], record['correct_option_id'])
            self.assertEqual('legacy-r1', record['baseline_semantic_revision'])
            if action['question_id'].startswith('sign-'):
                self.assertEqual([o['option_id'] for o in action['proposed_changes']['options']], record['option_ids_in_authored_order'])

    def test_1540_exact_image_occurrences_and_distinct_recognition_choices(self):
        total = 0
        for path, batch in self.files.items():
            if path.name != 'description-acceptance.json':
                continue
            for question in batch['questions']:
                images = question['images']
                total += len(images)
                self.assertEqual(4 if 'recognise' in question['question_id'] else 1, len(images))
                self.assertEqual(len(images), len({i['asset']['sha256'] for i in images}))
                self.assertTrue(all(i['description'] and i['review']['proof_sheet']['sha256'] for i in images))
                self.assertFalse(question['scored_activation'])
                if 'recognise' in question['question_id']:
                    self.assertTrue(all(o['pre_answer_text'] == '' for o in question['options']))
        self.assertEqual(1540, total)

    def test_308_descriptions_have_exact_source_byte_bindings_and_manual_authoring(self):
        library = self.files[assessment.BASE/'9D2/reviewed-descriptions.json']
        self.assertEqual(308, len(library['assets']))
        for asset in library['assets']:
            self.assertEqual(assessment.sha(Path(asset['asset']['path'])), asset['asset']['sha256'])
            self.assertNotIn('Study alt', asset['text'])
            self.assertFalse(asset['scored_activation'])

    def test_all_38_question_holds_remain_unreleased(self):
        baseline = assessment.read(Path('docs/curriculum/app-migration/verification.json'))['question_asset_holds']
        target_ids = {hold['question_id'] for hold in baseline}
        held = [q for p, b in self.files.items() if p.name == 'description-acceptance.json' for q in b['questions'] if q['question_id'] in target_ids]
        self.assertEqual(38, len(held))
        self.assertTrue(all(q['open_delivery_holds'] and not q['scored_activation'] for q in held))

    def test_missing_or_drifted_exact_asset_is_rejected(self):
        original = assessment.read
        def drift(path):
            data = original(path)
            if path == assessment.ACTIONS:
                q = next(q for q in data['questions'] if q['question_id'] == 'sign-meaning-A1')
                q['proposed_changes']['question_image_asset']['sha256'] = '0'*64
            return data
        with patch.object(assessment, 'read', side_effect=drift):
            with self.assertRaises(AssertionError):
                assessment.outputs()

    def test_saved_outputs_are_reproducible(self):
        for path, data in self.files.items():
            self.assertEqual(json.dumps(data, ensure_ascii=False, indent=2)+'\n', (assessment.ROOT/path).read_text())


if __name__ == '__main__':
    unittest.main()
