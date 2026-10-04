"""Step 6B: independently reproducible Chapter 1 review PDF."""
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
SOURCE='## 1. Choose to drive responsibly\n'+MANUSCRIPT.split('## 1. Choose to drive responsibly\n',1)[1].split('\n## 2. Prepare a car that is ready',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M01-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={
'M01-L02':{'file':'M01-v2.png','box':[35,171,827,501],'caption':'A tired learner and a companion pause beside a parked car. The keys remain on the bench.'},
'M01-L03':{'file':'M01-v2.png','box':[857,158,1631,501],'caption':'A passenger talks to the driver. In the road view, the car remains behind a van near a crest. Illustration, not a scale diagram of following distance.'},
'M01-L04':{'file':'F06-v4.png','box':[28,153,715,507],'caption':'Viewed over their shoulders, two people study a digital map on a tablet facing them. Rain falls outside. The map is illustrative, not live route guidance.'},
'M01-R':{'file':'M01-v2.png','box':[855,615,1631,755],'caption':'Three conditions to consider: tiredness, an appointment and worsening weather. No choice is shown.'}}

def para(text,style='body'):
    safe=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(text))
    safe=re.sub(r'\[([^]]+)\]\[([^]]+)\]',lambda m:f'<link href="{escape(REFS[m[2]],{chr(34):"&quot;"})}" color="#173E32">{m[1]}</link>',safe)
    return Paragraph(safe,STYLES[style])

class Scene(Flowable):
    """Non-destructive image placement: clip the approved board at PDF render time."""
    def __init__(self,key):
        Flowable.__init__(self);self.rec=ART[key];self.width=WIDTH
        l,t,r,b=self.rec['box'];self.height=WIDTH*(b-t)/(r-l)
    def draw(self):
        rec=self.rec;c=self.canv;l,t,r,b=rec['box'];p=ROOT/'pdf-design/gap-resolution'/rec['file']
        iw,ih=Image.open(p).size;s=self.width/(r-l)
        c.saveState();c._code.append('/Span << /ActualText <FEFF'+rec['caption'].encode('utf-16-be').hex() + '> >> BDC');path=c.beginPath();path.rect(0,0,self.width,self.height);c.clipPath(path,stroke=0)
        c.drawImage(str(p),-l*s,-(ih-b)*s,iw*s,ih*s);c._code.append('EMC');c.restoreState()

class Chapter(BookCanvas):
    def __init__(self,path):
        super().__init__(path);self.questions={};self.answers={};self.page_labels={}
        self.c.setTitle('KörkortGo | Chapter 1 | Choose to drive responsibly')
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
            if self.y<32*mm:raise ValueError('Writing lines overflow')
            self.c.line(M,self.y,W-M,self.y)
        self.y-=14

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Chapter(OUT/'chapter.pdf');answers=[]
    b.start('M01','Chapter 1',next_page=('M01-L01','M01-L01'))
    b.text('CHAPTER 01','source');b.text('Choose to drive responsibly','heading')
    b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24)
    b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():
        b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    b.add(Paragraph('<link href="#M01-answers" color="#173E32">Answers and review guidance</link>',STYLES['body']))
    b.add(Paragraph('<link href="#M01-references" color="#173E32">Official references</link>',STYLES['body']),24)
    disclaimer=re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1)
    b.add(panel(disclaimer,'disclaimer'));b.end()
    for num in range(1,5):
        key=f'M01-L{num:02d}';s=SECTIONS[key];paras=s['paragraphs'];goal=paras[0]
        worked=next(p for p in paras if p.startswith('**Worked decision.**'))
        check=next(p for p in paras if p.startswith('**Knowledge check.**'))
        q,a=check.split(' **Answer:** ',1);answers.append((key,a))
        remember=paras[-1];body=paras[1:paras.index(worked)]
        # Two pages per lesson keep scene + worked situation + check together.
        b.start(key,key,next_page=(key+' scenario',key+'-scenario'))
        b.text(key,'source');b.text(s['title'],'heading');b.add(panel(goal),18)
        first=body[:3] if num==1 else body
        for p in first:
            if num==4 and p==body[0]:
                b.text('Official advice · Trafikverket','source',6)
            b.text(p)
        b.end()
        b.start(key+'-scenario',key+' · Worked decision',next_page=(f'M01-L{num+1:02d}' if num<4 else 'M01-R',f'M01-L{num+1:02d}' if num<4 else 'M01-R'))
        b.text('Apply the learning','subheading')
        if num==1:
            for p in body[3:]:b.text(p)
        else:b.art(key)
        b.text(worked)
        b.text(q);b.questions[key]=b.page
        b.lines(3 if num!=1 else 5)
        b.text(remember,'caption');b.end()
    review=SECTIONS['M01-R']['paragraphs']
    question,review_answer=review[1].split(' **Review guide:** ',1)
    b.start('M01-R','M01-R · Self-assessment',next_page=('Reflect','M01-reflection'))
    b.text('Review and self-assessment','heading');b.art('M01-R');b.text(review[0]);b.text(question)
    b.questions['M01-R']=b.page;b.lines(9);b.end()
    b.start('M01-reflection','M01-R · Reflection',next_page=('Review your answers','M01-answers'))
    b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M01-answers','Answers and review guidance',next_page=('Official references','M01-references'))
    b.text('Review after answering','heading')
    for key,a in answers:
        b.text(key,'source',6);b.text('**Answer:** '+a,space=20);b.answers[key]=b.page
    b.text('M01-R','source',6);b.text('**Review guide:** '+review_answer);b.answers['M01-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M01-references' if offset==0 else f'M01-references-{offset//4+1}'
        b.start(key,'Official references');b.text('Official references','heading')
        b.text('Official sources checked 4 October 2026. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            url=REFS[alias];b.text(LABELS[alias],'body',4)
            b.add(Paragraph(f'<link href="{escape(url)}" color="#173E32">{escape(url)}</link>',STYLES['source']),20)
        b.end()
    b.c.save()
    r=PdfReader(OUT/'chapter.pdf');w=PdfWriter();w.clone_document_from_reader(r);w.root_object[NameObject('/Lang')]=TextStringObject('en-GB')
    w.root_object.pop(NameObject('/Outlines'),None)
    parent=w.add_outline_item('Chapter 1 · Choose to drive responsibly',0)
    lesson_parents={}
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M01':continue
        if key.endswith('-scenario'):
            w.add_outline_item('Worked decision and knowledge check',num-1,parent=lesson_parents[key.removesuffix('-scenario')])
        elif key in SECTIONS:
            lesson_parents[key]=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key=='M01-reflection':w.add_outline_item('Reflection',num-1,parent=lesson_parents['M01-R'])
        else:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels},indent=2)+'\n')
    for key,v in ART.items():
        p=ROOT/'pdf-design/gap-resolution'/v['file'];v['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(WIDTH/72),1)
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops; screen review','assets':ART,'required_sign_assets':[],'text_only':['M01-L01']},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-01.pdf')
    print(f'Built {len(r.pages)} pages')
if __name__=='__main__':run()
