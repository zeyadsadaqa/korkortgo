"""Fetch official road-sign artwork and a reproducible source manifest.
Only follows public pages inside the requested Transportstyrelsen section.
"""
import json, re, subprocess, hashlib
from pathlib import Path
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
BASE='https://www.transportstyrelsen.se'
ROOT=BASE+'/sv/vagtrafik/trafikregler-och-vagmarken/'
OUT=Path('tmp/sources'); OUT.mkdir(parents=True,exist_ok=True)
ASSETS=Path('composeApp/src/commonMain/composeResources/files/signs'); ASSETS.mkdir(parents=True,exist_ok=True)
def fetch(url):
 return subprocess.check_output(['curl','--fail','--silent','--show-error','--location','--max-time','25',url])
def page(url):
 key=hashlib.sha256(url.encode()).hexdigest()[:16]; file=OUT/(key+'.html')
 if not file.exists(): file.write_bytes(fetch(url))
 soup=BeautifulSoup(file.read_bytes(),'html.parser'); main=soup.find('main') or soup
 return soup,main
soup,main=page(ROOT+'vagmarken/')
categories=[]
for a in main.select('a[href]'):
 u=urljoin(BASE,a['href'])
 if u.startswith(ROOT+'vagmarken/') and u!=ROOT+'vagmarken/' and u.endswith('/') and u not in categories: categories.append(u)
print('Catalogue sections',len(categories),flush=True)
book={s['code']:s for s in json.loads(Path('content/book-sign-index.json').read_text())}
signs=[]; sources=[]
def section(url):
 try:
  soup,main=page(url); entries=[]
  for a in main.select('a[href]'):
   label=a.get_text(' ',strip=True); match=re.match(r'^([A-Z]+\d+[a-z]?)\.\s*(.+)',label)
   if not match: continue
   img=a.find('img')
   if not img:
    parent=a.parent
    img=parent.find('img') if parent else None
   if img: entries.append((match[1],match[2],urljoin(BASE,a['href']),urljoin(BASE,img.get('src',''))))
  return url,soup.title.get_text(),main.get_text('\n',strip=True),entries
 except Exception as e: print('SECTION ERROR',url,str(e),flush=True); return url,'','',[]
for url,title,text,entries in ThreadPoolExecutor(max_workers=5).map(section,categories):
 sources.append({'url':url,'title':title,'retrieved':'2026-09-26'})
 (OUT/(hashlib.sha256(url.encode()).hexdigest()[:16]+'.txt')).write_text(text)
 signs.extend(entries)
print('Sign entries',len(signs),flush=True)
def asset(item):
 code,title,url,img=item
 try:
  raw=fetch(img)
  if raw.startswith(b'\x89PNG'): ext='png'
  elif raw.startswith(b'\xff\xd8'): ext='jpg'
  elif b'<svg' in raw[:500]: ext='svg'
  elif raw.startswith(b'GIF'): ext='gif'
  else: raise ValueError('Unexpected image format')
  file=ASSETS/(code.lower()+'.'+ext); file.write_bytes(raw)
  return {'code':code,'labelSv':title,'label':book.get(code,{}).get('label',title),'page':book.get(code,{}).get('page',324),'url':url,'imageUrl':img,'image':'signs/'+file.name,'sha256':hashlib.sha256(raw).hexdigest(),'retrieved':'2026-09-26'}
 except Exception as e: print('ASSET ERROR',code,str(e),flush=True)
results=[r for r in ThreadPoolExecutor(max_workers=6).map(asset,{s[0]:s for s in signs}.values()) if r]
Path('content/signs.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
# Read all directly linked general rules and in-vehicle guidance pages.
rule_urls=[ROOT+'trafikregler/generella-trafikregler/',ROOT+'trafikregler/i-fordonet/',ROOT+'trafikregler/lasta-dra/']
for url in list(rule_urls):
 _,m=page(url)
 rule_urls.extend(urljoin(BASE,a['href']) for a in m.select('a[href]') if urljoin(BASE,a['href']).startswith(url) and a['href'].endswith('/'))
texts=[]
for url in dict.fromkeys(rule_urls):
 try:
  s,m=page(url); texts.append({'url':url,'text':m.get_text('\n',strip=True)})
  sources.append({'url':url,'title':s.title.get_text(),'retrieved':'2026-09-26'})
 except Exception as e: print('RULE ERROR',url,str(e),flush=True)
Path('content/source-manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
(OUT/'rules.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2))
print('Saved',len(results),'official images;',len(texts),'rule pages',flush=True)
