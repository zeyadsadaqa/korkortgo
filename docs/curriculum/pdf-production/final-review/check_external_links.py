"""Read-only public-reference response audit. No page content is uploaded."""
from pathlib import Path
import json,time,urllib.request,urllib.error,concurrent.futures
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent;PDF=HERE.parent/'korkortgo-curriculum-review.pdf'
r=PdfReader(PDF);urls=set()
for p in r.pages:
 for a in p.get('/Annots',[]):
  uri=a.get_object().get('/A',{}).get('/URI')
  if uri:urls.add(str(uri))
def check(url):
 errors=[]
 for method in ['HEAD','GET']:
  try:
   req=urllib.request.Request(url,method=method,headers={'User-Agent':'Mozilla/5.0 (compatible; curriculum reference verification)','Range':'bytes=0-1023'} if method=='GET' else {'User-Agent':'Mozilla/5.0 (compatible; curriculum reference verification)'})
   with urllib.request.urlopen(req,timeout=18) as resp:
    return {'url':url,'status':'reachable','http_status':resp.status,'method':method,'resolved_url':resp.url,'content_type':resp.headers.get('Content-Type')}
  except Exception as e:errors.append({'method':method,'error':str(e)[:250]})
 return {'url':url,'status':'unresolved','attempts':errors}
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
 for future in concurrent.futures.as_completed([pool.submit(check,url) for url in sorted(urls)]):
  rows.append(future.result())
  if len(rows)%50==0:print('Checked',len(rows),'of',len(urls),flush=True)
report={'checked_on':'2026-10-14','method':'HEAD, then bounded GET fallback; response reachability is not claim-level factual verification','total':len(rows),'reachable':sum(x['status']=='reachable' for x in rows),'unresolved':sum(x['status']=='unresolved' for x in rows),'links':sorted(rows,key=lambda x:x['url'])}
(HERE/'external-link-checks.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='links'},flush=True)
