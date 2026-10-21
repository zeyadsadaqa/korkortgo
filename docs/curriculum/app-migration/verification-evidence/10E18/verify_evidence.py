"""Verify evidence completeness and bindings; a pass is not T04 closure."""
import collections,gzip,hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());BASE=Path(__file__).resolve().parent.parent;HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();digest=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();checks=[]
def check(name,ok):checks.append({'name':name,'status':'pass' if ok else 'fail'})
def pointer(path,loc):
 v=read(path)
 for k in loc.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
 return v
r=read(HERE/'complete-question-review.json');bank=read(ROOT/'content/accepted-assessment-questions.json')['questions'];byid={q['key']['question_id']:q for q in bank};frozen=read(BASE/'10A3/question-batches.json');compiled=read(BASE/'10E1/compiled-question-contracts.json');audit=read(BASE/'10E1/question-disposition-audit.json');ledger=read(HERE/'defects.json');d1=read(HERE/'10D1-semantic-reconciliation.json')
check('Complete original ordered ID accounting',[q['question_id'] for q in r['questions']]==[q['key']['question_id'] for q in bank] and len(bank)==len({q['question_id'] for q in r['questions']})==1000)
check('Exact 500 concepts / disposition totals',len({q['concept_id'] for q in bank})==500 and collections.Counter(q['disposition'] for q in r['questions'])=={'retain':336,'rewrite':626,'replace':38})
check('Exact original frozen owner membership',collections.Counter(q['owner'] for q in r['questions'])==frozen['partition'])
check('Actual full compiled records and accepted identity equal JSON',compiled['questions']==bank and compiled['identity']==read(ROOT/'content/accepted-content-manifest.json')['identity'])
check('Fresh JVM exporter test passed',all(ET.parse(BASE/'10E1/TEST-se.korkort.QuestionContract10ETest.xml').getroot().get(k)==v for k,v in {'tests':'1','failures':'0','errors':'0','skipped':'0'}.items()))
check('9340 independent generic checks and336 unchanged retained payloads',audit['counts']['checks']==9340 and audit['counts']['failed']==0 and len(read(BASE/'10E1/retained-payload-diff.json')['questions'])==336 and all(q['status']=='pass' and q['original_payload_sha256']==q['accepted_projection_sha256'] for q in read(BASE/'10E1/retained-payload-diff.json')['questions']))
for q in r['questions']:
 path,loc=q['independent_disposition_review'].split('#');v=pointer((HERE/path).resolve(),loc)
 check(q['question_id']+' exact independent record and current snapshot',v['question_id']==q['question_id'] and v['status']==q['status'] and q['revision']==byid[q['question_id']]['key']['revision'] and digest(byid[q['question_id']])==q['accepted_snapshot_sha256'])
check('970 scoped passes and30 open description contexts',collections.Counter(q['status'] for q in r['questions'])=={'pass':970,'open_related_asset_description':30} and r['T04']=='open')
allcodes=[];changed=[];assigned=[]
for i in range(2,15):
 task=f'10E{i}';packet=read(BASE/task/'source-review-packet.json');notes=read(BASE/task/'reviewer-notes.json');allcodes.extend(p['code'] for p in packet)
 name=f'batch-{i-1:02}-question-review.json' if i<14 else 'replacement-question-review.json';rev=read(BASE/task/name)
 check(task+' exact notes, artwork sheet and membership',set(notes['notes'])=={p['code'] for p in packet} and (BASE/task/'reviewed-assets-1.png').exists() and len(rev['questions'])==frozen['partition'][task])
 for p in packet:
  src=p['official_source'];path=ROOT/src['file'];data=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
  check(task+' '+p['code']+' dated primary-source bytes',hashlib.sha256(data).hexdigest()==src['sha256'])
 for q in rev['questions']:
  assigned.append(q['question_id']);changed.extend([q['question_id']] if q['distractor_change'] else [])
  check(task+' '+q['question_id']+' semantic record and exact variant impacts',not q['failures'] and q['assessment_wording_key_feedback_status']=='pass' and len(q['options'])==4 and set(q['related_description_findings'])=={f['id'] for f in ledger['findings'] if q['question_id'] in f['affected_ids_files']})
check('308 exact target assets inspected;616 sign IDs;134 overlapping changes',len(allcodes)==len(set(allcodes))==308 and len(assigned)==len(set(assigned))==616 and set(changed)==set(frozen['distractor_change_ids']) and len(changed)==134)
check('10D1 pending work reconciled without closing T03',len(d1['questions'])==616 and d1['counts']['description_cases_open']==30 and d1['historical_10D_receipts_unchanged'] is True)
for task,name,count in [('10E15','scenario-review.json',8),('10E16','load-calculation-audit.json',30),('10E17','fuel-calculation-audit.json',4),('10E18','unit-wording-review.json',6)]:
 a=read(BASE/task/name);check(task+' all independent checks pass',a['counts']['questions']==len(a['questions'])==count and a['counts']['failed']==0 and all(all(q['checks'].values()) for q in a['questions']))
check('All8 scenarios fresh scoped primary review with separate10C2 addendum',len(read(BASE/'10E15/checked-claims.json')['questions'])==8 and len(read(BASE/'10E15/primary-fetch-observations.json')['sources'])==10)
check('Known unit residual explicit:3 questions,4 locations',len(r['known_approved_scope_limitation']['questions'])==3 and sum(len(q['locations']) for q in r['known_approved_scope_limitation']['questions'])==4)
check('Seven inherited and three newP2 defects remain open',len(ledger['inherited_open_product_defects'])==7 and len(ledger['open_product_defects'])==10 and len(ledger['findings'])==3 and all(f['severity']=='P2' and f['state']=='open' and all(k in f for k in ledger['required_record_fields']) for f in ledger['findings']))
check('Executed semantic dependency distinguished from platform blocker',ledger['resolved_verification_dependencies'][0]['status']=='executed_with_findings' and [x['id'] for x in ledger['open_verification_blockers']]==['BLOCK-10D-PLATFORM'])
baseline=read(HERE/'baseline-exit.json');check('Accepted inputs and historical receipts unchanged',baseline['status']=='pass' and not baseline['changed_baseline_inputs'] and not baseline['historical_receipts_modified'] and sha(ROOT/'content/accepted-content-manifest.json')==r['manifest_sha256']=='ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21')
for i in range(1,19):
 task=f'10E{i}'
 for c in read(BASE/task/'commands.json'):check(task+' retained command log '+c['log'],c['exit_code']==0 and sha(BASE/task/c['log'])==c['log_sha256'])
 if '--check-manifests' in sys.argv:
  for a in read(BASE/task/'artifacts.json'):check(task+' artifact '+a['path'],sha(BASE/task/a['path'])==a['sha256'])
report={'task':'10E evidence integrity','status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','T04':'open','counts':{'checks':len(checks),'failed':sum(c['status']=='fail' for c in checks)},'checks':checks}
if '--check-manifests' not in sys.argv:(HERE/'evidence-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'T04':'open','counts':report['counts'],'failures':[c for c in checks if c['status']=='fail']},indent=2));sys.exit(0 if report['status']=='pass' else 1)
