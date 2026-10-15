"""Check 9A2 scope and retained evidence; writes only this task's verification.json."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REL = str(HERE.relative_to(ROOT))
BASELINE = 'docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json'
QUIZ = 'composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt'
CURRICULUM = 'composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt'
TEST = 'composeApp/src/commonTest/kotlin/se/korkort/CurriculumContractTest.kt'
PLAN = 'docs/curriculum/implementation-plan.md'
PROGRESS = 'docs/curriculum/progress.md'

def sha(path):
    p = ROOT/path
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

base = json.loads((ROOT/BASELINE).read_text())
checks = []
def check(name, ok, evidence):
    checks.append({'name': name, 'passed': bool(ok), 'evidence': evidence})

check('9A1 accepted entry record', base['status'] == 'complete' and not base['blockers'] and base['totals']['checks_passed'] == 21, {'path': BASELINE, 'sha256': sha(BASELINE)})
expected = {r['path']: r['sha256'] for r in base['input_manifest']}
changed = [{'path': path, 'before_sha256': old, 'after_sha256': sha(path)} for path, old in expected.items() if sha(path) != old]
allowed = {QUIZ, PLAN}
check('Only declared existing baseline inputs changed', {r['path'] for r in changed} == allowed, changed)
quiz_bytes = (ROOT/QUIZ).read_bytes()
marker = b'\n// Migration contract only.'
prefix = quiz_bytes.split(marker, 1)[0]
check('Original quiz implementation byte-identical', marker in quiz_bytes and hashlib.sha256(prefix).hexdigest() == expected[QUIZ], {'legacy_prefix_sha256': hashlib.sha256(prefix).hexdigest(), 'expected': expected[QUIZ]})
source_paths = sorted(str(p.relative_to(ROOT)) for folder in ['composeApp/src','iosApp'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.kt','.swift','.plist'])
new_sources = sorted(set(source_paths)-set(expected))
check('Only declared Kotlin source additions', new_sources == sorted([CURRICULUM, TEST]), new_sources)
check('Gradle/dependency declarations unchanged', all(sha(path)==expected[path] for path in ['build.gradle.kts','composeApp/build.gradle.kts','settings.gradle.kts','gradle.properties']), 'Existing standard-library/common-test dependencies only')
check('Prior audit/approval and source payload identities retained', all(sha(path)==old for path,old in expected.items() if path not in allowed), {'unchanged_files': len(expected)-len(allowed), 'includes': 'question bank, assets, manuscript, production corrections, source registries, design approvals/previews, 9A1 checker and original audit manifests'})
xmls=[]
for name,count in [('CurriculumContractTest',5),('QuizTest',6)]:
    path = f'{REL}/TEST-se.korkort.{name}.xml'
    tree = ET.parse(ROOT/path).getroot()
    result = {k:int(tree.attrib[k]) for k in ['tests','failures','errors','skipped']}
    result.update({'path':path,'sha256':sha(path),'test_names':[n.attrib['name'] for n in tree.findall('testcase')]})
    check(name+' saved test suite passed', result['tests']==count and result['failures']==result['errors']==result['skipped']==0, result)
    # The current generated report must still agree with the retained run evidence.
    current = f'composeApp/build/test-results/desktopTest/TEST-se.korkort.{name}.xml'
    check(name+' build report matches retained run', sha(current)==result['sha256'], {'build_report':current})
    xmls.append(path)
for name in ['content-contract.md','review.md']:
    path=HERE/name
    broken=[]
    for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if '://' not in link and not link.startswith('#') and not (path.parent/link.split('#')[0]).exists():
            broken.append(link)
    check(name+' local links resolve',not broken,broken)
artifacts = [QUIZ,CURRICULUM,TEST,PLAN,PROGRESS,BASELINE,f'{REL}/content-contract.md',f'{REL}/review.md',f'{REL}/verify_contract.py',*xmls]
report = {'step':'9A2','date':'2026-10-15','authorization':'User: “ok next” after completed 9A1; next planned task is 9A2.',
          'status':'complete' if all(c['passed'] for c in checks) else 'blocked',
          'schema_version':1,'scope':'Typed model/schema declarations, local contract tests and retained-input scope verification. No runtime import/loader/UI integration.',
          'baseline':{'path':BASELINE,'sha256':sha(BASELINE),'incoming_check':'9A1 --check passed before any changes; 1174 bindings, 21 checks'},
          'intended_baseline_changes':changed,'new_source_paths':new_sources,
          'artifacts':[{'path':path,'sha256':sha(path)} for path in artifacts],
          'build':{'command':"JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon",'exit_code':0,'tests':11,'contract_tests':5,'existing_quiz_tests':6,'limitations':'Desktop/common compilation only; no Android/iOS/wasm/device/accessibility certification.'},
          'checks':checks,'totals':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'tests':11},
          'remaining_work':['9A3 deterministic validation/generation','9B/9C full content/source/assets import','9D identities/reveal integration and descriptions','9E–9J content/delivery/active-pool acceptance','9K–9O routing/UI/state/platform work','step 10 finished-app verification'],
          'next_step':'9A3, separately requested'}
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'totals':report['totals'],'failed_checks':[c for c in checks if not c['passed']]},indent=2))
raise SystemExit(0 if report['status']=='complete' else 1)
