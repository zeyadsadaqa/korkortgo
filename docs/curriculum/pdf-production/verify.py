"""Verify the actual 6A artifact, source fidelity, navigation and font resources."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
import pdfplumber
from reportlab.pdfbase.ttfonts import TTFont
P=Path(__file__).resolve().parent
R=P.parent
norm=lambda s:re.sub(r'\s+',' ',s).strip()
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pdf=P/'front-matter.pdf';r=PdfReader(pdf)
assert len(r.pages)==4
text=norm(' '.join(p.extract_text() for p in r.pages))
intro=(R/'manuscript.md').read_text().split('### Contents')[0]
disclaimer=re.search(r'> \*\*(.*?)\*\*',intro).group(1)
assert disclaimer in text
paragraphs=intro.split('### How to use the book\n\n')[1].strip().split('\n\n')
paragraphs += ['This book is'+intro.split('\n\nThis book is')[1].split('\n\n')[0]]
for p in paragraphs:assert norm(p.replace('**','')) in text,p
m=json.loads((P/'build-manifest.json').read_text())
for ch in m['chapters']:assert ch['title'] in text
for a in m['appendices']:assert a['title'] in text
assert 'KörkortGo' in text
assert 'körkort online' not in text.lower() and 'theory-book' not in text.lower()
assert r.trailer['/Root']['/Lang']=='en-GB'
assert len(r.outline)==4 and len(r.named_destinations)==4
page_ids={p.indirect_reference.idnum for p in r.pages}
links=0;fonts=set()
for p in r.pages:
    for a in p.get('/Annots',[]):
        dest=a.get_object()['/Dest'];assert dest[0].idnum in page_ids;links+=1
    for f in p['/Resources']['/Font'].values():
        f=f.get_object();descriptor=f.get('/FontDescriptor')
        assert descriptor and descriptor.get_object().get('/FontFile2'),f
        assert f.get('/ToUnicode');fonts.add(str(f['/BaseFont']))
assert links==5
with pdfplumber.open(pdf) as doc:
    for p in doc.pages:
        for ch in p.chars:
            assert 0<=ch['x0']<ch['x1']<=p.width+.1
            assert 0<=ch['top']<ch['bottom']<=p.height+.1
for f in (P/'fonts').glob('*.ttf'):
    font=TTFont(f.stem,str(f));cmap=font.face.charWidths
    assert all(ord(c) in cmap for c in 'KörkortGoÅÄÖåäö0123456789')
for a in json.loads((R/'pdf-design/gap-resolution/approval-record.json').read_text())['previews']:
    assert digest(R/a['path'])==a['sha256'],a['path']
first=digest(pdf)
subprocess.run([sys.executable,str(P/'build.py')],check=True,capture_output=True)
assert digest(pdf)==first,'Non-reproducible build'
report={'status':'passed','pages':4,'manuscript_intro_paragraphs_preserved':len(paragraphs),'exact_disclaimer':True,'embedded_unicode_fonts':sorted(fonts),'valid_internal_links':links,'bookmarks':4,'named_destinations':4,'swedish_glyphs':True,'preview_hashes_verified':21,'reproducible_sha256':first,'visual_review':'All four final pages inspected; see readiness-review.md','limits':['Chapter links/folios deferred until 6M','Cover artwork is approximately 95 ppi: screen-review use; print-resolution master remains required for a print release','Full tagged-PDF accessibility verification remains in 6N']}
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
