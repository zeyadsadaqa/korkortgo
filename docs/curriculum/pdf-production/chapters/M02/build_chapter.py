"""Step 6C: independently reproducible Chapter 2 review PDF."""
from pathlib import Path
import sys,json,re,hashlib,shutil
from xml.sax.saxutils import escape
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from build import *
from reportlab.platypus import Flowable
from PIL import Image
from pypdf.generic import NameObject,TextStringObject
OUT=Path(__file__).resolve().parent
MANUSCRIPT=(ROOT/'manuscript.md').read_text()
SOURCE='## 2. Prepare a car that is ready\n'+MANUSCRIPT.split('## 2. Prepare a car that is ready\n',1)[1].split('\n## 3. Read the road before acting',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M02-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={
'M02-L01':{'file':'M02-v3.png','box':[32,142,807,470],'polygon':[[32,166],[525,166],[540,142],[807,142],[807,470],[32,470]],'caption':'A learner consults the vehicle handbook beside a parked car. Establish the actual controls before driving; no universal dashboard layout is shown.'},
'M02-L02':{'file':'M02-v3.png','box':[833,146,1638,469],'caption':'A companion checks the rear of a stationary car and trailer. Check the trailer lights directly before moving.'},
'M02-L03':{'file':'M02-v3.png','box':[33,554,767,889],'caption':'An adult and child stand beside an open rear door. The empty booster and rear bench face forwards. This scene does not demonstrate installation or belt fit; follow the child-restraint and vehicle instructions.'},
'M02-L04':{'file':'parking-v3.png','box':[102,194,718,730],'width_mm':120,'caption':'A car and van occupy adjacent bays. A pedestrian is on the footway between the bays and the access lane. Consider what the driver may lose sight of. Diagram not to scale.'},
'M02-L04-cabin':{'file':'M02-v3.png','box':[796,560,1635,888],'width_mm':115,'caption':'The driver is in the left-hand seat and looks around before moving. Controls are illustrative; learn the actual vehicle.'},
'M02-R':{'file':'parking-v3.png','box':[777,156,1464,729],'width_mm':120,'polygon':[[777,156],[1464,156],[1464,729],[844,729],[844,446],[777,446]],'caption':'An unfamiliar car, a child with an adult, and confined parking beside a van. The footway separates the bays from the access lane. No manoeuvre is selected; diagram not to scale.'}}


def para(text,style='body'):
    safe=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(text))
    safe=re.sub(r'\[([^]]+)\]\[([^]]+)\]',lambda m:f'<link href="{escape(REFS[m[2]],{chr(34):"&quot;"})}" color="#173E32">{m[1]}</link>',safe)
    return Paragraph(safe,STYLES[style])

class Scene(Flowable):
    """Non-destructive image placement: clip the approved board at PDF render time."""
    def __init__(self,key):
        Flowable.__init__(self);self.rec=ART[key];self.width=self.rec.get('width_mm',170)*mm
        l,t,r,b=self.rec['box'];self.height=self.width*(b-t)/(r-l)
    def draw(self):
        rec=self.rec;c=self.canv;l,t,r,b=rec['box'];p=ROOT/'pdf-design/gap-resolution'/rec['file']
        iw,ih=Image.open(p).size;s=self.width/(r-l)
        c.saveState();c.translate((WIDTH-self.width)/2,0);c._code.append('/Span << /ActualText <FEFF'+rec['caption'].encode('utf-16-be').hex() + '> >> BDC');path=c.beginPath();
        if 'polygon' in rec:
            points=rec['polygon'];path.moveTo((points[0][0]-l)*s,(b-points[0][1])*s)
            for px,py in points[1:]:path.lineTo((px-l)*s,(b-py)*s)
            path.close()
        else:path.rect(0,0,self.width,self.height)
        c.clipPath(path,stroke=0)
        c.drawImage(str(p),-l*s,-(ih-b)*s,iw*s,ih*s);c._code.append('EMC');c.restoreState()

class Chapter(BookCanvas):
    def __init__(self,path):
        super().__init__(path);self.questions={};self.answers={};self.page_labels={}
        self.c.setTitle('KörkortGo | Chapter 2 | Prepare a car that is ready')
    def start(self,key,label,**kw):
        super().start(key,label,**kw);self.page_labels[self.page]=label
        if self.page==1:self.c.bookmarkPage('contents')
    def text(self,text,style='body',space=12):self.add(para(text,style),space)
    def art(self,key):
        self.add(Scene(key),7);self.text(ART[key]['caption'],'caption',18)
    def lines(self,n=5):
        self.c.setStrokeColor(COLORS['line']);self.c.setLineWidth(.5)
        for _ in range(n):
            self.y-=22
            if self.y<32*mm:raise ValueError(f'Writing lines overflow on page {self.page}')
            self.c.line(M,self.y,W-M,self.y)
        self.y-=14

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Chapter(OUT/'chapter.pdf');answers=[]
    b.start('M02','Chapter 2',next_page=('M02-L01','M02-L01'))
    b.text('CHAPTER 02','source');b.text('Prepare a car that is ready','heading')
    b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24)
    b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():
        b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    b.add(Paragraph('<link href="#M02-answers" color="#173E32">Answers and review guidance</link>',STYLES['body']))
    b.add(Paragraph('<link href="#M02-references" color="#173E32">Official references</link>',STYLES['body']),24)
    disclaimer=re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1)
    b.add(panel(disclaimer,'disclaimer'));b.end()
    for num in range(1,5):
        key=f'M02-L{num:02d}';s=SECTIONS[key];paras=s['paragraphs'];goal=paras[0]
        worked=next(p for p in paras if p.startswith('**Worked decision.**'))
        check=next(p for p in paras if p.startswith('**Knowledge check.**'))
        q,a=check.split(' **Answer:** ',1);answers.append((key,a))
        remember=paras[-1];body=paras[1:paras.index(worked)]
        # Two pages per lesson keep scene + worked situation + check together.
        b.start(key,key,next_page=(key+' scenario',key+'-scenario'))
        b.text(key,'source');b.text(s['title'],'heading');b.add(panel(goal),18)
        first=body
        for p in first:
            b.text(p)
        if num==4:b.art('M02-L04-cabin')
        b.end()
        b.start(key+'-scenario',key+' · Worked decision',next_page=(f'M02-L{num+1:02d}' if num<4 else 'M02-R',f'M02-L{num+1:02d}' if num<4 else 'M02-R'))
        b.text('Apply the learning','subheading')
        b.art(key)
        b.text(worked)
        b.text(q);b.questions[key]=b.page
        b.lines(3)
        b.text(remember,'caption');b.end()
    review=SECTIONS['M02-R']['paragraphs']
    question,review_answer=review[1].split(' **Review guide:** ',1)
    b.start('M02-R','M02-R · Self-assessment',next_page=('Reflect','M02-reflection'))
    b.text('Review and self-assessment','heading');b.art('M02-R');b.text(review[0]);b.text(question)
    b.questions['M02-R']=b.page;b.lines(3);b.end()
    b.start('M02-reflection','M02-R · Reflection',next_page=('Review your answers','M02-answers'))
    b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M02-answers','Answers and review guidance',next_page=('Official references','M02-references'))
    b.text('Review after answering','heading')
    for key,a in answers:
        b.text(key,'source',6);b.text('**Answer:** '+a,space=20);b.answers[key]=b.page
    b.text('M02-R','source',6);b.text('**Review guide:** '+review_answer);b.answers['M02-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M02-references' if offset==0 else f'M02-references-{offset//4+1}'
        b.start(key,'Official references');b.text('Official references','heading')
        b.text('Official sources checked 4 October 2026. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            url=REFS[alias];b.text(LABELS[alias],'body',4)
            b.add(Paragraph(f'<link href="{escape(url)}" color="#173E32">{escape(url)}</link>',STYLES['source']),20)
        b.end()
    b.c.save()
    r=PdfReader(OUT/'chapter.pdf');w=PdfWriter();w.clone_document_from_reader(r);w.root_object[NameObject('/Lang')]=TextStringObject('en-GB')
    w.root_object.pop(NameObject('/Outlines'),None)
    parent=w.add_outline_item('Chapter 2 · Prepare a car that is ready',0)
    lesson_parents={}
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M02':continue
        if key.endswith('-scenario'):
            w.add_outline_item('Worked decision and knowledge check',num-1,parent=lesson_parents[key.removesuffix('-scenario')])
        elif key in SECTIONS:
            lesson_parents[key]=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key=='M02-reflection':w.add_outline_item('Reflection',num-1,parent=lesson_parents['M02-R'])
        else:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels},indent=2)+'\n')
    for key,v in ART.items():
        p=ROOT/'pdf-design/gap-resolution'/v['file'];v['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops; screen review','assets':ART,'required_sign_assets':[],'text_only':[]},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-02.pdf')
    print(f'Built {len(r.pages)} pages')
if __name__=='__main__':run()
