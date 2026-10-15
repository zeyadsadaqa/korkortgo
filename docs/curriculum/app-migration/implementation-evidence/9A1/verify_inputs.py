"""9A1 local identity audit. --freeze writes only this step's baseline; --check is read-only."""
import argparse
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = 'docs/curriculum/'
MIG = BASE + 'app-migration/'

def read(path):
    return json.loads((ROOT / path).read_text())

def digest(path):
    p = ROOT / path
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def audit():
    bindings, checks, observed = [], [], {}
    def actual(path):
        if path not in observed:
            p = ROOT / path
            observed[path] = {'path': path, 'sha256': digest(path), 'bytes': p.stat().st_size if p.is_file() else None}
        return observed[path]['sha256']
    def bind(rec, authority, group):
        path, expected = rec['path'], rec['sha256']
        got = actual(path)
        bindings.append({'path': path, 'authority': authority, 'group': group,
                         'expected_sha256': expected, 'actual_sha256': got,
                         'status': 'match' if got == expected else ('missing' if got is None else 'changed')})
    def check(name, ok, detail):
        checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    b = read(MIG + 'baseline.json')
    v = read(MIG + 'verification.json')
    index_path = BASE + 'app-design/8n/package-index.json'
    index = read(index_path)
    final = read(BASE + 'app-design/8o/verification.json')
    approval_path = BASE + 'pdf-production/final-review/screen-release.json'
    approval = read(approval_path)
    for key in ['frozen_inputs', 'bundled_assets']:
        for n, rec in enumerate(b[key]):
            bind(rec, f'{MIG}baseline.json#/{key}/{n}', '7A/' + key)
    for n, rec in enumerate(v['input_manifest']):
        bind(rec, f'{MIG}verification.json#/input_manifest/{n}', '7G/input_manifest')
    for name in ['curriculum-map', 'question-map', 'question-actions', 'link-and-progress-map', 'implementation-backlog', 'preview-content']:
        d = read(MIG + name + '.json')
        key = 'input_bindings' if name == 'curriculum-map' else 'inputs'
        for n, rec in enumerate(d[key]):
            bind(rec, f'{MIG}{name}.json#/{key}/{n}', 'cross_stage')
    bind(index['specification'], index_path + '#/specification', 'design/specification')
    for n, rec in enumerate(index['inputs']):
        bind(rec, index_path + f'#/inputs/{n}', 'design/inputs')
    bind(final['package_index'], BASE + 'app-design/8o/verification.json#/package_index', 'design/index')
    for task in index['approved_preview_tasks']:
        owner = index_path + '#/' + task['step']
        for rec in [task['binding'], task['review'], *task['prompts'], *task['outputs']]:
            bind(rec, owner, 'design/approved_artifacts')
        content = read(task['binding']['path'])
        check(task['step'] + ' explicit revision approval', content['status'] == 'approved' and content['approval_record'] == task['approval'] and bool(task['approval']['user_statement']), task['approval'])
        for n, rec in enumerate(content.get('input_bindings', [])):
            bind(rec, task['binding']['path'] + f'#/input_bindings/{n}', 'design/bindings')
        for prefix in ['fixture', 'source']:
            if content.get(prefix + '_sha256'):
                bind({'path': content[prefix + '_path'], 'sha256': content[prefix + '_sha256']}, task['binding']['path'] + '#/' + prefix, 'design/bindings')
    for path in [approval['artifact'], BASE + 'pdf-production/korkortgo-curriculum-tagged.pdf', 'output/pdf/korkortgo-curriculum.pdf', 'output/pdf/korkortgo-curriculum-tagged.pdf']:
        bind({'path': path, 'sha256': approval['sha256']}, approval_path, 'release/delivery_copies')
    bind({'path': approval['earlier_approved_source'], 'sha256': approval['earlier_approved_sha256']}, approval_path, 'release/corrected_review_source')
    check('Approved screen release', approval['status'] == 'approved' and approval['edition'] == 'screen' and approval['pages'] == 578 and approval['sha256'] == b['release']['sha256'] == v['approved_release']['sha256'], {'sha256': approval['sha256'], 'pages': approval['pages'], 'approval_statement': approval['approval_statement']})
    check('Saved 7G acceptance', v['status'] == 'passed' and len(v['checks']) == 60 and all(c['passed'] for c in v['checks']) and not v['planning_blockers'], '60 saved checks; no upstream validators rerun or rewritten')
    check('Saved 8O technical acceptance', final['technical_result'] == 'PASS' and len(final['checks']) == 681 and all(c['pass'] for c in final['checks']), '681 saved checks; final human approval is recorded separately in app-design-review.md')
    review_path = BASE + 'app-design-review.md'
    review = (ROOT / review_path).read_text()
    approval_text = '**Final package approval:** Given on 15 October 2026. User statement: “yes approved”.'
    check('Complete-package approval recorded', approval_text in review and '8O and step 8 complete' in review, {'path': review_path, 'statement': approval_text})
    check('Approved preview coverage', len(index['approved_preview_tasks']) == 12 and sum(len(t['outputs']) for t in index['approved_preview_tasks']) == 16, {'tasks': 12, 'boards': 16})
    bank = read('content/questions.json')
    actions = read(MIG + 'question-actions.json')
    check('Baseline question identity', [q['id'] for q in bank] == b['question_ids_in_order'] and len(bank) == 1000 and len({q['id'] for q in bank}) == 1000 and len({q['concept'] for q in bank}) == 500, {'questions': len(bank), 'concepts': len({q['concept'] for q in bank})})
    counts = dict(collections.Counter(q['disposition'] for q in actions['questions']))
    check('Dispositions and holds retained', counts == {'retain': 336, 'rewrite': 626, 'replace': 38} and len(v['question_asset_holds']) == 38, counts)
    frozen_paths = {r['path'] for r in b['frozen_inputs']}
    source_paths = sorted(str(p.relative_to(ROOT)) for folder in ['composeApp/src', 'iosApp'] for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in ['.kt', '.swift', '.plist'])
    additions = sorted(set(source_paths) - frozen_paths)
    check('App source inventory covered', not additions, {'extensions': ['.kt', '.swift', '.plist'], 'files': len(source_paths), 'unreviewed_additions': additions})
    for path in source_paths:
        actual(path)
    # Newly frozen context has no invented historical checksum/approval claim.
    context_paths = [MIG + 'baseline.json', MIG + 'verification.json', MIG + 'verification.md', BASE + 'app-design/8o/verification.json', BASE + 'app-design/8o/verify_design_package.py', review_path, BASE + 'implementation-plan.md', str(Path(__file__).relative_to(ROOT))]
    for path in context_paths:
        actual(path)
    bad = [r for r in bindings if r['status'] != 'match']
    check('All retained identity bindings match', not bad, {'bindings': len(bindings), 'mismatches': len(bad)})
    blockers = [{'path': r['path'], 'status': r['status'], 'expected_sha256': r['expected_sha256'], 'actual_sha256': r['actual_sha256'], 'affected_audit': r['authority'], 'required_action': 'Refresh the affected audit and dependent package review; do not replace expected hashes solely to accept drift.'} for r in bad]
    blockers += [{'check': c['name'], 'detail': c['detail']} for c in checks if not c['passed'] and c['name'] != 'All retained identity bindings match']
    inventory = sorted(observed.values(), key=lambda r: r['path'])
    manifest_sha = hashlib.sha256(json.dumps(inventory, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    referenced = {r['path'] for r in bindings}
    return {'schema_version': 1, 'step': '9A1', 'executed_on': '2026-10-15',
            'authorization': 'User: “ok go ahead with 9A1”; no subsequent task authorized.',
            'status': 'complete' if not blockers else 'blocked',
            'scope': 'Local stored-input identity and approval readiness only; no new source-currency, content, rendering, device or scoring acceptance.',
            'input_manifest_sha256': manifest_sha, 'input_manifest': inventory,
            'retained_bindings': bindings,
            'newly_frozen_context': [{'path': p, 'sha256': actual(p), 'basis': 'Current execution context; no prior digest claimed. Final approval text was read from its recorded review.'} for p in context_paths if p not in referenced],
            'checks': checks, 'totals': {'unique_files': len(inventory), 'retained_bindings': len(bindings), 'matching_bindings': len(bindings)-len(bad), 'groups': dict(collections.Counter(r['group'] for r in bindings)), 'checks': len(checks), 'checks_passed': sum(c['passed'] for c in checks)},
            'blockers': blockers, 'carry_forward': v['carry_forward'],
            'carry_forward_interpretation': 'Historical design-not-started text is superseded by 8O approval; real delivery, scoring, source-currency and platform proof remain open. Print remains deferred.',
            'next_step': '9A2, only when separately requested' if not blockers else 'Resolve listed identity/approval blockers before 9A2'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--freeze', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    target = HERE / 'input-baseline.json'
    if args.freeze:
        with target.open('x') as stream:
            stream.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        matches = True
    else:
        saved = json.loads(target.read_text())
        matches = saved == result
        if not matches:
            old = {r['path']: r['sha256'] for r in saved['input_manifest']}
            now = {r['path']: r['sha256'] for r in result['input_manifest']}
            print(json.dumps({'changed_since_9A1': sorted(p for p in set(old) | set(now) if old.get(p) != now.get(p))}, indent=2))
    print(json.dumps({'status': result['status'], 'frozen_snapshot_matches': matches, 'totals': result['totals'], 'blockers': result['blockers']}, indent=2))
    raise SystemExit(0 if result['status'] == 'complete' and matches else 1)
