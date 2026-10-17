"""Complete-candidate structural checks, frozen content parity and release/compatibility rejection."""
import copy
import hashlib
import unittest
from pathlib import Path
from collections import Counter
from assemble_question_package_9j import ROOT, BASE, MAP, ACTIONS, prepare, assemble, read
from compile_curriculum import Validator, ContentError, manifest_digest
class QuestionPackageTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c,cls.s,cls.bank,cls.rels,cls.questions,cls.audit,cls.retained=prepare()
  cls.questions=read(Path('content/assessment-questions.json'))['questions']
  cls.manifest=read(Path('content/content-manifest.json'))
 def validate(self,payloads=None,manifest=None,profile='fixture'):
  return Validator(source_authority=str(BASE/'source-authority.json')).package(payloads or {'curriculum':self.c,'sources':self.s,'questions':{'schema_version':1,'questions':self.questions},'legacy_aliases':read(Path('content/legacy-aliases.json'))},manifest or self.manifest,profile)
 def test_every_id_and_exact_relationship_resolve(self):
  self.assertEqual(1000,len(self.questions));self.assertEqual(500,len({q['concept_id'] for q in self.questions}))
  for m,q in zip(read(MAP)['questions'],self.questions):
   for key in ['primary_lesson_id','related_lesson_ids','reference_ids','source_ids','content_version']:self.assertEqual(m[key],q['relationship'][key])
   self.assertEqual(m['source_reference_ids'],[u['reference_id'] for u in q['relationship']['source_uses']])
  self.assertEqual({'destinations':1123,'questions':1000,'assets':484,'profile':'fixture'},self.validate())
 def test_complete_eligibility_never_promotes_holds(self):
  self.assertEqual(Counter({'accepted':384,'held':616}),Counter(q['acceptance']['eligibility'] for q in self.questions))
  self.assertEqual(Counter({'retain':336,'rewrite':626,'replace':38}),Counter(q['relationship']['disposition'] for q in self.questions))
  self.assertEqual(192,len({q['concept_id'] for q in self.questions if q['acceptance']['eligibility']=='accepted'}))
  with self.assertRaisesRegex(ContentError,'unaccepted/retired'):self.validate(profile='release')
 def test_retained_fields_and_unapplied_replacements_are_unchanged(self):
  actions={a['question_id']:a for a in read(ACTIONS)['questions']}
  for row,q in zip(self.bank,self.questions):
   a=actions[row['id']]
   if a['disposition'] in ['retain','replace']:self.assertEqual(a['original'],row)
   if a['disposition']=='retain':
    self.assertEqual('legacy-r1',q['key']['revision'])
    self.assertEqual(row['prompt'],q['prompt'][0]['text']);self.assertEqual(row['explanation'],q['feedback']['explanation'][0]['text'])
    self.assertEqual(row['correct'],[o['id'] for o in q['options']].index(q['feedback']['correct_option_id']))
    for old,opt,fb in zip(row['options'],q['options'],q['feedback']['option_feedback']):
     self.assertEqual(old['text'],opt['text'][0]['text']);self.assertEqual(old['explanation'],fb['explanation'][0]['text'])
 def test_frozen_legacy_urls_cannot_be_teaching_evidence(self):
  p={'curriculum':self.c,'sources':self.s,'questions':{'schema_version':1,'questions':copy.deepcopy(self.questions)},'legacy_aliases':read(Path('content/legacy-aliases.json'))}
  legacy=read(Path('content/legacy-sources.json'))['references'][0]
  p['questions']['questions'][0]['feedback']['option_feedback'][0]['source_uses']=[{'reference_id':legacy['id'],'source_id':None,'scope_id':None,'locator':'not teaching evidence','editorial_inference':False}]
  with self.assertRaisesRegex(ContentError,'compatibility-only URL'):self.validate(p)
 def test_changed_compatibility_url_is_rejected(self):
  p={'curriculum':self.c,'sources':copy.deepcopy(self.s),'questions':{'schema_version':1,'questions':self.questions},'legacy_aliases':read(Path('content/legacy-aliases.json'))}
  p['sources']['references'][-1]['url']='https://example.invalid/changed'
  with self.assertRaisesRegex(ContentError,'unknown or changed approved source'):self.validate(p)
 def test_reproduction(self):assemble(check=True)
if __name__=='__main__':unittest.main()
