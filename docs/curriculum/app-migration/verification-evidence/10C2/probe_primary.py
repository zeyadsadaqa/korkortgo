"""Read public selected sources; retain response identities/limited excerpts, never update package data."""
import concurrent.futures,datetime,hashlib,html,json,urllib.request,urllib.error,io,re
from pathlib import Path
from html.parser import HTMLParser
HERE=Path(__file__).resolve().parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style') and self.skip:self.skip-=1
 def handle_data(self,v):
  if not self.skip:self.out.append(v)
def fetch(url):
 result={'url':url,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'KorkortGo-source-verification/10C (public source audit)'}),timeout=25) as response:
   data=response.read(25_000_001);result.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'),last_modified=response.headers.get('Last-Modified'),response_date=response.headers.get('Date'),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
  if len(data)>25_000_000:raise ValueError('Response exceeds read bound')
  if data.startswith(b'%PDF'):
   from pypdf import PdfReader
   reader=PdfReader(io.BytesIO(data));texts=[p.extract_text() or '' for p in reader.pages];result['pdf_pages']=len(texts);text='\n'.join(texts)
   # Saved text is local temporary inspection data; curated claim notes are the retained report.
   temp=Path('/tmp')/('korkort-10c-'+hashlib.sha256(url.encode()).hexdigest()[:12]+'.txt');temp.write_text(text);result['temporary_inspection_text']=str(temp)
   result['title_preview']=' '.join(text.split()[:20])
  else:
   parser=Text();parser.feed(data.decode('utf-8',errors='replace'));text=' '.join(' '.join(parser.out).split());temp=Path('/tmp')/('korkort-10c-'+hashlib.sha256(url.encode()).hexdigest()[:12]+'.txt');temp.write_text(text);result['temporary_inspection_text']=str(temp)
  result['status']='fetched_for_content_review'
 except Exception as e:result.update(status='unreachable_via_direct_probe',error=type(e).__name__+': '+str(e))
 return result
if __name__=='__main__':
 selected=json.loads((HERE/'risk-selection.json').read_text());urls=list(dict.fromkeys(c['url'] for c in selected['claims']))
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,urls))
 (HERE/'primary-fetch-observations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps([{'url':r['url'],'status':r['status'],'http_status':r.get('http_status'),'error':r.get('error'),'inspection':r.get('temporary_inspection_text')} for r in results],ensure_ascii=False,indent=2))
