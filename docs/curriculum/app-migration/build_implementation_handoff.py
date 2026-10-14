"""Build the 7F planning handoff. Never writes app, questions, assets or PDF files."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
APP = 'composeApp/src/commonMain/kotlin/se/korkort/'
RES = 'composeApp/src/commonMain/composeResources/files/'

def read(name):
    return json.loads((OUT / name).read_text())

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

c = read('curriculum-map.json')
a = read('question-actions.json')
l = read('link-and-progress-map.json')
q = read('question-map.json')
b = read('baseline.json')
items = []
def item(id, title, deps, files, output, acceptance):
    items.append(dict(id=id, title=title, dependencies=deps.split(), affected_files=files,
                      output=output, acceptance=acceptance))

item('9A', 'Freeze the accepted input package and import schema', '',
 ['tools/build_content.py', 'content/curriculum.json (new)', 'content/content-manifest.json (new)', APP+'Quiz.kt', APP+'Curriculum.kt (new)'],
 'A typed content contract and deterministic import boundary using 7B fields, stable option IDs, semantic question revisions and asset/source bindings. Freeze all 7A–7F identities before any live generation.',
 ['Fail on changed approved PDF/manuscript/registry, question or asset hashes until the affected audit is refreshed.',
  'Separate curriculum release from app package version; bind teaching, accepted questions, sources, assets and aliases by manifest digest. PDF hash alone is insufficient.',
  'Represent block types, hidden/revealed answer blocks, canonical IDs, source scopes, eligibility and pre-/post-answer image semantics. Keep compile-time Kotlin delivery unless a separately reviewed loader change is needed.',
  'Generator writes deterministically to explicit outputs, fails duplicate/unknown IDs and emits source-to-output traceability. No runtime JSON loader is assumed.'])
item('9B', 'Import the complete approved teaching and references', '9A',
 ['tools/build_content.py', 'content/curriculum.json (new)', APP+'Curriculum.kt (new)', APP+'Chapters.kt'],
 'Full independently written curriculum, not old summaries: ten module introductions, forty lessons, ten reviews, four appendices and twenty-four reference groups; preserve all 519 supporting anchors and registry targets.',
 ['Read each 7B source_location and final chapter/reference production corrections, including the page-193 wildlife reference; preserve exact approved titles/order.',
  'Preserve tables, examples, assumptions, knowledge checks, answer blocks and source/illustration placements. Every imported block has an origin locator; compare normalized content to approved production sources.',
  'Resolve all 1,123 published IDs (88 curriculum, 400 signs, 116 sources, 519 supporting anchors); supporting/front-matter anchors need not become top-level library cards.',
  'Keep legacy aliases separately; remove the 39 old summary payloads and unused 178 Topic summaries from learner content without importing court-case narratives.'])
item('9C', 'Import scoped sources, sign captions and exact verified assets', '9A',
 ['tools/build_content.py', 'content/curriculum.json (new)', 'content/sources.json (new)', RES+'curriculum/ (new)', APP+'Curriculum.kt (new)'],
 'Sources and assets with exact paths/hashes, code/variant/caption bindings, credits and editorial-English notices. Register 404 question URL records alongside 116 canonical source destinations, retaining module-specific URL choices.',
 ['Copy the approved 400 sign bindings and all lesson illustrations with manifest hashes and reuse records; verify bundled-byte parity and all block references.',
  'Derive source title/publisher/classification/check date/scope from retained evidence, not domain guesses or a blanket official label. Preserve commercial, foreign, research, manufacturer and editorial limits.',
  'Use exact 7C source_reference_ids to find URL records and canonical source_ids for navigation. Retain per-source dates; unknown date is explicit, never invented.',
  'Verify F31a case and exact sign variants. Study alt text may explain meaning; do not reuse it as assessment alt text. No sign artwork redrawing or PDF changes.'])
item('9D', 'Add assessment identities, neutral descriptions and reveal semantics', '9A 9C',
 ['tools/build_content.py', 'content/questions.json', APP+'Quiz.kt', APP+'App.kt', APP+'Bank.kt'],
 'Author and review physical descriptions for every image in all 616 sign questions; stable authored option identity replaces code-bearing label uniqueness. Derive display letters after shuffling.',
 ['All sign stems/options use the 7D exact-code proposal and caption/source; remove matching-code cues before answering. Keep code/meaning in metadata and revealed feedback.',
  'Review every physical description against the visible image, without naming the correct meaning or including a target/option code. Cover keyboard, focus and assistive-technology reading order and equivalent access.',
  'Assert unique option identity and distinct asset choices, not unique code text. Audit 134 distractor-set changes in both paired directions.',
  'Check shuffle/key/option-feedback association for all four positions and both feedback modes; hidden feedback and study captions must not leak through accessibility semantics.'])
item('9E', 'Apply the 578 sign rewrites', '9D',
 ['content/questions.json', 'tools/build_content.py', APP+'Bank.kt'],
 'Apply the assigned 578 non-held sign rewrites using the exact 7D per-question proposal, sources and reviewed descriptions; preserve question/concept IDs.',
 ['Work in deterministic batches of at most 50 IDs from the assignment manifest; record before/after diff and acceptance evidence for each ID.',
  'Check all four choices and explanations against exact captions, including C6, E3, S7 and T24 when present; no substitution based on similar code or shape.',
  'New semantic revisions and acceptance flags are required. The 38 held replacements belong to 9F, not this batch.'])
item('9F', 'Resolve 38 faint-outline delivery holds', '9D',
 ['content/questions.json', RES+'curriculum/ (new)', 'content/content-manifest.json (new)', APP+'App.kt', 'docs/curriculum/app-migration/implementation-evidence/ (new)'],
 'Nineteen exact codes, two question directions each, with reviewed intended-size delivery, zoom/accessibility and asset evidence. This task also enforces proof for any retained faint image elsewhere in an option set.',
 ['Process the exact 38 assigned IDs and their 7D research_holds. Original 105 dp options / 180 dp stems are baseline constraints, not approved final sizes.',
  'Use an exact legible official rendition or approved framing with unchanged geometry; never silently thicken, recolour, redraw or use a generated substitute. Record source/hash and pair consistency.',
  'Prove actual display and accessible equivalent on each supported target, light/dark surfaces and text scaling; include smallest approved image size and zoom return behaviour.',
  'Until proof passes, item is ineligible for scored use. If proof fails, return an explicit alternative-item/ID decision; do not silently drop an item or weaken quotas to ship.'])
item('9G', 'Apply the eight scenario corrections', '9A',
 ['content/questions.json', 'tools/build_content.py', APP+'Bank.kt'],
 'Apply the exact 7D draft patches for situations 032, 045, 105, 107, 125, 162, 172 and 178.',
 ['Review every changed option explanation as well as stem/key: weekday times, car lighting scope, conditional rural return, emergency braking, prompt notification, ready weight, inspection bans and personal-injury cover.',
  'Compare each full resulting question to question-actions.json; preserve cited limits and IDs/concepts and assign new semantic revisions.',
  'Recheck time-sensitive rules at implementation against primary sources; record dates/evidence if guidance changed and refresh affected decisions before acceptance.'])
item('9H', 'Apply the thirty load definitions', '9A',
 ['content/questions.json', 'tools/build_content.py', APP+'Bank.kt'],
 'Apply all 30 driver-inclusive ready-weight prompt drafts; retain the existing numeric answers.',
 ['Define Swedish tjänstevikt consistently and avoid a driver-excluding interpretation of unladen.',
  'Recalculate displayed inputs and all four numeric options independently; assert original numeric keys unchanged and each revised prompt has one answer.'])
item('9I', 'Apply four exact fuel tasks and six unit fixes', '9A',
 ['content/questions.json', 'tools/build_content.py', APP+'Bank.kt'],
 'Apply the four exact-result draft questions and six 1-litre grammar drafts from 7D.',
 ['Independently recompute Decimal keys 0.75, 2.25, 1.25 and 3.75 litres for the four midpoint questions; verify distinct false alternatives and every explanation.',
  'Prompts explicitly request no rounding; preserve hypothetical measured-rate assumptions. Six grammar-only fixes keep numeric keys.',
  'Preserve IDs/concepts; old attempts retain old values/snapshots and scores. Never regrade an earlier rounded answer against a new key.'])
item('9J', 'Assemble accepted questions and verify selection capacity', '9E 9F 9G 9H 9I',
 ['content/questions.json', 'content/content-manifest.json (new)', 'tools/build_content.py', APP+'Bank.kt', APP+'Quiz.kt'],
 'Versioned active question package: 336 retained assessments plus 626 reviewed rewrites and 38 proven replacements. Exact 7C relationships for every baseline ID; zero removals by default.',
 ['Use the machine-readable assignments as an exhaustive partition of 1,000 baseline IDs / 500 concepts; retained assessment fields stay unchanged except relationships/package metadata.',
  'Active questions must all have completed acceptance; no unreviewed fallback items. Derive visible counts from accepted package, not the old advertised 1,000.',
  'Preserve five category IDs/labels, 7/5/16/32/5 plus five random at 70, existing largest-remainder allocation for 1–70 and concept uniqueness. Verify per-category capacity and random residual after quota picks for every length.',
  'Check deterministic generation JSON/Kotlin parity, no missing links or duplicate option identities; selection/shuffle across fixed seeds exercises all key positions. Insufficient accepted capacity is a release blocker.'])
item('9K', 'Implement typed routes, aliases and explicit signal fallback', '9B 9C',
 [APP+'App.kt', APP+'Curriculum.kt (new)', 'content/legacy-aliases.json (new)', 'tools/build_content.py'],
 'One validated internal resolver and transition guard covering every 7E route/alias. SIG16–18 keep the explicit unavailable-exact-entry policy; no new approved sign IDs.',
 ['Cover all 1,000 question routes, 39 chapter aliases, 361 integers including 38 gaps, 178 topic identities and 343 sign records using frozen namespace '+l['legacy_namespace']['id']+'.',
  'Question identity beats page. Known single aliases open exact content; multi-target aliases show canonical choices. Unknown question/namespace/title/page never guesses nearest/first content.',
  'SIG16, SIG17 and SIG18 have no exact internal destination: show recorded 7E message, recorded official URL action and optional M03-L02 related teaching. Keep them separate from the 340 exact-code entries. External link failure leaves a usable unavailable/library state.',
  'Known removed-block parent gets moved-passage notice; retired one/many/none use reviewed replacement offer/chooser/unavailable. Production tombstones stay empty.',
  'All eight navigation states and twelve entry-point rules use the same unfinished-quiz guard and valid return context. No public deep-link parser or new platform URL scheme.'])
item('9L', 'Implement approved library, reader, reference and sources views', '9B 9C 9J 9K',
 [APP+'App.kt', APP+'Chapters.kt', APP+'Curriculum.kt (new)'],
 'Step 8 approved presentation of canonical library, complete lesson reader, answer/review reveal, sign/reference detail and dedicated sources area.',
 ['Implement only after explicit approval of step 8 imagegen previews; use preview-handoff.md exact fixtures and record approval/version. Revisions to design require another approval.',
  'Display ten modules/four lessons each/reviews; five category filters use all forty 7E lesson tags, retaining canonical order and all zero-question lessons. Search uses canonical content.',
  'Previous/next follows all 60 reading nodes; sources/signs/appendices return to validated origin; hide answers until deliberate reveal.',
  'Apply all fourteen 7E learner-label replacements, actual accepted counts, exact source attribution and official-art/editorial-English notices. No old book titles, chapter labels or source folios in learner views.',
  'Handle empty search, unavailable content, multi-target chooser, long content, tables, zoom, keyboard focus and large text without losing approved meaning.'])
item('9M', 'Preserve quiz sessions and versioned transient state', '9A 9J 9K',
 [APP+'Quiz.kt', APP+'App.kt'],
 'Implement all 22 state contracts without adding a database or inventing a saved-data migration.',
 ['Preserve immediate/end feedback, answers, score, index and review filters with exact shuffled option identity and package revision. Keep quit confirmation for every outbound target.',
  'Default compile-time upgrade/restart clears transient remember/session state as before. Missing results/review context shows no saved result and a setup action.',
  'Do not add hot replacement. If separately chosen later, pin the full old session/option order/keys/feedback/package through finish/quit/review and switch atomically at safe idle.',
  'No durable bookmarks, completion or answer history currently exists. Future-store compatibility follows 7E: no automatic completion credit, no same-ID regrade, no reinterpretation of unversioned shuffled indices. Treat it as separate authorized scope.'])
item('9N', 'Close assessment coverage briefs without changing the baseline bank', '9B',
 ['docs/curriculum/app-migration/assessment-coverage-briefs.md (new)'],
 'Reviewable additional-assessment briefs for M01-L01, M07-L04 and M10-L03; keep the baseline bank at 1,000 and preserve all teaching.',
 ['M01-L01: preparation/entitlement/training checklist, recheck current official requirements before authoring; zero primary and zero related questions today.',
  'M07-L04: combined-risk decision to adapt/stop/change route; zero primary and one related question today.',
  'M10-L03: whole-journey explanation/reflection with a rationale/rubric; consider the approved existing practice/reflection format rather than forcing an MCQ; zero primary and zero related questions.',
  'State objective, source, proposed format, plausible mistakes and acceptance rubric for each brief. Additional scored items/new IDs require a separate explicit content decision and updated counts/coverage; do not replace unrelated baseline IDs.'])
item('9O', 'Integrate platform packaging, provenance and release evidence', '9J 9L 9M 9N',
 ['README.md', 'tools/build_content.py', 'composeApp/build.gradle.kts', 'composeApp/src/commonTest/kotlin/se/korkort/ (tests)', 'docs/curriculum/app-migration/implementation-evidence/ (new)', 'content/content-manifest.json (new)'],
 'A reviewable release candidate, accurate learner feature claims and step 10 evidence inventory.',
 ['Replace README stale 37-chapter/supplied-book feature claims using accepted manifest; retain technical provenance/audit history and required artwork/source credits.',
  'Run meaningful common tests and build/resource checks for Android, desktop, iOS device/simulator and wasm targets configured in composeApp/build.gradle.kts; record exact commands and unavailable tooling honestly.',
  'Verify packaged files/hashes and offline teaching/assets; official URLs remain external. Do not add persistence, remote loader, analytics, URL schemes or new platforms.',
  'Record unresolved device/platform checks as release blockers, not successful checks. Step 10 runs the matrix below; step 9 completion alone does not certify the app.'])

# Exhaustive bounded question assignment, with no inferred ID ranges.
def assign(x):
    if x['disposition'] == 'retain': return '9J'
    if x['disposition'] == 'replace': return '9F'
    issues = set(x['issues'])
    for issue, task in [('SIGN-QUESTION-COPY','9E'), ('SCENARIO-SCOPE-OR-EXPLANATION','9G'), ('LOAD-WEIGHT-CONVENTION','9H'), ('FUEL-ROUNDING','9I'), ('FUEL-UNIT-GRAMMAR','9I')]:
        if issue in issues: return task
    raise ValueError(x['question_id'])
assignments = [dict(question_id=x['question_id'], disposition=x['disposition'], work_item_id=assign(x),
                    acceptance_pointer=f'question-actions.json#/questions/{i}',
                    link_pointer=f'question-map.json#/questions/{i}') for i,x in enumerate(a['questions'])]
coverage = {}
for key, task in [('curriculum_nodes','9B'),('source_destinations','9C'),('sign_entries','9C'),('supporting_destinations','9B')]:
    coverage['7B/'+key] = dict(work_item_ids=[task], record_ids=[x['id'] for x in c[key]])
for key, tasks in [('category_routes',['9J','9L']),('lesson_category_tags',['9L']),('navigation_routes',['9K','9M']),('reading_order',['9L']),('chapter_aliases',['9K']),('legacy_page_aliases',['9K']),('question_routes',['9J','9K']),('unused_topic_routes',['9B','9K']),('sign_routes',['9C','9K']),('source_routes',['9C']),('state_rules',['9M']),('entry_point_rules',['9K','9M']),('labels_to_replace',['9L']),('supporting_document_updates',['9B','9O']),('resolution_policy',['9K']),('version_transition',['9A','9M']),('unresolved_destinations',['9K'])]:
    value=l[key]; coverage['7E/'+key]=dict(work_item_ids=tasks, record_count=len(value) if isinstance(value,list) else 1, input_pointer='link-and-progress-map.json#/'+key)
for issue,count in a['issue_counts'].items():
    owners = sorted({assign(x) for x in a['questions'] if issue in x['issues']})
    coverage['7D/'+issue] = dict(work_item_ids=sorted(set(owners + (['9D'] if issue.startswith('SIGN-') else []))), record_count=count)
for dep in a['shared_implementation_dependencies']:
    coverage['7D/'+dep['id']] = dict(work_item_ids=['9D'] if 'IMG' in dep['id'] else ['9C','9J','9K'] if 'SOURCE' in dep['id'] else ['9D','9J','9M'])
for x in a['coverage_backlog']:
    coverage['7D/coverage/'+x['lesson_id']] = dict(work_item_ids=['9N'], brief=x)

matrix = [
 ('T01','9A 9B 9C','Manifest/import parity','Compare complete imported blocks with production-source origins; all 1,123 IDs unique/resolving, 400 exact signs, all illustrations/tables/answer blocks, correct titles/order and approved page-193 correction. Verify deterministic generated Kotlin and packaged hashes.'),
 ('T02','9C 9K 9L','Scoped sources and references','Exercise official law, foreign guidance, research, commercial shortcut, manufacturer and editorial arithmetic. Compare all exact question source-reference URLs and scoped canonical aliases to retained evidence; actual publisher/date/limits, valid return context, offline/unreachable external URL behaviour.'),
 ('T03','9D 9E 9F','Assessment visuals and accessibility','Inspect every revised sign asset/variant/physical description, all 134 distractor changes and 38 holds. Test smallest approved size, zoom, light/dark, keyboard/screen reader and large text on supported platforms; no code/answer leak pre-answer, no generated replacement artwork.'),
 ('T04','9G 9H 9I 9J','Question content and calculations','Diff all 1,000 assigned IDs, assert 336 assessment payloads unchanged, review all 626 rewrites/38 replacements against per-ID acceptance; independent numeric audit including four exact keys, 30 driver-inclusive definitions, six grammar fixes and eight scoped scenarios. No unaccepted active item.'),
 ('T05','9D 9J 9M','Quiz engine and answer identity','Check every length 1–70, category quotas/rounding, concept capacity after quota picks, random residual, unique concepts and stable shuffled option identities. Both feedback modes, all key positions, next/end/results/review filters and actual accepted counts; old rounded-answer snapshot retains its own score.'),
 ('T06','9K','Legacy/unknown routes','Run all 7E actual/synthetic examples plus full 39/361/178/343 alias tables. Same old page 46 with two question IDs gives different correct lessons; gaps, unknown question, wrong namespace, invalid number and case-sensitive F31a. SIG16–18 unavailable with exact official actions, never SIG1/SIG5/Y1 substitutions.'),
 ('T07','9K 9L 9M','Navigation and state','All eight states/twelve entry points, 60 reading-node previous/next edges and related/reference return contexts. Exit unfinished test guard, missing session setup, moved block parent notice, retired one/many/none. Restart clears only existing transient state; no fabricated migrated progress or auto-credit.'),
 ('T08','9L 9N','Library and teaching coverage','All ten modules/forty lessons/ten reviews, four appendices and 24 reference groups; all five filters and forty tags preserve canonical order. Search/empty states; zero-question lessons remain available and three additional-assessment briefs explicit, no new baseline IDs.'),
 ('T09','9L 9O','Design approval and learner copy','Compare implemented library/reader/review and fallback/source states with explicitly approved step 8 preview revision. Check every one of fourteen replacement rules across visible copy and accessibility semantics; no old book name/chapter labels/folios. Legitimate source publisher names remain in sources/credits.'),
 ('T10','9C 9F 9O','Platform/package release','Build/test Android, desktop, iOS device/simulator and wasm as configured; installed resource/offline and source-link smoke checks, image legibility/accessibility on actual supported devices. Save commands, versions, devices and evidence; unsupported execution stays open, no success inferred from compilation.')]
verification = [dict(id=i, work_item_ids=t.split(), title=title, procedure=p, evidence='Save actual result, platform/package identity and attachments under implementation-evidence; not executed in 7F.') for i,t,title,p in matrix]
inputs = ['baseline.json','curriculum-map.json','question-map.json','question-actions.json','link-and-progress-map.json']
input_bindings=[dict(path=str((OUT/n).relative_to(ROOT)),sha256=digest(str((OUT/n).relative_to(ROOT)))) for n in inputs]
batches = []
for task in ['9D','9E','9F','9G','9H','9I','9J']:
    group = [z['question_id'] for z in assignments if (z['question_id'].startswith('sign-') if task == '9D' else z['work_item_id'] == task)]
    batches += [dict(work_item_id=task,batch=i//50+1,question_ids=group[i:i+50]) for i in range(0,len(group),50)]
data = dict(schema_version=1,step='7F',prepared_on='2026-10-14',status='planning complete; implementation and design not started',
 inputs=input_bindings, execution_gate='7G verification, then separately requested step 8 imagegen previews and explicit design approval, then authorization for step 9. All 9A–9O are future work.',
 signal_decision='Retain explicit unavailable_exact_entry policy for SIG16–18; exact official URLs and optional M03-L02 related teaching from 7E. No approved destination or asset is added.',
 work_items=items,question_assignments=assignments,execution_batches=batches,coverage=coverage,verification_cases=verification)
save('implementation-backlog.json',data)

# Exact preview fixtures from frozen source records, with no new visual design.
nodes={x['id']:x for x in c['curriculum_nodes']}
source_path=nodes['M03-L02']['source_location']['path']
text=(ROOT/source_path).read_text()
lesson=text.split('### M03-L02 · ',1)[1].split('\n### ',1)[0]
lesson='### M03-L02 · '+lesson.rstrip()
lookup={x['question_id']:(i,x) for i,x in enumerate(a['questions'])}
questions=[]
for qid, field in [('situation-001','original'),('fuel-saving-150-0.5','proposed_changes/draft_question')]:
    i,x=lookup[qid]; payload=x['original'] if field=='original' else x['proposed_changes']['draft_question']
    order=[1,0,3,2]  # Illustrative session order, never the source order.
    questions.append(dict(question_id=qid,origin=f'question-actions.json#/questions/{i}/{field}',
      status='unchanged reviewed assessment' if field=='original' else '7D proposed revision; not live or accepted for scoring',
      question=payload, primary_lesson=nodes[x['primary_lesson_id']],
      display_option_order=order,selected_original_option=1,correct_display_index=order.index(payload['correct']),
      selected_display_index=order.index(1),feedback_state='answered incorrectly; feedback revealed',
      source_references=next(z['source_reference_ids'] for z in q['questions'] if z['question_id']==qid)))
sign=next(x for x in c['sign_entries'] if x['code']=='B1')
captions=json.loads((ROOT/'docs/curriculum/sign-captions.json').read_text())['captions']
caption=next(x for x in captions if x.get('code')=='B1')
source_ids=['REF-9f4b74a976fa03fb','REF-0f011d29fdd9c97f','REF-8994a6a11921a063']
# Retain the exact evidence records including dates and scope, without copying huge cached pages.
source_samples=[]
for sid in source_ids:
    i,s=next((i,s) for i,s in enumerate(q['source_registry']) if s['id']==sid)
    checks=[]
    for check in s['source_checks']:
        r=check['record']
        checks.append(dict(path=check['path'],json_pointer=check['json_pointer'],record={k:v for k,v in r.items() if k not in ['text','html']}))
    source_samples.append(dict(id=sid,origin=f'question-map.json#/source_registry/{i}',url=s['url'],classification=s['classification'],source_checks=checks))
previews=dict(schema_version=1,step='7F',status='content handoff only; no visual preview generated',inputs=input_bindings,
 library=dict(module=next(x for x in c['modules'] if x['id']=='M03'),children=[nodes[x] for x in ['M03-L01','M03-L02','M03-L03','M03-L04','M03-R']],
   category_filters=l['category_routes'], lesson_tags=l['lesson_category_tags'], zero_primary_question_lessons=a['coverage_backlog'],
   learner_copy={'title':'Learning library','module_count':'10 modules','lesson_count':'40 lessons','sources_action':'Sources','sign_reference_action':'Road signs and reference','empty_search':'No matching lessons.'}),
 lesson_reader=dict(content_id='M03-L02',source_path=source_path,sha256=digest(source_path),approved_markdown=lesson,
   previous_id='M03-L01',next_id='M03-L03',source_ids=['source-traffic-law','source-sign-law','source-panels'],
   knowledge_check_visibility='Question visible initially; split Answer into deliberately revealed block, including accessibility semantics.'),
 answer_reviews=questions,sign_reference=dict(entry=sign,caption=caption,usage='Study/reference or revealed feedback only; this caption is not pre-answer assessment semantics.'),
 sources=source_samples, legacy_examples=l['examples'], signal_unavailable_cases=l['unresolved_destinations'],
 auxiliary_copy={'chooser_title':'Choose related teaching','unavailable_title':'Content unavailable','library_action':'Open learning library',
   'moved_passage_notice':'This passage has moved. The related lesson is shown below.',
   'missing_result':'No saved result is available.','setup_action':'Set up a practice test',
   'historical_attempt_notice':'This attempt used an earlier question version. Its original answer and score are shown.'},
 constraints=['No design/layout is specified or approved by 7F. Step 8 must use imagegen and wait for explicit approval before implementation.',
   'Use exact source text, titles, options and asset bytes. For imagegen, composite/place the verified artwork later if the tool cannot preserve it exactly; generated sign shapes are not correctness evidence.',
   'Show source classification and limits honestly. Reviewed reference publisher names remain; learner-facing old book attribution/folios do not.',
   'Do not show 1,000 active questions as a promise until accepted pool passes all gates. Module/lesson totals describe teaching, not completed progress.',
   'No invented bookmarks, completion counters, saved-history feature or public deep links. Active-session state only; historical/version fixture is a future compatibility example, not a shipped history screen.',
   'Pre-answer sign descriptions remain a 9D authoring task; do not invent them as approved content. Use the exact B1 reference in a study/revealed context for preview.',
   'Include intended-size/zoom concept for faint-outline delivery in step 8; only later actual-device evidence clears 38 holds.'])
save('preview-content.json',previews)

lines=['# 7F — Implementation backlog','', '**Completed:** 14 October 2026. Planning only. The live app, question bank, assets and approved PDF are unchanged. Steps 7G–10 have not been executed.',
 '', '[Structured tasks and all 1,000 assignments](implementation-backlog.json) · [Preview handoff](preview-handoff.md) · [Exact preview content](preview-content.json) · [7F checks](handoff-checks.json)',
 '', 'Run 7G next. Step 8 remains a separate imagegen design request requiring explicit approval before implementation. Every task below is future step 9 work and inherits that gate. New paths are marked `(new)`; audit records are inputs, not app runtime payloads.',
 '', '## Scope and decisions','',
 'Preserve the baseline 1,000 question IDs / 500 concepts: 336 retain, 626 rewrite, 38 replace, zero remove. The JSON assigns each exact ID to one content owner and its 7C/7D evidence. Sign rewrites are bounded batches of at most 50 IDs; shared semantics applies to all 616 sign questions. The 134 distractor changes are overlapping work, not additional questions.',
 '', '**SIG16–18 decision:** retain 7E’s explicit unavailable internal route, recorded official-description action and optional M03-L02 related teaching. Do not add a registry entry, asset or similar-signal alias. This resolves the planning choice while keeping the exact-entry gap visible. Adding exact entries later requires the content/asset verification workflow and a refreshed package.',
 '', '**Release holds:** all 626 rewrites require acceptance; the 38 replacements additionally require exact-code delivery/accessible-equivalent proof. No release may silently omit held questions, fill quotas with unaccepted items or claim all 1,000 are active. Failure returns a bounded content/ID decision. These implementation holds are not cleared by this document.',
 '', '**Learner data:** no durable store exists to migrate. Implement the audited transient-state contracts; future persistence/hot replacement is conditional separate scope. Do not build a new database or history feature as part of this plan.',
 '', '## Executable work items','']
for x in items:
    lines += [f"### {x['id']} — {x['title']}",'', '**Depends on:** '+(', '.join(x['dependencies']) or 'approved planning/design gate')+'.', '', '**Affected files:** '+', '.join('`'+f+'`' for f in x['affected_files'])+'.', '', '**Output:** '+x['output'],'','**Acceptance:**','']
    lines += ['- '+s for s in x['acceptance']]+['']
lines += ['## Step 10 verification specification','', 'These are required future checks, not results. Save actual commands, expected/observed results, release manifest digest, devices and attachments. A missing platform run stays open. Each work item is covered below; the structured coverage map also binds every 7B destination, 7D issue/shared dependency/coverage brief and 7E record family to owners.','']
for x in verification:
    lines += [f"- **{x['id']} — {x['title']}** ({', '.join(x['work_item_ids'])}): {x['procedure']}"]
lines += ['', '## Rebuild and local handoff checks','', 'From the repository root:', '', '```sh','python3 docs/curriculum/app-migration/build_implementation_handoff.py','python3 docs/curriculum/app-migration/verify_implementation_handoff.py','```','', 'The builder only writes the four 7F handoff artifacts. The verifier checks input identities, exhaustive question ownership, destination/issue/state coverage, dependency ordering, exact fixtures and protected baseline bytes. This is a bounded 7F handoff check; the independent full-package 7G verification remains pending.','']
(OUT/'implementation-backlog.md').write_text('\n'.join(lines))

p=['# 7F — App-preview content handoff','', '**Prepared:** 14 October 2026. This is exact content and behaviour for future step 8, not a visual design or implementation approval.', '', '[Exact fixtures](preview-content.json) · [Work items](implementation-backlog.md) · [Source registry](curriculum-map.json) · [7F checks](handoff-checks.json)', '', '## Step 8 sequence and required views','',
 'When separately requested, use the imagegen skill for library, lesson-reader and answer-review previews. Present the generated previews for explicit feedback/approval and revise/reapprove if requested. Do not start step 9 on the strength of 7F approval. Record the approved preview revision and bind it to the implementation handoff.', '',
 'The JSON is the content authority: exact source locators/hashes, approved Markdown, unchanged assessment, proposed exact fuel revision, shuffled display order, sign bytes/caption, source evidence and legacy fixtures. Technical IDs and old folios are audit metadata; they are not required learner labels. No layout, colour palette or new design is prescribed here.', '',
 '## Library preview','', 'Use **Learning library**, with **10 modules** and **40 lessons**, module **3. Read the road before acting**, and these exact approved titles in order:','']
for id in ['M03-L01','M03-L02','M03-L03','M03-L04','M03-R']:
    p.append('- '+nodes[id]['title']+' (`'+id+'`).')
p += ['', 'Include Sources and Road signs and reference actions. Use the five existing category labels and 7E many-to-many tags from JSON, maintaining canonical module numbering under a filter. Empty search: “No matching lessons.” Do not invent completion badges/bookmark history. M01-L01, M07-L04 and M10-L03 must stay discoverable despite no primary bank questions. Use accepted-package question counts only after acceptance, not an unconditional active-1,000 label.', '',
 '## Lesson-reader preview','', 'Use M03-L02 **Combine the instructions** under module 3. Preserve approved reading content, requirements and exceptions; show the opening goal and first requirements paragraph below. The full exact lesson is in JSON. Previous: **Recognise what a sign asks**; next: **Find your way without rushing**. Sources: source-traffic-law, source-sign-law and source-panels; return to the same lesson/position after a reference visit.', '']
p += [s+'\n' for s in lesson.split('\n\n')[1:3]]
p += ['', 'Knowledge check: **Does amber mean accelerate to beat red?** Hide its approved answer until deliberate reveal: **No. The rule is to stop; the exception concerns an unsafe stop after the change, not a wish to save time.** Keep hidden content out of accessibility reading before reveal. Full import must also preserve tables, calculations and longer content, represented by M03-L04 in implementation verification.', '',
 '## Answer-review previews','', 'Show feedback only after answering, preserving both existing immediate and end-of-test modes. Do not offer related teaching as an unanswered-test escape from the existing guard. Use the exact shuffled fixture orders; the key is display position B in both samples, not the first displayed option.', '']
for x in questions:
    payload=x['question']; p += ['### '+x['question_id'],'', '**Content status:** '+x['status']+'.','',payload['prompt'],'']
    for j,idx in enumerate(x['display_option_order']):
        p.append(f"- {chr(65+j)}. {payload['options'][idx]['text']}"+(' — selected (incorrect)' if idx==1 else ' — correct' if idx==payload['correct'] else ''))
    p += ['', '**Revealed explanation:** '+payload['explanation'], '', '**Related lesson:** '+x['primary_lesson']['title']+' (`'+x['primary_lesson']['id']+'`). Exact source-reference IDs are in JSON; publisher/classification must come from those records, not a generic official-source badge.','']
p += ['The fuel sample is a proposed 7D revision, not an applied change or newly approved scored item. Its old 0.8-litre attempt, if later supported as a historical snapshot, keeps its original score and version notice. Current app has no saved-attempt store; do not turn this compatibility case into a new history feature.', '',
 '## Reference, source and legacy states','',
 '- **B1 study/reference:** use the exact registered Give way artwork, Swedish official name, CAP-B1 caption and editorial-English notice from JSON. Use unchanged asset bytes, not an imagegen approximation. This is revealed/reference content; assessment-specific physical alt text is still future 9D work.',
 '- **Sources:** include Swedish legislation (REF-9f4b74a976fa03fb), commercial stopping shortcut (REF-0f011d29fdd9c97f) and model-specific Volvo guidance (REF-8994a6a11921a063). Display actual title/publisher and retained dates/limits from evidence; never relabel all as Transportstyrelsen. Commercial constants are exercise assumptions, and manufacturer speed limits are not universal rules. Editorial arithmetic remains labelled as such.',
 '- **Ambiguous old link:** old page 46 with situation-017 opens M04-L03; with situation-103 opens M04-L01. Page alone uses reviewed canonical choices, without displaying old chapter names or implying PDF equivalence. JSON contains the complete frozen-namespace examples.',
 '- **Unavailable signal:** SIG16–18 use their exact recorded 7E message and official-description action plus optional Combine the instructions. No exact approved internal entry exists; do not show SIG1, SIG5 or Y1 as its replacement.',
 '- **Other fallbacks:** show canonical chooser, unavailable/library action, moved-passage notice for known parent, and missing-results/setup state from JSON. Retired one/many/none examples are synthetic compatibility tests; no question has actually been removed.', '',
 '## Constraints to carry into approval','',
 'Imagegen establishes visual direction; it does not verify official sign geometry, small-size legibility or assistive semantics. Use the registered B1 image for study/reference content. For faint-outline presentation, preview the proposed intended size, framing and zoom interaction while retaining the original geometry; label all 38 holds uncleared until actual delivery tests. Never generate substitute sign artwork. If imagegen cannot preserve exact assets/text, use a clearly marked placement placeholder for later verified compositing and retain the exact JSON copy alongside the preview.', '',
 'Include source/reference return, large-text/long-content handling, empty search, multi-target chooser and unavailable state in the review set. No old book names, borrowed chapter labels or source-book folios in learner copy. Legitimate publisher names remain in sources and credits. No invented progress, persistence or deep links. All new presentation still requires explicit user approval.', '']
for alias in ['traffic-law','sign-law','panels']:
    source = next(z for z in c['source_destinations'] if z['id']=='source-'+alias)
    p.append('['+alias+']: '+source.get('scoped_urls',{}).get('M03',source['url']))
p.append('')
(OUT/'preview-handoff.md').write_text('\n'.join(p))
print('Built four 7F handoff artifacts; no live content written.')
