"""Reproduce saved generator outputs and check 9A3 scope/evidence; writes only verification.json."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from compile_curriculum import ROOT_TYPES, compile_files


def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,passed,detail):checks.append({'name':name,'passed':bool(passed),'detail':detail})
golden=json.loads((HERE/'golden.json').read_text())
paths={k:HERE/'fixture'/(k+'.json') for k in ROOT_TYPES}
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)/'generated';trace=Path(tmp)/'trace.json'
    totals=compile_files(paths,HERE/'fixture/manifest.json',out,trace,symbol='fixture9A3')
    expected={p.name:sha(p) for p in out.glob('*.kt')}
    check('Fresh Kotlin output matches golden',expected==golden['outputs'],expected)
    check('Fresh trace matches golden',sha(trace)==golden['trace_sha256'],sha(trace))
    compile_files(paths,HERE/'fixture/manifest.json',out,trace,symbol='fixture9A3')
    check('Repeated generation byte-identical',expected=={p.name:sha(p) for p in out.glob('*.kt')} and sha(trace)==golden['trace_sha256'],totals)
check('Saved Kotlin files match fresh output',{p.name:sha(p) for p in (HERE/'generated').glob('*.kt')}==golden['outputs'],len(golden['outputs']))
check('Saved trace unchanged',sha(HERE/'trace.json')==golden['trace_sha256'],golden['trace_sha256'])
m=json.loads((HERE/'fixture/manifest.json').read_text())
check('Fixture identity and eligibility retained',m['identity']['manifest_sha256']==golden['manifest_sha256'] and m['question_revisions'][0]['eligibility']=='unreviewed',m['identity'])
review=json.loads((HERE/'incoming-review.json').read_text())
quiz=ROOT/'composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt'
check('Incoming Quiz.kt preserved',sha(quiz)==review['quiz_incoming_sha256'] and review['quiz_normalized_sha256']==review['quiz_predecessor_sha256'],review['reviewed_quiz_changes'])
module=ast.parse((ROOT/'tools/build_content.py').read_text())
legacy=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='build_legacy')
legacy_module=ast.Module(body=legacy.body,type_ignores=[])
check('Explicit legacy body unchanged',hashlib.sha256(ast.dump(legacy_module,include_attributes=False).encode()).hexdigest()==review['legacy_ast_sha256'],review['previous_tool_sha256'])
base=read('docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json')
allowed={'tools/build_content.py','composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','docs/curriculum/implementation-plan.md'}
unexpected=[r['path'] for r in base['input_manifest'] if r['path'] not in allowed and (not (ROOT/r['path']).is_file() or sha(ROOT/r['path'])!=r['sha256'])]
check('All other 9A1 inputs preserved',not unexpected,unexpected)
prev=read('docs/curriculum/app-migration/implementation-evidence/9A2/verification.json')
models=[r for r in prev['artifacts'] if r['path'].endswith('Curriculum.kt') or r['path'].endswith('CurriculumContractTest.kt')]
check('9A2 model and test files unchanged',all(sha(ROOT/r['path'])==r['sha256'] for r in models),models)
log=(HERE/'python-tests.log').read_text()
check('44 compiler tests passed',bool(re.search(r'Ran 44 tests in .*\n\nOK\s*$',log)),{'path':str((HERE/'python-tests.log').relative_to(ROOT)),'sha256':sha(HERE/'python-tests.log')})
test_results=[]
for name,expected in [('QuizTest',6),('CurriculumContractTest',5),('GeneratedFixtureTest',1)]:
    path=HERE/f'TEST-se.korkort.{name}.xml'
    xml=ET.parse(path).getroot()
    counts={k:int(xml.attrib[k]) for k in ['tests','failures','errors','skipped']}
    check(name+' passed',counts=={'tests':expected,'failures':0,'errors':0,'skipped':0},counts)
    test_results.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),**counts})
check('Configured Kotlin/Gradle build passed','BUILD SUCCESSFUL' in (HERE/'gradle-tests.log').read_text(),'Temporary desktop test source-set invocation; 12 tests')
for name in ['README.md','review.md']:
    broken=[]
    for link in re.findall(r'\]\(([^)]+)\)',(HERE/name).read_text()):
        if '://' in link or link.startswith('#') or link=='verification.json':continue
        if not (HERE/link.split('#')[0]).exists():broken.append(link)
    check(name+' local links resolve',not broken,broken)
artifacts=[p for p in HERE.rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts]
report={'step':'9A3','date':'2026-10-15','status':'complete' if all(c['passed'] for c in checks) else 'blocked',
        'scope':'Deterministic schema-1 compiler and exact unscored fixture; real imports and release/device acceptance remain later work.',
        'authorization':'User: “ok go ahead with next step” after 9A2.',
        'checks':checks,'totals':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'python_tests':44,'jvm_tests':12,**totals},
        'jvm_results':test_results,'fixture_identity':m['identity'],
        'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(artifacts)],
        'tool_files':[{'path':p,'sha256':sha(ROOT/p)} for p in ['tools/build_content.py','tools/content_schema.py','tools/compile_curriculum.py','tools/test_compile_curriculum.py']],
        'next_step':'9B1, separately requested'}
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':report['status'],'totals':report['totals'],'failed':[c for c in checks if not c['passed']]},indent=2))
raise SystemExit(0 if report['status']=='complete' else 1)
