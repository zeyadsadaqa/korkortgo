"""Verify this delivery review without promoting held candidates to accepted."""
import argparse,hashlib,json,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent

def receipt():
    preserved=['content/questions.json','content/curriculum.json','content/sources.json','composeApp/src/commonMain/kotlin/se/korkort/Bank.kt','composeApp/src/commonMain/composeResources/files/signs','composeApp/src/commonMain/composeResources/files/curriculum','docs/curriculum/sign-assets','docs/curriculum/app-migration/question-actions.json']
    for path in preserved:
        assert not subprocess.check_output(['git','diff','621cfb4','--',path],cwd=ROOT),path
    summary=json.loads((HERE/'delivery-summary.json').read_text())
    assert summary['steps_reviewed']==19 and summary['delivery_acceptances']==0
    assert summary['replacement_questions']==summary['legacy_replacements_excluded_from_scoring']==38
    assert summary['question_records_changed']==0
    assert sum(r['faint_small_preview'] for r in summary['steps'])==12
    for row in summary['steps']:
        proof=json.loads((HERE.parent/row['step']/'delivery-proof.json').read_text())
        assert not any(proof[k] for k in ['delivery_accepted','scored_activation','question_changes_applied'])
        for target in ['ios-simulator','wasm']:assert (HERE/target/(row['code']+'.png')).exists()
    captures=json.loads((HERE/'android/complete.json').read_text())['captures']
    assert len(captures)==76 and all(r['exact_assets_loaded'] and r['pixel_copy_result']==0 for r in captures)
    build=json.loads((HERE/'android/capture-build.json').read_text())
    for r in build['render_inputs']:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
    suites=[ET.parse(p).getroot() for p in (HERE/'tests').glob('TEST-*.xml')]
    assert sum(int(r.attrib['tests']) for r in suites)==39
    assert all(int(r.attrib['failures'])==int(r.attrib['errors'])==int(r.attrib['skipped'])==0 for r in suites)
    assert 'Ran 119 tests' in (HERE/'tests/python-tests.txt').read_text() and '\nOK\n' in (HERE/'tests/python-tests.txt').read_text()
    assert 'BUILD SUCCESSFUL' in (HERE/'tests/platform-build.txt').read_text()
    pixels=json.loads((HERE/'tests/assessment-min-height-pixels.json').read_text())
    assert pixels['height_px']==105 and pixels['painted_pixels']>100
    # Retain the reviewed scope after staging/committing makes git status clean.
    prior=HERE/'verification.json'
    paths=[r['path'] for r in json.loads(prior.read_text())['fingerprints']] if prior.exists() else []
    paths+=subprocess.check_output(['git','ls-files','--modified','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    fingerprints=[]
    for name in sorted(set(filter(None,paths))):
        p=ROOT/name
        if p==HERE/'verification.json' or not p.is_file():continue
        fingerprints.append({'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'checked_on':'2026-10-16','status':'implementation verified; delivery acceptance open','ios_scope':'User explicitly selected simulator instead of physical device','python_tests':119,'desktop_tests':39,'android_captures':76,'ios_simulator_codes':19,'wasm_codes':19,'delivery_acceptances':0,'held_originals':38,'faint_preview_codes':12,'painted_105px_regression':pixels,'unchanged_since_621cfb4':preserved,'fingerprints':fingerprints}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    value=json.dumps(receipt(),indent=2)+'\n';target=HERE/'verification.json'
    if args.check:assert target.read_text()==value,'Verification inputs changed; inspect then regenerate receipt.'
    else:target.write_text(value)
    print('Verified 119 Python / 39 desktop tests, all 19 delivery reviews and retained scoring holds.')
