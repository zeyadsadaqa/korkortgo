"""Step 6F: independently reproducible Chapter 5 review PDF."""
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
SOURCE='## 5. Make room in busy streets\n'+MANUSCRIPT.split('## 5. Make room in busy streets\n',1)[1].split('\n## 6. Travel beyond the town',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M05-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={'M05-L01': {'file': 'M05-v2.png',
             'box': [35, 198, 567, 825],
             'width_mm': 105,
             'caption': 'The bus signals to leave its stop. The full-width middle lane remains separate from '
                        'the opposing lane. In the worked decision the road limit is 40 km/h; available road '
                        'width does not remove the bus duty.'},
 'M05-L02': {'file': 'M05-v2.png',
             'box': [599, 198, 1128, 889],
             'width_mm': 100,
             'caption': 'At a pedestrian-street boundary, the official E7 sign identifies the street’s '
                        'purpose. Check whether your journey is permitted before entering; a navigation '
                        'shortcut is not an exemption.',
             'overlays': [{'code': 'E7', 'rect': [960, 198, 1128, 453]}]},
 'M05-L03-crossing': {'file': 'D03-v1.png',
                      'box': [310, 79, 1640, 330],
                      'width_mm': 170,
                      'caption': 'Travel is left to right. No stopping on the crossing or within 10 m before '
                                 'it. Shading shows the rule’s extent, not a braking distance; the drawing '
                                 'is not to scale.',
                      'overlays': [{'label': '10 m before', 'rect': [975, 183, 1165, 224]}]},
 'M05-L03-junction': {'file': 'D03-v1.png',
                      'box': [310, 350, 1640, 611],
                      'width_mm': 170,
                      'caption': 'Travel is left to right. No stopping in the junction or within 10 m of the '
                                 'nearest edge of the crossing carriageway. Distances run from the junction '
                                 'edges; this schematic is not to scale.',
                      'overlays': [{'label': '10 m', 'rect': [748, 442, 838, 490]},
                                   {'label': '10 m', 'rect': [1185, 442, 1277, 490]}]},
 'M05-L03-bus': {'file': 'D03-v1.png',
                 'box': [310, 631, 1640, 890],
                 'width_mm': 170,
                 'caption': 'Travel is left to right. With no marked stop extent, the restriction extends 20 '
                            'm before and 5 m after the stop sign. Other vehicles may stop only for boarding '
                            'or alighting without obstructing the service. Shading is explanatory, not a '
                            'road marking.',
                 'overlays': [{'code': 'E22', 'rect': [1097, 691, 1123, 724]},
                              {'label': 'Bus-stop sign', 'rect': [1031, 631, 1206, 673]},
                              {'label': '20 m before', 'rect': [771, 762, 953, 803]},
                              {'label': '5 m after', 'rect': [1135, 762, 1280, 803]}]},
 'M05-L04': {'file': 'parking-v3.png',
             'box': [100, 136, 719, 731],
             'width_mm': 130,
             'caption': 'Parking bays are above the footway; the access lane is below it. The white van can '
                        'hide a pedestrian from the reversing driver. No path is cleared or recommended by '
                        'this drawing.'},
 'M05-R-bus': {'file': 'M05-v2.png',
               'box': [1160, 168, 1635, 368],
               'width_mm': 170,
               'caption': 'Bus detail: identify the signal and the applicable road limit before explaining '
                          'your approach.'},
 'M05-R-cyclist': {'file': 'M05-v2.png',
                   'box': [1160, 376, 1635, 577],
                   'width_mm': 170,
                   'caption': 'Cyclist detail: observe the parked cars, opening door and space the rider may '
                              'need.'},
 'M05-R-crossing': {'file': 'M05-v2.png',
                    'box': [1160, 585, 1635, 762],
                    'width_mm': 170,
                    'caption': 'Crossing detail: assess the proposed collection point. The drawing provides '
                               'no measured clearance and does not label a lawful stopping place.'}}

def para(text,style='body'):
    safe=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(text))
    safe=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',safe)
    safe=re.sub(r'\[([^]]+)\]\[([^]]+)\]',lambda m:f'<link href="{escape(REFS[m[2]],{chr(34):"&quot;"})}" color="#173E32">{m[1]}</link>',safe)
    return Paragraph(safe,STYLES[style])

class Scene(Flowable):
    """Non-destructive image placement: clip the approved board at PDF render time."""
    def __init__(self,key,frame_width=WIDTH):
        Flowable.__init__(self);self.rec=ART[key];self.width=self.rec.get('width_mm',170)*mm;self.frame_width=frame_width
        l,t,r,b=self.rec['box'];self.height=self.width*(b-t)/(r-l)
    def draw(self):
        rec=self.rec;c=self.canv;l,t,r,b=rec['box'];p=ROOT/'pdf-design/gap-resolution'/rec['file']
        iw,ih=Image.open(p).size;s=self.width/(r-l)
        c.saveState();c.translate((self.frame_width-self.width)/2,0);c._code.append('/Span << /ActualText <FEFF'+rec['caption'].encode('utf-16-be').hex() + '> >> BDC');path=c.beginPath();
        if 'polygon' in rec:
            points=rec['polygon'];path.moveTo((points[0][0]-l)*s,(b-points[0][1])*s)
            for px,py in points[1:]:path.lineTo((px-l)*s,(b-py)*s)
            path.close()
        else:path.rect(0,0,self.width,self.height)
        c.clipPath(path,stroke=0)
        c.drawImage(str(p),-l*s,-(ih-b)*s,iw*s,ih*s)
        # Native PDF template inserts exact official artwork over reserved sign faces.
        # The approved raster files remain unchanged.
        for overlay in rec.get('overlays',[]):
            x1,y1,x2,y2=overlay['rect'];xx=(x1-l)*s;yy=(b-y2)*s;ww=(x2-x1)*s;hh=(y2-y1)*s
            c.setFillColor(HexColor('#FFFFFF'));c.rect(xx,yy,ww,hh,fill=1,stroke=0)
            if 'code' in overlay:
                asset=BINDINGS[overlay['code']]['preferred_asset'];path=REPO/asset['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256']
                sw,sh=Image.open(path).size;scale=min((ww-2)/sw,(hh-2)/sh)
                c.drawImage(str(path),xx+(ww-sw*scale)/2,yy+(hh-sh*scale)/2,sw*scale,sh*scale,mask='auto')
            else:
                style=ParagraphStyle('diagram',parent=STYLES['source'],fontSize=9.5,leading=13,alignment=1);f=Paragraph(escape(overlay['label']),style);_,fh=f.wrap(ww,hh);assert fh<=hh+.5;f.drawOn(c,xx,yy+(hh-fh)/2)
        c._code.append('EMC');c.restoreState()

class Chapter(BookCanvas):
    def __init__(self,path):
        super().__init__(path);self.questions={};self.answers={};self.page_labels={}
        self.c.setTitle('KörkortGo | Chapter 5 | Make room in busy streets')
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
GROUPS=[p for p in PLACEMENT['lesson_placements'] if p['location']['section_id'].startswith('M05')]
BINDINGS={b['code']:b for b in PLACEMENT['asset_caption_bindings']}
CAPTIONS={c['code']:c for c in json.loads((ROOT/'sign-captions.json').read_text())['captions']}
GROUP_TITLES={'LP023': 'Observe people and possible movement', 'LP024': 'Horses and riders', 'LP025': 'Recognise a bus stop and speed limit', 'LP026': 'Pedestrian streets and walking-speed areas', 'LP027': 'Cycle streets', 'LP028': 'Check access before choosing a route', 'LP029': 'Stopping or parking restrictions', 'LP030': 'Bus-stop extent', 'LP031': 'Read each parking condition', 'LP032': 'The worked example’s components', 'LP033': 'Other parking instructions', 'LP034': 'Marked spaces and parking arrangements'}
GROUP_NOTES={'LP023': 'Children, cyclists and riders have different needs. Sensory-impairment panels are separate examples; absence of a sign does not prove absence of risk.', 'LP024': 'This warning supports early observation. It does not specify a fixed passing distance.', 'LP025': 'The bus-stop marker and the 40 km/h speed sign are independent examples. The bus marker itself does not set the speed limit.', 'LP026': 'Two matched start/end pairs. Pedestrian-street access limits differ from walking-speed-area rules.', 'LP027': 'Matched beginning and ending signs. Retain the entry and exit yielding duties in the lesson.', 'LP028': 'Independent examples of access prohibitions, paths, reserved lanes and no-through roads. These are not all installed at the illustrated pedestrian street.', 'LP029': 'Compare no parking with no stopping and parking. An extent marking needs its actual accompanying restriction; it does not create permission.', 'LP030': 'The marked extent and the unmarked 20 m/5 m case are different situations. The later illustration shows the unmarked case.', 'LP031': 'Individual reference panels, not one sign assembly. T6 and T17 contain sample times that differ from the 09–18 worked example. Do not transfer their conditions to that exercise.', 'LP032': 'E19 and the two-hour T18 are shown separately here. The following exercise uses the illustrative assembly with 2 tim and black 9–18 on one plate.', 'LP033': 'Keep starts and ends paired by type. C45’s 8–18 and E30’s 30-minute conditions are separate examples, not the Tuesday two-hour exercise.', 'LP034': 'Each positioning panel is a separate arrangement. The marked-space boundary does not establish that a reversing path is safe.'}

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
        super().__init__(path);self.vectors=[];self.sign_records=[];self.cont=0;self.section='M05';self.group_pages={};self.scene_pages={};self.pending=False;self.native_diagrams=[]
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
        title=GROUP_TITLES[gid];note=GROUP_NOTES[gid]
        needed=para(title,'subheading').wrap(WIDTH,1000)[1]+para(note,'caption').wrap(WIDTH,1000)[1]+SignCard(group['items'][0]['code'],self,gid).height+48
        if self.pending or needed>self.y-30*mm:
            self.end();self.start(gid,self.section+' · Official examples')
        else:
            self.c.bookmarkPage(gid);self.destinations[gid]=self.page
        self.group_pages[gid]=self.page
        self.text(title,'subheading');self.text(note,'caption',16)
        for item in group['items']:
            code=item['code']
            headings={('LP023','T9'):'Sensory-impairment panels',('LP026','E7'):'Pedestrian street',('LP026','E9'):'Walking-speed area',('LP028','C1'):'Access prohibitions',('LP028','D4'):'Paths and reserved lanes',('LP028','E17'):'No-through roads',('LP033','C36'):'Date-based parking restrictions',('LP033','C40'):'Reserved purposes and places',('LP033','E20'):'Zone and combined instructions'}
            if (gid,code) in headings:
                label=headings[(gid,code)]
                if para(label,'subheading').wrap(WIDTH,1000)[1]+SignCard(code,self,gid).height+30>self.y-30*mm:
                    self.end();self.cont+=1;self.start(f'{self.section}-set-{self.cont}',self.section+' · Official examples')
                self.text(label,'subheading')
            self.ensure(SignCard(code,self,gid),12)
        self.y-=10

class Pair(Flowable):
    """Two independent approved scenes with selectable captions and a clear gutter."""
    def __init__(self,keys):
        super().__init__();self.keys=keys;self.width=WIDTH;self.cw=80*mm
        self.scenes=[Scene(k,self.cw) for k in keys];self.caps=[para(ART[k]['caption'],'caption') for k in keys]
        self.height=max(sc.height+8+cap.wrap(self.cw,1000)[1] for sc,cap in zip(self.scenes,self.caps))+12
    def draw(self):
        for j,(scene,cap) in enumerate(zip(self.scenes,self.caps)):
            x=j*90*mm;top=self.height-12;scene.drawOn(self.canv,x,top-scene.height)
            _,h=cap.wrap(self.cw,1000);cap.drawOn(self.canv,x,top-scene.height-8-h)

def scene_page(b,key,title,keys):
    b.end();b.start(key,b.section+' · Illustration');b.text(title,'subheading')
    if len(keys)==2:
        b.add(Pair(keys),18)
        for k in keys:b.scene_pages[k]=b.page
    else:b.art(keys[0])

class ParkingConditions(Flowable):
    """Exact official E19 plus the approved illustrative condition plate."""
    def __init__(self,b):
        super().__init__();self.book=b;self.width=WIDTH;self.height=83*mm
    def draw(self):
        c=self.canv;asset=BINDINGS['E19']['preferred_asset'];path=REPO/asset['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256']
        size=45*mm;top=self.height
        c._code.append('/Span << /ActualText <FEFF'+ 'Illustrative sign combination: official E19 parking sign above one plate with black 2 tim and 9–18. No disc or fee condition is shown.'.encode('utf-16-be').hex()+'> >> BDC')
        c.drawImage(str(path),0,top-size,size,size,mask='auto')
        c.setFillColor(HexColor('#FFFFFF'));c.setStrokeColor(HexColor('#000000'));c.setLineWidth(1.8)
        c.roundRect(0,top-size-25*mm,size,24*mm,2*mm,stroke=1,fill=1)
        c.setFillColor(HexColor('#000000'));c.setFont('BodyBold',23)
        c.drawCentredString(size/2,top-size-10*mm,'2 tim');c.drawCentredString(size/2,top-size-20*mm,'9–18');c._code.append('EMC')
        f=para('Illustrative sign combination','source');_,h=f.wrap(50*mm,1000);f.drawOn(c,0,top-size-28*mm-h)
        texts=['Ordinary Tuesday, not a holiday or the day before one.','In this example, parking is limited to two hours during 09–18.','Arrival: 10:00.']
        y=top
        for text in texts:
            f=para(text);_,h=f.wrap(110*mm,1000);f.drawOn(c,60*mm,y-h);y-=h+18
        self.book.native_diagrams.append({'kind':'parking_conditions','page':self.book.page,'official_code':'E19','asset':asset,'width_mm':45,'plate_text':['2 tim','9–18'],'plate_status':'illustrative typeset condition plate, not archived T6 artwork'})

class Timeline(Flowable):
    def __init__(self):super().__init__();self.width=WIDTH;self.height=44*mm
    def draw(self):
        c=self.canv;c.setFillColor(COLORS['sage']);c.rect(0,0,WIDTH,self.height,fill=1,stroke=0)
        c.setStrokeColor(COLORS['forest']);c.setFillColor(COLORS['forest']);c.setLineWidth(2)
        xs=[12*mm,48*mm,108*mm,158*mm];y=20*mm;c.line(xs[0],y,xs[-1],y)
        c.setFont('Body',12)
        for x,label in zip(xs,['09:00','10:00','12:00','18:00']):
            c.line(x,y-4*mm,x,y+4*mm);c.drawCentredString(x,y-10*mm,label)
        c.setLineWidth(1);c.line(xs[1],y+8*mm,xs[2],y+8*mm)
        c.line(xs[1],y+6*mm,xs[1],y+8*mm);c.line(xs[2],y+6*mm,xs[2],y+8*mm)
        c.setFont('BodyBold',12);c.drawCentredString((xs[1]+xs[2])/2,y+12*mm,'Two hours')

def parking_example(b,answer):
    b.text('Read the time conditions','heading');b.text('Worked example' if answer else 'Try it first','subheading')
    b.add(ParkingConditions(b),20)
    if answer:
        b.text('Schematic timeline - not to scale','subheading');b.add(Timeline(),18)
        b.add(panel('**The two-hour limit is reached at 12:00.**','disclaimer'),18)
        b.text('Check all other conditions before leaving the car.')
    else:
        b.text('When is the two-hour limit reached, and what else must you check?','subheading');b.lines(5)
        b.add(Paragraph('<link href="#D06-answer" color="#173E32">Read the worked example after answering.</link>',STYLES['caption']))
    b.text('[Time-panel meaning][sign-law] · Official E19 artwork with an illustrative condition plate.','source')

def lesson_body(b,n):
    key=f'M05-L{n:02d}';s=SECTIONS[key];paras=s['paragraphs'];b.section=key
    b.start(key,key);b.text(key,'source');b.text(s['title'],'heading');b.add(panel(paras[0]),18)
    worked=next(p for p in paras if p.startswith('**Worked decision.'))
    for p in paras[1:paras.index(worked)]:
        if p.startswith('|'):
            rows=[[para(v.strip(),'caption') for v in line.strip('|').split('|')] for line in p.splitlines() if not line.startswith('|---')]
            table=Table(rows,colWidths=[62*mm,108*mm],repeatRows=1)
            table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,0),COLORS['sage']),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]));b.ensure(table,18)
        else:b.text(p)
        for group in GROUPS:
            if group['location']['section_id']==key and group['location']['exact_quote']==p:b.signs(group)
    if n==1:
        scene_page(b,key+'-scenario','Leave room for the bus and people',[key]);b.text(worked)
    elif n==2:
        scene_page(b,key+'-scenario','Check before entering',[key]);b.text(worked)
    elif n==3:
        scene_page(b,key+'-scenario','Read the extent of the restriction',['M05-L03-crossing']);b.art('M05-L03-junction');b.art('M05-L03-bus')
        b.text(worked)
    else:
        scene_page(b,key+'-scenario','Observe behind the parked vehicles',[key]);b.text(worked)
    for group in GROUPS:
        if group['location']['section_id']==key and group['location']['exact_quote']==worked:b.signs(group)
    if n==3:
        b.end();b.start('D06-question','M05-L03 · Parking-time exercise');parking_example(b,False);b.questions['D06']=b.page;b.end()
    check=next(p for p in paras if p.startswith('**Knowledge check.'));q,a=check.split(' **Answer:** ',1)
    b.end();b.start(key+'-question',key+' · Knowledge check');b.text('Check your understanding','heading');b.text(q);b.questions[key]=b.page;b.lines(8);b.text(paras[-1],'caption');b.end()
    return key,a

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Production(OUT/'chapter.pdf');answers=[]
    b.start('M05','Chapter 5');b.text('CHAPTER 05','source');b.text('Make room in busy streets','heading');b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24);b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    for key,title in [('M05-answers','Answers and review guidance'),('M05-references','Official references')]:b.add(Paragraph(f'<link href="#{key}" color="#173E32">{title}</link>',STYLES['body']),13)
    b.add(panel(re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1),'disclaimer'));b.end()
    for n in range(1,5):answers.append(lesson_body(b,n))
    b.section='M05-R';review=SECTIONS['M05-R']['paragraphs'];q,a=review[1].split(' **Review guide:** ',1)
    b.start('M05-R','M05-R · Self-assessment');b.text('Review and self-assessment','heading');b.text(review[0]);b.art('M05-R-bus');b.art('M05-R-cyclist');b.end()
    b.start('M05-R-crossing','M05-R · Collection point');b.text('Choose a lawful collection point','subheading');b.art('M05-R-crossing');b.text(q);b.questions['M05-R']=b.page;b.lines(6);b.end()
    b.start('M05-reflection','M05-R · Reflection');b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M05-answers','Answers and review guidance');b.text('Review after answering','heading')
    for key,ans in answers:b.text(key,'source',6);b.text('**Answer:** '+ans,space=20);b.answers[key]=b.page
    b.text('M05-R','source',6);b.text('**Review guide:** '+a);b.answers['M05-R']=b.page;b.end()
    b.start('D06-answer','M05-L03 · Parking-time review');parking_example(b,True);b.answers['D06']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M05-references' if offset==0 else 'M05-references-2';b.start(key,'Official references');b.text('Official references','heading')
        b.text('Chapter references checked 5 October 2026. Individual sign captions and artwork use the verified official asset register. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            b.text(LABELS[alias],'body',4);b.add(Paragraph(f'<link href="{escape(REFS[alias])}" color="#173E32">{escape(REFS[alias])}</link>',STYLES['source']),20)
        if offset==4:b.text('Road-sign illustrations: Transportstyrelsen. Each reference example links to its official description. Swedish names are official; English labels and explanations are editorial translations. Road scenes are simplified illustrations, not to scale.','caption')
        if offset==4:
            b.text('T6 and T8 use exact vector extracts from the official Swedish road-sign poster, retained at their reviewed size.','caption')
            b.add(Paragraph('<link href="https://www.transportstyrelsen.se/globalassets/global/publikationer-och-rapporter/vag/vagmarken/ts_poster70x100_2021-10-01_webb.pdf" color="#173E32">Transportstyrelsen · Sveriges vägmärken (official poster)</link>',STYLES['source']))
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
    parent=w.add_outline_item('Chapter 5 · Make room in busy streets',0);current=parent
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M05':continue
        if key in SECTIONS:current=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key.startswith('LP'):w.add_outline_item(GROUP_TITLES[key],num-1,parent=current)
        elif key in ['M05-answers','M05-references','M05-reflection']:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
        elif key in ['D06-question','D06-answer','M05-R-crossing'] or any(key.endswith(suf) for suf in ['-compare','-priority','-stop','-join','-scenario','-entry','-exit','-question']):w.add_outline_item(b.page_labels[num],num-1,parent=current)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels,'group_pages':b.group_pages,'scene_pages':b.scene_pages},indent=2)+'\n')
    for key,v in ART.items():
        v['sha256']=hashlib.sha256((ROOT/'pdf-design/gap-resolution'/v['file']).read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
        for o in v.get('overlays',[]):
            if 'code' in o:o['asset']=BINDINGS[o['code']]['preferred_asset'];o['official_url']=BINDINGS[o['code']]['official_url']
    b.native_diagrams.append({'kind':'approved_design','file':'timeline-v4.png','sha256':hashlib.sha256((ROOT/'pdf-design/gap-resolution/timeline-v4.png').read_bytes()).hexdigest()})
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops and exact official sign insertions; screen review','assets':ART,'official_sign_placements':b.sign_records,'reference_cross_links':{},'native_diagrams':b.native_diagrams},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-05.pdf');print(f'Built {len(w.pages)} pages, {len(b.sign_records)} official reference placements and {len(ART)} scenes')
if __name__=='__main__':run()
