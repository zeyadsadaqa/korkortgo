"""Apply exact 9H1–9H6 load batches sequentially, independently verifying all weights."""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from compile_curriculum import Emitter, kotlin_string
from content_schema import Schema
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('docs/curriculum/app-migration/implementation-evidence/9H')
ACTIONS=Path('docs/curriculum/app-migration/question-actions.json')
BANK=Path('composeApp/src/commonMain/kotlin/se/korkort/Bank.kt')
IDS=[f'load-{ready}-{load}' for ready in range(1200,2551,150) for load in [350,450,550]]
BATCHES=[IDS[i:i+5] for i in range(0,30,5)]
def read(p):return json.loads((ROOT/p).read_text())
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def origin(p,locator):return {'file':{'path':str(p),'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()},'locator':locator,'evidence_ids':[],'pdf_evidence_page':None}
def rich(s):return [{'type':'text','text':s}]
def outputs(through_batch=6):
 assert 1 <= through_batch <= 6
 selected=IDS[:through_batch*5]
 files={}
 bank=read(Path('content/questions.json')); actions=read(ACTIONS)['questions']; mapping={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/question-map.json'))['questions']}; identities={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/implementation-evidence/9D1/authored-identities.json'))['questions']}
 assert not any(row.get('assessment') for row in bank if row['id'] in IDS[through_batch*5:]),'Cannot regenerate an earlier batch over later typed batches'
 review=read(BASE/'source-review.json'); emitter=Emitter(Schema(ROOT),'load9H'); lines=(ROOT/BANK).read_text().splitlines(True); receipts=[];typed=[]
 for n,qid in enumerate(selected):
  a=next(q for q in actions if q['question_id']==qid); draft=copy.deepcopy(a['proposed_changes']['draft_question']); before=a['original']; m=mapping[qid];option_ids=identities[qid]['option_ids_in_authored_order']
  assert review['verified_on']=='2026-10-16'
  inputs=re.fullmatch(r'A car has registered total weight \(totalvikt\) (\d+) kg and defined ready-for-service weight \(tjänstevikt\) (\d+) kg, already including the driver\. What is its maximum passenger and goods load from these figures\?',draft['prompt'])
  assert inputs,qid
  total,ready=map(int,inputs.groups());result=total-ready
  values=[int(re.fullmatch(r'(\d+) kg',o['text']).group(1)) for o in draft['options']]
  assert len(set(values))==4 and sum(v==result for v in values)==1
  assert values[draft['correct']]==result and draft['correct']==before['correct']
  assert [o['text'] for o in draft['options']]==[o['text'] for o in before['options']]
  assert draft['id']==before['id'] and draft['concept']==before['concept']
  equation=f'{total} − {ready} = {result} kg'
  for explanation in [draft['explanation']]+[o['explanation'] for o in draft['options']]:
   assert equation in explanation and 'driver is already included' in explanation
  assert values==[result,ready,total,total+result]
  arithmetic={'total_kg':total,'ready_kg':ready,'driver_included_once':True,'calculated_maximum_load_kg':result,'equation':equation,'option_checks':[{'option_id':oid,'value_kg':v,'equals_result':v==result,'difference_from_result_kg':v-result,'role':role} for oid,v,role in zip(option_ids,values,['maximum load','ready weight','total weight','total plus maximum load'])]}
  q={'key':{'question_id':qid,'revision':'load-r2'},'concept_id':draft['concept'],'category':draft['category'].lower(),'prompt':rich(draft['prompt']),'image':None,'options':[{'id':oid,'text':rich(o['text']),'image':None} for oid,o in zip(option_ids,draft['options'])],
   'feedback':{'target_sign_code':None,'english_label':None,'correct_option_id':option_ids[draft['correct']],'explanation':rich(draft['explanation']),'option_feedback':[{'option_id':oid,'explanation':rich(o['explanation']),'sign_code':None,'english_label':None,'source_uses':[]} for oid,o in zip(option_ids,draft['options'])]},
   'relationship':{**{k:copy.deepcopy(m[k]) for k in ['primary_lesson_id','related_lesson_ids','reference_ids','source_ids','content_version']},'disposition':'rewrite','source_uses':[]},
   'acceptance':{'eligibility':'accepted','content_review':{'record':origin(BASE/'source-review.json','json:/decision'),'reviewed_on':'2026-10-16'},'description_reviews':[],'delivery_proof':[],'open_holds':[]},'origin':origin(ACTIONS,f'json:/questions/{actions.index(a)}/proposed_changes/draft_question')}
  draft['assessment']=q;current=next(row for row in bank if row['id']==qid)
  assert current in (before,draft),f'Unexpected edits to {qid}'
  bank[bank.index(current)]=draft; call=emitter.emit(q,'AssessmentQuestion',qid)
  options=', '.join('Option('+', '.join(kotlin_string(o[k]) for k in ['text','explanation','image'])+')' for o in draft['options'])
  args=[kotlin_string(draft['id']),kotlin_string(draft['concept']),'Category.'+draft['category'],kotlin_string(draft['prompt']),'listOf('+options+')',str(draft['correct']),kotlin_string(draft['explanation']),str(draft['page']),kotlin_string(draft['source']),kotlin_string(draft['image']),call]
  matches=[i for i,l in enumerate(lines) if l.startswith('Question('+kotlin_string(qid)+',')];assert len(matches)==1
  lines[matches[0]]='Question('+', '.join(args)+'),\n'
  receipts.append({'step':f'9H{n//5+1}','question_id':qid,'before_revision':'legacy-r1','after_revision':'load-r2','content_acceptance':'passed','one_correct_answer':True,'correct_option_id':option_ids[draft['correct']],'all_explanations_reviewed':True,'arithmetic':arithmetic,'source_review':str(BASE/'source-review.json')+'#/decision','before':before,'after':draft});typed.append(q)
  if (n+1)%5==0:
   batch=n//5+1
   files[BASE/f'9H{batch}'/'question-acceptance.json']=dump({'schema_version':1,'step':f'9H{batch}','question_ids':BATCHES[batch-1],'questions':receipts[-5:],'content_acceptance':'passed','release_acceptance':False})
 return {**files,Path('content/questions.json'):dump(bank),BANK:''.join(lines),Path('composeApp/src/commonMain/kotlin/se/korkort/LoadClarifications9H.kt'):'package se.korkort\n\n// Generated by tools/apply_load_clarifications_9h.py.\n'+'\n'.join(f'internal fun {name}(): {kind} = {expression}\n' for name,kind,expression in emitter.functions),BASE/'questions.json':dump({'schema_version':1,'questions':typed})}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--through-batch',type=int,default=6,choices=range(1,7));args=p.parse_args()
 for path,value in outputs(args.through_batch).items():
  if args.check:assert (ROOT/path).read_text()==value,path
  else:
   (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
   (ROOT/path).write_text(value)
 print(f'9H1–9H{args.through_batch}: {args.through_batch*5} exact load clarifications; numeric keys preserved; load-r2 metadata.')
if __name__=='__main__':main()
