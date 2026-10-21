"""Verify10I evidence integrity and explicit scope, without claiming T08 target closure."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/curriculum/app-migration/verification-evidence'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(label,test):checks.append({'check':label,'pass':bool(test)})
identity=read(ROOT/'content/accepted-content-manifest.json')['identity']
first=read(BASE/'10I1/teaching-reachability-results.json');second=read(BASE/'10I2/library-search-filter-results.json');third=read(BASE/'10I3/coverage-gap-review.json')
for p in [first,second,third]:check(p['task']+' passing independentchecks',p['identity']==identity and p['status'].startswith('pass') and all(c['pass'] for c in p['checks']))
check('2973independentassertions',sum(len(p['checks']) for p in [first,second,third])==2973)
check('115routes91documents1316blocks50checks',all(first['totals'][k]==v for k,v in {'routes':115,'documents':91,'top_level_blocks':1316,'knowledge_checks':50}.items()))
check('allteachingcounts',all(first['totals'][k]==v for k,v in {'modules':10,'lessons':40,'reviews':10,'appendices':4,'reference_groups':24,'additional_front_matter':27}.items()))
check('288search5categories40tags',all(second['totals'][k]==v for k,v in {'search_cases':288,'category_filters':5,'tag_records':40}.items()))
check('3gaps3briefs18criteria',all(third['totals'][k]==v for k,v in {'gaps':3,'briefs':3,'rubric_criteria':18}.items()))
actual=read(BASE/'10I3/compiled-gap-observations.json')
check('1000accepted500conceptszeroheld',actual['accepted_questions']==1000 and actual['held_questions']==0 and actual['concepts']==500 and actual['release_accepted'])
for gap in third['gaps']:check(gap['lesson_id']+'noscorecompletion',not gap['became_scored_content'] and not gap['completion_or_mastery_awarded'] and len(gap['rubric_criteria'])==6)
prepared=[m['case_id'] for f in read(BASE/'10A3/data-cases.json')['families'] if f['gate']=='T08' for m in f['members']]
reconciled=read(BASE/'10I3/case-reconciliation.json');check('all139caseIDsreconciled',[r['case_id'] for r in reconciled['prepared_cases']]==prepared and len(prepared)==139)
check('threeoriginalclausesopen',len(reconciled['clauses'])==3 and all(c['status']=='open_pending_fresh10K' for c in reconciled['clauses']))
defects=read(BASE/'10I3/defects.json');prior=read(BASE/'10H3/defects.json')
check('12inheritedfindingsunchangednonew',defects['open_product_defects']==prior['open_product_defects'] and len(defects['open_product_defects'])==12 and not defects['findings'])
check('T08targetblockeropen',any(b['id']=='BLOCK-10I-TARGETS' and b['status']=='open' for b in defects['open_verification_blockers']) and reconciled['status']=='open_pending_fresh10K')
for name in ['10I1/baseline-entry.json','10I3/baseline-exit.json']:
 p=read(BASE/name);check(name,p['status']=='pass' and not p['changed_baseline_inputs'] and not p['historical_receipts_modified'])
tests=failures=errors=0
for n in range(1,4):
 p=BASE/f'10I{n}';env=read(p/'environment.json')
 check(f'10I{n}acceptedmanifest',env['identity']==identity and env['manifest_file_sha256']==sha(ROOT/'content/accepted-content-manifest.json'))
 for f in p.glob('TEST-*.xml'):
  x=ET.parse(f).getroot();tests+=int(x.get('tests'));failures+=int(x.get('failures'));errors+=int(x.get('errors'));check(f'{p.name}/{f.name}',int(x.get('failures'))==int(x.get('errors'))==int(x.get('skipped'))==0)
 for c in env['proof_classes']:check(c['path'],sha(ROOT/c['path'])==c['sha256'])
 for c in read(p/'capture-index.json')['captures']:check(f'{p.name}/'+c['path'],sha(p/c['path'])==c['sha256'] and (p/c['path']).stat().st_size==c['bytes'])
 if '--check-manifests' in sys.argv:
  manifest=read(p/'artifacts.json');expected={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name!='artifacts.json' and '__pycache__' not in f.parts}
  check(p.name+'manifestcomplete',{r['path'] for r in manifest}==expected)
  for c in manifest:check(f'{p.name}/'+c['path'],sha(p/c['path'])==c['sha256'] and (p/c['path']).stat().st_size==c['bytes'])
check('eightfinalJVMmethodspass',tests==8 and failures==errors==0)
result={'status':'pass_evidence_integrity_T08_target_gate_open' if all(c['pass'] for c in checks) else 'fail','totals':{'integrity_checks':len(checks),'final_test_methods':tests,'failures':failures,'errors':errors,'independent_assertions':2973},'checks':checks,'not_gate_closure':True}
if '--check-manifests' not in sys.argv:(BASE/'10I3/evidence-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
for c in checks:
 if not c['pass']:print('FAILED',c['check'])
assert all(c['pass'] for c in checks)
