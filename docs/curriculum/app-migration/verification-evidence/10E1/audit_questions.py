"""Independent full-ID/retained-payload and accepted compiled contract audit. No production helpers imported."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent;BASE=HERE.parent
cache={}
def read(path):
 p=ROOT/path
 if p not in cache:cache[p]=json.loads(p.read_text())
 return cache[p]
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def text(r):return ''.join(n.get('text',n.get('expression','')) if n['type'] in ['text','math'] else text(n.get('children',n.get('label',[]))) for n in r)
def resolve(origin):
 p=origin['file']['path'];assert sha(p)==origin['file']['sha256'],p;v=read(p)
 for key in origin['locator'].removeprefix('json:').strip('/').split('/'):
  v=v[int(key)] if isinstance(v,list) else v[key.replace('~1','/').replace('~0','~')]
 return v
q=read('content/accepted-assessment-questions.json')['questions'];actions=read('docs/curriculum/app-migration/question-actions.json')['questions'];am={a['question_id']:a for a in actions};frozen=read('docs/curriculum/app-migration/verification-evidence/10A3/question-batches.json');cases={x['question_id']:x for x in frozen['all_question_cases']};compiled=read('docs/curriculum/app-migration/verification-evidence/10E1/compiled-question-contracts.json')['questions'];cm={x['key']['question_id']:x for x in compiled};qm={x['question_id']:x for x in read('docs/curriculum/app-migration/question-map.json')['questions']};curriculum=read('content/curriculum.json');docs={x['id'] for x in curriculum['documents']};sources=read('content/package-sources.json');refs={x['id']:x for x in sources['references']};dest={x['id']:x for x in sources['destinations']};checks=[];rows=[];retained=[]
def check(name,ok,details=None):
 r={'case_id':f'10E1-{len(checks)+1:05}','name':name,'status':'pass' if ok else 'fail'}
 if details is not None:r['details']=details
 checks.append(r)
check('Exact original ordered 1000 IDs and no removal/duplication',[x['key']['question_id'] for x in q]==[x['question_id'] for x in actions]==read('docs/curriculum/app-migration/baseline.json')['question_ids_in_order'] and len(q)==len(cm)==len(cases)==1000)
check('Exactly 500 original concepts',{x['concept_id'] for x in q}=={x['concept_id'] for x in actions} and len({x['concept_id'] for x in q})==500)
for i,x in enumerate(q):
 start=len(checks);qid=x['key']['question_id'];a=am[qid];c=cases[qid];rel=x['relationship'];old=a['original'];mapping=qm[qid]
 check(qid+' entire actual compiled accepted record parity',cm[qid]==x)
 check(qid+' frozen acceptance snapshot hash',digest(x)==c['accepted_snapshot']['record_sha256'])
 check(qid+' exact disposition/revision/owner',rel['disposition']==a['disposition']==c['disposition'] and x['key']['revision']==c['revision'] and c['owner'] in frozen['partition'])
 check(qid+' concept/category unchanged',x['concept_id']==a['concept_id']==old['concept'] and x['category']==old['category'].lower())
 check(qid+' accepted and no active hold',x['acceptance']['eligibility']=='accepted' and x['acceptance']['open_holds']==[])
 check(qid+' source/teaching routing exact map',rel['primary_lesson_id']==mapping['primary_lesson_id'] and rel['related_lesson_ids']==mapping['related_lesson_ids'] and rel['reference_ids']==mapping['reference_ids'] and rel['source_ids']==mapping['source_ids'] and rel['primary_lesson_id'] in docs and set(rel['related_lesson_ids'])<=docs)
 check(qid+' original/content/description/delivery review locators resolve',resolve(x['origin']) is not None and resolve(x['acceptance']['content_review']['record']) is not None and all(resolve(r['record']) is not None for r in x['acceptance']['description_reviews']+x['acceptance']['delivery_proof']))
 check(qid+' exactly four authored option IDs and one valid key',len(x['options'])==len({o['id'] for o in x['options']})==4 and x['feedback']['correct_option_id'] in {o['id'] for o in x['options']} and {f['option_id'] for f in x['feedback']['option_feedback']}=={o['id'] for o in x['options']})
 uses=rel['source_uses']+[u for f in x['feedback']['option_feedback'] for u in f['source_uses']]
 check(qid+' every question/option source use resolves exact scope',all(u['reference_id'] in refs and (u['source_id'] is None and u['scope_id'] is None or u['source_id'] in dest and any(b['reference_id']==u['reference_id'] and b['scope_id']==u['scope_id'] for b in dest[u['source_id']]['scoped_urls'])) for u in uses))
 if rel['disposition']=='retain':
  original={k:old[k] for k in ['prompt','concept','category','correct','explanation']};original['options']=[{'text':o['text'],'explanation':o['explanation']} for o in old['options']]
  observed={'prompt':text(x['prompt']),'concept':x['concept_id'],'category':x['category'].upper(),'correct':next(j for j,o in enumerate(x['options']) if o['id']==x['feedback']['correct_option_id']),'explanation':text(x['feedback']['explanation']),'options':[{'text':text(o['text']),'explanation':text(next(f for f in x['feedback']['option_feedback'] if f['option_id']==o['id'])['explanation'])} for o in x['options']]}
  ok=original==observed and x['image'] is None and all(o['image'] is None for o in x['options']);check(qid+' retained assessment payload unchanged',ok)
  retained.append({'question_id':qid,'status':'pass' if ok else 'fail','original_payload_sha256':digest(original),'accepted_projection_sha256':digest(observed),'routing_provenance':'Approved canonical teaching/source/acceptance metadata compared separately; not part of legacy text payload.'})
 item=checks[start:];rows.append({'question_id':qid,'revision':x['key']['revision'],'disposition':rel['disposition'],'owner':c['owner'],'accepted_pointer':f'content/accepted-assessment-questions.json#/questions/{i}','accepted_record_sha256':digest(x),'content_review':x['acceptance']['content_review'],'description_reviews':x['acceptance']['description_reviews'],'delivery_proof':x['acceptance']['delivery_proof'],'check_ids':[r['case_id'] for r in item],'status':'pass' if all(r['status']=='pass' for r in item) else 'fail'})
counts={k:sum(r['disposition']==k for r in rows) for k in ['retain','rewrite','replace']};check('Exact 336/626/38 disposition totals',counts=={'retain':336,'rewrite':626,'replace':38});check('Every owner has exact frozen membership/count',all(sum(r['owner']==owner for r in rows)==count for owner,count in frozen['partition'].items()))
report={'task':'10E1','date':'2026-10-21','status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','manifest_sha256':sha('content/accepted-content-manifest.json'),'counts':{'questions':len(rows),'concepts':500,**counts,'checks':len(checks),'failed':sum(x['status']=='fail' for x in checks)},'questions':rows,'checks':checks,'limits':'Retained payload equality is independently checked; subsequent tasks supply changed-question semantic/arithmetic review. No source-date refresh, scored edit or old receipt rewrite.'}
(HERE/'question-disposition-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(HERE/'retained-payload-diff.json').write_text(json.dumps({'task':'10E1','count':len(retained),'questions':retained},indent=2)+'\n');print(json.dumps({'status':report['status'],'counts':report['counts'],'failures':[c for c in checks if c['status']=='fail'][:10]},indent=2));sys.exit(0 if report['status']=='pass' else 1)
