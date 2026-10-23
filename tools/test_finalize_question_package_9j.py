"""Reject stale per-revision decisions and unsupported delivery-scope claims."""
import copy,unittest
from pathlib import Path
from unittest.mock import patch
import finalize_step10_corrections as final
import stage_step10_corrections as staged
from compile_curriculum import ROOT,Validator,ContentError,manifest_digest

class AcceptedPackageTest(unittest.TestCase):
 def test_accepted_release_reproduces_and_covers_every_original_id(self):
  for path,text in final.outputs().items():self.assertEqual(text,(ROOT/path).read_text(),path)
  questions=final.read(Path('content/accepted-assessment-questions.json'))['questions']
  self.assertEqual(1000,len(questions));self.assertEqual(500,len({q['concept_id'] for q in questions}))
  self.assertTrue(all(q['acceptance']['eligibility']=='accepted' and not q['acceptance']['open_holds'] for q in questions))
 def test_stale_revision_and_unreviewed_semantics_cannot_be_promoted(self):
  _,_,data,changed=staged.build()
  questions=[q for q in data['content/accepted-assessment-questions.json']['questions'] if q['key']['question_id'] in changed]
  receipt=final.read(final.RECEIPT)
  self.assertEqual(7,len(final.require_delivery(receipt,questions)))
  stale=copy.deepcopy(receipt);stale['questions'][0]['revision']='unreviewed-revision'
  with self.assertRaises(AssertionError):final.require_delivery(stale,questions)
  altered=copy.deepcopy(questions);altered[0]['prompt'][0]['text']+=' Changed without review.'
  with self.assertRaises(AssertionError):final.require_delivery(receipt,altered)
 def test_simulator_evidence_is_not_misrepresented_as_physical_ios(self):
  manifest=copy.deepcopy(final.read(Path('content/accepted-content-manifest.json')))
  manifest['inputs']=[r for r in manifest['inputs'] if r['path']!='content/delivery-targets.json']
  manifest['identity']['manifest_sha256']=manifest_digest(manifest)
  payloads={r['kind']:final.read(Path(r['file']['path'])) for r in manifest['payloads'] if r['kind']!='asset'}
  with self.assertRaisesRegex(ContentError,'every configured target'):
   Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json').package(payloads,manifest,'release')

if __name__=='__main__':unittest.main()
