"""7G cross-stage migration planning audit. Never imports or edits live app content."""
import collections
import hashlib
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
checks = []
commands = []

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def test(name, ok, detail=None):
    checks.append(dict(name=name, passed=bool(ok), detail=detail))

@lru_cache(maxsize=None)
def doc(path):
    return read(ROOT/path)

def ptr(obj, path):
    for segment in path.lstrip('/').split('/'):
        if not segment:
            continue
        segment = segment.replace('~1', '/').replace('~0', '~')
        obj = obj[int(segment)] if isinstance(obj, list) else obj[segment]
    return obj

def group(name, fn):
    try:
        fn()
    except Exception as exc:
        test(name+' completed without structural errors', False, type(exc).__name__+': '+str(exc))

b = read(HERE/'baseline.json')
c = read(HERE/'curriculum-map.json')
q = read(HERE/'question-map.json')
a = read(HERE/'question-actions.json')
l = read(HERE/'link-and-progress-map.json')
f = read(HERE/'implementation-backlog.json')
p = read(HERE/'preview-content.json')
bank = doc('content/questions.json')
protected = b['frozen_inputs']+b['bundled_assets']
protected_start = {i['path']:sha(ROOT/i['path']) for i in protected}
# The full set of existing planning artifacts is part of the review snapshot.
package_paths = sorted(z for z in HERE.rglob('*') if z.is_file() and
    z.suffix in ['.py','.json','.md','.png'] and '__pycache__' not in z.parts and
    z.name not in ['verification.json','verification.md'])
extra_assets={ROOT/z['asset']['path'] for z in c['sign_entries']}
for loc in (ROOT/'docs/curriculum/pdf-production/chapters').glob('M*/illustrations.json'):
    illustrations=read(loc)
    extra_assets.update(ROOT/'docs/curriculum/pdf-design/gap-resolution'/z['file'] for z in illustrations['assets'].values())
    extra_assets.update(ROOT/z['path'] for z in illustrations.get('official_sign_placements',[]))
package_paths=sorted(set(package_paths)|extra_assets)
package_start = {str(z.relative_to(ROOT)):sha(z) for z in package_paths}

# Run the prior independent acceptance procedures in dependency order. These
# regenerate only their own planning-check files (7F also proves its rebuild).
for script in ['verify_question_map.py','verify_question_actions.py','verify_link_progress_map.py','verify_implementation_handoff.py']:
    result = subprocess.run([sys.executable,str(HERE/script)],capture_output=True,text=True)
    commands.append(dict(command='python3 docs/curriculum/app-migration/'+script,
        exit_code=result.returncode,stdout_sha256=hashlib.sha256(result.stdout.encode()).hexdigest(),
        diagnostic=(result.stdout+result.stderr)[-6000:] if result.returncode else None))
    test('fresh upstream acceptance: '+script,result.returncode==0)

approval = doc('docs/curriculum/pdf-production/final-review/screen-release.json')
nav = doc('docs/curriculum/pdf-production/assembly/navigation.json')['destinations']
registry = [z for k in ['curriculum_nodes','source_destinations','sign_entries','supporting_destinations'] for z in c[k]]
targets = {z['id'] for z in registry}
lessons = {z['id'] for z in c['curriculum_nodes'] if z['kind']=='lesson'}
sources = {z['id']:z for z in c['source_destinations']}
refs = {z['id']:z for z in q['source_registry']}
work = {z['id']:z for z in f['work_items']}
assign = {z['question_id']:z for z in f['question_assignments']}


def identities():
    test('approved screen release identity',approval['status']=='approved' and approval['edition']=='screen' and approval['pages']==578 and sha(ROOT/approval['artifact'])==approval['sha256']==b['release']['sha256'])
    test('approved screen delivery copies match',all(sha(ROOT/path)==approval['sha256'] for path in ['docs/curriculum/pdf-production/korkortgo-curriculum.pdf','docs/curriculum/pdf-production/korkortgo-curriculum-tagged.pdf','output/pdf/korkortgo-curriculum.pdf','output/pdf/korkortgo-curriculum-tagged.pdf']))
    test('7B–7E bind the same approved release',all(z['sha256']==approval['sha256'] and z['path']==approval['artifact'] for z in [c['release_binding'],q['release'],a['release'],l['approved_release']]))
    test('7B baseline digest current',c['baseline_sha256']==sha(HERE/'baseline.json'))
    test('all protected baseline inputs and bundled assets match',all(sha(ROOT/z['path'])==z['sha256'] for z in protected),dict(frozen_inputs=len(b['frozen_inputs']),bundled_assets=len(b['bundled_assets'])))
    bindings=[]
    for record,key in [(c,'input_bindings'),(q,'inputs'),(a,'inputs'),(l,'inputs'),(f,'inputs'),(p,'inputs')]:
        bindings.extend(record[key])
    bad=[z['path'] for z in bindings if not (ROOT/z['path']).is_file() or sha(ROOT/z['path'])!=z['sha256']]
    test('all cross-stage recorded input hashes current',not bad,dict(bindings=len(bindings),mismatches=bad))
    test('bank count IDs concepts categories from actual bytes',len(bank)==len({z['id'] for z in bank})==b['counts']['questions']==1000 and len({z['concept'] for z in bank})==b['counts']['concepts']==500 and dict(collections.Counter(z['category'] for z in bank))==b['counts']['categories'])
    test('baseline historical chapter count is audit-only',len(b['legacy_chapters'])==39 and len(c['modules'])==10 and len(lessons)==40 and len(l['chapter_aliases'])==39)
    test('print scope remains deferred',b['release']['edition']=='screen' and 'deferred' in b['release']['print_masters'] and 'deferred' in approval['print_requirements'])
group('input identities',identities)


def destinations():
    counts=collections.Counter(z['kind'] for z in c['curriculum_nodes'])
    test('88 curriculum nodes retain the full structure',counts==dict(module=10,lesson=40,module_review=10,appendix=4,sign_reference_group=24),dict(counts))
    test('all 1123 destination IDs unique and published',len(registry)==len(targets)==1123 and targets<=set(nav))
    test('all destination evidence folios agree with approved navigation',all(nav[z['id']]==z['pdf_evidence_page'] and 1<=z['pdf_evidence_page']<=578 for z in registry))
    bad=[]
    for z in registry:
        if 'source_location' not in z:
            continue
        loc=z['source_location'];path=ROOT/loc['path']
        if not path.is_file():
            bad.append(z['id']);continue
        if 'sha256' in loc and sha(path)!=loc['sha256']:
            bad.append(z['id'])
        if 'heading' in loc and path.read_text().splitlines()[loc['line']-1]!=loc['heading']:
            bad.append(z['id'])
        if 'json_pointer' in loc:
            ptr(doc(loc['path']),loc['json_pointer'])
    test('registered source locations and heading hashes resolve',not bad,bad)
    module_ids=[f'M{i:02}' for i in range(1,11)]
    test('canonical module lesson and review IDs ordered', [z['id'] for z in c['modules']]==module_ids and all(z['lesson_ids']==[z['id']+f'-L{i:02}' for i in range(1,5)] and z['review_id']==z['id']+'-R' for z in c['modules']))
    nodes={z['id']:z for z in c['curriculum_nodes']}
    test('module titles equal source registry titles',all(z['title']==nodes[z['id']]['title'] for z in c['modules']))
    test('lesson source IDs exist with explicit module scopes',all(set(z.get('source_destination_ids',[]))<=set(sources) and z.get('source_scope')==z['module_id'] for z in nodes.values() if z['kind']=='lesson'))
    test('60-node reading order matches curriculum',l['reading_order']==[i for mod in c['modules'] for i in [mod['id'],*mod['lesson_ids'],mod['review_id']]])
group('destinations',destinations)


def questions():
    ids=[z['id'] for z in bank]
    test('each of 7A–7F carries all baseline question IDs exactly once',all([z[key] for z in rows]==ids and len({z[key] for z in rows})==1000 for rows,key in [(q['questions'],'question_id'),(a['questions'],'question_id'),(l['question_routes'],'question_id'),(f['question_assignments'],'question_id')]) and b['question_ids_in_order']==ids)
    test('all originals in 7D equal the live frozen bank',all(z['original']==original for z,original in zip(a['questions'],bank)))
    invalid=[]
    for mp,act,route in zip(q['questions'],a['questions'],l['question_routes']):
        if not (mp['primary_lesson_id'] in lessons and set(mp['related_lesson_ids'])<=lessons and set(mp['reference_ids'])<=targets and set(mp['source_ids'])<=set(sources) and set(mp['source_reference_ids'])<=set(refs)):
            invalid.append(mp['question_id'])
        if not (act['primary_lesson_id']==route['target_id']==mp['primary_lesson_id'] and route['source_reference_ids']==mp['source_reference_ids'] and route['disposition']==act['disposition']):
            invalid.append(mp['question_id'])
    test('all question teaching source and route targets agree',not invalid,invalid)
    test('all 1000 teaching mappings covered without unresolved findings',all(z['coverage_status']=='covered' and z['teaching_evidence'] and not z['unresolved_mapping_findings'] for z in q['questions']))
    test('exact dispositions independently counted',dict(collections.Counter(z['disposition'] for z in a['questions']))=={'retain':336,'rewrite':626,'replace':38})
    test('all changes have evidence criteria and known task owner',all(z['evidence']['source_reference_ids'] and assign[z['question_id']]['work_item_id'] in work and (z['disposition']=='retain' or z['proposed_changes'] and z['acceptance_criteria']) for z in a['questions']))
    held=[z for z in a['questions'] if z['research_holds']]
    test('38 held replacements over 19 exact codes owned by 9F',len(held)==38 and len({q['questions'][ids.index(z['question_id'])]['sign_code'] for z in held})==19 and all(z['disposition']=='replace' and assign[z['question_id']]['work_item_id']=='9F' for z in held))
    test('no unrecorded hold types or hidden removals',all(all(h['type']=='asset/display evidence hold; meaning/key not disputed' for h in z['research_holds']) for z in held) and not any(z['disposition']=='remove' for z in a['questions']) and not l['production_tombstones'])
    test('four fuel midpoint cases have exact proposed revision owners',sum('FUEL-ROUNDING' in z['issues'] for z in a['questions'])==4 and all(assign[z['question_id']]['work_item_id']=='9I' and z['proposed_changes']['key_value_changes'] for z in a['questions'] if 'FUEL-ROUNDING' in z['issues']))
    test('three lesson sampling gaps have bounded additional-assessment briefs',{z['lesson_id'] for z in a['coverage_backlog']}=={'M01-L01','M07-L04','M10-L03'} and all(f['coverage']['7D/coverage/'+z['lesson_id']]['work_item_ids']==['9N'] for z in a['coverage_backlog']))
group('questions',questions)


def evidence():
    test('404 unique exact URL evidence records',len(refs)==len(q['source_registry'])==404 and len({z['url'] for z in refs.values()})==404)
    bad=[];n=0
    for r in refs.values():
        for s in r['source_checks']:
            n+=1
            if ptr(doc(s['path']),s['json_pointer'])!=s['record'] or s['record']['url']!=r['url']:
                bad.append(r['id'])
    test('all retained source check records equal cited evidence',not bad,dict(records=n,mismatches=bad))
    scoped=[]
    for mp in q['questions']:
        for s in mp['source_evidence']:
            if s.get('source_id'):
                node=sources[s['source_id']]
                if refs[s['reference_id']]['url']!=node.get('scoped_urls',{}).get(s['scope'],node['url']):
                    scoped.append(mp['question_id'])
    test('source URLs preserve canonical alias module scopes',not scoped,scoped)
    test('classifications retained rather than blanket official labels',all(z['classification'] for z in refs.values()) and any('Commercial' in z['classification'] for z in refs.values()) and any('Manufacturer' in z['classification'] for z in refs.values()))
    caps={z['code']:z for z in doc('docs/curriculum/sign-captions.json')['captions']}
    bad=[]
    for sign in c['sign_entries']:
        cap=caps[sign['code']]
        if sign['caption_id']!=cap['caption_id'] or sign['title']!=cap['label_en'] or sign['asset']!=cap['preferred_asset'] or sha(ROOT/sign['asset']['path'])!=sign['asset']['sha256'] or not cap['sources'] or not sign['eligible_for_placement']:
            bad.append(sign['id'])
    test('400 exact sign caption asset and eligibility bindings',len(c['sign_entries'])==400 and not bad,bad)
    checked=0;bad=[]
    for act in a['questions']:
        if not act['question_id'].startswith('sign-'):
            continue
        for opt in act['proposed_changes']['options']:
            checked+=1
            asset=opt['visual_description_brief']['exact_asset']
            if sha(ROOT/asset['path'])!=asset['sha256'] or opt['official_sources']!=caps[opt['code_metadata_after_reveal']]['sources']:
                bad.append(act['question_id'])
    test('2464 proposed sign option source and asset bindings',checked==2464 and not bad,bad)
    scenes=[]; placements=[]
    for path in sorted((ROOT/'docs/curriculum/pdf-production/chapters').glob('M*/illustrations.json')):
        illustrations=read(path)
        scenes.extend(illustrations['assets'].values())
        placements.extend(illustrations.get('official_sign_placements',[]))
    test('all 83 lesson scene placements retain approved source hashes and captions',len(scenes)==83 and all(sha(ROOT/'docs/curriculum/pdf-design/gap-resolution'/z['file'])==z['sha256'] and z['caption'] and z['alt_text'] and len(z['box'])==4 for z in scenes))
    test('all 329 final chapter sign placements retain exact assets and codes',len(placements)==329 and all(sha(ROOT/z['path'])==z['sha256'] and 'sign-'+z['code'] in targets for z in placements))

    test('assessment semantics and faint-display holds have separate owners','9D' in work and '9F' in work and len([z for z in f['execution_batches'] if z['work_item_id']=='9D'])==13)
    test('340 exact catalogue routes and three explicit unavailable routes',sum(z['target_id'] is not None for z in l['sign_routes'])==340 and [z['legacy_code'] for z in l['sign_routes'] if z['target_id'] is None]==['SIG16','SIG17','SIG18'])
    test('7F resolves exact-signal planning choice without guessed targets',p['signal_unavailable_cases']==l['unresolved_destinations'] and all(z['target_id'] is None and z['related_target_ids']==['M03-L02'] and z['legacy_external_url'].startswith('https://www.transportstyrelsen.se/') for z in l['unresolved_destinations']) and 'unavailable_exact_entry' in f['signal_decision'])
group('sources and assets',evidence)


def routing_state_backlog():
    test('legacy page span complete including explicit gaps',[z['legacy_page'] for z in l['legacy_page_aliases']]==list(range(6,367)) and sum(z['resolution']=='unavailable' for z in l['legacy_page_aliases'])==38)
    test('canonical choices in all old chapter aliases resolve',len(l['chapter_aliases'])==39 and all(z['target_ids'] and set(z['target_ids'])<=targets for z in l['chapter_aliases']))
    test('all five category labels and quotas preserved', {z['category_id']:z['baseline_quota_per_70'] for z in l['category_routes']}==dict(VEHICLE=7,ENVIRONMENT=5,SAFETY=16,RULES=32,PERSONAL=5))
    test('all forty lessons independently discoverable',{z['lesson_id'] for z in l['lesson_category_tags']}==lessons and p['library']['lesson_tags']==l['lesson_category_tags'])
    test('all 22 state contracts uniquely identified',len(l['state_rules'])==len({z['field'] for z in l['state_rules']})==22 and len(l['navigation_routes'])==8 and len(l['entry_point_rules'])==12)
    source_files=[z for root in ['composeApp/src','iosApp'] for z in (ROOT/root).rglob('*') if z.is_file() and z.suffix in ['.kt','.swift','.plist']]
    frozen_paths={z['path'] for z in b['frozen_inputs']}
    test('current app source inventory fully covered by frozen audit',all(str(z.relative_to(ROOT)) in frozen_paths for z in source_files),dict(source_files=len(source_files)))
    test('no durable learner store assumed or migration invented',b['persistent_user_data']['implementation_found'] is False and all(z['baseline'].startswith('no implementation') for z in l['state_rules'] if z['field'] in ['bookmarks','completed_lessons','question_history','persistent_storage_schema']))
    test('question revision and original shuffled score rules present',set(l['version_transition']['question_history_compatibility'])=={'retain','rewrite','replace','remove'} and 'Do not regrade' in l['version_transition']['unversioned_or_orderless_answers'] and 'do not create' in l['version_transition']['future_bookmark_completion_scope'] and 'authorise new persistence' in l['version_transition']['future_bookmark_completion_scope'])
    known=set(work);seen=set();valid=True
    for z in f['work_items']:
        valid &= set(z['dependencies'])<=seen
        seen.add(z['id'])
    test('all 15 work items have executable dependency order',len(work)==15 and valid and all(z['affected_files'] and z['output'] and z['acceptance'] for z in work.values()))
    test('all 7D shared dependencies and issue types have owners',all('7D/'+z['id'] in f['coverage'] for z in a['shared_implementation_dependencies']) and all(f['coverage']['7D/'+k]['record_count']==v for k,v in a['issue_counts'].items()))
    test('all recorded coverage owners resolve',all(z['work_item_ids'] and set(z['work_item_ids'])<=known for z in f['coverage'].values()))
    test('all fourteen learner-label replacement rules owned',len(l['labels_to_replace'])==14 and f['coverage']['7E/labels_to_replace']['record_count']==14 and f['coverage']['7E/labels_to_replace']['work_item_ids']==['9L'])
    test('all work items covered by ten future step10 procedures',len(f['verification_cases'])==10 and {id for z in f['verification_cases'] for id in z['work_item_ids']}==known)
    test('design preview and explicit approval gate retained','explicit design approval' in f['execution_gate'] and 'imagegen' in f['execution_gate'] and 'not started' in f['status'])
    test('proposed fuel preview is clearly not live scoring content','not live or accepted for scoring' in p['answer_reviews'][1]['status'])
    handoff=read(HERE/'handoff-checks.json')
    test('all 68 handoff checks pass on current exact artifacts',handoff['passed'] and len(handoff['checks'])==68 and all(sha(HERE/name)==digest for name,digest in handoff['artifact_sha256'].items()))
group('routes state and backlog',routing_state_backlog)

package_end={str(z.relative_to(ROOT)):sha(z) for z in package_paths}
test('prior package artifacts unchanged by fresh verification',package_start==package_end,[key for key in package_start if package_start[key]!=package_end[key]])
test('protected live and approved source bytes unchanged during 7G',all(sha(ROOT/path)==digest for path,digest in protected_start.items()))

holds=[dict(question_id=z['question_id'],sign_code=next(mp['sign_code'] for mp in q['questions'] if mp['question_id']==z['question_id']),work_item_id=assign[z['question_id']]['work_item_id'],holds=z['research_holds']) for z in a['questions'] if z['research_holds']]
carry=[
 dict(id='IMPLEMENTATION-ACCEPTANCE',scope='step 9/10 release gate',status='open future work',owner_ids=['9D','9E','9F','9G','9H','9I','9J'],detail='626 rewrites require per-item acceptance; 38 replacements additionally require exact official geometry, intended-size/zoom and accessible-equivalent proof. All remain unapplied. No silent omissions or quota changes.'),
 dict(id='SIG16-18',scope='explicit compatibility limitation',status='planning decision resolved; internal entries unavailable',owner_ids=['9K'],detail=f['signal_decision']),
 dict(id='ASSESSMENT-COVERAGE',scope='additional-assessment briefs',status='owned future work; no baseline question removal/addition',owner_ids=['9N'],detail='M01-L01 and M10-L03 have no primary or related questions; M07-L04 has no primary and one related. Keep teaching discoverable and prepare separately reviewed briefs.'),
 dict(id='SOURCE-CURRENCY',scope='implementation acceptance',status='dated evidence retained, no blanket new source verification',owner_ids=['9C','9G'],detail='7G verifies exact stored source/evidence bindings, not current availability or every legal claim. Recheck time-sensitive affected rules when applying edits and refresh records if changed.'),
 dict(id='DESIGN-AND-DEVICE-PROOF',scope='steps 8–10',status='not started',owner_ids=['9F','9L','9O'],detail='Step 8 must use imagegen and obtain explicit design approval. Real app builds/device/accessibility runs remain future evidence; planning checks do not certify runtime behaviour.'),
 dict(id='PRINT',scope='outside approved screen edition',status='explicitly deferred',owner_ids=[],detail='Print masters and print-resolution remediation were deferred by user scope; this audit does not reopen or certify them.')]
failed=[z for z in checks if not z['passed']]
report=dict(schema_version=1,step='7G',verified_on='2026-10-14',status='passed' if not failed else 'blocked',
 scope='Complete 7A–7F migration planning package; no app migration, new design, live legal review, device test or print certification.',
 approved_release=dict(path=approval['artifact'],sha256=approval['sha256'],pages=approval['pages'],edition='screen'),
 totals=dict(baseline_questions=len(bank),concepts=len({z['concept'] for z in bank}),modules=10,lessons=len(lessons),reviews=10,appendices=4,reference_groups=24,published_destinations=len(targets),sign_entries=len(c['sign_entries']),source_destinations=len(sources),question_source_records=len(refs),dispositions=dict(collections.Counter(z['disposition'] for z in a['questions'])),image_hold_questions=len(holds),lesson_scene_placements=83,chapter_sign_placements=329,implementation_items=len(work),future_verification_cases=len(f['verification_cases']),checks=len(checks),checks_passed=len(checks)-len(failed)),
 checks=checks,upstream_commands=commands,planning_blockers=failed,carry_forward=carry,question_asset_holds=holds,
 input_manifest=[dict(path=path,sha256=digest) for path,digest in sorted(package_end.items())],
 protected_inputs=dict(records=len(protected),unchanged=all(sha(ROOT/path)==digest for path,digest in protected_start.items())),
 next_step='8 — generate app previews with imagegen, then wait for explicit design approval; request separately.' if not failed else 'Revisit the failed input/substep before step 8.',
 live_bank_modified=False,app_implemented=False,design_previews_generated=False)
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# 7G — Complete app-migration planning verification','',
 '**Verified:** 14 October 2026. **Result: '+('PASS — step 7 planning complete.' if not failed else 'BLOCKED — planning checks require repair.')+'**', '',
 '[Machine-readable results and input hashes](verification.json) · [Implementation backlog](implementation-backlog.md) · [Preview handoff](preview-handoff.md)', '',
 f"Freshly ran 7C, 7D, 7E and 7F acceptance procedures, then checked the relationships across the full package. **{len(checks)-len(failed)}/{len(checks)} cross-stage checks pass.** The current 7F checker also reports 68/68. These are planning/evidence checks, not runtime app or design acceptance.", '',
 '## Verified package','',
 '| Area | Result |','|---|---|',
 '| Approved input | Tagged 578-page screen release; all stages agree on SHA-256 `'+approval['sha256']+'`; explicit 6N approval retained. |',
 '| Frozen input integrity | All '+str(len(b['frozen_inputs']))+' baseline input records and 343 bundled asset records match, as do recorded cross-stage hashes. Protected bytes and prior planning artifacts unchanged during verification. |',
 '| Curriculum | 10 modules, 40 lessons, 10 reviews, four appendices, 24 reference groups. All 1,123 published destinations unique, source-located and matched to approved navigation folios. |',
 '| Questions | All 1,000 baseline IDs in order across 7A–7F, 500 concepts, correct scoped teaching/source routes and unchanged original bank. |',
 '| Decisions | 336 retain, 626 rewrite, 38 replace, zero remove. Every changed item has evidence, acceptance criteria and a bounded implementation owner. Four exact fuel revisions remain proposals. |',
 '| Sources/assets | 116 canonical source destinations, 404 exact question URL records, 400 sign/caption/asset bindings and 2,464 proposed sign-option bindings checked against retained evidence; all 83 lesson scene placements and 329 chapter sign placements retain their approved source hashes. |',
 '| Legacy navigation | 39 chapters, 361 numeric page entries including 38 gaps, 178 topic identities and 343 catalogue records accounted for. 340 exact sign routes; three explicit unavailable policies. |',
 '| Learner state | Eight navigation states, 12 entry-point rules, 22 state contracts, original option-order/score preservation. No durable store or real data migration exists. |',
 '| Implementation/design handoff | 15 dependency-ordered work items, exhaustive question ownership/batches, all issue/state/label coverage, exact preview fixtures and ten future step 10 procedures. |','',
 '## Planning blockers and implementation limits','',
 'No blocking migration-planning issues remain.' if not failed else 'Planning blockers: '+json.dumps(failed,ensure_ascii=False), '',
 'The following are explicit future work or scope limits, not evidence that implementation acceptance has passed:','']
for z in carry:
    lines.append('- **'+z['id']+'** — '+z['detail'])
lines += ['', 'The 38 exact question holds, their 19 sign codes and 9F ownership are retained individually in the JSON report. If official delivery cannot meet acceptance, return an explicit alternative-item/ID decision. No removal or similar-signal alias is authorised by this audit.', '',
 '## Interpretation and reproducibility','',
 '7A–7E include historical “next step not started” statements and historical review-book hashes. They describe their own execution time, not current blockers. This report binds the current approved tagged release and current frozen package without rewriting historical evidence. The former 39-chapter app is compatibility input only; it is not the curriculum to import.', '',
 'Rerun from the repository root:', '', '```sh','python3 docs/curriculum/app-migration/verify_migration_package.py','```','',
 'The script runs upstream validators sequentially, independently checks cross-stage counts/IDs/inputs/links/evidence/assets/state/backlog and writes these two reports. It fails with a nonzero exit code on any blocking check. Its input manifest includes the verifier itself, prior artifacts and referenced sign/scene assets, excluding these output reports to avoid circular hashes.', '',
 '**Next:** '+report['next_step']+' No app code, live question, official asset or approved PDF was changed.','']
(HERE/'verification.md').write_text('\n'.join(lines))
print(json.dumps(dict(status=report['status'],totals=report['totals'],planning_blockers=failed),indent=2))
raise SystemExit(1 if failed else 0)
