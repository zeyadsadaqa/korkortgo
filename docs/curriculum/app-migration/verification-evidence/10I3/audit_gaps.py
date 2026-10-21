"""Independent accepted-bank gap counts and bounded editorial review of unchanged9N briefs."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent;BASE=HERE.parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(label,test):checks.append({'check':label,'pass':bool(test)})
actual=read(HERE/'compiled-gap-observations.json');authored=read(ROOT/'content/accepted-assessment-questions.json')['questions'];baseline=read(ROOT/'docs/curriculum/app-migration/question-map.json')['questions'];manifest=read(ROOT/'content/accepted-content-manifest.json');backlog=read(ROOT/'docs/curriculum/app-migration/question-actions.json')['coverage_backlog']
check('exactacceptedidentity',actual['identity']==manifest['identity'])
check('1000accepted0held500concepts',actual['release_accepted'] and actual['accepted_questions']==1000 and actual['held_questions']==0 and actual['concepts']==500)
ids=[q['key']['question_id'] for q in actual['questions']]
check('unchanged1000baselineIDset',len(ids)==len(set(ids))==1000 and set(ids)=={q['question_id'] for q in baseline}=={q['key']['question_id'] for q in authored})
compiled={q['key']['question_id']:q for q in actual['questions']}
for q in authored:
 a=compiled[q['key']['question_id']];check('unchangedauthoredrelationship '+q['key']['question_id'],a['key']==q['key'] and a['concept_id']==q['concept_id'] and a['eligibility']==q['acceptance']['eligibility']=='accepted' and a['relationship']==q['relationship'])
brief_path=ROOT/'docs/curriculum/app-migration/assessment-coverage-briefs.md';text=brief_path.read_text();headings=list(re.finditer(r'^## (M\d+-L\d+) · (.+?) — (9N\d)$',text,re.M));check('threeexactbriefs',len(headings)==3)
reviews={
 'M01-L01':{'objective':'Explain a preparation checklist with entitlement, permits, supervision, risk training and test-readiness boundaries.','format':'Proposed unscored text checklist with supplied dated fictional records; no new screen, artwork or personal-data entry.','rubric':['Entitlement and permit','Practice stage','Training stage','Examination stage','Actionable preparation','Explanation and uncertainty'],'review':'Six checkable criteria cover all supplied stages. Missing approval/permit, incomplete training before tests and retroactive date extensions cannot be treated as ready. Unknown facts require named record/source verification. Rubric is not an app score or official threshold.','source_scope':'Brief dated19October; no refresh of frozen manuscript/release dates or new legal-currency certification.'},
 'M07-L04':{'objective':'Reassess accumulated conditions, explain reduced margins and justify adaptation, stopping or changing/cancelling a plan.','format':'Proposed unscored three-stage text decision record; initial manageable adaptation, safe-stop route check, final refusal to resume with an unfit driver.','rubric':['Detect change','Explain combined risk','Adapt proportionately','Reassess and choose alternatives','Respect the continuation boundary','Explain and reflect'],'review':'Six criteria test carried-forward facts and combined risk, rather than a hazard list or numerical risk score. Safe alternatives may vary where supplied facts support them; the final no-continuation boundary cannot be waived by coffee, reduced speed or proximity.','source_scope':'Frozen brief cites official regulation/syllabus; any later author must recheck exact provisions. Related situation-053 remains primarily M01-L04.'},
 'M10-L03':{'objective':'Explain a complete outward/return journey, distinguish evidence from assumptions, identify unsafe choices and propose actionable safer alternatives.','format':'Proposed unscored five-stage journey review/reflection. Explicit geometry, crossing-distance, traffic and clear-path facts prevent hidden-fact scoring.','rubric':['Whole-journey coverage','Evidence and rationale','Hazard recognition','Safe alternatives','Process versus outcome','Actionable reflection'],'review':'Six criteria cover all five stages and require both sound and unsafe choices to be explained. No-collision luck does not validate an unsafe stop/overtake; written reflection does not certify real driving competence. Accept feasible safe alternatives with supported reasoning.','source_scope':'Original integrative teaching proposal, not an official test/court case; source dates unchanged and future authors must recheck provisions.'}}
rows=[]
for i,h in enumerate(headings):
 id,title,brief=h.groups();end=headings[i+1].start() if i+1<len(headings) else len(text);section=text[h.start():end]
 line=text[:h.start()].count('\n')+1;rubric=section.split('### Checkable acceptance rubric',1)[1].split('### Output boundary',1)[0]
 criteria=[line.split('|')[1].strip() for line in rubric.splitlines() if line.startswith('|') and not line.startswith('| ---')][1:]
 review=reviews[id];check(id+' sixexactrubricrows',criteria==review['rubric'])
 check(id+' explicitlyunscoredfutureproposal','unscored' in section and 'proposed content requires a separate content decision' in section)
 check(id+' rubricnotappscore','not an app score' in section)
 expected=next(r for r in backlog if r['lesson_id']==id)
 primary=[q['key']['question_id'] for q in authored if q['relationship']['primary_lesson_id']==id]
 related=[q['key']['question_id'] for q in authored if id in q['relationship']['related_lesson_ids']]
 observed=next(r for r in actual['gaps'] if r['id']==id)
 check(id+' frozenprimaryrelatedcounts',len(primary)==expected['primary_count']==0 and len(related)==expected['related_count'] and primary==observed['primary_question_ids'] and related==observed['related_question_ids'])
 check(id+' actualApprenderedunscoredcheck',observed['status']=='pass_shared_scope' and observed['existing_unscored_check_revealed_deliberately'] and not observed['scored_test_auto_started'])
 if id=='M07-L04':check(id+' exactsoleassociation',related==['situation-053'] and compiled['situation-053']['relationship']['primary_lesson_id']=='M01-L04')
 rows.append({'lesson_id':id,'title':title,'brief':brief,'status':'pass_existing_scope','brief_location':{'path':str(brief_path.relative_to(ROOT)),'heading_line':line,'sha256':sha(brief_path)},'primary_question_ids':primary,'related_question_ids':related,'teaching_discoverability':['../10I1/shared-route-observations.json','../10I1/shared-reader-observations.json','../10I2/compiled-search-observations.json','compiled-gap-observations.json'],'disclosure_location':'7D coverage_backlog,9N brief introductory/input/output sections and this review; no new learner-facing coverage screen is claimed.','editorial_review':review,'rubric_criteria':criteria,'future_authoring_acceptance':'Independent second review required by each brief before future acceptance; all rows met, equivalent safe reasoning allowed, no invented hidden facts.','became_scored_content':False,'completion_or_mastery_awarded':False})
result={'task':'10I3','status':'pass_existing_coverage_and_brief_scope' if all(c['pass'] for c in checks) else 'fail','identity':actual['identity'],'accepted_count':1000,'held_count':0,'concept_count':500,'gaps':rows,'checks':checks,'totals':{'gaps':3,'briefs':3,'rubric_criteria':18,'checks':len(checks)},'limits':['This is an audit of unchanged proposals and existing teaching, not authorization to implement their proposed exercises.','No new current legal advice/source-currency certification; dated9N checks remain their original evidence, with fresh source work assigned elsewhere.','Shared App journeys do not replace native/large-font/theme delivery evidence in10K.','No new scored ID, altered relationship, durable history, learner completion record or mastery transfer was created.'],'input_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [brief_path,ROOT/'content/accepted-content-manifest.json',ROOT/'content/accepted-assessment-questions.json',ROOT/'docs/curriculum/app-migration/question-actions.json']}}
(HERE/'coverage-gap-review.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ['status','totals']}))
for c in checks:
 if not c['pass']:print('FAILED',c['check'])
assert all(c['pass'] for c in checks)
