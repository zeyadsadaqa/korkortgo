"""Check chapter fidelity and assessment separation against the manuscript."""
from build_chapter import *
import pdfplumber,subprocess
norm=lambda s:re.sub(r'\s+',' ',s).strip()
def clean(s):return norm(re.sub(r'\[([^]]+)\]\[[^]]+\]',r'\1',s).replace('**',''))
pdf=OUT/'chapter.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==15
texts=[norm(p.extract_text()) for p in reader.pages]
alltext=' '.join(texts);verified=0
for key,sec in SECTIONS.items():
    for par in sec['paragraphs']:
        for part in re.split(r'(?=\*\*(?:Answer:|Review guide:)\*\*)',par):
            assert clean(part) in alltext,(key,part);verified+=1
assert clean(PARTS[0].split('\n\n',1)[1]) in alltext
nav=json.loads((OUT/'navigation.json').read_text())
for key,q in nav['questions'].items():
    a=nav['answers'][key];assert a-q>=2
    assert '**Answer:**' not in texts[q-1]
    if key!='M02-R':
        answer=next(p for p in SECTIONS[key]['paragraphs'] if p.startswith('**Knowledge check.**')).split(' **Answer:** ')[1]
    else:answer=SECTIONS[key]['paragraphs'][1].split(' **Review guide:** ')[1]
    assert clean(answer) in texts[a-1] and clean(answer) not in texts[q-1]
fonts=set();links=0;uris=set();page_ids={p.indirect_reference.idnum for p in reader.pages}
for p in reader.pages:
    for annot in p.get('/Annots',[]):
        a=annot.get_object()
        if '/Dest' in a:assert a['/Dest'][0].idnum in page_ids;links+=1
        elif '/A' in a:uris.add(str(a['/A']['/URI']))
    for font in p['/Resources']['/Font'].values():
        f=font.get_object();assert f['/FontDescriptor'].get_object().get('/FontFile2');assert '/ToUnicode' in f;fonts.add(str(f['/BaseFont']))
assert uris=={REFS[k] for k in ALIASES}
assert reader.trailer['/Root']['/Lang']=='en-GB'
assert len(reader.named_destinations)==16
assert all(key in reader.named_destinations for key in SECTIONS)
for i in [2,4,6,7,8,9]:assert b'/ActualText' in reader.pages[i].get_contents().get_data()
with pdfplumber.open(pdf) as doc:
    for p in doc.pages:
        for ch in p.chars:
            assert 0<=ch['x0']<ch['x1']<=p.width+.1
            assert 0<=ch['top']<ch['bottom']<=p.height+.1
assert 'körkort online' not in alltext.lower() and 'theory-book' not in alltext.lower()
approvals=json.loads((ROOT/'pdf-design/gap-resolution/approval-record.json').read_text())['previews']
for rec in ART.values():
    path=ROOT/'pdf-design/gap-resolution'/rec['file']
    approved=next(a for a in approvals if a['path'].endswith('/'+rec['file']))
    assert hashlib.sha256(path.read_bytes()).hexdigest()==approved['sha256']
assert (OUT/'chapter-source.md').read_text().startswith(SOURCE)
first=hashlib.sha256(pdf.read_bytes()).hexdigest()
subprocess.run([sys.executable,str(OUT/'build_chapter.py')],check=True,capture_output=True)
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==first
report={'status':'passed','pages':15,'complete_lessons':4,'module_reviews':1,'manuscript_blocks_preserved':verified,'illustrations':6,'image_actualtext_descriptions':6,'official_signs_required':0,'official_reference_urls':len(uris),'valid_internal_links':links,'named_destinations':16,'embedded_fonts':sorted(fonts),'answers_non_facing':True,'sha256':first,'reproducible':True,'visual_review':'15 pages inspected; review.md','release_limits':['Screen-review image resolution; print masters remain separate','Full tagged-PDF accessibility and final navigation/pagination checked in 6M–6N']}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
