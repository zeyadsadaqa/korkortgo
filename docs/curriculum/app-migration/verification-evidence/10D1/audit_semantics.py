"""Independent approved-proposal/description/asset reconciliation; 10E semantic review is a separate required input."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent;BASE=HERE.parent
cache={}
def read(path):
 p=ROOT/path
 if p not in cache:cache[p]=json.loads(p.read_text())
 return cache[p]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(name,d): (HERE/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def text(r):return ''.join(x.get('text',x.get('expression','')) if x['type'] in ['text','math'] else text(x.get('children',x.get('label',[]))) for x in r)
def resolve(record):
 p=record['file']['path'];assert sha(p)==record['file']['sha256'],p
 d=read(p);pointer=record['locator'].removeprefix('json:')
 if pointer=='whole-file':return d
 for k in pointer.strip('/').split('/'):d=d[int(k)] if isinstance(d,list) else d[k.replace('~1','/').replace('~0','~')]
 return d
questions={q['key']['question_id']:q for q in read('content/accepted-assessment-questions.json')['questions']};actions={q['question_id']:q for q in read('docs/curriculum/app-migration/question-actions.json')['questions']};assets={a['id']:a for a in read('content/curriculum.json')['assets']};batch=read('docs/curriculum/app-migration/verification-evidence/10A3/question-batches.json');compiled=read('docs/curriculum/app-migration/verification-evidence/10D1/compiled-artwork-contracts.json');compiled={q['question']['key']['question_id']:q for q in compiled['rows']};members={qid:r['owner'] for r in batch['sign_rewrite_batches']+batch['replacement_pairs'] for qid in r['question_ids']};rows=[];checks=[];descriptions=[]
def check(name,ok,detail=None):
 row={'check_id':f'10D1-{len(checks)+1:05}','name':name,'status':'pass' if ok else 'fail'}
 if detail is not None:row['detail']=detail
 checks.append(row);return row['check_id']
check('616 exact distinct assigned sign question IDs',len(members)==616 and len(compiled)==616 and set(members)==set(compiled))
for qid,owner in members.items():
 images_out=[];start=len(checks);q=questions[qid];a=actions[qid];p=a['proposed_changes'];options={o['id']:o for o in q['options']};feedback={o['option_id']:o for o in q['feedback']['option_feedback']};co=compiled[qid];pre=co['pre_answer'];image_rows=[]
 check(qid+' actual compiled accepted question parity',co['question']==q)
 check(qid+' exact proposed prompt and target',text(q['prompt'])==p['prompt'] and q['feedback']['target_sign_code']==p['target_code_metadata'] and q['feedback']['english_label']==p['post_answer_english_label'])
 check(qid+' authored option identities and unique key',list(options)==[o['option_id'] for o in p['options']] and [o['option_id'] for o in p['options'] if o['is_correct']]==[q['feedback']['correct_option_id']])
 check(qid+' exact post-answer rationale',text(q['feedback']['explanation'])==p['post_answer_explanation'])
 check(qid+' no pre-answer feedback or target metadata',pre['explanation'] is None and pre['target_code'] is None and pre['target_label'] is None and all(o['correct'] is None and o['feedback'] is None for o in pre['choices']))
 check(qid+' exact pre-answer content projection',pre['prompt']==p['prompt'] and {o['id'] for o in pre['choices']}==set(options))
 check(qid+' accepted revision retains evidence and no active holds',q['acceptance']['eligibility']=='accepted' and q['acceptance']['open_holds']==[] and bool(q['acceptance']['delivery_proof']) and all(resolve(r['record']) is not None for r in q['acceptance']['delivery_proof']))
 for o in p['options']:
  oid=o['option_id'];actual=options[oid];f=feedback[oid];projected=next(x for x in pre['choices'] if x['id']==oid)
  check(qid+' '+oid+' exact meaning/recognition label policy',text(actual['text'])==(o['meaning_option_text'] or '') and projected['text']==text(actual['text']))
  check(qid+' '+oid+' exact per-option code/label/feedback',f['sign_code']==o['code_metadata_after_reveal'] and f['english_label']==o['post_answer_label'] and text(f['explanation'])==o['post_answer_explanation'])
  if actual['image']:image_rows.append((oid,actual['image'],o['visual_description_brief']['exact_asset'],o['code_metadata_after_reveal']))
 if q['image']:image_rows.insert(0,('stem',q['image'],p['question_image_asset'],p['target_code_metadata']))
 for slot,binding,expected,code in image_rows:
  asset=assets[binding['asset_id']];neutral=binding['neutral_description'];review=resolve(neutral['review']['record']);frozen=review['asset'];projected=pre['image'] if slot=='stem' else next(x for x in pre['choices'] if x['id']==slot)['image']
  check(qid+' '+slot+' exact approved physical description',neutral['text']==review['description'] and review['slot']==slot and review['description_code_metadata_only']==code)
  check(qid+' '+slot+' exact variant bytes and asset code',asset['code_or_illustration_id']==code and asset['original']['path']==expected['path'] and sha(expected['path'])==expected['sha256']==asset['original']['sha256']==asset['bundled']['sha256']==sha(asset['bundled']['path'])==frozen['sha256'])
  check(qid+' '+slot+' neutral-only image projection',projected['description']==neutral['text'] and set(projected)=={'asset_id','description'} and not re.search(r'\b(?:correct answer|this means|official code|illustration [A-Z]\d+)\b',neutral['text'],re.I))
  descriptions.append(neutral['text']);image_rows_data={'slot':slot,'asset_id':binding['asset_id'],'code_metadata_only':code,'variant':asset['variant'],'source_asset':expected,'description':neutral['text'],'description_review':neutral['review']}
  # Replace tuple after checks only via a separate result collection.
  images_out.append(image_rows_data)
 if qid.startswith('sign-recognise-'):
  check(qid+' no duplicate option asset or physical description',len({assets[o['image']['asset_id']]['original']['sha256'] for o in q['options']})==4 and len({o['image']['neutral_description']['text'].strip().casefold() for o in q['options']})==4)
 else:check(qid+' no duplicate meaning option',len({text(o['text']).strip().casefold() for o in q['options']})==4)
 rowchecks=checks[start:];rows.append({'question_id':qid,'revision':q['key']['revision'],'owner_for_independent_semantic_review':owner,'disposition':q['relationship']['disposition'],'target_code_metadata_only':p['target_code_metadata'],'paired_question_id':qid.replace('sign-meaning-','sign-recognise-') if qid.startswith('sign-meaning-') else qid.replace('sign-recognise-','sign-meaning-'),'authored_option_codes':[o['code_metadata_after_reveal'] for o in p['options']],'authored_correct_option_id':q['feedback']['correct_option_id'],'image_bindings':images_out,'check_ids':[x['check_id'] for x in rowchecks],'data_audit_status':'pass' if all(x['status']=='pass' for x in rowchecks) else 'fail','independent_semantic_review':'pending_10E2–10E14'});images_out=[]
for row in rows:
 pair=next(x for x in rows if x['question_id']==row['paired_question_id']);check(row['question_id']+' pair preserves target and option-code direction',row['target_code_metadata_only']==pair['target_code_metadata_only'] and row['authored_option_codes']==pair['authored_option_codes'])
changed=[]
for qid in batch['distractor_change_ids']:
 p=actions[qid]['proposed_changes'];q=questions[qid];codes=[x['sign_code'] for x in q['feedback']['option_feedback']];ok=p['original_option_codes']!=p['proposed_option_codes'] and codes==p['proposed_option_codes']
 changed.append({'question_id':qid,'revision':q['key']['revision'],'original_codes':p['original_option_codes'],'proposed_codes':p['proposed_option_codes'],'accepted_codes':codes,'status':'pass' if ok else 'fail','counts_as_extra_question':False,'semantic_review_owner':members[qid]})
check('134 exact overlapping distractor changes',len(changed)==134 and len({x['question_id'] for x in changed})==134 and all(x['status']=='pass' for x in changed))
fail=[x for x in checks if x['status']=='fail'];report={'task':'10D1','status':'data_audit_fail' if fail else 'data_audit_pass_pending_10E','manifest_sha256':sha('content/accepted-content-manifest.json'),'counts':{'questions':len(rows),'rewrite':sum(x['disposition']=='rewrite' for x in rows),'replace':sum(x['disposition']=='replace' for x in rows),'image_occurrences':len(descriptions),'checks':len(checks),'failed':len(fail)},'questions':rows,'checks':checks,'closure_dependency':'Per-ID independent rule/variant/visual-neutrality review from 10E2–10E14 has not run; exact proposal/provenance parity and leak guards do not substitute.'}
dump('sign-semantics-audit.json',report);dump('distractor-change-audit.json',{'task':'10D1','count':len(changed),'status':'data_audit_pass_pending_10E' if all(x['status']=='pass' for x in changed) else 'fail','questions':changed});print(json.dumps({'status':report['status'],'counts':report['counts'],'failures':fail[:10]},indent=2));sys.exit(1 if fail else 0)
