"""Reproducible KörkortGo front matter and reusable ReportLab page components."""
from pathlib import Path
import hashlib, json, re, shutil
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, KeepTogether, Spacer
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent.parent
TOKENS = json.loads((REPO / 'design/brand/tokens.json').read_text())
COLORS = {k: HexColor(v) for k,v in (TOKENS['core'] | TOKENS['editorial']).items()}
W,H = A4
M = 20*mm
WIDTH = W-2*M
FONT_MAP = {'Body':'SourceSans3-Regular.ttf','BodyBold':'SourceSans3-Semibold.ttf',
            'Heading':'SourceSerif4-Bold.ttf','Subheading':'SourceSerif4-Semibold.ttf'}
for name, filename in FONT_MAP.items():
    pdfmetrics.registerFont(TTFont(name, str(HERE/'fonts'/filename)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='Body', boldItalic='BodyBold')
STYLES = {
 'body': ParagraphStyle('body', fontName='Body',fontSize=12,leading=17,textColor=COLORS['navy'],spaceAfter=12),
 'heading': ParagraphStyle('heading',fontName='Heading',fontSize=28,leading=34,textColor=COLORS['navy'],spaceAfter=18,keepWithNext=True),
 'subheading': ParagraphStyle('subheading',fontName='Subheading',fontSize=20,leading=26,textColor=COLORS['navy'],spaceAfter=12,keepWithNext=True),
 'caption': ParagraphStyle('caption',fontName='Body',fontSize=10,leading=14,textColor=COLORS['ink']),
 'source': ParagraphStyle('source',fontName='Body',fontSize=9.5,leading=13,textColor=COLORS['forest']),
}

def paragraph(text, style='body'):
    text = re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(text))
    return Paragraph(text, STYLES[style])

def panel(text, kind='goal'):
    """Auto-height approved labelled teaching panels; never shrink the type."""
    shade={'goal':'sage','advice':'mist','disclaimer':'cream','review':'sage'}[kind]
    t=Table([[paragraph(text)]],colWidths=[WIDTH])
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,-1),COLORS[shade]),
      ('BOX',(0,0),(-1,-1),.6,COLORS['gold'] if kind=='disclaimer' else COLORS[shade]),
      ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
      ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14)]))
    return t

def lesson_heading(identifier,title,goal):
    return [paragraph(identifier,'source'),Spacer(1,8),paragraph(title,'subheading'),panel('**Your goal:** '+goal),Spacer(1,18)]

def reference_table(rows,widths):
    """Reusable repeated-header reference table for later chapter builds."""
    t=Table([[paragraph(str(c),'caption') for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,0),COLORS['sage']),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8)]))
    return t

class BookCanvas:
    def __init__(self,path):
        self.c=canvas.Canvas(str(path),pagesize=A4,invariant=1,initialFontName='Body')
        self.c.setTitle('KörkortGo | Swedish category B learning guide')
        self.c.setAuthor('KörkortGo')
        self.c.setSubject('A learning aid for Swedish driving theory')
        self.destinations={}
        self.page=0
    def start(self,key,label,cover=False,previous=None,next_page=None):
        c=self.c;self.page+=1
        c.setFillColor(COLORS['paper']);c.rect(0,0,W,H,fill=1,stroke=0)
        c.bookmarkPage(key);c.addOutlineEntry(label,key,level=0)
        self.destinations[key]=self.page
        if not cover:
            c.setFillColor(COLORS['forest']);c.setFont('Body',10)
            c.drawString(M,H-20*mm,'KörkortGo · '+label)
            c.setStrokeColor(COLORS['gold']);c.setLineWidth(.5)
            c.line(M,H-23*mm,W-M,H-23*mm);c.line(M,23*mm,W-M,23*mm)
            c.drawCentredString(W/2,16*mm,str(self.page))
            c.drawString(M,16*mm,'Contents');c.linkRect('', 'contents',(M,14*mm,M+48,21*mm),relative=0,thickness=0)
            if next_page:
                title,dest=next_page;c.drawRightString(W-M,16*mm,title+' >')
                c.linkRect('',dest,(W-M-125,14*mm,W-M,21*mm),relative=0,thickness=0)
        self.y=H-34*mm
    def add(self,flow,space=12):
        w,h=flow.wrap(WIDTH,self.y-30*mm)
        if self.y-h<30*mm:raise ValueError(f'Page {self.page} overflow: {self.y-h}')
        flow.drawOn(self.c,M,self.y-h);self.y-=h+space
    def end(self):self.c.showPage()


def build():
    manifest=json.loads((HERE/'build-manifest.json').read_text())
    intro=(ROOT/'manuscript.md').read_text().split('### Contents')[0]
    disclaimer=re.search(r'> \*\*(.*?)\*\*',intro).group(1)
    audience=intro.split('\n\nThis book is')[1].split('\n\n')[0]
    audience='This book is'+audience
    paras=intro.split('### How to use the book\n\n')[1].strip().split('\n\n')
    out=HERE/'front-matter.pdf';b=BookCanvas(out);c=b.c
    b.start('cover','Cover',cover=True)
    # Place the approved artwork with a PDF clipping window; original raster is unchanged.
    # Only the left-page landscape below all generated typography is visible.
    source=ROOT/'pdf-design/5b/cover-opening-v4.png'
    scale=(W-20*mm)/710
    x=10*mm-25*scale;y=10*mm-15*scale
    c.saveState();clip=c.beginPath();clip.moveTo(10*mm,10*mm);clip.lineTo(W-10*mm,10*mm);clip.lineTo(W-10*mm,10*mm+745*scale);clip.lineTo(10*mm+575*scale,10*mm+650*scale);clip.lineTo(10*mm,10*mm+650*scale);clip.close();c.clipPath(clip,stroke=0)
    c.drawImage(str(source),x,y,width=1491*scale,height=1055*scale);c.restoreState()
    c.setStrokeColor(COLORS['forest']);c.setLineWidth(.8);c.rect(10*mm,10*mm,W-20*mm,H-20*mm,stroke=1,fill=0)
    c.setFillColor(COLORS['forest']);c.setFont('Heading',70);c.drawString(M,H-55*mm,'KörkortGo')
    c.setFont('Body',18);c.drawString(M,H-70*mm,'Swedish category B learning guide')
    c.setFont('Body',13);c.drawString(M,H-88*mm,'A learning aid')
    b.end()
    b.start('introduction','Before you begin',next_page=('How to use this book','study-guide'))
    b.add(paragraph('Before you begin','heading'))
    b.add(panel(disclaimer,'disclaimer'),20)
    b.add(paragraph(audience))
    b.add(paragraph('How to use this book','subheading'))
    for p in paras[:2]:b.add(paragraph(p))
    b.end()
    b.start('study-guide','How to use this book',next_page=('Contents','contents'))
    b.add(paragraph('Read, reflect and practise','heading'))
    for title,p in zip(['Read the labels','Use the official references','Check current guidance'],paras[2:]):
        b.add(paragraph(title,'subheading'));b.add(paragraph(p),24)
    b.end()
    b.start('contents','Contents')
    b.add(paragraph('Your learning journey','heading'),12)
    rows=[]
    for i,ch in enumerate(manifest['chapters'],1):
        rows.append([f'**{i:02d}**',ch['title']])
    t=Table([[paragraph(a),paragraph(b)] for a,b in rows],colWidths=[28,WIDTH-28],hAlign='LEFT')
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,0),COLORS['paper']),('LINEBELOW',(0,0),(-1,-1),.4,COLORS['gold']),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    b.add(t,24);b.add(paragraph('Keep these close','subheading'),8)
    for a in manifest['appendices']:
        b.add(paragraph('Appendix '+a['id'][-1]+' · '+a['title']),8)
    b.add(paragraph('Official references'))
    b.end();c.save()
    # Explicit PDF navigation targets only for pages actually present; chapter targets
    # remain in navigation.json until assembly, never pointing at fabricated pages.
    reader=PdfReader(out);writer=PdfWriter();writer.clone_document_from_reader(reader)
    from pypdf.generic import NameObject,TextStringObject
    writer.root_object[NameObject('/Lang')]=TextStringObject('en-GB')
    for key,num in b.destinations.items():writer.add_named_destination(key,num-1)
    with out.open('wb') as f:writer.write(f)
    nav={'built':b.destinations,'pending_assembly':[{ 'destination':ch['destination'],'title':ch['title'],'children':ch['lessons']+[ch['review']]} for ch in manifest['chapters']]+manifest['appendices']+[{'destination':'official-references'}]}
    (HERE/'navigation.json').write_text(json.dumps(nav,ensure_ascii=False,indent=2)+'\n')
    destination=REPO/'output/pdf/korkortgo-front-matter.pdf';destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(out,destination)
    print(f'Built {len(reader.pages)} pages: {out}')

if __name__=='__main__':build()
