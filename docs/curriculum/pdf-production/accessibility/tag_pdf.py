"""Deterministic semantic repair of the approved PDF, preserving its painted content.

The original review and approval identity are never overwritten. The tag tree is
built from actual text runs/annotations and exact source-table rows. All original
painting operators remain in order; Tj strings are split only at link boundaries.
Run the independent validator and render comparison before accepting the output.
"""
from pathlib import Path
import json,re,hashlib,copy,collections,shutil
from xml.sax.saxutils import escape
from pypdf import PdfReader,PdfWriter
from pypdf._cmap import get_encoding
from pypdf.generic import (NameObject as N,DictionaryObject as D,ArrayObject as A,
 NumberObject as I,TextStringObject as T,BooleanObject as B,ByteStringObject,
 DecodedStreamObject,NullObject)
HERE=Path(__file__).resolve().parent;PROD=HERE.parent;ROOT=PROD.parents[2]
SOURCE=PROD/'korkortgo-curriculum-review.pdf';TARGET=PROD/'korkortgo-curriculum-tagged.pdf'
IDENTITY=[1.,0.,0.,1.,0.,0.]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ' '.join(s.replace('*','').replace('\u00ad','').split())
def clean_md(s):return norm(re.sub(r'\[([^]]+)\]\[[^]]+\]',r'\1',s))
def mul(a,b):
 return [a[0]*b[0]+a[2]*b[1],a[1]*b[0]+a[3]*b[1],a[0]*b[2]+a[2]*b[3],a[1]*b[2]+a[3]*b[3],a[0]*b[4]+a[2]*b[5]+a[4],a[1]*b[4]+a[3]*b[5]+a[5]]
def point(m,x,y):return (m[0]*x+m[2]*y+m[4],m[1]*x+m[3]*y+m[5])
def box_points(b):return [(b[0],b[1]),(b[2],b[1]),(b[2],b[3]),(b[0],b[3])]
def bounds(points):return [min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)]
def raw(v):
 if isinstance(v,bytes):return bytes(v)
 try:return v.original_bytes
 except Exception:return str(v).encode('latin1')
class Tracker:
 def __init__(self,page,annotations):
  self.state={'cm':IDENTITY.copy(),'clip':[float(page.mediabox.left),float(page.mediabox.bottom),float(page.mediabox.right),float(page.mediabox.top)],'font':None,'size':12.,'tc':0.,'tw':0.,'tz':1.,'ts':0.,'tl':0.};self.stack=[];self.tm=IDENTITY.copy();self.lm=IDENTITY.copy();self.annotations=annotations;self.fonts={};self.break_pending=False;self.shown=False;self.path_points=[]
  for key,ref in page['/Resources'].get('/Font',{}).items():
   font=ref.get_object();encoding,cmap=get_encoding(font)
   self.fonts[str(key)]={'font':font,'map':cmap,'encoding':encoding,'first':int(font.get('/FirstChar',0)),'widths':font.get('/Widths',[])}
 def advance(self,dx):self.tm[4]+=dx*self.tm[0];self.tm[5]+=dx*self.tm[1]
 def newline(self,x=0,y=None):
  y=-self.state['tl'] if y is None else y;self.lm[4]+=x*self.lm[0]+y*self.lm[2];self.lm[5]+=x*self.lm[1]+y*self.lm[3];self.tm=self.lm.copy();self.break_pending=True
 def glyphs(self,v):
  s=self.state;f=self.fonts[s['font']];data=raw(v);size=int(f['map'].get(-1,1));assert size==1,'Unexpected multi-byte font; extend decoder before use'
  parts=[]
  for code in data:
   encoded=chr(code);text=f['map'].get(encoded,encoded)
   if '\x00' in text and code:raise ValueError(('Unmapped meaningful glyph',s['font'],code))
   idx=code-f['first'];width=float(f['widths'][idx]) if 0<=idx<len(f['widths']) else 0.
   dx=(width*s['size']/1000+s['tc']+(s['tw'] if code==32 else 0))*s['tz']
   matrix=mul(s['cm'],self.tm);xy=point(matrix,dx/2,s['ts']+s['size']*.25)
   hits=[a for a in self.annotations if a['rect'][0]-.25<=xy[0]<=a['rect'][2]+.25 and a['rect'][1]-.25<=xy[1]<=a['rect'][3]+.25]
   hits.sort(key=lambda a:(a['rect'][2]-a['rect'][0])*(a['rect'][3]-a['rect'][1]))
   ann=hits[0]['index'] if hits else None
   bb=bounds([point(matrix,x,y) for x,y in [(0,s['ts']-s['size']*.2),(dx,s['ts']-s['size']*.2),(0,s['ts']+s['size']*.8),(dx,s['ts']+s['size']*.8)]])
   if parts and parts[-1]['annotation']==ann:parts[-1]['bytes']+=bytes([code]);parts[-1]['text']+=text;parts[-1]['points']+=box_points(bb)
   else:parts.append({'bytes':bytes([code]),'text':text,'annotation':ann,'points':box_points(bb)})
   self.advance(dx)
  if parts and self.break_pending and self.shown:parts[0]['text']=' '+parts[0]['text']
  if parts:self.shown=True;self.break_pending=False
  return parts
 def op(self,args,op):
  s=self.state;points=[];pieces=[]
  if op==b'q':self.stack.append(copy.deepcopy(s))
  elif op==b'Q':self.state=self.stack.pop()
  elif op==b'cm':s['cm']=mul(s['cm'],list(map(float,args)))
  elif op==b'BT':self.tm=IDENTITY.copy();self.lm=self.tm.copy();self.shown=False;self.break_pending=False
  elif op==b'Tm':self.tm=list(map(float,args));self.lm=self.tm.copy()
  elif op==b'Td':self.newline(float(args[0]),float(args[1]))
  elif op==b'TD':s['tl']=-float(args[1]);self.newline(float(args[0]),float(args[1]))
  elif op==b'T*':self.newline()
  elif op==b'Tf':s['font']=str(args[0]);s['size']=float(args[1])
  elif op in [b'Tc',b'Tw',b'TL',b'Ts',b'Tz']:
   key={b'Tc':'tc',b'Tw':'tw',b'TL':'tl',b'Ts':'ts',b'Tz':'tz'}[op];s[key]=float(args[0])/(100 if op==b'Tz' else 1)
  elif op==b'Tj':pieces=self.glyphs(args[0])
  elif op==b'TJ':
   # The current ReportLab source uses Tj; numeric kerning requires preserving TJ arrays.
   raise ValueError('TJ operator requires a reviewed extension; refusing a lossy repair')
  elif op in [b"'",b'"']:raise ValueError('Unsupported text-show operator')
  elif op==b're':
   x,y,w,h=map(float,args);points=[point(s['cm'],x,y),point(s['cm'],x+w,y+h)]
  elif op in [b'm',b'l']:points=[point(s['cm'],float(args[0]),float(args[1]))]
  elif op==b'c':points=[point(s['cm'],float(args[j]),float(args[j+1])) for j in [0,2,4]]
  elif op in [b'v',b'y']:points=[point(s['cm'],float(args[j]),float(args[j+1])) for j in [0,2]]
  elif op==b'Do':points=[point(s['cm'],x,y) for x,y in [(0,0),(1,0),(1,1),(0,1)]]
  if op in [b're',b'm',b'l',b'c',b'v',b'y']:
   self.path_points+=points;points=[]
  elif op in [b'W',b'W*']:
   if self.path_points:
    bb=bounds(self.path_points);cl=self.state['clip'];self.state['clip']=[max(cl[0],bb[0]),max(cl[1],bb[1]),min(cl[2],bb[2]),min(cl[3],bb[3])]
  elif op in [b'S',b's',b'f',b'F',b'f*',b'B',b'B*',b'b',b'b*']:
   points=self.path_points;self.path_points=[]
  elif op==b'n':self.path_points=[]
  if points:
   bb=bounds(points);cl=self.state['clip'];bb=[max(bb[0],cl[0]),max(bb[1],cl[1]),min(bb[2],cl[2]),min(bb[3],cl[3])]
   points=box_points(bb) if bb[2]>=bb[0] and bb[3]>=bb[1] else []
  return pieces,points

def discover(page,page_number):
 annotations=[]
 for i,ref in enumerate(page.get('/Annots',[])):
  a=ref.get_object();assert a['/Subtype']=='/Link'
  annotations.append({'index':i,'object':a,'ref':ref,'rect':list(map(float,a['/Rect']))})
 track=Tracker(page,annotations);ops=page.get_contents().operations;units=[];i=0
 while i<len(ops):
  args,op=ops[i]
  if op==b'BDC' and isinstance(args[1],dict) and '/ActualText' in args[1]:
   start=i;depth=1;i+=1;pts=[];runs=[]
   while depth:
    a,o=ops[i];pieces,p=track.op(a,o);pts+=p
    if pieces:runs.append({'offset':i-start,'pieces':pieces})
    if o in [b'BDC',b'BMC']:depth+=1
    elif o==b'EMC':depth-=1
    i+=1
   assert pts
   units.append({'kind':'figure','start':start,'end':i,'ops':ops[start:i],'text':str(args[1]['/ActualText']),'box':bounds(pts),'runs':runs})
  elif op==b'BT':
   start=i;rows=[];size=0;pts=[];text='';i+=1;track.op(args,op)
   while ops[i][1]!=b'ET':
    a,o=ops[i];pieces,p=track.op(a,o);pts+=p
    if o==b'Tf':size=max(size,float(a[1]))
    if pieces:
     rows.append({'offset':i-start,'pieces':pieces});text+=''.join(x['text'] for x in pieces)
     for piece in pieces:pts+=piece['points']
    if o in [b'T*',b'Td',b'TD'] and text:text+='\n'
    i+=1
   track.op(*ops[i]);i+=1
   if text.strip():
    assert pts;bb=bounds(pts);linked=any(x['annotation'] is not None for run in rows for x in run['pieces'])
    artifact=(bb[1]>770 or bb[3]<65) and not linked
    units.append({'kind':'text','start':start,'end':i,'ops':ops[start:i],'runs':rows,'text':norm(text),'box':bb,'size':size,'artifact':artifact})
  elif op==b'Do':
   _,pts=track.op(args,op)
   assert page_number==1,('Uncaptioned image outside the cover',page_number)
   units.append({'kind':'figure','start':i,'end':i+1,'ops':[ops[i]],'text':'Illustrative winding road beside a Swedish lake, with a car, forest and distant hills. Cover artwork, not a measured road layout.','box':bounds(pts)});i+=1
  else:track.op(args,op);i+=1
 return units,annotations,ops

def source_tables():
 result=[]
 for mod in ['M04','M05','M08']:
  path=PROD/'chapters'/mod/'chapter-source.md';s=path.read_text()
  for block in re.findall(r'(?m)^\|.*(?:\n\|.*)+',s):
   rows=[[clean_md(v.strip()) for v in line.strip('|').split('|')] for line in block.splitlines() if not line.startswith('|---')]
   result.append({'rows':rows,'path':str(path.relative_to(ROOT)),'header':rows[0]})
 return result

def run():
 source_sha=digest(SOURCE);approved=json.loads((PROD/'final-review/approval-record.json').read_text());assert approved['sha256']==source_sha
 reader=PdfReader(SOURCE);writer=PdfWriter();writer.clone_document_from_reader(reader);writer._header=b'%PDF-1.7'
 nav=json.loads((PROD/'assembly/navigation.json').read_text());module_titles={x['destination']:x['title'] for x in nav['contents'] if re.fullmatch('M\\d\\d',x['destination'])}
 tree=D({N('/Type'):N('/StructTreeRoot'),N('/K'):A()});tree_ref=writer._add_object(tree)
 def element(role,parent,page=None,title=None):
  ob=D({N('/Type'):N('/StructElem'),N('/S'):N('/'+role),N('/P'):parent,N('/K'):A()})
  if page is not None:ob[N('/Pg')]=page.indirect_reference
  if title:ob[N('/T')]=T(title)
  ref=writer._add_object(ob);return ref,ob
 doc_ref,doc=element('Document',tree_ref,title='KörkortGo — Swedish category B learning guide');tree['/K'].append(doc_ref)
 parts={};parent_nums=[];roles=collections.Counter();pages_report=[];link_key=len(writer.pages);unmatched=[];tables_count=0;total_spans=0;all_units=[];sources=source_tables();last_heading_level=0
 swedish_names={norm(c['official_name_sv']) for c in json.loads((PROD.parent/'sign-captions.json').read_text())['captions']}
 for pno,page in enumerate(writer.pages,1):
  part=next(x['part'] for x in nav['page_map'] if x['page']==pno)
  if part not in parts:
   ref,ob=element('Part',doc_ref,title=module_titles.get(part,'Opening pages' if part=='front' else 'Appendices and references'));doc['/K'].append(ref);parts[part]=(ref,ob)
  sect_ref,sect=element('Sect',parts[part][0],page,title='Page '+str(pno));parts[part][1]['/K'].append(sect_ref)
  page[N('/StructParents')]=I(pno-1);page[N('/Tabs')]=N('/S')
  units,annotations,ops=discover(page,pno);paragraphs={};unit_parents={};containers=[];table_members=set();last_list=None
  text_units=[u for u in units if u['kind']=='text' and not u['artifact']]
  # Ruled reference tables are authored with fixed row-major cell paragraphs.
  expected=[]
  for src in sources:
   starts=[i for i,u in enumerate(text_units) if norm(u['text'])==norm(src['header'][0])]
   for start in starts:
    flat=[v for row in src['rows'] for v in row];candidate=text_units[start:start+len(flat)]
    if len(candidate)==len(flat) and all(norm(u['text'])==norm(v) for u,v in zip(candidate,flat)):expected.append((candidate,src['rows'],src['path']))
  if pno in [348,349,*range(536,543)]:
   candidates=[u for u in text_units if u['size']<=10.1 and u['box'][1]>65]
   # Exclude introductions; exact header identifies the table cell sequence.
   header='Study group' if pno in [348,349] else 'Swedish term'
   starts=[i for i,u in enumerate(candidates) if norm(u['text']).lower().startswith(header.lower())]
   assert len(starts)==1,(pno,'table header not found',[u['text'] for u in candidates[:5]])
   cells=candidates[starts[0]:];assert len(cells)%3==0,(pno,len(cells))
   expected.append((cells,[['']*3 for _ in range(len(cells)//3)],'reference/reference-source.md'))
  for cells,rows,source_path in expected:
   tab_ref,tab=element('Table',sect_ref,page);tables_count+=1;roles['Table']+=1
   containers.append({'ref':tab_ref,'box':bounds([xy for u in cells for xy in box_points(u['box'])])})
   at=0
   for rownum,row in enumerate(rows):
    tr_ref,tr=element('TR',tab_ref,page);tab['/K'].append(tr_ref);roles['TR']+=1
    for colnum,_ in enumerate(row):
     u=cells[at];at+=1;table_members.add(id(u));role='TH' if rownum==0 or colnum==0 else 'TD'
     cell_ref,cell=element(role,tr_ref,page);tr['/K'].append(cell_ref);roles[role]+=1
     if role=='TH':cell[N('/A')]=D({N('/O'):N('/Table'),N('/Scope'):N('/Column' if rownum==0 else '/Row')})
     if pno>=536 and pno<=542 and colnum==0 and rownum:cell[N('/Lang')]=T('sv-SE')
     unit_parents[id(u)]=(cell_ref,cell)
  for u in units:
   if u['kind']=='text' and u['artifact']:continue
   if id(u) in table_members:continue
   if u['kind']=='figure':role='Figure'
   elif pno==1 and u['size']>=30:role='H1'
   elif u['size']>=24:
    role='H2' if part=='front' or u['text'] in module_titles.values() or pno in [345,347,536,543,545] else 'H3'
   elif u['size']>=16:role='H3' if part=='front' else 'H4'
   else:role='P'
   if role.startswith('H'):
    level=min(int(role[1:]),last_heading_level+1);last_heading_level=level;role='H'+str(level)
   numbered=re.match(r'^(\d+)[.)]\s',u['text']) if role=='P' else None
   if numbered:
    ordinal=int(numbered[1])
    if last_list and last_list['ordinal']+1==ordinal and abs(last_list['box'][0]-u['box'][0])<3:
     list_ref,list_ob=last_list['owner'];last_list['container']['box']=bounds(box_points(last_list['container']['box'])+box_points(u['box']))
    else:
     list_ref,list_ob=element('L',sect_ref,page);list_ob[N('/A')]=D({N('/O'):N('/List'),N('/ListNumbering'):N('/Decimal')});roles['L']+=1
     entry={'ref':list_ref,'box':u['box']};containers.append(entry);last_list={'owner':(list_ref,list_ob),'container':entry,'box':u['box']}
    li_ref,li=element('LI',list_ref,page);list_ob['/K'].append(li_ref);body_ref,body=element('LBody',li_ref,page);li['/K'].append(body_ref)
    ref,ob=element('P',body_ref,page);body['/K'].append(ref);roles['LI']+=1;roles['LBody']+=1;roles['P']+=1;last_list['ordinal']=ordinal
   else:
    last_list=None;ref,ob=element(role,sect_ref,page);roles[role]+=1;containers.append({'ref':ref,'box':u['box']})
   if norm(u['text']) in swedish_names:ob[N('/Lang')]=T('sv-SE')
   if role=='Figure':ob[N('/Alt')]=T(u['text'])
   unit_parents[id(u)]=(ref,ob)
  # Sort full paragraph/card blocks by actual placement, not merged stream order.
  containers.sort(key=lambda c:(-round(c['box'][3],2),round(c['box'][0],2)))
  sect['/K'].extend(c['ref'] for c in containers)
  mcid_refs=[];links={};link_units={};new=[];cursor=0
  def add_mark(role,owner,text=None):
   nonlocal total_spans
   mid=len(mcid_refs);mcid_refs.append(owner[0]);owner[1]['/K'].append(I(mid));prop=D({N('/MCID'):I(mid)})
   if text is not None:prop[N('/ActualText')]=T(text)
   total_spans+=1;return ([N('/'+role),prop],b'BDC')
  def artifact(segment):
   if segment:new.append(([N('/Artifact')],b'BMC'));new.extend(segment);new.append(([],b'EMC'))
  for u in units:
   artifact(ops[cursor:u['start']]);cursor=u['end']
   if u['kind']=='text' and u['artifact']:artifact(u['ops']);continue
   parent=unit_parents[id(u)]
   def emit_piece(piece):
    if not piece['text']:
     artifact([([ByteStringObject(piece['bytes'])],b'Tj')]);return
    ai=piece['annotation']
    if ai is not None:
     if ai not in links:
      ref,ob=element('Link',parent[0],page);parent[1]['/K'].append(ref);links[ai]=(ref,ob);roles['Link']+=1
     owner=links[ai];previous=str(owner[1].get('/Alt',''));separator=' ' if previous and link_units.get(ai)!=id(u) and not previous.endswith(' ') and not piece['text'].startswith(' ') else '';owner[1][N('/Alt')]=T(previous+separator+piece['text']);link_units[ai]=id(u)
     new.append(add_mark('Link',owner,piece['text']))
    else:
     ref,ob=element('Span',parent[0],page);parent[1]['/K'].append(ref);roles['Span']+=1;new.append(add_mark('Span',(ref,ob),piece['text']))
    new.append(([ByteStringObject(piece['bytes'])],b'Tj'));new.append(([],b'EMC'))
   runs={run['offset']:run['pieces'] for run in u.get('runs',[])}
   if u['kind']=='figure':
    segment=u['ops'];lo=1 if segment[0][1]==b'BDC' else 0;hi=len(segment)-1 if lo else len(segment)
    new.append(add_mark('Figure',parent));opened=True
    for offset in range(lo,hi):
     if offset in runs and any(x['annotation'] is not None for x in runs[offset]):
      new.append(([],b'EMC'));opened=False
      for piece in runs[offset]:emit_piece(piece)
      new.append(add_mark('Figure',parent));opened=True
     elif segment[offset][1] not in [b'BMC',b'BDC',b'EMC']:new.append(segment[offset])
    if opened:new.append(([],b'EMC'))
    continue
   buffer=[]
   for offset,(args,op) in enumerate(u['ops']):
    if offset not in runs:buffer.append((args,op));continue
    artifact(buffer);buffer=[]
    for piece in runs[offset]:emit_piece(piece)
   artifact(buffer)
  artifact(ops[cursor:])
  # Associate annotations with the actual marked link text (and duplicate regions).
  for a in annotations:
   ai=a['index'];owner=links.get(ai)
   if owner is None:
    duplicate=next((links[b['index']] for b in annotations if b['index'] in links and min(b['rect'][2],a['rect'][2])>max(b['rect'][0],a['rect'][0]) and min(b['rect'][3],a['rect'][3])>max(b['rect'][1],a['rect'][1]) and b['object'].get('/A')==a['object'].get('/A') and b['object'].get('/Dest')==a['object'].get('/Dest')),None)
    owner=duplicate
   if owner is None:unmatched.append({'page':pno,'annotation':ai,'rect':a['rect']});continue
   ann=a['object'];ann[N('/StructParent')]=I(link_key);ann[N('/Contents')]=T(norm(str(owner[1]['/Alt'])));ann[N('/F')]=I(int(ann.get('/F',0))|4)
   owner[1]['/K'].append(D({N('/Type'):N('/OBJR'),N('/Obj'):a['ref'],N('/Pg'):page.indirect_reference}));parent_nums.append((link_key,owner[0]));link_key+=1
  parent_nums.append((pno-1,A(mcid_refs)));stream=DecodedStreamObject();from pypdf.generic import ContentStream
  replacement=ContentStream(None,writer);replacement.operations=new;stream.set_data(replacement.get_data());page[N('/Contents')]=writer._add_object(stream.flate_encode())
  pages_report.append({'page':pno,'part':part,'text_blocks':sum(u['kind']=='text' and not u['artifact'] for u in units),'figures':sum(u['kind']=='figure' for u in units),'mcids':len(mcid_refs),'annotations':len(annotations),'tables':len(expected)})
  all_units.append({'page':pno,'blocks':[{'kind':u['kind'],'text':u['text'],'box':u['box'],'size':u.get('size'),'artifact':u.get('artifact',False)} for u in units]})
  if pno%100==0:print('Tagged',pno,'pages',flush=True)
 assert not unmatched,('Unmatched link annotations',unmatched[:20],len(unmatched))
 nums=A()
 for key,value in sorted(parent_nums):nums.extend([I(key),value])
 pt=writer._add_object(D({N('/Nums'):nums}));tree[N('/ParentTree')]=pt;tree[N('/ParentTreeNextKey')]=I(link_key)
 writer.root_object[N('/StructTreeRoot')]=tree_ref;writer.root_object[N('/MarkInfo')]=D({N('/Marked'):B(True)});writer.root_object[N('/Lang')]=T('en-GB');writer.root_object[N('/ViewerPreferences')]=D({N('/DisplayDocTitle'):B(True)})
 xmp=f'''<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:pdfuaid="http://www.aiim.org/pdfua/ns/id/"><dc:title><rdf:Alt><rdf:li xml:lang="x-default">KörkortGo — Swedish category B learning guide</rdf:li></rdf:Alt></dc:title><dc:language><rdf:Bag><rdf:li>en-GB</rdf:li></rdf:Bag></dc:language><pdfuaid:part>1</pdfuaid:part></rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>'''
 metadata=DecodedStreamObject();metadata.set_data(xmp.encode('utf-8'));metadata[N('/Type')]=N('/Metadata');metadata[N('/Subtype')]=N('/XML');writer.root_object[N('/Metadata')]=writer._add_object(metadata)
 writer.add_metadata({'/Title':'KörkortGo | Swedish category B learning guide','/Author':'KörkortGo','/Subject':'Tagged screen-review candidate; validate before acceptance','/CreationDate':'D:20261014000000Z','/ModDate':'D:20261014000000Z'})
 temporary=TARGET.with_suffix('.building.pdf')
 with temporary.open('wb') as f:writer.write(f)
 temporary.replace(TARGET)
 shutil.copyfile(TARGET,ROOT/'output/pdf'/TARGET.name)
 report={'created_on':'2026-10-14','source_path':str(SOURCE.relative_to(ROOT)),'source_sha256':source_sha,'tagged_path':str(TARGET.relative_to(ROOT)),'tagged_sha256':digest(TARGET),'pages':len(writer.pages),'roles':dict(roles),'total_mcids':total_spans,'tables':tables_count,'annotation_parent_entries':link_key-len(writer.pages),'unmatched_links':unmatched,'pages_report':pages_report,'status':'created_pending_independent_validation_and_render_review'}
 (HERE/'tagging-manifest.json').write_text(json.dumps(report,indent=2)+'\n');(HERE/'semantic-blocks.json').write_text(json.dumps(all_units,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in report.items() if k!='pages_report'},flush=True)
if __name__=='__main__':run()
