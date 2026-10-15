"""M01 regression checks for complete teaching, source authority and approved image regions."""
import copy
import hashlib
import unittest
from compile_curriculum import Validator, ContentError, manifest_digest
from import_curriculum_m01 import build, opening, read, EVIDENCE, ROOT, IDS

class M01ImportTest(unittest.TestCase):
    def setUp(self):
        self.payloads={'curriculum':read('content/curriculum.json'),**{k:read(str((EVIDENCE/(k+'.json')).relative_to(ROOT))) for k in ['questions','sources','legacy_aliases']}}
        self.manifest=read(str((EVIDENCE/'staging-manifest.json').relative_to(ROOT)))
    def validate(self):return Validator().package(self.payloads,self.manifest)
    def rejects(self,pattern):
        with self.assertRaisesRegex(ContentError,pattern):self.validate()
    def doc(self,id):return next(d for d in self.payloads['curriculum']['documents'] if d['id']==id)
    def crop(self):return next(b['payload'] for b in self.doc('M01-L02')['body_blocks'] if b['payload']['type']=='cropped_image')
    def ref(self):
        return next(r for r in self.payloads['sources']['references'] if r['url'].endswith('/handledare/'))
    def test_complete_staging_package(self):
        self.assertEqual({'destinations':80,'questions':0,'assets':4,'profile':'fixture'},self.validate())
    def test_import_is_idempotent_and_preserves_unrelated_documents(self):
        p=copy.deepcopy(self.payloads['curriculum']);state=read('content/curriculum-import-state.json')
        result,newstate,_=build(p,state)
        self.assertEqual(p,result);self.assertEqual(state,newstate)
        baseline,_=opening()
        self.assertEqual([d for d in baseline['documents'] if d['id'] not in IDS],[d for d in result['documents'] if d['id'] not in IDS])
    def test_historical_parliamentary_explanation_is_not_labelled_current_law(self):
        ref=next(r for r in self.payloads['sources']['references'] if 'gm0343' in r['url'])
        self.assertEqual(['swedish_parliamentary_material'],ref['classifications'])
        self.assertIn('not current legal rules',ref['classification_note'])
    def test_hypothetical_microsleep_arithmetic_is_editorial_inference(self):
        block=next(b for b in self.doc('M01-L02')['body_blocks'] if b['metadata']['id']=='M01-L02/microsleep')
        self.assertTrue(block['metadata']['source_uses'][0]['editorial_inference'])
    def test_refuses_to_overwrite_edited_module(self):
        p=self.payloads['curriculum'];self.doc('M01-L02')['body_blocks'].pop()
        with self.assertRaisesRegex(ValueError,'Refusing to overwrite'):build(p,read('content/curriculum-import-state.json'))
    def test_answers_are_separate_and_referenced_once(self):
        for id in IDS[1:]:
            d=self.doc(id);answer=d['answer_blocks'][0]
            checks=[b['payload'] for b in d['body_blocks'] if b['payload']['type']=='knowledge_check']
            self.assertEqual([answer['metadata']['id']],[b['answer_id'] for b in checks])
            self.assertEqual('after_deliberate_reveal',answer['visibility'])
    def test_curriculum_only_source_id_cannot_be_invented(self):
        ref=self.ref();old=ref['id'];ref['id']='REF-invented'
        for s in self.payloads['sources']['destinations']:
            for b in s['scoped_urls']:
                if b['reference_id']==old:b['reference_id']=ref['id']
        self.rejects('unknown or changed approved source URL')
    def test_curriculum_only_source_requires_matching_frozen_evidence(self):
        self.ref()['evidence'][0]['origin']=self.payloads['sources']['references'][0]['evidence'][0]['origin']
        self.rejects('unknown or changed approved source URL')
    def test_curriculum_only_source_rejects_arbitrary_url_even_with_matching_hash_id(self):
        ref=self.ref();ref['url']='https://example.com/unapproved';ref['id']='REF-'+hashlib.sha256(ref['url'].encode()).hexdigest()[:16]
        self.rejects('unknown source reference|URL differs')
    def test_crop_must_be_inside_source(self):
        self.crop()['region']['right']=999999;self.rejects('pixel bounds')
    def test_crop_must_have_positive_area(self):
        crop=self.crop();crop['region']['bottom']=crop['region']['top'];self.rejects('pixel bounds')
    def test_crop_cannot_have_negative_origin(self):
        self.crop()['region']['left']=-1;self.rejects('pixel bounds')
    def test_official_sign_cannot_be_clipped(self):
        asset=self.payloads['curriculum']['assets'][0];asset['kind']='official_sign';asset['rendering']['contain_without_crop']=True
        self.rejects('limited to contextual illustrations')
    def test_missing_crop_asset_fails(self):
        self.crop()['asset_id']='missing';self.rejects('unknown asset')
    def test_truncated_answer_does_not_reproduce_approved_import(self):
        self.doc('M01-L02')['answer_blocks'][0]['blocks'][0]['payload']['text']=[{'type':'text','text':'No.'}]
        with self.assertRaisesRegex(ValueError,'Refusing to overwrite'):build(self.payloads['curriculum'],read('content/curriculum-import-state.json'))

if __name__=='__main__':unittest.main(verbosity=2)
