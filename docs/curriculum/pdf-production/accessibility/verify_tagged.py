"""Verify the repaired tag tree and invariant curriculum/navigation contents."""
from pathlib import Path
import hashlib,json,collections,xml.etree.ElementTree as ET
from pypdf import PdfReader
from pypdf.generic import NumberObject
HERE=Path(__file__).resolve().parent;PROD=HERE.parent
src=PdfReader(PROD/'korkortgo-curriculum-review.pdf');pdf=PROD/'korkortgo-curriculum-tagged.pdf';tag=PdfReader(pdf)
assert len(src.pages)==len(tag.pages)==578
assert src.page_labels==tag.page_labels
assert set(src.named_destinations)==set(tag.named_destinations)
for k in src.named_destinations:assert src.get_destination_page_number(src.named_destinations[k])==tag.get_destination_page_number(tag.named_destinations[k]),k
root=tag.trailer['/Root'];assert root['/MarkInfo']['/Marked'] and root['/Lang']=='en-GB';assert root['/ViewerPreferences']['/DisplayDocTitle']
tree=root['/StructTreeRoot'].get_object();nums=tree['/ParentTree'].get_object()['/Nums'];parents={int(nums[i]):nums[i+1] for i in range(0,len(nums),2)}
roles=collections.Counter();visited=set();actual_by_page={};bad=[]
def walk(ref,parent=None):
 ob=ref.get_object();assert ob.indirect_reference.idnum not in visited,('Repeated/cyclic structure child',ob.indirect_reference.idnum);visited.add(ob.indirect_reference.idnum)
 assert ob['/Type']=='/StructElem';assert ob['/P'].indirect_reference==parent
 role=str(ob['/S']);roles[role]+=1
 if role=='/Figure':assert ob.get('/Alt')
 if role=='/TH':assert ob['/A']['/Scope'] in ['/Row','/Column']
 if role=='/L':assert all(x.get_object()['/S']=='/LI' for x in ob['/K'])
 if role=='/Table':assert all(x.get_object()['/S']=='/TR' for x in ob['/K'])
 for child in ob['/K']:
  if isinstance(child,NumberObject):
   page=ob['/Pg'].get_object();key=int(page['/StructParents']);mid=int(child);assert parents[key][mid].indirect_reference==ob.indirect_reference
  elif isinstance(child.get_object(),dict) and child.get_object().get('/Type')=='/OBJR':
   obj=child['/Obj'].get_object();assert parents[int(obj['/StructParent'])].indirect_reference==ob.indirect_reference;assert role=='/Link'
  else:walk(child,ob.indirect_reference)
for x in tree['/K']:walk(x,tree.indirect_reference)
assert roles['/Table']==13 and roles['/Figure']==815 and roles['/LI']==14
for i,(a,b) in enumerate(zip(src.pages,tag.pages)):
 assert b['/Tabs']=='/S' and int(b['/StructParents'])==i
 assert len(a.get('/Annots',[]))==len(b.get('/Annots',[]))
 for aa,bb in zip(a.get('/Annots',[]),b.get('/Annots',[])):
  x=aa.get_object();y=bb.get_object();assert x['/Rect']==y['/Rect'];assert x.get('/A')==y.get('/A');assert x.get('/Dest')==y.get('/Dest');assert '/StructParent' in y and y.get('/Contents')
 # Each page's meaningful MCIDs are unique, consecutive and resolve into the parent tree.
 mids=[];depth=0
 for args,op in b.get_contents().operations:
  if op==b'BDC' and isinstance(args[1],dict) and '/MCID' in args[1]:mids.append(int(args[1]['/MCID']))
 assert mids==list(range(len(mids))),(i+1,'MCID order or duplicates')
 assert len(parents[i])==len(mids)
xml=ET.parse(HERE/'verapdf.xml');reports=[e for e in xml.iter() if e.tag.endswith('validationReport')];assert len(reports)==1 and reports[0].get('isCompliant')=='true'
current=hashlib.sha256(pdf.read_bytes()).hexdigest();manifest=json.loads((HERE/'tagging-manifest.json').read_text());assert manifest['tagged_sha256']==current
render=json.loads((HERE/'render-comparison.json').read_text());label=json.loads((HERE/'link-label-verification.json').read_text());assert render['pixel_identical_pages']==578 and not render['differences'];assert label['unchanged_page_streams']==578 and label['current_sha256']==current and label['previous_sha256']==render['tagged_sha256']
result={'checked_on':'2026-10-14','tagged_sha256':current,'pages':578,'structure_roles':dict(roles),'unique_structure_objects':len(visited),'page_parent_entries':578,'annotation_parent_entries':len(parents)-578,'unchanged_navigation_and_annotation_regions':True,'verapdf_version':'1.30.3','verapdf_profile':'PDF/UA-1','verapdf_machine_result':'passed','rendered_pages_identical':578,'text_paint_streams_unchanged_after_link_label_refinement':True,'status':'machine_and_fidelity_checks_passed','human_check_scope':'Representative reading order, headings, image descriptions, table rows/cells and link activation observed through macOS Preview accessibility API; see reader-review.md. No exhaustive VoiceOver listening claim.'}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='structure_roles'})
