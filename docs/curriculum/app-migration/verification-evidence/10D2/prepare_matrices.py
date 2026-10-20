"""Reconcile exact replacement/faint bindings and prepare all fresh per-platform artwork contexts."""
import hashlib,json
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent;BASE=HERE.parent
read=lambda p:json.loads((ROOT/p).read_text());sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(n,d):(HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
b=read('docs/curriculum/app-migration/verification-evidence/10A3/question-batches.json');m=read('docs/curriculum/app-migration/verification-evidence/10A3/runtime-matrix.json');qs={q['key']['question_id']:q for q in read('content/accepted-assessment-questions.json')['questions']};assets={a['id']:a for a in read('content/curriculum.json')['assets']};historical=read('docs/curriculum/app-migration/implementation-evidence/9F/delivery-summary.json');accept=read('docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14/delivery-acceptance.json');accepted={q['question_id']:q for q in accept['questions']};frames=read('docs/curriculum/app-design/faint-assets-v1/asset-bindings.json');sem=read('docs/curriculum/app-migration/verification-evidence/10D1/sign-semantics-audit.json');sem={q['question_id']:q for q in sem['questions']}
pairs=[]
for pair in b['replacement_pairs']:
 rows=[]
 for qid in pair['question_ids']:
  q=qs[qid];a=accepted[qid];contexts=[c for c in m['artwork_contexts'] if c['question_id']==qid]
  assert q['key']['revision']==a['revision']=='replacement-candidate-r2' and q['acceptance']['eligibility']=='accepted' and q['acceptance']['open_holds']==[] and a['status']=='passed'
  assert len(contexts)==16 and all(c['revision']==q['key']['revision'] for c in contexts)
  old=next(x for x in historical['steps'] if qid in x['question_ids'])
  rows.append({'question_id':qid,'revision':q['key']['revision'],'historical_9F_status':old['status'],'accepted_status':q['acceptance'],'later_delivery_record':a,'image_bindings':sem[qid]['image_bindings'],'required_context_ids':[c['case_id'] for c in contexts],'data_status':'pass','fresh_visual_accessibility_status':'pending_10K'})
 pairs.append({'pair':pair['id'],'questions':rows,'status':'binding_pass_fresh_delivery_pending'})
assert len(pairs)==19 and sum(len(p['questions']) for p in pairs)==38
slots=[]
for q in qs.values():
 for slot,im in [('stem',q['image'])]+[(o['id'],o['image']) for o in q['options']]:
  if im and im['asset_id'] in b['faint_asset_ids']:
   slots.append({'question_id':q['key']['question_id'],'revision':q['key']['revision'],'slot':slot,'asset_id':im['asset_id']})
assert sorted(slots,key=lambda x:(x['question_id'],x['slot']))==sorted(b['faint_slot_bindings'],key=lambda x:(x['question_id'],x['slot']))
assert len(slots)==24 and {s['question_id'] for s in slots}==set(b['faint_question_ids'])
faint=[]
for a in frames['assets']:
 asset=assets[a['asset_id']]
 assert sha(a['original']['path'])==a['original']['sha256']==asset['original']['sha256']==asset['bundled']['sha256']==sha(asset['bundled']['path'])
 bindings=[x for x in slots if x['asset_id']==a['asset_id']];contexts=[x for x in m['artwork_contexts'] if x['question_id'] in {s['question_id'] for s in bindings}]
 assert len(bindings)==2 and len(contexts)==32
 faint.append({'asset_id':a['asset_id'],'code':a['code'],'original':asset['original'],'bundled':asset['bundled'],'original_bytes_unchanged':True,'approved_presentation':'docs/curriculum/app-design/faint-assets-v1/review.md','bindings':bindings,'overlap_with_replacements':[x['question_id'] for x in bindings if x['revision']=='replacement-candidate-r2'],'required_full_question_context_ids':[x['case_id'] for x in contexts],'data_status':'pass','visual_status':'pending_fresh_10K_observations','comparison_sheet_role':'Intended-size/shared viewer comparison only; cannot establish full-question/native acceptance.'})
assert len(faint)==12
contexts=[]
for c in m['artwork_contexts']:
 q=qs[c['question_id']];assert q['key']['revision']==c['revision']
 slots_actual={'stem':q['image']} if q['image'] else {}
 slots_actual.update({o['id']:o['image'] for o in q['options'] if o['image']})
 assert {x['slot']:x['asset_id'] for x in c['zoom_slots']}=={k:v['asset_id'] for k,v in slots_actual.items()}
 contexts.append({**c,'steps':['Open exact accepted revision and setting at actual measured viewport; preserve font size/insets.','Capture pre-answer and pending selection; check geometry/white backing/equal option frames/clipping/scrolling.','For every listed slot capture fit and 150% viewer, Reset, Close; preserve selection and restore same trigger focus.','Record exact bounds, loaded asset hash, renderer/host identity and actual assistive method.'],'result_status':'not_run_pending_10K'})
dump('replacement-delivery-matrix.json',{'task':'10D2','status':'binding_pass_fresh_delivery_pending','counts':{'pairs':19,'questions':38,'required_full_question_contexts':608},'pairs':pairs})
dump('faint-artwork-matrix.json',{'task':'10D2','status':'binding_pass_fresh_delivery_pending','counts':{'assets':12,'questions':24,'slot_bindings':24,'overlap_replacement_questions':sum(len(a['overlap_with_replacements']) for a in faint),'required_full_question_contexts':384},'assets':faint,'slot_bindings':slots})
dump('artwork-platform-cases.json',{'task':'10D2','counts':m['artwork_context_counts'],'viewport_policy':m['viewport_policy'],'settings':m['settings'],'contexts':contexts,'note':'Cases are the original frozen 10A3 IDs/revisions, not completed runtime observations.'})
print(json.dumps({'pairs':len(pairs),'faint_assets':len(faint),'faint_bindings':len(slots),'platform_cases':len(contexts)}))
