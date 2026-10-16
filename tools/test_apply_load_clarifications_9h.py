"""Verify six exact batch boundaries, prompt inputs, keys and every explanation."""
import copy
import re
import unittest
from pathlib import Path
from apply_load_clarifications_9h import ROOT, BASE, ACTIONS, IDS, BATCHES, read, outputs
from compile_curriculum import Validator
from apply_sign_rewrites_9e import build
from apply_scenario_corrections_9g import IDS as SCENARIO_IDS
from apply_fuel_corrections_9i import IDS as FUEL_IDS
class LoadClarificationsTest(unittest.TestCase):
 def test_only_thirty_authorized_records_change_after_9g(self):
  before=build(12)[0];after=read(Path('content/questions.json'))
  self.assertEqual(IDS,[a['id'] for a,b in zip(before,after) if a!=b and a['id'] not in SCENARIO_IDS+FUEL_IDS])
  self.assertEqual([q['id'] for q in before],[q['id'] for q in after])
 def test_six_batch_boundaries_and_exact_proposals(self):
  actions={q['question_id']:q for q in read(ACTIONS)['questions']};live={q['id']:q for q in read(Path('content/questions.json'))}
  prior={q['id']:copy.deepcopy(q) for q in live.values()}
  for qid in IDS:prior[qid]=actions[qid]['original']
  for batch,ids in enumerate(BATCHES,1):
   receipt=read(BASE/f'9H{batch}'/'question-acceptance.json');self.assertEqual(ids,receipt['question_ids'])
   next_stage=copy.deepcopy(prior)
   for result,qid in zip(receipt['questions'],ids):
    self.assertEqual(actions[qid]['original'],result['before']);self.assertEqual(live[qid],result['after'])
    row=copy.deepcopy(live[qid]);row.pop('assessment')
    self.assertEqual(actions[qid]['proposed_changes']['draft_question'],row)
    next_stage[qid]=live[qid]
   self.assertEqual(ids,[qid for qid in IDS if prior[qid]!=next_stage[qid]])
   prior=next_stage
 def test_independent_arithmetic_and_feedback(self):
  validator=Validator()
  for row in read(Path('content/questions.json')):
   if row['id'] not in IDS:continue
   q=row['assessment'];validator.typed(q,'AssessmentQuestion',row['id'])
   total,ready=map(int,re.findall(r'(\d+) kg',row['prompt']));expected=total-ready
   values=[int(o['text'].removesuffix(' kg')) for o in row['options']]
   self.assertEqual(1,values.count(expected));self.assertEqual(expected,values[row['correct']])
   self.assertIn('already including the driver',row['prompt'])
   self.assertEqual('load-r2',q['key']['revision'])
   self.assertEqual(q['options'][row['correct']]['id'],q['feedback']['correct_option_id'])
   for i,(o,f) in enumerate(zip(row['options'],q['feedback']['option_feedback'])):
    self.assertIn(f'{total} − {ready} = {expected} kg',o['explanation'])
    self.assertIn('driver is already included',o['explanation'])
    self.assertEqual(o['explanation'],f['explanation'][0]['text'])
    if i!=row['correct']:self.assertTrue(o['explanation'].startswith(f'{values[i]} kg is not'))
 def test_outputs_reproduce(self):
  for path,value in outputs().items():self.assertEqual((ROOT/path).read_text(),value,str(path))
 def test_cannot_remove_later_batch_metadata(self):
  with self.assertRaises(AssertionError):outputs(1)
if __name__=='__main__':unittest.main()
