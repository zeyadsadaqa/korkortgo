"""Executable validation/compiler regression checks for the exact 9A3 fixture."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from compile_curriculum import (ROOT, MARKER, ContentError, Emitter, Validator, canonical,
                                compile_files, kotlin_string, manifest_digest, read_json, pointer)

EVIDENCE=ROOT/'docs/curriculum/app-migration/implementation-evidence/9A3'
FIXTURE=EVIDENCE/'fixture'
PATHS={k:FIXTURE/(k+'.json') for k in ['curriculum','questions','sources','legacy_aliases']}

class CompilerTest(unittest.TestCase):
    def setUp(self):
        self.p={k:read_json(p) for k,p in PATHS.items()}
        self.m=read_json(FIXTURE/'manifest.json')
        # Keep retained 9A3 evidence immutable while testing evolving tool/model bytes.
        for record in self.m['inputs']:
            if record['path'] in {*__import__('content_schema').MODEL_PATHS, 'tools/compile_curriculum.py', 'tools/content_schema.py', 'tools/build_content.py'}:
                record['sha256']=hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()
        self.m['identity']['manifest_sha256']=manifest_digest(self.m)
        (ROOT/'tmp').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'tmp')
        self.addCleanup(self.temp.cleanup)
        self.manifest_path=Path(self.temp.name)/'manifest.json'
        # Historical fixtures bind the pre-rewrite question bytes, not the evolving live bank.
        archive=ROOT/'docs/curriculum/app-migration/implementation-evidence/9E1/incoming-questions.json'
        self.paths=dict(PATHS)
        if archive.exists():
            def relocate(value):
                if isinstance(value,dict):
                    if value.get('path')=='content/questions.json' and value.get('sha256')==hashlib.sha256(archive.read_bytes()).hexdigest():
                        value['path']=str(archive.relative_to(ROOT))
                    for child in value.values():relocate(child)
                elif isinstance(value,list):
                    for child in value:relocate(child)
            relocate(self.p)
            staged=Path(self.temp.name)/'questions.json'
            staged.write_text(json.dumps(self.p['questions']))
            self.paths['questions']=staged
            record=next(r for r in self.m['payloads'] if r['kind']=='questions')
            record['file']={'path':str(staged.relative_to(ROOT)),'sha256':hashlib.sha256(staged.read_bytes()).hexdigest()}
            self.m['identity']['manifest_sha256']=manifest_digest(self.m)
        self.manifest_path.write_text(json.dumps(self.m))

    def validate(self,profile='fixture'):
        self.m['identity']['manifest_sha256']=manifest_digest(self.m)
        return Validator().package(self.p,self.m,profile)

    def rejects(self,fragment):
        with self.assertRaisesRegex(ContentError,fragment):self.validate()

    def test_exact_fixture_is_unscored_and_valid(self):
        self.assertEqual({'destinations':10,'questions':1,'assets':1,'profile':'fixture'},self.validate())
        self.assertEqual('unreviewed',self.p['questions']['questions'][0]['acceptance']['eligibility'])

    def test_manifest_hash_has_a_fixed_independent_golden_vector(self):
        # SHA256 is calculated over this literal byte string, independently of compiler canonicalization.
        expected=hashlib.sha256(b'{"identity":{"content_version":"a"},"schema_version":1}').hexdigest()
        self.assertEqual(expected,manifest_digest({'schema_version':1,'identity':{'manifest_sha256':'f'*64,'content_version':'a'}}))
        self.assertNotEqual(expected,manifest_digest({'schema_version':1,'identity':{'manifest_sha256':'f'*64,'content_version':'b'}}))

    def test_duplicate_canonical_id(self):
        self.p['curriculum']['documents'].append(copy.deepcopy(self.p['curriculum']['documents'][0]));self.rejects('duplicate id')

    def test_unknown_canonical_id(self):
        self.p['curriculum']['documents'][0]['id']='invented';self.rejects('unknown canonical')

    def test_wrong_destination_kind(self):
        self.p['curriculum']['documents'][1]['kind']='module_review';self.rejects('wrong destination kind')

    def test_duplicate_question_id(self):
        self.p['questions']['questions']*=2;self.rejects('duplicate question_id')

    def test_duplicate_option_id(self):
        q=self.p['questions']['questions'][0];q['options'][1]['id']=q['options'][0]['id'];self.rejects('duplicate id')

    def test_missing_option_feedback(self):
        self.p['questions']['questions'][0]['feedback']['option_feedback'].pop();self.rejects('feedback identities')

    def test_key_must_be_authored_option_identity(self):
        self.p['questions']['questions'][0]['feedback']['correct_option_id']='A';self.rejects('authored option identities')

    def test_relabelled_option_identity_is_rejected_even_if_key_and_feedback_agree(self):
        q=self.p['questions']['questions'][0]
        old=q['options'][0]['id']
        q['options'][0]['id']='display-A'
        for item in q['feedback']['option_feedback']:
            if item['option_id']==old:item['option_id']='display-A'
        if q['feedback']['correct_option_id']==old:q['feedback']['correct_option_id']='display-A'
        self.rejects('authored assignment')

    def test_duplicate_visual_choices_even_with_distinct_option_ids(self):
        q=self.p['questions']['questions'][0]
        img={'asset_id':self.p['curriculum']['assets'][0]['id'],'neutral_description':None}
        q['options'][0]['image']=img;q['options'][1]['image']=copy.deepcopy(img);self.rejects('repeated visual')

    def test_unknown_asset(self):
        self.p['curriculum']['documents'][1]['body_blocks'][1]['payload']['asset_id']='wrong';self.rejects('unknown asset')

    def test_unknown_source(self):
        self.p['curriculum']['documents'][2]['source_ids']=['source-invented'];self.rejects('unknown source destination')

    def test_wrong_scoped_source_use(self):
        self.p['curriculum']['documents'][2]['body_blocks'][1]['metadata']['source_uses'][0]['scope_id']='M03-L01';self.rejects('exact scoped URL')

    def test_invalid_date(self):
        self.p['sources']['references'][0]['evidence'][0]['dates']['checked_on']='2026-02-30';self.rejects('valid ISO date')

    def test_missing_required_fields(self):
        del self.p['curriculum']['documents'][0]['origin'];self.rejects('fields differ')

    def test_unknown_fields(self):
        self.p['curriculum']['documents'][0]['old_book_page']=46;self.rejects('unknown=.*old_book_page')

    def test_unsupported_schema(self):
        self.p['curriculum']['schema_version']=2;self.rejects('unsupported schema')

    def test_origin_hash_drift(self):
        self.p['curriculum']['documents'][0]['origin']['file']['sha256']='f'*64;self.rejects('hash mismatch')

    def test_refreezing_current_hash_does_not_clear_approved_source_drift(self):
        v=Validator()
        path=self.p['curriculum']['documents'][0]['origin']['file']['path']
        v.approved[path]='f'*64
        with self.assertRaisesRegex(ContentError,'approved source changed'):
            v.package(self.p,self.m)

    def test_origin_locator_resolves(self):
        self.p['curriculum']['documents'][0]['origin']['locator']='line:999999';self.rejects('invalid source line')

    def test_path_traversal(self):
        self.p['curriculum']['assets'][0]['original']['path']='../private.png';self.rejects('without traversal')

    def test_table_shape(self):
        self.p['curriculum']['documents'][1]['body_blocks'][2]['payload']['rows'][0]['cells'].pop();self.rejects('row/column mismatch')

    def test_missing_answer(self):
        self.p['curriculum']['documents'][2]['answer_blocks']=[];self.rejects('unknown separate answer')

    def test_duplicate_block_id(self):
        d=self.p['curriculum']['documents'][2];d['body_blocks'].append(copy.deepcopy(d['body_blocks'][0]));self.rejects('duplicate or unscoped block')

    def test_open_holds_cannot_be_scored(self):
        a=self.p['questions']['questions'][0]['acceptance'];a['eligibility']='accepted';a['open_holds']=[{'id':'h','reason':'pending','release_condition':'proof'}];self.rejects('incomplete content review or holds')

    def test_manifest_revision_parity(self):
        self.m['question_revisions'][0]['key']['revision']='different';self.rejects('revision/eligibility mismatch')

    def test_wrong_legacy_namespace(self):
        self.p['legacy_aliases']['aliases'][0]['lookup']={'type':'page','namespace':'wrong','page':46};self.rejects('unknown legacy namespace')

    def test_valid_but_wrong_question_destination_is_rejected(self):
        self.p['questions']['questions'][0]['relationship']['primary_lesson_id']='M03-L01';self.rejects('differs from 7C')

    def test_valid_but_wrong_alias_destination_is_rejected(self):
        self.p['legacy_aliases']['aliases'][0]['outcome']['target']['content_id']='M03-L01';self.rejects('target choices differ')

    def test_unregistered_source_url_is_rejected(self):
        self.p['sources']['references'][-1]['url']='https://example.com/unverified';self.rejects('approved source URL|URL differs from approved')

    def test_set_order_and_duplicates_are_not_silently_normalized(self):
        self.p['sources']['references'][0]['classifications']=['research','research'];self.rejects('duplicate-free')

    def test_basic_date_format_is_not_extended_iso_date(self):
        self.p['sources']['references'][0]['evidence'][0]['dates']['checked_on']='20261015';self.rejects('valid ISO date')

    def test_fixture_cannot_be_a_release(self):
        with self.assertRaisesRegex(ContentError,'release assets|incomplete canonical'):
            self.validate('release')

    def test_manifest_asset_files_are_not_duplicated(self):
        self.m['payloads'].append(copy.deepcopy(self.m['payloads'][-1]));self.rejects('duplicate asset file record')

    def test_retained_question_text_is_not_rewritten(self):
        self.p['questions']['questions'][0]['prompt']=[{'type':'text','text':'Altered wording'}];self.rejects('retained assessment')

    def test_json_duplicate_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'input.json';p.write_text('{"id":1,"id":2}')
            with self.assertRaisesRegex(ContentError,'duplicate JSON key'):read_json(p)

    def test_malformed_manifest_has_a_useful_contract_error(self):
        with self.assertRaisesRegex(ContentError,'expected ContentManifest object'):
            Validator().package(self.p,[])

    def test_non_enum_set_members_have_a_useful_contract_error(self):
        self.p['sources']['references'][0]['classifications']=[1,'research'];self.rejects('unknown SourceClassification')

    def test_manifest_tampering(self):
        self.m['identity']['manifest_sha256']='f'*64
        with self.assertRaisesRegex(ContentError,'manifest digest mismatch'):Validator().package(self.p,self.m)

    def test_importing_legacy_entrypoint_has_no_side_effects(self):
        protected=['content/questions.json','content/signs.json','composeApp/src/commonMain/kotlin/se/korkort/Bank.kt']
        before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in protected}
        spec=importlib.util.spec_from_file_location('legacy_entrypoint',ROOT/'tools/build_content.py')
        spec.loader.exec_module(importlib.util.module_from_spec(spec))
        self.assertEqual(before,{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in protected})
        result=subprocess.run([sys.executable,str(ROOT/'tools/build_content.py')],capture_output=True)
        self.assertEqual(2,result.returncode)

    def test_determinism_trace_and_staging_ownership(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'kotlin';trace=Path(tmp)/'trace.json'
            compile_files(self.paths,self.manifest_path,out,trace,symbol='fixture9A3')
            first={p.name:p.read_bytes() for p in out.glob('*.kt')};trace_bytes=trace.read_bytes()
            compile_files(self.paths,self.manifest_path,out,trace,symbol='fixture9A3')
            self.assertEqual(first,{p.name:p.read_bytes() for p in out.glob('*.kt')})
            self.assertEqual(trace_bytes,trace.read_bytes())
            for record in json.loads(trace_bytes)['records']:
                path,ptr=record['input'].split('#',1)
                pointer(read_json(ROOT/path),ptr,'trace')
                line=(out/record['output_file']).read_text().splitlines()[record['output_line']-1]
                self.assertIn('fun '+record['symbol']+'(',line)
            (out/'GeneratedCurriculumPart9999.kt').write_text('human-authored')
            with self.assertRaisesRegex(ContentError,'non-generated'):compile_files(self.paths,self.manifest_path,out,trace)
            self.assertEqual(first['GeneratedCurriculum.kt'],(out/'GeneratedCurriculum.kt').read_bytes())

    def test_outputs_cannot_overwrite_live_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ContentError,'staging/build directory'):
                compile_files(self.paths,self.manifest_path,ROOT/'composeApp/src/commonMain',Path(tmp)/'trace.json')

    def test_payload_hash_must_match_manifest(self):
        with tempfile.TemporaryDirectory(dir=EVIDENCE) as tmp:
            p=Path(tmp)/'questions.json';p.write_text(json.dumps(self.p['questions']))
            with self.assertRaisesRegex(ContentError,'matching questions payload'):
                compile_files({**self.paths,'questions':p},self.manifest_path,Path(tmp)/'out',Path(tmp)/'trace.json')

    def test_kotlin_strings_escape_interpolation_and_controls(self):
        self.assertEqual('"\\${notCode}\\n\\\"\\\\\\u000c"',kotlin_string('${notCode}\n"\\\f'))
        self.assertIn('joinToString',kotlin_string('å'*5000))

if __name__=='__main__':unittest.main(verbosity=2)
