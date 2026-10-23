"""Non-mutating current reader and frozen-baseline checks after bounded step10 edits."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import build_reader
from compile_curriculum import ROOT
import stage_step10_corrections as staged
import finalize_step10_corrections as release


def verify_reader():
    files=build_reader.generate()
    historical=Path('docs/curriculum/app-migration/implementation-evidence/9L/reader-parity.tsv')
    files[release.RELEASE/'reader-parity.tsv']=files.pop(historical)
    for path,text in files.items(): assert (ROOT/path).read_text()==text,path
    print('PASS: every current reader Kotlin file and full teaching/asset parity; historical9L receipt untouched.')


def verify_baseline():
    author=release.read(staged.AUTHOR);base_path=Path(author['base_release']['path'])
    assert release.identity(base_path)==author['base_release']
    baseline=json.loads(gzip.decompress((ROOT/base_path).read_bytes()))['files']
    before=baseline['content/accepted-assessment-questions.json']['questions']
    after=release.read(Path('content/accepted-assessment-questions.json'))['questions']
    assert len(before)==len(after)==1000
    changed=set(author['descriptions']['X9']['image_question_ids'])
    assert len(changed)==7 and [q['key']['question_id'] for q in before]==[q['key']['question_id'] for q in after]
    for original,current in zip(before,after):
        id=original['key']['question_id']
        if id not in changed: assert current==original,id;continue
        assert current['key']['revision']==original['key']['revision']+'-step10-description-r1'
        for field in set(original)-{'key','image','options','acceptance'}: assert current[field]==original[field],(id,field)
        assert [o['id'] for o in current['options']]==[o['id'] for o in original['options']]
        for old,new in zip(original['options'],current['options']):
            for field in set(old)-{'image'}:assert old[field]==new[field],(id,field)
        assert current['acceptance']['eligibility']=='accepted' and not current['acceptance']['open_holds']
        assert current['acceptance']['content_review']==original['acceptance']['content_review']
    assert len({q['concept_id'] for q in after})==500
    old_assets=baseline['content/curriculum.json']['assets'];new_assets=release.read(Path('content/curriculum.json'))['assets']
    assert len(old_assets)==len(new_assets)==484
    for old,new in zip(old_assets,new_assets):
        assert old['id']==new['id'] and old['original']==new['original'] and old['bundled']==new['bundled']
        for file in (new['original'],new['bundled']):assert release.identity(Path(file['path']))==file
    assert release.read(Path('content/legacy-aliases.json'))==baseline['content/legacy-aliases.json']
    protected=release.read(Path('docs/curriculum/app-migration/verification-evidence/10L2/DEF-10H-001/candidate-fingerprint.json'))['source_files']
    for path in ['content/assessment-questions.json','content/content-manifest.json','content/questions.json','content/question-relationships.json','content/delivery-targets.json']:
        assert release.identity(Path(path))['sha256']==protected[path],path
    for path,digest in protected.items():
        if Path(path).name.startswith('QuestionPackage9J') and path.endswith('.kt'):
            assert release.identity(Path(path))['sha256']==digest,path
    assert release.read(Path('content/delivery-targets.json'))['ios_scope']=='simulator'
    print('PASS:993 questions byte-object unchanged;7 bounded revisions;500concepts;484 unchanged artwork bindings; frozen candidate/aliases/policy retained.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('scope',choices=['reader','baseline']);a=p.parse_args()
    (verify_reader if a.scope=='reader' else verify_baseline)()


if __name__=='__main__':main()
