"""10B14 exhaustive source coverage and repeated deterministic generation in isolation."""
import ast,hashlib,json,re,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=Path(__file__).resolve().parent.parent;OUT=BASE/'10B14'
sys.path.insert(0,str(Path(__file__).resolve().parent));import verify_10b as audit
sys.path.insert(0,str(ROOT/'tools'))
def sha_bytes(x):return hashlib.sha256(x).hexdigest()
def check(name,ok,details=None):checks.append({'name':name,'passed':bool(ok),'details':details})
checks=[];C=audit.C;compiled=audit.load(str((BASE/'10B1/compiled-content.json').relative_to(ROOT)))
# All source paragraphs before definitions are required independently of observed imported block count.
for module in range(1,11):
 path=f'docs/curriculum/pdf-production/chapters/M{module:02d}/chapter-source.md';raw=(ROOT/path).read_text();teaching=re.split(r'^\[[^]]+\]: ',raw,1,flags=re.M)[0].strip()
 source_parts=[p for p in teaching.split('\n\n') if not p.startswith('#')]
 imported=[b for d in C['documents'] for b in audit.walk(d) if b['metadata']['origin']['file']['path']==path]
 for i,p in enumerate(source_parts):
  expected=audit.markdown(p);rows=[b for b in imported if audit.source(json.dumps(b['metadata']['origin']))==p]
  check(f'M{module:02d} source paragraph {i+1} has exact imported origin',bool(rows),{'path':path,'first_line':raw[:raw.index(p)].count('\n')+1,'source_sha256':sha_bytes(expected.encode()),'block_ids':sorted({b['metadata']['id'] for b in rows})})
# Direct approved-PDF text checks for the separately imported opening and first two modules.
for doc in C['documents']:
 if doc.get('module_id') not in ('M01','M02') and doc['id'] not in ('cover','introduction','study-guide'):continue
 if doc.get('module_id')=='M01':begin,end=5,21
 elif doc.get('module_id')=='M02':begin,end=22,40
 else:begin,end={'cover':(1,1),'introduction':(2,2),'study-guide':(3,3)}[doc['id']]
 pdf=audit.compact(' '.join(r['text'] for r in audit.PAGES[begin-1:end]))
 for block in audit.walk(doc):
  payload=block['payload'];typ=payload['type']
  if typ in ('related_links','sign_examples'):continue
  if typ=='table':
   segments=[' '.join(audit.rich(c['heading']) for c in payload['columns'])]+[' '.join(audit.rich(c) for c in r['cells']) for r in payload['rows']]
  else:segments=[audit.text(block)]
  for i,value in enumerate(segments):
   if not value:continue
   check(block['metadata']['id']+f' approved PDF text segment {i+1}',audit.compact(value) in pdf,{'pages':[begin,end],'text':value})
# Every full source record and all metadata fields—not a count or generator self-comparison.
for name in ['documents','modules','reading_order','lesson_category_tags','assets','sign_entries','reference_groups']:
 check('Fresh actual compiled '+name+' exact JSON parity',C[name]==compiled[name],{'expected_sha256':audit.digest(C[name]),'observed_sha256':audit.digest(compiled[name])})
# Every compiled route must preserve the authored canonical target, including exact anchor block IDs.
resolved=audit.load(str((BASE/'10B1/compiled-destinations.json').relative_to(ROOT)))
anchors={r['id']:r['target'] for r in C['anchors']}
check('Compiled anchor map exactly matches authored canonical anchors',compiled['anchors']==anchors)
for row in resolved:
 wanted=anchors.get(row['id'],{'content_id':row['id'],'block_id':None})
 check(row['id']+' compiled resolver exact target',row['target']==wanted,{'expected':wanted,'observed':row['target']})
check('Compiled scoped source destinations exact authoring parity',compiled['sources']['destinations']==audit.S['destinations'])
compiled_refs={r['id']:r for r in compiled['sources']['references']}
for ref in audit.S['references']:check(ref['id']+' complete source metadata compiled',compiled_refs.get(ref['id'])==ref)
for doc in C['documents']:
 node=next((r for r in audit.REG['curriculum_nodes'] if r['id']==doc['id']),None)
 if node:check(doc['id']+' exact registry title',doc['title']==node['title'])
# Each teaching/reference use preserves its approved source scope and exact URL.
registry_sources={r['id']:r for r in audit.REG['source_destinations']}
references={r['id']:r for r in audit.S['references']}
for doc in C['documents']+C['reference_groups']:
 for block in audit.walk(doc):
  for number,use in enumerate(block['metadata']['source_uses'],1):
   source=registry_sources.get(use['source_id']);reference=references.get(use['reference_id'])
   expected=source['scoped_urls'].get(use['scope_id']) if source else None
   check(block['metadata']['id']+f' exact scoped reference {number}',expected is not None and reference is not None and reference['url']==expected,{'source_id':use['source_id'],'scope_id':use['scope_id'],'expected_url':expected,'observed_url':reference['url'] if reference else None})
# Reconcile crop coordinate systems with actual approved sheet dimensions.
import struct
for doc in C['documents']+C['reference_groups']:
 for block in audit.walk(doc):
  payload=block['payload']
  if 'region' not in payload:continue
  asset=audit.ASSETS[payload['asset_id']];data=(ROOT/asset['original']['path']).read_bytes();width,height=struct.unpack('>II',data[16:24]);region=payload['region']
  check(block['metadata']['id']+' approved original pixel coordinate system',region['source_width']==width and region['source_height']==height,{'original_size':[width,height],'observed_size':[region['source_width'],region['source_height']]})
cover=next(b['payload'] for b in audit.DOC['cover']['body_blocks'] if b['metadata']['id']=='cover/illustration')
# Invert the approved PDF drawImage transform: source x starts 25 pixels left of the window,
# source y starts 15 pixels below it, and the 1055px-high sheet uses a bottom-origin PDF frame.
polygon=[{'x':x,'y':1055-(15+y)} for x,y in [(25,0),(25+710,0),(25+710,745),(25+575,650),(25,650)]]
check('Cover uses exact inverted approved production polygon',cover['polygon']==polygon,{'source':'docs/curriculum/pdf-production/build.py:99-106','derived_polygon':polygon,'observed_polygon':cover['polygon']})
# Reconcile each PDF character interval independently using frozen allocation offsets and approved sign text.
pages=audit.PAGES;diag=audit.LEDGER;captions={r['code']:r for r in audit.load('docs/curriculum/sign-captions.json')['captions']};page_results=[]
for page in range(41,579):
 body=audit.norm(pages[page-1]['body']);counts=[0]*len(body);spans=[]
 for r in diag['matches']+diag['print_metadata']:
  if r['page']==page:
   start=r['offset'];end=start+r['characters'];actual=body[start:end]
   if 'normalized_sha256' in r:check(r['id']+' frozen PDF allocation text',sha_bytes(actual.encode())==r['normalized_sha256'],{'page':page,'offset':start,'characters':r['characters']})
   elif 'text' in r:check(f'page {page} print furniture exact',actual==r['text'],r)
   spans.append((start,end,'allocated'))
 # Complete official cards use canonical exact strings and must match the entire consecutive PDF passage.
 for claim in [r for r in diag['sign_examples'] if r['page']==page]:
  cap=captions[claim['code']]
  full=audit.norm(claim['code']+' · '+cap['label_en']+' '+cap['official_name_sv']+' '+cap['teaching_caption_en']+(' '+cap['variant_description_en'] if cap.get('variant_description_en') else '')+' Transportstyrelsen · official description')
  candidates=[m.start() for m in re.finditer(re.escape(full),body)]
  chosen=next((start for start in candidates if not any(a<=start<b for a,b,_ in spans)),None)
  if chosen is not None:spans.append((chosen,chosen+len(full),'official-card'))
  check(claim['id']+' exact complete PDF sign card',chosen is not None,{'page':page,'code':claim['code']})
 for a,b,kind in spans:
  for j in range(a,b):counts[j]+=1
 missing=[j for j,c in enumerate(body) if not c.isspace() and counts[j]==0];duplicate=[j for j,c in enumerate(body) if not c.isspace() and counts[j]>1]
 result={'page':page,'missing_nonspace_characters':len(missing),'duplicate_nonspace_characters':len(duplicate),'intervals':len(spans),'passed':not missing and not duplicate};page_results.append(result)
 check(f'PDF page {page} teaching accounted for exactly once',result['passed'],result)
audit.save(OUT/'independent-pdf-coverage.json',page_results)
# Production reader/nav return maps generated in memory, then written only to an isolated temp tree.
from build_reader import generate as reader_generate
from build_navigation import generate as navigation_generate
from finalize_question_package_9j import build as accepted_generate
from compile_curriculum import compile_files
runs=[]
with tempfile.TemporaryDirectory(prefix='korkort-10b-') as temp:
 for number in (1,2):
  folder=Path(temp)/str(number);folder.mkdir()
  generated={**reader_generate(),**navigation_generate(),**{Path(k):v for k,v in accepted_generate(check=True).items()}}
  entries=[]
  for p,value in sorted(generated.items(),key=lambda x:str(x[0])):
   dest=folder/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(value)
   entries.append({'path':str(p),'sha256':sha_bytes(dest.read_bytes()),'matches_production':dest.read_bytes()==(ROOT/p).read_bytes()})
  manifest=ROOT/'content/accepted-content-manifest.json';m=audit.load('content/accepted-content-manifest.json');paths={r['kind']:ROOT/r['file']['path'] for r in m['payloads'] if r['kind']!='asset'}
  totals=compile_files(paths,manifest,folder/'full-package',folder/'trace.json',profile='release',symbol='verified10B',source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json')
  full=[{'path':p.name,'sha256':sha_bytes(p.read_bytes())} for p in sorted((folder/'full-package').glob('*.kt'))]
  runs.append({'run':number,'production_outputs':entries,'full_package_outputs':full,'trace_sha256':sha_bytes((folder/'trace.json').read_bytes()),'release_totals':totals})
 check('Two isolated reader/navigation/accepted generation runs byte-identical',runs[0]['production_outputs']==runs[1]['production_outputs'])
 check('Every regenerated production output exactly matches candidate',all(r['matches_production'] for r in runs[0]['production_outputs']))
 check('Two isolated full accepted-package Kotlin/trace generations identical',runs[0]['full_package_outputs']==runs[1]['full_package_outputs'] and runs[0]['trace_sha256']==runs[1]['trace_sha256'])
audit.save(OUT/'repeated-generation.json',runs)
# Exact complete manifest file/hash references, each distinct binding.
pairs=set()
def refs(v):
 if isinstance(v,dict):
  if isinstance(v.get('path'),str) and re.fullmatch('[0-9a-f]{64}',str(v.get('sha256',''))):pairs.add((v['path'],v['sha256']))
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
for p in ['content/accepted-content-manifest.json','content/curriculum.json','content/accepted-assessment-questions.json','content/package-sources.json','content/legacy-aliases.json']:refs(audit.load(p))
for path,wanted in sorted(pairs):check(path+' manifest referenced bytes',audit.sha(path)==wanted,{'sha256':wanted})
accepted=audit.load('content/accepted-assessment-questions.json')['questions'];check('Separate accepted release is 1000 accepted / 0 held',len(accepted)==1000 and all(q['acceptance']['eligibility']=='accepted' and not q['acceptance']['open_holds'] for q in accepted))
report={'task':'10B14','status':'pass' if all(c['passed'] for c in checks) else 'fail','checks':checks,'totals':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'manifest_references':len(pairs),'pdf_pages':len(page_results),'production_generated_outputs':len(runs[0]['production_outputs']),'full_package_generated_outputs':len(runs[0]['full_package_outputs'])}}
audit.save(OUT/'closure-checks.json',report)
print(json.dumps({'status':report['status'],'totals':report['totals'],'failures':[r for r in checks if not r['passed']][:20]},ensure_ascii=False,indent=2));sys.exit(0 if report['status']=='pass' else 1)
