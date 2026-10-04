"""Verify manuscript fidelity, exact official asset bindings and PDF navigation."""
from build_chapter import *
import pdfplumber,subprocess
norm=lambda s:re.sub(r'\s+',' ',s).strip()
def clean(s):return norm(re.sub(r'\[([^]]+)\]\[[^]]+\]',r'\1',s).replace('**',''))
pdf=OUT/'chapter.pdf';reader=PdfReader(pdf);texts=[norm(p.extract_text()) for p in reader.pages];alltext=' '.join(texts);verified=0
for key,sec in SECTIONS.items():
    for par in sec['paragraphs']:
        if par.startswith('|'):
            for line in par.splitlines():
                if line.startswith('|---'):continue
                for cell in line.strip('|').split('|'):assert clean(cell) in alltext
            verified+=1;continue
        for part in re.split(r'(?=\*\*(?:Answer:|Review guide:)\*\*)',par):
            assert clean(part) in alltext,(key,part);verified+=1
assert clean(PARTS[0].split('\n\n',1)[1]) in alltext
nav=json.loads((OUT/'navigation.json').read_text());art=json.loads((OUT/'illustrations.json').read_text())
for key,q in nav['questions'].items():
    a=nav['answers'][key];assert a-q>=2
    answer=next(p for p in SECTIONS[key]['paragraphs'] if p.startswith('**Knowledge check.**')).split(' **Answer:** ')[1] if key!='M03-R' else SECTIONS[key]['paragraphs'][1].split(' **Review guide:** ')[1]
    assert clean(answer) in texts[a-1] and clean(answer) not in texts[q-1]
fonts=set();links=0;uris=set();page_ids={p.indirect_reference.idnum for p in reader.pages}
for p in reader.pages:
    for annot in p.get('/Annots',[]):
        a=annot.get_object()
        if '/Dest' in a:assert a['/Dest'][0].idnum in page_ids;links+=1
        elif '/A' in a:uris.add(str(a['/A']['/URI']))
    for font in p['/Resources'].get('/Font',{}).values():
        f=font.get_object();assert f['/FontDescriptor'].get_object().get('/FontFile2');assert '/ToUnicode' in f;fonts.add(str(f['/BaseFont']))
assert {REFS[k] for k in ALIASES}<=uris
assert reader.trailer['/Root']['/Lang']=='en-GB'
assert all(key in reader.named_destinations for key in SECTIONS)
for pg in nav['scene_pages'].values():assert b'/ActualText' in reader.pages[pg-1].get_contents().get_data()
records=art['official_sign_placements']
for group in GROUPS:
    gid=group['placement_id'];assert gid in nav['group_pages']
    if gid=='LP014':continue
    assert [r['code'] for r in records if r['group']==gid]==[i['code'] for i in group['items']]
for rec in records:
    bind=BINDINGS[rec['code']];asset=bind['preferred_asset'];assert rec['sha256']==asset['sha256']==hashlib.sha256((REPO/rec['path']).read_bytes()).hexdigest()
    assert bind['official_url'] in uris
    assert clean(CAPTIONS[rec['code']]['teaching_caption_en']) in texts[rec['page']-1]
    if rec['vector']:assert rec['width_mm']+.001>=asset['minimum_reviewed_width_mm']
    else:
        assert rec['width_mm']<=asset['max_size_mm_at_300ppi'][0]+.001
        assert rec['height_mm']<=asset['max_size_mm_at_300ppi'][1]+.001
    assert b'/ActualText' in reader.pages[rec['page']-1].get_contents().get_data()
with pdfplumber.open(pdf) as doc:
    for p in doc.pages:
        for ch in p.chars:assert 0<=ch['x0']<ch['x1']<=p.width+.1 and 0<=ch['top']<ch['bottom']<=p.height+.1,(p.page_number,ch)
assert 'körkort online' not in alltext.lower() and 'theory-book' not in alltext.lower()
approvals=json.loads((ROOT/'pdf-design/gap-resolution/approval-record.json').read_text())['previews']
for rec in ART.values():
    approved=next(a for a in approvals if a['path'].endswith('/'+rec['file']))
    assert hashlib.sha256((ROOT/'pdf-design/gap-resolution'/rec['file']).read_bytes()).hexdigest()==approved['sha256']
assert (OUT/'chapter-source.md').read_text().startswith(SOURCE)
first=hashlib.sha256(pdf.read_bytes()).hexdigest();subprocess.run([sys.executable,str(OUT/'build_chapter.py')],check=True,capture_output=True);assert hashlib.sha256(pdf.read_bytes()).hexdigest()==first
report={'status':'passed','pages':len(reader.pages),'complete_lessons':4,'module_reviews':1,'manuscript_blocks_preserved':verified,'illustrations':len(ART),'official_sign_placements':len(records),'unique_official_assets':len({r['code'] for r in records}),'required_groups':len(GROUPS),'vector_placements':sum(r['vector'] for r in records),'official_reference_urls':len(uris),'valid_internal_links':links,'named_destinations':len(reader.named_destinations),'embedded_fonts':sorted(fonts),'answers_non_facing':True,'sha256':first,'reproducible':True,'visual_review':'See review.md','release_limits':['Approved scene crops are screen-review resolution; print masters remain separate','Full tagged-PDF accessibility and final navigation/pagination checked in 6M–6N']}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
