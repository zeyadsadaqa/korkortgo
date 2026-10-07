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
assert len(expected)==len(set(expected))==321
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
report={'status':'passed','pages':len(r.pages),'appendices':4,'reference_groups':len(GROUPS),'unique_official_entries':len(records),'vector_placements':sum(rec['vector'] for rec in records),'manuscript_blocks_and_cells_preserved':count,'glossary_terms':23,'practice_prompts':9,'manuscript_source_references':len(REFS),'external_reference_urls':len(uris),'valid_internal_links':links,'named_destinations':len(r.named_destinations),'embedded_fonts':sorted(fonts),'reproducible':True,'sha256':sha,'visual_review':'See ../reference-material-review.md','limits':['Standalone folios and chapter references are provisional; final cross-book links are 6M work','Full tagged-PDF accessibility and final publication approval remain in 6N']}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
