"""Check preparation coverage/locators; no functional app verification is performed."""
import hashlib
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent

def read(name):return json.loads((OUT/name).read_text())
def canon(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
index=read('verification-case-index.json');data=read('data-cases.json');q=read('question-batches.json');runtime=read('runtime-matrix.json')
checks=[]
def check(id,expected,observed,evidence):
 checks.append({'id':id,'status':'pass' if expected==observed else 'fail','expected':expected,'observed':observed,'evidence':evidence})
inputs={}
for alias,r in index['oracles'].items():
 path=ROOT/r['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'],alias
 inputs[alias]=json.loads(path.read_text())
for row in index['supporting_file_oracles']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
locators=0
case_ids=[]
def walk(v):
 global locators
 if isinstance(v,dict):
  if isinstance(v.get('oracle'),str) and 'pointer' in v and 'record_sha256' in v:
   doc=inputs[v['oracle']]
   for part in v['pointer'].strip('/').split('/') if v['pointer'] else []:
    part=part.replace('~1','/').replace('~0','~');doc=doc[int(part)] if isinstance(doc,list) else doc[part]
   assert canon(doc)==v['record_sha256'],v
   locators+=1
  if 'case_id' in v:
   assert v['status'] in ['not_run','conditional_future_scope'],v['case_id']
   case_ids.append(v['case_id'])
  for c in v.values():walk(c)
 elif isinstance(v,list):
  for c in v:walk(c)
for obj in [index,data,q,runtime]:walk(obj)
check('10A3-UNIQUE-CASES',len(case_ids),len(set(case_ids)),'verification-case-index.json; data-cases.json; question-batches.json; runtime-matrix.json')
check('10A3-GATES',{f'T{i:02d}' for i in range(1,11)}=={c['gate'] for c in index['gate_clauses']},True,'verification-case-index.json#/gate_clauses')
check('10A3-COVERAGE-FAMILIES',set(inputs['backlog']['coverage'])=={c['original_family'] for c in index['original_coverage_crosswalk']},True,'verification-case-index.json#/original_coverage_crosswalk')
check('10A3-QUESTIONS',1000,len({c['question_id'] for c in q['all_question_cases']}),'question-batches.json#/all_question_cases')
check('10A3-REWRITE-BATCHES',[50]*11+[28],[b['count'] for b in q['sign_rewrite_batches']],'question-batches.json#/sign_rewrite_batches')
check('10A3-REPLACEMENT-PAIRS',[2]*19,[b['count'] for b in q['replacement_pairs']],'question-batches.json#/replacement_pairs')
check('10A3-DISTRACTORS',134,len(set(q['distractor_change_ids'])),'question-batches.json#/distractor_change_ids')
check('10A3-FAINT',[12,24,24],[len(q['faint_asset_ids']),len(q['faint_question_ids']),len(q['faint_slot_bindings'])],'question-batches.json#/faint_slot_bindings')
families={f['id']:f for f in data['families']}
for name,count in [('registry_curriculum_nodes',88),('registry_source_destinations',116),('registry_sign_entries',400),('registry_supporting_destinations',519),('reference_groups',24),('artwork_bindings',484),('question_source_urls',404),('chapter_aliases',39),('legacy_page_aliases',361),('unused_topic_routes',178),('sign_routes',343),('question_routes',1000),('navigation_routes',8),('entry_point_rules',12),('state_contracts',22),('reading_edges',60),('category_routes',5),('lesson_category_tags',40),('copy_rules',14),('approved_previews',12)]:
 check('10A3-FAMILY-'+name,count,len(families[name]['members']),f"data-cases.json#/families/{list(families).index(name)}")
check('10A3-CONDITIONAL',4,sum(c['status']=='conditional_future_scope' for c in families['state_contracts']['members']),f"data-cases.json#/families/{list(families).index('state_contracts')}")
check('10A3-ARTWORK-MATRIX',{'desktop':2464,'android':152,'ios_simulator':152,'wasm_js':152},dict(Counter(c['target'] for c in runtime['artwork_contexts'])),'runtime-matrix.json#/artwork_contexts')
check('10A3-ENGINE-MATRIX',2800,len(runtime['engine_cartesian_matrix']['lengths'])*len(runtime['engine_cartesian_matrix']['seeds'])*len(runtime['engine_cartesian_matrix']['feedback_modes']),'runtime-matrix.json#/engine_cartesian_matrix')
check('10A3-SOURCE-EXAMPLES',6,len(runtime['source_class_matrix']['frozen_examples']),'runtime-matrix.json#/source_class_matrix')
order=index['valid_completion_order'];deps=index['task_dependencies'];assert len(order)==len(deps)==70
check('10A3-DEPENDENCIES',True,all(order.index(d)<order.index(t) for t,ds in deps.items() for d in ds),'verification-case-index.json#/task_dependencies')
for c in index['gate_clauses']:
 assert all(o in deps for o in c['owners'])
for f in data['families']:
 assert f['owner']=='per_member' or f['owner'] in deps
 for c in f['members']:
  if 'owner' in c:assert c['owner'] in deps
check('10A3-ORACLE-LOCATORS',True,locators>0,'all hash-bound oracle/pointer records resolve to retained independent contracts or explicitly labelled candidate snapshots')
result={'task':'10A3','status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','candidate':index['candidate'],'checks':checks,'counts':{'gate_clauses':len(index['gate_clauses']),'original_coverage_families':len(index['original_coverage_crosswalk']),'data_cases':sum(len(f['members']) for f in data['families']),'question_cases':1000,'explicit_case_ids':len(case_ids),'verified_oracle_locators':locators,'artwork_contexts':2920,'engine_cartesian_cases':2800,'production_journey_contexts':len(runtime['production_journeys']),'additional_representative_contexts':96,'source_contexts':72,'narrow_reflow_contexts':144,'dependency_nodes':70},'all_functional_gates':'not_run; preparation integrity only','known_open_preparation_blockers':[]}
(OUT/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':result['status'],'preparation_checks':len(checks),'counts':result['counts']},indent=2));raise SystemExit(result['status']!='pass')
