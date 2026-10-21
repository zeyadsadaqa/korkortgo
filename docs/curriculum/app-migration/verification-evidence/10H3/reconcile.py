"""Assemble scoped 10H dispositions from exact new receipts and frozen 7E/10A3."""
import hashlib,json,platform,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/curriculum/app-migration/verification-evidence'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
frozen=read(ROOT/'docs/curriculum/app-migration/link-and-progress-map.json')
identity=read(BASE/'10H1/navigation-transition-results.json')['identity']
observations=read(BASE/'10H3/accepted-state-observations.json')
actual={r['id']:r for r in observations['contracts_and_runs'] if 'id' in r}
contracts=[]
for i,rule in enumerate(frozen['state_rules'],1):
 id=f'7E-STATE-{i:02}';row={'id':id,**rule,'case_id':f'T07-state_contracts-{i-1}'}
 if i<=18:row.update(actual[id]);row['scope']='Fresh accepted-bank compiled transient model; shared production UI is supplemental, native relaunch remains10K.'
 else:row.update(status='conditional_future_scope',basis='No existing records or store/schema in audited baseline. No persistence/import/hot replacement is authorised or implemented by this verification.',tests=[],automatic_progress_or_mastery=False)
 contracts.append(row)
write(BASE/'10H3/state-contract-results.json',{'identity':identity,'contracts':contracts,'totals':{'recorded':22,'current_transient_passed':18,'future_conditional':4},'defaults':{'count_text':'70','feedback':'immediate'},'status':'pass_accepted_transient_scope','fresh_owner':read(BASE/'10H3/fresh-owner-results.json'),'production_owner_journeys':read(BASE/'10H3/shared-production-observations.json'),'limits':['Native restart/focus/browser modality pending10K.','Synthetic future bank is not installed or imported; no durable history is created.','DEF-10F-001 remains open: these valid-identity checks do not prove rejection of invalid package identities.'],'persistence_added':False})
prior=read(BASE/'10G3/defects.json');defects=dict(prior)
defects.update(task='10H3',continues='../10G3/defects.json',inherited_open_product_defects=prior['open_product_defects'],open_product_defects=prior['open_product_defects']+['DEF-10H-001'])
defects['findings']=[{'id':'DEF-10H-001','severity':'P1','state':'open','type':'navigation_return','detected_in_task':'10H1','case_ids':['T07-navigation_routes-2','T07-entry_point_rules-3','10H-READ-SIGN-RETURN'],'candidate':identity,'expected':'After lesson→sign→catalogue, Return to reading restores the validated origin and reading context.','observed':'The registered action executes but Road signs and signals stays displayed. returnToReading updates target/restored but leaves references=true; that branch takes precedence over target.','reproduction':['Open actual LearningRoute M03-L01/teaching-005.','Invoke rendered B1 internal link callback.','Choose ‹ Road signs and reference.','Choose Return to reading; catalogue remains.'],'evidence':['../10H1/reading-sign-return-observations.json','../10H1/TEST-se.korkort.ReadingSignReturn10HTest.xml','../10H1/sign-return-test.txt','../10H1/captures/catalogue-return-stuck.png'],'affected_ids_files':['M03-L01','sign-B1','composeApp/src/commonMain/kotlin/se/korkort/LearningRoute.kt:returnToReading / references branch'],'owners':['10L bounded navigation correction','10K target retest'],'impacted_gates':['T07'],'fix_scope':'Restore a found reading origin from the reference-catalogue route by clearing incompatible route state; preserve validated position/focus and library/review context. Verify nested sign/group/source paths. No redesign or storage.','approval_if_required':'No new design/persistence is proposed; execute bounded10L under its existing change-control process.','invalidation':'Any route correction invalidates affected shared return observations and requires normal/proof target identity capture again. Accepted content need not change for route-only repair.','retest':['ReadingSignReturn10HTest must pass without changing its expected behaviour.','Repeat source/group/sign nested returns, moved/unknown origin recovery, library filters and review returns.','Fresh affected Android/desktop/iOS simulator/wasmJs route/focus observations through10K.'],'closure_reason':None}]
defects['open_verification_blockers']=prior['open_verification_blockers']+[{'id':'BLOCK-10H-NATIVE','status':'open','owner':'10K2/10K3/10K4/10K6','gate':'T07','expected':'Fresh actual-target navigation, native pointer/keyboard focus, modal background exclusion and real restart/no-restoration observations; shared JVM semantics and model restart do not close them.'}]
write(BASE/'10H3/defects.json',defects)
# Exact prepared case-ID reconciliation; historical not_run inputs remain untouched.
cases=[]
for family in read(BASE/'10A3/data-cases.json')['families']:
 if family['gate']!='T07':continue
 for member in family['members']:
  row={'case_id':member['case_id'],'subject':member['subject'],'oracle':member['oracle']}
  if family['id']=='state_contracts':row.update(status=contracts[int(member['case_id'].split('-')[-1])]['status'],evidence='state-contract-results.json')
  elif family['id']=='reading_edges':row.update(status='pass_frozen_vs_compiled',evidence='../10H1/reading-edge-results.json')
  elif family['id']=='version_transition':
   key=member['case_id'].removeprefix('T07-version_transition-')
   row.update(status='checked_existing_accepted_identity' if key in ['initial_update','package_identity','new_package_manifest'] else 'conditional_future_scope',evidence='state-contract-results.json',basis='Initial restart is model/shared scope; future hot replacement/history/import is absent and remains conditional. Invalid-identity gate DEF-10F-001 stays open.')
  else:row.update(status='audited_shared_scope_gate_open',evidence='../10H1/results.json',remaining='DEF-10H-001 and/or fresh10K target observations; do not infer gate closure.')
  cases.append(row)
write(BASE/'10H3/case-reconciliation.json',{'gate':'T07','status':'open','prepared_cases':cases,'totals':{'prepared':len(cases),'recorded':len(cases)},'production_defect':'DEF-10H-001','native_gate':'BLOCK-10H-NATIVE'})
for n in range(1,4):
 p=BASE/f'10H{n}';tests=[]
 for f in sorted(p.glob('TEST-*.xml')):
  x=ET.parse(f).getroot();tests.append({'receipt':f.name,**{k:x.attrib[k] for k in ['name','tests','failures','errors','timestamp']}})
 environment={'date':'2026-10-21','entry_commit':'0023ca5','host':platform.platform(),'python':platform.python_version(),'java_home':'/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home','identity':identity,'manifest_file_sha256':'ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21','source_runtime_fingerprint':'ac0d4e6b6b226b1f87f8d09521b4c334cccecd6cb7827c1bbd3889127402973c','scope':'Compiled production model and shared Compose scene1000x1800, default light/font1; source focus tests800x1600 and library800x1800 as recorded in unchanged test source. No actual OS/browser delivery inferred.','tests':tests}
 environment['proof_classes']=[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for source in sorted(p.glob('*.kt')) if (f:=ROOT/'composeApp/build/classes/kotlin/desktop/test/se/korkort'/f'{source.stem}.class').exists()]
 write(p/'environment.json',environment)
 # Record commands as found in logs; Gradle test filters are in review.md and reproducible scripts.
 logs=[]
 for f in sorted(p.glob('*test.txt')):logs.append({'log':f.name,'successful':'BUILD SUCCESSFUL' in f.read_text(),'failure':'BUILD FAILED' in f.read_text()})
 write(p/'commands.json',{'base_command':"JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/verification-evidence/10H1/jvm-test-init.gradle --tests <class-or-method>",'receipt_logs':logs,'historical_diagnostics':'Initial direct-return assumption, subsequent live return failure, offscreen review control and tombstone harness field diagnostic retained separately; none is treated as a passing product receipt.'})
 # Preserve logical capture aliases while storing identical PNG bytes once.
 previous=read(p/'capture-index.json')['captures'] if (p/'capture-index.json').exists() else []
 captures=[];stored={}
 for f in sorted((p/'captures').glob('*.png')):
  digest=sha(f);relative=str(f.relative_to(p));canonical=stored.setdefault(digest,relative)
  captures.append({'path':relative,'stored_path':canonical,'bytes':f.stat().st_size,'sha256':digest})
  if relative!=canonical:f.unlink()
 known={r['path'] for r in captures}
 for row in previous:
  if row['path'] not in known:
   target=p/row.get('stored_path',row['path'])
   if target.exists() and sha(target)==row['sha256']:captures.append(row)
 captures.sort(key=lambda row:row['path'])
 write(p/'capture-index.json',{'captures':captures,'scope':'Shared raster captures; representative sign-return failure and modal/review captures inspected, not native-platform screenshots.'})
print(json.dumps({'contracts_passed':18,'conditional':4,'prepared_cases':len(cases),'new_product_findings':1,'gate':'T07 open'}))
