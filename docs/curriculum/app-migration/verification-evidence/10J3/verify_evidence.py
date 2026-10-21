"""Verify scoped claims and sealed artifacts without changing historical or product inputs."""
import argparse,hashlib,json,re,subprocess,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
OUT=Path(__file__).parent;B=OUT.parent;R=OUT.parents[4]
args=argparse.ArgumentParser();args.add_argument('--check-manifests',action='store_true');opt=args.parse_args()
load=lambda p:json.loads(p.read_text())
checks=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
i=load(B/'10J1/design-comparison-index.json');v=load(B/'10J2/comparison-results.json');c=load(OUT/'learner-copy-results.json');l=load(OUT/'defects.json');rec=load(OUT/'case-reconciliation.json')
check('seventeen boards',len(i['approved_boards'])==17)
for x in i['approved_boards']+i['approval_input_checks']+i['approval_authority']:check('approval identity '+x['path'],sha(R/x['path'])==x['sha256'])
check('38 unique mapped states',len(i['states'])==len({s['state_id'] for s in i['states']})==38)
check('every state compared or explicitly unresolved',set(x['state_id'] for x in i['states'])==set(x['state_id'] for x in v['states']) and all(x['status'] in ['open_fidelity_finding','captured_pending_detailed_visual_and_target_review','pending_fresh_capture'] for x in v['states']))
check('all17 boards covered',set(x['path'] for x in i['approved_boards'])=={p for s in i['states'] for p in s['approved_references']})
check('fresh10K absent clearly marked',v['fresh10K_captures_available'] is False)
for f,n in [('shared-presentation-observations.json',88),('shared-production-observations.json',8)]:check(f+' count',len(load(B/'10J2'/f)['cases'])==n)
for x in load(B/'10J2/capture-index.json')['captures']:check('capture '+x['path'],sha(B/'10J2'/x.get('stored_path',x['path']))==x['sha256'])
check('96 logical captures',len(load(B/'10J2/capture-index.json')['captures'])==96)
cleanup=load(B/'10J2/cleanup.json')
check('91 physical PNGs retain96 observations',cleanup['logical_captures']==96 and cleanup['physical_png_files']==len(list((B/'10J2/captures').glob('*.png')))==91 and cleanup['removed_duplicate_files']==5)
for x in cleanup['duplicates']:
 check('duplicate alias '+x['logical_path'],sha(B/'10J2'/x['stored_path'])==x['sha256'] and not (B/'10J2'/x['logical_path']).exists())
check('six final distinct JVM methods',sum(int(ET.parse(p).getroot().get('tests')) for p in [B/'10J2/TEST-se.korkort.Presentation10JTest.xml',OUT/'TEST-se.korkort.Copy10JTest.xml'])==6)
for p in [B/'10J2/TEST-se.korkort.Presentation10JTest.xml',OUT/'TEST-se.korkort.Copy10JTest.xml',OUT/'source-scope-correction-receipt.xml']:
 e=ET.parse(p).getroot();check('final runtime receipt '+p.name,all(int(e.get(k,'0'))==0 for k in ['failures','errors','skipped']))
check('initial home diagnostic retained',int(ET.parse(B/'10J2/initial-harness-diagnostic.xml').getroot().get('failures'))==1)
for task in [B/'10J2',OUT]:
 for x in load(task/'environment.json')['proof_classes']:check('runtime class '+x['path'],sha(R/x['path'])==x['sha256'])
check('54 independent checks pass',len(c['checks'])==54 and all(x['pass'] for x in c['checks']) and c['all_checks_pass'])
check('14 rules no accidental final pass',len(c['copy_rules'])==14 and not c['all_rules_final_pass'])
check('13 available scoped pass one inherited classification issue',sum(x['status']=='pass_available_shared_copy_scope' for x in c['copy_rules'])==13 and sum(x['status']=='open_inherited_source_classification_defects' for x in c['copy_rules'])==1)
check('no observed forbidden learner copy',c['legacy_hits']==[])
check('3563 surfaces',sum(c['observations'].values())==3563)
for name,count in [('reader',1548),('source',519),('sign',400),('question',1000)]:
 rows=load(OUT/f'{name}-copy-observations.json')['cases'];check(name+' count and complete expected text',len(rows)==count and all(not x.get('missing_segments') for x in rows))
check('accepted source records exact',load(OUT/'source-copy-observations.json')['records']==load(R/'content/package-sources.json')['references'])
check('29 prepared data cases unique',len(rec['cases'])==len({x['case_id'] for x in rec['cases']})==29)
prepared=load(B/'10A3/data-cases.json');check('29 exact prepared IDs',{x['case_id'] for x in rec['cases']}=={x['case_id'] for f in prepared['families'] if f['gate']=='T09' for x in f['members']})
check('three clauses retain open disposition',len(rec['clauses'])==3 and all(x['status']=='open_pending_final_acceptance' for x in rec['clauses']))
check('12 inherited and6 new findings stay open',len(l['inherited_open_product_defects'])==12 and len(l['open_product_defects'])==18 and len(l['findings'])==6 and all(x['state']=='open' for x in l['findings']))
for x in l['findings']:
 check(x['id']+' complete record',set(l['required_record_fields'])<=set(x))
 for p in x['evidence']:check(x['id']+' local evidence '+p,(OUT/p).exists())
for p in [B/'10J1/baseline-entry.json',OUT/'baseline-exit.json']:
 d=load(p);check(p.name+' pass and no historical mutation',d['status']=='pass' and not d['changed_baseline_inputs'] and not d['historical_receipts_modified'])
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,val in attrs:
   if key in ['src','href']:check('HTML link '+val,(B/'10J2/annotated-comparisons'/val).exists())
Links().feed((B/'10J2/annotated-comparisons/index.html').read_text())
if opt.check_manifests:
 for n in [1,2,3]:
  task=B/f'10J{n}';m=load(task/'artifacts.json');actual={str(p.relative_to(task)) for p in task.rglob('*') if p.is_file() and p.name!='artifacts.json' and '__pycache__' not in p.parts}
  check('manifest membership '+task.name,actual=={x['path'] for x in m['files']})
  for x in m['files']:check('manifest '+task.name+'/'+x['path'],sha(task/x['path'])==x['sha256'])
result={'status':'pass' if all(x['pass'] for x in checks) else 'fail','checks':len(checks),'failures':[x for x in checks if not x['pass']],'scope':'evidence integrity; not product fidelity/classification/target acceptance','T09':'open'}
if not opt.check_manifests:(OUT/'evidence-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='pass' else 1)
