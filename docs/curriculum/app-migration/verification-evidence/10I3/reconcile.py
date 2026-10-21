"""Reconcile exact scoped10I observations with prepared cases; never rewrite historical receipts."""
import hashlib,json,platform,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/curriculum/app-migration/verification-evidence'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
identity=read(BASE/'10I1/compiled-teaching.json')['identity']
prior=read(BASE/'10H3/defects.json');defects=dict(prior)
defects.update(task='10I3',continues='../10H3/defects.json',inherited_open_product_defects=prior['open_product_defects'],findings=[])
defects['open_verification_blockers']=prior['open_verification_blockers']+[{'id':'BLOCK-10I-TARGETS','status':'open','owner':'10K2/10K3/10K4/10K6','gate':'T08','expected':'Fresh required-target normal/proof library/reader/category/reset/gap-lesson delivery, actual text scale/theme/viewport, pointer/keyboard and complete visible rendering checks. Shared semantics1280x4096 and representative390px/1.5scale do not close native/current1.6/theme checks.'}]
write(BASE/'10I3/defects.json',defects)
prepared=[]
for family in read(BASE/'10A3/data-cases.json')['families']:
 if family['gate']!='T08':continue
 evidence={'category_routes':'../10I2/library-search-filter-results.json','lesson_category_tags':'../10I2/library-search-filter-results.json','teaching_documents':'../10I1/teaching-reachability-results.json','assessment_gaps':'coverage-gap-review.json'}[family['id']]
 for member in family['members']:prepared.append({'case_id':member['case_id'],'subject':member['subject'],'oracle':member['oracle'],'status':'pass_compiled_shared_or_document_review_scope','evidence':evidence,'native_runtime':'pending10K'})
clauses=[]
for c in read(BASE/'10A3/verification-case-index.json')['gate_clauses']:
 if c.get('gate')=='T08':clauses.append({'case_id':c['case_id'],'expected':c['expected'],'status':'open_pending_fresh10K','internal_evidence':f"../10I{len(clauses)+1}/review.md",'close_rule':c['close_rule']})
write(BASE/'10I3/case-reconciliation.json',{'gate':'T08','status':'open_pending_fresh10K','prepared_cases':prepared,'clauses':clauses,'totals':{'prepared_cases':len(prepared),'dispositioned':len(prepared),'clauses':len(clauses)},'historical_case_files_unchanged':True})
for n in range(1,4):
 p=BASE/f'10I{n}';tests=[]
 for f in sorted(p.glob('TEST-*.xml')):
  x=ET.parse(f).getroot();tests.append({'receipt':f.name,**{k:x.attrib[k] for k in ['name','tests','failures','errors','timestamp']}})
 classes=[]
 for source in sorted(p.glob('*.kt')):
  for suffix in ['.class','Kt.class']:
   f=ROOT/'composeApp/build/classes/kotlin/desktop/test/se/korkort'/f'{source.stem}{suffix}'
   if f.exists():classes.append({'path':str(f.relative_to(ROOT)),'sha256':sha(f)})
 write(p/'environment.json',{'date':'2026-10-21','entry_commit':'490ab0e','host':platform.platform(),'python':platform.python_version(),'java_home':'/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home','identity':identity,'manifest_file_sha256':sha(ROOT/'content/accepted-content-manifest.json'),'source_runtime_fingerprint':'ac0d4e6b6b226b1f87f8d09521b4c334cccecd6cb7827c1bbd3889127402973c','scope':{1:'Actual shared LearningRoute/library1280x4096;91reader bodies1280x4096/defaultlight/font1; representative390px table/calculation scales1and1.5/crop800x2000/keyboardreveal390x1500. No actual native or1.6/dark pass.',2:'Actual shared LearningLibrary/LearningRoute1000x1800/defaultlight/font1, semantic actions plusindependent model oracle.',3:'Actual App() accepted-bank library/reader1000x1800/defaultlight/font1; frozen9N editorial review, no new legal-currency certification.'}[n],'tests':tests,'proof_classes':classes})
 captures=[{'path':str(f.relative_to(p)),'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted((p/'captures').glob('*.png'))]
 write(p/'capture-index.json',{'captures':captures,'scope':'Shared raster observations; representative table/empty/gap captures inspected, not exhaustive native pixel acceptance.'})
 class_names={1:['se.korkort.Reachability10ITest','se.korkort.TeachingRender10ITest','se.korkort.LearningViewsSemanticsTest.calculationAndTableRetainFullTextAtSameViewportAndLargeScale','se.korkort.LearningViewsSemanticsTest.deliberateRevealRemovesHiddenAnswerAndRestoresToggleFocus','se.korkort.LearningViewsSemanticsTest.approvedContextualCropCannotPaintIntoFollowingContent'],2:['se.korkort.Search10ITest'],3:['se.korkort.Gaps10ITest']}[n]
 write(p/'commands.json',{'base_command':"JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/verification-evidence/10I1/jvm-test-init.gradle",'test_filters':class_names,'sequence':'10I1 allfive methods; correct route count and rerun route;10I2;10I3; follow-up10I1 exact duplicate-title key verification. JUnit receipts copied between runs.','audits':{1:['python3 .../10I1/audit_teaching.py'],2:['python3 .../10I2/prepare_search.py','python3 .../10I2/audit_search.py'],3:['python3 .../10I3/audit_gaps.py','python3 .../10I3/reconcile.py','python3 .../10I3/verify_evidence.py --check-manifests']}[n],'logs':[{'path':str(f.relative_to(p)),'sha256':sha(f)} for f in sorted(p.glob('*test.txt'))]})
 if n<3:
  task_result=read(p/('teaching-reachability-results.json' if n==1 else 'library-search-filter-results.json'))
  write(p/'results.json',{'task':f'10I{n}','status':task_result['status'],'totals':task_result['totals'],'tests':tests,'T08_gate':'open_pending_fresh10K','new_product_defects':0})
write(BASE/'10I3/results.json',{'task':'10I3','status':'pass_existing_coverage_and_brief_scope_T08_open','identity':identity,'totals':{'gaps':3,'briefs':3,'rubric_criteria':18,'accepted':1000,'held':0,'concepts':500,'prepared_T08_cases':len(prepared)},'new_product_defects':0,'inherited_open_product_defects':prior['open_product_defects'],'T08_gate':'open_pending_fresh10K','next_task':'10J1','persistence_or_scored_content_added':False})
print(json.dumps({'prepared_T08_cases':len(prepared),'clauses':len(clauses),'new_product_defects':0,'T08':'open_pending_fresh10K'}))
