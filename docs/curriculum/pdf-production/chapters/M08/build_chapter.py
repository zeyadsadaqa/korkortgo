"""Step 6I: independently reproducible Chapter 8 review PDF."""
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
SOURCE='## 8. Take responsibility for the vehicle and load\n'+MANUSCRIPT.split('## 8. Take responsibility for the vehicle and load\n',1)[1].split('\n## 9. Reduce the impact of each journey',1)[0]
REFS=dict(re.findall(r'^\[([^]]+)\]: (.+)$',MANUSCRIPT,re.M))
PARTS=re.split(r'^### (M08-[^ ]+) · (.+)\n',SOURCE,flags=re.M)
SECTIONS={PARTS[i]:{'title':PARTS[i+1],'paragraphs':PARTS[i+2].strip().split('\n\n')} for i in range(1,len(PARTS),3)}
ALIASES=list(dict.fromkeys(re.findall(r'\]\[([^]]+)\]',SOURCE)))
LABELS={key:next(label for label,k in re.findall(r'\[([^]]+)\]\[([^]]+)\]',SOURCE) if k==key) for key in ALIASES}
ART={'M08-L01': {'file': 'M08-v2.png',
             'box': [29, 169, 827, 404],
             'width_mm': 170,
             'caption': 'Hypothetical registered total weights: 2,200 kg + '
                        '1,500 kg = 3,700 kg. Check entitlement and technical '
                        'limits separately. The pictured vehicle does not '
                        'establish its capacity.'},
 'M08-L02': {'file': 'M08-v2.png',
             'box': [843, 165, 1643, 399],
             'width_mm': 170,
             'caption': 'Hypothetical loading calculation: 400 kg ready weight '
                        '+ 500 kg cargo = 900 kg actual weight. Example towing '
                        'limit: 800 kg. The goods are beside the trailer for '
                        'planning; this is not a secured-load demonstration.'},
 'M08-L04': {'file': 'M08-v2.png',
             'box': [29, 545, 827, 887],
             'width_mm': 170,
             'caption': 'The driver follows the temporary road path and '
                        'remains responsible for control. The left marker '
                        'bands slope down towards the road; the right markers '
                        'slope down the opposite way. Official X3 artwork: '
                        'Transportstyrelsen. Simplified scene, not to scale.',
             'overlays': [{'code': 'X3-2',
                           'rect': [115, 685, 134, 758],
                           'side': 'left'},
                          {'code': 'X3-2',
                           'rect': [198, 683, 209, 734],
                           'side': 'left'},
                          {'code': 'X3-2',
                           'rect': [243, 683, 249, 716],
                           'side': 'left'},
                          {'code': 'X3-2',
                           'rect': [489, 682, 495, 715],
                           'side': 'right'},
                          {'code': 'X3-2',
                           'rect': [507, 685, 516, 725],
                           'side': 'right'},
                          {'code': 'X3-2',
                           'rect': [536, 689, 548, 741],
                           'side': 'right'},
                          {'code': 'X3-2',
                           'rect': [617, 704, 641, 793],
                           'side': 'right'},
                          {'code': 'X3-2',
                           'rect': [763, 706, 798, 841],
                           'side': 'right'}]},
 'M08-R': {'file': 'M08-v2.png',
           'box': [843, 542, 1640, 756],
           'width_mm': 170,
           'caption': 'A borrowed car and trailer await loading. Establish the '
                      'missing figures and documents before deciding to drive. '
                      'The drawing supplies no verified weight, entitlement or '
                      'towing capacity.'}}

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
                sw,sh=Image.open(path).size
                # Select the matching member of the official paired asset; no mirroring or redraw.
                sx1,sx2=(0,877) if overlay['side']=='left' else (1533,2410)
                c.saveState();clip=c.beginPath();clip.rect(xx,yy,ww,hh);c.clipPath(clip,stroke=0)
                c.drawImage(str(path),xx-sx1*ww/(sx2-sx1),yy,sw*ww/(sx2-sx1),hh,mask='auto');c.restoreState()
            else:
                f=para(overlay['label'],'source');_,fh=f.wrap(ww-4,hh);f.drawOn(c,xx+2,yy+(hh-fh)/2)
        c._code.append('EMC');c.restoreState()

class Chapter(BookCanvas):
    def __init__(self,path):
        super().__init__(path);self.questions={};self.answers={};self.page_labels={}
        self.c.setTitle('KörkortGo | Chapter 8 | Take responsibility for the vehicle and load')
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
GROUPS=[p for p in PLACEMENT['lesson_placements'] if p['location']['section_id'].startswith('M08')]
BINDINGS={b['code']:b for b in PLACEMENT['asset_caption_bindings']}
CAPTIONS={c['code']:c for c in json.loads((ROOT/'sign-captions.json').read_text())['captions']}
GROUP_TITLES={'LP048':'Weight restrictions and vehicle symbols','LP049':'Dimensions and bearing capacity','LP050':'Trailer access and vehicle symbols'}
GROUP_NOTES={'LP048':'These are independent reference examples. Distinguish actual gross weight, combination weight and axle loads from a registered-weight qualifier. Vehicle symbols are shown separately; they are not a combined sign assembly.', 'LP049':'Independent examples distinguish width, height, length, a width plate and bearing-capacity classes. A general vehicle limit does not override a lower signed restriction.', 'LP050':'C6 controls access for the specified trailer combinations; it does not set a speed limit. The vehicle symbols are independent references, not additions to the pictured C6 sign.'}

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
        super().__init__(path);self.vectors=[];self.sign_records=[];self.cont=0;self.section='M08';self.group_pages={};self.scene_pages={};self.pending=False
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
    key=f'M08-L{n:02d}';s=SECTIONS[key];paras=s['paragraphs'];b.section=key
    b.start(key,key);b.text(key,'source');b.text(s['title'],'heading');b.add(panel(paras[0]),18)
    worked=next(p for p in paras if p.startswith('**Worked decision.'))
    for p in paras[1:paras.index(worked)]:
        if p.startswith('|'):
            rows=[[para(v.strip(),'caption') for v in line.strip('|').split('|')] for line in p.splitlines() if not line.startswith('|---')]
            table=Table(rows,colWidths=[45*mm,125*mm],repeatRows=1)
            table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,0),COLORS['sage']),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]));b.ensure(table,18)
        else:b.text(p)
        for group in GROUPS:
            if group['location']['section_id']==key and group['location']['exact_quote']==p:b.signs(group)
    titles={1:'Two separate checks',2:'Know the actual load',4:'Assistance has limits'}
    if n!=3:scene_page(b,key+'-scenario',titles[n],[key])
    if n==4:b.add(Paragraph('<link href="'+BINDINGS['X3-2']['official_url']+'" color="#173E32">Transportstyrelsen · X3 official description</link>',STYLES['source']),12)
    b.text(worked)
    check=next(p for p in paras if p.startswith('**Knowledge check.'));q,a=check.split(' **Answer:** ',1)
    b.end();b.start(key+'-question',key+' · Knowledge check');b.text('Check your understanding','heading');b.text(q);b.questions[key]=b.page;b.lines(8);b.text(paras[-1],'caption');b.end()
    return key,a

def run():
    (OUT/'chapter-source.md').write_text(SOURCE+'\n\n'+'\n'.join(f'[{k}]: {REFS[k]}' for k in ALIASES)+'\n')
    b=Production(OUT/'chapter.pdf');answers=[]
    b.start('M08','Chapter 8');b.text('CHAPTER 08','source');b.text('Take responsibility for the vehicle and load','heading');b.text(PARTS[0].split('\n\n',1)[1].strip(),space=24);b.text('In this chapter','subheading')
    for key,v in SECTIONS.items():b.add(Paragraph(f'<link href="#{key}" color="#173E32"><b>{key}</b> · {escape(v["title"])}</link>',STYLES['body']),13)
    for key,title in [('M08-answers','Answers and review guidance'),('M08-references','Official references')]:b.add(Paragraph(f'<link href="#{key}" color="#173E32">{title}</link>',STYLES['body']),13)
    b.add(panel(re.search(r'> \*\*(.*?)\*\*',MANUSCRIPT).group(1),'disclaimer'));b.end()
    for n in range(1,5):answers.append(lesson_body(b,n))
    b.section='M08-R';review=SECTIONS['M08-R']['paragraphs'];q,a=review[1].split(' **Review guide:** ',1)
    b.start('M08-R','M08-R · Self-assessment');b.text('Review and self-assessment','heading');b.text(review[0]);b.art('M08-R')
    b.text(q);b.questions['M08-R']=b.page;b.lines(9);b.end()
    b.start('M08-reflection','M08-R · Reflection');b.text('Keep a practice record','heading');b.text(review[2]);b.lines(17);b.end()
    b.start('M08-answers','Answers and review guidance');b.text('Review after answering','heading')
    for key,ans in answers:b.text(key,'source',6);b.text('**Answer:** '+ans,space=20);b.answers[key]=b.page
    b.text('M08-R','source',6);b.text('**Review guide:** '+a);b.answers['M08-R']=b.page;b.end()
    for offset in range(0,len(ALIASES),4):
        key='M08-references' if offset==0 else f'M08-references-{offset//4+1}';b.start(key,'Official references');b.text('Official references','heading')
        b.text('Chapter references checked 5 October 2026. Individual sign captions and artwork use the verified official asset register. Always consult current official guidance and the applicable rules.','caption',18)
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
    parent=w.add_outline_item('Chapter 8 · Take responsibility for the vehicle and load',0);current=parent
    for key,num in b.destinations.items():
        w.add_named_destination(key,num-1)
        if key=='M08':continue
        if key in SECTIONS:current=w.add_outline_item(key+' · '+SECTIONS[key]['title'],num-1,parent=parent)
        elif key.startswith('LP'):w.add_outline_item(GROUP_TITLES[key],num-1,parent=current)
        elif key in ['M08-answers','M08-references','M08-reflection']:w.add_outline_item(b.page_labels[num],num-1,parent=parent)
        elif key in ['M08-R-conditions'] or any(key.endswith(suf) for suf in ['-scenario','-rail','-works','-question']):w.add_outline_item(b.page_labels[num],num-1,parent=current)
    w.add_named_destination('contents',0)
    with (OUT/'chapter.pdf').open('wb') as f:w.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'questions':b.questions,'answers':b.answers,'page_labels':b.page_labels,'group_pages':b.group_pages,'scene_pages':b.scene_pages},indent=2)+'\n')
    for key,v in ART.items():
        v['sha256']=hashlib.sha256((ROOT/'pdf-design/gap-resolution'/v['file']).read_bytes()).hexdigest();v['alt_text']=v['caption'];v['print_ppi']=round((v['box'][2]-v['box'][0])/(v.get('width_mm',170)*mm/72),1)
        for o in v.get('overlays',[]):
            if 'code' in o:o['asset']=BINDINGS[o['code']]['preferred_asset'];o['official_url']=BINDINGS[o['code']]['official_url']
    (OUT/'illustrations.json').write_text(json.dumps({'status':'approved crops and exact official reference assets; screen review','assets':ART,'official_sign_placements':b.sign_records,'reference_cross_links':{},'review_preview_reconciliation':'Approved M08-v2 scenes retained. M08-L03 remains a text checklist. Arithmetic and review prompts are selectable text; eight marker faces use the matching member of exact official X3-2 artwork.'},indent=2)+'\n')
    shutil.copyfile(OUT/'chapter.pdf',REPO/'output/pdf/korkortgo-chapter-08.pdf');print(f'Built {len(w.pages)} pages, {len(b.sign_records)} official reference placements and {len(ART)} scenes')
if __name__=='__main__':run()
