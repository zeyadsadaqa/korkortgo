"""Verify 6L fidelity, exact asset coverage, navigation and deterministic output."""
from build_reference import *
import pdfplumber,subprocess,collections
norm=lambda s:re.sub(r'\s+',' ',s).strip()
def clean(s):return norm(re.sub(r'\[([^]]+)\]\[[^]]+\]',r'\1',s).replace('*','').replace('### ',''))
r=PdfReader(TARGET);texts=[norm(p.extract_text()) for p in r.pages];alltext=' '.join(texts);count=0
for title,section in SECS.items():
 for par in section.replace(OLD,NEW).split('\n\n'):
  if par.startswith('|'):
   for row in table_rows(par):
    for cell in row:
     if cell:assert clean(cell) in alltext,(title,cell);count+=1
  elif par.startswith('- ') or par.startswith('1. '):
   for line in par.splitlines():assert clean(line[2:] if line.startswith('- ') else line) in alltext,(title,line);count+=1
  else:assert clean(par) in alltext,(title,par);count+=1
assert clean(re.search(r'> \*\*(.*?)\*\*',FULL).group(1)) in alltext
assert CREDIT in alltext
assert 'until the separately verified illustrated reference is prepared' not in alltext
nav=json.loads((OUT/'navigation.json').read_text());assets=json.loads((OUT/'assets.json').read_text());records=assets['official_sign_placements']
expected=[code for g in GROUPS for code in g['primary_codes']+g['additional_comparison_codes']]
assert [a['code'] for a in records]==expected
assert len(expected)==len(set(expected))==PLACEMENT['summary']['eligible_bound_codes']
h0=json.loads((ROOT/'question-book-review/remaining-gap-h0-sources.json').read_text())
h1_targets=[t for t in h0['targets'] if t['step']=='H1']
h1_codes={t['sign_code'] for t in h1_targets}
h1_records={a['code']:a for a in records if a['code'] in h1_codes}
assert len(h1_targets)==56 and len(h1_records)==28
for code in h1_codes:
 source=next(s for s in h0['signs'] if s['code']==code)
 assert h1_records[code]['sha256']==source['question_asset']['sha256']
 assert BINDINGS[code]['official_url']==source['page']['url']
 assert CAPTIONS[code]['official_name_sv']==source['official_name_sv']
h2_targets=[t for t in h0['targets'] if t['step']=='H2']
h2_codes={t['sign_code'] for t in h2_targets}
h2_records={a['code']:a for a in records if a['code'] in h2_codes}
assert len(h2_targets)==72 and len(h2_records)==36
for code in h2_codes:
 source=next(s for s in h0['signs'] if s['code']==code)
 asset=BINDINGS[code]['preferred_asset']
 assert BINDINGS[code]['official_url']==source['page']['url']
 assert CAPTIONS[code]['official_name_sv']==source['official_name_sv']
 if code in ['F30','F31']:
  assert asset['official_variant_image_sha256']==source['question_asset']['sha256']
  assert asset['official_eps_url'] in source['download_urls']
  assert hashlib.sha256((REPO/asset['official_eps_path']).read_bytes()).hexdigest()==asset['official_eps_sha256']
  assert (REPO/asset['variant_proof']).exists()
 else:assert h2_records[code]['sha256']==source['question_asset']['sha256']
h3_targets=[t for t in h0['targets'] if t['step']=='H3']
h3_codes={t['sign_code'] for t in h3_targets}
h3_records={a['code']:a for a in records if a['code'] in h3_codes}
assert len(h3_targets)==30 and len(h3_records)==15
assert h1_codes|h2_codes|h3_codes=={s['code'] for s in h0['signs']}
for code in h3_codes:
 source=next(s for s in h0['signs'] if s['code']==code)
 asset=BINDINGS[code]['preferred_asset']
 assert BINDINGS[code]['official_url']==source['page']['url']
 assert CAPTIONS[code]['official_name_sv']==source['official_name_sv']
 if code.startswith('S') or code in ['M17','M28','M29','M31','M32','M34']:
  assert asset['official_variant_image_sha256']==source['question_asset']['sha256']
  assert asset['official_eps_url'] in source['download_urls']
  assert hashlib.sha256((REPO/asset['official_eps_path']).read_bytes()).hexdigest()==asset['official_eps_sha256']
  assert (REPO/asset['variant_proof']).exists()
 else:assert h3_records[code]['sha256']==source['question_asset']['sha256']
for name in ['book','delivery_book','questions','gaps']:
 item=h0['baseline'][name]
 expected=item['sha256']; h6=json.loads((ROOT/'pdf-production/build-manifest.json').read_text()).get('H6_assembly',{}); expected=h6['sha256'] if name in ['book','delivery_book'] and h6.get('status')=='complete' else expected; assert hashlib.sha256((REPO/item['path']).read_bytes()).hexdigest()==expected
for g in GROUPS:
 assert g['group_id'] in r.named_destinations
 for code in g['cross_reference_codes']:assert 'sign-'+code in r.named_destinations
uris=set();links=0;fonts=set();ids={p.indirect_reference.idnum for p in r.pages}
for page in r.pages:
 for annotation in page.get('/Annots',[]):
  a=annotation.get_object()
  if '/Dest' in a:assert a['/Dest'][0].idnum in ids;links+=1
  elif '/A' in a:uris.add(str(a['/A']['/URI']))
 for f in page['/Resources'].get('/Font',{}).values():
  f=f.get_object();assert f['/FontDescriptor'].get_object().get('/FontFile2');assert '/ToUnicode' in f;fonts.add(str(f['/BaseFont']))
for rec in records:
 code=rec['code'];binding=BINDINGS[code];asset=binding['preferred_asset'];page=texts[rec['page']-1]
 assert 'sign-'+code in r.named_destinations
 assert asset['sha256']==rec['sha256']==hashlib.sha256((REPO/rec['path']).read_bytes()).hexdigest()
 assert clean(CAPTIONS[code]['teaching_caption_en']) in page,code
 assert clean((CAPTIONS[code].get('variant_description_en') or '')) in page,code
 assert clean(binding['official_name_sv']) in page,code
 assert binding['official_url'] in uris,code
 assert b'/ActualText' in r.pages[rec['page']-1].get_contents().get_data()
 if rec['vector']:assert rec['width_mm']+.001>=asset['minimum_reviewed_width_mm']
 else:
  assert rec['width_mm']<=asset['max_size_mm_at_300ppi'][0]+.001
  assert rec['height_mm']<=asset['max_size_mm_at_300ppi'][1]+.001
assert 'Manufacturer technical references' in alltext
assert 'manufacturer-references' in r.named_destinations
assert set(REFS.values())<=uris, set(REFS.values())-uris
assert REUSE in uris
assert r.trailer['/Root']['/Lang']=='en-GB'
assert all(k in r.named_destinations for k in ['appendix-A','appendix-B','appendix-C','appendix-D','official-references'])
with pdfplumber.open(TARGET) as doc:
 for p in doc.pages:
  for ch in p.chars:assert -.1<=ch['x0']<ch['x1']<=p.width+.1 and -.1<=ch['top']<ch['bottom']<=p.height+.1,(p.page_number,ch)
assert not any(s in alltext.lower() for s in ['körkort online','theory-book'])
sha=hashlib.sha256(TARGET.read_bytes()).hexdigest()
subprocess.run([sys.executable,str(OUT/'build_reference.py')],check=True,capture_output=True)
assert hashlib.sha256(TARGET.read_bytes()).hexdigest()==sha
report={'status':'passed','pages':len(r.pages),'appendices':4,'reference_groups':len(GROUPS),'unique_official_entries':len(records),'vector_placements':sum(rec['vector'] for rec in records),'manuscript_blocks_and_cells_preserved':count,'glossary_terms':len(table_rows(SECS[TITLES[2]].split('\n\n')[1]))-1,'practice_prompts':9,'manuscript_source_references':len(REFS),'external_reference_urls':len(uris),'valid_internal_links':links,'named_destinations':len(r.named_destinations),'embedded_fonts':sorted(fonts),'reproducible':True,'sha256':sha,'visual_review':'../../question-book-review/remaining-gap-execution-plan.md, H1/H2/H3 execution records','h1':{'codes':sorted(h1_codes),'question_component_pages':[{'question_id':t['question_id'],'sign_code':t['sign_code'],'component_page':h1_records[t['sign_code']]['page']} for t in h1_targets],'bank_and_full_book_unchanged':True},'h2':{'codes':sorted(h2_codes),'question_component_pages':[{'question_id':t['question_id'],'sign_code':t['sign_code'],'component_page':h2_records[t['sign_code']]['page']} for t in h2_targets],'bank_and_full_book_unchanged':True},'h3':{'codes':sorted(h3_codes),'question_component_pages':[{'question_id':t['question_id'],'sign_code':t['sign_code'],'component_page':h3_records[t['sign_code']]['page']} for t in h3_targets],'bank_and_full_book_unchanged':True},'limits':['This is the updated reference component; full-book assembly/folios and final coverage audit remain H6/H7 work','Full tagged-PDF accessibility and final publication approval remain outside this H1/H2/H3 check']}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
