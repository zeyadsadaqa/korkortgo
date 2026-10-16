"""Check all 9E batch boundaries and the complete generated bank against approved proposals."""
import copy
import json
import unittest
from pathlib import Path
from apply_sign_rewrites_9e import build, ids, read, ROOT, dump, split_kotlin
from compile_curriculum import Validator

class AllSignRewritesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stages={n:build(n) for n in range(2,13)}
        cls.live=read(Path('content/questions.json'))
        # Later 9G/9H/9I changes have independent scope tests; compare 9E with its frozen stage.
        from apply_scenario_corrections_9g import IDS as SCENARIO_IDS
        from apply_load_clarifications_9h import IDS as LOAD_IDS
        from apply_fuel_corrections_9i import IDS as FUEL_IDS
        IDS=SCENARIO_IDS+LOAD_IDS+FUEL_IDS
        original={q['id']:q for q in cls.stages[12][0]}
        cls.live=[original[q['id']] if q['id'] in IDS else q for q in cls.live]
        cls.actions={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/question-actions.json'))['questions']}
    def test_each_batch_changes_only_exact_backlog_ids(self):
        for n in range(3,13):
            with self.subTest(batch=n):
                before=self.stages[n-1][0];after=self.stages[n][0]
                self.assertEqual(ids(n),[a['id'] for a,b in zip(before,after) if a!=b])
                self.assertEqual([q['id'] for q in before],[q['id'] for q in after])
    def test_final_bank_and_generated_kotlin_reproduce(self):
        self.assertEqual(self.live,self.stages[12][0])
        for path,value in split_kotlin(self.stages[12][1]).items():
            live=(ROOT/path).read_text()
            if path.name=='Bank.kt':
                from apply_scenario_corrections_9g import IDS as SCENARIO_IDS
                from apply_load_clarifications_9h import IDS as LOAD_IDS
                from apply_fuel_corrections_9i import IDS as FUEL_IDS
                IDS=SCENARIO_IDS+LOAD_IDS+FUEL_IDS
                original_lines={line.split(',',1)[0]:line for line in value.splitlines(True) if line.startswith('Question(')}
                live=''.join(original_lines[line.split(',',1)[0]] if any(line.startswith('Question(\"'+qid+'\",') for qid in IDS) else line for line in live.splitlines(True))
            self.assertEqual(live,value)
    def test_all_578_rewrites_and_422_untouched(self):
        baseline=read(Path('docs/curriculum/app-migration/implementation-evidence/9E1/incoming-questions.json'))
        expected=[q['id'] for q in baseline if q['id'].startswith(('sign-meaning-','sign-recognise-')) and self.actions[q['id']]['disposition']=='rewrite']
        self.assertEqual(578,len(expected))
        self.assertEqual(expected,[a['id'] for a,b in zip(baseline,self.live) if a!=b])
        self.assertEqual(422,sum(a==b for a,b in zip(baseline,self.live)))
    def test_exact_proposals_all_options_keys_and_sources(self):
        for row in self.live:
            if not row.get('assessment'):continue
            q=row['assessment'];p=self.actions[row['id']]['proposed_changes']
            with self.subTest(question=row['id']):
                self.assertEqual(p['prompt'],row['prompt'])
                self.assertEqual('rewrite-r2',q['key']['revision'])
                self.assertEqual(row['concept'],q['concept_id'])
                self.assertEqual(p['post_answer_explanation'],q['feedback']['explanation'][0]['text'])
                for o,f,a in zip(q['options'],q['feedback']['option_feedback'],p['options']):
                    self.assertEqual(a['option_id'],o['id']);self.assertEqual(o['id'],f['option_id'])
                    self.assertEqual(a['meaning_option_text'] or '',o['text'][0]['text'] if o['text'] else '')
                    self.assertEqual(a['post_answer_explanation'],f['explanation'][0]['text'])
                    self.assertEqual(a['post_answer_label'],f['english_label'])
                    self.assertEqual(a['code_metadata_after_reveal'],f['sign_code'])
                    self.assertEqual(a['is_correct'],o['id']==q['feedback']['correct_option_id'])
                self.assertEqual(q['options'][row['correct']]['id'],q['feedback']['correct_option_id'])
    def test_all_images_and_descriptions_are_typed_exact_files(self):
        validator=Validator()
        for row in self.live:
            if row.get('assessment'):validator.typed(row['assessment'],'AssessmentQuestion',row['id'])
    def test_paired_distractors_consistent(self):
        pairs={}
        for row in self.live:
            if row.get('assessment'):pairs.setdefault(row['concept'],[]).append(row['assessment'])
        self.assertEqual(289,len(pairs))
        for pair in pairs.values():
            self.assertEqual(2,len(pair))
            self.assertEqual([f['sign_code'] for f in pair[0]['feedback']['option_feedback']],[f['sign_code'] for f in pair[1]['feedback']['option_feedback']])
    def test_all_rewrites_are_held_without_delivery_proof(self):
        for row in self.live:
            if not row.get('assessment'):continue
            a=row['assessment']['acceptance']
            self.assertEqual('held',a['eligibility']);self.assertTrue(a['open_holds']);self.assertEqual([],a['delivery_proof'])
    def test_separate_batch_outputs_reproduce(self):
        for n in range(2,13):
            base=Path(f'docs/curriculum/app-migration/implementation-evidence/9E{n}')
            _,_,q,a,d=self.stages[n]
            self.assertEqual(q,read(base/'questions.json'));self.assertEqual(a,read(base/'batch-acceptance.json'))
            self.assertEqual(d,(ROOT/base/'before-after.diff').read_text())
            self.assertEqual(len(ids(n)),d.count('--- sign-'))
if __name__=='__main__':unittest.main()
