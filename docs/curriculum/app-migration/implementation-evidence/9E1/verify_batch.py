"""Verify exact batch scope, source bindings, generated output, eligibility and retained test evidence."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from apply_sign_rewrite_9e1 import build,dump,BASE,read,digest
from compile_curriculum import Validator

def verify():
    bank,kotlin,typed,acceptance,diff=build()
    for path,value in {Path('content/questions.json'):dump(bank),Path('composeApp/src/commonMain/kotlin/se/korkort/Bank.kt'):kotlin,BASE/'questions.json':dump(typed),BASE/'batch-acceptance.json':dump(acceptance),BASE/'before-after.diff':diff}.items():assert (ROOT/path).read_text()==value,path
    baseline='fd77202'
    for source,archive in [('content/questions.json','incoming-questions.json'),('composeApp/src/commonMain/kotlin/se/korkort/Bank.kt','incoming-bank.kt.txt')]:
        assert subprocess.check_output(['git','show',baseline+':'+source],cwd=ROOT)==(HERE/archive).read_bytes()
    previous=HERE.parent/'9B17'
    payloads={'curriculum':read(Path('content/curriculum.json')),'questions':typed,'sources':read(Path('content/sources.json')),'legacy_aliases':json.loads((previous/'legacy_aliases.json').read_text())}
    totals=Validator().package(payloads,read(BASE/'validation-manifest.json'),'fixture')
    for path in ['content/curriculum.json','content/signs.json','content/sources.json','docs/curriculum/app-migration/question-actions.json','docs/curriculum/app-migration/implementation-backlog.json']:
        assert hashlib.sha256(subprocess.check_output(['git','show',baseline+':'+path],cwd=ROOT)).hexdigest()==digest(Path(path)),path
    suites=[]
    for p in sorted(HERE.glob('TEST-*.xml')):
        a=ET.parse(p).getroot().attrib
        assert int(a['failures'])==int(a['errors'])==int(a.get('skipped',0))==0
        suites.append({'name':a['name'],'tests':int(a['tests'])})
    assert sum(s['tests'] for s in suites)==23
    assert re.search(r'Ran 98 tests in [\d.]+s\s+OK',(HERE/'python-tests.txt').read_text())
    assert 'BUILD SUCCESSFUL' in (HERE/'gradle-tests.txt').read_text()
    paths={p.relative_to(ROOT) for p in HERE.rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts}
    paths.update(Path(p) for p in ['content/questions.json','composeApp/src/commonMain/kotlin/se/korkort/Bank.kt','composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','composeApp/src/commonTest/kotlin/se/korkort/QuizTest.kt','composeApp/src/commonTest/kotlin/se/korkort/SignRewriteBatchTest.kt','tools/apply_sign_rewrite_9e1.py','tools/test_apply_sign_rewrite_9e1.py','tools/test_compile_curriculum.py','docs/curriculum/implementation-plan.md','docs/curriculum/progress.md'])
    return {'status':'passed','step':'9E1','checked_on':'2026-10-16','counts':{'rewritten':50,'other_questions_unchanged':950,'distractor_change_records':12,'image_bindings':125,'delivery_held':50,'scored_activation':0,'python_tests':98,'kotlin_desktop_tests':23},'package':totals,'test_suites':suites,'baseline_revision':baseline,'limitations':['No image-delivery/device or route-integration acceptance; all 50 questions remain held.','Historical 9D receipts retain their original pre-rewrite execution context.'],'files':[{'path':str(p),'sha256':digest(p)} for p in sorted(paths)]}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();data=dump(verify())
    if args.check:assert (HERE/'verification.json').read_text()==data,'Stale 9E1 receipt'
    else:(HERE/'verification.json').write_text(data)
    print('9E1 verified: 50 rewrites, 950 unchanged, 125 image bindings; 98 Python / 23 Kotlin tests; all rewritten questions held from scoring.')
if __name__=='__main__':main()
