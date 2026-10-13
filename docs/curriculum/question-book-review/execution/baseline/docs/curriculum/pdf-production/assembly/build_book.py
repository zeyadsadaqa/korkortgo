"""6M: assemble verified parts, retaining page artwork and adding global navigation."""
from pathlib import Path
import sys, json, re, hashlib, io, shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build import *
import pdfplumber
from pypdf.generic import NameObject, TextStringObject, ArrayObject, NumberObject
from pypdf.annotations import Link
OUT=Path(__file__).resolve().parent
TARGET=OUT.parent/'korkortgo-curriculum-review.pdf'
MANIFEST=json.loads((HERE/'build-manifest.json').read_text())

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def footer_free(page):
    """Remove only complete text objects at the shared absolute footer baseline.
    Body text is placed in translated local frames; never flatten or mask page art.
    """
    stream=page.get_contents();ops=stream.operations;clean=[];i=0;removed=0
    while i<len(ops):
        if ops[i][1]==b'BT':
            j=i+1
            while ops[j][1]!=b'ET':j+=1
            block=ops[i:j+1]
            is_footer=any(op==b'Tm' and abs(float(a[5])-16*mm)<.01 and float(a[4])>=M-.01 for a,op in block)
            if is_footer:removed+=1
            else:clean.extend(block)
            i=j+1
        else:clean.append(ops[i]);i+=1
    stream.operations=clean;page[NameObject('/Contents')]=stream
    page[NameObject('/Annots')]=ArrayObject([a for a in page.get('/Annots',[]) if float(a.get_object()['/Rect'][3])>23*mm])
    return removed

def single_page(draw):
    buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=A4,invariant=1,initialFontName='Body');draw(c);c.showPage();c.save();buf.seek(0);return PdfReader(buf)

def run():
    parts=[{'id':'front','path':HERE/'front-matter.pdf','nav':json.loads((HERE/'navigation.json').read_text())['built']}]
    for ch in MANIFEST['chapters']:
        path=HERE/ch['pdf'];assert digest(path)==ch['sha256'],ch['id']
        nav=json.loads((path.parent/'navigation.json').read_text())
        parts.append({'id':ch['id'],'path':path,'nav':nav['destinations'],'qa':nav})
    path=HERE/'reference-material.pdf';assert digest(path)==MANIFEST['reference_material']['sha256']
    parts.append({'id':'reference','path':path,'nav':json.loads((HERE/'reference/navigation.json').read_text())['destinations']})
    dest={};page_map=[];offset=0
    for part in parts:
        part['reader']=PdfReader(part['path']);part['offset']=offset
        for key,local in part['nav'].items():
            assert key not in dest,key
            dest[key]=offset+local
        page_map.extend({'part':part['id'],'local_page':i+1,'page':offset+i+1} for i in range(len(part['reader'].pages)))
        offset+=len(part['reader'].pages)
    # Named source destinations connect the complete references to chapter reading.
    refs=dict(re.findall(r'^\[([^]]+)\]: (.+)$',(ROOT/'manuscript.md').read_text(),re.M))
    refpart=parts[-1]
    for alias,url in refs.items():
        candidates=[]
        for i,page in enumerate(refpart['reader'].pages):
            if refpart['offset']+i+1<dest['official-references']:continue
            if any(str(a.get_object().get('/A',{}).get('/URI',''))==url for a in page.get('/Annots',[])):candidates.append(refpart['offset']+i+1)
        assert candidates,alias
        dest['source-'+alias]=candidates[0]
    writer=PdfWriter()
    for part in parts:
        reader=part['reader']
        saved=[page.pop(NameObject('/Annots'),ArrayObject()) for page in reader.pages]
        writer.append(reader,import_outline=False)
        old_indices={page.indirect_reference.idnum:i for i,page in enumerate(reader.pages)}
        for local,annots in enumerate(saved):
            reader.pages[local][NameObject('/Annots')]=annots
            for obj in annots:
                a=obj.get_object();rect=[float(x) for x in a['/Rect']]
                if rect[3]<=23*mm:continue
                if '/A' in a and a['/A'].get('/S')=='/URI':
                    link=Link(rect=rect,url=str(a['/A']['/URI']))
                elif '/Dest' in a:
                    d=a['/Dest'];target=old_indices[d[0].idnum]
                    link=Link(rect=rect,target_page_index=part['offset']+target)
                else:raise AssertionError(('Unexpected annotation',a))
                writer.add_annotation(part['offset']+local,link)
    writer.root_object.pop(NameObject('/Names'),None);writer.root_object.pop(NameObject('/Outlines'),None)
    # Replace the provisional contents with the same approved template and actual folios.
    toc_rows=[]
    for i,ch in enumerate(MANIFEST['chapters'],1):toc_rows.append((f'{i:02d}',ch['title'],ch['id']))
    for a in MANIFEST['appendices']:toc_rows.append((a['id'][-1],a['title'],a['id']))
    toc_rows.append(('', 'Official references','official-references'))
    toc_rects=[]
    def contents(c):
        c.setFillColor(COLORS['paper']);c.rect(0,0,W,H,stroke=0,fill=1)
        c.setFillColor(COLORS['forest']);c.setFont('Body',10);c.drawString(M,H-20*mm,'KörkortGo · Contents')
        c.setStrokeColor(COLORS['gold']);c.setLineWidth(.5);c.line(M,H-23*mm,W-M,H-23*mm);c.line(M,23*mm,W-M,23*mm)
        y=H-34*mm
        f=paragraph('Your learning journey','heading');_,h=f.wrap(WIDTH,1000);f.drawOn(c,M,y-h);y-=h+18
        for j,(label,title,key) in enumerate(toc_rows):
            if j==10:
                y-=12;f=paragraph('Keep these close','subheading');_,h=f.wrap(WIDTH,1000);f.drawOn(c,M,y-h);y-=h+8
            f=paragraph(title);_,h=f.wrap(WIDTH-75,1000);row_h=max(29,h+10)
            c.setFillColor(COLORS['forest']);c.setFont('BodyBold',12);c.drawString(M,y-15,label)
            f.drawOn(c,M+27,y-h-5);c.setFont('Body',12);c.drawRightString(W-M,y-15,str(dest[key]))
            toc_rects.append((key,[M,y-row_h,W-M,y]));c.setStrokeColor(COLORS['gold']);c.line(M,y-row_h+2,W-M,y-row_h+2);y-=row_h
        assert y>30*mm,y
    toc=single_page(contents);writer.pages[3].replace_contents(toc.pages[0].get_contents())
    writer.pages[3][NameObject('/Resources')]=toc.pages[0]['/Resources'].clone(writer)
    writer.pages[3][NameObject('/Annots')]=ArrayObject()
    # Remove standalone footer text and links; add selectable continuous folios.
    removed={};footer_links=0
    for i,page in enumerate(writer.pages):
        if i==0:continue
        removed[str(i+1)]=footer_free(page)
        def footer(c):
            c.setFillColor(COLORS['forest']);c.setFont('Body',9)
            c.drawString(M,16*mm,'Contents');c.drawString(M+51,16*mm,'Sources')
            c.drawRightString(W/2-22,16*mm,'Previous page');c.drawCentredString(W/2,16*mm,str(i+1))
            if i+1<len(writer.pages):c.drawRightString(W-M,16*mm,'Next page')
        page.merge_page(single_page(footer).pages[0])
        for rect,target in [([M,14*mm,M+44,21*mm],3),([M+50,14*mm,M+89,21*mm],dest['official-references']-1),([W/2-88,14*mm,W/2-20,21*mm],i-1)]+([([W-M-55,14*mm,W-M,21*mm],i+1)] if i+1<len(writer.pages) else []):
            writer.add_annotation(i,Link(rect=rect,target_page_index=target));footer_links+=1
    for key,rect in toc_rects:writer.add_annotation(3,Link(rect=rect,target_page_index=dest[key]-1))
    # Attach links to printed lesson/review IDs and chapter sign captions, with exact text geometry.
    cache_path=OUT/'cross-link-candidates.json'
    cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
    fingerprints={str(p['path'].relative_to(HERE)):digest(p['path']) for p in parts}
    if cache.get('inputs')==fingerprints and '--refresh-navigation' not in sys.argv:
        added=cache['links']
        for link in added:writer.add_annotation(link['page']-1,Link(rect=link['rect'],target_page_index=dest[link['target']]-1))
    else:
        added=[]
        for part in parts[1:]:
            with pdfplumber.open(part['path']) as doc:
                for local,page in enumerate(doc.pages):
                    global_page=part['offset']+local+1
                    for word in page.extract_words():
                        token=word['text'].strip('.,;:()')
                        target=None
                        if re.fullmatch(r'M\d{2}-(?:L\d{2}|R)',token) and token in dest:target=token
                        elif part['id']!='reference' and 'sign-'+token in dest:target='sign-'+token
                        if not target or dest[target]==global_page or word['top']<25*mm or word['bottom']>H-25*mm:continue
                        rect=[word['x0'],H-word['bottom'],word['x1'],H-word['top']]
                        # Existing linked text retains its original reviewed action.
                        if any(float(a.get_object()['/Rect'][0])<=rect[0] and float(a.get_object()['/Rect'][2])>=rect[2] and float(a.get_object()['/Rect'][1])<=rect[1] and float(a.get_object()['/Rect'][3])>=rect[3] for a in writer.pages[global_page-1].get('/Annots',[])):continue
                        writer.add_annotation(global_page-1,Link(rect=rect,target_page_index=dest[target]-1));added.append({'page':global_page,'target':target,'rect':rect})
        cache_path.write_text(json.dumps({'inputs':fingerprints,'links':added},indent=2)+'\n')
    for key,num in dest.items():writer.add_named_destination(key,num-1)
    writer.add_outline_item('Cover',0);writer.add_outline_item('Before you begin',1);writer.add_outline_item('How to use this book',2);writer.add_outline_item('Contents',3)
    for ch in MANIFEST['chapters']:
        parent=writer.add_outline_item(ch['id']+' · '+ch['title'],dest[ch['id']]-1)
        for key in ch['lessons']+[ch['review'],ch['id']+'-answers',ch['id']+'-references']:
            writer.add_outline_item(key+(' · Answers' if key.endswith('-answers') else ' · Official references' if key.endswith('-references') else ''),dest[key]-1,parent=parent)
    parent=writer.add_outline_item('Appendices and sign reference',dest['reference-contents']-1)
    for a in MANIFEST['appendices']:
        child=writer.add_outline_item('Appendix '+a['id'][-1]+' · '+a['title'],dest[a['id']]-1,parent=parent)
        if a['id']=='appendix-B':
            for g in json.loads((ROOT/'sign-placement-map.json').read_text())['reference_groups']:writer.add_outline_item(g['group_id']+' · '+g['title'],dest[g['group_id']]-1,parent=child)
            writer.add_outline_item('Sign code and family lookup',dest['sign-family-index']-1,parent=child)
    writer.add_outline_item('Official references',dest['official-references']-1);writer.add_outline_item('Artwork and source credits',dest['artwork-credits']-1)
    writer.root_object[NameObject('/Lang')]=TextStringObject('en-GB');writer.set_page_label(0,len(writer.pages)-1,style='/D',start=1)
    writer.add_metadata({'/Title':'KörkortGo | Swedish category B learning guide','/Author':'KörkortGo','/Subject':'Complete curriculum review edition | A learning aid','/CreationDate':'D:20261007000000Z','/ModDate':'D:20261007000000Z'})
    with TARGET.open('wb') as f:writer.write(f)
    (OUT/'navigation.json').write_text(json.dumps({'pages':len(writer.pages),'destinations':dest,'page_map':page_map,'contents':[{'title':title,'destination':key,'page':dest[key]} for _,title,key in toc_rows],'cross_links':added,'footer_links':footer_links},ensure_ascii=False,indent=2)+'\n')
    (OUT/'inputs.json').write_text(json.dumps([{'id':p['id'],'path':str(p['path'].relative_to(HERE)),'sha256':digest(p['path']),'pages':len(p['reader'].pages),'offset':p['offset']} for p in parts],indent=2)+'\n')
    (OUT/'footer-replacement.json').write_text(json.dumps(removed,indent=2)+'\n')
    shutil.copyfile(TARGET,REPO/'output/pdf/korkortgo-curriculum-review.pdf')
    print('Built',len(writer.pages),'pages;',len(added),'cross-links;',len(dest),'destinations',flush=True)

if __name__=='__main__':run()
