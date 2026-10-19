"""Reject stale per-revision decisions and unsupported delivery-scope claims."""
import copy,unittest
from pathlib import Path
from unittest.mock import patch
import finalize_question_package_9j as final
from compile_curriculum import ROOT,Validator,ContentError,manifest_digest

class AcceptedPackageTest(unittest.TestCase):
 def test_accepted_release_reproduces_and_covers_every_original_id(self):
  final.build(check=True)
  questions=final.read(Path('content/accepted-assessment-questions.json'))['questions']
  self.assertEqual(1000,len(questions));self.assertEqual(500,len({q['concept_id'] for q in questions}))
  self.assertTrue(all(q['acceptance']['eligibility']=='accepted' and not q['acceptance']['open_holds'] for q in questions))
 def test_stale_revision_and_unreviewed_semantics_cannot_be_promoted(self):
  original=final.read
  decisions=copy.deepcopy(original(final.BASE/'delivery-acceptance.json'))
  decisions['questions'][0]['revision']='unreviewed-revision'
  with patch.object(final,'read',side_effect=lambda p: decisions if p==final.BASE/'delivery-acceptance.json' else original(p)):
   with self.assertRaises(AssertionError):final.build(check=True)
  questions=copy.deepcopy(original(Path('content/assessment-questions.json')))
  next(q for q in questions['questions'] if q['acceptance']['eligibility']=='held')['prompt'][0]['text']+=' Changed without review.'
  with patch.object(final,'read',side_effect=lambda p: questions if p==Path('content/assessment-questions.json') else original(p)):
   with self.assertRaises(AssertionError):final.build(check=True)
 def test_simulator_evidence_is_not_misrepresented_as_physical_ios(self):
  manifest=copy.deepcopy(final.read(Path('content/accepted-content-manifest.json')))
  manifest['inputs']=[r for r in manifest['inputs'] if r['path']!='content/delivery-targets.json']
  manifest['identity']['manifest_sha256']=manifest_digest(manifest)
  payloads={r['kind']:final.read(Path(r['file']['path'])) for r in manifest['payloads'] if r['kind']!='asset'}
  with self.assertRaisesRegex(ContentError,'every configured target'):
   Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json').package(payloads,manifest,'release')

if __name__=='__main__':unittest.main()
