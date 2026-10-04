"""Step 6E: independently reproducible Chapter 4 review PDF."""
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
SOURCE='## 4. Negotiate shared space\n'+MANUSCRIPT.split('## 4. Negotiate shared space\n',1)[1].split('\n## 5. Make room in busy streets',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M04-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={'M04-L01': {'box': [621, 210, 1140, 880],
             'caption': 'Driveway exit: the teal car is entering across the footway. Identify the exit duty '
                        'before choosing a gap.',
             'file': 'D01-v2.png',
             'width_mm': 80},
 'M04-L01-ordinary': {'box': [34, 210, 599, 880],
                      'caption': 'Ordinary junction: no signs, signals or special rule apply. The yellow car '
                                 'approaches from the teal driver’s right. Road width alone does not determine '
                                 'priority.',
                      'file': 'D01-v2.png',
                      'width_mm': 80},
 'M04-L01-priority': {'box': [34, 144, 1637, 880],
                      'caption': 'Driving on a priority road: B4 is after the junction on the right verge. B1 '
                                 'controls the side-road approach. Continue observing; priority does not make a '
                                 'collision acceptable.',
                      'file': 'D01-priority-v3.png',
                      'overlays': [{'code': 'B4', 'rect': [902, 143, 979, 215]},
                                   {'code': 'B1', 'rect': [997, 216, 1073, 280]},
                                   {'label': 'B4', 'rect': [984, 159, 1209, 210]}],
                      'width_mm': 170},
 'M04-L01-stop': {'box': [1163, 210, 1640, 880],
                  'caption': 'Stop duty: the teal car approaches the stop line. A complete stop is required at '
                             'the line. This detail shows the stopping point, not the whole junction.',
                  'file': 'D01-v2.png',
                  'overlays': [{'code': 'B2', 'rect': [1548, 387, 1625, 457]}],
                  'width_mm': 80},
 'M04-L02': {'box': [465, 660, 1638, 891],
             'caption': 'Right turn beside a cyclist: the cycling route and receiving road remain open. Check the '
                        'cyclist’s movement before crossing the route. No movement arrow grants priority.',
             'file': 'D04-v3.png',
             'width_mm': 170},
 'M04-L02-join': {'box': [1091, 153, 1638, 633],
                  'caption': 'Acceleration-lane join: a distinct joining lane meets the through lane. Adapt speed '
                             'and join safely; do not force a gap.',
                  'file': 'D04-v3.png',
                  'width_mm': 80},
 'M04-L02-lane': {'box': [34, 153, 578, 633],
                  'caption': 'Lane change: two marked lanes continue. A signal communicates an intention; check '
                             'for a safe opportunity before moving sideways.',
                  'file': 'D04-v3.png',
                  'width_mm': 80},
 'M04-L02-merge': {'box': [603, 153, 1068, 633],
                   'caption': 'Mutual merge: two lanes narrow into one. Both drivers adapt with mutual '
                              'consideration.',
                   'file': 'D04-v3.png',
                   'width_mm': 80},
 'M04-L03': {'box': [1225, 143, 1637, 740],
             'caption': 'Passage after a roundabout exit: the cyclist is approaching the marked passage on the '
                        'receiving road. The exit movement matters to the driver’s duty.',
             'file': 'D02-v4.png',
             'width_mm': 80},
 'M04-L03-crossing': {'box': [842, 143, 1210, 740],
                      'caption': 'Cycle crossing: B8, the crossing markings and the raised treatment distinguish '
                                 'this example. Surface colour alone does not determine the duty.',
                      'file': 'D02-v4.png',
                      'overlays': [{'code': 'B8', 'rect': [1098, 528, 1210, 740]}],
                      'width_mm': 80},
 'M04-L03-passage': {'box': [439, 143, 826, 740],
                     'caption': 'Uncontrolled cycle passage approached without turning: M16 blocks mark the '
                                'passage. There is no B8 cycle-crossing sign in this example.',
                     'file': 'D02-v4.png',
                     'overlays': [{'code': 'M16', 'rect': [714, 528, 826, 740]}],
                     'width_mm': 80},
 'M04-L03-pedestrian': {'box': [34, 143, 425, 740],
                        'caption': 'Uncontrolled pedestrian crossing: a person is about to enter. The B3 sign and '
                                   'zebra marking identify this separate example.',
                        'file': 'D02-v4.png',
                        'overlays': [{'code': 'B3', 'rect': [313, 528, 424, 740]}],
                        'width_mm': 80},
 'M04-L04': {'box': [559, 176, 1108, 870],
             'caption': 'Circulation: two lanes surround the island. The teal car in the inner lane and yellow '
                        'car in the outer lane need separate space; the inner lane confers no exit priority.',
             'file': 'D05-v3.png',
             'width_mm': 80},
 'M04-L04-entry': {'box': [26, 176, 541, 870],
                   'caption': 'Approach: B1 and D3 identify the entry instructions. The teal car approaches the '
                              'yield point while the yellow car circulates anticlockwise.',
                   'file': 'D05-v3.png',
                   'overlays': [{'code': 'B1', 'rect': [379, 589, 427, 630]},
                                {'code': 'D3', 'rect': [380, 630, 427, 675]}],
                   'width_mm': 80},
 'M04-L04-exit': {'box': [1127, 176, 1644, 870],
                  'caption': 'Exit: the teal car approaches a cycle passage. Signal right when leaving and check '
                             'the passage as a separate conflict.',
                  'file': 'D05-v3.png',
                  'width_mm': 80},
 'M04-R-crossing': {'box': [845, 168, 1240, 641],
                    'caption': '3. Approaching a raised cycle crossing. Read the official B8 sign and the '
                               'markings before explaining the duty.',
                    'file': 'M04R-v3.png',
                    'overlays': [{'code': 'B8', 'rect': [1198, 484, 1238, 516]}],
                    'width_mm': 80},
 'M04-R-entry': {'box': [1256, 165, 1649, 641],
                 'caption': '4. Entry detail. This companion image shows a single-lane entry; use the separate '
                            'two-lane view for the written scenario’s lane decisions.',
                 'file': 'M04R-v3.png',
                 'width_mm': 80},
 'M04-R-exit': {'box': [22, 165, 426, 641],
                'caption': '1. Leaving a car park. Describe the duty and the observations needed before entering '
                           'the road.',
                'file': 'M04R-v3.png',
                'width_mm': 80},
 'M04-R-turn': {'box': [444, 168, 825, 641],
                'caption': '2. Preparing a left turn on a two-way road. Identify the vehicles and paths you need '
                           'to observe.',
                'file': 'M04R-v3.png',
                'width_mm': 80},
 'M04-R-two-lane': {'box': [559, 176, 1108, 870],
                    'caption': 'Two-lane companion view for the written scenario. Identify nearby vehicles and '
                               'explain how you would plan a lane change and exit. No route is selected.',
                    'file': 'D05-v3.png',
                    'width_mm': 95}}

def para(text,style='body'):
    safe=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(text))
    safe=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',safe)
    safe=re.sub(r'\[([^]]+)\]\[([^]]+)\]',lambda m:f'<link href="{escape(REFS[m[2]],{chr(34):"&quot;"})}" color="#173E32">{m[1]}</link>',safe)
    safe=safe.replace('M04-L03 still apply','<link href="#M04-L03" color="#173E32">M04-L03</link> still apply')
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
                f=para(overlay['label'],'source');_,fh=f.wrap(ww-4,hh);f.drawOn(c,xx+2,yy+(hh-fh)/2)
        c._code.append('EMC');c.restoreState()

class Chapter(BookCanvas):
    def __init__(self,path):
        super().__init__(path);self.questions={};self.answers={};self.page_labels={}
        self.c.setTitle('KörkortGo | Chapter 4 | Negotiate shared space')
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
GROUPS=[p for p in PLACEMENT['lesson_placements'] if p['location']['section_id'].startswith('M04')]
BINDINGS={b['code']:b for b in PLACEMENT['asset_caption_bindings']}
CAPTIONS={c['code']:c for c in json.loads((ROOT/'sign-captions.json').read_text())['captions']}
GROUP_TITLES={'LP015': 'Priority and junction instructions', 'LP016': 'Yielding and stopping', 'LP017': 'Choose a permitted direction', 'LP018': 'Changing and merging lanes', 'LP019': 'Recognise a pedestrian crossing', 'LP020': 'Identify a cycle crossing', 'LP021': 'Signals and crossing duties', 'LP022': 'Roundabout instructions'}
GROUP_NOTES={'LP015': 'Independent examples: A29 variants show different branch layouts. Read thick and thin roads on each T15 panel; do not assume an approach orientation.', 'LP016': 'Signs and markings are labelled counterparts. The separate stopping-point illustration shows how the line relates to the car.', 'LP017': 'Prohibitions, mandatory directions, one-way signs and lane arrows are separate sets. They are not all present at one fictional junction.', 'LP018': 'Compare merging, lane increase, lane reduction and a lane-change arrow. Establish the actual road layout before deciding how to move.', 'LP019': 'The warning identifies an approach. B3 and M15 identify the crossing itself; the mirrored B3 artwork does not change the duty.', 'LP020': 'Separately labelled components. M16 alone does not establish a cycle crossing; read the sign, markings and road design together.', 'LP021': 'Pedestrian indications and vehicle indications control different users. Printed pictures do not reproduce audible signals or guarantee conflict-free movement.', 'LP022': 'Approach warning, circulation direction, yielding, lane guidance and island marker are distinct instructions. Read the actual combination on the road.'}

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
        super().__init__(path);self.vectors=[];self.sign_records=[];self.cont=0;self.section='M04';self.group_pages={};self.scene_pages={};self.pending=False
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
            headings={('LP017','C25'):'Prohibited movements',('LP017','D1'):'Mandatory directions',('LP017','E16'):'One-way road',('LP017','M19'):'Lane arrows',('LP021','SIG6'):'Pedestrian signals',('LP021','SIG1'):'Vehicle signals'}
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

def lesson_body(b,n):
    key=f'M04-L{n:02d}';s=SECTIONS[key];paras=s['paragraphs'];b.section=key
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
        scene_page(b,key+'-compare','Ordinary junction or exit?', ['M04-L01-ordinary',key]);b.text(worked)
        scene_page(b,key+'-priority','Driving on a priority road',['M04-L01-priority'])
        scene_page(b,key+'-stop','Where a stop is required',['M04-L01-stop'])
    elif n==2:
        scene_page(b,key+'-compare','Changing lane or merging?', ['M04-L02-lane','M04-L02-merge'])
        scene_page(b,key+'-join','Joining from an acceleration lane',['M04-L02-join'])
        b.text('This companion scene shows a distinct acceleration lane. Adapt speed to the traffic in the lane you intend to join and leave the acceleration lane as soon as this can be done without danger or unnecessary obstruction. [Traffic Regulation, chapter 3 §23][traffic-law]')
        scene_page(b,key+'-scenario','Observe the complete turn',[key]);b.text(worked)
    elif n==3:
        scene_page(b,key+'-compare','Two different crossing situations',['M04-L03-pedestrian','M04-L03-passage'])
        b.text('The official artwork in each white reference card identifies the illustrated control or marking; it is not a new roadside sign assembly.','caption')
        scene_page(b,key+'-scenario','Identify the crossing and your movement',['M04-L03-crossing',key]);b.text(worked)
    else:
        scene_page(b,key+'-entry','Entry and circulation are separate decisions',['M04-L04-entry',key]);b.text(worked)
        scene_page(b,key+'-exit','Check the receiving road',['M04-L04-exit'])
    check=next(p for p in paras if p.startswith('**Knowledge check.'));q,a=check.split(' **Answer:** ',1)
    b.end();b.start(key+'-question',key+' · Knowledge check');b.text('Check your understanding','heading');b.text(q);b.questions[key]=b.page;b.lines(8);b.text(paras[-1],'caption');b.end()
    return key,a

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Production(OUT/'chapter.pdf');answers=[]
    b.start('M04','Chapter 4');b.text('CHAPTER 04','source');b.text('Negotiate shared space','heading');b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24);b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    for key,title in [('M04-answers','Answers and review guidance'),('M04-references','Official references')]:b.add(Paragraph(f'<link href="#{key}" color="#173E32">{title}</link>',STYLES['body']),13)
    b.add(panel(re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1),'disclaimer'));b.end()
    for n in range(1,5):answers.append(lesson_body(b,n))
    b.section='M04-R';review=SECTIONS['M04-R']['paragraphs'];q,a=review[1].split(' **Review guide:** ',1)
    b.start('M04-R','M04-R · Self-assessment');b.text('Review and self-assessment','heading');b.text(review[0]);b.add(Pair(['M04-R-exit','M04-R-turn']),18)
    for k in ['M04-R-exit','M04-R-turn']:b.scene_pages[k]=b.page
    b.text(q);b.end()
    b.start('M04-R-crossings','M04-R · Continue');b.text('Crossing and entry details','subheading');b.add(Pair(['M04-R-crossing','M04-R-entry']),18)
    for k in ['M04-R-crossing','M04-R-entry']:b.scene_pages[k]=b.page
    b.text('Use the two-lane companion view on the next page for the final part of the written scenario.','caption');b.end()
    b.start('M04-R-two-lanes','M04-R · Two-lane companion');b.text('Plan the two-lane section','subheading');b.art('M04-R-two-lane');b.text(q);b.questions['M04-R']=b.page;b.lines(3);b.end()
    b.start('M04-reflection','M04-R · Reflection');b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M04-answers','Answers and review guidance');b.text('Review after answering','heading')
    for key,ans in answers:b.text(key,'source',6);b.text('**Answer:** '+ans,space=20);b.answers[key]=b.page
    b.text('M04-R','source',6);b.text('**Review guide:** '+a);b.answers['M04-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M04-references' if offset==0 else 'M04-references-2';b.start(key,'Official references');b.text('Official references','heading')
        b.text('Chapter references checked 4 October 2026. Individual sign captions and artwork use the verified official asset register. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            b.text(LABELS[alias],'body',4);b.add(Paragraph(f'<link href="{escape(REFS[alias])}" color="#173E32">{escape(REFS[alias])}</link>',STYLES['source']),20)
        if offset==4:b.text('Road-sign illustrations: Transportstyrelsen. Each reference example links to its official description. Swedish names are official; English labels and explanations are editorial translations. Road scenes are simplified illustrations, not to scale.','caption')
        b.end()
    b.c.save();r=PdfReader(OUT/'chapter.pdf');w=PdfWriter();w.clone_document_from_reader(r)
    assert not b.vectors,'M04 currently uses only verified raster sign assets'
    w.root_object[NameObject('/Lang')]=TextStringObject('en-GB');w.root_object.pop(NameObject('/Outlines'),None)
    parent=w.add_outline_item('Chapter 4 · Negotiate shared space',0);current=parent
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M04':continue
        if key in SECTIONS:current=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key.startswith('LP'):w.add_outline_item(GROUP_TITLES[key],num-1,parent=current)
        elif key in ['M04-answers','M04-references','M04-reflection']:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
        elif key in ['M04-R-crossings','M04-R-two-lanes'] or any(key.endswith(suf) for suf in ['-compare','-priority','-stop','-join','-scenario','-entry','-exit','-question']):w.add_outline_item(b.page_labels[num],num-1,parent=current)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels,'group_pages':b.group_pages,'scene_pages':b.scene_pages},indent=2)+'\n')
    for key,v in ART.items():
        v['sha256']=hashlib.sha256((ROOT/'pdf-design/gap-resolution'/v['file']).read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
        for o in v.get('overlays',[]):
            if 'code' in o:o['asset']=BINDINGS[o['code']]['preferred_asset'];o['official_url']=BINDINGS[o['code']]['official_url']
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops and exact official sign insertions; screen review','assets':ART,'official_sign_placements':b.sign_records,'reference_cross_links':{},'review_preview_reconciliation':'Single-lane M04R entry is labelled as a companion detail; approved D05 two-lane view supports the unchanged manuscript scenario.'},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-04.pdf');print(f'Built {len(w.pages)} pages, {len(b.sign_records)} official reference placements and {len(ART)} scenes')
if __name__=='__main__':run()
