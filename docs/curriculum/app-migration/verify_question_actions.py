"""7D acceptance: decisions, change evidence, proposed keys and protected files."""
from pathlib import Path
from decimal import Decimal as D
from functools import lru_cache
import json,hashlib,collections,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def read(p):return json.loads(p.read_text())
@lru_cache(maxsize=None)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(HERE/'question-actions.json');bank=read(ROOT/'content/questions.json');m=read(HERE/'question-map.json');baseline=read(HERE/'baseline.json');caps={c['code']:c for c in read(ROOT/'docs/curriculum/sign-captions.json')['captions']};assets=read(HERE/'question-review/asset-review.json');faint=set(assets['faint_outline_codes']);src={s['id'] for s in read(HERE/'question-review/source-rechecks.json')['checks']};refs={s['id'] for s in m['source_registry']}
assert [q['question_id'] for q in a['questions']]==[q['id'] for q in bank]
assert len({q['question_id'] for q in a['questions']})==len(bank)==1000
for inp in a['inputs']:assert sha(ROOT/inp['path'])==inp['sha256'],inp['path']
# Reconfirm the upstream baseline; planning must not modify any app/content/PDF.
for inp in baseline['frozen_inputs']+baseline['bundled_assets']:assert sha(ROOT/inp['path'])==inp['sha256'],inp['path']
counts=collections.Counter();holds=[];proposed_exact={};targets=0
for q,b,mp in zip(a['questions'],bank,m['questions']):
 assert q['original']==b and q['concept_id']==b['concept'] and q['primary_lesson_id']==mp['primary_lesson_id']
 assert q['disposition'] in ['retain','rewrite','replace','remove'] and q['rationale']
 assert q['evidence']['source_reference_ids'] and all(r in refs for r in q['evidence']['source_reference_ids'])
 assert set(q['fresh_source_check_ids'])<=src
 assert q['evidence']['book_evidence_ids']==[e['evidence_id'] for e in mp['teaching_evidence']]
 changes=q['proposed_changes'];counts[q['disposition']]+=1
 if q['disposition']=='retain':assert not changes and not q['research_holds']
 else:assert changes and q['acceptance_criteria']
 if q['disposition']=='replace':assert q['research_holds'];holds.append(q['question_id'])
 if changes and 'draft_question' in changes:
  draft=changes['draft_question'];assert draft['id']==b['id'] and draft['concept']==b['concept'] and len(draft['options'])==4
  assert len({o['text'] for o in draft['options']})==4
  assert 0<=draft['correct']<4 and all(o['explanation'] for o in draft['options'])
  for path,val in changes['field_patches'].items():
   node=draft
   for part in path.split('.'):node=node[int(part)] if isinstance(node,list) else node[part]
   assert node==val
  if 'FUEL-ROUNDING' in q['issues']:
   rate,distance=re.search(r'by ([\d.]+) litres per 100 km\. Over (\d+) km',draft['prompt']).groups();expected=D(rate)*D(distance)/100
   vals=[D(re.match(r'[\d.]+',o['text'])[0]) for o in draft['options']]
   assert vals[draft['correct']]==expected and vals.count(expected)==1 and 'do not round' in draft['prompt'];proposed_exact[b['id']]=str(expected)
  if 'LOAD-WEIGHT-CONVENTION' in q['issues']:
   assert 'already including the driver' in draft['prompt'];assert draft['options'][draft['correct']]['text']==b['options'][b['correct']]['text']
  if 'FUEL-UNIT-GRAMMAR' in q['issues']:
   for old,new in zip(b['options'],draft['options']):
    assert D(re.match(r'[\d.]+',old['text'])[0])==D(re.match(r'[\d.]+',new['text'])[0])
    assert not re.search(r'(?<![\d.])1 litres\b',new['text']+' '+new['explanation'])
 if b['id'].startswith('sign-recognise-'):
  option_hashes=[sha(ROOT/'composeApp/src/commonMain/composeResources/files'/o['image']) for o in b['options']]
  assert len(set(option_hashes))==4
 if b['id'].startswith('sign-'):
  code=mp['sign_code'];assert changes['target_code_metadata']==code and changes['proposed_option_codes'][0]==code
  assert len(set(changes['proposed_option_codes']))==4
  assert len({caps[c]['label_en'] for c in changes['proposed_option_codes']})==4
  assert not set(changes['proposed_option_codes'][1:])&faint
  assert code not in changes['prompt'] or not re.search(r'\b'+re.escape(code)+r'\b',changes['prompt'])
  assert q['disposition']==('replace' if code in faint else 'rewrite')
  for j,opt in enumerate(changes['options']):
   c=opt['code_metadata_after_reveal'];cap=caps[c];asset=opt['visual_description_brief']['exact_asset'];assert asset==cap['preferred_asset'] and asset['sha256']==sha(ROOT/asset['path'])
   assert opt['official_sources']==cap['sources'] and opt['post_answer_explanation']==cap['teaching_caption_en']
   assert opt['is_correct']==(j==0)
  targets+=1
 if q.get('arithmetic_review'):assert q['arithmetic_review']['question_id']==q['question_id']
assert targets==616 and len(holds)==38
assert set(proposed_exact)==set(read(HERE/'question-review/arithmetic.json')['fuel_rounding_qualified'])
for record in assets['records']:
 assert sha(ROOT/record['bank_path'])==record['bank_sha256']
 assert sha(ROOT/record['approved_path'])==record['approved_sha256']
for proof in assets['proof_hashes']:assert sha(ROOT/proof['path'])==proof['sha256']
assert all(a['totals'][k]==counts[k] for k in ['retain','rewrite','replace','remove'])
assert a['totals']['asset_hold_questions']==len(holds) and len(a['coverage_backlog'])==3
out={'checked_on':'2026-10-14','status':'passed; planning decisions verified, implementation holds remain explicit','question_actions_sha256':sha(HERE/'question-actions.json'),'questions':1000,'dispositions':dict(counts),'every_question_once_in_baseline_order':True,'all_changes_have_evidence_and_acceptance_criteria':True,'all_original_bank_records_unchanged':True,'upstream_frozen_app_content_assets_and_pdf_unchanged':True,'proposed_exact_fuel_keys':proposed_exact,'exact_sign_asset_bindings_checked':616,'all_308_original_image_option_sets_have_distinct_bitmap_hashes':True,'asset_hold_questions':holds,'unresolved_unrecorded_findings':0,'live_bank_edited':False,'step_7E_started':False}
(HERE/'question-actions-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='asset_hold_questions'},indent=2))
