"""Step 6G: independently reproducible Chapter 6 review PDF."""
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
SOURCE='## 6. Travel beyond the town\n'+MANUSCRIPT.split('## 6. Travel beyond the town\n',1)[1].split('\n## 7. Adapt when conditions change',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M06-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={'M06-L01': {'file': 'M06-v1.png',
             'box': [30, 160, 569, 506],
             'width_mm': 170,
             'caption': 'Narrow bridge: the obstruction is on the teal driver’s right and the van approaches '
                        'in its own lane. Reduce speed before the narrowing and stop if necessary. The scene '
                        'does not measure a safe lateral gap.'},
 'M06-L02': {'file': 'M06-v1.png',
             'box': [588, 160, 1045, 506],
             'width_mm': 150,
             'caption': 'Following a slower vehicle towards a hidden bend. The visible straight does not '
                        'establish a complete pass and return path. The depicted spacing is illustrative, '
                        'not a recommended following distance.'},
 'M06-L03-entry': {'file': 'M06-v1.png',
                   'box': [1069, 141, 1419, 505],
                   'width_mm': 80,
                   'caption': 'Acceleration-lane detail: the teal car approaches traffic already on the main '
                              'carriageway. Judge speed and a safe joining opportunity; this still image '
                              'does not guarantee a usable gap.'},
 'M06-L03-exit': {'file': 'M06-v1.png',
                  'box': [1428, 140, 1641, 505],
                  'width_mm': 80,
                  'caption': 'Exit detail: plan the receiving lane early. If the necessary move cannot be '
                             'made safely, continue to a permitted exit and re-plan; never reverse to '
                             'recover the route.'},
 'M06-L04-rail': {'file': 'M06-v1.png',
                  'box': [30, 604, 562, 894],
                  'width_mm': 170,
                  'caption': 'Railway-crossing detail: the tracks are unoccupied but traffic is queued '
                             'beyond them. Check that the whole vehicle can clear the railway before '
                             'entering. The crop does not depict every sign, signal or barrier.'},
 'M06-L04-works': {'file': 'M06-v1.png',
                   'box': [574, 604, 860, 893],
                   'width_mm': 105,
                   'caption': 'Roadworks detail: machinery and cones alter the usable road edge. The scene '
                              'illustrates observation and space, not a complete approved traffic-management '
                              'layout. Follow the actual signs, signals and authorised directions.'},
 'M06-R-meeting': {'file': 'M06-v1.png',
                   'box': [886, 587, 1251, 723],
                   'width_mm': 80,
                   'caption': 'Rural meeting detail: identify the visible road space and what an approaching '
                              'vehicle changes.'},
 'M06-R-bend': {'file': 'M06-v1.png',
                'box': [1262, 587, 1640, 724],
                'width_mm': 80,
                'caption': 'Hidden-road detail: identify what remains out of view beyond the bend.'},
 'M06-R-junction': {'file': 'M06-v1.png',
                    'box': [886, 730, 1251, 892],
                    'width_mm': 80,
                    'caption': 'Ordinary rural-junction detail: assess possible joining traffic. This is '
                               'separate from the motorway-entry detail shown later.'},
 'M06-R-rail': {'file': 'M06-v1.png',
                'box': [1262, 730, 1640, 893],
                'width_mm': 80,
                'caption': 'Railway detail: assess the queue and the available space beyond the tracks. No '
                           'safe clearance is measured by the drawing.'},
 'M06-R-slow': {'file': 'M06-v1.png',
                'box': [588, 160, 1045, 506],
                'width_mm': 80,
                'caption': 'Slower-vehicle detail for the written trip: describe the observations and space '
                           'needed before deciding whether to pass.'},
 'M06-R-entry': {'file': 'M06-v1.png',
                 'box': [1069, 141, 1419, 505],
                 'width_mm': 80,
                 'caption': 'Motorway-entry detail for the written trip: describe how you would assess speed '
                            'and traffic before joining.'},
 'M06-R-works': {'file': 'M06-v1.png',
                 'box': [574, 604, 860, 893],
                 'width_mm': 95,
                 'caption': 'Roadworks detail for the written trip: identify the information you need about '
                            'the temporary route. No path is selected for you.'}}

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
                f=para(overlay['label'],'source');_,fh=f.wrap(ww-4,hh);f.drawOn(c,xx+2,yy+(hh-fh)/2)
        c._code.append('EMC');c.restoreState()

class Chapter(BookCanvas):
    def __init__(self,path):
        super().__init__(path);self.questions={};self.answers={};self.page_labels={}
        self.c.setTitle('KörkortGo | Chapter 6 | Travel beyond the town')
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
GROUPS=[p for p in PLACEMENT['lesson_placements'] if p['location']['section_id'].startswith('M06')]
BINDINGS={b['code']:b for b in PLACEMENT['asset_caption_bindings']}
CAPTIONS={c['code']:c for c in json.loads((ROOT/'sign-captions.json').read_text())['captions']}
GROUP_TITLES={'LP035': 'Read the rural road ahead', 'LP036': 'Recognise animal warnings', 'LP037': 'Slow vehicles and following space', 'LP038': 'Overtaking signs and line information', 'LP039': 'Motorways and expressways', 'LP040': 'Read the joining-road layout', 'LP041': 'Prepare the exit early', 'LP042': 'Railway warnings and crossing controls', 'LP043': 'Roadworks and temporary guidance'}
GROUP_NOTES={'LP035': 'Independent examples of bends, gradients, narrowings, uneven road and passing places. Gradient numbers are percentages, not a safe-speed formula.', 'LP036': 'Each animal symbol has its own meaning. These examples do not imply that unpictured animals are absent.', 'LP037': 'The 50 m shown on C19 is a particular signed minimum distance, not a universal following gap for slow vehicles.', 'LP038': 'The prohibition and its end form a pair. For combined lines, identify the line nearest your lane. M20a warns of a coming centre-line or divider change; it is not an ordinary lane-change arrow.', 'LP039': 'Matched start/end pairs. The road regime does not override vehicle eligibility or the need to reduce speed for conditions.', 'LP040': 'Independent joining and lane-configuration examples. A road retaining its own lane differs from an acceleration lane; visual resemblance alone does not establish priority.', 'LP041': 'Independent navigation examples, not a single continuous route connecting the printed destinations. The separation marker does not authorise a late lane change.', 'LP042': 'Advance warnings, three/two/one countdown markers, crossbucks and active controls have different roles. Countdown boards do not specify fixed metre intervals. A still image does not reproduce flashing or sound. No crossing-ID number is invented.', 'LP043': 'Independent recognition sets, not one verified work-zone layout. Keep directional, diagonal and horizontal markers distinct. Actual signs, signals and authorised directions govern the route.'}

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
        super().__init__(path);self.vectors=[];self.sign_records=[];self.cont=0;self.section='M06';self.group_pages={};self.scene_pages={};self.pending=False
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
            headings={('LP035','A1'):'Bends and gradients',('LP035','A8'):'Narrow and uneven roads',('LP038','M3'):'Line information',('LP039','E1'):'Motorway',('LP039','E3'):'Expressway',('LP042','A35'):'Advance warnings',('LP042','A38'):'Countdown to the crossing',('LP042','A39'):'Crossing markers',('LP042','Y1'):'Signals, sound and barriers',('LP043','A20'):'Warnings',('LP043','F23'):'Diversions and temporary routes',('LP043','X1'):'Markers and physical guidance',('LP043','V1'):'Authorised guard instructions'}
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

def scene_page(b,key,title,keys,intro=None):
    b.end();b.start(key,b.section+' · Illustration');b.text(title,'subheading')
    if intro:b.text(intro)
    if len(keys)==2:
        b.add(Pair(keys),18)
        for k in keys:b.scene_pages[k]=b.page
    else:b.art(keys[0])

def lesson_body(b,n):
    key=f'M06-L{n:02d}';s=SECTIONS[key];paras=s['paragraphs'];b.section=key
    b.start(key,key);b.text(key,'source');b.text(s['title'],'heading');b.add(panel(paras[0]),18)
    worked=next(p for p in paras if p.startswith('**Worked decision.'))
    deferred=None
    for p in paras[1:paras.index(worked)]:
        # Keep the passing approach with its illustration, avoiding a one-paragraph page.
        if n==2 and p.startswith('**Learning approach.'):
            deferred=p;continue
        if p.startswith('|'):
            rows=[[para(v.strip(),'caption') for v in line.strip('|').split('|')] for line in p.splitlines() if not line.startswith('|---')]
            table=Table(rows,colWidths=[62*mm,108*mm],repeatRows=1)
            table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,0),COLORS['sage']),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]));b.ensure(table,18)
        else:b.text(p)
        for group in GROUPS:
            if group['location']['section_id']==key and group['location']['exact_quote']==p:b.signs(group)
    if n==1:
        scene_page(b,key+'-scenario','Make room at the narrowing',[key]);b.text(worked)
    elif n==2:
        scene_page(b,key+'-scenario','Assess the whole passing path',[key],deferred);b.text(worked)
    elif n==3:
        scene_page(b,key+'-scenario','Plan entry and exit',['M06-L03-entry','M06-L03-exit']);b.text(worked)
    else:
        scene_page(b,key+'-rail','Check the space beyond the tracks',['M06-L04-rail']);b.text(worked)
        b.text('The crossing ID is on the back of the crossbuck. Use it only if available without returning to danger; see the official level-crossing guide. [Trafikverket: level-crossing safety][rail]','caption')
        scene_page(b,key+'-works','Read the temporary road',['M06-L04-works'])
    check=next(p for p in paras if p.startswith('**Knowledge check.'));q,a=check.split(' **Answer:** ',1)
    b.end();b.start(key+'-question',key+' · Knowledge check');b.text('Check your understanding','heading');b.text(q);b.questions[key]=b.page;b.lines(8);b.text(paras[-1],'caption');b.end()
    return key,a

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Production(OUT/'chapter.pdf');answers=[]
    b.start('M06','Chapter 6');b.text('CHAPTER 06','source');b.text('Travel beyond the town','heading');b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24);b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    for key,title in [('M06-answers','Answers and review guidance'),('M06-references','Official references')]:b.add(Paragraph(f'<link href="#{key}" color="#173E32">{title}</link>',STYLES['body']),13)
    b.add(panel(re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1),'disclaimer'));b.end()
    for n in range(1,5):answers.append(lesson_body(b,n))
    b.section='M06-R';review=SECTIONS['M06-R']['paragraphs'];q,a=review[1].split(' **Review guide:** ',1)
    b.start('M06-R','M06-R · Self-assessment');b.text('Review and self-assessment','heading');b.text(review[0]);b.add(Pair(['M06-R-meeting','M06-R-bend']),18)
    for k in ['M06-R-meeting','M06-R-bend']:b.scene_pages[k]=b.page
    b.text('Use these rural details to describe what you can see and what remains uncertain.','caption');b.lines(5);b.end()
    for key,title,keys in [('M06-R-crossings','Crossing and junction details',['M06-R-junction','M06-R-rail']),('M06-R-route','Slower traffic and motorway entry',['M06-R-slow','M06-R-entry'])]:
        b.start(key,'M06-R · Continue');b.text(title,'subheading');b.add(Pair(keys),18)
        for k in keys:b.scene_pages[k]=b.page
        b.text('Relate the details to the written trip. Explain what would change your decision.','caption');b.lines(4);b.end()
    b.start('M06-R-works','M06-R · Temporary route');b.text('Bring the journey together','subheading');b.art('M06-R-works');b.text(q);b.questions['M06-R']=b.page;b.lines(4);b.end()
    b.start('M06-reflection','M06-R · Reflection');b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M06-answers','Answers and review guidance');b.text('Review after answering','heading')
    for key,ans in answers:b.text(key,'source',6);b.text('**Answer:** '+ans,space=20);b.answers[key]=b.page
    b.text('M06-R','source',6);b.text('**Review guide:** '+a);b.answers['M06-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M06-references' if offset==0 else 'M06-references-2';b.start(key,'Official references');b.text('Official references','heading')
        b.text('Chapter references checked 5 October 2026. Individual sign captions and artwork use the verified official asset register. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            b.text(LABELS[alias],'body',4);b.add(Paragraph(f'<link href="{escape(REFS[alias])}" color="#173E32">{escape(REFS[alias])}</link>',STYLES['source']),20)
        if offset==4:b.text('Road-sign illustrations: Transportstyrelsen. Each reference example links to its official description. Swedish names are official; English labels and explanations are editorial translations. Road scenes are simplified illustrations, not to scale.','caption')
        b.end()
    b.c.save();r=PdfReader(OUT/'chapter.pdf');w=PdfWriter();w.clone_document_from_reader(r)
    assert not b.vectors,'M06 currently uses only verified raster sign assets'
    w.root_object[NameObject('/Lang')]=TextStringObject('en-GB');w.root_object.pop(NameObject('/Outlines'),None)
    parent=w.add_outline_item('Chapter 6 · Travel beyond the town',0);current=parent
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M06':continue
        if key in SECTIONS:current=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key.startswith('LP'):w.add_outline_item(GROUP_TITLES[key],num-1,parent=current)
        elif key in ['M06-answers','M06-references','M06-reflection']:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
        elif key in ['M06-R-crossings','M06-R-route','M06-R-works'] or any(key.endswith(suf) for suf in ['-scenario','-rail','-works','-question']):w.add_outline_item(b.page_labels[num],num-1,parent=current)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels,'group_pages':b.group_pages,'scene_pages':b.scene_pages},indent=2)+'\n')
    for key,v in ART.items():
        v['sha256']=hashlib.sha256((ROOT/'pdf-design/gap-resolution'/v['file']).read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
        for o in v.get('overlays',[]):
            if 'code' in o:o['asset']=BINDINGS[o['code']]['preferred_asset'];o['official_url']=BINDINGS[o['code']]['official_url']
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops and exact official reference assets; screen review','assets':ART,'official_sign_placements':b.sign_records,'reference_cross_links':{},'review_preview_reconciliation':'All four approved review details retained. Approved lesson scenes provide the slower-vehicle, motorway-entry and roadwork details required by the unchanged written scenario. Ordinary junction is explicitly separate from motorway entry.'},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-06.pdf');print(f'Built {len(w.pages)} pages, {len(b.sign_records)} official reference placements and {len(ART)} scenes')
if __name__=='__main__':run()
