"""Audit saved evidence and deterministically assemble 10M1; never rerun historical writers.

Exit 0 means report accounting is valid. Product acceptance remains blocked/incomplete.
--check compares the generated report/index/results without writing any file.
"""
import argparse
from collections import Counter
from functools import cache
import hashlib
import json
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
B = OUT.parent
R = B.parents[3]
ISSUE = 'DEF-10H-001'
L = '10L3/' + ISSUE
@cache
def load(p):
    return json.loads(p.read_text())


sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
dump = lambda x: json.dumps(x, indent=2, ensure_ascii=False) + '\n'
digest = lambda x: hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
checks = Counter()


def check(group, value, detail):
    if not value:
        raise AssertionError(group + ': ' + str(detail))
    checks[group] += 1


def pointer(value, path):
    for part in path.strip('/').split('/') if path else []:
        key = part.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def reference(p):
    return {'path': str(p.relative_to(B)), 'sha256': sha(p)}


def local_reference(origin, target):
    name, _, fragment = target.partition('#')
    p = (origin.parent / name).resolve()
    check('local_references', p.is_file(), target)
    if fragment.startswith('/'):
        return pointer(load(p), fragment)
    return p


def assemble():
    entry = load(OUT / 'entry.json')
    prepared = load(B / '10A3/verification-case-index.json')
    baseline = load(B / '10A1/candidate-baseline.json')
    fp = load(B / ('10L2/' + ISSUE + '/candidate-fingerprint.json'))
    impact = load(B / L / 'evidence-invalidation-map.json')
    current = {p: sha(R / p) for p in fp['source_files']}
    check('candidate', current == fp['source_files'], 'live source inputs')
    actual_fp = hashlib.sha256(json.dumps(sorted(current.items()), separators=(',', ':')).encode()).hexdigest()
    check('candidate', actual_fp == fp['candidate_source_runtime_fingerprint'], 'runtime fingerprint')
    deviations = [x['path'] for x in baseline['tracked_input_fingerprints'] if not (R / x['path']).is_file() or sha(R / x['path']) != x['sha256']]
    allowed = fp['changed_source_inputs'] + ['docs/curriculum/implementation-plan.md', 'docs/curriculum/progress.md']
    check('candidate', sorted(deviations) == sorted(allowed), deviations)
    check('candidate', sha(R / 'content/accepted-content-manifest.json') == fp['accepted_manifest_file_sha256'], 'accepted manifest')
    check('candidate', impact['new_source_runtime_fingerprint'] == actual_fp, 'invalidation map')
    for row in baseline['accepted_bound_file_checks']:
        check('accepted_bound_files', sha(R / row['path']) == row['expected_sha256'], row['path'])

    manifests = sorted(p for p in B.rglob('artifacts.json') if OUT not in p.parents)
    task_rows = []
    for m in manifests:
        data = load(m)
        rows = data if isinstance(data, list) else data['files']
        for row in rows:
            p = m.parent / row['path']
            check('historical_artifact_hashes', p.is_file() and sha(p) == row['sha256'], p)
            if 'bytes' in row:
                check('historical_artifact_sizes', p.stat().st_size == row['bytes'], p)
        task = m.parent.relative_to(B).parts[0]
        reproduction = [p for p in m.parent.iterdir() if p.name == 'commands.json' or p.suffix in ('.py', '.gradle') or p.name in ('review.md', 'reproduction.md', 'defect-triage.md', 'fix-review.md')]
        check('task_accounting', bool(reproduction), task)
        task_rows.append({'task': task, 'execution': 'executed_bounded_cycle' if task.startswith('10L') else 'executed_available_scope',
                          'acceptance': 'complete_preparation_or_import' if task[2] in ('A', 'B') else 'bounded_issue_closed_only' if task.startswith('10L') else 'gate_requirements_remain_open',
                          'dependencies': prepared['task_dependencies'][task], 'artifact_manifest': reference(m), 'artifact_count': len(rows),
                          'reproduction_sources': [reference(p) for p in sorted(reproduction)],
                          'rerun_scope': 'Saved commands/steps and scripts retained and hashed; this audit does not execute historical build/UI/source-check writers. Live old-baseline checks require the explicit 10L impact disposition.'})
    prior_tasks = set(prepared['task_dependencies']) - {'10M1', '10M2'}
    check('task_accounting', {x['task'] for x in task_rows} == prior_tasks and len(task_rows) == 68, 'all prior executable tasks')

    oracle_data = {}
    for key, row in prepared['oracles'].items():
        p = R / row['path']
        check('oracle_files', sha(p) == row['sha256'], key)
        oracle_data[key] = load(p)
    data_cases = load(B / '10A3/data-cases.json')['families']
    for family in data_cases:
        for member in family['members']:
            loc = member['oracle']
            check('prepared_oracle_records', digest(pointer(oracle_data[loc['oracle']], loc['pointer'])) == loc['record_sha256'], member['case_id'])
    for row in prepared['original_coverage_crosswalk']:
        loc = row['oracle']
        check('coverage_families', digest(pointer(oracle_data[loc['oracle']], loc['pointer'])) == loc['record_sha256'], row['original_family'])

    question_source = B / '10E18/complete-question-review.json'
    questions = load(question_source)
    frozen_questions = load(B / '10A3/question-batches.json')['all_question_cases']
    by_id = {q['question_id']: q for q in questions['questions']}
    accepted_by_id = {q['question_id']: q for q in frozen_questions}
    check('questions', len(by_id) == len(questions['questions']) == 1000 and set(by_id) == set(accepted_by_id), 'exact 1000 unique IDs')
    question_rows = []
    for i, q in enumerate(questions['questions']):
        frozen = accepted_by_id[q['question_id']]
        loc = frozen['accepted_snapshot']
        accepted = pointer(oracle_data[loc['oracle']], loc['pointer'])
        check('questions', digest(accepted) == q['accepted_snapshot_sha256'] == loc['record_sha256'], q['question_id'])
        check('questions', q['revision'] == frozen['revision'] and q['owner'] == frozen['owner'], q['question_id'])
        for key in ('generic_contract_review', 'independent_disposition_review'):
            local_reference(question_source, q[key])
        normalized = dict(q)
        for key in ('generic_contract_review', 'independent_disposition_review'):
            name, _, fragment = q[key].partition('#')
            normalized[key] = str((question_source.parent / name).resolve().relative_to(B)) + ('#' + fragment if fragment else '')
        question_rows.append({**normalized, 'outcome_locator': '10E18/complete-question-review.json#/questions/' + str(i),
                              'applicability': 'unchanged_content_input_review; not full runtime/release acceptance'})
    question_counts = Counter(q['status'] for q in question_rows)
    check('questions', question_counts == {'pass': 970, 'open_related_asset_description': 30}, question_counts)
    check('questions', len({q['concept_id'] for q in question_rows}) == 500, '500 concepts')

    approvals = load(B / '10J1/design-comparison-index.json')
    approval_rows = approvals['approval_authority'] + approvals['approval_input_checks']
    approval_rows += [r for board in approvals['approved_boards'] for r in (board, board['review'])]
    for row in approval_rows:
        check('approval_hashes', sha(R / row['path']) == row['sha256'], row['path'])
    check('approval_hashes', len(approvals['approved_boards']) == 17 and len(approvals['states']) == 38, 'approved boards/state index')

    ledger = load(B / L / 'defects.json')
    check('defects', len(ledger['open_product_defects']) == 18 and ledger['closed_product_defects'] == [ISSUE] and not ledger['step10_complete'], '18 open / 1 closed')
    check('defects', set(ledger['open_product_defects'] + ledger['closed_product_defects']) == set(load(B / '10K7/defects.json')['open_product_defects']), 'all 19 findings retained')
    check('defects', {r['id'] for r in ledger['findings']} == set(ledger['open_product_defects'] + ledger['closed_product_defects']), 'records agree with IDs')
    for q in question_rows:
        check('defects', set(q['open_description_findings']).issubset(ledger['open_product_defects']), q['question_id'])
    for name in ('android-route-result.json', 'web-route-result.json', 'web-normal-route-result.json', 'restoration-results.json', 'cleanup-results.json'):
        check('bounded_retest', load(B / L / name)['status'] == 'pass', name)
    suites = [ET.parse(p).getroot() for p in (B / L / 'shared-test-reports').glob('TEST-*.xml')]
    check('bounded_retest', {k: sum(int(s.get(k, 0)) for s in suites) for k in ('tests', 'failures', 'errors', 'skipped')} == {'tests': 38, 'failures': 0, 'errors': 0, 'skipped': 0}, '38 shared tests')
    original = ET.parse(B / L / 'original-case-after.xml').getroot()
    check('bounded_retest', original.get('tests') == '1' and original.get('failures') == '0', 'original assertion')
    check('bounded_retest', ET.parse(B / L / 'before-regression.xml').getroot().get('failures') == '1', 'pre-fix failure retained')
    ios = load(B / L / 'ios-native-result.json')
    check('bounded_retest', (ios['passedTests'], ios['failedTests'], ios['skippedTests']) == (1, 0, 0), 'native iOS')
    for alias in load(B / L / 'capture-storage.json')['aliases']:
        p = B / L / alias['stored_path']
        check('capture_aliases', sha(p) == alias['sha256'] and p.stat().st_size == alias['bytes'], alias['logical_path'])

    scope = load(B / '10A2/scope-matrix.json')
    contracts = load(B / '10H3/state-contract-results.json')
    conditional = [r for r in contracts['contracts'] if r['status'] == 'conditional_future_scope']
    check('scope', len(conditional) == 4 and {r['id'] for r in conditional} == {r['id'] for r in scope['conditional_state_contracts']}, 'exact four conditional contracts')
    scope_rows = [{'id': r['id'], 'target': r['target'], 'dimension': r['dimension'], 'requirement': r['requirement'],
                   'basis': r['basis'], 'owner': r['owner'], 'frozen_scope_locator': '10A2/scope-matrix.json#/rows/' + str(i),
                   'execution_disposition': 'Excluded/unperformed, never passed' if r['requirement'].startswith('excluded') else 'See bounded 10L receipts and open full platform cases; preparation availability is not execution proof'} for i, r in enumerate(scope['rows'])]
    check('scope', len({r['id'] for r in scope_rows}) == len(scope_rows) == 54, '54 exact target scope rows')

    platform = load(B / '10K7/platform-matrix.json')
    frozen_runtime = load(B / '10A3/runtime-matrix.json')
    for key, expected in [('artwork_cases', 2920), ('normal_production_journeys', 132)]:
        rows = platform[key]
        frozen = frozen_runtime['artwork_contexts' if key == 'artwork_cases' else 'production_journeys']
        check('platform_cases', len(rows) == expected and {r['case_id'] for r in rows} == {r['case_id'] for r in frozen}, key)
    for row in platform['platforms']:
        check('platform_cases', sha(B / row['result']) == row['sha256'], row['task'])
    resources = list((B / L).glob('*-resources.json'))
    check('resources', len(resources) == 9, '8 normal/proof + installed iOS')
    for p in resources:
        data = load(p)
        check('resources', data['status'] == 'pass' and len(data['checks']) == 490 and all(x['pass'] for x in data['checks']), p.name)
    http = load(B / L / 'normal-http-parity.json')
    check('resources', http['status'] == 'pass' and http['files'] == 783 and all(x['pass'] for x in http['checks']), 'normal HTTP saved receipts')

    md_links = 0
    for m in sorted(B.rglob('*.md')):
        if OUT in m.parents or m == B / 'verification-report.md':
            continue
        for target in re.findall(r'\]\(([^)]+)\)', m.read_text()):
            if '://' not in target and not target.startswith('#'):
                check('historical_markdown_links', (m.parent / target.split('#')[0]).exists(), str(m) + ': ' + target)
                md_links += 1

    gate_reviews = dict(zip(['T%02d' % n for n in range(1, 11)], ['10B14', '10C3', '10D4', '10E18', '10F4', '10G3', '10H3', '10I3', '10J3', '10K7']))
    reasons = {
        'T01': 'Pass for unchanged accepted import/content inputs; compiled parity rerun in 10L. Does not certify every other gate.',
        'T02': 'Six source metadata findings, Volvo handbook currency disposition and remaining exact source/platform/failure cases.',
        'T03': 'Required native visible-selection and browser semantics failures, description dependencies and full visual/assistive matrix.',
        'T04': 'Three description findings in 30 question contexts. 970 scoped per-ID passes are not release acceptance.',
        'T05': 'Three injected identity-rejection counterexamples (one finding); complete exact normal-production journeys remain open.',
        'T06': 'Internal aliases/recovery checks pass in saved scope; exact remaining SIG16–18 target dispatch/failure/return cases remain open.',
        'T07': 'DEF-10H-001 closed by bounded retest; remaining full native state/focus/modal/relaunch matrix remains required.',
        'T08': 'Shared library/teaching/search/gap audits pass; remaining visible target, font/theme, interaction and assistive cases remain open.',
        'T09': 'Six fidelity findings, source classification and remaining exact-board/target/copy accessibility acceptance.',
        'T10': 'Required failures and full platform/cross-gate matrices remain open; bounded fresh builds/routes do not close them.',
    }
    clauses = []
    for clause in prepared['gate_clauses']:
        gate = clause['gate']
        owners = clause['owners']
        receipts = [r['artifact_manifest'] for r in task_rows if r['task'] in owners]
        check('clauses', len(receipts) == len(owners), clause['case_id'])
        clauses.append({'case_id': clause['case_id'], 'gate': gate, 'expected': clause['expected'], 'owners': owners,
                        'status': 'pass_unchanged_input_scope' if gate == 'T01' else 'open_final_candidate_acceptance',
                        'available_evidence': receipts, 'gate_review': reference(B / gate_reviews[gate] / 'review.md'),
                        'disposition': reasons[gate], 'current_candidate_impact': '10L3/' + ISSUE + '/evidence-invalidation-map.json',
                        'historical_clause_detail': ('10K7/platform-matrix.json#/T10_clauses/' + str(int(clause['case_id'][-2:]) - 1)) if gate == 'T10' else None})
    check('clauses', len(clauses) == 42 and len({x['case_id'] for x in clauses}) == 42, '42 unique clauses')
    gates = [{'gate': gate, 'status': 'pass_unchanged_input_scope' if gate == 'T01' else 'open', 'disposition': reason,
              'review': reference(B / gate_reviews[gate] / 'review.md'), 'clauses': [x['case_id'] for x in clauses if x['gate'] == gate]} for gate, reason in reasons.items()]
    task_rows += [{'task': '10M1', 'execution': 'report_assembled_and_audited', 'acceptance': 'blocked_incomplete', 'dependencies': prepared['task_dependencies']['10M1']},
                  {'task': '10M2', 'execution': 'not_run_not_authorized', 'acceptance': 'blocked_by_nonpassing_10M1', 'dependencies': ['10M1']}]
    index = {'schema_version': 1, 'task': '10M1', 'status': 'blocked_incomplete', 'step10_complete': False, 'entry': entry,
             'candidate': {'accepted_identity': fp['accepted_identity'], 'accepted_manifest_file_sha256': fp['accepted_manifest_file_sha256'],
                           'source_runtime_fingerprint': actual_fp, 'source_fingerprint_receipt': reference(B / ('10L2/' + ISSUE + '/candidate-fingerprint.json')),
                           'baseline_inputs_checked': len(baseline['tracked_input_fingerprints']), 'baseline_deviations': deviations,
                           'documentation_only_since_tested_fix': 'Entry HEAD contains the tested route/test changes and evidence/progress commits; current source hashes exactly match the 10L tested inputs.'},
             'tasks': task_rows, 'gate_clauses': clauses, 'gates': gates,
             'original_coverage_crosswalk': [{**r, 'prepared_status': r['status'], 'status': 'oracle_and_owners_audited',
                                              'acceptance': 'See owning task/gate dispositions; oracle accounting does not close a gate.'} for r in prepared['original_coverage_crosswalk']],
             'data_families': [{'family': f['id'], 'gate': f['gate'], 'owner': f['owner'], 'required_cases': len(f['members']),
                                'prepared_locator': '10A3/data-cases.json#/families/' + str(i),
                                'disposition': reasons[f['gate']]} for i, f in enumerate(data_cases)],
             'questions': question_rows, 'question_counts': dict(question_counts),
             'question_scope': 'All 1000 IDs/revisions/concepts/owners and accepted snapshots reconciled; exact referenced review pointers resolve. Content outcomes remain independent of full platform acceptance.',
             'platform_cases': {key: [{**row, 'current_candidate_acceptance': 'open', 'historical_locator': '10K7/platform-matrix.json#/' + key + '/' + str(i),
                                     'applicability': 'Historical 10K observation; bounded 10L replacements do not close this complete case.'} for i, row in enumerate(platform[key])] for key in ('artwork_cases', 'normal_production_journeys')},
             'historical_platform_counts': platform['counts'],
             'current_full_case_closures': {'artwork': 0, 'normal_production_journeys': 0},
             'defects': {'source': reference(B / L / 'defects.json'), 'open': ledger['open_product_defects'], 'closed': ledger['closed_product_defects'],
                         'records': [{'id': x['id'], 'severity': x['severity'], 'state': x['state'], 'locator': L + '/defects.json#/findings/' + str(i)} for i, x in enumerate(ledger['findings'])]},
             'approvals': {'source': reference(B / '10J1/design-comparison-index.json'), 'boards': 17, 'states': 38, 'new_design_approval': False, 'unresolved_exact_board_states': approvals['unresolved_exact_board_states']},
             'scope_rows': scope_rows, 'scope_requirement_counts': dict(Counter(r['requirement'] for r in scope_rows)),
             'conditional_contracts': conditional,
             'retained_evidence_policy': impact, 'limitations': limitations(),
             'reproduction': {'audit': 'python3 docs/curriculum/app-migration/verification-evidence/10M1/audit_report.py --check',
                              'meaning': 'Checks saved hashes, exact case/ID accounting, current protected inputs and deterministic report output. Does not rerun app/UI, legal sources or historical writers.',
                              'platform_commands': [reference(B / '10K7/toolchain.json'), reference(B / L / 'commands.json')],
                              'historical_baseline': '10A1 and 10K live old-fingerprint checkers are expected to reject the two declared source changes. Use the 10L invalidation map; never reseal old receipts.'},
             'audit': {'historical_manifests': len(manifests), 'historical_artifact_files': checks['historical_artifact_hashes'], 'historical_local_markdown_links': md_links,
                       'counts': dict(checks), 'new_platform_runs': 0, 'new_source_currency_checks': 0},
             'next': 'Another bounded 10L correction, affected verification and remaining required matrices; repeat 10M1 after blockers are cleared. 10M2 requires a passing 10M1.',
             'publication': False}
    return index


def limitations():
    return [
        {'kind': 'excluded_unperformed', 'scope': 'Physical iPhone signing/install/runtime/VoiceOver/legibility', 'basis': 'Existing iOS simulator policy; iosArm64 device build/resource verification remains required and has fresh bounded receipts.'},
        {'kind': 'conditional', 'scope': '7E-STATE-19 bookmarks, 20 completed_lessons, 21 question_history and 22 persistent_storage_schema', 'basis': 'No production persistence/history/import/hot replacement is implemented. Exact fields/dispositions remain in 10H3/state-contract-results.json and the evidence index.'},
        {'kind': 'required_open', 'scope': 'Android TalkBack traversal/listening and remaining target visual/modal/focus cases', 'basis': 'Shared semantics, simulator nodes and successful compiles do not prove speech or complete native accessibility.'},
        {'kind': 'scope_limit', 'scope': 'iOS simulator VoiceOver listening, desktop native installer/OS accessibility/browser bridge, browser screen-reader listening/cross-engine/cold-offline', 'basis': 'Configured shared desktop JAR/Compose harness, existing simulator exclusions and Wasm static-host policy; no invented delivery claims. Android offline observations do not establish browser cold-offline operation.'},
        {'kind': 'required_open', 'scope': 'Source currency and exact remaining source/platform/failure cases', 'basis': 'Volvo handbook inspection/disposition remains blocked; old publisher evidence dates are retained. URL dispatch and this report do not certify current law.'},
        {'kind': 'assessment_gap', 'scope': 'M01-L01, M10-L03 and M07-L04', 'basis': 'First two have zero primary/related questions; M07-L04 has zero primary and one related (situation-053). Three 9N briefs and 18 rubric criteria are future editorial proposals, not implemented/scored exercises or official thresholds.'},
        {'kind': 'editorial_limit', 'scope': 'LIMIT-9I5-UNIT-GRAMMAR', 'basis': 'Approved six option-unit drafts pass; retained 1 litres wording appears at four locations in three questions. No silent broader grammar repair.'},
        {'kind': 'required_open', 'scope': 'Six visual fidelity findings and uncompleted target/design comparisons', 'basis': 'Seventeen approved boards do not approve a future repair. New design proposals require imagegen and explicit user approval.'},
        {'kind': 'evidence_limit', 'scope': 'Historical 384 accepted / 616 held fixtures versus production 1000 accepted / zero held', 'basis': 'Historical render fixtures, model contracts, proof hosts and partial normal flows remain distinct. None closes the full normal runtime matrix.'},
    ]


def report(x):
    gate_table = '\n'.join('| ' + g['gate'] + ' | ' + g['status'] + ' | ' + g['disposition'] + ' [Evidence](' + g['review']['path'] + '). |' for g in x['gates'])
    finding_table = '\n'.join('| ' + r['id'] + ' | ' + r['severity'] + ' | ' + r['state'] + ' |' for r in x['defects']['records'])
    limits = '\n'.join('- **' + r['kind'] + ' — ' + r['scope'] + ':** ' + r['basis'] for r in x['limitations'])
    return f'''# 10M1 — verification report

**Blocked/incomplete. Step 10 remains open.** This report is assembled and its evidence accounting is audited; the 10M1 acceptance condition is not met. Eighteen required product findings and uncompleted platform/cross-gate cases prevent closure. Only T01 passes within its unchanged accepted-input scope. T02–T10 remain open. No 10M2 completion record or release acceptance is issued.

The candidate at entry commit `{x['entry']['entry_commit']}` has accepted content version `{x['candidate']['accepted_identity']['content_version']}`, declared manifest identity `{x['candidate']['accepted_identity']['manifest_sha256']}` and manifest file SHA `{x['candidate']['accepted_manifest_file_sha256']}`. These two manifest hashes have different roles. The tested source/runtime fingerprint is `{x['candidate']['source_runtime_fingerprint']}`. Live source hashes match the [10L corrected candidate](10L2/{ISSUE}/candidate-fingerprint.json); all {x['candidate']['baseline_inputs_checked']:,} baseline inputs were compared. Only the two declared source files and plan/progress documentation differ from the entry baseline. This fingerprint identifies source/resource inputs; executable hashes and normal/proof labels remain separate receipts.

The [complete evidence index](evidence-index.json) accounts for all 70 executable tasks: 68 prior task records, this incomplete 10M1 audit and unexecuted 10M2. It maps every one of the 42 T01–T10 clauses, all 36 original coverage families, all prepared data families, all 1,000 per-ID outcomes and all frozen platform cases. Each clause retains its original expected outcome and owning artifact manifests. An executed task or valid hash does not mean its gate passed.

| Gate | Current disposition | Evidence and remaining work |
|---|---|---|
{gate_table}

## Curriculum, questions, sources and artwork

[10B14](10B14/review.md) independently verified all 578 PDF pages, exact imported blocks, 1,123 canonical destinations, 400 official sign entries, 24 reference groups, four fonts and two licence texts. Two isolated generation runs matched production. The page-193 correction and hidden-answer/source/artwork bindings remain accounted for. [10I](10I3/review.md) verified 115 forward routes, 91 documents/1,316 body blocks, 50 deliberate reveals and 288 search/filter cases. These are scoped input/shared checks; full actual-target visual acceptance remains open.

[Per-ID content review](10E18/complete-question-review.json) reconciles 336 retained + 578 sign rewrites + 38 replacements + 8 scenarios + 30 load calculations + 4 exact-fuel calculations + 6 unit drafts = 1,000 IDs and 500 concepts. The 134 overlapping distractor changes are not extra questions. This audit resolves both original review pointers for every ID and verifies each accepted snapshot hash, revision and owner. **970 pass within the reviewed content scope; 30 retain description findings** (C18: eight contexts, M8: ten, X9: twelve). No wrong scored key was identified by that audit. This is not a 970-question release-ready claim. Accepted production remains 1,000 accepted/zero held.

[Source audit](10C3/review.md) records 404 exact URLs, 116 destinations, 519 compiled references and 8,166 question/option bindings. Six metadata classifications and the Volvo handbook currency disposition remain unresolved. Later dated scenario/source support does not silently refresh all legal review dates. This reporting task performs no new external-source inspection or legal-currency certification.

## Platform counts and applicability after the correction

The [frozen platform matrix](10K7/platform-matrix.json) contains **2,920 required artwork contexts and 132 exact normal production journeys**. All original case IDs reconcile with the prepared matrix; none is removed or turned into an exclusion. The historical 10K run observed 2,489/2,920 functional renderer contexts (2,464 shared plus 25 Android), leaving 431 without those completed observations. Android stopped at 25/152 replacement rows, leaving 127; the full iOS replacement matrix also remains uncompleted. Functional rendering did not close full visual/platform acceptance: **zero fully closed artwork cases and zero fully closed exact normal journeys**. The index retains every case and marks its current full acceptance open. These denominators overlap other gate case sets and must not be added as disjoint coverage.

10K's executables/runtime captures use the previous fingerprint `ac0d4e6b6b226b1f87f8d09521b4c334cccecd6cb7827c1bbd3889127402973c`. They are historical evidence after the route change. The [10L impact map](10L3/{ISSUE}/evidence-invalidation-map.json) preserves unchanged input/content/resource checks and supersedes only the bounded failed return case. It does not promote old target observations to final-candidate acceptance.

[Fresh bounded 10L receipts](10L3/{ISSUE}/review.md) include 38 passing shared tests, the unchanged original assertion, actual Android and iOS proof-host returns and both normal/proof browser returns. The pre-fix failure remains retained. Configured normal Android APK, desktop JAR, iOS simulator/shared app, device ARM64 framework and production Wasm builds succeed. Eight normal/proof packages each pass 490 saved resource checks; installed normal iOS adds another 490, and all 783 served normal web files match. Normal native apps and initial device/tab/server state were restored. These observations close **DEF-10H-001 only** and do not complete the full state/artwork/assistive/journey matrices.

## Approvals, findings and exact limitations

[Approval index](10J1/design-comparison-index.json) binds 17 approved boards and 38 state dispositions. All authority, board, review and 40 input hashes were checked. The 13 unresolved exact-board state dispositions and six fidelity findings remain explicit; existing approval is not a waiver for mismatched implementation. This task proposes no visual design and changes no product code/content/assets.

The [latest defect ledger](10L3/{ISSUE}/defects.json) retains all 19 IDs from 10K: 18 open and one fixed/retested. Individual affected IDs/files, severity, action scope, dependencies, original failures and closure evidence remain in that ledger and [triage](10L1/{ISSUE}/defect-triage.md).

| Finding | Severity | Current state |
|---|---|---|
{finding_table}

All 54 frozen target-scope dimensions are indexed individually: 37 required and 17 excluded by the existing policy, with their exact target, dimension, basis and owner. These scope dimensions overlap the executable case sets; the exclusions do not remove required failures. Four future-store contracts remain conditional rather than passed.

{limits}

## Audit and reproduction

This audit verifies **{x['audit']['historical_manifests']} historical artifact manifests / {x['audit']['historical_artifact_files']:,} file hashes**, accepted bound-file hashes, original oracle records, approval inputs, exact question/case coverage and {x['audit']['historical_local_markdown_links']} historical local Markdown links. All resolve. [Audit results](10M1/audit-results.json) record accounting counts. All successful integrity assertions describe truthful evidence accounting; product acceptance is still blocked. Historical receipts are not rewritten.

Rerun the report audit from repository root:

```sh
python3 docs/curriculum/app-migration/verification-evidence/10M1/audit_report.py --check
```

Without `--check`, the same script regenerates only this report, index and 10M1 audit results from saved evidence. Per-task reproduction/command files and script hashes are indexed for all 68 prior tasks; [toolchain](10K7/toolchain.json) and [latest commands](10L3/{ISSUE}/commands.json) retain exact environment/build/test details. Static command/script availability was checked; historical app/UI/source-check jobs were not rerun. They require their recorded platforms and permissions, isolated new output paths and normal/proof labels. The original 10A/10K live baseline checks correctly reject the two declared source changes; never reseal them or rerun historical writers to erase that distinction. Temporary build paths are execution provenance, not durable binary delivery promises.

The [10M1 artifact manifest](10M1/artifacts.json) seals this report/index and audit inputs. Subsequent changes require a new audited report; 10M2's separate final-candidate check has not run. Next work is bounded 10L corrections, affected retests and all remaining required matrices, followed by a repeated 10M1 audit. A passing 10M1 is required before 10M2 can record completion. No commit, push, merge, deployment or publication is performed by this request.
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    index = assemble()
    text = report(index)
    for target in re.findall(r'\]\(([^)]+)\)', text):
        p = B / target.split('#')[0]
        check('report_links', p.is_file() or p in (B / 'evidence-index.json', OUT / 'audit-results.json', OUT / 'artifacts.json'), target)
    results = {'task': '10M1', 'status': 'pass_report_accounting_product_acceptance_blocked', 'product_acceptance': 'blocked_incomplete',
               'step10_complete': False, 'checks': dict(checks), 'total_assertions': sum(checks.values()),
               'tasks': 70, 'prior_manifests': 68, 'clauses': 42, 'original_coverage_families': 36, 'question_outcomes': index['question_counts'],
               'open_product_findings': 18, 'closed_product_findings': 1, 'required_artwork_cases': 2920, 'required_normal_journeys': 132,
               'new_platform_runs': 0, 'new_source_currency_checks': 0}
    outputs = {B / 'evidence-index.json': dump(index), B / 'verification-report.md': text, OUT / 'audit-results.json': dump(results)}
    for p, contents in outputs.items():
        if args.check:
            check('deterministic_outputs', p.read_text() == contents, p.name)
        else:
            p.write_text(contents)
    if args.check:
        for row in load(OUT / 'artifacts.json')['files']:
            p = OUT / row['path']
            check('report_artifact_hashes', sha(p) == row['sha256'], p)
    else:
        files = [*outputs, OUT / 'entry.json', Path(__file__).resolve()]
        (OUT / 'artifacts.json').write_text(dump({'task': '10M1', 'scope': 'Report accounting, not product acceptance',
                                               'files': [{'path': os.path.relpath(p, OUT), 'sha256': sha(p)} for p in sorted(files)]}))
    print('10M1 report accounting PASS; product acceptance BLOCKED/INCOMPLETE; 18 findings, 9 gates and required matrices remain open.')


if __name__ == '__main__':
    main()
