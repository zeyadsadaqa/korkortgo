"""Verify this correction's receipts without accepting the remaining step10 gates."""
import argparse
import hashlib
import json
import re
import socket
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).resolve().parent
R = OUT.parents[5]
B = OUT.parents[1]
ISSUE = 'DEF-10H-001'
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
folders = [B / task / ISSUE for task in ('10L1', '10L2', '10L3')]
excluded = {'artifacts.json', 'integrity-results.json'}
parser = argparse.ArgumentParser()
parser.add_argument('--seal', action='store_true')
args = parser.parse_args()
def files(folder):
    return sorted(p for p in folder.rglob('*') if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts)
if args.seal:
    for folder in folders:
        rows = [{'path': str(p.relative_to(folder)), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in files(folder)]
        (folder / 'artifacts.json').write_text(json.dumps({'batch': ISSUE, 'files': rows, 'excluded': sorted(excluded)}, indent=2) + '\n')
checks = []
def check(name, value):
    checks.append({'name': name, 'pass': bool(value)})
    if not value:
        raise AssertionError(name)
for folder in folders:
    rows = load(folder / 'artifacts.json')['files']
    check(str(folder.relative_to(B)) + ' exact inventory', {r['path'] for r in rows} == {str(p.relative_to(folder)) for p in files(folder)})
    for row in rows:
        p = folder / row['path']
        check(str(p.relative_to(B)), sha(p) == row['sha256'] and p.stat().st_size == row['bytes'])
entry = load(folders[0] / 'entry-candidate.json')
fp = load(folders[1] / 'candidate-fingerprint.json')
current = {p: sha(R / p) for p in entry['source_files']}
changed = sorted(p for p in current if current[p] != entry['source_files'][p])
check('exact two bounded source changes', changed == sorted(fp['changed_source_inputs']) and len(changed) == 2)
check('final candidate exact source hashes', current == fp['source_files'])
check('final candidate fingerprint', hashlib.sha256(json.dumps(sorted(current.items()), separators=(',', ':')).encode()).hexdigest() == fp['candidate_source_runtime_fingerprint'])
check('accepted manifest unchanged', sha(R / 'content/accepted-content-manifest.json') == entry['manifest_file_sha256'])
check('all other protected inputs unchanged', all(current[p] == digest for p, digest in entry['source_files'].items() if p not in changed))
before = ET.parse(OUT / 'before-regression.xml').getroot()
check('pre-fix failure retained', before.get('tests') == '1' and before.get('failures') == '1')
suites = [ET.parse(p).getroot() for p in (OUT / 'shared-test-reports').glob('TEST-*.xml')]
totals = {k: sum(int(s.get(k, 0)) for s in suites) for k in ('tests', 'failures', 'errors', 'skipped')}
check('38 affected shared tests pass', totals == {'tests': 38, 'failures': 0, 'errors': 0, 'skipped': 0})
original = ET.parse(OUT / 'original-case-after.xml').getroot()
check('original assertion passes unchanged', original.get('tests') == '1' and original.get('failures') == '0')
check('native pre-fix binary identity', load(OUT / 'android-before-identity.json')['same'])
check('native pre-fix catalogue failure retained', 'Road signs and signals' in (OUT / 'android-before-retained-proof-return.json').read_text())
for name in ('android-route-result.json', 'web-route-result.json', 'web-normal-route-result.json', 'restoration-results.json', 'cleanup-results.json'):
    check(name, load(OUT / name)['status'] == 'pass')
ios = load(OUT / 'ios-native-result.json')
check('one actual iOS return assertion passes', ios['passedTests'] == 1 and ios['failedTests'] == 0 and ios['skippedTests'] == 0)
aliases = {x['logical_path']: x for x in load(OUT / 'capture-storage.json')['aliases']}
for logical, row in aliases.items():
    stored = OUT / row['stored_path']
    check('deduplicated capture ' + logical, not (OUT / logical).exists() and sha(stored) == row['sha256'] and stored.stat().st_size == row['bytes'])
attachments = [a for test in load(OUT / 'ios-native-evidence/manifest.json') for a in test['attachments']]
check('eight final logical native iOS attachments', len(attachments) == 8)
for attachment in attachments:
    logical = 'ios-native-evidence/' + attachment['exportedFileName']
    check('native attachment resolves ' + logical, (OUT / aliases.get(logical, {}).get('stored_path', logical)).is_file())
resource_files = list(OUT.glob('*-resources.json'))
check('nine resource receipts including installed app', len(resource_files) == 9)
for p in resource_files:
    x = load(p)
    check(p.name + '490 exact bytes', x['status'] == 'pass' and len(x['checks']) == 490 and all(c['pass'] for c in x['checks']))
http = load(OUT / 'normal-http-parity.json')
check('783 actual normal HTTP files', http['status'] == 'pass' and http['files'] == 783 and all(x['pass'] for x in http['checks']))
for x in load(OUT / 'cleanup-results.json')['servers']:
    port = int(x['origin'].rsplit(':', 1)[1])
    with socket.socket() as connection:
        connection.settimeout(.3)
        check('QA server stopped ' + str(port), connection.connect_ex(('127.0.0.1', port)) != 0)
ledger = load(OUT / 'defects.json')
check('one selected finding closed and18 retained', ledger['closed_product_defects'] == [ISSUE] and len(ledger['open_product_defects']) == 18 and not ledger['step10_complete'])
check('no defect IDs discarded', set(ledger['closed_product_defects'] + ledger['open_product_defects']) == set(load(B / '10K7/defects.json')['open_product_defects']))
check('T07 remains open beyond bounded correction', load(OUT / 'evidence-invalidation-map.json')['gate_dispositions']['T07'].endswith('still open'))
check('original baseline deviation exactly declared', sorted(load(OUT / 'original-baseline-deviation.json')['changed_baseline_inputs']) == changed)
historical_changes = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD', '--', str(B.relative_to(R))], cwd=R, text=True).splitlines()
check('no historical evidence modified', not [p for p in historical_changes if not any('/' + stage + '/' in p for stage in ('10L1', '10L2', '10L3'))] and not load(OUT / 'original-baseline-deviation.json')['historical_receipts_modified'])
# Check the saved10K artifacts independently of its live old-candidate fingerprint assertion.
historical_count = 0
for n in range(1, 8):
    folder = B / f'10K{n}'
    for row in load(folder / 'artifacts.json')['files']:
        check('historical ' + str((folder / row['path']).relative_to(B)), sha(folder / row['path']) == row['sha256'])
        historical_count += 1
for folder in folders:
    for p in folder.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' not in target and not target.startswith('#'):
                check(str(p.relative_to(B)) + ' link ' + target, (p.parent / target.split('#')[0]).exists() or (p.parent == OUT and target == 'integrity-results.json'))
result = {'status': 'pass_bounded_fix_evidence_integrity', 'checks': len(checks), 'artifact_files': sum(len(load(p / 'artifacts.json')['files']) for p in folders), 'historical_10K_files_verified_unchanged': historical_count, 'closed': [ISSUE], 'remaining_open_product_findings': 18, 'step10_complete': False, 'results': checks}
(OUT / 'integrity-results.json').write_text(json.dumps(result, indent=2) + '\n')
print(result['status'], result['checks'], 'checks;', result['artifact_files'], 'new files;', historical_count, 'historical files unchanged')
