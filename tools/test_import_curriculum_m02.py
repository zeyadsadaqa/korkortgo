"""Cumulative M02 import and production-mask regressions."""
import copy
import hashlib
import unittest
from compile_curriculum import Validator,ContentError,manifest_digest
from import_curriculum_m02 import build, read, EVIDENCE, ROOT, IDS

class M02ImportTest(unittest.TestCase):
    def setUp(self):
        snapshot=ROOT/'docs/curriculum/app-migration/implementation-evidence/9B17'
        curriculum=snapshot/'incoming-curriculum.json';state=snapshot/'incoming-import-state.json'
        if not curriculum.exists():curriculum=ROOT/'content/curriculum.json';state=ROOT/'content/curriculum-import-state.json'
        self.p={'curriculum':read(str(curriculum.relative_to(ROOT))),**{k:read(str((EVIDENCE/(k+'.json')).relative_to(ROOT))) for k in ['questions','sources','legacy_aliases']}}
        self.m=read(str((EVIDENCE/'staging-manifest.json').relative_to(ROOT)))
        record=next(r for r in self.m['payloads'] if r['kind']=='curriculum')
        self.assertEqual(record['file']['sha256'],hashlib.sha256(curriculum.read_bytes()).hexdigest())
        record['file']['path']=str(curriculum.relative_to(ROOT))
        for record in self.m['inputs']:
            if record['path']=='content/curriculum-import-state.json':record['path']=str(state.relative_to(ROOT))
            if record['path'] in {*__import__('content_schema').MODEL_PATHS,'tools/compile_curriculum.py'} or record['path']==str(state.relative_to(ROOT)):
                record['sha256']=hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()
        self.m['identity']['manifest_sha256']=manifest_digest(self.m)
        self.state=read(str(state.relative_to(ROOT)))
    def doc(self,id):return next(d for d in self.p['curriculum']['documents'] if d['id']==id)
    def mask(self):return next(b['payload'] for b in self.doc('M02-R')['body_blocks'] if b['payload']['type']=='polygon_image')
    def validate(self):return Validator().package(self.p,self.m)
    def rejects(self,pattern):
        with self.assertRaisesRegex(ContentError,pattern):self.validate()
    def test_cumulative_package_valid(self):
        self.assertEqual({'destinations':97,'questions':0,'assets':10,'profile':'fixture'},self.validate())
    def test_import_reproduces_without_mutating_input(self):
        before=copy.deepcopy(self.p['curriculum']);state=copy.deepcopy(self.state)
        p,s,refs=build(self.p['curriculum'],self.state)
        self.assertEqual(before,p);self.assertEqual(state,s);self.assertEqual(before,self.p['curriculum']);self.assertEqual(refs,self.p['sources'])
    def test_only_M02_documents_change(self):
        before=read(str((EVIDENCE/'incoming-curriculum.json').relative_to(ROOT)))
        self.assertEqual([d for d in before['documents'] if d['id'] not in IDS],[d for d in self.p['curriculum']['documents'] if d['id'] not in IDS])
        self.assertEqual(before['assets'],[a for a in self.p['curriculum']['assets'] if a['id'].startswith('M01')])
    def test_hidden_answers_are_separate(self):
        for id in IDS[1:]:
            doc=self.doc(id);checks=[b['payload'] for b in doc['body_blocks'] if b['payload']['type']=='knowledge_check']
            self.assertEqual([a['metadata']['id'] for a in doc['answer_blocks']],[c['answer_id'] for c in checks])
            self.assertEqual('after_deliberate_reveal',doc['answer_blocks'][0]['visibility'])
    def test_table_retains_all_rows_and_related_lesson(self):
        table=next(b['payload'] for b in self.doc('M02-L01')['body_blocks'] if b['payload']['type']=='table')
        self.assertEqual(3,len(table['columns']));self.assertEqual(4,len(table['rows']))
        self.assertEqual('M02-L02',table['rows'][-1]['cells'][-1][-2]['target']['target']['content_id'])
    def test_table_shape_is_validated(self):
        next(b['payload'] for b in self.doc('M02-L01')['body_blocks'] if b['payload']['type']=='table')['rows'][0]['cells'].pop()
        self.rejects('row/column mismatch')
    def test_polygon_has_enough_vertices(self):
        self.mask()['polygon']=self.mask()['polygon'][:2];self.rejects('distinct vertices')
    def test_polygon_vertices_cannot_repeat(self):
        self.mask()['polygon'].append(self.mask()['polygon'][0]);self.rejects('distinct vertices')
    def test_polygon_stays_inside_region(self):
        self.mask()['polygon'][0]['x']=0;self.rejects('region bounds')
    def test_polygon_has_nonzero_area(self):
        self.mask()['polygon']=[{'x':777,'y':156},{'x':778,'y':156},{'x':779,'y':156}];self.rejects('nonzero area')
    def test_official_sign_may_not_be_masked(self):
        asset=next(a for a in self.p['curriculum']['assets'] if a['id']==self.mask()['asset_id']);asset['kind']='official_sign';asset['rendering']['contain_without_crop']=True
        self.rejects('limited to contextual illustrations')
    def test_scoped_evidence_is_accumulated_without_overwriting_M01(self):
        prior=read('docs/curriculum/app-migration/implementation-evidence/9B2/sources.json')
        for old in prior['references']:
            actual=next(r for r in self.p['sources']['references'] if r['id']==old['id'])
            self.assertEqual(old['evidence'],actual['evidence'][:len(old['evidence'])])
        seats=next(r for r in self.p['sources']['references'] if '/saten-och-huvudstod/' in r['url'])
        self.assertEqual(['2026-10-04','2026-10-12'],[r['dates']['checked_on'] for r in seats['evidence']])
    def test_manufacturer_and_research_are_not_relabelled_official_advice(self):
        refs=self.p['sources']['references']
        self.assertEqual(['manufacturer'],next(r for r in refs if 'volvocars.com' in r['url'])['classifications'])
        self.assertEqual(['research'],next(r for r in refs if 'vti-rapport' in r['url'])['classifications'])
        fuse=next(r for r in refs if 'elinstallationer/' in r['url'])
        self.assertTrue(any('maritime' in limit for e in fuse['evidence'] for limit in e['limitations']))
    def test_edited_teaching_and_assets_are_not_overwritten(self):
        p=copy.deepcopy(self.p['curriculum']);next(d for d in p['documents'] if d['id']=='M02-L01')['body_blocks'].pop()
        with self.assertRaisesRegex(ValueError,'Refusing to overwrite'):build(p,self.state)
        p=copy.deepcopy(self.p['curriculum']);next(a for a in p['assets'] if a['id']=='M02-R/illustration')['study_alt_text']='Changed'
        with self.assertRaisesRegex(ValueError,'Refusing to overwrite'):build(p,self.state)
    def test_practice_example_uses_production_order(self):
        ids=[b['metadata']['id'] for b in self.doc('M02-L02')['body_blocks']]
        self.assertLess(ids.index('M02-L02/worked-decision'),ids.index('M02-L02/practice-example'))
        self.assertLess(ids.index('M02-L02/practice-example'),ids.index('M02-L02/knowledge-check'))

if __name__=='__main__':unittest.main(verbosity=2)
