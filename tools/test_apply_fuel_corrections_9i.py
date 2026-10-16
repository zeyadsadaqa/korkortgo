"""Independent exact-rational arithmetic, stage scope and snapshot input checks."""
import copy
from fractions import Fraction
from pathlib import Path
import re
import unittest
from apply_fuel_corrections_9i import ROOT, BASE, ACTIONS, IDS, BATCHES, outputs, read
from apply_sign_rewrites_9e import build
from apply_scenario_corrections_9g import IDS as SCENARIO_IDS
from apply_load_clarifications_9h import IDS as LOAD_IDS
from compile_curriculum import Validator
class FuelCorrectionsTest(unittest.TestCase):
 def test_only_ten_authorized_changes_after_9h(self):
  before=build(12)[0];after=read(Path('content/questions.json'))
  changed=[a['id'] for a,b in zip(before,after) if a!=b and a['id'] not in SCENARIO_IDS+LOAD_IDS]
  self.assertEqual(set(IDS),set(changed));self.assertEqual(10,len(changed))
  self.assertEqual([q['id'] for q in before],[q['id'] for q in after])
 def test_independent_fraction_calculation_full_feedback_and_revision(self):
  validator=Validator();actions={q['question_id']:q for q in read(ACTIONS)['questions']}
  for row in read(Path('content/questions.json')):
   if row['id'] not in IDS:continue
   q=row['assessment'];validator.typed(q,'AssessmentQuestion',row['id'])
   plain=copy.deepcopy(row);plain.pop('assessment')
   self.assertEqual(actions[row['id']]['proposed_changes']['draft_question'],plain)
   nums=re.findall(r'\d+(?:\.\d+)?',row['prompt'])
   rate,distance=(Fraction(nums[0]),Fraction(nums[2]))
   exact=rate*distance/100
   vals=[Fraction(o['text'].split()[0]) for o in row['options']]
   self.assertEqual(1,vals.count(exact));self.assertEqual(exact,vals[row['correct']])
   self.assertEqual(q['options'][row['correct']]['id'],q['feedback']['correct_option_id'])
   revision='fuel-exact-r2' if row['id'] in IDS[:4] else 'fuel-unit-r2'
   self.assertEqual(revision,q['key']['revision'])
   self.assertEqual(row['explanation'],q['feedback']['explanation'][0]['text'])
   for option,feedback in zip(row['options'],q['feedback']['option_feedback']):self.assertEqual(option['explanation'],feedback['explanation'][0]['text'])
 def test_exactly_five_stage_boundaries_and_before_after(self):
  live={q['id']:q for q in read(Path('content/questions.json'))};actions={q['question_id']:q for q in read(ACTIONS)['questions']}
  prior={qid:actions[qid]['original'] for qid in IDS}
  for step,ids in enumerate(BATCHES,1):
   receipt=read(BASE/f'9I{step}'/'question-acceptance.json');self.assertEqual(ids,receipt['question_ids'])
   after=copy.deepcopy(prior)
   for result,qid in zip(receipt['questions'],ids):
    self.assertEqual(actions[qid]['original'],result['before']);self.assertEqual(live[qid],result['after'])
    self.assertEqual(step<5,result['arithmetic']['numeric_key_changed']);after[qid]=live[qid]
   self.assertEqual(ids,[qid for qid in IDS if after[qid]!=prior[qid]])
   prior=after
 def test_reproduction_and_rewind_protection(self):
  for path,value in outputs().items():self.assertEqual((ROOT/path).read_text(),value,str(path))
  with self.assertRaises(AssertionError):outputs(1)
if __name__=='__main__':unittest.main()
