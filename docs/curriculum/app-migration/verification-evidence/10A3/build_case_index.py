"""Prepare independent verification cases. This never runs or passes T01–T10."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
BASE=OUT.parent
M='docs/curriculum/app-migration/'
PATHS={'backlog':M+'implementation-backlog.json','actions':M+'question-actions.json','links':M+'link-and-progress-map.json','registry':M+'curriculum-map.json','question_map':M+'question-map.json','accepted':'content/accepted-assessment-questions.json','curriculum':'content/curriculum.json','manifest':'content/accepted-content-manifest.json','sources':'content/package-sources.json','handoff':M+'implementation-evidence/evidence-index.json','faint':'docs/curriculum/app-design/faint-assets-v1/asset-bindings.json','scope':str((BASE/'10A2/scope-matrix.json').relative_to(ROOT)), 'design_package':'docs/curriculum/app-design/8n/package-index.json'}
DATA={k:json.loads((ROOT/p).read_text()) for k,p in PATHS.items()}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def escape(s):return str(s).replace('~','~0').replace('/','~1')
def locator(alias,pointer,value):return {'oracle':alias,'pointer':pointer,'record_sha256':digest(value)}
def pointer(doc,p):
 for part in p.strip('/').split('/') if p else []:
  part=part.replace('~1','/').replace('~0','~');doc=doc[int(part)] if isinstance(doc,list) else doc[part]
 return doc

def build():
 assert all(json.loads((BASE/f'{s}/results.json').read_text())['status']=='pass' for s in ['10A1','10A2'])
 actions=DATA['actions']['questions']; accepted=DATA['accepted']['questions']; aq={q['key']['question_id']:q for q in accepted};action_by={q['question_id']:q for q in actions}
 assert set(aq)==set(action_by) and len(aq)==1000
 owner={};batches=[]
 for b in DATA['backlog']['execution_batches']:
  if b['work_item_id']=='9E':
   n=b['batch'];ids=b['question_ids'];task=f'10E{n+1}'
   assert len(ids)==(28 if n==12 else 50)
   batches.append({'id':f'9E{n}','owner':task,'question_ids':ids,'count':len(ids),'source':locator('backlog',f"/execution_batches/{DATA['backlog']['execution_batches'].index(b)}",b)})
   for qid in ids:assert qid not in owner;owner[qid]=task
 replacements=[]
 for s in DATA['handoff']['steps']:
  if re.fullmatch('9F\\d+',s['step']):
   ids=s['accepted_question_ids'];assert len(ids)==2
   replacements.extend(ids);batches.append({'id':s['step'],'owner':'10E14','delivery_owner':'10D2','question_ids':ids,'count':2,'source':locator('handoff',f"/steps/{DATA['handoff']['steps'].index(s)}",s)})
   for qid in ids:assert qid not in owner;owner[qid]='10E14'
 issue_owner={'SCENARIO-SCOPE-OR-EXPLANATION':'10E15','LOAD-WEIGHT-CONVENTION':'10E16','FUEL-ROUNDING':'10E17','FUEL-UNIT-GRAMMAR':'10E18'}
 for q in actions:
  qid=q['question_id']
  if qid not in owner:
   choices=[v for k,v in issue_owner.items() if k in q['issues']]
   assert len(choices)<=1
   owner[qid]=choices[0] if choices else '10E1'
 assert collections.Counter(owner.values())==collections.Counter({'10E1':336,**{f'10E{n+1}':50 if n<12 else 28 for n in range(1,13)},'10E14':38,'10E15':8,'10E16':30,'10E17':4,'10E18':6})
 distractors=[q['question_id'] for q in actions if 'SIGN-OUTLINE-DISTRACTOR' in q['issues']]
 assert len(distractors)==134 and len(replacements)==38
 faint_ids={a['asset_id'] for a in DATA['faint']['assets']}
 faint_slots=[]
 for q in accepted:
  for slot,image in [('stem',q['image'])]+[(o['id'],o['image']) for o in q['options']]:
   if image and image['asset_id'] in faint_ids:faint_slots.append({'question_id':q['key']['question_id'],'revision':q['key']['revision'],'slot':slot,'asset_id':image['asset_id']})
 faint_questions=sorted({s['question_id'] for s in faint_slots});assert len(faint_ids)==12 and len(faint_questions)==24 and set(faint_questions)<=set(replacements)
 inventory=[]
 for i,q in enumerate(actions):
  qid=q['question_id'];a=aq[qid]
  inventory.append({'case_id':'T04-Q-'+qid,'question_id':qid,'revision':a['key']['revision'],'disposition':q['disposition'],'owner':owner[qid],'status':'not_run','oracle':locator('actions',f'/questions/{i}',q),'accepted_snapshot':locator('accepted',f'/questions/{accepted.index(a)}',a),'acceptance_locator':locator('accepted',f'/questions/{accepted.index(a)}/acceptance',a['acceptance']),'issues':q['issues']})
 question_data={'schema_version':1,'status':'prepared_not_executed','partition':dict(collections.Counter(owner.values())),'sign_rewrite_batches':batches[:12], 'replacement_pairs':batches[12:],'all_question_cases':inventory,'distractor_change_ids':distractors,'faint_asset_ids':sorted(faint_ids),'faint_question_ids':faint_questions,'faint_slot_bindings':faint_slots,'review_rule':'Use approved 7D draft/original, per-ID acceptance/source evidence and independent arithmetic. Accepted snapshot pins the candidate; its presence is not proof of correctness. Retained payload equality excludes approved routing/provenance metadata changes.'}
 families=[]
 def family(name,gate,task,alias,key,expect):
  value=pointer(DATA[alias],key);items=list(enumerate(value)) if isinstance(value,list) else list(value.items())
  rows=[]
  for i,v in items:
   subject=v.get('id',v.get('question_id',v.get('field',v.get('entry',str(i))))) if isinstance(v,dict) else str(v)
   conditional=name=='state_contracts' and isinstance(v,dict) and v.get('baseline','').startswith('no implementation')
   rows.append({'case_id':f'{gate}-{name}-{i}','subject':subject,'status':'conditional_future_scope' if conditional else 'not_run','oracle':locator(alias,key+'/'+escape(i),v)})
  families.append({'id':name,'gate':gate,'owner':task,'coverage':'exhaustive','expected':expect,'members':rows})
 for key in ['curriculum_nodes','source_destinations','sign_entries','supporting_destinations']:
  family('registry_'+key,'T01','10B13' if key=='sign_entries' else '10B1','registry','/'+key,'Canonical identity/type/order/target matches approved registry and source origin; no omission, duplicate or folio-based route.')
 family('reference_groups','T01','10B13','curriculum','/reference_groups','All 24 groups retain exact membership/order/title and complete sign/reference navigation.')
 family('artwork_bindings','T01','10B13','curriculum','/assets','Compare original/bundled bytes, exact variant, approved crop, reuse/credit and accessibility text; follow approval/origin locators.')
 family('official_entries','T01','10B13','curriculum','/sign_entries','Compare caption/meaning/code with approved sign-caption origin and source records; package equality alone does not verify meaning.')
 block_cases=[]
 def visit(v,p,doc):
  if isinstance(v,dict):
   if isinstance(v.get('metadata'),dict) and 'origin' in v['metadata']:
    origin=v['metadata']['origin'];module=re.match(r'M(\d{2})',doc)
    task=f'10B{int(module[1])+1}' if module else '10B12' if doc.startswith('appendix-') else '10B13' if doc.startswith(('reference-','sign-')) else '10B1'
    block_cases.append({'case_id':f'T01-BLOCK-{len(block_cases)+1:04d}','subject':v['metadata']['id'],'document':doc,'owner':task,'status':'not_run','oracle':locator('curriculum',p,v),'approved_origin':origin,'expected':'Complete normalized block agrees with approved production source at the origin locator and PDF folio, including tables/scenarios/answer separation. Do not merely compare generated output with its own input.'})
   for k,c in v.items():visit(c,p+'/'+escape(k),doc)
  elif isinstance(v,list):
   for i,c in enumerate(v):visit(c,p+'/'+str(i),doc)
 for i,d in enumerate(DATA['curriculum']['documents']):visit(d,f'/documents/{i}',d['id'])
 families.append({'id':'teaching_blocks','gate':'T01','owner':'per_member','coverage':'exhaustive','members':block_cases})
 family('question_source_urls','T02','10C1','question_map','/source_registry','Compare all exact URLs/publishers/classifications/dates/limits with retained evidence; check aliases in their module scope.')
 family('canonical_sources','T02','10C1','sources','/destinations','Source destination/alias resolves to correct scoped reference and preserves actual publisher/claim limits.')
 family('source_reference_records','T02','10C1','sources','/references','Retain exact recorded classification/dates/scope and references; claim-specific currency is separately checked by 10C2.')
 for key in ['chapter_aliases','legacy_page_aliases','unused_topic_routes','sign_routes','question_routes','examples','resolution_policy','unresolved_destinations']:
  family(key,'T06','10G3' if key=='unresolved_destinations' else '10G2' if key in ['examples','resolution_policy'] else '10G1','links','/'+key,'Resolver result and explicit recovery/chooser actions equal this independent 7E contract; no guessed page/namespace/code fallback.')
 for key in ['navigation_routes','entry_point_rules','state_rules','version_transition']:
  family('state_contracts' if key=='state_rules' else key,'T07','10H3' if key=='state_rules' else '10H1' if key in ['navigation_routes','entry_point_rules'] else '10F3','links','/'+key,'Execute the complete recorded rule, including pinned context/guard/reset boundaries; conditional absent-store cases remain outside runtime scope.')
 reading=DATA['links']['reading_order'];edges=[]
 for i,x in enumerate(reading):
  edges.append({'case_id':f'T07-EDGE-{i+1:02d}','subject':x,'previous':reading[i-1] if i else None,'next':reading[i+1] if i+1<len(reading) else None,'status':'not_run','oracle':locator('links',f'/reading_order/{i}',x)})
 families.append({'id':'reading_edges','gate':'T07','owner':'10H1','coverage':'exhaustive','expected':'Previous/next equals frozen canonical sequence including null boundaries; source/reference returns preserve origin.','members':edges})
 for key in ['category_routes','lesson_category_tags']:
  family(key,'T08','10I2','links','/'+key,'Exact expected membership, canonical module order, retained query/filter and explicit empty reset; never open unrelated first lesson.')
 family('teaching_documents','T08','10I1','curriculum','/documents','All approved teaching/appendix/reference documents remain available with complete body, separately revealed answers and canonical title/order.')
 family('assessment_gaps','T08','10I3','actions','/coverage_backlog','M01-L01/M10-L03 zero primary/related, M07-L04 zero primary/one related; teaching discoverable, brief/rubric retained and no new scored IDs.')
 family('copy_rules','T09','10J3','links','/labels_to_replace','Each exact replacement rule holds in visible and accessible text; legitimate publishers/artwork credits remain.')
 family('supporting_document_updates','T09','10J3','links','/supporting_document_updates','Current documentation claims agree with accepted features/counts; technical provenance remains outside learner copy.')
 family('approved_previews','T09','10J1','design_package','/approved_preview_tasks','Compare implemented states with exact approved revision and bound artwork/content. Read final app-design-review.md to resolve historical 8N pending approval; later faint-artwork revision is separately bound.')
 # Preserve all original 7F coverage families as an explicit crosswalk.
 coverage=[]
 for k,v in DATA['backlog']['coverage'].items():
  if k.startswith('7B/'):tasks=['10B1','10B13','10B14']
  elif k.startswith('7E/'):
   name=k.split('/')[1];tasks=['10H1'] if name=='reading_order' else next(([f['owner']] for f in families if f['id']==('state_contracts' if name=='state_rules' else name)),['10C1','10C3'] if name=='source_routes' else ['10G2','10H3'])
  else:
   if 'coverage/' in k:tasks=['10I3']
   elif 'SOURCE' in k:tasks=['10C1','10C3']
   elif 'SHUFFLE' in k:tasks=['10F2']
   elif 'SIGN' in k or 'SEMANTICS' in k:tasks=['10D1','10D2','10D3','10D4']
   else:tasks=[issue_owner.get(k.split('/',1)[1],'10E18')]
  coverage.append({'original_family':k,'owners':tasks,'oracle':locator('backlog','/coverage/'+escape(k),v),'status':'not_run'})
 # Each clause specifies its observable outcome and independent oracle.
 clause_specs={
 'T01':[
 ('10B1','All 1,123 canonical IDs unique/resolving; titles/order/opening disclaimer exact.','registry'),
 ('10B2–10B11','All ten modules, forty lessons and ten reviews: complete explanations/scenarios/tables/answer blocks and approved scenes, via teaching_blocks.','registry'),
 ('10B12','All four appendices complete and correctly linked.','registry'),
 ('10B13','All 400 official entries, 24 groups and 484 artwork bindings preserve exact official geometry, crops, caption/reuse evidence.','registry'),
 ('10B14','Approved page-193 correction explicitly checked at its mapped origin, full JSON/Kotlin parity and deterministic generation.','question_map')],
 'T02':[
 ('10C1','All 404 exact question-source URL entries, 116 canonical aliases and 519 package references preserve scoped publisher/date/limits.','question_map'),
 ('10C2','Claim-specific primary-source recheck for selected high-risk/affected rules; no universal freshness claim.','sources'),
 ('10C3','Official law, foreign guidance, research, commercial shortcut, manufacturer and editorial arithmetic: details, exact external callback, unreachable/offline path and same return context.','sources')],
 'T03':[
 ('10D1','Every revised sign/variant/neutral physical description and 134 overlapping distractor changes inspected in both paired directions.','actions'),
 ('10D2','All 38 formerly held replacements and twelve faint assets/24 affected questions bind exact accepted revisions.','actions'),
 ('10D3','Fresh four-setting full-question/fit/zoom/return legibility matrix, equal option sizes, 220 dp minimum frames and narrow reflow; never generate substitute official art.','faint'),
 ('10D4','No pre-answer code/key/classification leak; keyboard/semantics/required TalkBack, modal exclusion and exact trigger return; distinguish exclusions.','scope')],
 'T04':[
 ('10E1','All 1,000 IDs accounted; 336 retained assessment payloads unchanged, no unaccepted active item.','actions'),
 ('10E2–10E13','All 578 sign rewrites meet independent per-ID approved drafts, including distractor/description/source checks.','actions'),
 ('10E14','All 38 replacements meet approved payload and acceptance rules; fresh delivery remains T03.','actions'),
 ('10E15','Eight scoped scenario corrections supported with exact conditions/exceptions.','actions'),
 ('10E16','Thirty driver-inclusive load calculations independently recomputed.','actions'),
 ('10E17','Four fuel keys independently computed from decimal prompt values and units; no old rounded-key reuse.','actions'),
 ('10E18','Six bounded unit drafts and known residual wording reviewed; all 626 rewrites + 38 replacements reconciled.','actions')],
 'T05':[
 ('10F1','Every length 1–70, seeds 0–19, both modes: independent largest-remainder quota/tie oracle, concept capacity after category picks, five residual slots at 70, uniqueness.','links'),
 ('10F2','All key positions and authored/display shuffle identities, immediate/deferred boundaries, next/end/results/filter/score persist.','links'),
 ('10F3','Old rounded-answer snapshot retains original score/order/key/feedback; invalid, held and mismatched package inputs rejected.','links'),
 ('10F4','Real accepted-bank production journeys in both modes preserve count, scores, review/filter/source/teaching context; distinguish harness fixtures.','scope')],
 'T06':[
 ('10G1','Exhaustive 39/361/178/343 alias families and all 1,000 question routes resolve to exact expected outcomes.','links'),
 ('10G2','Every 7E example plus page46 context pairs, page gaps, unknown question, wrong namespace, invalid number and case-sensitive F31a.','links'),
 ('10G3','SIG16–18 unavailable, exact official actions and optional M03-L02; never SIG1/SIG5/Y1 substitutes.','links')],
 'T07':[
 ('10H1','All eight states/twelve entry rules and sixty reading-node previous/next edges preserve context including related/reference return.','links'),
 ('10H2','Cancel/confirm unfinished-test exit, missing-session setup, moved-block parent notice, retired zero/one/many, no pre-answer reading shortcut.','links'),
 ('10H3','All eighteen applicable transient contracts pass; four absent-store cases conditional. Same-process preferences and fresh-process defaults/reset; no fabricated progress or auto-credit.','links')],
 'T08':[
 ('10I1','10/40/10 teaching units, four appendices and 24 groups discoverable and complete, with deliberate reveal.','registry'),
 ('10I2','All five category filters/forty tags and combined search/empty/reset states retain canonical order and query context.','links'),
 ('10I3','Three zero/low-question lessons remain discoverable; three assessment briefs explicit and no new baseline IDs.','actions')],
 'T09':[
 ('10J1','Every approved preview revision maps to implemented home/setup/library/reader/review/source/reference/fallback/guard state including faint-layout revision.','faint'),
 ('10J2','Current rendering matches approved hierarchy/type/spacing/size/scroll/interaction in themes/large text; any design fix awaits preview approval.','scope'),
 ('10J3','All fourteen copy rules in visible and accessibility text; no legacy book names/chapter labels/folios, legitimate publishers/licences/credits/disclaimer retained.','links')],
 'T10':[
 ('10K1','Fresh common suites and six generation/release checks, accepted identity and source/resource parity.','manifest'),
 ('10K2','Android normal/proof distinction, APK/resources/offline/native/production/source/legibility/assistive checks and restoration.','scope'),
 ('10K3','Configured desktop JAR/classpath/harness/keyboard/semantic checks; no native product/bridge claim.','scope'),
 ('10K4','Normal iOS simulator framework/app/resources, native cases, description/trait audits, existing device restored; no listening/device claim.','scope'),
 ('10K5','Normal iOS device ARM64/framework/resource build; physical execution excluded, not passed.','scope'),
 ('10K6','Normal production Wasm distribution, fresh-origin source callbacks/runtime/keyboard/artwork; static host and excluded cold-offline/speech limits.','scope'),
 ('10K7','Commands/toolchains/devices/binary hashes/candidate fingerprint match final cross-gate evidence; unavailable required execution blocks closure.','scope')]
 }
 clauses=[]
 for gate,specs in clause_specs.items():
  original=next(c for c in DATA['backlog']['verification_cases'] if c['id']==gate)
  for i,(tasks,expected,oracle) in enumerate(specs):
   if '–' in tasks:
    a,b=tasks.split('–');prefix=re.match(r'10[A-M]',a)[0];owners=[prefix+str(n) for n in range(int(a[len(prefix):]),int(b[len(prefix):])+1)]
   else:owners=[tasks]
   clauses.append({'case_id':f'{gate}-CLAUSE-{i+1:02d}','gate':gate,'owners':owners,'expected':expected,'oracle':oracle,'status':'not_run','observed':None,'evidence':[],'original_procedure':original['procedure'], 'required_artifacts':['review.md','results.json','commands or steps with environment','hash-bound captures/logs'], 'close_rule':'All required cases in the mapped exhaustive families and runtime matrix pass on the final candidate; original clause remains open otherwise.'})
 # Runtime matrix: use accepted revisions, never historical held objects as scored input.
 sign_ids=[q['question_id'] for q in actions if 'SIGN-QUESTION-COPY' in q['issues']]
 settings=[{'id':f'{theme}-{int(scale*100)}','theme':theme,'font_scale':scale} for theme in ['light','dark'] for scale in [1.0,1.6]]
 contexts=[]
 for target,ids in [('desktop',sign_ids),('android',replacements),('ios_simulator',replacements),('wasm_js',replacements)]:
  for qid in ids:
   q=aq[qid];slots=[{'slot':'stem','asset_id':q['image']['asset_id']}] if q['image'] else []
   slots += [{'slot':o['id'],'asset_id':o['image']['asset_id']} for o in q['options'] if o['image']]
   for setting in settings:
    contexts.append({'case_id':f'T03-ART-{target}-{qid}-{setting["id"]}','owner':{'desktop':'10K3','android':'10K2','ios_simulator':'10K4','wasm_js':'10K6'}[target],'review_owners':['10D3','10D4'],'target':target,'question_id':qid,'revision':q['key']['revision'],'setting':setting['id'],'zoom_slots':slots,'faint':qid in faint_questions,'status':'not_run'})
 assert len(sign_ids)==616 and len(contexts)==2920
 engine={'family_id':'T05-ENGINE','owner':'10F1','lengths':list(range(1,71)),'seeds':list(range(20)),'feedback_modes':['IMMEDIATE','AT_END'],'expansion_rule':'For each length, seed, feedback: case_id=T05-ENGINE-<length>-<seed>-<feedback>; all 2,800 cases required, not sampling.','expanded_count':2800,'status':'not_run','independent_oracle':'Compute fixed 7/5/16/32/5 category weights plus five random slots at 70 using exact integer largest-remainder arithmetic and the preserved tie priority VEHICLE, ENVIRONMENT, SAFETY, RULES, PERSONAL, RANDOM; assert quotas before random residual and concept deduplication. Do not call QuizEngine.allocation to calculate expected values. Preserve original rounding contract and boundary fixtures; both modes check exact authored selections/scores.','key_positions':[0,1,2,3],'result_filters':['All','Incorrect','Correct'],'invalid_count_inputs':['','0','71','1.5'],'boundary_fixtures':['insufficient category concepts after quota picks','insufficient unique residual concepts','held item','retired item','wrong manifest/revision','old rounded-fuel snapshot']}
 source_classes=['swedish_legislation','foreign_guidance','research','commercial_shortcut','manufacturer_caution','editorial_arithmetic']
 source_ids=['REF-9f4b74a976fa03fb','REF-4c8313a9f060c341','REF-642e8e5d8ee346e2','REF-0f011d29fdd9c97f','REF-8994a6a11921a063','REF-642e8e5d8ee346e2']
 source_examples=[]
 for name,rid in zip(source_classes,source_ids):
  record=next(r for r in DATA['sources']['references'] if r['id']==rid)
  source_examples.append({'case_class':name,'reference_id':rid,'url':record['url'],'publisher':record['publisher'],'recorded_classifications':record['classifications'],'oracle':locator('sources',f"/references/{DATA['sources']['references'].index(record)}",record),'expected_scope':'Editorial variable-time arithmetic in reaction-20-0.5, with independent distance = speed/3.6 × time; underlying research link is contextual support, not an official arithmetic rule or an invented editorial publisher/URL.' if name=='editorial_arithmetic' else 'Keep exact classification, publisher, evidence dates, model/jurisdiction/claim limits; opening a page is not source freshness verification.','status':'not_run'})
 journeys=[('production-immediate','Setup 1 then production start; select wrong authored choice, cancel leave guard, confirm immediate feedback, finish 0/1; Incorrect expanded review→teaching→source→same review; retain setup count.'),('production-deferred','Same production flow with AT_END; no correct answer/feedback before finish, then exact 0/1 snapshot and return context.'),('library-reader','Search M01-L01, read full lesson, deliberate reveal, next/previous, source return and retained query; intersect Environment to empty state and clear/reset.'),('reference-viewer','Catalogue→B1 exact reference→zoom150/pan/reset/close; return to exact trigger and catalogue; verify background exclusion.'),('recovery','Unknown question, legacy chooser, wrong namespace/invalid page, SIG16–18 exact official action and related teaching; no first-lesson fallback.'),('restart','Same-process preferences survive permitted navigation; fresh process/load restores count70/IMMEDIATE, no saved result/auto-credit.'),('source-callback','Open actual external URL from reader and review; distinguish callback launch from website response; controlled unreachable/offline branch preserves app context.'),('keyboard-accessibility','Tab/reverse Tab/activate/dismiss, neutral semantic names and answer visibility, modal background exclusion, focus return; native supported focus methods separately recorded.'),('talkback','Android representative spoken traversal of reader/reveal/selected question/feedback/zoom/return; retain observations separately from node trees; restore original service setting.')]
 journey_cases=[]
 for target in ['android','desktop','ios_simulator','wasm_js']:
  for name,steps in journeys:
   if name=='talkback' and target!='android':continue
   for setting in settings:
    journey_cases.append({'case_id':f'FLOW-{target}-{name}-{setting["id"]}','target':target,'owner':{'android':'10K2','desktop':'10K3','ios_simulator':'10K4','wasm_js':'10K6'}[target],'setting':setting['id'],'steps_and_expected':steps,'status':'not_run','input':'normal real accepted bank' if target!='desktop' else 'labelled accepted-question production-owner fixture plus separate actual-bank engine/parity; no desktop app exists'})
 # Choose reproducible native examples outside replacement set for renderer diversity.
 representative=['situation-001','situation-017','situation-103','fuel-saving-150-1.5','sign-meaning-A1','sign-recognise-A1','sign-meaning-M17a','sign-recognise-M17a']
 assert set(representative)<=set(aq)
 runtime={'schema_version':1,'status':'prepared_not_executed','settings':settings,'viewport_policy':DATA['scope']['viewport_policy'],'artwork_contexts':contexts,'artwork_context_counts':dict(collections.Counter(c['target'] for c in contexts)),'engine_cartesian_matrix':engine,'production_journeys':journey_cases,'representative_native_questions':[{'question_id':qid,'revision':aq[qid]['key']['revision'],'expected':'Source/classification/key/selected option remains exact; for M17a preserve tiled geometry during zoom without Android canvas crash.','status':'not_run'} for qid in representative], 'representative_sampling_rule':'Each native/browser target must cover all eight named representative IDs in all four settings (32 supplementary contexts per target); exhaustive data/sign checks are not replaced by this sample. Random production flows record actual selected ID/revision/option order; replay failure using a labelled fixed-session harness, never change the production bank.','source_class_matrix':{'classes':source_classes,'frozen_examples':source_examples,'targets':['android','desktop','ios_simulator','wasm_js'],'states':['details_return','external_dispatch','unreachable_return'],'expected_cases':72,'owner':'10C3','selection_rule':'Use the six frozen examples; 10C1 independently reviews classification/claim before runtime. Any justified example replacement gets a new input record. Editorial arithmetic retains its contextual research URL and explicit editorial exercise scope; never invent a source URL. Desktop uses mocked dispatch; physical/speech exclusions remain as in scope.'},'narrow_reflow_matrix':{'targets':['desktop','wasm_js'],'logical_widths':[320,390,1280],'states':['library','dense_reader','image_recognition','review','source','recovery'],'settings':[s['id'] for s in settings],'expected_cases':144,'owner':'10J2','rule':'Keep font family and scaling; measure 220dp image frame and no clipped required copy at narrow width; this is a diagnostic test range, not approved minimum device width.'},'evidence_requirements':['candidate content and runtime fingerprint','build/normal-or-proof executable hash','target/device/tool versions and actual viewport/insets/density','pre-answer and selected inline capture','each image slot fit/zoom150/reset/close and same trigger/selection','expected/observed/assertions plus failures','required assistive method observed, not inferred','restore original device/service/network settings and normal app'],'fixture_limits':'Current CandidateDelivery9JTest historical-candidate coverage must be reconciled to accepted revisions before reuse. A held fixture can prove renderer behaviour only; production journeys must use acceptedPracticeBank9J. No T03/T05/T10 result is passed by this index.'}
 plan=(ROOT/'docs/curriculum/implementation-plan.md').read_text();section=plan.split('## 10. Verify the finished app',1)[1].split('## Content principle',1)[0];task_ids=re.findall(r'^#### (10[A-M]\d+)\.',section,re.M)
 deps={t:['10A3'] for t in task_ids};deps.update({'10A1':[],'10A2':['10A1'],'10A3':['10A1','10A2'],'10B14':[f'10B{i}' for i in range(1,14)],'10C2':['10C1'],'10C3':['10C1','10K2','10K3','10K4','10K6'],'10D1':[f'10E{i}' for i in range(2,15)]+['10B13'],'10D2':['10D1'],'10D3':['10D2','10K2','10K3','10K4','10K6'],'10D4':['10D1','10K2','10K3','10K4','10K6'],'10E18':[f'10E{i}' for i in range(1,18)],'10F1':['10A3','10E1'],'10F2':['10F1'],'10F3':['10F2'],'10F4':['10F1','10F2','10F3','10K2','10K3','10K4','10K6'],'10G1':['10A3','10B1'],'10G2':['10G1'],'10G3':['10G1','10G2','10C3'],'10H1':['10A3','10B1','10G1'],'10H2':['10H1','10G2','10K2','10K3','10K4','10K6'],'10H3':['10H1','10H2','10F3'],'10I1':['10B14','10H1'],'10I2':['10I1'],'10I3':['10I2','10E18'],'10J2':['10J1','10K2','10K3','10K4','10K6'],'10J3':['10J1','10K2','10K3','10K4','10K6'],'10K1':['10B14','10E18','10F1','10F2','10F3','10G1','10G2'],'10K7':[t for t in task_ids if re.match(r'10[C-J]',t)]+[f'10K{i}' for i in range(1,7)],'10L1':['10A3'],'10L2':['10L1'],'10L3':['10L2'],'10M1':['10K7','10L3'],'10M2':['10M1']})
 for i in range(2,15):deps[f'10E{i}']=['10E1','10B13']
 for i in range(15,18):deps[f'10E{i}']=['10E1']
 for i in range(2,7):deps[f'10K{i}']=['10K1']
 # Validate completion graph, separating preparation from platform evidence closure.
 order=[];pending=dict(deps)
 while pending:
  ready=[k for k,v in pending.items() if all(d in order for d in v)]
  assert ready,('dependency cycle',pending)
  for k in ready:order.append(k);del pending[k]
 index={'schema_version':1,'task':'10A3','status':'prepared_not_executed','candidate':json.loads((BASE/'10A1/results.json').read_text())['candidate'],'source_fingerprint':json.loads((BASE/'10A1/results.json').read_text())['source_fingerprint'], 'oracles':{k:{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for k,p in PATHS.items()},'gate_clauses':clauses,'original_coverage_crosswalk':coverage,'task_dependencies':deps,'valid_completion_order':order,'supporting_file_oracles':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in ['docs/curriculum/app-design-review.md','docs/curriculum/app-design-spec.md','docs/curriculum/app-design/faint-assets-v1/review.md','docs/curriculum/app-migration/assessment-coverage-briefs.md','docs/curriculum/app-migration/implementation-backlog.md','docs/curriculum/pdf-production/final-review/screen-release.json']],'platform_preparation_rule':'10C3/10D3/10D4/10F4/10G3/10H2/10J2/10J3 can prepare their cases before 10K, but complete only after fresh 10K evidence. 10K uses prepared cases without requiring their final closure. 10L is a conditional fix loop; no-fix disposition permitted. Changes invalidate affected prior results.', 'case_files':{'data-cases.json':'exhaustive content/source/route/state/copy families','question-batches.json':'all 1,000 IDs, exact 12 rewrite batches and 19 replacement pairs, distractors and faint slots','runtime-matrix.json':'explicit high-risk contexts plus fully specified Cartesian engine/source/reflow/journey sets'},'future_case_status':'not_run except four explicit conditional state cases and scope exclusions; no functional pass inferred','evidence_contract':{'status_values':['pass','fail','blocked','not_run','excluded_by_policy','conditional_future_scope'],'required_fields':['case_id','candidate_content_identity','runtime_fingerprint','input_refs','command_or_reproduction_steps','expected','observed','status','environment','attachments_and_hashes','limitations','defect_id_if_failed'],'failure_rule':'Required fail/blocked/not_run prevents affected gate closure. Retain original evidence and link fresh superseding results after a fix.'}}
 return {'verification-case-index.json':index,'data-cases.json':{'schema_version':1,'status':'prepared_not_executed','families':families},'question-batches.json':question_data,'runtime-matrix.json':runtime}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();outputs=build()
 for name,data in outputs.items():
  path=OUT/name;encoded=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
  if args.check:assert path.read_text()==encoded,f'{name} differs from frozen inputs/recipe'
  else:path.write_text(encoded)
 print(json.dumps({'status':'pass','mode':'check' if args.check else 'prepare','gate_clauses':len(outputs['verification-case-index.json']['gate_clauses']),'original_coverage_families':len(outputs['verification-case-index.json']['original_coverage_crosswalk']),'data_cases':sum(len(f['members']) for f in outputs['data-cases.json']['families']),'question_cases':len(outputs['question-batches.json']['all_question_cases']),'sign_batches':len(outputs['question-batches.json']['sign_rewrite_batches']),'replacement_pairs':len(outputs['question-batches.json']['replacement_pairs']),'artwork_contexts':len(outputs['runtime-matrix.json']['artwork_contexts']),'production_journeys':len(outputs['runtime-matrix.json']['production_journeys']),'task_dependencies':len(outputs['verification-case-index.json']['task_dependencies']),'functional_checks_run':0},indent=2))
if __name__=='__main__':main()
