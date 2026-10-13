"""Step 6L: reproducible appendices, complete sign reference and official sources."""
from pathlib import Path
import sys,re,json,hashlib,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'chapters/M10'))
from build_chapter import *
OUT=Path(__file__).resolve().parent
TARGET=OUT.parent/'reference-material.pdf'
FULL=(ROOT/'manuscript.md').read_text()
RAW=FULL.split('## Appendix A · ',1)[1]
SOURCE='## Appendix A · '+RAW
BODY=SOURCE.split('\n[aeb]:',1)[0]
PARTS=re.split(r'^## (.+)\n',BODY,flags=re.M)
SECS={PARTS[i]:PARTS[i+1].strip() for i in range(1,len(PARTS),2)}
TITLES=list(SECS)
GROUPS=PLACEMENT['reference_groups']
CREDIT='Road-sign illustrations: Transportstyrelsen. Source links and verification dates are recorded in the official references.'
OLD='Use the [official Transportstyrelsen catalogue][signs] alongside this manuscript until the separately verified illustrated reference is prepared.'
NEW='Use the [official Transportstyrelsen catalogue][signs] alongside this illustrated reference.'
REUSE='https://www.transportstyrelsen.se/sv/om-oss/pressrum/pressbilder/'

def table_rows(text):
 return [[cell.strip() for cell in row.strip('|').split('|')] for row in text.splitlines() if row.startswith('|') and not row.startswith('|---')]

class Reference(BookCanvas):
 def __init__(self):
  super().__init__(TARGET);self.page_labels={};self.sign_records=[];self.vectors=[];self.section='reference-contents';self.cont=0
  self.c.setTitle('KörkortGo | Appendices and official references')
 def start(self,key,label):
  super().start(key,label);self.page_labels[self.page]=label
  if self.page==1:self.c.bookmarkPage('contents')
 def ensure(self,f,space=12):
  if f.wrap(WIDTH,1000)[1]+space>self.y-30*mm:
   self.end();self.cont+=1;self.start(self.section+'-continued-'+str(self.cont),self.page_labels[self.page]+' · Continued' if 'Continued' not in self.page_labels[self.page] else self.page_labels[self.page]);self.add(para('Continue the reference','subheading'),15)
  self.add(f,space)
 def text(self,t,style='body',space=12):
  f=Paragraph('<link href="'+escape(t)+'" color="#173E32">'+escape(t)+'</link>',STYLES[style]) if t.startswith('https://') else para(t,style)
  self.ensure(f,space)
 def link(self,key,label):self.ensure(Paragraph('<link href="#'+key+'" color="#173E32">'+escape(label)+'</link>',STYLES['body']),10)
 def table(self,rows,widths):
  t=Table([[para(c,'caption') for c in r] for r in rows],colWidths=widths,repeatRows=1)
  t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Body'),('BACKGROUND',(0,0),(-1,0),COLORS['mist']),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,COLORS['line']),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
  self.ensure(t,18)
 def lines(self,n):
  self.c.setStrokeColor(COLORS['line']);self.c.setLineWidth(.5)
  for _ in range(n):
   self.y-=22;assert self.y>30*mm;self.c.line(M,self.y,W-M,self.y)
  self.y-=16

class RefCard(SignCard):
 def __init__(self,code,b,group):
  super().__init__(code,b,group)
  # Extend the established caption unit with the full URL and actual caption-check date.
  self.source=para(self.bind['official_url'],'source')
  self.sh=self.source.wrap(WIDTH,1000)[1]+20
  self.original_height=self.height;self.height+=self.sh
 def draw(self):
  c=self.canv;self.book.c.bookmarkPage('sign-'+self.code);self.book.destinations['sign-'+self.code]=self.book.page
  h=self.height;self.height=self.original_height
  c.saveState();c.translate(0,self.sh);super().draw();c.restoreState();self.height=h
  date=CAPTIONS[self.code]['reviewed_on']
  f=para('Caption checked '+date+' · English wording is editorial.','source');_,fh=f.wrap(WIDTH,1000);f.drawOn(c,0,self.sh-fh-3)
  _,fh=self.source.wrap(WIDTH,1000);self.source.drawOn(c,0,1)

def run():
 (OUT/'reference-source.md').write_text(SOURCE.replace(OLD,NEW))
 b=Reference();b.start('reference-contents','Reference material');b.text('APPENDICES AND SOURCES · 2026 version','source');b.text('Keep learning, checking and practising','heading')
 for i,title in enumerate(TITLES):b.link('appendix-'+chr(65+i) if i<4 else 'official-references',title)
 b.link('sign-group-index','Sign groups RB01–RB24');b.link('sign-family-index','Sign code and family lookup')
 b.add(panel(re.search(r'> \*\*(.*?)\*\*',FULL).group(1),'disclaimer'),18);b.end()
 # A: complete practical checklists, with enough room for each routine.
 b.section='appendix-A';b.start(b.section,'Appendix A');b.text(TITLES[0].split(' · ')[1],'heading')
 for p in SECS[TITLES[0]].split('\n\n'):
  if p.startswith('### '):
   title=p[4:]
   if title=='While approaching a new situation':b.end();b.start('appendix-A-situations','Appendix A · Situations')
   b.text(title,'subheading')
  elif p.startswith('- '):
   for item in p.splitlines():b.text(item[2:])
  elif p.startswith('1. '):
   for item in p.splitlines():b.text(item)
  else:b.text(p)
 b.end()
 # B introduction and full manuscript family table.
 b.section='appendix-B';b.start(b.section,'Appendix B');b.text(TITLES[1].split(' · ')[1],'heading')
 paras=SECS[TITLES[1]].replace(OLD,NEW).split('\n\n');b.text(paras[0]);b.text(CREDIT,'caption');b.text('Swedish names are official. English names and explanations are editorial translations. Examples are independent, not verified sign assemblies.','caption');b.text(paras[-1]);b.end()
 rows=table_rows(paras[1])
 for j in range(1,len(rows),6):
  b.start('appendix-B-study-'+str(j),'Appendix B · Study groups');b.text('Study the decision','heading');b.table([rows[0]]+rows[j:j+6],[48*mm,89*mm,33*mm]);b.end()
 for offset in [0,12]:
  b.start('sign-group-index' if offset==0 else 'sign-group-index-2','Appendix B · Group index');b.text('Find a sign group','heading')
  for g in GROUPS[offset:offset+12]:b.link(g['group_id'],g['group_id']+' · '+g['title'])
  b.end()
 for g in GROUPS:
  gid=g['group_id'];b.section=gid;b.start(gid,gid+' · '+g['title']);b.text(gid,'source');b.text(g['title'],'heading');b.text(g['learning_purpose'],'caption');b.text('Related lessons: '+', '.join(g['selection_intended_lessons']),'source')
  codes=g['primary_codes']+g['additional_comparison_codes']
  if RefCard(codes[0],b,gid).height+16>b.y-30*mm:
   b.text('In this group','subheading')
   for offset in range(0,len(codes),5):
    links=' · '.join('<link href="#sign-'+code+'" color="#173E32">'+code+'</link>' for code in codes[offset:offset+5])
    b.ensure(Paragraph(links,STYLES['body']),12)
   b.text('Use the links to compare each example with its explanation. Read the main sign and any qualifications together.','caption')
  for code in codes:b.ensure(RefCard(code,b,gid),16)
  if g['cross_reference_codes']:
   b.text('Related entries','subheading')
   for code in g['cross_reference_codes']:b.link('sign-'+code,code+' · '+BINDINGS[code]['label_en'])
  b.end()
 # Family lookup: codes link to unique primary entries, never repeat the artwork.
 families={}
 for bind in BINDINGS.values():families.setdefault(bind['family'],[]).append(bind['code'])
 b.section='sign-family-index';b.start(b.section,'Appendix B · Code lookup');b.text('Find a code or family','heading')
 for fam,codes in families.items():
  b.text(fam,'subheading')
  for start in range(0,len(codes),8):
   labels=' · '.join('<link href="#sign-'+escape(code)+'" color="#173E32">'+escape(code)+'</link>' for code in codes[start:start+8]);b.ensure(Paragraph(labels,STYLES['body']),12)
 b.end()
 # C: repeated headers on glossary pages; retain every term and stable lesson reference.
 pars=SECS[TITLES[2]].split('\n\n');rows=table_rows(pars[1]);b.section='appendix-C'
 for j in range(1,len(rows),6):
  b.start('appendix-C' if j==1 else 'appendix-C-'+str(j),'Appendix C · Glossary');b.text(TITLES[2].split(' · ')[1] if j==1 else 'Glossary continued','heading')
  if j==1:b.text(pars[0])
  b.table([rows[0]]+rows[j:j+6],[52*mm,88*mm,30*mm]);b.end()
 # D: all nine prompts, distributed over two pages for handwriting.
 pars=SECS[TITLES[3]].split('\n\n');rows=table_rows(pars[1]);b.section='appendix-D'
 for j in [1,6]:
  b.start('appendix-D' if j==1 else 'appendix-D-continued','Appendix D · Practice record');b.text(TITLES[3].split(' · ')[1] if j==1 else 'Continue your practice record','heading')
  if j==1:b.text(pars[0])
  b.text('Prompt · Your record','source')
  for row in rows[j:j+5]:b.text(row[0],'body',3);b.lines(2)
  if j==6:b.text(pars[-1])
  b.end()
 # Complete approved reference list with original factual-check dates and full URLs.
 pars=SECS[TITLES[4]].split('\n\n');entries=pars[1].splitlines();b.section='official-references'
 for j in range(0,len(entries),4):
  b.start('official-references' if j==0 else 'official-references-'+str(j//4+1),'Official references');b.text('Official references','heading')
  if j==0:b.text(pars[0]);b.text('Later chapter checks are recorded with those chapters. Link availability for this reference edition was checked separately on 7 October 2026; this does not change the factual-check dates below.','caption')
  for entry in entries[j:j+4]:
   b.text(entry[2:],'body',4);alias=re.search(r'\]\[([^]]+)\]',entry)[1];b.text(REFS[alias],'source',20)
  b.end()
 b.start('artwork-credits','Artwork and source credits');b.text('Artwork and source credits','heading');b.text(CREDIT);b.text('English sign labels and explanations are editorial translations. The sign reference uses official catalogue artwork in its teaching context. This learning material is not endorsed by Transportstyrelsen.');b.text('Individual sign-caption checks are dated in each entry. Source pages were retrieved on 1 October 2026 and captions reviewed on 2 October; resolved official-vector assets were verified on 3 October. Original artwork is preserved.','caption');b.text('Transportstyrelsen · road-sign reuse guidance','body',4);b.text(REUSE,'source');b.text('Transportstyrelsen · official sign catalogue','body',4);b.text(REFS['signs'],'source');b.text('The first-aid reference is limited to 1177 public healthcare guidance. No clinical procedure is reproduced.','caption');b.end()
 b.c.save();r=PdfReader(TARGET);w=PdfWriter();w.clone_document_from_reader(r)
 from pypdf import Transformation
 from pypdf.generic import DecodedStreamObject
 for rec in b.vectors:
  vector=PdfReader(REPO/rec['path']).pages[0];content=vector.get_contents();assert not any(op in (b'Tj',b'TJ',b'"',b"'",b'Do') for _,op in content.operations)
  content.operations=[(args,op) for args,op in content.operations if op!=b'Tf'];vector[NameObject('/Contents')]=content;vector['/Resources'].pop(NameObject('/Font'),None)
  stream=DecodedStreamObject();stream.set_data(('/Span << /ActualText <FEFF'+rec['alt'].encode('utf-16-be').hex()+'> >> BDC\n').encode()+vector.get_contents().get_data()+b'\nEMC');vector[NameObject('/Contents')]=stream
  scale=rec['width']/float(vector.mediabox.width);w.pages[rec['page']-1].merge_transformed_page(vector,Transformation().scale(scale).translate(rec['x'],rec['y']))
 w.root_object[NameObject('/Lang')]=TextStringObject('en-GB');w.root_object.pop(NameObject('/Outlines'),None)
 parent=w.add_outline_item('Appendices and official references',0);current=parent
 for key,num in b.destinations.items():
  w.add_named_destination(key,num-1)
  if key in ['appendix-A','appendix-B','appendix-C','appendix-D','official-references','artwork-credits']:current=w.add_outline_item(b.page_labels[num],num-1,parent=parent)
  elif key in [g['group_id'] for g in GROUPS]:w.add_outline_item(b.page_labels[num],num-1,parent=current)
 w.add_named_destination('contents',0)
 with TARGET.open('wb') as f:w.write(f)
 (OUT/'navigation.json').write_text(json.dumps({'destinations':b.destinations,'page_labels':b.page_labels},indent=2)+'\n')
 (OUT/'assets.json').write_text(json.dumps({'official_sign_placements':b.sign_records,'source_inputs':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['sign-placement-map.json','sign-captions.json','manuscript.md']},'editorial_changes':[{'original':OLD,'replacement':NEW,'reason':'The illustrated reference is now present; remove obsolete production-stage wording.'}]},indent=2)+'\n')
 shutil.copyfile(TARGET,REPO/'output/pdf/korkortgo-reference-material.pdf');print('Built',len(w.pages),'pages;',len(b.sign_records),'sign entries;',len(b.vectors),'vectors')
if __name__=='__main__':run()
