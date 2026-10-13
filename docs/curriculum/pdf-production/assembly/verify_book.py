"""Verify assembly fidelity and exact global link targets, without modifying inputs."""
from build_book import *
import collections,subprocess
r=PdfReader(TARGET);nav=json.loads((OUT/'navigation.json').read_text());inputs=json.loads((OUT/'inputs.json').read_text());dest=nav['destinations']
total=sum(x['pages'] for x in inputs)
assert len(r.pages)==nav['pages']==total
ids={p.indirect_reference.idnum:i+1 for i,p in enumerate(r.pages)}
def target(a):
    d=a.get('/Dest') or a.get('/A',{}).get('/D')
    if d is None:return None
    if isinstance(d,str):return r.get_destination_page_number(r.named_destinations[d])+1
    return ids[d[0].idnum] if hasattr(d[0],'idnum') else int(d[0])+1
for key,num in dest.items():assert r.get_destination_page_number(r.named_destinations[key])+1==num,key
assert r.page_labels==[str(i) for i in range(1,total+1)]
assert len(set((p['part'],p['local_page']) for p in nav['page_map']))==total
body_pages=0;original_links=0;external=set();internal=0;fonts=set();minimum_qa_gap=999
norm=lambda t:re.sub(r'\s+',' ',t).strip()
for item in inputs:
    path=HERE/item['path'];assert digest(path)==item['sha256']
    src=PdfReader(path);oldids={p.indirect_reference.idnum:i for i,p in enumerate(src.pages)}
    for local,page in enumerate(src.pages):
        index=item['offset']+local;output=r.pages[index]
        if index!=3:
            if index:
                footer_free(page)
                from pypdf.generic import DecodedStreamObject
                stream=DecodedStreamObject();stream.set_data(page.get_contents().get_data());page[NameObject('/Contents')]=stream
            # Exact text sequence of every source page, excluding the deliberately replaced footer.
            expected=norm(page.extract_text());actual=norm(output.extract_text())
            assert actual.startswith(expected),(index+1,'source text differs')
            assert actual[len(expected):].strip()==('Contents Sources Previous page '+str(index+1)+(' Next page' if index<total-1 else '')) if index else actual==expected
            body_pages+=1
            for obj in page.get('/Annots',[]):
                a=obj.get_object();rect=[float(x) for x in a['/Rect']]
                if rect[3]<=23*mm:continue
                matches=[o.get_object() for o in output.get('/Annots',[]) if list(o.get_object()['/Rect'])==list(a['/Rect'])]
                if '/Dest' in a:
                    expected_target=item['offset']+oldids[a['/Dest'][0].idnum]+1
                    assert any(target(m)==expected_target for m in matches),(index+1,'original link target')
                elif '/A' in a:
                    assert any(m.get('/A',{}).get('/URI')==a['/A']['/URI'] for m in matches),(index+1,'external link')
                original_links+=1
    if item['id'].startswith('M'):
        q=json.loads((path.parent/'navigation.json').read_text())
        for key,num in q['questions'].items():
            ap=item['offset']+q['answers'][key];qp=item['offset']+num
            assert ap-qp>=2
            assert not (qp%2==0 and ap==qp+1)
            minimum_qa_gap=min(minimum_qa_gap,ap-qp)
for i,page in enumerate(r.pages):
    for obj in page.get('/Annots',[]):
        a=obj.get_object();t=target(a)
        if t is not None:assert 1<=t<=total;internal+=1
        elif '/A' in a:assert a['/A']['/S']=='/URI';external.add(str(a['/A']['/URI']))
    if i:
        ann=[a.get_object() for a in page['/Annots']]
        assert any(target(a)==4 and abs(float(a['/Rect'][0])-M)<.01 for a in ann)
        assert any(target(a)==dest['official-references'] and abs(float(a['/Rect'][0])-(M+50))<.01 for a in ann)
    for f in page['/Resources'].get('/Font',{}).values():
        f=f.get_object();assert f['/FontDescriptor'].get_object().get('/FontFile2');assert '/ToUnicode' in f;fonts.add(str(f['/BaseFont']))
for link in nav['cross_links']:
    assert any(target(a.get_object())==dest[link['target']] and all(abs(float(x)-float(y))<.001 for x,y in zip(a.get_object()['/Rect'],link['rect'])) for a in r.pages[link['page']-1]['/Annots'])
for row in nav['contents']:
    assert any(target(a.get_object())==row['page'] for a in r.pages[3]['/Annots'])
assert len([k for k in dest if re.fullmatch('M[0-9]{2}-L[0-9]{2}',k)])==40
assert len([k for k in dest if re.fullmatch('M[0-9]{2}-R',k)])==10
assert r.trailer['/Root']['/Lang']=='en-GB'
# H6 verifies the new teaching anchors and sign destinations, not final coverage.
h0=json.loads((ROOT/'question-book-review/remaining-gap-h0-sources.json').read_text())
assert digest(REPO/h0['baseline']['questions']['path'])==h0['baseline']['questions']['sha256']
assert digest(REPO/h0['baseline']['gaps']['path'])==h0['baseline']['gaps']['sha256']
new_anchors=['M03-L04-approximate-model','M03-L04-approximate-examples','M09-L02-fuel-arithmetic','M09-L02-fuel-rounding','commercial-teaching-references']
for key in new_anchors:assert key in dest
for sign in h0['signs']:assert 'sign-'+sign['code'] in dest
assert len([key for key in dest if key.startswith('sign-') and key not in ['sign-group-index','sign-group-index-2'] and not key.startswith('sign-family-index')])==400
for key,phrase in [('M03-L04-approximate-model','Rough reaction estimate'),('M03-L04-approximate-examples','27.8 m'),('M09-L02-fuel-arithmetic','Journey consumption'),('M09-L02-fuel-rounding','ties-to-even'),('commercial-teaching-references','commercial teaching source')]:
 assert phrase in r.pages[dest[key]-1].extract_text(),(key,phrase)
outline_text=[]
def walk_outline(items):
 for item in items:
  if isinstance(item,list):walk_outline(item)
  else:outline_text.append(item.title)
walk_outline(r.outline)
for label in ['Approximate stopping model','Stopping worked examples','Fuel consumption and savings','Exact values and rounding','Supplementary commercial teaching references']:
 assert label in outline_text,label
sha=digest(TARGET)
subprocess.run([sys.executable,str(OUT/'build_book.py')],check=True,capture_output=True)
assert digest(TARGET)==sha
assert digest(REPO/'output/pdf/korkortgo-curriculum-review.pdf')==sha
report={'status':'passed','pages':total,'chapters':10,'lessons':40,'self_assessments':10,'appendices':4,'source_pages_preserved':body_pages,'original_body_links_preserved':original_links,'internal_links':internal,'external_urls':len(external),'named_destinations':len(dest),'new_cross_links':len(nav['cross_links']),'embedded_fonts':sorted(fonts),'minimum_question_answer_page_gap':minimum_qa_gap,'reproducible':True,'sha256':sha,'visual_review':'../../question-book-review/remaining-gap-execution-plan.md, H6 execution record','h6':{'new_teaching_anchors':{key:dest[key] for key in new_anchors},'planned_sign_codes_verified':79,'question_bank_unchanged':True,'final_coverage_audit':'H7 not run'},'scope':'H6 assembly fidelity, folios, PDF labels, bookmarks and navigation. H7 full-question coverage and separate publication/accessibility work remain.'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
