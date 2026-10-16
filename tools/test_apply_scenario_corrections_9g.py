"""Scope, typed contract and proposal regression checks for all eight 9G stages."""
import copy
import unittest
from pathlib import Path
from apply_scenario_corrections_9g import ROOT, BASE, ACTIONS, BANK, IDS, read, outputs
from apply_sign_rewrites_9e import build
from compile_curriculum import Validator
class ScenarioCorrectionsTest(unittest.TestCase):
 def test_only_eight_records_change_from_9e(self):
  before=build(12)[0];after=read(Path('content/questions.json'))
  from apply_load_clarifications_9h import IDS as LOAD_IDS
  from apply_fuel_corrections_9i import IDS as FUEL_IDS
  original={q['id']:q for q in before}
  after=[original[q['id']] if q['id'] in LOAD_IDS+FUEL_IDS else q for q in after]
  self.assertEqual(IDS,[a['id'] for a,b in zip(before,after) if a!=b])
  self.assertEqual([q['id'] for q in before],[q['id'] for q in after])
 def test_exact_proposals_typed_contract_and_feedback(self):
  actions={q['question_id']:q for q in read(ACTIONS)['questions']};validator=Validator()
  for row in read(Path('content/questions.json')):
   if row['id'] not in IDS:continue
   q=row['assessment'];validator.typed(q,'AssessmentQuestion',row['id'])
   legacy=copy.deepcopy(row);legacy.pop('assessment')
   self.assertEqual(actions[row['id']]['proposed_changes']['draft_question'],legacy)
   self.assertEqual('scenario-r2',q['key']['revision'])
   self.assertEqual(q['options'][row['correct']]['id'],q['feedback']['correct_option_id'])
   for o,f,old in zip(q['options'],q['feedback']['option_feedback'],row['options']):
    self.assertEqual(o['id'],f['option_id']);self.assertEqual(old['explanation'],f['explanation'][0]['text'])
 def test_generated_outputs_and_order_reproduce(self):
  for path,value in outputs().items():self.assertEqual((ROOT/path).read_text(),value,str(path))
  self.assertEqual(IDS,read(BASE/'question-acceptance.json')['execution_order'])
if __name__=='__main__':unittest.main()
