"""Reproduce all 9E outputs and verify immutable inputs, package validation and test evidence."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from apply_sign_rewrites_9e import build,read,dump,digest,ids,split_kotlin
from compile_curriculum import Validator

def verify():
    bank,kotlin,_,_,_=build(12)
    assert read(Path('content/questions.json'))==bank
    for path,value in split_kotlin(kotlin).items():assert (ROOT/path).read_text()==value
    batches=[]
    for n in range(2,13):
        _,_,q,a,d=build(n);base=HERE.parent/f'9E{n}'
        assert json.loads((base/'questions.json').read_text())==q
        assert json.loads((base/'batch-acceptance.json').read_text())==a
        assert (base/'before-after.diff').read_text()==d
        assert a['question_ids']==ids(n)
        batches.append({'step':f'9E{n}','rewritten':len(q['questions']),'distractor_change_records':sum(r['distractors_changed'] for r in a['questions'])})
    original=read(Path('docs/curriculum/app-migration/implementation-evidence/9E1/incoming-questions.json'))
    assigned=[qid for n in range(1,13) for qid in ids(n)]
    assert [a['id'] for a,b in zip(original,bank) if a!=b]==assigned
    assert sum(a==b for a,b in zip(original,bank))==422
    baseline='0b9ef0a'
    for source,archive in [('content/questions.json','incoming-questions.json'),('composeApp/src/commonMain/kotlin/se/korkort/Bank.kt','incoming-bank.kt.txt')]:
        assert subprocess.check_output(['git','show',baseline+':'+source],cwd=ROOT)==(HERE.parent/'9E2'/archive).read_bytes()
    for path in ['content/curriculum.json','content/signs.json','content/sources.json','docs/curriculum/app-migration/question-actions.json','docs/curriculum/app-migration/implementation-backlog.json']:
        assert hashlib.sha256(subprocess.check_output(['git','show',baseline+':'+path],cwd=ROOT)).hexdigest()==digest(Path(path)),path
    # Prior completed batch and all its evidence remain byte-exact.
    for item in subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'docs/curriculum/app-migration/implementation-evidence/9E1'],cwd=ROOT,text=True).splitlines():
        assert subprocess.check_output(['git','show',baseline+':'+item],cwd=ROOT)==(ROOT/item).read_bytes(),item
    payloads={'curriculum':read(Path('content/curriculum.json')),'questions':json.loads((HERE/'questions.json').read_text()),'sources':read(Path('content/sources.json')),'legacy_aliases':json.loads((HERE.parent/'9B17/legacy_aliases.json').read_text())}
    assert payloads['questions']['questions']==[r['assessment'] for r in bank if r.get('assessment')]
    totals=Validator().package(payloads,json.loads((HERE/'validation-manifest.json').read_text()),'fixture')
    assert totals['questions']==578
    questions=payloads['questions']['questions']
    assert sum(bool(q['image'])+sum(bool(o['image']) for o in q['options']) for q in questions)==1445
    assert sum(r['distractors_changed'] for n in range(1,13) for r in read(Path(f'docs/curriculum/app-migration/implementation-evidence/9E{n}/batch-acceptance.json'))['questions'])==128
    assert all(q['acceptance']['eligibility']=='held' and not q['acceptance']['delivery_proof'] for q in payloads['questions']['questions'])
    suites=[]
    for p in sorted(HERE.glob('TEST-*.xml')):
        a=ET.parse(p).getroot().attrib
        assert int(a['failures'])==int(a['errors'])==int(a.get('skipped',0))==0
        suites.append({'name':a['name'],'tests':int(a['tests'])})
    assert sum(s['tests'] for s in suites)==23
    assert re.search(r'Ran 113 tests in [\d.]+s\s+OK',(HERE/'python-tests.txt').read_text())
    assert 'BUILD SUCCESSFUL' in (HERE/'gradle-tests.txt').read_text()
    paths={p.relative_to(ROOT) for n in range(2,13) for p in (HERE.parent/f'9E{n}').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    paths.update(p.relative_to(ROOT) for p in HERE.rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts)
    paths.update(split_kotlin(kotlin))
    paths.update(Path(p) for p in ['content/questions.json','composeApp/src/commonMain/kotlin/se/korkort/Bank.kt','composeApp/src/commonTest/kotlin/se/korkort/SignRewriteBatchTest.kt','tools/apply_sign_rewrite_9e2.py','tools/apply_sign_rewrites_9e.py','tools/test_apply_sign_rewrite_9e1.py','tools/test_apply_sign_rewrite_9e2.py','tools/test_apply_sign_rewrites_9e.py','docs/curriculum/implementation-plan.md','docs/curriculum/progress.md'])
    return {'status':'passed','checked_on':'2026-10-16','baseline_revision':baseline,'counts':{'new_rewrites':528,'all_9E_rewrites':578,'untouched_questions':422,'image_occurrences':1445,'distractor_change_records':128,'delivery_held':578,'scored_activation':0,'python_tests':113,'kotlin_desktop_tests':23},'batches':batches,'package':totals,'test_suites':suites,'limitations':['All rewritten questions remain held until exact-asset delivery and assessment route integration acceptance.','38 replacement questions remain separate 9F work.'],'files':[{'path':str(p),'sha256':digest(p)} for p in sorted(paths)]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();data=dump(verify())
    if args.check:assert (HERE/'verification.json').read_text()==data,'Stale 9E verification'
    else:(HERE/'verification.json').write_text(data)
    print('9E verified: 578 rewrites held; 422 untouched; 113 Python / 23 desktop tests passed.')
if __name__=='__main__':main()
