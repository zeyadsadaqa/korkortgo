"""Read-only package checks; writes only 8O verification.json. No OCR/runtime audit."""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'docs/curriculum'
CHECKS = []

def read(path):
    return json.loads((ROOT / path).read_text())

def check(name, condition, evidence):
    CHECKS.append({'name': name, 'pass': bool(condition), 'evidence': evidence})

def hash_check(record, kind):
    p = ROOT / record['path']
    actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    check(kind, actual == record['sha256'], {'path': record['path'], 'expected': record['sha256'], 'actual': actual})

index_path = 'docs/curriculum/app-design/8n/package-index.json'
index = read(index_path)
fixtures = read('docs/curriculum/app-migration/preview-content.json')
canonical = read('docs/curriculum/app-migration/curriculum-map.json')
legacy = read('docs/curriculum/app-migration/link-and-progress-map.json')
registry = {x['id']: x for x in canonical['curriculum_nodes']}
hash_check(index['specification'], '8N specification unchanged')
for rec in index['inputs']:
    hash_check(rec, '8N dependency unchanged')
records = index['approved_preview_tasks']
check('Twelve approved task records', {x['step'] for x in records} == {'8' + c for c in 'BCDEFGHIJKLM'}, len(records))
check('Sixteen approved boards', sum(len(x['outputs']) for x in records) == 16, index['totals'])
bindings = {}
for task in records:
    step = task['step']
    for rec in [task['binding'], task['review']] + task['prompts'] + task['outputs']:
        hash_check(rec, step + ' approved artifact unchanged')
    b = read(task['binding']['path'])
    bindings[step] = b
    check(step + ' explicit approval identity', b['status'] == 'approved' and b['approval_record'] == task['approval'] and bool(task['approval']['user_statement']), task['approval'])
    check(step + ' executable owner', bool(task['implementation_owners']), task['implementation_owners'])
    if b.get('fixture_sha256'):
        hash_check({'path': b['fixture_path'], 'sha256': b['fixture_sha256']}, step + ' fixture bytes')
    for rec in b.get('input_bindings', []):
        hash_check(rec, step + ' route/input bytes')
    if b.get('source_sha256'):
        hash_check({'path': b['source_path'], 'sha256': b['source_sha256']}, step + ' production bytes')

library = fixtures['library']
check('8B canonical rows and totals', bindings['8B']['rows'] == [{'id': x['id'], 'title': x['title']} for x in library['children']] and bindings['8B']['learner_copy'] == library['learner_copy'], 'M03-L01–L04/M03-R; 10 modules/40 lessons')
check('All library lesson tags resolve', len(library['lesson_tags']) == 40 and all(x['lesson_id'] in registry for x in library['lesson_tags']), '40 canonical lessons')
safety = next(x for x in library['category_filters'] if x['category_id'] == 'SAFETY')
expected = [x['id'] for x in library['children'] if x['id'] in safety['lesson_ids']]
check('8C exact filtered result', bindings['8C']['filtered_state']['visible_lesson_ids'] == expected == ['M03-L02', 'M03-L03', 'M03-L04'], expected)
check('8C exact empty copy', bindings['8C']['empty_state']['message'] == library['learner_copy']['empty_search'], bindings['8C']['empty_state'])
check('Zero-primary lessons preserved', {x['lesson_id'] for x in library['zero_primary_question_lessons']} == {'M01-L01', 'M07-L04', 'M10-L03'}, 'No question-count exclusion')
reader = fixtures['lesson_reader']
check('8D goal/requirements exact', bindings['8D']['goal'] in reader['approved_markdown'] and bindings['8D']['requirements_opening'] in reader['approved_markdown'], reader['content_id'])
check('8D previous/next exact', bindings['8D']['navigation']['previous']['id'] == reader['previous_id'] and bindings['8D']['navigation']['next']['id'] == reader['next_id'], [reader['previous_id'], reader['next_id']])
check('8E exact check and reveal', bindings['8E']['question'] in reader['approved_markdown'] and bindings['8E']['answer'] in reader['approved_markdown'] and bindings['8E']['states']['collapsed']['answer_in_accessibility_tree'] is False, 'Question visible; hidden answer excluded until reveal')
source_text = (ROOT / bindings['8F']['source_path']).read_text()
check('8F complete context retained', all(x in source_text for x in bindings['8F']['approved_context_blocks'].values()), list(bindings['8F']['approved_context_blocks']))
check('8F arithmetic', Decimal(7)*1*3 + Decimal(7)**2*Decimal('0.4') == Decimal('40.6'), '21 + 19.6 = 40.6 m')
for step, fixture in zip(['8G', '8H'], fixtures['answer_reviews']):
    b = bindings[step]
    check(step + ' full exact question fixture', b['fixture'] == fixture, fixture['question_id'])
    order = fixture['display_option_order']
    display = [{'letter': chr(65+i), 'original_index': n, **fixture['question']['options'][n]} for i, n in enumerate(order)]
    check(step + ' selected A/key B and explanations', b['display_options'] == display and order[0] == fixture['selected_original_option'] and order[1] == fixture['question']['correct'], order)
    check(step + ' related/source routes', fixture['primary_lesson']['id'] in registry and b['source_reference_ids'] == fixture['source_references'], fixture['source_references'])
check('8H exact unrounded arithmetic', Decimal('150')*Decimal('0.5')/100 == Decimal('0.75'), '0.75 litres')
check('8H proposed scoring status retained', 'not live or accepted for scoring' in bindings['8H']['fixture']['status'] and bindings['8H']['historical_compatibility']['conditional_only'], bindings['8H']['content_status'])
check('8I three exact source fixtures', bindings['8I']['source_fixtures'] == fixtures['sources'], [x['id'] for x in fixtures['sources']])
commercial = next(x for x in fixtures['sources'] if x['id'] == bindings['8I']['detail_source_id'])
check('8I external URL exact', bindings['8I']['external_detail_url'] == commercial['url'], commercial['url'])
check('8I valid source return parent', bindings['8I']['origin']['content_id'] in registry and len(bindings['8I']['return_contract']) >= 4, bindings['8I']['origin'])
check('8J exact caption/asset/source fixture', bindings['8J']['fixture'] == fixtures['sign_reference'], 'sign-B1/CAP-B1')
hash_check(fixtures['sign_reference']['entry']['asset'], 'B1 official bytes')
check('8J delivery holds remain open', bindings['8J']['faint_outline_holds']['count'] == 38 and not bindings['8J']['faint_outline_holds']['cleared'], 'No hold waived by preview approval')
alias = next(x for x in legacy['legacy_page_aliases'] if x['legacy_page'] == 46)
check('8K exact alias/choice order', bindings['8K']['legacy_alias'] == alias and bindings['8K']['chooser_choices'] == [{'id': i, 'title': registry[i]['title']} for i in alias['target_ids']], alias['target_ids'])
for case, target in [('same-old-page-a', 'M04-L03'), ('same-old-page-b', 'M04-L01')]:
    actual = next(x for x in bindings['8K']['exact_examples'] if x['id'] == case)
    check('8K ' + case, actual['after']['content_id'] == target, actual)
check('8K moved notice exact', bindings['8K']['auxiliary_copy']['moved_passage_notice'] == fixtures['auxiliary_copy']['moved_passage_notice'], 'Known parent only; no invented offset')
check('8L exact signals and no substitutions', bindings['8L']['signal_cases'] == fixtures['signal_unavailable_cases'] and all(x['target_id'] is None and x['related_target_ids'] == ['M03-L02'] for x in bindings['8L']['signal_cases']), 'SIG16–18 distinct exact URLs')
check('8L generic copy exact', bindings['8L']['exact_copy'] == {k: fixtures['auxiliary_copy'][k] for k in ['unavailable_title', 'library_action']}, bindings['8L']['exact_copy'])
check('8M recovery exact', bindings['8M']['exact_copy'] == {'message': fixtures['auxiliary_copy']['missing_result'], 'action': fixtures['auxiliary_copy']['setup_action']}, bindings['8M']['exact_copy'])
check('8M setup/result/review contracts retained', bindings['8M']['routes'] == [x for x in legacy['navigation_routes'] if x['legacy'] in ['Page.SETUP', 'Page.RESULTS', 'Page.REVIEW']], 'No fabricated session or auto-start')
# Guard stored planning/source/app/asset inputs independently of the design index.
prior = read('docs/curriculum/app-migration/verification.json')
for rec in prior['input_manifest']:
    hash_check(rec, '7G protected input unchanged')
# Scan actual learner fixture text, not audit prose/negative prompt instructions or source provenance.
learner = [x['title'] for x in registry.values()]
learner += [bindings['8D']['goal'], bindings['8D']['requirements_opening'], bindings['8E']['question'], bindings['8E']['answer']]
for task in ['8G', '8H']:
    q = bindings[task]['fixture']['question']
    learner += [q['prompt'], q['explanation']] + [x['text'] for x in q['options']] + [x['explanation'] for x in q['options']]
learner += list(fixtures['auxiliary_copy'].values()) + [x['learner_message'] for x in fixtures['signal_unavailable_cases']]
bad = [s for s in learner if re.search(r'Theory Book 2026|\bSTR\b|Book pages?\s*\d|Theory Book.*pages?', s, re.I)]
check('Learner fixture legacy-name/folio exclusion', not bad, {'scanned_strings': len(learner), 'findings': bad, 'limits': 'Targeted textual fixture check; not raster OCR or full imported-app validation.'})
check('Legitimate source publishers preserved', bindings['8I']['source_fixtures'] == fixtures['sources'], 'Do not erase provenance during legacy-label replacement')
for p in [BASE/'app-design-spec.md'] + [ROOT/x['review']['path'] for x in records]:
    for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
        if '://' not in link:
            check('Local reference resolves', (p.parent/link.split('#')[0]).exists(), {'document': str(p.relative_to(ROOT)), 'link': link})
report = {'step': '8O', 'verified_on': '2026-10-15', 'technical_result': 'PASS' if all(x['pass'] for x in CHECKS) else 'FAIL', 'status': 'awaiting_final_package_approval', 'scope': 'Stored artifact/fixture/route/copy verification. No OCR, source-currency, runtime, device or implementation claims.', 'package_index': {'path': index_path, 'sha256': hashlib.sha256((ROOT/index_path).read_bytes()).hexdigest()}, 'checks': CHECKS, 'totals': {'checks': len(CHECKS), 'passed': sum(x['pass'] for x in CHECKS), 'failed': sum(not x['pass'] for x in CHECKS), 'approved_tasks': len(records), 'approved_boards': 16}, 'complete_package_approval': None, 'implementation_started': False, 'visual_disposition': 'Retain individually approved chip/icon variants per state; no harmonised redesign selected. See app-design-review.md; subject to final package approval.', 'remaining_implementation_holds': ['38 image-delivery holds', 'proposed question acceptance', 'source-currency checks', 'actual platform/accessibility/reflow/asset proof']}
output = BASE/'app-design/8o/verification.json'
output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report['totals']))
raise SystemExit(0 if report['technical_result'] == 'PASS' else 1)
