"""Independent acceptance checks for 7C; no app/PDF/bank mutations."""
from pathlib import Path
import collections,hashlib,json,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return re.sub(r'\s+','',s).replace('\u00ad','')
m=read(HERE/'question-map.json');bank=read(ROOT/'content/questions.json');base=read(HERE/'baseline.json');cm=read(HERE/'curriculum-map.json');ev=read(HERE/'question-map-evidence.json');old=read(ROOT/'docs/curriculum/question-book-review/all-question-coverage.json')['questions']
assert len(bank)==len(m['questions'])==1000
assert [q['question_id'] for q in m['questions']]==[q['id'] for q in bank]==base['question_ids_in_order']
assert len({q['question_id'] for q in m['questions']})==1000
for x in m['inputs']:assert sha(ROOT/x['path'])==x['sha256'],('Changed input',x['path'])
for x in base['frozen_inputs']+base['bundled_assets']:assert sha(ROOT/x['path'])==x['sha256'],('Stale baseline',x['path'])
assert cm['baseline_sha256']==sha(HERE/'baseline.json')
assert m['release']['sha256']==sha(ROOT/m['release']['path'])==base['release']['sha256']==ev['release']['sha256']
assert read(ROOT/'docs/curriculum/pdf-production/final-review/screen-release.json')['status']=='approved'
lessons={n['id'] for n in cm['curriculum_nodes'] if n['kind']=='lesson'};targets={n['id'] for n in cm['curriculum_nodes']}|{n['id'] for n in cm['sign_entries']};sources={s['id'] for s in cm['source_destinations']};refs={r['id']:r for r in m['source_registry']};source_nodes={r['id']:r for r in cm['source_destinations']};pages={p['page']:p for p in ev['pages']};counts=collections.Counter();related=collections.Counter();qual=[];missing_source_evidence=[]
assert len(refs)==len(m['source_registry'])
for record in base['release_refresh']['changes']:
 assert record['sha256']==next(x['sha256'] for x in base['frozen_inputs'] if x['path']==record['path'])
for entry in refs.values():
 for check in entry['source_checks']:
  obj=read(ROOT/check['path'])
  for segment in check['json_pointer'].split('/')[1:]:
   segment=segment.replace('~1','/').replace('~0','~');obj=obj[int(segment)] if isinstance(obj,list) else obj[segment]
  assert obj==check['record'] and obj['url']==entry['url']

for p in pages.values():assert hashlib.sha256(p['text'].encode()).hexdigest()==p['text_sha256']
for q,b,h in zip(m['questions'],bank,old):
 assert q['concept_id']==b['concept'] and q['category']==b['category']
 assert q['primary_lesson_id'] in lessons and all(x in lessons for x in q['related_lesson_ids'])
 assert q['primary_lesson_id'] not in q['related_lesson_ids']
 assert all(x in targets for x in q['reference_ids']) and all(x in sources for x in q['source_ids'])
 assert q['source_reference_ids'] and all(x in refs for x in q['source_reference_ids'])
 assert set(q['source_reference_ids'])=={x['reference_id'] for x in q['source_evidence']}
 for support in q['source_evidence']:
  if support.get('source_id'):
   node=source_nodes[support['source_id']]
   assert refs[support['reference_id']]['url']==node.get('scoped_urls',{}).get(support['scope'],node['url'])
 assert q['coverage_status']=='covered' and not q['unresolved_mapping_findings']
 assert [e['pdf_page'] for e in q['teaching_evidence']]==h['book_pages']
 assert q['teaching_evidence'] and q['disposition']=='not assessed; 7D'
 for e in q['teaching_evidence']:
  assert e['evidence_id']==f"book-page-{e['pdf_page']:03}" and norm(e['passage']) in norm(pages[e['pdf_page']]['text'])
 if q.get('sign_code'):
  assert 'sign-'+q['sign_code'] in q['reference_ids']
  assert any(q['sign_code'] in e['passage'] for e in q['teaching_evidence'])
  assert all(x['provenance']['caption_id']=='CAP-'+q['sign_code'] for x in q['source_evidence'])
 if h.get('claim_linkage'):assert q['retained_claims']==h['claim_linkage']
 if q['findings']:qual.append(q['question_id']);assert h.get('rounding_qualification')
 if not any(refs[x]['source_checks'] for x in q['source_reference_ids']) and not q.get('sign_code'):missing_source_evidence.append(q['question_id'])
 counts[q['primary_lesson_id']]+=1;related.update(q['related_lesson_ids'])
for row in m['lesson_coverage']:
 assert row['primary_questions']==counts[row['lesson_id']] and row['related_questions']==related[row['lesson_id']]
assert sum(counts.values())==1000 and len(m['lesson_coverage'])==40
assert sorted(qual)==['fuel-saving-150-0.5','fuel-saving-150-1.5','fuel-saving-250-0.5','fuel-saving-250-1.5']
assert not missing_source_evidence,missing_source_evidence
checks={'checked_on':'2026-10-14','step':'7C','status':'passed','questions':1000,'unique_ids_and_bank_order':True,'all_frozen_input_hashes_match':True,'all_lesson_reference_and_source_targets_resolve':True,'approved_passage_substrings_and_page_hashes_match':True,'retained_reviewed_claim_questions':sum(bool(q['retained_claims']) for q in m['questions']),'sign_questions':sum('sign_code' in q for q in m['questions']),'mapping_unresolved':0,'rounding_qualified_question_ids':qual,'lessons_without_primary_questions':[x for x in lessons if not counts[x]],'independent_quality_review':'7D not started','map_sha256':sha(HERE/'question-map.json')}
checks['lessons_without_primary_questions'].sort();(HERE/'question-map-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
