"""Apply 9I1–9I5 exact fuel drafts sequentially with independent Decimal arithmetic."""
import argparse
import copy
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path
from compile_curriculum import Emitter, kotlin_string
from content_schema import Schema
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('docs/curriculum/app-migration/implementation-evidence/9I')
ACTIONS=Path('docs/curriculum/app-migration/question-actions.json')
BANK=Path('composeApp/src/commonMain/kotlin/se/korkort/Bank.kt')
BATCHES=[['fuel-saving-150-0.5'],['fuel-saving-150-1.5'],['fuel-saving-250-0.5'],['fuel-saving-250-1.5'],['fuel-40-5','fuel-saving-100-0.5','fuel-saving-100-1','fuel-saving-100-2','fuel-saving-200-0.5','fuel-saving-200-1']]
IDS=[qid for batch in BATCHES for qid in batch]
def number(text):return Decimal(re.fullmatch(r'(\d+(?:\.\d+)?) litres?',text).group(1))
def fmt(value):return format(value.normalize(),'f')
def read(p):return json.loads((ROOT/p).read_text())
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def origin(p,locator):return {'file':{'path':str(p),'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()},'locator':locator,'evidence_ids':[],'pdf_evidence_page':None}
def rich(s):return [{'type':'text','text':s}]
def outputs(through_step=5):
 assert 1 <= through_step <= 5
 selected=[qid for batch in BATCHES[:through_step] for qid in batch]
 files={}
 bank=read(Path('content/questions.json')); actions=read(ACTIONS)['questions']; mapping={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/question-map.json'))['questions']}; identities={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/implementation-evidence/9D1/authored-identities.json'))['questions']}
 assert not any(row.get('assessment') for row in bank if row['id'] in IDS[len(selected):]),'Cannot regenerate an earlier batch over later typed batches'
 review=read(BASE/'content-review.json'); emitter=Emitter(Schema(ROOT),'fuel9I'); lines=(ROOT/BANK).read_text().splitlines(True); receipts=[];typed=[]
 for n,qid in enumerate(selected):
  a=next(q for q in actions if q['question_id']==qid); draft=copy.deepcopy(a['proposed_changes']['draft_question']); before=a['original']; m=mapping[qid];option_ids=identities[qid]['option_ids_in_authored_order']
  step=next(i for i,batch in enumerate(BATCHES,1) if qid in batch)
  exact=step<5
  revision='fuel-exact-r2' if exact else 'fuel-unit-r2'
  assert review['reviewed_on']=='2026-10-16'
  if qid=='fuel-40-5':
   match=re.fullmatch(r'A car averages (\d+(?:\.\d+)?) litres per 100 km over a (\d+) km journey\. Approximately how much fuel does the journey use\?',draft['prompt'])
   rate,distance=map(Decimal,match.groups())
  else:
   match=re.fullmatch(r'Smoother driving reduces measured consumption by (\d+(?:\.\d+)?) litres per 100 km\. Over (\d+) km, how much fuel is saved\?(?: Give the exact result in litres; do not round\.)?',draft['prompt'])
   rate,distance=map(Decimal,match.groups())
  result=distance*rate/Decimal(100);values=[number(o['text']) for o in draft['options']]
  assert len(set(values))==4 and sum(v==result for v in values)==1
  assert values[draft['correct']]==result and draft['correct']==before['correct']
  assert draft['id']==before['id'] and draft['concept']==before['concept']
  equation=f'{fmt(distance)} × {fmt(rate)} ÷ 100 = {fmt(result)}'
  for explanation in [draft['explanation']]+[o['explanation'] for o in draft['options']]:assert equation in explanation
  if exact:
   assert draft['prompt'].endswith('Give the exact result in litres; do not round.')
   assert values==[result,result/2,result*Decimal('1.5'),result*2]
   for explanation in [draft['explanation']]+[o['explanation'] for o in draft['options']]:assert 'not a guaranteed real-world saving' in explanation
   assert number(before['options'][before['correct']]['text'])!=result
  else:
   assert values==[number(o['text']) for o in before['options']]
   # Only the exact approved field patches are allowed, including their documented limits.
   patched=copy.deepcopy(before)
   for path,value in a['proposed_changes']['field_patches'].items():
    keys=path.split('.');target=patched
    for key in keys[:-1]:target=target[int(key)] if isinstance(target,list) else target[key]
    target[int(keys[-1]) if isinstance(target,list) else keys[-1]]=value
   assert patched==draft
  arithmetic={'distance_km':fmt(distance),'supplied_rate_l_per_100km':fmt(rate),'exact_result_l':fmt(result),'equation':equation,'rounding':'none','old_key':before['options'][before['correct']]['text'],'new_key':draft['options'][draft['correct']]['text'],'numeric_key_changed':exact,'option_checks':[{'option_id':oid,'value_l':fmt(v),'equals_result':v==result,'difference_from_result_l':fmt(v-result)} for oid,v in zip(option_ids,values)]}
  q={'key':{'question_id':qid,'revision':revision},'concept_id':draft['concept'],'category':draft['category'].lower(),'prompt':rich(draft['prompt']),'image':None,'options':[{'id':oid,'text':rich(o['text']),'image':None} for oid,o in zip(option_ids,draft['options'])],
   'feedback':{'target_sign_code':None,'english_label':None,'correct_option_id':option_ids[draft['correct']],'explanation':rich(draft['explanation']),'option_feedback':[{'option_id':oid,'explanation':rich(o['explanation']),'sign_code':None,'english_label':None,'source_uses':[]} for oid,o in zip(option_ids,draft['options'])]},
   'relationship':{**{k:copy.deepcopy(m[k]) for k in ['primary_lesson_id','related_lesson_ids','reference_ids','source_ids','content_version']},'disposition':'rewrite','source_uses':[]},
   'acceptance':{'eligibility':'accepted','content_review':{'record':origin(BASE/'content-review.json','json:/decision'),'reviewed_on':'2026-10-16'},'description_reviews':[],'delivery_proof':[],'open_holds':[]},'origin':origin(ACTIONS,f'json:/questions/{actions.index(a)}/proposed_changes/draft_question')}
  draft['assessment']=q;current=next(row for row in bank if row['id']==qid)
  assert current in (before,draft),f'Unexpected edits to {qid}'
  bank[bank.index(current)]=draft; call=emitter.emit(q,'AssessmentQuestion',qid)
  options=', '.join('Option('+', '.join(kotlin_string(o[k]) for k in ['text','explanation','image'])+')' for o in draft['options'])
  args=[kotlin_string(draft['id']),kotlin_string(draft['concept']),'Category.'+draft['category'],kotlin_string(draft['prompt']),'listOf('+options+')',str(draft['correct']),kotlin_string(draft['explanation']),str(draft['page']),kotlin_string(draft['source']),kotlin_string(draft['image']),call]
  matches=[i for i,l in enumerate(lines) if l.startswith('Question('+kotlin_string(qid)+',')];assert len(matches)==1
  lines[matches[0]]='Question('+', '.join(args)+'),\n'
  receipts.append({'step':f'9I{step}','question_id':qid,'before_revision':'legacy-r1','after_revision':revision,'content_acceptance':'passed','one_correct_answer':True,'correct_option_id':option_ids[draft['correct']],'all_explanations_reviewed':True,'arithmetic':arithmetic,'content_review':str(BASE/'content-review.json')+'#/decision','before':before,'after':draft});typed.append(q)
  if qid==BATCHES[step-1][-1]:
   files[BASE/f'9I{step}'/'question-acceptance.json']=dump({'schema_version':1,'step':f'9I{step}','question_ids':BATCHES[step-1],'questions':receipts[-len(BATCHES[step-1]):],'content_acceptance':'passed','release_acceptance':False})
 return {**files,Path('content/questions.json'):dump(bank),BANK:''.join(lines),Path('composeApp/src/commonMain/kotlin/se/korkort/FuelCorrections9I.kt'):'package se.korkort\n\n// Generated by tools/apply_fuel_corrections_9i.py.\n'+'\n'.join(f'internal fun {name}(): {kind} = {expression}\n' for name,kind,expression in emitter.functions),BASE/'questions.json':dump({'schema_version':1,'questions':typed})}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--through-step',type=int,default=5,choices=range(1,6));args=p.parse_args()
 for path,value in outputs(args.through_step).items():
  if args.check:assert (ROOT/path).read_text()==value,path
  else:
   (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
   (ROOT/path).write_text(value)
 print(f'9I1–9I{args.through_step}: exact fuel drafts verified with Decimal arithmetic.')
if __name__=='__main__':main()
