"""Rebuild the bounded, unscored compiler fixture from retained approved source records."""
from pathlib import Path
import copy
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools'))
from compile_curriculum import manifest_digest
HERE=Path(__file__).resolve().parent
OUT=HERE/'fixture'

def read(p):return json.loads((ROOT/p).read_text())
def file(p):return {'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}
def origin(p,locator):return {'file':file(p),'locator':locator,'evidence_ids':[],'pdf_evidence_page':None}
def text(v):return [{'type':'text','text':v}]
def block(id,loc,payload):return {'metadata':{'id':id,'origin':loc,'source_uses':[],'related_content':[]},'payload':payload}
registry=read('docs/curriculum/app-migration/curriculum-map.json')
qmap=read('docs/curriculum/app-migration/question-map.json')
preview=read('docs/curriculum/app-migration/preview-content.json')
reader=read('docs/curriculum/app-design/8d/content-bindings-v1.json')
check=read('docs/curriculum/app-design/8e/content-bindings-v2.json')
module=next(x for x in registry['modules'] if x['id']=='M03')
chapter='docs/curriculum/pdf-production/chapters/M03/chapter-source.md'
source_text=(ROOT/chapter).read_text()
version=qmap['questions'][0]['content_version']
release={'content_version':version,'pdf':{'path':registry['release_binding']['path'],'sha256':registry['release_binding']['sha256']}}
nodes={x['id']:x for x in registry['curriculum_nodes']}
docs=[]
for index,id in enumerate(['M03',*module['lesson_ids'],'M03-R']):
 n=nodes[id]
 heading=n['source_location']['heading']
 section=source_text.split(heading,1)[1].split('\n### ',1)[0].strip()
 first=section.split('\n\n')[0]
 body=[block(id+'/fixture-opening',origin(chapter,'heading:'+heading),{'type':'paragraph','text':text(first),'role':'explanation'})]
 docs.append({'id':id,'kind':{'module':'module_introduction'}.get(n['kind'],n['kind']),'module_id':None if id=='M03' else 'M03','title':n['title'],'order':n['order'],'objectives':[],'body_blocks':body,'answer_blocks':[],'source_ids':[],'asset_bindings':[],'related_content':[],'content_version':version,'revision':'fixture-r1','origin':origin(chapter,'heading:'+heading)})
lesson=docs[2]
loc=origin('docs/curriculum/app-design/8d/content-bindings-v1.json','json:/requirements_opening')
lesson['body_blocks'].append(block('M03-L02/fixture-requirement',loc,{'type':'paragraph','text':text(reader['requirements_opening']),'role':'requirement'}))
checkloc=origin('docs/curriculum/app-design/8e/content-bindings-v2.json','json:/question')
lesson['body_blocks'].append(block('M03-L02/fixture-check',checkloc,{'type':'knowledge_check','prompts':[block('M03-L02/fixture-check/prompt',checkloc,{'type':'paragraph','text':text(check['question']),'role':'explanation'})],'answer_id':'M03-L02/fixture-answer'}))
lesson['answer_blocks']=[{'metadata':{'id':'M03-L02/fixture-answer','origin':origin('docs/curriculum/app-design/8e/content-bindings-v2.json','json:/answer'),'source_uses':[],'related_content':[]},'visibility':'after_deliberate_reveal','blocks':[block('M03-L02/fixture-answer/text',origin('docs/curriculum/app-design/8e/content-bindings-v2.json','json:/answer'),{'type':'paragraph','text':text(check['answer']),'role':'explanation'})]}]
sign=preview['sign_reference'];entry=sign['entry'];cap=sign['caption'];asset=entry['asset']
asset_id=asset['source_asset_id']
sign_origin=origin('docs/curriculum/app-migration/preview-content.json','json:/sign_reference')
review={'record':origin('docs/curriculum/sign-captions.json','json:/captions/'+str(next(i for i,c in enumerate(read('docs/curriculum/sign-captions.json')['captions']) if c['code']=='B1'))),'reviewed_on':cap['reviewed_on']}
art={'id':asset_id,'kind':'official_sign','code_or_illustration_id':'B1','variant':cap['variant_description_en'],'original':{'path':asset['path'],'sha256':asset['sha256']},'bundled':{'path':asset['path'],'sha256':asset['sha256']},'caption_id':cap['caption_id'],'study_alt_text':cap['alt_text_en'],'translation_status':'editorial_english','reuse':[{'evidence':origin('docs/curriculum/sign-reuse.md','whole-file'),'conditions':'Retain the verified reuse conditions and official artwork unchanged.','credit':'Transportstyrelsen'}],'rendering':{'preserve_geometry_and_colours':True,'contain_without_crop':True,'maximum_print_size_mm':{'width':str(asset['max_size_mm_at_300ppi'][0]),'height':str(asset['max_size_mm_at_300ppi'][1])},'notes':[asset['reason'],'Fixture binds the retained source file; it does not deliver an app resource or prove legibility.']},'approval':[review]}
reference_urls=[qmap['source_registry'][0]['url'],*[s['url'] for s in cap['sources']]]
refs=[]
for url in reference_urls:
 record=next(x for x in qmap['source_registry'] if x['url']==url)
 if any(r['id']==record['id'] for r in refs):continue
 if url==reference_urls[0]:title,publisher,classification='Traffic Regulation (1998:1276)','Swedish Government; published by Sveriges riksdag','swedish_legislation'
 elif 'riksdagen' in url:title,publisher,classification='Road Signs Regulation (2007:90)','Swedish Government; published by Sveriges riksdag','swedish_legislation'
 else:title,publisher,classification=cap['official_name_sv'],'Transportstyrelsen','swedish_authority_guidance'
 ev=next((e for e in record['source_checks'] if 'M03/' in e['path']),None)
 if ev:
  evloc=origin(ev['path'],'json:'+ev['json_pointer']);data=ev['record']
 else:
  evloc=sign_origin;data=next(s for s in cap['sources'] if s['url']==url)
 refs.append({'id':record['id'],'title':title,'publisher':publisher,'url':url,'classifications':[classification],'classification_note':record['classification'],'editorial_inference':False,'original_evidence_ids':[data.get('source_id',data.get('alias','traffic-law'))],'evidence':[{'origin':evloc,'dates':{'checked_on':data.get('checked_on',data.get('reviewed_on')),'retrieved_on':data.get('retrieved_on'),'published_on':None},'scope':data.get('locator','Retained M03 passage-specific check'),'finding':data.get('finding',data.get('locator','Official illustration and description')),'limitations':['Stored evidence only; no new source-currency verification.']}]})
source_nodes=[]
for id in ['source-traffic-law','source-sign-law']:
 n=next(x for x in registry['source_destinations'] if x['id']==id)
 url=n.get('scoped_urls',{}).get('M03',n['url']);ref=next(r for r in refs if r['url']==url)
 source_nodes.append({'id':id,'original_alias':n['alias'],'title':ref['title'],'scoped_urls':[{'scope_id':'M03','reference_id':ref['id']}],'origin':origin('docs/curriculum/app-migration/curriculum-map.json','json:/source_destinations/'+str(registry['source_destinations'].index(n)))})
def use(id):
 src=next(x for x in source_nodes if x['id']==id)
 return {'reference_id':src['scoped_urls'][0]['reference_id'],'source_id':id,'scope_id':'M03','locator':'Retained approved M03 passage and its source evidence.','editorial_inference':False}
lesson['source_ids']=['source-traffic-law','source-sign-law']
lesson['body_blocks'][1]['metadata']['source_uses']=[use('source-traffic-law')]
lesson['body_blocks'][2]['metadata']['source_uses']=[use('source-sign-law')]
sign_entry={'id':'sign-B1','code':'B1','official_name_sv':cap['official_name_sv'],'english_label':cap['label_en'],'caption_id':cap['caption_id'],'caption':text(cap['teaching_caption_en']),'asset_id':asset_id,'translation_status':'editorial_english','source_uses':[use('source-sign-law')],'limitations':[],'origin':sign_origin}
docs[1]['asset_bindings']=[asset_id]
docs[1]['body_blocks'].append(block('M03-L01/fixture-B1',sign_origin,{'type':'image','asset_id':asset_id,'caption':text(cap['teaching_caption_en'])}))
# Preserve a real source table as a structured table, not a generated approximation.
lines=source_text.splitlines();start=next(i for i,l in enumerate(lines) if l.startswith('| Family |'))
table_lines=[]
for line in lines[start:]:
 if not line.startswith('|'):break
 table_lines.append(line)
cells=lambda line:[text(c.strip()) for c in line.strip('|').split('|')]
docs[1]['body_blocks'].append(block('M03-L01/fixture-families',origin(chapter,f'line:{start+1}-{start+len(table_lines)}'),{'type':'table','caption':None,'columns':[{'heading':t} for t in cells(table_lines[0])],'rows':[{'cells':cells(l)} for l in table_lines[2:]]}))
qold=read('content/questions.json')[0];qorigin=origin('content/questions.json','json:/0')
options=[{'id':qold['id']+'-option-'+str(i+1),'text':text(o['text']),'image':None} for i,o in enumerate(qold['options'])]
question={'key':{'question_id':qold['id'],'revision':'retained-fixture-r1'},'concept_id':qold['concept'],'category':qold['category'].lower(),'prompt':text(qold['prompt']),'image':None,'options':options,'feedback':{'target_sign_code':None,'english_label':None,'correct_option_id':options[qold['correct']]['id'],'explanation':text(qold['explanation']),'option_feedback':[{'option_id':o['id'],'explanation':text(old['explanation']),'sign_code':None,'english_label':None,'source_uses':[use('source-traffic-law')]} for o,old in zip(options,qold['options'])]},'relationship':{'primary_lesson_id':'M03-L02','related_lesson_ids':[],'reference_ids':[],'source_ids':['source-traffic-law'],'source_uses':[use('source-traffic-law')],'disposition':'retain','content_version':version},'acceptance':{'eligibility':'unreviewed','content_review':None,'description_reviews':[],'delivery_proof':[],'open_holds':[]},'origin':qorigin}
group={'id':'RB02','title':nodes['RB02']['title'],'order':nodes['RB02']['order'],'body_blocks':[],'entry_ids':['sign-B1'],'origin':origin('docs/curriculum/app-migration/curriculum-map.json','json:/curriculum_nodes/'+str(registry['curriculum_nodes'].index(nodes['RB02']))),'revision':'fixture-r1'}
# Only imported IDs are emitted; this subset is expressly not a complete curriculum.
curriculum={'schema_version':1,'source_curriculum':release,'modules':[module],'documents':docs,'reference_groups':[group],'anchors':[],'sign_entries':[sign_entry],'assets':[art],'reading_order':['M03',*module['lesson_ids'],'M03-R'],'lesson_category_tags':{}}
# Tags use the exact existing record format.
tags=read('docs/curriculum/app-migration/link-and-progress-map.json')['lesson_category_tags']
for id in module['lesson_ids']:
 rec=next(x for x in tags if x['lesson_id']==id)
 curriculum['lesson_category_tags'][id]=sorted(x.lower() for x in rec['category_ids'])
payloads={'curriculum':curriculum,'questions':{'schema_version':1,'questions':[question]},'sources':{'schema_version':1,'destinations':source_nodes,'references':refs},'legacy_aliases':{'schema_version':1,'aliases':[{'lookup':{'type':'question','question_id':'situation-001'},'outcome':{'type':'content','target':{'content_id':'M03-L02','block_id':None}},'origin':origin('docs/curriculum/app-migration/question-map.json','json:/questions/0')}],'tombstones':[]}}
for key,value in payloads.items():
 (OUT/(key+'.json')).write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
inputs=['docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json','docs/curriculum/app-migration/link-and-progress-map.json','docs/curriculum/app-migration/curriculum-map.json','docs/curriculum/app-migration/baseline.json','docs/curriculum/app-migration/question-actions.json','docs/curriculum/app-migration/question-map.json','composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt','composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','tools/build_content.py','tools/content_schema.py','tools/compile_curriculum.py','docs/curriculum/app-migration/implementation-evidence/9A2/content-contract.md']
manifest={'schema_version':1,'identity':{'content_version':'fixture-9A3-unscored','manifest_sha256':'0'*64},'source_curriculum':release,'inputs':[file(p) for p in inputs],'payloads':[{'kind':key,'file':file(str((OUT/(key+'.json')).relative_to(ROOT)))} for key in payloads]+[{'kind':'asset','file':art['bundled']}],'canonical_revisions':[{'id':r['id'],'revision':r.get('revision','fixture-r1')} for r in [*docs,group,sign_entry,*source_nodes]],'question_revisions':[{'key':question['key'],'eligibility':'unreviewed'}],'source_bindings':[dict(source_id=s['id'],**b) for s in source_nodes for b in s['scoped_urls']],'asset_bindings':[{'id':asset_id,'file':art['bundled']}]}
manifest['identity']['manifest_sha256']=manifest_digest(manifest)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print('Fixture prepared:',manifest['identity']['manifest_sha256'])
