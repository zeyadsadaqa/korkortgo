"""Independent frozen-registry/content comparison of fresh compiled and shared UI observations."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
actual=read(HERE/'compiled-teaching.json');authored=read(ROOT/'content/curriculum.json');registry=read(ROOT/'docs/curriculum/app-migration/curriculum-map.json');frozen=read(ROOT/'docs/curriculum/app-migration/link-and-progress-map.json')
checks=[]
def check(label,test):checks.append({'check':label,'pass':bool(test)})
for key in ['modules','documents','reference_groups','reading_order']:
 check('full compiled/authored '+key,actual[key]==authored[key])
check('modules frozenregistry',actual['modules']==registry['modules'])
check('reading frozen7E',actual['reading_order']==frozen['reading_order'])
for node in registry['curriculum_nodes']:
 doc=next(d for d in actual['documents']+actual['reference_groups'] if d['id']==node['id'])
 check('registered '+node['id'],doc['title']==node['title'] and doc['order']==node['order'])
routes=read(HERE/'shared-route-observations.json')['routes']
expected_ids=[d['id'] for d in authored['documents']]+[g['id'] for g in authored['reference_groups']]
check('everyactualrouteexactlyonce',len(routes)==len(expected_ids)==115 and {r['id'] for r in routes}==set(expected_ids))
for r in routes:
 check('reachable '+r['id'],r['status']=='pass_shared_semantics')
 if r['entry']=='library button':check('exact typed callback '+r['id'],r['typed_callback_target']=={'content_id':r['id'],'block_id':None})
reader=read(HERE/'shared-reader-observations.json');expectedblocks=[(d['id'],b['metadata']['id']) for d in authored['documents'] for b in d['body_blocks']]
check('all91readerdocuments',[d['id'] for d in reader['documents']]==[d['id'] for d in authored['documents']])
check('alltopblocksordered',[(r['document_id'],r['block_id']) for r in reader['blocks']]==expectedblocks)
for r in reader['blocks']:check('complete sharedblock '+r['block_id'],r['status']=='pass' and not r['premature_answer_pane'] and r['answer_collapsed'] is not False)
result={'task':'10I1','status':'pass_compiled_and_shared_scope' if all(c['pass'] for c in checks) else 'fail','identity':actual['identity'],'totals':{'modules':10,'lessons':40,'reviews':10,'appendices':4,'reference_groups':24,'additional_front_matter':27,'documents':len(actual['documents']),'routes':len(routes),'top_level_blocks':len(expectedblocks),'knowledge_checks':sum(r['answer_collapsed'] is not None for r in reader['blocks']),'checks':len(checks)},'checks':checks,'input_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'content/curriculum.json',ROOT/'docs/curriculum/app-migration/curriculum-map.json',ROOT/'docs/curriculum/app-migration/link-and-progress-map.json']},'dependencies':{'10B1–10B14':'previous complete source/PDF/import/render parity retained; fresh10I checks do not rewrite it','10H1':'all128 transitions,118edges andtwo boundaries; DEF-10H-001 still open'},'limits':['Shared semantic reachability does not establish native pointer hit testing or exhaustive visual nontruncation.','Representative narrow table/crop/reveal tests are supplemental; fresh actual-target font/theme/native observations remain10K.','Inherited reference-catalogue return defect does not prevent forward teaching discovery, but remains required for T07 closure.']}
(HERE/'teaching-reachability-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ['status','totals']}))
for c in checks:
 if not c['pass']:print('FAILED',c['check'])
assert all(c['pass'] for c in checks)
