"""Verify exact 9D evidence, frozen live content, generated identity and test results."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'tools'))
from prepare_assessment_9d import outputs, BASE, sha, read


def verify():
    expected = outputs()
    for path, data in expected.items():
        assert (ROOT/path).read_text() == json.dumps(data, ensure_ascii=False, indent=2)+'\n', path
    batches = [data for path, data in expected.items() if path.name == 'description-acceptance.json']
    rows = [q for batch in batches for q in batch['questions']]
    assert len(rows) == len({q['question_id'] for q in rows}) == 616
    assert sum(len(q['images']) for q in rows) == 1540
    assert sum(bool(q['open_delivery_holds']) for q in rows) == 38
    assert all(not q['scored_activation'] for q in rows)
    library = expected[BASE/'9D2/reviewed-descriptions.json']['assets']
    for asset in library:
        for evidence in [asset['asset'], asset['review']['proof_sheet'], asset['review']['detail_sheet']]:
            if evidence:
                assert sha(Path(evidence['path'])) == evidence['sha256'], evidence['path']
    trace = read(BASE/'9D1/trace.json')
    for output in trace['outputs']:
        assert sha(BASE/'9D1/generated'/output['path']) == output['sha256']
    generated = '\n'.join(p.read_text() for p in (HERE/'generated').glob('*.kt'))
    for n in range(1,5):
        assert f'OptionId("situation-001-option-{n}")' in generated
    reports = sorted(HERE.glob('TEST-*.xml'))
    suites = []
    for path in reports:
        data = ET.parse(path).getroot().attrib
        assert int(data['failures']) == int(data['errors']) == int(data.get('skipped', 0)) == 0
        suites.append({'suite': data['name'], 'tests': int(data['tests'])})
    assert sum(s['tests'] for s in suites) == 21
    assert 'BUILD SUCCESSFUL' in (HERE/'gradle-tests.txt').read_text()
    python_log = (HERE/'python-tests.txt').read_text()
    assert re.search(r'Ran 91 tests in [\d.]+s\s+OK', python_log)
    # Fixed pre-9D revision: later commits do not silently redefine the original baseline.
    baseline = '5264f7c1187d6cd26a2ece977523404d1ee3fa24'
    protected = ['content/questions.json', 'content/curriculum.json', 'content/signs.json',
                 'composeApp/src/commonMain/kotlin/se/korkort/Bank.kt',
                 'docs/curriculum/app-migration/question-actions.json',
                 'docs/curriculum/app-migration/implementation-backlog.json']
    unchanged = []
    for path in protected:
        original = subprocess.check_output(['git','show',f'{baseline}:{path}'], cwd=ROOT)
        digest = hashlib.sha256(original).hexdigest()
        assert sha(Path(path)) == digest, f'Protected input changed: {path}'
        unchanged.append({'path':path, 'sha256':digest})
    paths = set(expected)
    for n in range(1,16):
        paths.update(p.relative_to(ROOT) for p in (ROOT/BASE/f'9D{n}').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'verification.json')
    paths.update(Path(p) for p in [
        'composeApp/build.gradle.kts', 'composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt',
        'composeApp/src/commonMain/kotlin/se/korkort/Assessment.kt',
        'composeApp/src/commonMain/kotlin/se/korkort/AssessmentCard.kt',
        'composeApp/src/commonTest/kotlin/se/korkort/AssessmentTest.kt',
        'composeApp/src/desktopTest/kotlin/se/korkort/AssessmentSemanticsTest.kt',
        'tools/compile_curriculum.py', 'tools/test_compile_curriculum.py',
        'tools/prepare_assessment_9d.py', 'tools/test_prepare_assessment_9d.py'])
    return {'schema_version':1, 'status':'passed', 'checked_on':'2026-10-16',
            'completed_steps':[f'9D{n}' for n in range(1,16)],
            'counts':{'baseline_questions':1000,'authored_option_ids':4000,'sign_questions':616,
                      'review_batches':13,'physical_descriptions':308,'image_occurrences':1540,
                      'open_target_delivery_holds':38,'python_tests':91,'kotlin_desktop_tests':21},
            'test_suites':suites, 'protected_baseline_revision':baseline, 'unchanged_inputs':unchanged,
            'scored_activation':False, 'device_acceptance':False,
            'scope':'Identity, component reveal/keyboard/semantics, and per-ID physical-description review. Full question and image delivery acceptance remain 9E/9F/9L/9O.',
            'files':[{'path':str(path),'sha256':sha(path)} for path in sorted(paths)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(verify(), ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert (HERE/'verification.json').read_text() == data, 'Stale verification receipt'
    else:
        (HERE/'verification.json').write_text(data)
    print('9D1–9D15 verified: 616 questions, 308 physical descriptions, 1,540 image occurrences; 91 Python and 21 Kotlin/desktop tests; 38 delivery holds retained.')


if __name__ == '__main__':
    main()
