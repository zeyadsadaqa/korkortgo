"""Integrity/completeness check, deliberately distinct from T06 external-target acceptance."""
import collections,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());BASE=Path(__file__).resolve().parent.parent;HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(name,ok):checks.append({'name':name,'status':'pass' if ok else 'fail'})
a=read(BASE/'10G1/complete-alias-results.json');b=read(BASE/'10G2/route-edge-results.json');c=read(HERE/'unavailable-sign-results.json');r=read(HERE/'results.json');ledger=read(HERE/'defects.json');m=read(ROOT/'docs/curriculum/app-migration/link-and-progress-map.json');manifest=read(ROOT/'content/accepted-content-manifest.json');compiled=read(BASE/'10G1/compiled-alias-observations.json');raw=read(ROOT/'content/legacy-aliases.json')
expected={'chapter_aliases':39,'legacy_page_aliases':361,'unused_topic_routes':178,'sign_routes':343,'question_routes':1000}
check('Exact accepted identity/manifest unchanged',a['identity']==b['identity']==c['identity']==manifest['identity'] and sha(ROOT/'content/accepted-content-manifest.json')=='ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21')
check('All1921 exact typed records/family counts/no production tombstones',len(a['aliases'])==len(compiled['aliases'])==len(raw['aliases'])==1921 and a['counts']['families']==expected and collections.Counter(x['family'] for x in a['aliases'])==expected and compiled['tombstones']==raw['tombstones']==m['production_tombstones']==[])
check('8888 alias/registry/relationship oracle checks pass',a['status']=='pass' and len(a['checks'])==8888 and a['counts']['failed']==0 and all(x['status']=='pass' for x in a['checks']))
for row in a['aliases']:
 check('Alias '+str(row['lookup']),row['status']=='pass' and row['actual']['type']==row['expected']['type'] and row['source_locator'].startswith('json:/'+row['family']+'/'))
compiledAliases={json.dumps(x['lookup'],sort_keys=True):x for x in compiled['aliases']};rawAliases={json.dumps(x['lookup'],sort_keys=True):x for x in raw['aliases']}
check('Fresh full alias contract/provenance matches accepted JSON',len(compiledAliases)==len(rawAliases)==1921 and all(compiledAliases[k]['origin']==v['origin'] and compiledAliases[k]['declared_outcome']==v['outcome'] and v['origin']['file']['sha256']==sha(ROOT/v['origin']['file']['path']) for k,v in rawAliases.items()))
accepted={q['key']['question_id']:q for q in read(ROOT/'content/accepted-assessment-questions.json')['questions']}
for row in a['questions']:
 q=accepted[row['key']['question_id']];check('Question '+q['key']['question_id'],row['status']=='pass' and row['key']==q['key'] and row['relationship']==q['relationship'] and row['actual']==row['with_page_context'])
check('All1000 question routes exactly once',len(a['questions'])==len({x['key']['question_id'] for x in a['questions']})==1000 and {x['key']['question_id'] for x in a['questions']}==set(accepted))
check('Every9 frozen example/10 policies retained',len(b['examples'])==9 and {e['example_id'] for e in b['examples']}=={e['id'] for e in m['examples']} and set(b['policy_evidence'])==set(m['resolution_policy']) and all(e['status']=='pass' for e in b['examples']))
check('56 independent edge reconciliation checks pass',b['status']=='pass' and b['counts']['failed']==0 and len(b['checks'])==56 and all(x['status']=='pass' for x in b['checks']))
edge=read(BASE/'10G2/compiled-edge-observations.json');ui=read(BASE/'10G2/recovery-action-observations.json')
check('Typed45 edges/noninteger5/blank2, chooser4/shared7 and synthetic3 distinct',len(edge['cases'])==45 and len(edge['noninteger_boundaries'])==5 and len(edge['construction_boundaries'])==2 and len(edge['chooser_actions'])==4 and len(ui['actions'])==7 and len(ui['retirement_fixtures'])==3 and all(x['status']=='pass' for x in ui['actions']))
examples={e['example_id']:e['actual'] for e in b['examples']};check('Page46 context yields different exact lessons',examples['same-old-page-a']['target']['content_id']=='M04-L03' and examples['same-old-page-b']['target']['content_id']=='M04-L01')
check('Frozen host entry source hashes still match',all(sha(ROOT/f['path'])==f['sha256'] for f in b['entry_source_hashes']))
check('Three explicit unavailable signals/exact URLs, six attempt callbacks',len(c['signals'])==3 and {x['code'] for x in c['signals']}=={'SIG16','SIG17','SIG18'} and c['counts']['shared_uri_attempts']==6 and len(c['checks'])==15 and c['counts']['failed']==0 and all(x['status']=='pass' for x in c['checks']))
for s in c['signals']:
 policy=next(x for x in m['unresolved_destinations'] if x['legacy_code']==s['code']);check(s['code']+' exact missing-entry scope and URI',s['status']=='pass_shared_scope' and s['policy']=='unavailable_exact_entry' and s['actual_resolution']['type']=='unavailable' and s['official_reference']['url']==policy['legacy_external_url'] and s['attempted_urls']==[policy['legacy_external_url']]*2 and s['related_action']=={'content_id':'M03-L02','block_id':None})
check('Twelve target cases remain truthful pending observations',len(c['required_target_cases'])==12 and {(x['target'],x['legacy_code']) for x in c['required_target_cases']}=={(t,code) for t in ['android','desktop','ios_simulator','wasm_js'] for code in ['SIG16','SIG17','SIG18']} and all(x['status']=='not_run_pending_10K' and x['observation'] is None for x in c['required_target_cases']) and c['counts']['fresh_target_uri_passes']==0 and r['T06']=='open')
check('Historical10C3 source evidence unchanged',sha(BASE/'10C3/source-runtime-results.json')==c['prior_source_runtime_evidence']['sha256'])
check('Eleven inherited findings remain open; no new product finding',len(ledger['inherited_open_product_defects'])==len(ledger['open_product_defects'])==11 and ledger['findings']==r['new_product_findings']==[] and any(x['id']=='BLOCK-10G-EXTERNAL-TARGETS' and x['status']=='open' for x in ledger['open_verification_blockers']))
for task,classes in [('10G1',['Alias10GTest']),('10G2',['Edges10GTest','RecoveryActions10GTest']),('10G3',['UnavailableSignals10GTest'])]:
 p=BASE/task
 for cls in classes:
  x=ET.parse(p/f'TEST-se.korkort.{cls}.xml').getroot();check(task+' actual JVM '+cls,x.get('tests')=='1' and x.get('failures')==x.get('errors')=='0')
 for cmd in read(p/'commands.json'):check(task+' command log '+cmd['log'],cmd['exit_code']==0 and sha(p/cmd['log'])==cmd['log_sha256'])
 if task!='10G1':
  index=read(p/'capture-index.json');check(task+' all logical captures hash-resolve',index['logical_count']==len(index['captures']) and index['stored_count']==len({x['stored_path'] for x in index['captures']}) and all(sha(p/x['stored_path'])==x['sha256'] for x in index['captures']))
 if '--check-manifests' in sys.argv:
  for f in read(p/'artifacts.json'):check(task+' artifact '+f['path'],sha(p/f['path'])==f['sha256'])
base=read(HERE/'baseline-exit.json');check('Protected source/accepted/historical inputs unchanged',base['status']=='pass' and base['changed_baseline_inputs']==[] and base['historical_receipts_modified'] is False)
report={'status':'pass' if all(x['status']=='pass' for x in checks) else 'fail','meaning':'Evidence integrity only; target external action acceptance remains open.','T06':'open','counts':{'checks':len(checks),'failed':sum(x['status']=='fail' for x in checks)},'checks':checks}
if '--check-manifests' not in sys.argv:(HERE/'evidence-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}|{'failures':[x for x in checks if x['status']=='fail']},indent=2));sys.exit(0 if report['status']=='pass' else 1)
