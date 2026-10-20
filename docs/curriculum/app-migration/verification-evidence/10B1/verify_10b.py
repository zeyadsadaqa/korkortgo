"""Independent 10B audit. Reads production origins/PDF and fresh compiled/runtime exports.
Never imports the production importer or emitter to calculate expected teaching.
"""
import argparse,ast,hashlib,json,re,sys
from collections import Counter
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
PDF='docs/curriculum/pdf-production/korkortgo-curriculum.pdf'
def load(path):return json.loads((ROOT/path).read_text())
@lru_cache(None)
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def norm(s):return ' '.join(s.split())
def compact(s):return ''.join(s.split())
def markdown(s):
 s=re.sub(r'\[([^\]]+)\]\[[^\]]+\]',r'\1',s)
 s=re.sub(r'^(?:#{1,6}|>) ', '',s,flags=re.M)
 s=s.replace('**','');s=re.sub(r'(?<!\w)\*([^*\n]+)\*(?!\w)',r'\1',s)
 if s.startswith('|'):
  s=' '.join(c.strip() for l in s.splitlines() if not re.fullmatch(r'[| :\-]+',l) for c in l.strip('|').split('|'))
 s=re.sub(r'^- ', '',s,flags=re.M)
 return norm(s)
def rich(nodes):return ''.join(n['text'] if n['type']=='text' else n['expression'] if n['type']=='math' else rich(n.get('children',n.get('label',[]))) for n in nodes)
def text(b):
 p=b['payload'];t=p['type']
 if t in ('paragraph','heading'):return rich(p['text'])
 if t=='table':return ' '.join([rich(c['heading']) for c in p['columns']]+[rich(c) for row in p['rows'] for c in row['cells']])
 if t=='list_items':return ' '.join((str(p['start']+i)+'. ' if p['ordered'] else '')+' '.join(text(c) for c in item) for i,item in enumerate(p['items']))
 if t in ('scenario','callout'):return ' '.join(text(c) for c in p['blocks'])
 if t=='knowledge_check':return ' '.join(text(c) for c in p['prompts'])
 if t=='related_links':return ' '.join(rich(l['label']) for l in p['links'])
 if 'caption' in p:return rich(p['caption'])
 if t=='sign_examples':return ' '.join(rich(SIGNS[i]['caption']) for i in p['entry_ids'])
 return ''
def walk(value):
 if isinstance(value,dict):
  if 'metadata' in value and 'payload' in value:yield value
  for v in value.values():yield from walk(v)
 elif isinstance(value,list):
  for v in value:yield from walk(v)
def strings(value):
 if isinstance(value,dict):
  for k,v in value.items():
   if k in ('text','expression') and isinstance(v,str):yield v
   else:yield from strings(v)
 elif isinstance(value,list):
  for v in value:yield from strings(v)
@lru_cache(None)
def content(path):return (ROOT/path).read_text()
def pointer(value,ptr):
 for key in ptr.lstrip('/').split('/') if ptr else []:value=value[int(key)] if isinstance(value,list) else value[key.replace('~1','/').replace('~0','~')]
 return value
@lru_cache(None)
def source(origin_text):
 o=json.loads(origin_text);path=o['file']['path'];loc=o['locator']
 if loc.startswith('line:'):
  a,_,b=loc[5:].partition('-');return '\n'.join(content(path).splitlines()[int(a)-1:int(b or a)])
 if loc.startswith('json:'):return pointer(load(path),loc[5:])
 return None

def extract():
 from pypdf import PdfReader
 expected=load('docs/curriculum/app-migration/implementation-evidence/9B17/pdf-text.json')
 reader=PdfReader(ROOT/PDF);pages=[]
 for i,page in enumerate(reader.pages):
  actual=page.extract_text();old=expected[i]
  pages.append({'page':i+1,'fresh_text_sha256':hashlib.sha256(actual.encode()).hexdigest(),'retained_text_sha256':hashlib.sha256(old['text'].encode()).hexdigest(),'passed':actual==old['text']})
 report={'pdf':{'path':PDF,'sha256':sha(PDF)},'extractor':'pypdf '+__import__('pypdf').__version__,'page_count':len(reader.pages),'pages':pages,'passed':len(pages)==578 and all(r['passed'] for r in pages)}
 save(HERE/'fresh-pdf-parity.json',report);print('Fresh PDF:',report['passed'],len(pages));return report['passed']

C=load('content/curriculum.json');S=load('content/sources.json');REG=load('docs/curriculum/app-migration/curriculum-map.json')
DOC={d['id']:d for d in C['documents']};SIGNS={s['id']:s for s in C['sign_entries']};ASSETS={a['id']:a for a in C['assets']}
PAGES=load('docs/curriculum/app-migration/implementation-evidence/9B17/pdf-text.json')
LEDGER=load('docs/curriculum/app-migration/implementation-evidence/9B17/import-diagnostics.json')
MATCH={r['id']:r for r in LEDGER['matches'] if r.get('production_extra')}

def audit(task):
 out=BASE/task;out.mkdir(exist_ok=True);checks=[]
 def check(name,ok,details=None):checks.append({'case_id':task+'-'+str(len(checks)+1).zfill(5),'name':name,'passed':bool(ok),'details':details})
 compiled=load(str((HERE/'compiled-content.json').relative_to(ROOT)))
 check('Candidate PDF freshly extracted without text drift',load(str((HERE/'fresh-pdf-parity.json').relative_to(ROOT)))['passed'])
 check('Accepted candidate manifest unchanged',sha('content/accepted-content-manifest.json')=='ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21')
 n=int(task[3:])
 if n==1:
  docs=[DOC[i] for i in ['cover','introduction','study-guide','contents','official-references','artwork-credits']]
  known=[r for k in ['curriculum_nodes','supporting_destinations','source_destinations','sign_entries'] for r in REG[k]]
  actual=[r['id'] for k in ['documents','reference_groups','sign_entries','anchors'] for r in C[k]]+[r['id'] for r in S['destinations']]
  resolutions=load(str((HERE/'compiled-destinations.json').relative_to(ROOT)))
  check('All 1123 identities exact and unique',len(actual)==len(set(actual))==1123 and set(actual)=={r['id'] for r in known})
  check('Actual compiled resolver resolves every destination',len(resolutions)==1123 and {r['id'] for r in resolutions}==set(actual) and all(r['target'] and r['notice'] is None for r in resolutions))
  check('Reading order matches registry module/lesson/review order',C['reading_order']==[r['id'] for r in REG['curriculum_nodes'] if r['kind'] in ('module','lesson','module_review')],C['reading_order'])
  check('All sixty reading nodes have full bodies',len(C['reading_order'])==60 and all(DOC[i]['body_blocks'] for i in C['reading_order']))
  for a,b in zip(C['modules'],REG['modules']):check(a['id']+' exact module title',a['id']==b['id'] and a['title']==b['title'],{'expected':b['title'],'observed':a['title']})
  disclaimer=re.search(r'> \*\*(.*?)\*\*',content('docs/curriculum/manuscript.md')).group(1)
  observed=text(next(b for b in DOC['introduction']['body_blocks'] if b['metadata']['id']=='introduction/disclaimer'))
  check('Exact approved learning-aid disclaimer',disclaimer==observed,{'expected':disclaimer,'observed':observed})
  check('Front matter precedes reading bodies', [d['id'] for d in C['documents'][:4]]==['cover','introduction','study-guide','contents'])
  check('Compiled order and modules exactly match authoring',compiled['reading_order']==C['reading_order'] and compiled['modules']==C['modules'])
  save(out/'destination-parity.json',{'checks':checks[2:],'destinations':resolutions})
 elif n<=11:
  module=f'M{n-1:02d}';docs=[d for d in C['documents'] if d['id']==module or d['id'].startswith(module+'-')]
  check('Introduction, four lessons and review present',all(i in {d['id'] for d in docs} for i in [module,*[module+f'-L{j:02d}' for j in range(1,5)],module+'-R']))
  check('Four full lesson objectives and five hidden answer sets',sum(d['kind']=='lesson' and bool(d['objectives']) for d in docs)==4 and sum(len(d['answer_blocks']) for d in docs)==5)
 elif n==12:docs=[DOC['appendix-'+x] for x in 'ABCD']
 elif n==13:
  docs=[*C['reference_groups'],DOC['reference-contents'],DOC['official-references'],DOC['artwork-credits']]
  captions={c['code']:c for c in load('docs/curriculum/sign-captions.json')['captions']};placement=load('docs/curriculum/pdf-production/reference/assets.json')['official_sign_placements']
  for group in C['reference_groups']:
   wanted=['sign-'+r['code'] for r in placement if r['group']==group['id']]
   check(group['id']+' exact membership and order',group['entry_ids']==wanted,{'expected':wanted,'observed':group['entry_ids']})
  for sign in C['sign_entries']:
   cap=captions[sign['code']];reg=next(r for r in REG['sign_entries'] if r['id']==sign['id'])
   expected=cap['teaching_caption_en']+(' '+cap['variant_description_en'] if cap.get('variant_description_en') else '')
   check(sign['id']+' exact official/editorial identity and caption',sign['code']==reg['code'] and sign['official_name_sv']==reg['official_name_sv']==cap['official_name_sv'] and sign['english_label']==cap['label_en'] and rich(sign['caption'])==expected and sign['translation_status']=='editorial_english' and ASSETS[sign['asset_id']]['study_alt_text']==cap['alt_text_en'],{'caption_origin':sign['origin'],'asset_id':sign['asset_id']})
   asset=ASSETS[sign['asset_id']]
   check(sign['id']+' exact code/variant/artwork binding',asset['original']['path']==reg['asset']['path'] and asset['original']['sha256']==reg['asset']['sha256'] and asset['code_or_illustration_id']==sign['code'] and asset['variant']==(cap.get('variant_description_en') or sign['code']) and sign['caption_id']==reg['caption_id']==asset['caption_id'],{'registry_artwork':reg['asset'],'observed_artwork':asset['original'],'variant':asset['variant']})
  check('Compiled reference groups and signs match every authoring field',compiled['reference_groups']==C['reference_groups'] and compiled['sign_entries']==C['sign_entries'])
  check('400 exact primary entries across 24 groups',len(C['reference_groups'])==24 and sum(len(g['entry_ids']) for g in C['reference_groups'])==400 and len({s for g in C['reference_groups'] for s in g['entry_ids']})==400)
  check('Case-sensitive variant and unavailable signals preserved','sign-F31a' in SIGNS and not any('sign-'+s in SIGNS for s in ['SIG16','SIG17','SIG18']))
 else:docs=C['documents']+C['reference_groups']
 all_blocks=[]
 for doc in docs:
  if 'kind' in doc:
   cd=next(d for d in compiled['documents'] if d['id']==doc['id'])
   check(doc['id']+' compiled complete object parity',doc==cd,{'authoring_sha256':digest(doc),'compiled_sha256':digest(cd)})
  for b in walk(doc):
   all_blocks.append(b);id=b['metadata']['id'];o=b['metadata']['origin'];p=b['payload'];typ=p['type'];raw=source(json.dumps(o));observed=norm(text(b))
   check(id+' origin bytes',sha(o['file']['path'])==o['file']['sha256'],o)
   if o['file']['path']==PDF:
    row=MATCH[id];page=norm(PAGES[row['page']-1]['body']);expected=page[row['offset']:row['offset']+row['characters']]
    check(id+' exact approved PDF passage',compact(expected)==compact(observed),{'page':row['page'],'offset':row['offset'],'characters':row['characters'],'expected_sha256':hashlib.sha256(compact(expected).encode()).hexdigest(),'observed_sha256':hashlib.sha256(compact(observed).encode()).hexdigest()})
   elif o['file']['path'].endswith('.md') and isinstance(raw,str):
    expected=markdown(raw)
    if re.search(r'/item-\d+$',id):
     item=int(id.rsplit('-',1)[1])-1
     expected=markdown(re.sub(r'^(?:- |\d+\. )','',raw.splitlines()[item]))
    if typ=='knowledge_check':
     answer=next(a for a in doc['answer_blocks'] if a['metadata']['id']==p['answer_id']);observed=norm(observed+' '+' '.join(text(c) for c in answer['blocks']))
    if '/prompt' in id:expected=re.split(r'\*\*(?:Answer|Review guide):\*\*',raw,maxsplit=1)[0];expected=markdown(expected)
    elif '/answer' in id and re.search(r'\*\*(?:Answer|Review guide):\*\*',raw):expected=markdown(re.search(r'(\*\*(?:Answer|Review guide):\*\*.*)',raw,re.S)[1])
    check(id+' complete source text parity',expected==observed,{'expected':expected,'observed':observed})
   elif o['file']['path'].endswith('.py') and typ in ('paragraph','heading'):
    tree=ast.parse(content(o['file']['path']));literals=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
    check(id+' production text literal',any(norm(markdown(v))==observed or observed in norm(markdown(v)) for v in literals),{'observed':observed,'origin':o})
   elif typ=='sign_examples':
    check(id+' exact shared official example',all(s in SIGNS and SIGNS[s]['code']==raw['code'] for s in p['entry_ids']),{'entries':p['entry_ids'],'caption_origin':o})
   elif typ in ('cropped_image','composite_image','polygon_image') and isinstance(raw,dict):
    region=p['region'];box=[region[k] for k in ['left','top','right','bottom']]
    check(id+' approved crop/caption',box==raw['box'] and rich(p['caption'])==raw['caption'],{'source':raw,'observed':p})
    if typ=='polygon_image':check(id+' approved polygon',p['polygon']==[{'x':x,'y':y} for x,y in raw['polygon']])
    if typ=='composite_image':
     expected=[{'left':a['rect'][0],'top':a['rect'][1],'right':a['rect'][2],'bottom':a['rect'][3],'asset_id':'official/'+a['code'] if 'code'in a else None,'label':[{'type':'text','text':a['label']}] if a.get('label') else [],'inset_pixels':2} for a in raw['overlays']]
     observed_overlays=[{**v,'label':[{'type':'text','text':rich(v['label'])}] if v['label'] else []} for v in p['overlays']]
     check(id+' exact ordered overlay geometry/artwork/labels',observed_overlays==expected,{'expected':expected,'observed':observed_overlays})
   elif typ=='related_links':check(id+' related links resolve',all(l['target'].get('reference_id') in {r['id'] for r in S['references']} if l['target']['type']=='external_source' else l['target']['target']['content_id'] in DOC for l in p['links']))
  for answer in doc.get('answer_blocks',[]):check(answer['metadata']['id']+' deliberately separated answer',answer['visibility']=='after_deliberate_reveal' and any(b['payload'].get('answer_id')==answer['metadata']['id'] for b in walk(doc['body_blocks'])))
 if n in range(1,13):
  runtime=load(str((out/'reader-runtime.json').relative_to(ROOT)));expected_ids={b['metadata']['id'] for d in docs for b in d['body_blocks']}
  observed_ids={r['block_id'] for r in runtime['observations']}
  check('Actual reader visited every top-level block',expected_ids==observed_ids,{'expected':len(expected_ids),'observed':len(observed_ids)})
  for r in runtime['observations']:check(r['block_id']+' reader content and answer reveal',r['passed'],r)
 if n==7 or n==14:
  b=next(b for b in DOC['M06-L01']['body_blocks'] if b['metadata']['id']=='M06-L01/teaching-009')
  check('Approved page-193 correction at exact origin','small waterways' in text(b) and 'drains' not in text(b) and 'small waterways' in norm(PAGES[192]['text']),{'block_id':b['metadata']['id'],'source':b['metadata']['origin'],'page':193})
 if n==11 or n==13:
  value=' '.join(text(b) for b in DOC['M10-L02']['body_blocks'])
  check('Limited 1177 reference retained','1177' in value and 'No clinical procedure is reproduced' in PAGES[577]['text'])
 if n in (1,13,14):
  assets=C['assets'] if n!=1 else [ASSETS['cover/illustration']]
  for a in assets:check(a['id']+' original/bundled bytes and provenance',sha(a['original']['path'])==a['original']['sha256']==a['bundled']['sha256']==sha(a['bundled']['path']) and bool(a['reuse']) and bool(a['approval']),{'original':a['original'],'bundled':a['bundled'],'kind':a['kind'],'reuse':a['reuse']})
  if n==13:
   check('484 bindings / 419 physical files',len(assets)==484 and len({a['bundled']['path'] for a in assets})==419)
   fonts=sorted((ROOT/'composeApp/src/commonMain/composeResources/font').glob('*'));licences=sorted((ROOT/'composeApp/src/commonMain/composeResources/files/font-licenses').glob('*'))
   check('Four fonts and two licences packaged',len(fonts)==4 and len(licences)==2,[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.relative_to(ROOT))} for p in fonts+licences])
   for resource in fonts+licences:
    original=Path('docs/curriculum/pdf-production/fonts')/resource.name
    check(resource.name+' exact approved font/licence bytes',sha(resource.relative_to(ROOT))==sha(original),{'original':str(original),'bundled':str(resource.relative_to(ROOT)),'sha256':sha(original)})
   runtime=load(str((out/'reference-runtime.json').relative_to(ROOT)))
   check('Actual reference renderer visited all 400 signs and 24 groups',len(runtime['observations'])==424 and {r['id'] for r in runtime['observations']}=={r['id'] for r in C['sign_entries']+C['reference_groups']})
   for row in runtime['observations']:check(row['id']+' actual reference text/credits',row['passed'],row)
 filename='opening-parity.json' if n==1 else f'M{n-1:02d}-parity.json' if n<=11 else 'appendix-parity.json' if n==12 else 'reference-parity.json' if n==13 else 'complete-import-parity.json'
 report={'task':task,'date':'2026-10-20','candidate_manifest_sha256':sha('content/accepted-content-manifest.json'),'status':'pass' if all(c['passed'] for c in checks) else 'fail','checks':checks,'totals':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'documents':len(docs),'blocks_recursive':len(all_blocks)},'limits':['Content/import/shared-reader verification; final cross-platform presentation is 10K.','Fresh primary-source currency review belongs to 10C.']}
 save(out/filename,report)
 if n==13:save(out/'artwork-origin-parity.json',{'status':report['status'],'checks':[r for r in checks if any(x in r['name'] for x in ['crop','polygon','overlay','original/bundled','fonts','physical'])]})
 print(json.dumps({'task':task,'status':report['status'],'totals':report['totals'],'failures':[r for r in checks if not r['passed']][:20]},ensure_ascii=False,indent=2))
 return report['status']=='pass'

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('task',nargs='?');p.add_argument('--extract',action='store_true');a=p.parse_args()
 sys.exit(0 if (extract() if a.extract else audit(a.task)) else 1)
