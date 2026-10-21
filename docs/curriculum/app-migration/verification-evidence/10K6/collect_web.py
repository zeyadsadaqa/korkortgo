"""Reconcile saved browser observations; does not automate or modify the UI."""
import hashlib
import json
import socket
from pathlib import Path

OUT = Path(__file__).parent
E = OUT / 'browser-evidence'
load = lambda p: json.loads(p.read_text())
write = lambda name, value: (OUT / name).write_text(json.dumps(value, indent=2) + '\n')
normal = load(OUT / 'normal-distribution.json')
restored = load(OUT / 'restore-normal-distribution.json')
original_hashes = {x['path']: x['sha256'] for x in normal['files']}
restored_hashes = {x['path']: x['sha256'] for x in restored['files']}
unchanged = original_hashes == restored_hashes
ports = []
for port in (60160, 60621, 61047):
    with socket.socket() as connection:
        connection.settimeout(.3)
        ports.append({'port': port, 'stopped': connection.connect_ex(('127.0.0.1', port)) != 0})
assert all(x['stopped'] for x in ports)
write('runtime-restored.json', {
    'status': 'pass' if unchanged else 'rebuilt_normal_distribution_differs_requires_retest',
    'normal_vs_restored_distribution_identical': unchanged,
    'normal_files': len(original_hashes), 'restored_files': len(restored_hashes),
    'proof_flag_after_restoration': False, 'temporary_servers': ports,
    'tabs': load(E / 'tab-cleanup.json'),
    'interruption': 'Original server and transient assessment tab ended across interrupted turn; restarted normal origin60621. Never promote interrupted deferred sample to a completed journey.'})
pending = load(E / 'pending-choice-dom.json')
assert pending['checked'] is None and pending['selected'] is None and pending['pressed'] is None
assert 'Your answer' in (E / 'immediate-confirmed.txt').read_text()
assert 'Correct answer' in (E / 'immediate-expanded-review.txt').read_text()
assert '0 / 1' in (E / 'deferred-results.txt').read_text()
deferred = (E / 'deferred-confirmed-no-feedback.txt').read_text()
assert 'Answer saved.' in deferred and 'Correct answer' not in deferred
finding = {
    'id': 'DEF-10K-001', 'severity': 'P2', 'status': 'open',
    'title': 'Wasm selected assessment choice lacks exposed browser selection state',
    'target': 'normal production Wasm; IAB; sampled sign-recognise-M7/rewrite-r2',
    'expected': 'The selected pending choice exposes a programmatic selected/checked state before confirmation, including after modal and leave-guard return.',
    'actual': 'Known wrong A is functionally retained and becomes Your answer/Incorrect with score0/1, but its pending DOM role is button and aria-checked/aria-selected/aria-pressed are absent. Pending AX does not announce selection.',
    'reproduction': ['Start one-question immediate production test', 'Select A on sign-recognise-M7', 'Cancel leave guard; enlarge/close option A', 'Inspect pending choice browser DOM/AX', 'Confirm; compare Your answer A and correct D'],
    'affected_ids': ['sign-recognise-M7/rewrite-r2 (observed sample)'],
    'affected_surface': 'Assessment choice semantics at the browser accessibility bridge; root cause and wider affected set require10L1 triage.',
    'gate_dependencies': ['T03', 'T05', 'T07', 'T10'],
    'evidence': ['browser-evidence/pending-choice-dom.json', 'browser-evidence/immediate-pending-after-viewer.txt', 'browser-evidence/immediate-pending-after-viewer.png', 'browser-evidence/immediate-confirmed.txt', 'browser-evidence/immediate-results.txt'],
    'distinction': 'Android exposes checked/Selected but lacks persistent visible styling (DEF-10D-001). This finding concerns absent browser programmatic state, not spoken screen-reader listening.',
    'acceptance_check': 'Repeat pending selection/guard/viewer return on normal Wasm; selected state is exposed and matches the subsequently confirmed answer. Retest dependent required cases.'}
write('defects.json', {'task': '10K6', 'new_product_findings': [finding], 'repairs_performed': False})
signal_tabs = load(E / 'signal-callback-tabs.json')
signals = []
for code, tab in zip(('SIG16', 'SIG17', 'SIG18'), signal_tabs):
    assert tab['url'].startswith('https://www.transportstyrelsen.se/')
    assert 'Content unavailable' in (E / f'proof-{code}-unavailable.txt').read_text()
    signals.append({'code': code, 'observed_url': tab['url'], 'tab_title': tab['title'],
                    'status': 'exact_callback_destination_observed',
                    'recovery': 'related M03-L02 teaching' if code == 'SIG16' else 'learning library',
                    'scope': 'labelled proof route; online destination; no controlled external failure or source currency re-audit'})
write('web-results.json', {
    'task': '10K6', 'status': 'executed_required_browser_selection_failure_and_remaining_matrix_open',
    'scope': 'Production Wasm copied distribution; fresh origins60160 and60621, Cache-Control:no-store; IAB canvas DOM/AX and visible screenshots; no user account or publication.',
    'builds': ['normal-distribution.json', 'proof-distribution.json', 'restore-normal-distribution.json'],
    'resource_checks_per_build': 490, 'http_files_verified': load(OUT / 'http-parity.json')['served_files'],
    'http_receipts': ['initial-http-parity.json', 'http-parity.json'],
    'production_bank': 'Accepted1000/zeroheld; no candidate fixture used for scored browser samples',
    'normal_observations': [
        {'mode': 'IMMEDIATE', 'question_id': 'sign-recognise-M7', 'revision': 'rewrite-r2', 'selected': 'A', 'correct': 'D', 'score': '0/1',
         'scope': 'guard cancellation; neutral viewer/zoom/Home/reset/Escape; feedback; expanded Incorrect review; M03-L02 deliberate reveal/hide; source detail and internal return; expanded review and count1 retained',
         'receipt_prefix': 'browser-evidence/immediate-', 'external_destination_followup': 'browser-evidence/callback-followup.json'},
        {'mode': 'AT_END', 'question_id': 'sign-meaning-M8', 'revision': 'rewrite-r2', 'selected': 'A World Heritage site', 'correct': 'D Continuous line', 'score': '0/1',
         'scope': 'Answer saved without correctness; finish; expanded Incorrect review; exact Heldragen linje callback; related M03-L02; expanded review and count1 retained',
         'receipt_prefix': 'browser-evidence/deferred-', 'external_callback': 'browser-evidence/review-source-callback.json'},
        *load(E / 'continued-observations.json')],
    'signal_callbacks': signals,
    'proof_recovery': {'unknown_question': 'Unavailable then explicit library recovery; no guessed lesson',
                       'legacy_chooser': 'Not completed: verification-only hash parser does not decode The%20foundations. Saved unavailable result; not a production route defect or chooser pass.'},
    'settings': 'Fixed production light/default font; first screenshots481x724, continuation1280x720. Actual PNG sizes retained; no imposed viewport/theme/font matrix.',
    'full_normal_journeys_completed': [],
    'new_product_findings': [finding], 'restoration': 'runtime-restored.json',
    'limitations': ['New required browser selection semantics failure; inherited visual selection failure remains',
                    'Required artwork/platform/font/theme/focus/assistive matrix is not completed; sampled flows do not close132 normal journeys',
                    'Actual source callbacks observed; controlled unreachable/false-handler browser case not run; no external failure-handling pass',
                    'No cold-offline, cross-engine, screen-reader listening or physical-device claim',
                    'Callback destinations verify dispatch only; do not refresh or certify all legal/source currency'],
    'publication': False})
print('Web evidence reconciled; required acceptance remains open; normal restored identical:', unchanged)
