"""9B1: deterministic, bounded import of approved opening text and reading metadata."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'docs/curriculum/app-migration/implementation-evidence/9B1'
SOURCE='docs/curriculum/manuscript.md'
PRODUCTION='docs/curriculum/pdf-production/build.py'
REGISTRY='docs/curriculum/app-migration/curriculum-map.json'
LINKS='docs/curriculum/app-migration/link-and-progress-map.json'
CURRICULUM=ROOT/'content/curriculum.json'
STATE=ROOT/'content/curriculum-import-state.json'


def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def file(path):return {'path':path,'sha256':sha(path)}
def origin(path,locator,page=None):return {'file':file(path),'locator':locator,'evidence_ids':[],'pdf_evidence_page':page}
def rich(text):
    # Approved front matter uses strong emphasis only; preserve it as structure.
    parts=[]
    for i,part in enumerate(re.split(r'\*\*(.*?)\*\*',text,flags=re.S)):
        if part:parts.append({'type':'strong','children':[{'type':'text','text':part}]} if i%2 else {'type':'text','text':part})
    return parts

def build():
    c=read(REGISTRY);links=read(LINKS)
    source=(ROOT/SOURCE).read_text();lines=source.splitlines()
    production=(ROOT/PRODUCTION).read_text()
    tree=ast.parse(production)
    literals=[node for node in ast.walk(tree) if isinstance(node,ast.Constant) and isinstance(node.value,str)]
    authority={row['path']:row['sha256'] for row in read('docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json')['input_manifest']}
    required=[SOURCE,PRODUCTION,REGISTRY,LINKS,*{row['source_location']['path'] for row in c['curriculum_nodes'] if row['kind'] in ('module','lesson','module_review')}]
    for path in required:
        if path not in authority or sha(path)!=authority[path]:raise ValueError(f'Approved input changed or not frozen: {path}')
    def production_origin(text,page):
        node=next((node for node in literals if node.value==text),None)
        if node is None:raise ValueError(f'Production literal missing: {text}')
        return origin(PRODUCTION,f'line:{node.lineno}-{node.end_lineno}',page)
    def source_origin(text,page):
        if source.count(text)!=1:raise ValueError('Opening passage must occur exactly once in manuscript')
        start=source.index(text);first=source[:start].count('\n')+1
        return origin(SOURCE,f'line:{first}-{first+text.count(chr(10))}',page)
    def block(id,payload,loc):return {'metadata':{'id':id,'origin':loc,'source_uses':[],'related_content':[]},'payload':payload}
    def paragraph(id,text,loc,role='explanation'):
        return block(id,{'type':'paragraph','text':rich(text),'role':role},loc)
    def heading(parent,id,text,level,page):
        return block(parent+'/'+id,{'type':'heading','level':level,'text':rich(text)},production_origin(text,page))
    release={'content_version':read('docs/curriculum/app-migration/question-map.json')['questions'][0]['content_version'],'pdf':{'path':c['release_binding']['path'],'sha256':c['release_binding']['sha256']}}
    def document(id,title,order,blocks,loc,kind='front_matter',module_id=None,revision='opening-9B1-v1'):
        return {'id':id,'kind':kind,'module_id':module_id,'title':title,'order':order,'objectives':[],'body_blocks':blocks,'answer_blocks':[],'source_ids':[],'asset_bindings':[],'related_content':[],'content_version':release['content_version'],'revision':revision,'origin':loc}
    cover=[]
    for i,text in enumerate(['KörkortGo','Swedish category B learning guide','A learning aid','2026 version']):
        loc=production_origin(text,1)
        cover.append(heading('cover','title',text,1,1) if i==0 else paragraph('cover/'+['subtitle','learning-aid','edition'][i-1],text,loc))
    docs=[document('cover','Cover',1,cover,production_origin('Cover',1))]
    intro=source.split('### Contents',1)[0]
    disclaimer=re.search(r'> \*\*(.*?)\*\*',intro).group(1)
    audience='This book is'+intro.split('\n\nThis book is',1)[1].split('\n\n',1)[0]
    paras=intro.split('### How to use the book\n\n',1)[1].strip().split('\n\n')
    if len(paras)!=5:raise ValueError('Expected the five approved study-guide paragraphs')
    body=[heading('introduction','title','Before you begin',1,2),
          paragraph('introduction/disclaimer',disclaimer,source_origin(disclaimer,2),'disclaimer'),
          paragraph('introduction/audience',audience,source_origin(audience,2)),
          heading('introduction','how-to-use','How to use this book',2,2)]
    for id,text in zip(['learning-sequence','study-method'],paras[:2]):
        body.append(paragraph('introduction/'+id,text,source_origin(text,2)))
    docs.append(document('introduction','Before you begin',2,body,production_origin('Before you begin',2)))
    body=[heading('study-guide','title','Read, reflect and practise',1,3)]
    for id,title,text in zip(['labels','references','current-guidance'],['Read the labels','Use the official references','Check current guidance'],paras[2:]):
        body.extend([heading('study-guide',id+'-heading',title,2,3),paragraph('study-guide/'+id,text,source_origin(text,3))])
    docs.append(document('study-guide','How to use this book',3,body,production_origin('How to use this book',3)))
    module_items=[]
    for i,module in enumerate(c['modules']):
        loc=origin(REGISTRY,f'json:/modules/{i}',4)
        text=[{'type':'link','label':rich(module['title']),'target':{'type':'internal','target':{'content_id':module['id'],'block_id':None}}}]
        module_items.append([block('contents/module-'+module['id'],{'type':'paragraph','text':text,'role':'explanation'},loc)])
    body=[heading('contents','title','Your learning journey',1,4),block('contents/modules',{'type':'list_items','ordered':True,'start':1,'items':module_items},origin(REGISTRY,'json:/modules',4)),heading('contents','appendices-heading','Keep these close',2,4)]
    appendices=[(i,node) for i,node in enumerate(c['curriculum_nodes']) if node['kind']=='appendix']
    appendix_items=[]
    for i,node in appendices:
        item=paragraph('contents/'+node['id'],node['title'],origin(REGISTRY,f'json:/curriculum_nodes/{i}',4))
        item['payload']['text'].insert(0,{'type':'text','text':node['id'][-1]+' '})
        appendix_items.append([item])
    body.append(block('contents/appendices',{'type':'list_items','ordered':False,'start':1,'items':appendix_items},origin(REGISTRY,'json:/curriculum_nodes',4)))
    body.append(paragraph('contents/source-heading','Sources and references',production_origin('Sources and references',4)))
    docs.append(document('contents','Contents',4,body,production_origin('Contents',4)))
    node_by_id={node['id']:node for node in c['curriculum_nodes']}
    pending=[]
    for id in links['reading_order']:
        node=node_by_id[id];loc=node['source_location'];actual=(ROOT/loc['path']).read_text().splitlines()
        if sha(loc['path'])!=loc['sha256'] or actual[loc['line']-1]!=loc['heading']:
            raise ValueError(f'Invalid production locator for {id}')
        docs.append(document(id,node['title'],node['order'],[],origin(loc['path'],f'line:{loc["line"]}',node['pdf_evidence_page']),{'module':'module_introduction'}.get(node['kind'],node['kind']),node.get('module_id'),revision='structure-9B1-v1'))
        module_id=node.get('module_id',id)
        owner='9B'+str(int(module_id[1:])+1)
        pending.append({'id':id,'status':'structure_only','body_owner':owner,'required_source_ids':node.get('source_destination_ids',[]),'asset_register':node.get('asset_binding_register'),'exact_title':node['title'],'origin':docs[-1]['origin']})
    tags={row['lesson_id']:sorted(value.lower() for value in row['category_ids']) for row in links['lesson_category_tags']}
    payload={'schema_version':1,'source_curriculum':release,'modules':c['modules'],'documents':docs,'reference_groups':[],'anchors':[],'sign_entries':[],'assets':[],'reading_order':links['reading_order'],'lesson_category_tags':tags}
    state={'step':'9B1','status':'opening_text_and_reading_structure_imported','production_ready':False,
           'content_payload':'content/curriculum.json','front_matter_ids':['cover','introduction','study-guide','contents'],
           'library_policy':{'top_level_card_ids':[m['id'] for m in c['modules']],'exclude_front_matter_ids':['cover','introduction','study-guide','contents'],'supporting_anchors_are_cards':False,'fabricated_completion':False},
           'opening_text':{'status':'imported','disclaimer_block_id':'introduction/disclaimer','exact_disclaimer':disclaimer,'origin_files':[file(SOURCE),file(PRODUCTION)]},
           'pending_reading_nodes':pending,
           'deferred':[
             {'id':'cover-artwork','owner':'9C4','source':file('docs/curriculum/pdf-design/5b/cover-opening-v4.png'),'status':'asset_not_imported','rule':'Retain approved book artwork/crop evidence; app presentation remains subject to its approved design.'},
             *[{'id':n['id'],'owner':'9B'+str(12+i),'status':'appendix_body_and_action_pending','retained_title':n['title']} for i,(_,n) in enumerate(appendices)],
             {'id':'official-references','owner':'9C1/9L8','status':'source_directory_action_pending','retained_label':'Sources and references'},
             {'id':'question-bank','owner':'9D–9J','status':'live_legacy_bank_unchanged; staging_assessments_empty'},
             {'id':'reference-groups-signs-sources-supporting-anchors','owner':'9B16/9B17/9C','status':'not imported in 9B1'}],
           'omitted_pdf_chrome':['running headers','printed folios','PDF Contents/Sources/Previous page/Next page controls'],
           'source_inputs':[file(path) for path in sorted(set(required))]}
    return payload,state


def encoded(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n'


def stage(payload):
    from compile_curriculum import manifest_digest, compile_files, ROOT_TYPES, AUTHORITY, MODEL_PATHS, REGISTRY, BASELINE, ACTIONS
    placeholders={'questions':{'schema_version':1,'questions':[]},'sources':{'schema_version':1,'destinations':[],'references':[]},'legacy_aliases':{'schema_version':1,'aliases':[],'tombstones':[]}}
    for key,value in placeholders.items():(EVIDENCE/(key+'.json')).write_text(encoded(value))
    inputs=[AUTHORITY,REGISTRY,BASELINE,ACTIONS,'docs/curriculum/app-migration/question-map.json',LINKS,*MODEL_PATHS,SOURCE,PRODUCTION,'tools/build_content.py','tools/content_schema.py','tools/compile_curriculum.py','tools/import_curriculum_opening.py','content/curriculum-import-state.json',str((EVIDENCE/'pdf-opening-text.json').relative_to(ROOT))]
    paths={'curriculum':CURRICULUM,**{key:EVIDENCE/(key+'.json') for key in placeholders}}
    m={'schema_version':1,'identity':{'content_version':'staging-9B1-opening-and-structure','manifest_sha256':'0'*64},'source_curriculum':payload['source_curriculum'],'inputs':[file(path) for path in inputs],'payloads':[{'kind':key,'file':file(str(path.relative_to(ROOT)))} for key,path in paths.items()],'canonical_revisions':[{'id':d['id'],'revision':d['revision']} for d in payload['documents']],'question_revisions':[],'source_bindings':[],'asset_bindings':[]}
    m['identity']['manifest_sha256']=manifest_digest(m)
    manifest=EVIDENCE/'staging-manifest.json';manifest.write_text(encoded(m))
    return compile_files(paths,manifest,EVIDENCE/'generated',EVIDENCE/'trace.json',profile='fixture',symbol='stagedCurriculum9B1')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true',help='Initialize the bounded payload and stage its Kotlin output.')
    mode.add_argument('--check',action='store_true',help='Compare opening/reading data without writing files.')
    args=parser.parse_args()
    try:
        payload,state=build()
        if args.check:
            if not CURRICULUM.is_file() or read(str(CURRICULUM.relative_to(ROOT)))!=payload or read(str(STATE.relative_to(ROOT)))!=state:raise ValueError('9B1 payload/state differ from the bounded source import')
            print('PASS: exact 9B1 opening and 60-node structure reproduce without writes.');return 0
        for path,value in [(CURRICULUM,payload),(STATE,state)]:
            if path.exists() and path.read_text()!=encoded(value):raise ValueError(f'Refusing to overwrite changed/accumulated imports: {path.relative_to(ROOT)}')
        CURRICULUM.write_text(encoded(payload));STATE.write_text(encoded(state))
        print(json.dumps(stage(payload),sort_keys=True))
        return 0
    except (ValueError,OSError) as exc:
        print(str(exc),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
