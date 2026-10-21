"""Fresh retrieval receipts, separate from historical 10C2 and 9G acceptance dates."""
import concurrent.futures,datetime,hashlib,json,urllib.request
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent
old=json.loads((ROOT/'docs/curriculum/app-migration/implementation-evidence/9G/source-review.json').read_text())['questions'];urls={q['primary_url'] for q in old}
for q in old:
 for c in q['retained_claim_limits']:
  urls.update(s['url'] for s in c['sources'])
def fetch(url):
 r={'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Curriculum verification/10E15'}),timeout=35) as f:
   data=f.read();r.update(http_status=f.status,final_url=f.url,body_sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),content_type=f.headers.get('Content-Type'))
  r['claim_verification']='Separate manual scoped review required; HTTP success alone proves no legal fact.'
 except Exception as e:r['error']=str(e)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:rows=list(ex.map(fetch,sorted(urls)))
(HERE/'primary-fetch-observations.json').write_text(json.dumps({'task':'10E15','date':'2026-10-21','sources':rows},indent=2)+'\n')
print(json.dumps([{'url':r['url'],'status':r.get('http_status',r.get('error')),'bytes':r.get('bytes')} for r in rows],indent=2))
