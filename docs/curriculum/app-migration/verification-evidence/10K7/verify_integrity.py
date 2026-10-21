"""Validate saved10K receipts and honest open dispositions; never declare product acceptance."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).resolve().parent
B = OUT.parent
R = OUT.parents[4]
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
parser = argparse.ArgumentParser()
parser.add_argument('--seal', action='store_true', help='Write new per-task artifact manifests before verification')
args = parser.parse_args()
excluded = {'artifacts.json', 'integrity-results.json'}
def files(folder):
    return sorted(p for p in folder.rglob('*') if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts)
if args.seal:
    for n in range(1, 8):
        folder = B / f'10K{n}'
        rows = [{'path': str(p.relative_to(folder)), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in files(folder)]
        (folder / 'artifacts.json').write_text(json.dumps({'task': folder.name, 'files': rows, 'excluded': sorted(excluded)}, indent=2) + '\n')
checks = []
def check(name, value):
    checks.append({'name': name, 'pass': bool(value)})
    if not value:
        raise AssertionError(name)
for n in range(1, 8):
    folder = B / f'10K{n}'
    rows = load(folder / 'artifacts.json')['files']
    check(f'{folder.name} exact manifest inventory', set(x['path'] for x in rows) == {str(p.relative_to(folder)) for p in files(folder)})
    for row in rows:
        p = folder / row['path']
        check(f'{folder.name}/{row["path"]}', p.exists() and sha(p) == row['sha256'] and p.stat().st_size == row['bytes'])
    environment = load(folder / 'environment.json')
    check(f'{folder.name} same candidate fingerprint', environment['source_runtime_fingerprint'] == load(OUT / 'final-candidate-fingerprint.json')['candidate_source_fingerprint'])
    storage = folder / 'capture-storage.json'
    if storage.exists():
        mapping = load(storage)
        check(f'{folder.name} duplicate count', len(mapping['aliases']) == mapping['removed_duplicate_files'])
        for alias in mapping['aliases']:
            logical, stored = folder / alias['logical_path'], folder / alias['stored_path']
            check(f'{folder.name} logical capture {alias["logical_path"]}',
                  not logical.exists() and stored.is_file() and sha(stored) == alias['sha256'] and stored.stat().st_size == alias['bytes'])
captures = load(B / '10K3/capture-index.json')['captures']
check('148 desktop logical captures retained', len(captures) == 148)
for capture in captures:
    check('desktop capture ' + capture['path'], sha(B / '10K3' / capture.get('stored_path', capture['path'])) == capture['sha256'])
cleanup = load(OUT / 'cleanup-record.json')
check('37 exact duplicates removed with aliases', cleanup['removed_duplicate_screenshots'] == 37 and cleanup['bytes_saved'] == 4592412)
for task, expected in [('10K1', (85, 0, 0, 0)), ('10K3', (44, 2, 0, 0))]:
    suites = [ET.parse(p).getroot() for p in (B / task / 'test-reports').glob('TEST-*.xml')]
    totals = tuple(sum(int(s.get(k, 0)) for s in suites) for k in ('tests', 'failures', 'errors', 'skipped'))
    check(f'{task} actual JUnit totals {expected}', totals == expected)
common = load(B / '10K1/common-results.json')
check('150 actual Python tests', common['python_unittest']['tests'] == 150 and common['python_unittest']['status'] == 'pass')
resources = []
for n in range(2, 7):
    for p in (B / f'10K{n}').glob('*resource*.json'):
        x = load(p)
        if 'checks' in x:
            resources.append(p)
            check(str(p.relative_to(B)) + ' all490 bytes', x['status'] == 'pass' and len(x['checks']) == 490 and all(c['pass'] for c in x['checks']))
check('all12 normal/proof/restored resource receipts', len(resources) == 12)
for name in ('initial-http-parity.json', 'http-parity.json'):
    x = load(B / '10K6' / name)
    check(name + '783 HTTP bytes', x['status'] == 'pass' and x['served_files'] == 783 and all(c['pass'] for c in x['checks']))
for task in ('10K2', '10K4', '10K6'):
    check(task + ' restoration', load(B / task / 'runtime-restored.json')['status'] == 'pass')
ios = load(B / '10K4/ios-simulator-results.json')
check('iOS native6/6 with no skip', ios['native_tests'] == {'tests': 6, 'passed': 6, 'failed': 0, 'skipped': 0})
device = load(B / '10K5/ios-device-build-results.json')
check('device ARM64 platform2 all2837 objects', device['architecture'] == 'arm64' and device['object_build_platforms'] == {'2': 2837} and device['proof_flag'] is False)
fp = load(OUT / 'final-candidate-fingerprint.json')
check('source/runtime files still exact', all(sha(R / p) == digest for p, digest in fp['source_files'].items()))
check('accepted manifest file unchanged', sha(R / 'content/accepted-content-manifest.json') == fp['manifest_file_sha256'])
baseline = load(OUT / 'baseline-exit.json')
check('protected baseline and historical receipts unchanged', baseline['status'] == 'pass' and not baseline['historical_receipts_modified'] and not baseline['changed_baseline_inputs'])
matrix = load(OUT / 'platform-matrix.json')
check('all2920 artwork and132 exact flow cases dispositioned', len(matrix['artwork_cases']) == 2920 and len(matrix['normal_production_journeys']) == 132)
check('no false full matrix passes', matrix['counts']['required_artwork_cases_closed'] == 0 and matrix['counts']['normal_production_journeys_closed'] == 0)
check('seven T10 clauses; five remain required open', len(matrix['T10_clauses']) == 7 and sum(x['status'].startswith('open_') for x in matrix['T10_clauses']) == 5)
check('same1000 renderer payloads independently reconciled', len(load(OUT / 'renderer-fixture-reconciliation.json')['questions']) == 1000 and load(OUT / 'renderer-fixture-reconciliation.json')['all_renderer_payloads_identical'])
defects = load(OUT / 'defects.json')
check('18 inherited plus1 new =19 open', len(defects['open_product_defects']) == 19 and len(defects['new_product_findings']) == 1)
for finding in defects['new_product_findings']:
    for evidence in finding['evidence']:
        check('new finding evidence ' + evidence, (B / '10K6' / evidence).is_file())
for n in range(1, 8):
    for p in (B / f'10K{n}').glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' not in target and not target.startswith('#'):
                check(str(p.relative_to(B)) + ' link ' + target, (p.parent / target.split('#')[0]).exists() or (p.parent == OUT and target == 'integrity-results.json'))
result = {'status': 'pass_saved_evidence_integrity_not_product_acceptance', 'checks': len(checks),
          'artifact_files': sum(len(load(B / f'10K{n}' / 'artifacts.json')['files']) for n in range(1, 8)),
          'failed_integrity_checks': 0, 'product_acceptance': 'T10 and step10 incomplete;19 product findings and uncompleted required matrix retained',
          'check_results': checks}
(OUT / 'integrity-results.json').write_text(json.dumps(result, indent=2) + '\n')
print(result['status'], result['checks'], 'checks,', result['artifact_files'], 'files')
