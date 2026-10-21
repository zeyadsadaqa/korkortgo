"""Integrity/scope verification; success never closes the retained T07 failure."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/curriculum/app-migration/verification-evidence'
read=lambda p:json.loads(p.read_text());checks=[]
def check(label,test):
 checks.append({'check':label,'pass':bool(test)})
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
frozen=read(ROOT/'docs/curriculum/app-migration/link-and-progress-map.json')
h1=read(BASE/'10H1/results.json');h2=read(BASE/'10H2/guard-recovery-results.json');h3=read(BASE/'10H3/state-contract-results.json')
identity=h3['identity']
check('all compiled/frozen checks pass',len(h1['checks'])==2661 and all(c['pass'] for c in h1['checks']))
check('128 transitions and60nodes',h1['totals']['transitions']==128 and h1['totals']['nodes']==60)
check('118 edges two boundaries',h1['totals']['edges']==118 and h1['totals']['null_boundaries']==2)
check('all12 entry points exact frozen rules',[r['rule'] for r in h1['entry_points']]==[r['rule'] for r in frozen['entry_point_rules']])
check('sign return remains productfailure',h1['shared_sign_return']['status']=='fail' and not h1['shared_sign_return']['returned_to_origin'])
check('same accepted identity',h2['identity']==identity==read(BASE/'10H1/navigation-transition-results.json')['identity'])
check('18 plus4 exactcontracts',len(h3['contracts'])==22 and sum(c['status']=='pass_accepted_model_scope' for c in h3['contracts'])==18 and sum(c['status']=='conditional_future_scope' for c in h3['contracts'])==4)
for i,c in enumerate(h3['contracts']):check(c['id']+' frozenfield/rule',all(c[k]==frozen['state_rules'][i][k] for k in ['field','baseline','migration_rule']))
check('defaults retained',h3['defaults']=={'count_text':'70','feedback':'immediate'} and not h3['persistence_added'])
check('fresh owner exactdefaults',len(h3['fresh_owner']['runs'])==2 and all(r['fresh_count']=='70' and r['fresh_feedback']=='immediate' and not r['session_auto_started'] for r in h3['fresh_owner']['runs']))
journeys=h3['production_owner_journeys']['journeys']
check('both acceptedproductionfeedbackjourneys',len(journeys)==2 and {j['mode'] for j in journeys}=={'immediate','at_end'} and all(j['bank_count']==1000 and j['held_count']==0 and len(j['questions'])==3 and j['status']=='pass' for j in journeys))
check('allrecordedH2modelcasespass',all(r['status']=='pass' for r in h2['cases']))
check('bothH2productionguards',len(read(BASE/'10H2/shared-production-guard-results.json')['cases'])==2)
case_map=read(BASE/'10H3/case-reconciliation.json')
prepared=[m['case_id'] for family in read(BASE/'10A3/data-cases.json')['families'] if family['gate']=='T07' for m in family['members']]
check('110preparedcaseIDsfullyreconciled',[r['case_id'] for r in case_map['prepared_cases']]==prepared and len(prepared)==110)
defects=read(BASE/'10H3/defects.json');check('one new finding plus11inherited',len(defects['findings'])==1 and len(defects['open_product_defects'])==12 and defects['findings'][0]['id']=='DEF-10H-001')
check('T07 remainsopen',case_map['status']=='open' and any(b['id']=='BLOCK-10H-NATIVE' for b in defects['open_verification_blockers']))
for name in ['10H1/baseline-entry.json','10H3/baseline-exit.json']:
 baseline=read(BASE/name);check(name,baseline['status']=='pass' and not baseline['changed_baseline_inputs'] and not baseline['historical_receipts_modified'])
total=failures=0
for n in range(1,4):
 p=BASE/f'10H{n}'
 for f in p.glob('TEST-*.xml'):
  x=ET.parse(f).getroot();total+=int(x.get('tests'));failures+=int(x.get('failures'))
  check(str(f.relative_to(BASE)),int(x.get('failures'))==(1 if 'ReadingSignReturn10HTest' in f.name else 0) and int(x.get('errors'))==0)
 for row in read(p/'capture-index.json')['captures']:check(str(p.name)+'/'+row['path'],sha(p/row.get('stored_path',row['path']))==row['sha256'])
 for row in read(p/'environment.json')['proof_classes']:check('compiled '+row['path'],sha(ROOT/row['path'])==row['sha256'])
 if '--check-manifests' in sys.argv:
  rows=read(p/'artifacts.json');expected={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name!='artifacts.json' and '__pycache__' not in f.parts}
  check(p.name+' complete manifest',{r['path'] for r in rows}==expected)
  for row in rows:check(p.name+'/'+row['path'],sha(p/row['path'])==row['sha256'] and (p/row['path']).stat().st_size==row['bytes'])
check('24finalmethods23pass1productfailure',total==24 and failures==1)
result={'status':'pass_evidence_integrity_T07_still_open' if all(c['pass'] for c in checks) else 'fail','checks':checks,'totals':{'integrity_checks':len(checks),'final_test_methods':total,'passing':total-failures,'expected_product_failures':failures},'not_gate_closure':True}
if '--check-manifests' not in sys.argv:(BASE/'10H3/evidence-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
for c in checks:
 if not c['pass']:print('FAILED',c['check'])
assert all(c['pass'] for c in checks)
