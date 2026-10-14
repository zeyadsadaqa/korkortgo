"""Read-only release checks; preserves historical H7 records and records current evidence."""
from pathlib import Path
import json,re,hashlib,sys,subprocess
from pypdf import PdfReader
import pdfplumber
ROOT=Path(__file__).resolve().parents[4];PROD=ROOT/'docs/curriculum/pdf-production';OUT=Path(__file__).resolve().parent
pdf=PROD/'korkortgo-curriculum-review.pdf'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def norm(t):return ' '.join(t.split())
r=PdfReader(pdf);nav=json.loads((PROD/'assembly/navigation.json').read_text());dest=nav['destinations'];total=len(r.pages)
assert total==578==nav['pages'];assert r.page_labels==[str(i) for i in range(1,total+1)]
for key,num in dest.items():assert r.get_destination_page_number(r.named_destinations[key])+1==num,key
assert r.trailer['/Root']['/Lang']=='en-GB'
page_ids={p.indirect_reference.idnum:i+1 for i,p in enumerate(r.pages)}
internal=0;external=set();fontnames=set();font_objects=set();actualtext_pages=[]
for i,p in enumerate(r.pages):
 for obj in p.get('/Annots',[]):
  a=obj.get_object();target=a.get('/Dest') or a.get('/A',{}).get('/D')
  if target is not None:
   if isinstance(target,str):number=r.get_destination_page_number(r.named_destinations[target])+1
   else:number=page_ids[target[0].idnum] if hasattr(target[0],'idnum') else int(target[0])+1
   assert 1<=number<=total;internal+=1
  elif '/A' in a:
   assert a['/A']['/S']=='/URI';external.add(str(a['/A']['/URI']))
 for f in p['/Resources'].get('/Font',{}).values():
  if f.idnum in font_objects:continue
  font_objects.add(f.idnum);f=f.get_object();assert f['/FontDescriptor'].get_object().get('/FontFile2');assert '/ToUnicode' in f;fontnames.add(str(f['/BaseFont']))
 if b'/ActualText' in p.get_contents().get_data():actualtext_pages.append(i+1)
print('Navigation/fonts checked:',internal,'links,',len(dest),'destinations',flush=True)
cache=OUT/'current-pages.json'
if cache.exists() and json.loads(cache.read_text())['pdf_sha256']==sha(pdf):
 texts=json.loads(cache.read_text())['pages'];print('Using verified text cache for exact PDF hash',flush=True)
else:
 texts=[]
 for i,p in enumerate(r.pages):
  texts.append(p.extract_text() or '')
  if (i+1)%100==0:print('Extracted',i+1,'pages',flush=True)
 cache.write_text(json.dumps({'pdf_sha256':sha(pdf),'pages':texts},ensure_ascii=False)+'\n')
old=json.loads((OUT/'pre-correction-pages.json').read_text());changed=[i+1 for i,(a,b) in enumerate(zip(old,texts)) if norm(a)!=norm(b)]
assert changed==[193],changed
old_phrase='Prevention belongs here; actions after a collision are in M10-L01.'
new_phrase='Prevention belongs here; actions after a wildlife collision are in M10-L02.'
assert norm(old[192]).replace(old_phrase,new_phrase)==norm(texts[192])
alltext='\n'.join(texts);assert not re.search(r'theory[ -]book|körkort\s*online|korkortonline|hagberg',alltext,re.I)
disclaimer='This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.'
assert disclaimer in norm(texts[1]);assert 'one year' in texts[5] and '19 August 2026' in texts[5]
assert len([k for k in dest if re.fullmatch(r'M\d\d-L\d\d',k)])==40
assert len([k for k in dest if re.fullmatch(r'M\d\d-R',k)])==10
# Transfer historical H7 evidence only after validating its input identity and exact text change.
cov=json.loads((ROOT/'docs/curriculum/question-book-review/all-question-coverage.json').read_text());assert sha(ROOT/'content/questions.json')==cov['metadata']['questions_sha256']
assert cov['metadata']['book_sha256']==json.loads((OUT/'pre-correction-render-comparison.json').read_text())['pdf_sha256']
question_checks=[];affected=[]
for q in cov['questions']:
 assert q['status']=='covered' and all(1<=p<=total for p in q['book_pages'])
 for e in q['evidence']:
  original=norm(e.get('page_text',e.get('excerpt','')));assert original
  current=norm(texts[e['pdf_page']-1])
  expected=original.replace(old_phrase,new_phrase)
  assert expected in current,(q['question_id'],e['pdf_page'])
 if 193 in q['book_pages']:affected.append(q['question_id'])
 question_checks.append({'question_id':q['question_id'],'status':'covered_evidence_revalidated','book_pages':q['book_pages']})
(OUT/'coverage-revalidation.json').write_text(json.dumps({'reviewed_on':'2026-10-14','book_sha256':sha(pdf),'historical_H7_book_sha256':cov['metadata']['book_sha256'],'method':'Revalidated every H7 evidence page against current extraction; only normalized text change is the corrected wildlife lesson reference on page 193. H7 arithmetic/meaning checks retained, not newly certified.','totals':{'covered':len(question_checks),'missing':0},'affected_question_ids':affected,'rounding_qualified_questions':cov['metadata']['rounding_qualified_questions'],'questions':question_checks},indent=2)+'\n')
print('All 1,000 question evidence records revalidated',flush=True)
# Verify every recorded placed official file against its saved hash.
asset_checks=[];seen={};issues=[];scene_res=[]
for path in [*(PROD/'chapters').glob('*/illustrations.json'),PROD/'reference/assets.json']:
 data=json.loads(path.read_text())
 for entry in data.get('official_sign_placements',[]):
  ap=ROOT/entry['path'];seen.setdefault(str(ap),sha(ap));assert seen[str(ap)]==entry['sha256'],entry['path'];asset_checks.append({'code':entry['code'],'path':entry['path'],'hash_pass':True,'component_page':entry['page'],'component_register':str(path.relative_to(ROOT))})
 for key,entry in data.get('assets',{}).items():
  if 'print_ppi' in entry:scene_res.append({'id':key,'ppi':entry['print_ppi'],'component_register':str(path.relative_to(ROOT))})
(OUT/'asset-checks.json').write_text(json.dumps({'official_placements_checked':len(asset_checks),'unique_files_checked':len(seen),'placements':asset_checks,'scene_resolution':scene_res},indent=2)+'\n')
# Full-book text geometry, control-glyph and text-size audit. Exact visual review remains separate.
bounds=[];replacement=[];minsize=999;chars=0
with pdfplumber.open(pdf) as doc:
 for i,p in enumerate(doc.pages):
  for c in p.chars:
   chars+=1;minsize=min(minsize,c['size'])
   if c['text']=='\ufffd':replacement.append(i+1)
   if not (-.1<=c['x0']<=c['x1']<=p.width+.1 and -.1<=c['top']<=c['bottom']<=p.height+.1):bounds.append({'page':i+1,'text':c['text'],'box':[c['x0'],c['top'],c['x1'],c['bottom']]})
  if (i+1)%100==0:print('Geometry checked',i+1,'pages',flush=True)
assert not bounds and not replacement,(bounds[:5],replacement)
root=r.trailer['/Root'];tagged='/StructTreeRoot' in root and bool(root.get('/MarkInfo',{}).get('/Marked'))
report={'reviewed_on':'2026-10-14','step':'6N','status':'verification_in_progress_accessibility_hold','pdf':str(pdf.relative_to(ROOT)),'sha256':sha(pdf),'pages':total,'internal_links':internal,'distinct_external_urls':len(external),'external_urls':sorted(external),'named_destinations':len(dest),'fonts':sorted(fontnames),'text_chars_checked':chars,'minimum_text_size_pt':minsize,'text_bounds_issues':bounds,'replacement_glyph_pages':replacement,'exact_disclaimer':True,'source_book_name_scan':'passed','only_changed_text_page':193,'question_evidence_records_revalidated':1000,'official_asset_placements_checked':len(asset_checks),'actualtext_page_count':len(actualtext_pages),'document_language':'en-GB','structure_tree_present':'/StructTreeRoot' in root,'marked_document':tagged,'tagged_accessibility':'passed' if tagged else 'failed: no structure tree/marked document; semantic headings, tables, reading order and image/link tags not established','cover_resolution_ppi_from_saved_review':95,'scene_resolution_min_ppi':min(x['ppi'] for x in scene_res),'print_release':'held: higher-resolution approved artwork required','user_final_approval':'not given'}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print('Finished structural/content/geometry checks; accessibility and print limitations recorded.',flush=True)
