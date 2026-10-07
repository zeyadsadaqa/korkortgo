"""Step 6J: independently reproducible Chapter 9 review PDF."""
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
SOURCE='## 9. Reduce the impact of each journey\n'+MANUSCRIPT.split('## 9. Reduce the impact of each journey\n',1)[1].split('\n## 10. Respond, reflect and keep learning',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M09-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={'M09-L02': {'file': 'M09-v2.png',
             'box': [29, 160, 800, 487],
             'width_mm': 170,
             'caption': 'The teal car approaches a queue on the right side of '
                        'the road. Look ahead, retain room to stop and keep '
                        'the crossing clear. The illustration does not specify '
                        'a measured following distance.'},
 'M09-L03': {'file': 'M09-v2.png',
             'box': [835, 177, 1630, 450],
             'width_mm': 170,
             'caption': 'Separate journeys: home - shop - home, then home - '
                        'library - home. Combined journey: home - shop - '
                        'library - home. These are schematic options, not '
                        'measured routes or a promised saving. Check practical '
                        'needs and timing.'},
 'M09-L04': {'file': 'M09-v2.png',
             'box': [29, 586, 799, 893],
             'width_mm': 170,
             'caption': 'Check the vehicle record and the current local '
                        'decision before departure. The official E31 class-2 '
                        'example is for recognition only; it does not '
                        'establish a real boundary or permission for the '
                        'illustrated car.',
             'overlays': [{'rect': [554, 605, 783, 872], 'code': 'E31-2'}]},
 'M09-R': {'file': 'M09-v2.png',
           'box': [821, 586, 1455, 881],
           'width_mm': 170,
           'caption': 'Walking, cycling, public transport and a car are '
                      'options to compare against actual access needs, '
                      'services and conditions. The pictures do not rank the '
                      'modes or supply emissions figures.'}}

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
        self.c.setTitle('KörkortGo | Chapter 9 | Reduce the impact of each journey')
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
GROUPS=[p for p in PLACEMENT['lesson_placements'] if p['location']['section_id'].startswith('M09')]
BINDINGS={b['code']:b for b in PLACEMENT['asset_caption_bindings']}
CAPTIONS={c['code']:c for c in json.loads((ROOT/'sign-captions.json').read_text())['captions']}
GROUP_TITLES={'LP051':'Recognise environmental-zone starts and ends','LP052':'Charging and parking are different'}
GROUP_NOTES={'LP051':'Independent official examples. Match an ending to the same class at the start. These signs do not assert a current municipal boundary.','LP052':'A charging facility and a parking qualification are different. Neither symbol gives permission to enter an environmental zone.'}

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
        super().__init__(path);self.vectors=[];self.sign_records=[];self.cont=0;self.section='M09';self.group_pages={};self.scene_pages={};self.pending=False
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
            headings={}
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
    key=f'M09-L{n:02d}';s=SECTIONS[key];paras=s['paragraphs'];b.section=key
    b.start(key,key);b.text(key,'source');b.text(s['title'],'heading');b.add(panel(paras[0]),18)
    worked=next(p for p in paras if p.startswith('**Worked decision.'))
    for p in paras[1:paras.index(worked)]:
        b.text(p)
        for group in GROUPS:
            if group['location']['section_id']==key and group['location']['exact_quote']==p:b.signs(group)
    titles={1:'Compare the same environmental effect',2:'Look ahead and preserve room',3:'Combine a practical journey',4:'Check access before leaving'}
    if n==1:
        b.text(worked)
    else:
        scene_page(b,key+'-scenario',titles[n],[key]);b.text(worked)
    check=next(p for p in paras if p.startswith('**Knowledge check.'));q,a=check.split(' **Answer:** ',1)
    b.end();b.start(key+'-question',key+' · Knowledge check');b.text('Check your understanding','heading');b.text(q);b.questions[key]=b.page;b.lines(8);b.text(paras[-1],'caption');b.end()
    return key,a

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Production(OUT/'chapter.pdf');answers=[]
    b.start('M09','Chapter 9');b.text('CHAPTER 09','source');b.text('Reduce the impact of each journey','heading');b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24);b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    for key,title in [('M09-answers','Answers and review guidance'),('M09-references','Official references')]:b.add(Paragraph(f'<link href="#{key}" color="#173E32">{title}</link>',STYLES['body']),13)
    b.add(panel(re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1),'disclaimer'));b.end()
    for n in range(1,5):answers.append(lesson_body(b,n))
    b.section='M09-R';review=SECTIONS['M09-R']['paragraphs'];q,a=review[1].split(' **Review guide:** ',1)
    b.start('M09-R','M09-R · Self-assessment');b.text('Review and self-assessment','heading');b.text(review[0]);b.art('M09-R')
    b.text(q);b.questions['M09-R']=b.page;b.lines(7);b.end()
    b.start('M09-reflection','M09-R · Reflection');b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M09-answers','Answers and review guidance');b.text('Review after answering','heading')
    for key,ans in answers:b.text(key,'source',6);b.text('**Answer:** '+ans,space=20);b.answers[key]=b.page
    b.text('M09-R','source',6);b.text('**Review guide:** '+a);b.answers['M09-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M09-references' if offset==0 else f'M09-references-{offset//4+1}';b.start(key,'Official references');b.text('Official references','heading')
        b.text('Chapter references checked 7 October 2026. Individual sign captions and artwork use the verified official asset register. Always consult current official guidance and the applicable rules.','caption',18)
        for alias in ALIASES[offset:offset+4]:
            b.text(LABELS[alias],'body',4);b.add(Paragraph(f'<link href="{escape(REFS[alias])}" color="#173E32">{escape(REFS[alias])}</link>',STYLES['source']),20)
        if offset+4>=len(ALIASES):b.text('Road-sign illustrations: Transportstyrelsen. Each reference example links to its official description. Swedish names are official; English labels and explanations are editorial translations. Road scenes are simplified illustrations, not to scale.','caption')
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
    parent=w.add_outline_item('Chapter 9 · Reduce the impact of each journey',0);current=parent
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M09':continue
        if key in SECTIONS:current=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key.startswith('LP'):w.add_outline_item(GROUP_TITLES[key],num-1,parent=current)
        elif key in ['M09-answers','M09-references','M09-reflection']:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
        elif key in ['M09-R-conditions'] or any(key.endswith(suf) for suf in ['-scenario','-rail','-works','-question']):w.add_outline_item(b.page_labels[num],num-1,parent=current)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels,'group_pages':b.group_pages,'scene_pages':b.scene_pages},indent=2)+'\n')
    for key,v in ART.items():
        v['sha256']=hashlib.sha256((ROOT/'pdf-design/gap-resolution'/v['file']).read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
        for o in v.get('overlays',[]):
            if 'code' in o:o['asset']=BINDINGS[o['code']]['preferred_asset'];o['official_url']=BINDINGS[o['code']]['official_url']
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops and exact official reference assets; screen review','assets':ART,'official_sign_placements':b.sign_records,'reference_cross_links':{},'review_preview_reconciliation':'M09-v2 approved scenes retained; M09-L01 remains text-only. Official E31-2 replaces the reserved sign panel. Route labels are transcribed in a selectable caption; the review retains four modes and uses native blank writing lines.'},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-09.pdf');print(f'Built {len(w.pages)} pages, {len(b.sign_records)} official reference placements and {len(ART)} scenes')
if __name__=='__main__':run()
