import json
import unittest
from pathlib import Path
from apply_sign_rewrite_9e2 import build,ids,ROOT,BASE,read,digest,guard_current
from compile_curriculum import Validator

class SignRewriteBatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.bank,cls.kotlin,cls.payload,cls.acceptance,cls.diff=build()
    def test_exact_50_only_and_order_preserved(self):
        before=read(BASE/'incoming-questions.json')
        self.assertEqual([q['id'] for q in before],[q['id'] for q in self.bank])
        changed=[a['id'] for a,b in zip(before,self.bank) if a!=b]
        self.assertEqual(ids(),changed)
        self.assertEqual(950,sum(a==b for a,b in zip(before,self.bank)))
    def test_exact_7d_stem_options_key_and_feedback(self):
        proposals={q['question_id']:q['proposed_changes'] for q in read(Path('docs/curriculum/app-migration/question-actions.json'))['questions']}
        for q in self.payload['questions']:
            p=proposals[q['key']['question_id']]
            self.assertEqual(p['prompt'],q['prompt'][0]['text'])
            self.assertEqual('rewrite-r2',q['key']['revision'])
            for o,f,proposal in zip(q['options'],q['feedback']['option_feedback'],p['options']):
                self.assertEqual(proposal['option_id'],o['id']);self.assertEqual(o['id'],f['option_id'])
                self.assertEqual(proposal['post_answer_explanation'],f['explanation'][0]['text'])
                self.assertEqual(proposal['code_metadata_after_reveal'],f['sign_code'])
                self.assertEqual(proposal['post_answer_label'],f['english_label'])
                self.assertEqual(proposal['is_correct'],o['id']==q['feedback']['correct_option_id'])
    def test_all_50_remain_held_with_no_delivery_proof(self):
        self.assertEqual(50,len(self.payload['questions']))
        for q in self.payload['questions']:
            self.assertEqual('held',q['acceptance']['eligibility'])
            self.assertTrue(q['acceptance']['open_holds']);self.assertEqual([],q['acceptance']['delivery_proof'])
    def test_typed_contract_and_exact_asset_bindings(self):
        validator=Validator()
        for q in self.payload['questions']:validator.typed(q,'AssessmentQuestion',q['key']['question_id'])
    def test_paired_directions_share_distractors(self):
        for concept in {q['concept_id'] for q in self.payload['questions']}:
            pair=[q for q in self.payload['questions'] if q['concept_id']==concept]
            self.assertEqual(2,len(pair))
            self.assertEqual([f['sign_code'] for f in pair[0]['feedback']['option_feedback']],[f['sign_code'] for f in pair[1]['feedback']['option_feedback']])
    def test_unrelated_current_edits_cannot_be_overwritten(self):
        guard_current('before','before','after')
        guard_current('after','before','after')
        with self.assertRaisesRegex(ValueError,'Refusing to overwrite'):
            guard_current('user edit','before','after')
    def test_saved_outputs_and_diff_are_exact(self):
        live={q['id']:q for q in read(Path('content/questions.json'))}
        for q in self.bank:
            if q.get('assessment'):self.assertEqual(q,live[q['id']])
        self.assertEqual(self.acceptance,read(BASE/'batch-acceptance.json'))
        self.assertEqual(50,self.diff.count('--- sign-'))
if __name__=='__main__':unittest.main()
