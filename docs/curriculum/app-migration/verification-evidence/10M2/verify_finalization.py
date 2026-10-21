"""Check the recorded incomplete finalization without changing the frozen 10M1 report."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
B = OUT.parent
R = B.parents[3]
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = 0


def check(value, description):
    global checks
    if not value:
        raise AssertionError(description)
    checks += 1


record = load(OUT / 'completion-record.json')
for row in record['evidence_inputs']:
    p = R / row['path']
    check(p.is_file() and sha(p) == row['sha256'], row['path'])
for row in load(OUT / 'finalization-files.json')['files']:
    p = R / row['path']
    check(p.is_file() and sha(p) == row['sha256'], row['path'])
fp = load(B / '10L2/DEF-10H-001/candidate-fingerprint.json')
current = {p: sha(R / p) for p in fp['source_files']}
check(current == fp['source_files'], 'exact tested source/resource hashes')
fingerprint = hashlib.sha256(json.dumps(sorted(current.items()), separators=(',', ':')).encode()).hexdigest()
check(fingerprint == record['candidate']['source_runtime_fingerprint'], 'source/runtime fingerprint')
check(sha(R / 'content/accepted-content-manifest.json') == record['candidate']['accepted_manifest_file_sha256'], 'accepted manifest')
index = load(B / 'evidence-index.json')
check(index['candidate']['source_runtime_fingerprint'] == fingerprint, '10M1 candidate matches final record')
check(index['status'] == 'blocked_incomplete' and not index['step10_complete'], '10M1 remains incomplete')
check(record['task_status'] == 'blocked_by_incomplete_10M1' and not record['prerequisite_passing_10M1'], 'M2 prerequisite explicitly unmet')
check(not record['step10_complete'] and not record['plan_complete'] and not record['release_accepted'], 'no false closure')
check(record['open_product_findings'] == index['defects']['open'] and len(record['open_product_findings']) == 18, 'all open findings retained')
check(record['closed_product_findings'] == index['defects']['closed'] == ['DEF-10H-001'], 'bounded closure retained')
check(record['open_gates'] == [g['gate'] for g in index['gates'] if g['status'] == 'open'], 'all nine open gates retained')
check(record['required_cases']['artwork'] == len(index['platform_cases']['artwork_cases']) == 2920, 'artwork denominator')
check(record['required_cases']['normal_production_journeys'] == len(index['platform_cases']['normal_production_journeys']) == 132, 'journey denominator')
check(record['conditional_contracts'] == [c['id'] for c in index['conditional_contracts']], 'four conditional contracts retained')
for target in re.findall(r'\]\(([^)]+)\)', (B / 'verification-report.md').read_text()):
    if '://' not in target and not target.startswith('#'):
        check((B / target.split('#')[0]).is_file(), 'report link ' + target)
changed = subprocess.check_output(['git', 'diff', '--name-only', record['entry_commit'], '--'], cwd=R, text=True).splitlines()
allowed = {'docs/curriculum/implementation-plan.md', 'docs/curriculum/progress.md'}
prefix = str(OUT.relative_to(R)) + '/'
check(all(p in allowed or p.startswith(prefix) for p in changed), 'only finalization documentation changed since entry')
untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=R, text=True).splitlines()
check(all(p.startswith(prefix) for p in untracked), 'no untracked production input')
plan = (R / 'docs/curriculum/implementation-plan.md').read_text()
progress = (R / 'docs/curriculum/progress.md').read_text()
check('Finalization status — 21 October 2026: recorded incomplete' in plan, 'plan status visible')
check('Closure evaluated; blocked by incomplete 10M1' in progress, 'tracker stays blocked')
check(not record['publication'], 'no publication')
print(f'PASS: {checks} finalization checks; candidate unchanged; plan and step 10 remain incomplete with 18 findings.')
