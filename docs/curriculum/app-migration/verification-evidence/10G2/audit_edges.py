"""Review every frozen7E example and policy against fresh typed/model/shared observations."""
import hashlib,json,sys
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent;BASE=HERE.parent
read=lambda p:json.loads((ROOT/p).read_text());sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest();m=read('docs/curriculum/app-migration/link-and-progress-map.json');e=read(str(HERE.relative_to(ROOT)/'compiled-edge-observations.json'));ui=read(str(HERE.relative_to(ROOT)/'recovery-action-observations.json'));alias=read(str(BASE.relative_to(ROOT)/'10G1/complete-alias-results.json'));bycase={r['case_id']:r for r in e['cases']};rows=[];checks=[]
def check(name,ok):checks.append({'name':name,'status':'pass' if ok else 'fail'})
def found(result,id):return result['type']=='found' and result['target']=={'content_id':id,'block_id':None}
for example in m['examples']:
 actual=bycase[example['id']]['actual'];expected=example['after'];kind=expected['kind'];ok=found(actual,expected['content_id']) if kind=='content' else actual['type']=='unavailable'
 if example['id']=='missing-block':ok=ok and bool(actual['notice'])
 if example['id']=='missing-exact-signal':ok=ok and actual['related']==[{'content_id':expected['related_content_id'],'block_id':None}] and actual['official_reference_id'] is not None
 check('7E example '+example['id'],ok);rows.append({'example_id':example['id'],'kind':example['kind'],'input':example['before'],'expected':expected,'actual':actual,'original_scope':example['expected'],'status':'pass' if ok else 'fail'})
for r in e['cases']:
 id=r['case_id'];a=r['actual']
 if r['example_id']:continue
 if id=='F31a-exact':ok=found(a,next(s['target_id'] for s in m['sign_routes'] if s['legacy_code']=='F31a'))
 elif id in ['normalized-chapter','page46-alone']:
  targets=m['chapter_aliases'][0]['target_ids'] if id=='normalized-chapter' else next(s['target_ids'] for s in m['legacy_page_aliases'] if s['legacy_page']==46)
  ok=a['type']=='choices' and [x['target']['content_id'] for x in a['choices']]==targets and bool(a['notice'])
 elif id=='valid-canonical-over-question':ok=found(a,'M01-L01')
 else:ok=a['type']=='unavailable' and bool(a['message'])
 check('Typed boundary '+id,ok)
check('Distinct page46 context lessons',found(bycase['same-old-page-a']['actual'],'M04-L03') and found(bycase['same-old-page-b']['actual'],'M04-L01'))
check('Four exact chooser actions navigate deliberately',len(e['chooser_actions'])==4 and all(r['decision']['type']=='allow' and r['offered']==r['navigated']['target'] for r in e['chooser_actions']))
check('Moved precise passage clears old offset/focus',found(e['moved_restore']['resolution'],'M03-L04') and e['moved_restore']['position'] is None and e['moved_restore']['focus_id'] is None)
check('Noninteger and overflow are outside typed Int lookup, not a new parser',len(e['noninteger_boundaries'])==5 and all(r['status']=='not_representable_as_LegacyLookup_Page_Int' for r in e['noninteger_boundaries']))
check('Blank typed question/canonical IDs rejected',len(e['construction_boundaries'])==2 and all(r['status']=='rejected_by_typed_constructor' for r in e['construction_boundaries']))
check('Actual chooser/recovery component actions pass',len(ui['actions'])==7 and all(r['status']=='pass' for r in ui['actions']) and ui['status']=='pass_shared_scope')
for i,r in enumerate(ui['retirement_fixtures']):check('Synthetic retirement '+str(i),len(r['replacement_ids'])==i and (r['actual']['type']=='unavailable' if i==0 else r['actual']['type']=='choices' and [v['target']['content_id'] for v in r['actual']['choices']]==r['replacement_ids']))
check('No production retirement data or bank activation inferred',e['production_tombstones']==[] and ui['historical_unaccepted_candidate_scoring_gate'].startswith('rejected') and alias['status']=='pass')
paths=['composeApp/src/androidMain/AndroidManifest.xml','iosApp/Info.plist','composeApp/src/androidMain/kotlin/se/korkort/MainActivity.kt','composeApp/src/iosMain/kotlin/se/korkort/MainViewController.kt','composeApp/src/wasmJsMain/kotlin/se/korkort/main.kt']
check('Audited hosts still launch App without public deep-link registration','android.intent.action.VIEW' not in (ROOT/paths[0]).read_text() and 'CFBundleURLTypes' not in (ROOT/paths[1]).read_text() and all('App()' in (ROOT/p).read_text() for p in paths[2:]))
policy_evidence={
'order':['valid-canonical-over-question','invalid-canonical-no-question-fallback','same-old-page-a','unknown-question-no-page-fallback','normalized-chapter','page46-alone'],
'question_context_precedence':['same-old-page-a','same-old-page-b','unknown-question-no-page-fallback','unknown-question-no-title-fallback'],
'unknown_canonical':['unknown-canonical','shared unavailable→explicit library'],
'missing_block':['missing-block','moved_restore'],
'multi_target_alias':['page46-alone','chooser_actions','shared four chooser actions'],
'invalid_legacy_page':['page MIN/MAX/negative/out-of-range/gaps','wrong namespace','noninteger boundaries: typed API exclusion'],
'retired_content':['three labelled retirement_fixtures; no production tombstones'],
'retired_question':['retired-question: unknown synthetic question stays unavailable; production removes zero'],
'unaccepted_replacement_question':['replacement-image teaching route','historical_unaccepted_candidate_scoring_gate','current accepted status separately audited10G1'],
'native_and_web_entry':paths}
assert set(policy_evidence)==set(m['resolution_policy'])
report={'task':'10G2','status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','identity':e['identity'],'counts':{'frozen_examples':len(rows),'typed_resolution_cases':len(e['cases']),'noninteger_boundaries':5,'constructor_rejections':2,'chooser_model_actions':4,'shared_recovery_actions':7,'synthetic_retirement_cases':3,'resolution_policies':len(policy_evidence),'checks':len(checks),'failed':sum(c['status']=='fail' for c in checks)},'examples':rows,'typed_cases':e['cases'],'checks':checks,'policy_evidence':policy_evidence,'entry_source_hashes':[{'path':p,'sha256':sha(p)} for p in paths],'scope':'Internal typed routes; noninteger inputs cannot enter an Int parameter. Shared components use semantic actions, not native/browser hit-testing or a public URL parser. Retired examples do not introduce a history/import/removal feature.'}
(HERE/'route-edge-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'counts':report['counts'],'failures':[c for c in checks if c['status']=='fail']},indent=2));sys.exit(0 if report['status']=='pass' else 1)
