"""Check evidence accounting and honesty of pending statuses; this does not close T02."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());BASE=ROOT/'docs/curriculum/app-migration/verification-evidence';HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok):
 checks.append({'name':name,'status':'pass' if ok else 'fail'})
a=read(BASE/'10C1/source-binding-audit.json');b=read(BASE/'10C2/checked-claims.json');c=read(HERE/'source-runtime-results.json');d=read(HERE/'defects.json');baseline=read(HERE/'baseline-exit.json')
check('C1 exact count accounting with six explicit classification failures',a['counts']=={'references':519,'canonical_sources':116,'original_question_URLs':404,'questions':1000,'uses':8166,'checks':19121,'passed':19115,'failed':6} and len([x for x in a['checks'] if x['status']=='fail'])==6)
check('Every prepared T02 data case has actual linked execution checks',len(a['prepared_cases'])==1039 and all(x['evidence_checks'] for x in a['prepared_cases']))
check('C2 every selected claim explicitly supported, defective or blocked',len(b['claims'])==29 and all(x['checked_on']=='2026-10-20' and x['status'] in ['supported_with_scope','defect_confirmed','blocked_unreachable'] for x in b['claims']))
check('C2 actual counts match stated summary',all(sum(x['status']==k for x in b['claims'])==v for k,v in b['counts'].items() if k!='selected'))
check('All three briefs retain exact coverage and future unscored boundary',len(b['briefs'])==3 and all(x['coverage_matches'] and x['status']=='pass' for x in b['briefs']) and b['briefs'][1]['related_question_ids']==['situation-053'])
check('Editorial arithmetic independently recomputed',next(x for x in b['claims'] if x['case_id']=='10C2-CLAIM-22')['independent_arithmetic']['numeric_check'])
check('C3 exactly 72 uniquely identified prepared cases',len(c['cases'])==len({x['case_id'] for x in c['cases']})==72)
check('Only actual shared desktop matrix cases pass; remaining 54 pending 10K',sum(x['status']=='pass_shared_desktop_harness' and x['target']=='desktop' and x['observation']['status']=='pass' for x in c['cases'])==18 and sum(x['status']=='not_run_pending_10K' and x['observation'] is None for x in c['cases'])==54 and c['status']=='partial_pending_10K')
check('Three actual supplemental recovery/return observations pass',len(c['supplemental_observations'])==3 and all(x['status']=='pass' for x in c['supplemental_observations']))
for task,name in [('10C1','SourceBindingVerification10CTest'),('10C3','SourceRuntimeVerification10CTest')]:
 xml=ET.parse(BASE/task/f'TEST-se.korkort.{name}.xml').getroot();check(task+' fresh JVM execution receipt passes',xml.attrib['tests']=='1' and xml.attrib['failures']==xml.attrib['errors']=='0')
check('Six open source defects and two explicit closure blockers retained',len(d['open_product_defects'])==len(d['findings'])==6 and len(d['open_verification_blockers'])==2 and all(x['state']=='open' and all(k in x for k in d['required_record_fields']) for x in d['findings']))
check('Candidate identity unchanged',sha(ROOT/'content/accepted-content-manifest.json')==a['candidate_manifest_sha256']==c['candidate_manifest_sha256']=='ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21')
check('Baseline entry/exit prove no input or historical receipt drift',baseline['status']=='pass' and baseline['changed_baseline_inputs']==[] and baseline['historical_receipts_modified'] is False)
for task in ['10C1','10C2','10C3']:
 for r in read(BASE/task/'commands.json'):
  check(task+' command/log receipt '+r['log'],sha(BASE/task/r['log'])==r['log_sha256'])
 if '--check-manifests' in sys.argv:
  for r in read(BASE/task/'artifacts.json'):check(task+' artifact '+r['path'],sha(BASE/task/r['path'])==r['sha256'])
report={'task':'10C evidence accounting','status':'pass' if all(x['status']=='pass' for x in checks) else 'fail','gate_T02':'open','checks':checks}
if '--check-manifests' not in sys.argv:(HERE/'evidence-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));sys.exit(0 if report['status']=='pass' else 1)
