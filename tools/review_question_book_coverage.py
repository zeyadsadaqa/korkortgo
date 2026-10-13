"""Reproduce the revised-book coverage audit from reviewed evidence, not stale folios.

Use the bundled Python (pypdf). Scenario decisions bind to the current PDF/bank
hashes and actual teaching guards. Sign coverage requires an illustrated caption
unit with a verified asset placement, not a lookup or bibliography mention.
This is curriculum coverage, not independent legal/medical certification.
"""
import hashlib,json,re,math
import copy
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from collections import Counter
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/question-book-review'
LEDGER=OUT/'g-step-changes.json';PROD=ROOT/'docs/curriculum/pdf-production'
BOOK=PROD/'korkortgo-curriculum-review.pdf';BANK=ROOT/'content/questions.json'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(t):return ' '.join(t.split())
def save(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def family(ident):return 'fuel-saving' if ident.startswith('fuel-saving-') else ident.split('-')[0]
def value(text):return float(re.search(r'-?\d+(?:\.\d+)?',text)[0])
def body(text):return re.sub(r'\nContents\nSources\nPrevious page\n\d+\n(?:Next page\n?)?$','',text).strip()
def teaching_body(text):return norm(re.split(r'\nContents\nSources(?: and references)?\n',text)[0])

def main():
 questions=json.loads(BANK.read_text());assert len(questions)==len({q['id'] for q in questions})==1000
 ledger=json.loads(LEDGER.read_text());records=ledger['records']
 review=copy.deepcopy(records['G12/scenario-decisions.json']);assert review['bank_sha256']==digest(BANK)
 h0=json.loads((OUT/'remaining-gap-h0-sources.json').read_text())
 assert digest(BANK)==h0['baseline']['questions']['sha256']
 assert digest(BOOK)==digest(ROOT/'output/pdf/korkortgo-curriculum-review.pdf')
 audit_path=OUT/'remaining-gap-h7-audit.json'
 if audit_path.exists():
  previous=json.loads(audit_path.read_text())['previous_audit']
 else:
  prior=json.loads((OUT/'all-question-coverage.json').read_text())
  assert prior['metadata']['book_sha256']==review['book_sha256']
  previous=dict(metadata=prior['metadata'],statuses={e['question_id']:e['status'] for e in prior['questions']},
                scenario_pages={str(ev['pdf_page']):ev['page_text'] for e in prior['questions'] if family(e['question_id'])=='situation' for ev in e['evidence']})
  previous['gaps_snapshot']=(OUT/'question-coverage-gaps.json').read_text()
 assert hashlib.sha256(previous['gaps_snapshot'].encode()).hexdigest()==h0['baseline']['gaps']['sha256']
 assert previous['metadata']['totals']['covered']==772
 prior_gaps=json.loads(previous['gaps_snapshot'])['questions'];gap_statuses={e['question_id']:e['status'] for e in prior_gaps}
 assert set(previous['statuses'])=={q['id'] for q in questions}
 assert previous['statuses']=={q['id']:gap_statuses.get(q['id'],'covered') for q in questions}
 assembly=json.loads((PROD/'assembly/verification.json').read_text());assert assembly['status']=='passed' and assembly['sha256']==digest(BOOK)
 nav=json.loads((PROD/'assembly/navigation.json').read_text());inputs=json.loads((PROD/'assembly/inputs.json').read_text());offsets={i['id']:i['offset'] for i in inputs}
 reader=PdfReader(BOOK);pages=[p.extract_text() or '' for p in reader.pages];assert len(pages)==nav['pages']==578
 assert reader.page_labels==[str(p) for p in range(1,579)]
 # Remap retained semantic decisions by preserved teaching bodies, never offsets.
 remap={}
 for old,text in previous['scenario_pages'].items():
  matches=[p for p,t in enumerate(pages,1) if teaching_body(t)==teaching_body(text)]
  assert len(matches)==1,('changed scenario teaching requires review',old,matches)
  remap[int(old)]=matches[0]
 for d in review['questions']:
  d['book_pages']=[remap[p] for p in d['book_pages']]
  d['primary_book_page']=d['book_pages'][0]
  for guard in d.get('required_teaching_anchors',[]):guard['pages']=[remap[p] for p in guard['pages']]
  for guard in d.get('evidence_guards',[]):
   old=guard['pdf_page'];guard['historical_page_sha256']=guard['body_sha256']
   prior_page=previous['scenario_pages'][str(old)]+f'\nContents\nSources\nPrevious page\n{old}\nNext page'
   assert hashlib.sha256(norm(prior_page).encode()).hexdigest()==guard['body_sha256'],d['question_id']
   guard['pdf_page']=remap[old];guard['body_sha256']=hashlib.sha256(norm(pages[remap[old]-1]).encode()).hexdigest()
 decisions={d['question_id']:d for d in review['questions']};assert len(decisions)==178
 assert set(decisions)=={q['id'] for q in questions if q['id'].startswith('situation-')}
 # All teaching guard checks are run against fresh PDF extraction on every run.
 for ident,d in decisions.items():
  assert d['status']=='covered' and d['reviewed_on']=='2026-10-13'
  for g in d.get('required_teaching_anchors',[]):assert all(g['phrase'].lower() in norm(pages[p-1]).lower() for p in g['pages']),ident
  for g in d.get('evidence_guards',[]):assert hashlib.sha256(norm(pages[g['pdf_page']-1]).encode()).hexdigest()==g['body_sha256'],ident
  assert d.get('required_teaching_anchors') or d.get('evidence_guards'),ident
 # Exact placements in the verified chapter/reference components establish image presence.
 placements={}
 for i in inputs:
  if i['id']=='front':continue
  art=json.loads((PROD/'reference/assets.json' if i['id']=='reference' else PROD/f"chapters/{i['id']}/illustrations.json").read_text())
  if 'official_sign_placements' not in art:
   assert i['id'] in ['M01','M02']  # These chapters have scene assets, no independent sign-caption units.
  for rec in art.get('official_sign_placements',[]):
   assert digest(ROOT/rec['path'])==rec['sha256']
   placements.setdefault(rec['code'],set()).add(i['offset']+rec['page'])
 signs={}
 for code,where in placements.items():
  for p in sorted(where):
   match=re.search(r'(?:^|\n)'+re.escape(code)+r' · ([^\n]+)\n',pages[p-1])
   assert match,(code,p)
   # End at the next caption unit, not a code-only lookup line or source section.
   next_unit=re.search(r'\n[A-Z]+\d+(?:[a-z]|-\d+)? · ',pages[p-1][match.end():])
   end=match.end()+next_unit.start() if next_unit else len(body(pages[p-1]))
   signs.setdefault(code,[]).append(dict(pdf_page=p,excerpt=norm(pages[p-1][match.start():end]),illustration_asset_verified=True))
 # Calculation anchors are semantic searches inside specific lessons, not fixed page numbers.
 def teaching(lesson,phrase):
  start=nav['destinations'][lesson];next_lessons=[n for k,n in nav['destinations'].items() if re.fullmatch(r'M\d\d-(?:L\d\d|R)',k) and n>start]
  end=min(next_lessons) if next_lessons else len(pages)+1
  found=[p for p in range(start,end) if phrase.lower() in norm(pages[p-1]).lower()];assert len(found)==1,(lesson,phrase,found);return found[0]
 reaction=teaching('M03-L04','metres per second: 50 ÷ 3.6.');gap=teaching('M03-L04','60 ÷ 3.6 × 3 = 50 metres')
 braking=teaching('M03-L04','braking distance is approximately proportional to speed squared')
 disc=teaching('M05-L03','set it to the next half-hour after arrival')
 load=teaching('M08-L02','Total weight minus the defined ready weight')
 rough=teaching('M03-L04','A rough calculation method');rough_examples=teaching('M03-L04','Apply the rough model')
 fuel=teaching('M09-L02','Calculate journey consumption and savings');rounding=teaching('M09-L02','Exact values and displayed answers')
 assert [rough,rough_examples,fuel,rounding]==[86,87,298,299]
 teaching_guards={rough:['R = (v ÷ 10) × t × 3 metres','B = (v ÷ 10)² × 0.4 metres','S = R + B','commercial teaching source','good-brake, good-tyre and dry-asphalt'],
  rough_examples:['6 + 6.4 = 12.4 m','21 + 19.6 = 40.6 m','30 + 10 = 40 m','27.8 m','8% overestimate'],
  fuel:['journey litres = distance in km × consumption in litres/100 km ÷ 100','litres saved = distance in km × reduction in litres/100 km ÷ 100','7.8 litres','4.5 litres','editorial arithmetic'],
  rounding:['ties-to-even','exactly 0.75 litres','2.25 litres, displayed as 2.2','exactly 1.25 litres','exactly 3.75 litres','report the exact result']}
 for p,phrases in teaching_guards.items():assert all(phrase in norm(pages[p-1]) for phrase in phrases),(p,phrases)
 bank_signs={s['code']:s for s in json.loads((ROOT/'content/signs.json').read_text())}
 entries=[];arithmetic=[]
 for position,q in enumerate(questions,1):
  ident=q['id'];answer=q['options'][q['correct']]['text'];f=family(ident)
  e=dict(question_id=ident,question_number=position,category=q['category'],prompt=q['prompt'],options=q['options'],correct_option_index=q['correct'],correct_answer=answer,question_explanation=q['explanation'],question_image=q.get('image',''),original_source_page=q.get('page'))
  refs=[];support=[];status='covered';detail={}
  if f=='situation':
   d=decisions[ident];assert answer==d['keyed_answer'] and q['prompt']==d['prompt'];refs=d['book_pages'];basis=d['basis'];reason=d['rationale']
   detail={k:d[k] for k in ['lesson','claim_ids','claim_linkage','coverage_limit','coverage_detail_limit','semantic_review','required_teaching_anchors'] if k in d}
  elif f=='sign':
   code=ident.split('-',2)[2];support=signs.get(code,[]);refs=[x['pdf_page'] for x in support];e['sign_code']=code
   expected_image=bank_signs[code]['image'];assert answer==bank_signs[code]['label'] if ident.startswith('sign-meaning-') else answer=='Illustration '+code
   assert (q['image'] if ident.startswith('sign-meaning-') else q['options'][q['correct']]['image'])==expected_image
   if ident.startswith('sign-recognise-'):assert answer=='Illustration '+code and q['options'][q['correct']]['image']
   else:assert q['image'] and f'({code})' in q['prompt']
   status='covered' if refs else 'not_covered';basis='illustrated_sign_entry' if refs else 'missing_sign_entry'
   reason=f'The verified book illustrates and explains exact code {code}; English editorial labels may differ from the bank.' if refs else f'No illustrated caption unit for {code} exists in the revised book. A family overview, lookup, source link or related sign cannot teach this exact illustration.'
  else:
   parts=ident.split('-');numeric=None
   if f in ['reaction','gap']:
    speed=float(re.search(r'At ([0-9.]+) km/h',q['prompt'])[1]);time=float(re.search(r'reaction time of ([0-9.]+) seconds|a ([0-9.]+)-second',q['prompt']).group(1 if f=='reaction' else 2));assert [speed,time]==list(map(float,parts[1:]));numeric=round(speed/3.6*time,1);refs=[reaction] if f=='reaction' else list(dict.fromkeys([gap,reaction]));basis='application_of_book_calculation';reason='Apply the taught speed ÷ 3.6 × seconds relationship with the supplied speed/time. This is distance at assumed constant speed, not a guarantee of safe reaction/following distance.'
   elif f=='disc':
    hour,minute=map(int,re.search(r'at ([0-9]{2}):([0-9]{2})',q['prompt']).groups());assert [hour,minute]==list(map(int,parts[1:]));minutes=int(math.ceil((hour*60+minute)/30))*30;expected=f'{minutes//60%24:02d}:{minutes%60:02d}';assert answer==expected
    refs=[disc];basis='application_of_book_rule';reason='The book teaches setting the disc to the next half-hour after arrival. Apply it to the stated arrival under the active restriction.';arithmetic.append(dict(question_id=ident,method='next half-hour',expected_answer=expected,status='passed'))
   elif f=='load':
    total,ready=map(float,re.search(r'total weight ([0-9.]+) kg and unladen weight ([0-9.]+) kg',q['prompt']).groups());numeric=total-ready;assert [ready,numeric]==list(map(float,parts[1:]));refs=[load];basis='application_of_book_calculation';reason='Use the book’s maximum-load relationship: registered total weight minus defined ready/unladen weight, with the question’s figures; do not add the driver twice.'
   elif f=='braking':
    initial,factor=map(float,re.search(r'braking distance of ([0-9.]+) m.*speed becomes ([0-9.]+) times',q['prompt']).groups());assert [initial,factor]==list(map(float,parts[1:]));numeric=initial*factor**2;refs=[braking];basis='application_of_book_calculation';reason='The book now teaches braking distance proportional to speed squared for unchanged grip/deceleration/gradient. Multiply initial braking distance by the square of the speed factor; reaction distance is excluded.';detail['newly_covered_by']='G3 square-of-speed teaching'
   elif f=='stopping':
    speed,time=map(Decimal,re.search(r'At ([0-9.]+) km/h and ([0-9.]+) seconds',q['prompt']).groups());assert [speed,time]==list(map(Decimal,parts[1:]));r=speed*Decimal('0.3')*time;b=speed**2*Decimal('0.004');exact=r+b;numeric=float(exact);assert Decimal(str(value(answer)))==exact
    for explanation in [q['explanation']]+[o['explanation'] for o in q['options']]:
     assert list(map(Decimal,re.search(r'Reaction: ([0-9.]+) m\. Braking: ([0-9.]+) m\. Total: ([0-9.]+) m',explanation).groups()))==[r,b,exact]
    refs=[rough,rough_examples];basis='application_of_book_approximate_model';reason='Apply the printed rough exercise reaction and braking equations, then add. Keep this model separate from exact unit conversion and actual stopping predictions; dry-asphalt/good-brake/good-tyre assumptions and commercial shortcut provenance are printed.'
    detail['calculation']=dict(speed_kmh=str(speed),reaction_seconds=str(time),reaction_metres=str(r),braking_metres=str(b),exact_model_total_metres=str(exact))
   elif f in ['fuel','fuel-saving']:
    rate=Decimal(re.search(r'(?:averages|by) ([0-9.]+) litres per 100 km',q['prompt'])[1]);distance=Decimal(re.search(r'[Oo]ver (?:a )?([0-9.]+) km',q['prompt'])[1]);assert [distance,rate]==list(map(Decimal,parts[2:] if f=='fuel-saving' else parts[1:]));exact=distance*rate/100;key=Decimal(str(value(answer)));qualified=exact!=key;numeric=float(exact.quantize(Decimal('0.1'),rounding=ROUND_HALF_EVEN))
    assert key==exact or key==exact.quantize(Decimal('0.1'),rounding=ROUND_HALF_EVEN)
    for explanation in [q['explanation']]+[o['explanation'] for o in q['options']]:assert Decimal(re.search(r'= ([0-9.]+) litres',explanation)[1])==exact
    refs=[fuel]+([rounding] if qualified else []);basis='application_of_book_fuel_arithmetic';reason='Apply the printed distance × litres-per-100-km rate ÷ 100 calculation using supplied exercise assumptions; savings rates are not guaranteed benefits.'
    detail['calculation']=dict(distance_km=str(distance),litres_per_100_km=str(rate),exact_litres=str(exact),keyed_litres=str(key),exact_key_match=not qualified)
    if qualified:
     assert ident in h0['findings']['rounding'];detail['rounding_qualification']='Prompt omits precision/convention. Printed page 299 discloses this existing key as one-decimal ties-to-even; coverage supports keyed selection with that qualification, not exact equality or a corrected prompt.'
     reason+=' The printed rounding disclosure permits selection of the existing rounded key; the original prompt omission remains.'
   else:raise ValueError(ident)
   if numeric is not None:
    assert abs(value(answer)-numeric)<.051,(ident,answer,numeric)
    arithmetic.append(dict(question_id=ident,method=basis,expected_numeric_answer=numeric,status='passed'))
  assert all(1<=p<=len(pages) for p in refs)
  if not support:support=[dict(pdf_page=p,section=pages[p-1].splitlines()[0],page_text=body(pages[p-1])) for p in refs]
  e.update(status=status,answerable_from_book=status=='covered',basis=basis,rationale=reason,book_pages=refs,primary_book_page=refs[0] if refs else None,evidence=support,**detail);entries.append(e)
 counts=Counter(e['status'] for e in entries);base=records['baseline-coverage.json'];old={e['question_id']:e for e in base['questions']};gained=[e['question_id'] for e in entries if e['status']=='covered' and old[e['question_id']]['status']!='covered'];regressed=[e['question_id'] for e in entries if old[e['question_id']]['status']=='covered' and e['status']!='covered'];assert not regressed
 targets={q['question_id'] for q in records['tracker.json']['questions']};assert len(targets)==55 and all(e['status']=='covered' for e in entries if e['question_id'] in targets)
 metadata=dict(review_date='2026-10-13',book_path=str(BOOK.relative_to(ROOT)),book_sha256=digest(BOOK),questions_path=str(BANK.relative_to(ROOT)),questions_sha256=digest(BANK),book_page_count=len(pages),criterion=review['criterion'],status_definitions=dict(covered='Printed teaching/illustration supplies keyed-answer selection or required principle/formula; retained rounding qualifications apply.',not_covered='Exact required illustration or knowledge missing.',prompt_only='Supplied numbers/formulas permit arithmetic, but the book does not teach this method/model.'))
 assert len(arithmetic)==206
 h7_gained=[e['question_id'] for e in entries if e['status']=='covered' and previous['statuses'][e['question_id']]!='covered']
 assert set(h7_gained)=={t['question_id'] for t in h0['targets']}
 assert all(e['status']=='covered' for e in entries if previous['statuses'][e['question_id']]=='covered')
 assert counts['covered']==1000 and counts['not_covered']==counts['prompt_only']==0
 qualifications=[e['question_id'] for e in entries if 'rounding_qualification' in e]
 assert set(qualifications)==set(h0['findings']['rounding'])
 metadata.update(schema_version='3.0',audit_step='H7',page_numbering='One-based physical PDF pages including cover; continuous printed folios and PDF labels verified in H6. Original bank page field is unrelated.',
  method='Fresh extraction of all 578 pages. All 178 retained scenario decisions checked against exactly preserved teaching bodies and remapped anchors/guards, retaining 55 target decisions and 68 claim links. All 616 sign questions matched to exact illustrated caption units and hashed asset placements. All 206 numerical instances recalculated from prompt inputs; new stopping/fuel calculations use Decimal. Four fuel midpoint keys remain qualified by printed rounding disclosure. External links, lookup and bibliography are not teaching evidence.',
  totals=dict(total=1000,covered=1000,not_covered=0,prompt_only=0,not_answerable_from_book=0),
  baseline_totals=previous['metadata']['totals'],change=dict(newly_covered=228,regressions=0,previously_covered_preserved=772,target_questions_verified=228),rounding_qualified_questions=qualifications)
 save('question-page-map.json',dict(metadata=metadata,questions=[e for e in entries if e['status']=='covered']))
 save('question-coverage-gaps.json',dict(metadata=metadata,questions=[e for e in entries if e['status']!='covered']))
 save('all-question-coverage.json',dict(metadata=metadata,questions=entries))
 def audit_save(name,data):
  audit_records[name]=data
 audit_records={}
 audit_save('arithmetic-validation.json',dict(status='passed',instances=len(arithmetic),questions=arithmetic))
 audit_save('coverage-changes.json',dict(status='passed',newly_covered=h7_gained,regressions=[],old_totals=previous['metadata']['totals'],new_totals=metadata['totals']))
 missing=sorted({e['sign_code'] for e in entries if e.get('sign_code') and e['status']=='not_covered'})
 audit_save('missing-signs.json',dict(unique_missing_codes=len(missing),affected_questions=[e['question_id'] for e in entries if e.get('sign_code') and e['status']=='not_covered'],codes=missing))
 by=Counter((family(e['question_id']),e['status']) for e in entries)
 report=['# Final question coverage review','',
  'H7 reviewed all **1,000 questions** against the final **578-page book** on 13 October 2026. **1,000 covered, 0 not-covered, 0 prompt-only**, under the existing keyed-answer-selection criterion. Four fuel answers retain the rounding qualifications below.','',
  '| Result | Prior G12 book | Final H7 book |','|---|---:|---:|','| Covered | 772 | 1000 |','| Missing teaching/illustration | 158 | 0 |','| Prompt-only | 70 | 0 |','',
  'All 772 previously covered records retain support. The 228 gains are 158 exact sign meaning/recognition questions (79 codes), 30 rough stopping calculations and 40 fuel calculations. The bank and both final PDFs retain their approved hashes.','',
  '| Family | Covered | Missing | Prompt-only |','|---|---:|---:|---:|']
 for f in dict.fromkeys(family(e['question_id']) for e in entries):report.append(f'| {f} | {by[f,"covered"]} | 0 | 0 |')
 report+=['','## Verification','',
  'All 178 scenario decisions were checked against freshly extracted, exactly preserved teaching bodies; supporting pages and teaching guards were remapped to final folios. The retained 55 target decisions and 68 source-linked claims keep their original semantic scope. All 616 sign records require actual illustrated caption units and verified asset placements. All 206 numerical instances were recalculated from their prompt inputs; the 70 new calculations use exact Decimal arithmetic.','',
  'Stopping equations/assumptions and examples are on pages 86–87. Fuel equations/examples are on page 298; precision and rounding disclosure are on page 299. Every covered record includes actual final teaching-page evidence. PDF labels 1–578, source/delivery equality, bank hash, complete ID ordering, disjoint output partition and zero regressions pass.','',
  '## Retained rounding qualifications','',
  'Four savings prompts omit precision and rounding convention. Page 299 explicitly teaches the existing one-decimal ties-to-even keys. These are covered for keyed-answer selection with that printed disclosure; coverage does not erase the prompt omission or assert exact equality.','',
  '| Question | Exact litres | Keyed litres |','|---|---:|---:|']
 for e in entries:
  if 'rounding_qualification' in e:report.append(f'| `{e["question_id"]}` | {e["calculation"]["exact_litres"]} | {e["calculation"]["keyed_litres"]} |')
 report+=['','## Evidence and limits','',
  '- [All-question coverage](all-question-coverage.json): all 1,000 records in bank order, final pages and extracted evidence.',
  '- [Question-page map](question-page-map.json): all 1,000 covered records.',
  '- [Coverage gaps](question-coverage-gaps.json): empty question list with final metadata.',
  '- [H7 audit](remaining-gap-h7-audit.json): prior status/page evidence, remap, 206 arithmetic checks, gains and qualifications.',
  '- [Execution plan](remaining-gap-execution-plan.md): H0–H7 decisions and validation.',
  '- [Historical G-step evidence](g-step-changes.json): preserved original audit and source/claim limits.','',
  'The criterion is selecting the keyed answer from printed teaching and reasonable application, not reproducing every distractor explanation or certifying every bank claim. Existing scenario detail limits, source retrieval limits, and review-edition print/accessibility/publication limits remain. No new legal/medical or live external-source audit is claimed.','',
  'The retained wildlife-collision cross-reference observation now concerns M06-L01 page 193: it points to M10-L01, while the relevant lesson is M10-L02 page 330. Both affected questions retain correctly mapped teaching evidence.','',
  'Book SHA-256: `'+digest(BOOK)+'`. Bank SHA-256: `'+digest(BANK)+'`.']
 (OUT/'review.md').write_text('\n'.join(report)+'\n')
 save('remaining-gap-h7-audit.json',dict(metadata=metadata,status='passed',previous_audit=previous,
  scenario_page_remap={str(k):v for k,v in remap.items()},scenario_decisions=list(decisions.values()),
  validations=audit_records,h7_newly_covered=h7_gained,rounding_qualifications=[e for e in entries if 'rounding_qualification' in e],
  teaching_guards={str(p):phrases for p,phrases in teaching_guards.items()},
  outputs={name:digest(OUT/name) for name in ['all-question-coverage.json','question-page-map.json','question-coverage-gaps.json','review.md']},
  protected_inputs=dict(book_sha256=digest(BOOK),delivery_sha256=digest(ROOT/'output/pdf/korkortgo-curriculum-review.pdf'),bank_sha256=digest(BANK),historical_ledger_sha256=digest(LEDGER))))
 # Exhaustive disjoint partition and authoritative ordering/page checks.
 covered=json.loads((OUT/'question-page-map.json').read_text())['questions'];gaps=json.loads((OUT/'question-coverage-gaps.json').read_text())['questions']
 assert len(covered)+len(gaps)==1000;assert {e['question_id'] for e in covered}.isdisjoint(e['question_id'] for e in gaps);assert {e['question_id'] for e in covered+gaps}=={q['id'] for q in questions}
 assert [e['question_id'] for e in entries]==[q['id'] for q in questions];assert all(e['book_pages'] and e['evidence'] for e in covered);assert all(not e['book_pages'] for e in gaps)
 print(json.dumps(metadata['totals'],indent=2));print('PASS: H7: 1000 unique covered IDs; 228 gains; prior 772 preserved; 206 calculations; four rounding qualifications retained.');print('Missing sign codes:',len(missing))
if __name__=='__main__':main()
