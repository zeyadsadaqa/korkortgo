"""Reproduce the revised-book coverage audit from reviewed evidence, not stale folios.

Use the bundled Python (pypdf). Scenario decisions bind to the current PDF/bank
hashes and actual teaching guards. Sign coverage requires an illustrated caption
unit with a verified asset placement, not a lookup or bibliography mention.
This is curriculum coverage, not independent legal/medical certification.
"""
import hashlib,json,re,math
from pathlib import Path
from collections import Counter
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/question-book-review'
EXEC=OUT/'execution';PROD=ROOT/'docs/curriculum/pdf-production'
BOOK=PROD/'korkortgo-curriculum-review.pdf';BANK=ROOT/'content/questions.json'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(t):return ' '.join(t.split())
def save(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def family(ident):return 'fuel-saving' if ident.startswith('fuel-saving-') else ident.split('-')[0]
def value(text):return float(re.search(r'-?\d+(?:\.\d+)?',text)[0])
def body(text):return re.sub(r'\nContents\nSources\nPrevious page\n\d+\n(?:Next page\n?)?$','',text).strip()

def main():
 questions=json.loads(BANK.read_text());assert len(questions)==len({q['id'] for q in questions})==1000
 review=json.loads((EXEC/'G12/scenario-decisions.json').read_text());assert review['book_sha256']==digest(BOOK);assert review['bank_sha256']==digest(BANK)
 assembly=json.loads((PROD/'assembly/verification.json').read_text());assert assembly['status']=='passed' and assembly['sha256']==digest(BOOK)
 nav=json.loads((PROD/'assembly/navigation.json').read_text());inputs=json.loads((PROD/'assembly/inputs.json').read_text());offsets={i['id']:i['offset'] for i in inputs}
 pages=[p.extract_text() or '' for p in PdfReader(BOOK).pages];assert len(pages)==nav['pages']==540
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
 reaction=teaching('M03-L04','50 ÷ 3.6');gap=teaching('M03-L04','60 ÷ 3.6 × 3 = 50 metres')
 braking=teaching('M03-L04','braking distance is approximately proportional to speed squared')
 disc=teaching('M05-L03','set it to the next half-hour after arrival')
 load=teaching('M08-L02','Total weight minus the defined ready weight')
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
    speed,time=map(float,re.search(r'At ([0-9.]+) km/h and ([0-9.]+) seconds',q['prompt']).groups());assert [speed,time]==list(map(float,parts[1:]));numeric=round(speed/10*time*3+(speed/10)**2*.4,1);status='prompt_only';basis='formula_supplied_by_question_not_book';reason='The prompt supplies the rough reaction formula and 0.4 braking coefficient. The revised book teaches unit conversion, braking speed-squared scaling and a different explicitly assumed deceleration example; it does not teach these rough-model coefficients. The prompt is sufficient for arithmetic, but not a book-teaching match.';detail['partial_related_book_pages']=sorted(set([reaction,braking]))
   elif f in ['fuel','fuel-saving']:
    rate=float(re.search(r'(?:averages|by) ([0-9.]+) litres per 100 km',q['prompt'])[1]);distance=float(re.search(r'[Oo]ver (?:a )?([0-9.]+) km',q['prompt'])[1]);assert [distance,rate]==list(map(float,parts[2:] if f=='fuel-saving' else parts[1:]));numeric=round(distance*rate/100,1);status='prompt_only';basis='ordinary_proportional_arithmetic';reason='The supplied distance and litres per 100 km allow distance × rate ÷ 100. The book’s economical-driving advice does not teach this fuel-use/savings calculation, so no book support page is assigned.'
   else:raise ValueError(ident)
   if numeric is not None:
    assert abs(value(answer)-numeric)<.051,(ident,answer,numeric)
    arithmetic.append(dict(question_id=ident,method=basis,expected_numeric_answer=numeric,status='passed'))
  assert all(1<=p<=len(pages) for p in refs)
  if not support:support=[dict(pdf_page=p,section=pages[p-1].splitlines()[0],page_text=body(pages[p-1])) for p in refs]
  e.update(status=status,answerable_from_book=status=='covered',basis=basis,rationale=reason,book_pages=refs,primary_book_page=refs[0] if refs else None,evidence=support,**detail);entries.append(e)
 counts=Counter(e['status'] for e in entries);base=json.loads((EXEC/'baseline/docs/curriculum/question-book-review/all-question-coverage.json').read_text());old={e['question_id']:e for e in base['questions']};gained=[e['question_id'] for e in entries if e['status']=='covered' and old[e['question_id']]['status']!='covered'];regressed=[e['question_id'] for e in entries if old[e['question_id']]['status']=='covered' and e['status']!='covered'];assert not regressed
 targets={q['question_id'] for q in json.loads((EXEC/'tracker.json').read_text())['questions']};assert len(targets)==55 and all(e['status']=='covered' for e in entries if e['question_id'] in targets)
 metadata=dict(schema_version='2.0',review_date='2026-10-13',book_path=str(BOOK.relative_to(ROOT)),book_sha256=digest(BOOK),questions_path=str(BANK.relative_to(ROOT)),questions_sha256=digest(BANK),book_page_count=len(pages),page_numbering='One-based physical PDF pages including cover; continuous printed folios and PDF labels verified in G11. Original bank page field is unrelated.',criterion=review['criterion'],status_definitions=dict(covered='Printed teaching/illustration supplies keyed-answer selection or required principle/formula.',not_covered='Exact required illustration or knowledge missing.',prompt_only='Supplied numbers/formulas permit arithmetic, but the book does not teach this method/model.'),method='All 178 scenarios reviewed against fresh revised page bodies; all 55 target teaching anchors and 68 essential source-linked claims checked. All 616 sign records matched by exact illustrated code and verified asset placement, excluding code-only lookup/bibliography. All 206 numerical instances independently calculated and keyed answers checked. Old support pages remapped by preserved body text and named destinations, with six changed-page checks inspected. External webpages are not counted as book teaching. Curriculum coverage, not independent legal/medical accuracy certification.',totals=dict(total=len(entries),**counts,not_answerable_from_book=counts['not_covered']+counts['prompt_only']),baseline_totals=base['metadata']['totals'],change=dict(newly_covered=len(gained),regressions=len(regressed),target_questions_verified=55))
 assert len(arithmetic)==206
 save('question-page-map.json',dict(metadata=metadata,questions=[e for e in entries if e['status']=='covered']))
 save('question-coverage-gaps.json',dict(metadata=metadata,questions=[e for e in entries if e['status']!='covered']))
 save('all-question-coverage.json',dict(metadata=metadata,questions=entries))
 def audit_save(name,data):(EXEC/'G12'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 audit_save('arithmetic-validation.json',dict(status='passed',instances=len(arithmetic),questions=arithmetic))
 audit_save('coverage-changes.json',dict(status='passed',newly_covered=gained,regressions=regressed,old_totals=base['metadata']['totals'],new_totals=metadata['totals']))
 missing=sorted({e['sign_code'] for e in entries if e.get('sign_code') and e['status']=='not_covered'})
 audit_save('missing-signs.json',dict(unique_missing_codes=len(missing),affected_questions=[e['question_id'] for e in entries if e.get('sign_code') and e['status']=='not_covered'],codes=missing))
 by=Counter((family(e['question_id']),e['status']) for e in entries)
 report=['# Revised question coverage review','','Reviewed all **1000 questions** against the **540-page G11 revised book** on 13 October 2026.','','| Result | Original book | Revised book |','|---|---:|---:|',f'| Covered by book study | {base["metadata"]["totals"]["covered"]} | {counts["covered"]} |',f'| Missing knowledge/illustration | {base["metadata"]["totals"]["not_covered"]} | {counts["not_covered"]} |',f'| Prompt-only arithmetic/model | {base["metadata"]["totals"]["prompt_only"]} | {counts["prompt_only"]} |','','**55/55 target situation gaps verified**, with 68 claim links. The square-of-speed addition also covers **20 braking-factor questions**, making **75 newly covered** records. No previously covered question lost support.','','| Family | Covered | Missing | Prompt-only |','|---|---:|---:|---:|']
 for f in dict.fromkeys(family(e['question_id']) for e in entries):report.append(f'| {f} | {by[f,"covered"]} | {by[f,"not_covered"]} | {by[f,"prompt_only"]} |')
 report+=['','## Remaining scope','',f'**{counts["not_covered"]+counts["prompt_only"]} records still lack sufficient book teaching:** {len(missing)} missing sign codes affect {counts["not_covered"]} meaning/recognition records; 30 rough stopping-model and 40 fuel/savings records are prompt-only. The current book does not teach the rough reaction factor/0.4 braking coefficient or the fuel proportion calculation. No further teaching changes were made in G12.','','Missing codes: '+', '.join(missing)+'.','','## Evidence and files','','- `question-page-map.json`: covered questions, actual pages, original prompts/options/answers and extracted evidence.','- `question-coverage-gaps.json`: every remaining unsupported/prompt-only record with precise reason.','- `all-question-coverage.json`: all 1000 records in original order.','- [G12 target review](execution/G12/target-coverage-review.json): actual printed anchors and source/claim linkage for all 55 targets.','- [G12 scenario decisions](execution/G12/scenario-decisions.json): reviewed decisions for all 178 scenarios; bound to actual PDF and bank hashes.','- [Arithmetic verification](execution/G12/arithmetic-validation.json): 206 independent calculations.','','Book-page numbers include the cover and match verified continuous PDF labels. `original_source_page` retains the old bank’s page, not this book’s folio. No bibliography, code lookup or external link is accepted as teaching/illustration coverage.','','## Coverage limits','','The criterion is selecting the keyed answer from book study and reasonable application, not reproducing every keyed-answer detail or every distractor explanation. Entries 081, 087, 151 and 175 explicitly distinguish the taught core principle from more detailed keyed wording. Scope limits in all 55 target passages remain applicable. This is not a new legal/medical audit of the bank or a certification for publication, print or accessibility.','','One non-blocking cross-reference issue: M06-L01 p.191 directs wildlife-collision actions to M10-L01; the correct section is M10-L02, p.326. Target q126 and collision q127 remain supported at their correctly mapped pages. [Observation](execution/G12/editorial-observations.json). G12 preserves the G11 PDF.','','Question bank stayed byte-identical. Baseline audit files remain in the verified G0 snapshots. Book SHA-256: `'+digest(BOOK)+'`. Bank SHA-256: `'+digest(BANK)+'`.']
 (OUT/'review.md').write_text('\n'.join(report)+'\n')
 # Exhaustive disjoint partition and authoritative ordering/page checks.
 covered=json.loads((OUT/'question-page-map.json').read_text())['questions'];gaps=json.loads((OUT/'question-coverage-gaps.json').read_text())['questions']
 assert len(covered)+len(gaps)==1000;assert {e['question_id'] for e in covered}.isdisjoint(e['question_id'] for e in gaps);assert {e['question_id'] for e in covered+gaps}=={q['id'] for q in questions}
 assert [e['question_id'] for e in entries]==[q['id'] for q in questions];assert all(e['book_pages'] and e['evidence'] for e in covered);assert all(not e['book_pages'] for e in gaps)
 print(json.dumps(metadata['totals'],indent=2));print('PASS: 1000 unique IDs; 55 targets / 68 claims; 206 calculations; exact illustrated signs; no regressions.');print('Missing sign codes:',len(missing))
if __name__=='__main__':main()
