"""Step 6D: independently reproducible Chapter 3 review PDF."""
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
SOURCE='## 3. Read the road before acting\n'+MANUSCRIPT.split('## 3. Read the road before acting\n',1)[1].split('\n## 4. Negotiate shared space',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M03-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={'M03-L01': {'box': [35, 164, 437, 515],
             'caption': 'A narrow rural bridge with an oncoming van. The scene shows the approach; the '
                        'separate official examples explain warnings and priority. Not to scale.',
             'file': 'M03-v4.png',
             'width_mm': 105},
 'M03-L02': {'box': [627, 164, 1105, 515],
             'caption': 'A green signal and a queue beyond the junction. Opposing traffic is separated and '
                        'the stop line is before the crossing road. The scene is illustrative, not to scale.',
             'file': 'M03-v4.png',
             'width_mm': 130},
 'M03-L03': {'box': [1135, 144, 1637, 377],
             'caption': 'Drivers approach a decision point in marked lanes. Plan the permitted route early. '
                        'The illustration does not assign destinations to particular lanes.',
             'file': 'M03-v4.png'},
 'M03-L03-follow': {'box': [1135, 411, 1637, 515],
                    'caption': 'Continue on the permitted route after a missed turn and find another safe '
                               'opportunity. Not to scale.',
                    'file': 'M03-v4.png'},
 'M03-L04': {'box': [36, 620, 620, 898],
             'caption': 'A driver approaches a queue on a divided road. The illustrated gap is not a '
                        'measured safe following distance. Look ahead and leave room to respond.',
             'file': 'M03-v4.png'},
 'M03-R': {'box': [1395, 599, 1635, 769],
           'caption': 'A junction approach with a changing traffic situation. Describe your decision before '
                      'reading the review guide. Not to scale.',
           'file': 'M03-v4.png',
           'width_mm': 85},
 'M03-R-route': {'box': [902, 599, 1141, 769],
                 'caption': 'A route decision on an unfamiliar road. Use the written scenario and the linked '
                            'official examples; these separate illustrations do not form one verified '
                            'junction.',
                 'file': 'M03-v4.png',
                 'width_mm': 85}}


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
        self.c.setTitle('KörkortGo | Chapter 3 | Read the road before acting')
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

PLACEMENT=json.loads((ROOT/'sign-placement-map.json').read_text())
GROUPS=[p for p in PLACEMENT['lesson_placements'] if p['location']['section_id'].startswith('M03')]
BINDINGS={b['code']:b for b in PLACEMENT['asset_caption_bindings']}
CAPTIONS={c['code']:c for c in json.loads((ROOT/'sign-captions.json').read_text())['captions']}
GROUP_TITLES=['Five sign families','Yield and stop','Narrow roads: warning and priority','Authorised directions','Ordinary vehicle signals','Lane and public-transport signals','Read the marking on your side','Read the supplementary panel','Advance directions and lane choice','Walking and cycling routes','Destinations and route numbers','Facilities and services','Limits and road regimes','Retrieve the examples']
GROUP_NOTES={
'LP001':'Separate examples, not a roadside assembly. Read each caption as well as the shape and colour.',
'LP002':'Signs and markings are labelled teaching counterparts. These examples do not establish their position in a particular road scene.',
'LP003':'Compare the three narrowing shapes. B6 and B7 show opposing viewpoints, never simultaneous instructions to one approach.',
'LP004':'Separate examples. A static picture does not show the complete movement; read the description and the official instruction.',
'LP005':'Red, red/amber, green and amber appear in that order. Flashing amber is a separate condition, not the next stage of the normal cycle. Arrow indications apply to the direction shown.',
'LP006':'Lane-control signals and public-transport signals are separate sets. Follow the instruction that applies to your lane and traffic.',
'LP007':'For paired lines, identify the line immediately beside your side of the road. The line on the far side does not grant you permission to cross.',
'LP008':'Independent recognition examples. A supplementary panel qualifies the sign above it on the road; these examples are not stacked into an invented instruction.',
'LP009':'Sample destinations are independent examples. They do not describe one continuous route.',
'LP010':'These walking and cycling examples are separate from car-route guidance. Standalone symbols retain their own official meaning.',
'LP011':'Compare route numbers and solid or dashed borders. The permanent alternative-route example is distinct from temporary orange guidance.',
'LP012':'Separate reference examples for recognising facilities, services and tourist routes.',
'LP013':'Numeric maximum-speed examples are independent. Start and end types are labelled individually; unequal values do not form a sequence.'}

class SignCard(Flowable):
    def __init__(self,code,b,group):
        Flowable.__init__(self);self.code=code;self.book=b;self.group=group
        self.bind=BINDINGS[code];self.cap=CAPTIONS[code];self.asset=self.bind['preferred_asset'];self.path=REPO/self.asset['path']
        assert self.bind['eligibility'] and hashlib.sha256(self.path.read_bytes()).hexdigest()==self.asset['sha256']
        self.vector=self.path.suffix=='.pdf'
        if self.vector:
            page=PdfReader(self.path).pages[0];iw,ih=float(page.mediabox.width),float(page.mediabox.height)
            self.iw=self.asset['minimum_reviewed_width_mm']*mm;self.ih=self.iw*ih/iw
            self.tw=WIDTH;self.tx=0
        else:
            iw,ih=Image.open(self.path).size
            maxw,maxh=self.asset['max_size_mm_at_300ppi']
            scale=min(70*mm/iw,48*mm/ih,maxw*mm/iw,maxh*mm/ih)
            self.iw=iw*scale;self.ih=ih*scale;self.tw=WIDTH-78*mm;self.tx=78*mm
        caption=self.cap['teaching_caption_en']
        variant=self.cap.get('variant_description_en')
        if variant:caption+=' '+variant
        self.flows=[para('**'+code+' · '+self.bind['label_en']+'**','caption'),para(self.bind['official_name_sv'],'source'),para(caption,'caption'),Paragraph('<link href="'+escape(self.bind['official_url'])+'" color="#173E32">Transportstyrelsen · official description</link>',STYLES['source'])]
        self.th=sum(f.wrap(self.tw,1000)[1]+5 for f in self.flows)
        self.width=WIDTH;self.height=(self.ih+12+self.th if self.vector else max(self.ih,self.th))+18
    def draw(self):
        c=self.canv;top=self.height-9
        x=(WIDTH-self.iw)/2 if self.vector else (70*mm-self.iw)/2
        y=top-self.ih
        alt=self.bind['alt_text_en']
        if self.vector:
            c.saveState();c.setFillColor(HexColor('#FFFFFF'));c.rect(x,y,self.iw,self.ih,fill=1,stroke=0);c.restoreState()
            _,ay=c.absolutePosition(0,y);ax,_=c.absolutePosition(x,0)
            self.book.vectors.append({'page':self.book.page,'path':self.asset['path'],'x':ax,'y':ay,'width':self.iw,'height':self.ih,'alt':alt})
        else:
            c._code.append('/Span << /ActualText <FEFF'+alt.encode('utf-16-be').hex()+'> >> BDC')
            c.drawImage(str(self.path),x,y,self.iw,self.ih,mask='auto');c._code.append('EMC')
        texty=y-12 if self.vector else top
        for f in self.flows:
            _,h=f.wrap(self.tw,1000);f.drawOn(c,self.tx,texty-h);texty-=h+5
        c.setStrokeColor(COLORS['line']);c.setLineWidth(.4);c.line(0,0,WIDTH,0)
        self.book.sign_records.append({'group':self.group,'code':self.code,'page':self.book.page,'path':self.asset['path'],'sha256':self.asset['sha256'],'width_mm':round(self.iw/mm,3),'height_mm':round(self.ih/mm,3),'vector':self.vector})

class Production(Chapter):
    def __init__(self,path):
        super().__init__(path);self.vectors=[];self.sign_records=[];self.cont=0;self.section='M03';self.group_pages={};self.scene_pages={};self.pending=False
    def start(self,*args,**kw):
        self.pending=False;super().start(*args,**kw)
    def end(self):
        if not self.pending:super().end()
        self.pending=True
    def ensure(self,flow,space=12):
        if self.pending:
            self.cont+=1;self.start(f'{self.section}-learning-{self.cont}',self.section+' · Continue')
            self.text('Continue the learning','subheading')
        if flow.wrap(WIDTH,1000)[1]+space>self.y-30*mm:
            self.end();self.cont+=1;self.start(f'{self.section}-continued-{self.cont}',self.section+' · Continued');self.text('Continue the learning','subheading')
        self.add(flow,space)
    def text(self,text,style='body',space=12):self.ensure(para(text,style),space)
    def art(self,key):
        flow=Scene(key);cap=para(ART[key]['caption'],'caption')
        if flow.height+cap.wrap(WIDTH,1000)[1]+25>self.y-30*mm:
            self.end();self.cont+=1;self.start(f'{self.section}-scene-{self.cont}',self.section+' · Illustration')
        self.scene_pages[key]=self.page;self.add(flow,7);self.text(ART[key]['caption'],'caption',18)
    def signs(self,group):
        gid=group['placement_id']
        title=GROUP_TITLES[int(gid[2:])-1];note=GROUP_NOTES[gid]
        needed=para(title,'subheading').wrap(WIDTH,1000)[1]+para(note,'caption').wrap(WIDTH,1000)[1]+SignCard(group['items'][0]['code'],self,gid).height+48
        if self.pending or needed>self.y-30*mm:
            self.end();self.start(gid,self.section+' · Official examples')
        else:
            self.c.bookmarkPage(gid);self.destinations[gid]=self.page
        self.group_pages[gid]=self.page
        self.text(title,'subheading');self.text(note,'caption',16)
        for item in group['items']:
            code=item['code']
            if gid=='LP006' and code in ['SIG12','SIG8']:
                label='Lane control' if code=='SIG12' else 'Public transport'
                if para(label,'subheading').wrap(WIDTH,1000)[1]+SignCard(code,self,gid).height+30>self.y-30*mm:
                    self.end();self.cont+=1;self.start(f'{self.section}-signals-{self.cont}',self.section+' · Official examples')
                self.text(label,'subheading')
            if gid=='LP005' and code=='SIG5':self.text('Separate condition: flashing amber','subheading')
            self.ensure(SignCard(code,self,gid),12)
        self.y-=10

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Production(OUT/'chapter.pdf');answers=[]
    b.start('M03','Chapter 3');b.text('CHAPTER 03','source');b.text('Read the road before acting','heading')
    b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24);b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    for key,title in [('M03-answers','Answers and review guidance'),('M03-references','Official references')]:b.add(Paragraph(f'<link href="#{key}" color="#173E32">{title}</link>',STYLES['body']),13)
    b.add(panel(re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1),'disclaimer'));b.end()
    for n in range(1,5):
        key=f'M03-L{n:02d}';b.section=key;s=SECTIONS[key];b.start(key,key);b.text(key,'source');b.text(s['title'],'heading');b.add(panel(s['paragraphs'][0]),18)
        for p in s['paragraphs'][1:]:
            if p.startswith('**Worked decision.'):
                b.end();b.start(key+'-scenario',key+' · Worked decision');b.text('Apply the learning','subheading');b.art(key)
                if n==3:b.art(key+'-follow')
            if p.startswith('|'):
                rows=[[v.strip() for v in line.strip('|').split('|')] for line in p.splitlines() if not line.startswith('|---')]
                b.ensure(reference_table(rows,[49*mm,53*mm,68*mm]),18)
            elif p.startswith('**Knowledge check.'):
                q,a=p.split(' **Answer:** ',1);answers.append((key,a))
                f=para(q)
                if f.wrap(WIDTH,1000)[1]+90>b.y-30*mm:
                    b.end();b.start(key+'-question',key+' · Knowledge check');b.text('Check your understanding','subheading')
                b.text(q);b.questions[key]=b.page;b.lines(3)
            else:b.text(p)
            for group in GROUPS:
                if group['location']['section_id']==key and group['location']['exact_quote']==p:
                    b.signs(group)
        b.end()
    b.section='M03-R';review=SECTIONS['M03-R']['paragraphs'];q,a=review[1].split(' **Review guide:** ',1)
    b.start('M03-R','M03-R · Self-assessment');b.text('Review and self-assessment','heading');b.art('M03-R-route');b.art('M03-R');b.text(review[0]);b.text(q);b.questions['M03-R']=b.page
    b.text('Use these earlier independent examples as references:','caption',6)
    for code,gid in [('F1-1','LP009'),('SIG3','LP005'),('T11','LP008')]:b.add(Paragraph(f'<link href="#{gid}" color="#173E32">{code} · {BINDINGS[code]["label_en"]}</link>',STYLES['caption']),5)
    b.group_pages['LP014']=b.page;b.end()
    b.start('M03-reflection','M03-R · Reflection');b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M03-answers','Answers and review guidance');b.text('Review after answering','heading')
    for key,ans in answers:b.text(key,'source',6);b.text('**Answer:** '+ans,space=20);b.answers[key]=b.page
    b.text('M03-R','source',6);b.text('**Review guide:** '+a);b.answers['M03-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M03-references' if offset==0 else 'M03-references-2';b.start(key,'Official references');b.text('Official references','heading')
        b.text('Chapter references checked 4 October 2026. Individual sign captions and artwork use the verified official asset register. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            b.text(LABELS[alias],'body',4);b.add(Paragraph(f'<link href="{escape(REFS[alias])}" color="#173E32">{escape(REFS[alias])}</link>',STYLES['source']),20)
        if offset==4:
            b.text('Road-sign illustrations: Transportstyrelsen. Each example links to its official description. Swedish names are official; English labels and explanations are editorial translations.','caption')
            b.text('Some outline examples are exact vector extracts from the official Swedish road-sign poster. They are retained at their reviewed size.','caption')
            url='https://www.transportstyrelsen.se/globalassets/global/publikationer-och-rapporter/vag/vagmarken/ts_poster70x100_2021-10-01_webb.pdf'
            b.add(Paragraph(f'<link href="{url}" color="#173E32">Transportstyrelsen · Sveriges vägmärken (official poster)</link>',STYLES['source']))
        b.end()
    b.c.save();r=PdfReader(OUT/'chapter.pdf');w=PdfWriter();w.clone_document_from_reader(r)
    from pypdf import Transformation
    from pypdf.generic import DecodedStreamObject
    for rec in b.vectors:
        vector=PdfReader(REPO/rec['path']).pages[0]
        # Poster vectors have no text painting. Remove unused font selections/resources
        # in this in-memory placement only; original official files remain unchanged.
        content=vector.get_contents()
        assert not any(op in (b'Tj',b'TJ',b'\"',b"'",b'Do') for _,op in content.operations)
        content.operations=[(args,op) for args,op in content.operations if op!=b'Tf']
        vector[NameObject('/Contents')]=content;vector['/Resources'].pop(NameObject('/Font'),None)
        stream=DecodedStreamObject()
        stream.set_data(('/Span << /ActualText <FEFF'+rec['alt'].encode('utf-16-be').hex()+'> >> BDC\n').encode()+vector.get_contents().get_data()+b'\nEMC')
        vector[NameObject('/Contents')]=stream
        scale=rec['width']/float(vector.mediabox.width)
        w.pages[rec['page']-1].merge_transformed_page(vector,Transformation().scale(scale).translate(rec['x'],rec['y']))
    w.root_object[NameObject('/Lang')]=TextStringObject('en-GB');w.root_object.pop(NameObject('/Outlines'),None)
    parent=w.add_outline_item('Chapter 3 · Read the road before acting',0);current=parent
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M03':continue
        if key in SECTIONS:current=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key.startswith('LP'):w.add_outline_item(GROUP_TITLES[int(key[2:])-1],num-1,parent=current)
        elif key in ['M03-answers','M03-references','M03-reflection']:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels,'group_pages':b.group_pages,'scene_pages':b.scene_pages},indent=2)+'\n')
    for key,v in ART.items():
        v['sha256']=hashlib.sha256((ROOT/'pdf-design/gap-resolution'/v['file']).read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops; screen review','assets':ART,'official_sign_placements':b.sign_records,'reference_cross_links':{'LP014':['LP009','LP005','LP008']}},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-03.pdf');print(f'Built {len(w.pages)} pages, {len(b.sign_records)} official placements')
if __name__=='__main__':run()
