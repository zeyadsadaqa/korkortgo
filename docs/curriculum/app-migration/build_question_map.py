"""Build the 7C planning map from frozen questions and approved teaching evidence.

Run with --extract to refresh the saved evidence from the approved PDF (pypdf
required). Default rebuild uses the hash-bound saved extraction. This never edits
the question bank, generated Kotlin, app sources or PDF.
"""
from pathlib import Path
import argparse, collections, hashlib, json, re
from functools import lru_cache
from urllib.parse import urlparse
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CUR=HERE.parent
PROD=CUR/'pdf-production'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
@lru_cache(maxsize=None)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return re.sub(r'\s+','',s).replace('\u00ad','')
def pointer(p):return ''.join('/'+str(s).replace('~','~0').replace('/','~1') for s in p)
def walk(v,p=()):
 if isinstance(v,dict):
  yield v,p
  for k,x in v.items():yield from walk(x,p+(k,))
 elif isinstance(v,list):
  for i,x in enumerate(v):yield from walk(x,p+(i,))
def bound(p):return {'path':str(p.relative_to(ROOT)),'sha256':sha(p)}
args=argparse.ArgumentParser();args.add_argument('--extract',action='store_true');args=args.parse_args()
base=read(HERE/'baseline.json');cm=read(HERE/'curriculum-map.json');release=ROOT/base['release']['path']
assert sha(release)==base['release']['sha256']==cm['release_binding']['sha256']
assert read(PROD/'final-review/screen-release.json')['status']=='approved'
bank=read(ROOT/'content/questions.json');coverage=read(CUR/'question-book-review/all-question-coverage.json');cov=coverage['questions']
assert [q['id'] for q in bank]==base['question_ids_in_order']==[q['question_id'] for q in cov]
assert sha(ROOT/'content/questions.json')==coverage['metadata']['questions_sha256']
used=sorted({e['pdf_page'] for q in cov for e in q['evidence']})
evidence_path=HERE/'question-map-evidence.json'
if args.extract:
 from pypdf import PdfReader
 r=PdfReader(release);pages=[]
 for no in used:
  page=r.pages[no-1];urls=[]
  for a in page.get('/Annots',[]):
   url=a.get_object().get('/A',{}).get('/URI')
   if url and str(url) not in urls:urls.append(str(url))
  text=page.extract_text();pages.append(dict(page=no,text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest(),external_urls=urls))
 write(evidence_path,{'release':bound(release),'method':'Fresh pypdf extraction of every cited teaching page; source URLs are actual page annotation targets.','pages':pages})
evidence=read(evidence_path);assert evidence['release']['sha256']==sha(release)
pages={p['page']:p for p in evidence['pages']};assert sorted(pages)==used
nodes={n['id']:n for n in cm['curriculum_nodes']};lessons={k:v for k,v in nodes.items() if v['kind']=='lesson'}
nav=read(PROD/'assembly/navigation.json')['destinations'];signs={s['code']:s for s in cm['sign_entries']}
captions={s['code']:s for s in read(CUR/'sign-captions.json')['captions']}
groups=sorted((n['pdf_evidence_page'],n['id']) for n in nodes.values() if n['kind']=='sign_reference_group')
group_lessons=dict(zip([f'RB{i:02}' for i in range(1,25)],['M03-L01','M04-L01','M03-L02','M03-L02','M03-L02','M03-L02','M03-L03','M03-L03','M03-L03','M03-L03','M03-L01','M03-L01','M04-L03','M04-L04','M05-L02','M05-L03','M06-L01','M06-L03','M06-L04','M06-L04','M07-L02','M08-L01','M09-L04','M10-L01']))
# Curated topical exceptions: choose the most specific teaching lesson, retaining
# the original primary PDF folio separately as historical evidence.
overrides={'situation-039':'M06-L02','situation-108':'M06-L04','situation-112':'M06-L04','situation-115':'M07-L01','situation-129':'M01-L03','situation-168':'M02-L02'}
# Exact source aliases for non-claim scenario records. Claim-linked records retain
# the earlier reviewed claim/source associations instead of these selections.
aliases={}
def assign(numbers,*refs):
 for n in numbers:aliases[f'situation-{n:03}']=list(refs)
assign(range(1,13),'traffic-law');assign([2,3,4],'traffic-law','sign-law')
assign([14,15,16],'sign-law','traffic-law');assign(range(17,22),'traffic-law','cycles','pedestrians');assign(range(22,25),'roundabout','traffic-law')
assign(range(25,31),'parking','traffic-law');assign([31,32],'sign-law','parking');assign([33,34],'parking','traffic-law')
assign(range(35,42),'traffic-law');assign(range(42,45),'special-streets','traffic-law');assign([46],'traffic-law')
assign([47,49],'syllabus','practical');assign([48],'practical');assign([50,51,55,56],'syllabus','traffic-law');assign([52],'rail','traffic-law');assign([53,54],'planning','syllabus')
assign([57,58],'drink-law');assign([59,60],'alcohol','traffic-law');assign([61],'alcohol','medical','traffic-law');assign([63,64],'phone','traffic-law');assign([65],'planning','phone');assign([66],'traffic-law');assign([67],'phone','traffic-law')
assign([72,74],'traffic-law','syllabus');assign([80,81,89,91],'eco','traffic-law');assign([87],'noise','eco');assign([93],'hybrid');assign([95],'syllabus');assign([96],'zones','stfs');assign([97],'zones')
assign([100,101,102,103,110,111],'traffic-law');assign([108],'works','traffic-law');assign([109],'horses','traffic-law');assign([112],'rail','traffic-law');assign([113],'friction','traffic-law');assign([115],'traffic-law','lights')
assign([118,120,121,122],'traffic-law');assign([123],'first-aid','breakdown','traffic-law');assign([124,125],'traffic-law');assign([127],'wildlife','traffic-law');assign([128],'breakdown','traffic-law')
assign([130],'airbags','belts');assign([133,134],'child-rules','child-advice','airbags');assign([137,139],'friction');assign(range(140,144),'winter');assign([144],'tyre-basics','tyre-advice');assign([147],'winter');assign([151],'crash','friction');assign([155],'friction','crash')
assign([160],'load-advice','traffic-law');assign([161,162],'weights');assign([163],'b','trailer');assign([164],'trailer-guide','towing');assign([166],'traffic-law');assign([167],'lights');assign([168,169,175],'practical');assign([170,171],'inspection');assign([176],'registration');assign([177],'off-road-inspection','inspection');assign([178],'insurance')
family_sources={'reaction':['friction'],'gap':['friction','traffic-law'],'braking':['braking-model'],'stopping':['stopping-shortcut','stopping-principles'],'disc':['parking','traffic-law'],'load':['weights'],'fuel':['eco']}
# The URL in scoped_urls takes precedence over an identically named alias from a
# different module. The app source ID is unchanged.
sources={s['id']:s for s in cm['source_destinations']}
def resolve(alias,module):
 s=sources['source-'+alias];return s.get('scoped_urls',{}).get(module,s['url'])
# Preserve source checks with JSON pointers, including later G/H amendments.
check_files=list(sorted((PROD/'chapters').glob('M*/source-checks.json')))+[CUR/'question-book-review/remaining-gap-h0-sources.json',CUR/'manuscript-sources.json']
checks=collections.defaultdict(list)
for p in check_files:
 for obj,ptr in walk(read(p)):
  if isinstance(obj.get('url'),str):checks[obj['url']].append({'path':str(p.relative_to(ROOT)),'json_pointer':pointer(ptr),'record':obj})
def classify(url):
 host=urlparse(url).hostname or ''
 if host in ['www.riksdagen.se','riksdagen.se']:return 'Swedish legislation or parliamentary material; retain passage-specific distinction'
 if host.endswith(('transportstyrelsen.se','trafikverket.se')) or host=='trafikverket.diva-portal.org':return 'Swedish transport authority guidance or hosted research; retain passage-specific distinction'
 if host.endswith(('1177.se','naturvardsverket.se','smhi.se','polisen.se','msb.se','krisinformation.se','mfd.se','gagnef.se','goteborg.se','energiochklimatradgivningen.se')):return 'Swedish public-service guidance'
 if host.endswith(('volvocars.com','kia.com','ownersmanual.kia.com','fordservicecontent.com')):return 'Manufacturer technical guidance; vehicle/model limits apply'
 if host=='trafiko.se':return 'Commercial teaching shortcut; not official guidance or a real stopping-distance prediction'
 if host.endswith(('.gov','.gov.uk','.gov.au','.govt.nz','.govt.uk')) or '.gov.' in host or host in ['www.nsw.gov.au','nzta.govt.nz']:return 'Foreign public authority guidance; not Swedish law'
 return 'Retain publisher and limits from linked local source evidence; no official status inferred'
registry={}
def ref(url):
 rid='REF-'+hashlib.sha256(url.encode()).hexdigest()[:16]
 registry.setdefault(rid,{'id':rid,'url':url,'classification':classify(url),'source_checks':checks.get(url,[]),'fresh_network_check_in_7C':False})
 return rid
out=[];mismatches=[];lessoncounts=collections.Counter();relatedcounts=collections.Counter()
for q,b in zip(cov,bank):
 qid=q['question_id'];assert b['prompt']==q['prompt'] and b['options']==q['options'] and b['correct']==q['correct_option_index']
 teaching=[]
 for e in q['evidence']:
  no=e['pdf_page'];old=e.get('page_text',e.get('excerpt',''));current=pages[no]['text'];match=norm(old) in norm(current)
  corrected=norm(old).replace(norm('actions after a collision are in M10-L01.'),norm('actions after a wildlife collision are in M10-L02.')) in norm(current)
  assert match or (no==193 and corrected),(qid,no,'Historical evidence changed unexpectedly')
  if not match:mismatches.append({'question_id':qid,'page':no,'reason':'Approved 6N wildlife cross-reference M10-L01 → M10-L02; teaching otherwise unchanged'})
  teaching.append({'pdf_page':no,'evidence_id':f'book-page-{no:03}','passage':old if match else current,'passage_kind':'exact illustrated caption' if 'excerpt' in e else 'supporting approved page text','historical_H7_match':match,'approved_6N_correction_applied':not match})
 lesson_ids=[]
 for e in teaching:
  # Read only the page header, so incidental cross-references cannot select a lesson.
  hit=re.search(r'M\d{2}-L\d{2}',pages[e['pdf_page']]['text'].split('\n',1)[0])
  if hit and hit[0] not in lesson_ids:lesson_ids.append(hit[0])
 refs=[];reason='Existing teaching-page header identifies its canonical lesson.'
 if 'sign_code' in q:
  code=q['sign_code'];s=signs[code];cap=captions[code]
  gp=next(g for start,g in reversed(groups) if start<=s['pdf_evidence_page']);refs=[s['id'],gp]
  primary=lesson_ids[0] if lesson_ids else group_lessons[gp]
  if group_lessons[gp] not in lesson_ids:lesson_ids.append(group_lessons[gp])
  reason='Exact sign/caption target retained; lesson is its actual teaching-page lesson, or the reviewed decision-topic lesson for its reference group.'
  official=[{'reference_id':ref(x['url']),'relationship':'exact sign description or applicable sign regulation','locator':x.get('locator'),'source_register_id':x.get('source_id'),'provenance':{'path':'docs/curriculum/sign-captions.json','caption_id':cap['caption_id']}} for x in cap['sources']]
  srcids=['source-signs','source-sign-law']
 else:
  primary=overrides.get(qid,q.get('lesson') or (lesson_ids[0] if lesson_ids else None));assert primary,qid
  family=qid.split('-')[0];selected=aliases.get(qid) if family=='situation' else family_sources[family]
  official=[];srcids=[]
  if q.get('claim_linkage'):
   for claim in q['claim_linkage']:
    for s in claim['sources']:
     official.append({'reference_id':ref(s['url']),'relationship':'retained reviewed claim support','claim_id':claim['claim_id'],'classification':claim['classification'],'scope_limits':claim.get('scope_limits'),'publisher':s.get('publisher'),'locator':s.get('locator')})
     if 'source-'+s.get('alias','') in sources:srcids.append('source-'+s['alias'])
  else:
   assert selected,('Missing curated source selection',qid)
   # Some supporting sources belong to a related lesson/module (e.g. sound and eco).
   for alias in selected:
    candidates=[primary[:3]]+[x[:3] for x in lesson_ids if x[:3]!=primary[:3]]
    s=sources['source-'+alias];scope=next((x for x in candidates if x in s.get('scoped_urls',{})),primary[:3]);url=resolve(alias,scope)
    srcids.append(s['id']);official.append({'reference_id':ref(url),'relationship':'teaching context and applicable duty' if family in ['reaction','gap','fuel'] else 'supporting lesson reference','source_id':s['id'],'scope':scope,'locator':'Read with cited approved passage and retained source-check finding; not a new claim-level verification.'})
 if primary not in lesson_ids:lesson_ids.insert(0,primary)
 related=[x for x in lesson_ids if x!=primary];assert primary in lessons and all(x in lessons for x in related)
 srcids=list(dict.fromkeys(srcids));findings=[]
 if q.get('rounding_qualification'):findings.append({'id':'7D-FUEL-ROUNDING','status':'carry forward to 7D','description':q['rounding_qualification']})
 row={'question_id':qid,'concept_id':b['concept'],'category':b['category'],'content_version':'screen-2026-10-14-'+sha(release)[:12],'primary_lesson_id':primary,'related_lesson_ids':related,'reference_ids':refs,'source_ids':srcids,'source_reference_ids':list(dict.fromkeys(x['reference_id'] for x in official)),'source_evidence':official,'mapping_rationale':reason if qid not in overrides else 'Curated topic-specific lesson overrides the earliest general/answer page; all original teaching folios retained.','coverage_status':'covered','coverage_basis':q['basis'],'coverage_rationale':q['rationale'],'teaching_evidence':teaching,'original_H7_primary_folio':q['primary_book_page'],'historical_bank_page_policy':'Not an app target; legacy link reconciliation belongs to 7E.','scope_limits':q.get('coverage_limit','Keyed-answer selection coverage; does not certify every distractor explanation or question quality.'),'retained_claims':q.get('claim_linkage',[]),'calculation':q.get('calculation'),'findings':findings,'unresolved_mapping_findings':[],'disposition':'not assessed; 7D'}
 if 'sign_code' in q:row['sign_code']=q['sign_code']
 out.append(row);lessoncounts[primary]+=1;relatedcounts.update(related)
inputs=[HERE/'build_question_map.py',HERE/'verify_question_map.py',HERE/'baseline.json',HERE/'curriculum-map.json',ROOT/'content/questions.json',CUR/'question-book-review/all-question-coverage.json',CUR/'question-book-review/remaining-gap-h7-audit.json',PROD/'final-review/coverage-revalidation.json',CUR/'sign-captions.json',PROD/'assembly/navigation.json',evidence_path]+check_files
report={'schema_version':'1.0','step':'7C','status':'complete with explicit quality qualifications reserved for 7D','prepared_on':'2026-10-14','release':bound(release),'edition':'approved screen; print masters deferred','inputs':[bound(p) for p in inputs],'method':'Reuse all H7 semantic decisions only after frozen-bank parity and fresh approved-page passage checks; preserve 6N correction, reviewed claim limits, exact sign captions and calculation assumptions. Curated topic exceptions/source aliases are in build_question_map.py.','source_policy':'Source IDs resolve through 7B; REF IDs resolve through source_registry below. Local dated verification is reused, not refreshed externally in 7C. Foreign, manufacturer, hosted research and commercial teaching sources retain their classifications; agency context does not make editorial equations official formulas.','app_navigation_policy':'primary_lesson_id, related_lesson_ids and reference_ids are app destinations. PDF folios/passages are evidence only; original bank page values are not navigation targets.','source_registry':list(registry.values()),'totals':{'questions':len(out),'covered':len(out),'unmatched':0,'ambiguous':0,'rounding_qualified':sum(bool(q['findings']) for q in out),'primary_lessons_used':len(lessoncounts),'sign_questions':sum('sign_code' in q for q in out)},'approved_correction_revalidation':mismatches,'lesson_coverage':[{'lesson_id':lid,'title':lessons[lid]['title'],'primary_questions':lessoncounts[lid],'related_questions':relatedcounts[lid],'teaching_mapping_gaps':0,'bank_sampling_gap':lessoncounts[lid]==0} for lid in lessons],'questions':out}
write(HERE/'question-map.json',report)
print(json.dumps(report['totals']));print('Historical passage corrections:',len(mismatches));print('Source references:',len(registry))
