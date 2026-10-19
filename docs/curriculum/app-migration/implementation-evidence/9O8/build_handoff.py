"""Build/check the dated implementation handoff index; never modifies app content."""
import argparse
import collections
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/curriculum/app-migration/implementation-evidence'
INDEX = BASE / 'evidence-index.json'

@lru_cache(maxsize=None)
def read(path):
    return json.loads((ROOT / path).read_text())

@lru_cache(maxsize=None)
def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def build():
    files = {}
    def record(path):
        path = Path(path)
        path = path.relative_to(ROOT) if path.is_absolute() else path
        assert (ROOT / path).is_file(), path
        if ROOT / path in (INDEX, BASE / '9O8/results.json'):
            return {'path': str(path), 'binding': 'derived handoff artifact; no recursive hash'}
        row = {'path': path.as_posix(), 'sha256': digest(path)}
        files[row['path']] = row
        return row
    def evidence(path):
        path = Path(path)
        if path.is_dir():
            return [record(p) for p in sorted(path.rglob('*')) if p.is_file() and p.name != '.DS_Store']
        return [record(path)]
    plan_path = Path('docs/curriculum/implementation-plan.md')
    plan = (ROOT / plan_path).read_text()
    groups = list(re.finditer(r'^### (9[A-O])\. .*$', plan, re.M))
    headings = list(re.finditer(r'^#{3,4} .+$', plan, re.M))
    steps = []
    def links(text):
        result = []
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', '#')):
                continue
            path = (ROOT / plan_path.parent / target.split('#')[0]).resolve()
            assert path.is_relative_to(ROOT) and path.exists(), target
            result.extend(evidence(path))
        return sorted({r['path'] for r in result})
    for match in re.finditer(r'^#### (9[A-O]\d+)\. (.+)$', plan, re.M):
        step, title = match.groups()
        group = re.match(r'9[A-O]', step)[0]
        gm = next(g for g in groups if g[1] == group)
        group_end = next(h.start() for h in headings if h.start() > gm.start())
        intro = plan[gm.end():group_end]
        end = next((h.start() for h in headings if h.start() > match.start()), len(plan))
        body = plan[match.end():end]
        statements = re.findall(r'^\*\*(?:Status|Completed|Execution record|Execution |Current status)[^\n]*', body, re.M)
        inherited = re.findall(r'^\*\*(?:Status|Completed|Execution record|Execution |Current status)[^\n]*', intro, re.M)
        assert statements or inherited, step
        refs = links(intro) + links(body)
        assert refs, step
        row = {'step': step, 'title': title, 'plan_line': plan[:match.start()].count('\n') + 1,
               'status': 'complete_recorded_implementation', 'completion_records': statements,
               'group_records': inherited, 'evidence_paths': sorted(set(refs))}
        if step == '9O6':
            row['status'] = 'build_resources_complete_physical_runtime_excluded_by_policy'
        if group == '9F':
            code = re.search(r'Prove exact (\S+) delivery', title)[1]
            row['accepted_question_ids'] = ['sign-meaning-' + code, 'sign-recognise-' + code]
        for field in ['Input', 'Output', 'Done when']:
            found = re.search(r'^\*\*' + field + r':\*\* (.+)$', body, re.M)
            assert found, (step, field)
            row[field.lower().replace(' ', '_')] = found[1]
        steps.append(row)
    assert len(steps) == 125 and len({s['step'] for s in steps}) == 125
    assert steps[-1]['step'] == '9O8'

    mpath = 'content/accepted-content-manifest.json'
    manifest = read(mpath)
    accepted = read('content/accepted-assessment-questions.json')['questions']
    actions = {q['question_id']: q for q in read('docs/curriculum/app-migration/question-actions.json')['questions']}
    assert len(accepted) == len(actions) == 1000
    assert {q['key']['question_id'] for q in accepted} == set(actions)
    assert len({q['concept_id'] for q in accepted}) == 500
    sources = read('content/package-sources.json')
    references = {r['id'] for r in sources['references']}
    curriculum = read('content/curriculum.json')
    lessons = {i for m in curriculum['modules'] for i in m['lesson_ids']}
    assets = {a['id'] for a in curriculum['assets']}
    def receipt(item):
        ref = item['record']
        path = ref['file']['path']
        row = record(path)
        assert row['sha256'] == ref['file']['sha256'], path
        locator = ref['locator']
        if locator.startswith('json:/'):
            value = read(path)
            for key in locator[6:].split('/'):
                key = key.replace('~1', '/').replace('~0', '~')
                value = value[int(key)] if isinstance(value, list) else value[key]
        return {'path': path, 'locator': locator}
    questions = []
    for n, q in enumerate(accepted):
        key = q['key']; a = q['acceptance']; rel = q['relationship']
        assert a['eligibility'] == 'accepted' and not a['open_holds']
        assert rel['disposition'] == actions[key['question_id']]['disposition']
        assert rel['primary_lesson_id'] in lessons
        assert rel['source_uses'] and all(s['reference_id'] in references for s in rel['source_uses'])
        images = [i for i in [q['image']] + [o['image'] for o in q['options']] if i]
        assert all(i['asset_id'] in assets for i in images)
        content = receipt(a['content_review'])
        for r in a['description_reviews'] + a['delivery_proof']:
            receipt(r)
        if images:
            assert a['description_reviews'] and a['delivery_proof']
        questions.append({'key': key, 'concept_id': q['concept_id'], 'disposition': rel['disposition'],
                          'eligibility': 'accepted', 'primary_lesson_id': rel['primary_lesson_id'],
                          'source_reference_ids': [s['reference_id'] for s in rel['source_uses']],
                          'asset_ids': sorted({i['asset_id'] for i in images}),
                          'accepted_record_locator': f'json:/questions/{n}', 'content_review': content,
                          'description_review_count': len(a['description_reviews']),
                          'delivery_proof_count': len(a['delivery_proof'])})
    counts = dict(collections.Counter(q['disposition'] for q in questions))
    assert counts == {'retain': 336, 'rewrite': 626, 'replace': 38}
    by_id = {q['key']['question_id']: q for q in questions}
    for step in steps:
        for id in step.get('accepted_question_ids', []):
            assert by_id[id]['disposition'] == 'replace'
    aliases = read('content/legacy-aliases.json')
    assert len(aliases['aliases']) == 1921 and not aliases['tombstones']
    alias_counts = dict(collections.Counter(a['lookup']['type'] for a in aliases['aliases']))
    assert alias_counts == {'question': 1000, 'chapter': 39, 'page': 361, 'topic': 178, 'sign': 343}
    canonical_count = (len(curriculum['documents']) + len(curriculum['anchors']) +
                       len(curriculum['reference_groups']) + len(curriculum['sign_entries']) + len(sources['destinations']))
    assert canonical_count == 1123 and len(curriculum['reading_order']) == 60
    assert len(curriculum['lesson_category_tags']) == 40 and len(curriculum['reference_groups']) == 24
    kinds = collections.Counter(d['kind'] for d in curriculum['documents'])
    assert kinds['module_review'] == 10 and kinds['appendix'] == 4
    assert len(curriculum['modules']) == 10 and len(lessons) == 40 and len(assets) == 484
    policy = read('content/delivery-targets.json')
    assert policy['ios_scope'] == 'simulator' and 'ios_device' not in policy['required_platforms']

    platforms = []
    for number in range(2, 8):
        path = BASE / f'9O{number}/results.json'
        report = json.loads(path.read_text())
        assert report['accepted_manifest']['sha256'] == digest(mpath), path
        for row in report['artifacts']:
            assert record(row['path'])['sha256'] == row['sha256'], row['path']
        current_sources = []
        if number == 3:
            current_sources = read(str((BASE / '9O3/test-inputs-final.json').relative_to(ROOT)))
        elif number == 4:
            current_sources = read(str((BASE / '9O4/candidate.json').relative_to(ROOT)))['test_sources']
        elif number == 5:
            current_sources = read(str((BASE / '9O5/candidate.json').relative_to(ROOT)))['source_inputs']
        for source in current_sources:
            assert record(source['path'])['sha256'] == source['sha256'], source['path']
        platforms.append({'step': f'9O{number}', 'result': record(path), 'status': report['status']})
    closure = read('docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14/verification.json')
    drift = []
    for row in closure['files']:
        current = record(row['path'])
        if current['sha256'] != row['sha256']:
            drift.append({'path': row['path'], 'historical_sha256': row['sha256'], 'current_sha256': current['sha256']})
    assert {r['path'] for r in drift} == {'README.md', str(plan_path), 'docs/curriculum/progress.md',
                                        'composeApp/src/verificationAndroidTest/kotlin/se/korkort/NativeReaderRouteTest.kt'}
    for row in drift:
        row['disposition'] = 'expected later documentation update or 9O3 test-selector correction; historical receipt preserved'

    gates = {
        'T01': ('9A 9B 9C', ['9B17/import-parity.json','9O2/resource-origin-parity.json']),
        'T02': ('9C 9K 9L', ['9K/entry-point-checks.json','9O7/source-detail.txt']),
        'T03': ('9D 9E 9F', ['closure-9j-9m-9l14/delivery-acceptance.json','faint-assets-approved/README.md']),
        'T04': ('9G 9H 9I 9J', ['9G/question-acceptance.json','9H/README.md','9I/content-review.json','9J/retained-review.json']),
        'T05': ('9D 9J 9M', ['closure-9j-9m-9l14/accepted-state-contract-results.json','9O2/results.json']),
        'T06': ('9K', ['9K/entry-point-checks.json','9O3/results.json']),
        'T07': ('9K 9L 9M', ['closure-9j-9m-9l14/accepted-state-contract-results.json','9O5/results.json']),
        'T08': ('9L 9N', ['9L/README.md','9O7/library-recovered.txt']),
        'T09': ('9L 9O', ['closure-9j-9m-9l14/learner-copy-audit.json']),
        'T10': ('9C 9F 9O', ['9O2/results.json','9O3/results.json','9O4/results.json','9O5/results.json','9O6/results.json','9O7/results.json'])}
    matrix = []
    for gate, (owners, paths) in gates.items():
        matrix.append({'gate': gate, 'owner_groups': owners.split(),
                       'status': 'implementation_evidence_available_independent_step10_pending',
                       'evidence': [record(BASE / p) for p in paths]})
    required = [mpath, 'content/accepted-assessment-questions.json', 'content/curriculum.json',
                'content/package-sources.json', 'content/legacy-aliases.json', 'content/delivery-targets.json',
                'docs/curriculum/app-migration/question-actions.json', str(plan_path),
                'docs/curriculum/progress.md', 'docs/curriculum/app-migration/assessment-coverage-briefs.md',
                'docs/curriculum/app-migration/provenance-inventory.json', 'docs/curriculum/app-design-review.md',
                'docs/curriculum/app-design/faint-assets-v1/review.md',
                'docs/curriculum/app-migration/implementation-backlog.md',
                'docs/curriculum/app-migration/implementation-evidence/implementation-review.md',
                'docs/curriculum/app-migration/implementation-evidence/9O8/build_handoff.py',
                'docs/curriculum/app-migration/implementation-evidence/9O8/commands.json']
    for path in required:
        record(path)
    commands = read('docs/curriculum/app-migration/implementation-evidence/9O8/commands.json')
    assert len(commands) == 6 and all(c['exit_code'] == 0 for c in commands)
    for row in commands:
        record(row['log'])
    return {'date': '2026-10-20', 'scope': 'Step 9 implementation handoff; not step 10 verification or publication',
            'status': 'implementation_complete_with_recorded_scope_exclusions',
            'accepted_manifest': {'file': record(mpath), 'identity': manifest['identity']},
            'totals': {'executable_steps': len(steps), 'questions': 1000, 'concepts': 500,
                       'accepted': 1000, 'held': 0, 'dispositions': counts, 'canonical_destinations': canonical_count,
                       'aliases': 1921, 'alias_types': alias_counts, 'assets': 484, 'source_references': len(references)},
            'policy': policy, 'steps': steps, 'questions': questions, 'platforms': platforms,
            'step10_matrix': matrix, 'historical_closure_drift': drift,
            'current_implementation_blockers': [], 'step10_status': 'not_started_separate_user_request_required',
            'files': [files[p] for p in sorted(files)]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write the index; default compares it without writes.')
    args = parser.parse_args()
    value = build()
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if args.write:
        INDEX.write_text(text)
    else:
        assert INDEX.read_text() == text, 'handoff index drift; review changed inputs before rebuilding'
    print(f"PASS: {len(value['steps'])} steps, 1000 accepted IDs, 10 pending step-10 gates, {len(value['files'])} file fingerprints.")

if __name__ == '__main__':
    main()
