"""A release receipt cannot substitute flags for exact revised-question delivery."""
import copy
import unittest
from unittest.mock import patch

import finalize_step10_corrections as release
import stage_step10_corrections as staged


class Step10ReleaseAcceptanceTest(unittest.TestCase):
    def setUp(self):
        _, _, data, changed = staged.build()
        self.questions = [q for q in data['content/accepted-assessment-questions.json']['questions'] if q['key']['question_id'] in changed]
        settings=['light/1','light/1.6','dark/1','dark/1.6']
        self.observed={name:[{'question_id':q['key']['question_id'],'revision':q['key']['revision'],'setting':s,'width':w} for q in self.questions for s in settings for w in ([390,1280] if name=='desktop' else [None])] for name in ('android','desktop','ios_simulator','browser')}
        self.receipt={'status':'passed_exact_changed_revision_delivery','ios_scope':'simulator','candidate_manifest':release.identity(staged.OUT/'candidate-manifest.json'),'inputs':[release.identity(staged.AUTHOR)],'questions':[{'question_id':q['key']['question_id'],'revision':q['key']['revision'],'assessment_sha256':release.sha(release.canonical({k:v for k,v in q.items() if k!='acceptance'})),'status':'passed','reviewed_description_and_artwork':True,'targets':{name:{'status':'passed','settings':settings} for name in self.observed},'assets':[{'asset_id':i,'asset_sha256':next(a for a in data['content/curriculum.json']['assets'] if a['id']==i)['bundled']['sha256'],'status':'passed','platforms':release.read(__import__('pathlib').Path('content/delivery-targets.json'))['required_platforms']} for i in sorted({x['asset_id'] for x in [q['image'],*[o['image'] for o in q['options']]] if x})]} for q in self.questions]}

    def verify(self, receipt=None, observed=None):
        with patch.object(release,'observed_delivery',return_value=(observed or self.observed,[staged.AUTHOR])):
            return release.require_delivery(receipt or self.receipt,self.questions)

    def test_complete_exact_revision_inputs_are_accepted(self):
        self.assertEqual(7,len(self.verify()))

    def test_flags_cannot_replace_missing_platform_setting_or_revision(self):
        for mutation in ('target','setting','revision'):
            observed=copy.deepcopy(self.observed)
            if mutation=='target': observed['android']=[]
            elif mutation=='setting': observed['browser'].pop()
            else: observed['desktop'][0]['revision']='stale-revision'
            with self.assertRaises(AssertionError): self.verify(observed=observed)

    def test_changed_payload_or_candidate_identity_cannot_reuse_acceptance(self):
        for mutation in ('payload','candidate','input','asset','asset_platform'):
            receipt=copy.deepcopy(self.receipt)
            if mutation=='payload': receipt['questions'][0]['assessment_sha256']='0'*64
            elif mutation=='candidate': receipt['candidate_manifest']['sha256']='0'*64
            elif mutation=='input': receipt['inputs'][0]['sha256']='0'*64
            elif mutation=='asset': receipt['questions'][0]['assets'][0]['asset_sha256']='0'*64
            else: receipt['questions'][0]['assets'][0]['platforms']=[]
            with self.assertRaises(AssertionError): self.verify(receipt=receipt)

    def test_duplicate_question_or_missing_raw_binding_is_rejected(self):
        for mutation in ('duplicate','raw'):
            receipt=copy.deepcopy(self.receipt)
            if mutation=='duplicate':receipt['questions'][0]=receipt['questions'][1]
            else:receipt['inputs']=[]
            with self.assertRaises(AssertionError):self.verify(receipt=receipt)


if __name__=='__main__':unittest.main()
