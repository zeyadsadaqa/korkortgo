"""Independent exact-ID scenario/arithmetic/unit audits. No production calculation helpers."""
import hashlib,json,re,sys
from decimal import Decimal
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());BASE=Path(__file__).resolve().parent.parent
read=lambda p:json.loads((ROOT/p).read_text())
digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
text=lambda r:''.join(x.get('text',x.get('expression','')) for x in r)
def resolve(ref):
 p=ref['file']['path'];assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==ref['file']['sha256'];v=read(p)
 for k in ref['locator'].removeprefix('json:').strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
 return v
bank={q['key']['question_id']:q for q in read('content/accepted-assessment-questions.json')['questions']};frozen=read('docs/curriculum/app-migration/verification-evidence/10A3/question-batches.json');cases=[r for r in frozen['all_question_cases'] if r['owner']==sys.argv[1]];task=sys.argv[1];out=BASE/task;out.mkdir(exist_ok=True);rows=[]
receipts={}
for p in (ROOT/'docs/curriculum/app-migration/implementation-evidence').glob('9*/**/question-acceptance.json'):
 for r in json.loads(p.read_text()).get('questions',[]):
  if 'after' in r and r['question_id'] in bank:receipts[r['question_id']]=r
claims={r['question_id']:r for r in read('docs/curriculum/app-migration/verification-evidence/10E15/checked-claims.json')['questions']}
for case in cases:
 q=bank[case['question_id']];qid=q['key']['question_id'];p=text(q['prompt']);ex=text(q['feedback']['explanation']);opts=[text(o['text']) for o in q['options']];key=q['feedback']['correct_option_id'];idx=next(i for i,o in enumerate(q['options']) if o['id']==key);a=receipts[qid];ap=a['after'];checks={};feedback={f['option_id']:text(f['explanation']) for f in q['feedback']['option_feedback']}
 checks['exact approved per-ID prompt/options/key/feedback']=p==ap['prompt'] and opts==[o['text'] for o in ap['options']] and idx==ap['correct'] and ex==ap['explanation'] and all(feedback[o['id']]==ap['options'][i]['explanation'] for i,o in enumerate(q['options']))
 checks['exact current revision/frozen hash/accepted/no hold']=q['key']['revision']==case['revision']==a['after_revision'] and digest(q)==case['accepted_snapshot']['record_sha256'] and q['acceptance']['eligibility']=='accepted' and not q['acceptance']['open_holds']
 checks['exact origin and content acceptance bindings resolve']=bool(resolve(q['origin'])) and bool(resolve(q['acceptance']['content_review']['record']))
 checks['four distinct alternatives with one authored key']=len(set(opts))==len(opts)==4 and key==a['correct_option_id']
 review={}
 if task=='10E15':
  review=claims[qid];checks['scoped independent primary meaning/options review']=review['status']=='supported_with_recorded_limits'
 else:
  if task=='10E16':
   match=re.search(r'total weight \(totalvikt\) (\d+) kg.*weight \(tjänstevikt\) (\d+) kg',p);assert match,qid
   total,ready=map(int,match.groups());answer=Decimal(total-ready);units='kg';values=[Decimal(o.removesuffix(' kg')) for o in opts]
   checks['driver explicitly included once']= 'already including the driver' in p and 'driver is already included' in ex and 'passengers and goods' in ex
   equation=f'{total} − {ready} = {answer} kg';checks['independent equation in every explanation']=all(equation in f for f in [ex,*feedback.values()]);review={'total_kg_from_prompt':total,'ready_kg_from_prompt':ready,'driver_added_or_subtracted_again':False,'calculation':equation,'legal_definition':'../10E15/checked-claims.json: situation-162; fresh primary Vikter headings, no real-vehicle axle/seat/route limit inferred'}
  else:
   match=re.search(r'by ([\d.]+) litres per 100 km\. Over (\d+) km',p)
   if match:rate,distance=map(Decimal,match.groups())
   else:
    match=re.search(r'averages ([\d.]+) litres per 100 km over a (\d+) km',p);assert match,qid
    rate,distance=map(Decimal,match.groups())
   answer=distance*rate/Decimal(100);units='litres';values=[Decimal(re.fullmatch(r'([\d.]+) litres?',o).group(1)) for o in opts]
   equation=f'{distance} × {rate} ÷ 100 = {answer.normalize():f}'
   checks['independent equation in every explanation']=all(equation in f for f in [ex,*feedback.values()]);review={'distance_km_from_prompt':str(distance),'rate_litres_per_100km_from_prompt':str(rate),'calculation':equation,'exact_result_litres':f'{answer.normalize():f}','oracle':'Decimal multiplication/division from prompt numbers, not question ID or old key.'}
   if task=='10E17':
    checks['exact unrounded revision/precision']='exact result' in p and 'do not round' in p and q['key']['revision']=='fuel-exact-r2' and 'not a guaranteed real-world saving' in ex
    review['historical_key']=ap.get('old_key',a.get('arithmetic',{}).get('old_key'));review['historical_scores_mutated']=False
   else:
    checks['singular litre applies to every one-valued option']=all(o=='1 litre' for o,v in zip(opts,values) if v==1)
    residual=[{'location':loc,'text':t} for loc,t in [('prompt',p),('explanation',ex),*[(f'option_feedback/{k}',v) for k,v in feedback.items()]] if '1 litres' in t]
    review['known_residual_1_litres']=residual;review['scope']='Exact six approved option-unit drafts, not a broader prompt/feedback grammar repair. Any editorial correction requires bounded 10L review; no repair made.'
  checks['numeric alternatives distinct and exactly one correct']=len(set(values))==4 and values.count(answer)==1 and values[idx]==answer
  review['option_numeric_checks']=[{'option_id':o['id'],'value':str(v),'unit':units,'equals_independent_result':v==answer} for o,v in zip(q['options'],values)]
 rows.append({'question_id':qid,'revision':q['key']['revision'],'concept_id':q['concept_id'],'category':q['category'],'prompt':p,'options':q['options'],'correct_authored_option_id':key,'feedback':q['feedback'],'teaching_and_sources':q['relationship'],'accepted_status':q['acceptance'],'accepted_snapshot_sha256':digest(q),'checks':checks,'independent_review':review,'status':'pass' if all(checks.values()) else 'fail'})
assert len(rows)==frozen['partition'][task]
name={'10E15':'scenario-review.json','10E16':'load-calculation-audit.json','10E17':'fuel-calculation-audit.json','10E18':'unit-wording-review.json'}[task]
r={'task':task,'date':'2026-10-21','status':'pass' if all(r['status']=='pass' for r in rows) else 'fail','counts':{'questions':len(rows),'checks':sum(len(r['checks']) for r in rows),'failed':sum(not c for r in rows for c in r['checks'].values())},'questions':rows,'limits':'Generic revision/source/lesson/acceptance checks are also linked per ID in 10E1. No accepted payload, source date, production code, identity or historical score modified.'};(out/name).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'task':task,'status':r['status'],'counts':r['counts'],'failures':[(r['question_id'],k) for r in rows for k,v in r['checks'].items() if not v]},indent=2));sys.exit(0 if r['status']=='pass' else 1)
