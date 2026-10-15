"""9B3: import only approved M02 teaching, hidden answers and illustration windows."""
import argparse
import ast
import copy
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from import_curriculum_opening import ROOT, read, sha, file, origin, encoded, CURRICULUM, STATE, build as opening
from compile_curriculum import AUTHORITY, REGISTRY, BASELINE, ACTIONS, MODEL_PATHS, manifest_digest, compile_files

EVIDENCE=ROOT/'docs/curriculum/app-migration/implementation-evidence/9B3'
CHAPTER='docs/curriculum/pdf-production/chapters/M02/'
SOURCE=CHAPTER+'chapter-source.md'
BUILDER=CHAPTER+'build_chapter.py'
CHECKS=CHAPTER+'source-checks.json'
ART=CHAPTER+'illustrations.json'
LINKS='docs/curriculum/app-migration/link-and-progress-map.json'
QUESTION_MAP='docs/curriculum/app-migration/question-map.json'
IDS=['M02','M02-L01','M02-L02','M02-L03','M02-L04','M02-R']
# Authored IDs are assigned once; wording, pagination and text hashes do not define identity.
PARAGRAPH_IDS={
'M02-L01':['goal','safety-check','controls','braking-steering','vehicle-boundary','brake-circuits','abs','symptoms','symptom-table','fuse','worked-decision','knowledge-check','remember'],
'M02-L02':['goal','walkaround','tyre-requirements','lighting','steering-vibration','temporary-spare','practice-example','worked-decision','knowledge-check','remember'],
'M02-L03':['goal','restraint-requirements','child-exceptions','recommendations','airbags','head-restraints','rear-facing','crumple-zones','practice-example','worked-decision','knowledge-check','remember'],
'M02-L04':['goal','movement-requirements','observation','hill-starts','worked-decision','knowledge-check','remember'],
'M02-R':['scenario','review-check','reflection']}



def source_parts():
    text=(ROOT/SOURCE).read_text()
    body=text.split('\n[practical]:',1)[0].strip()
    parts=re.split(r'^### (M02-\S+) · (.+)\n',body,flags=re.M)
    sections={'M02':[parts[0].split('\n\n',1)[1].strip()]}
    for i in range(1,len(parts),3):sections[parts[i]]=parts[i+2].strip().split('\n\n')
    urls=dict(re.findall(r'^\[([^]]+)\]: (.+)$',text,re.M))
    return text,sections,urls


def sources(urls):
    registry=read(REGISTRY);known={r['alias']:(i,r) for i,r in enumerate(registry['source_destinations'])}
    references={r['url']:r for r in read(QUESTION_MAP)['source_registry']}
    checks=read(CHECKS);labels=dict((k,label) for label,k in reversed(re.findall(r'\[([^]]+)\]\[([^]]+)\]',(ROOT/SOURCE).read_text())))
    destinations=[];records=[];lookup={}
    for alias,url in urls.items():
        index,node=known[alias]
        local_records=[{'path':CHECKS,'json_pointer':f'/{group}/{i}','record':r} for group in ['sources','G2_sources'] for i,r in enumerate(checks[group]) if r['alias']==alias and r['url']==url]
        ref=references.get(url) or {'id':'REF-'+hashlib.sha256(url.encode()).hexdigest()[:16],'classification':'Curriculum-only source; exact 7B M02 URL and retained production source check.'}
        if node['scoped_urls']['M02']!=url:raise ValueError('Source scope differs from 7B: '+alias)
        if not local_records:raise ValueError('Missing M02 source evidence: '+alias)
        rec=local_records[-1]['record']
        classification=('foreign_public_authority' if alias in ['abs-driving','vehicle-faults','crumple-zones'] else
                        'manufacturer' if alias in ['abs-feedback','temporary-spare'] else
                        'research' if alias=='friction' else
                        'swedish_legislation' if alias in ['traffic-law','brake-circuits','brake-inspection','syllabus'] else 'swedish_authority_guidance')
        publisher=rec.get('publisher') or ('Sveriges riksdag' if alias=='traffic-law' else 'VTI; hosted by Transportstyrelsen' if alias=='friction' else 'Transportstyrelsen' if 'transportstyrelsen.se' in url else 'Trafikverket')
        lookup[alias]=(node['id'],ref['id'])
        destinations.append({'id':node['id'],'original_alias':alias,'title':labels[alias],
            'scoped_urls':[{'scope_id':'M02','reference_id':ref['id']}],
            'origin':origin(REGISTRY,f'json:/source_destinations/{index}')})
        records.append({'id':ref['id'],'title':rec.get('title',labels[alias]),'publisher':publisher,'url':url,
            'classifications':[classification], 'classification_note':ref['classification']+(' Hosted VTI research; physical friction principle, not legislation.' if alias=='friction' else ''),
            'editorial_inference':False,'original_evidence_ids':[e['record']['source_id'] for e in local_records if e['record'].get('source_id')],
            'evidence':[{'origin':origin(CHECKS,'json:'+e['json_pointer']),
                'dates':{'checked_on':checks['G2_checked_on'] if e['json_pointer'].startswith('/G2_sources/') else checks['checked_on'],'retrieved_on':e['record'].get('retrieved_on'),'published_on':None},
                'scope':'M02; '+e['record'].get('locator','chapter teaching scope'),
                'finding':e['record'].get('supports',e['record'].get('finding')),
                'limitations':[e['record'][k] for k in ['fallback_reason','scope_limits','version'] if e['record'].get(k)]} for e in local_records]})
    return {'schema_version':1,'destinations':destinations,'references':records},lookup


def rich(text,lookup):
    # Explicitly reject unhandled Markdown instead of dropping teaching or links.
    result=[];pattern=r'\*\*(.+?)\*\*|\[([^]]+)\]\[([^]]+)\]|\bM\d{2}-L\d{2}\b'
    offset=0
    for m in re.finditer(pattern,text):
        if m.start()>offset:result.append({'type':'text','text':text[offset:m.start()]})
        if m[1] is not None:result.append({'type':'strong','children':rich(m[1],lookup)})
        elif m[3] is not None:result.append({'type':'link','label':[{'type':'text','text':m[2]}],'target':{'type':'external_source','reference_id':lookup[m[3]][1]}})
        else:result.append({'type':'link','label':[{'type':'text','text':m[0]}],'target':{'type':'internal','target':{'content_id':m[0],'block_id':None}}})
        offset=m.end()
    if offset<len(text):result.append({'type':'text','text':text[offset:]})
    if any('**' in n.get('text','') or '][' in n.get('text','') for n in result):raise ValueError('Unhandled Markdown')
    return result


def build(payload,state):
    authority={r['path']:r['sha256'] for r in read(AUTHORITY)['input_manifest']}
    required=[SOURCE,BUILDER,CHECKS,ART,CHAPTER+'navigation.json',CHAPTER+'review.md',REGISTRY,QUESTION_MAP,LINKS]
    for path in required:
        if sha(path)!=authority.get(path):raise ValueError('Approved M02 input drift: '+path)
    text,sections,urls=source_parts();source_payload,lookup=sources(urls)
    pristine,_=opening();skeleton={d['id']:d for d in pristine['documents']}
    payload=copy.deepcopy(payload);state=copy.deepcopy(state);docs={d['id']:d for d in payload['documents']}
    tree=ast.parse((ROOT/BUILDER).read_text());literals=[n for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
    def prodloc(value):
        n=next(n for n in literals if n.value==value)
        return origin(BUILDER,f'line:{n.lineno}-{n.end_lineno}')
    def loc(value):
        if text.count(value)!=1:raise ValueError('Ambiguous source paragraph')
        start=text[:text.index(value)].count('\n')+1
        return origin(SOURCE,f'line:{start}-{start+value.count(chr(10))}')
    def block(id,payload,where,raw=''):
        uses=[{'reference_id':lookup[a][1],'source_id':lookup[a][0],'scope_id':'M02','locator':where['locator'],'editorial_inference':False} for a in dict.fromkeys(re.findall(r'\]\[([^]]+)\]',raw))]
        related=[{'content_id':i,'block_id':None} for i in dict.fromkeys(re.findall(r'\bM\d{2}-L\d{2}\b',raw))]
        return {'metadata':{'id':id,'origin':where,'source_uses':uses,'related_content':related},'payload':payload}
    def paragraph(id,raw,where,role='explanation'):
        return block(id,{'type':'paragraph','text':rich(raw,lookup),'role':role},where,raw)
    def heading(id,value):return block(id,{'type':'heading','level':2,'text':rich(value,lookup)},prodloc(value))
    art=read(ART)['assets'];assets=[]
    def image(id):
        a=art[id];path='docs/curriculum/pdf-design/gap-resolution/'+a['file']
        if sha(path)!=a['sha256'] or sha(path)!=authority[path]:raise ValueError('Illustration changed')
        width,height=struct.unpack('>II',(ROOT/path).read_bytes()[16:24]);left,top,right,bottom=a['box']
        asset_id=id+'/illustration';where=origin(ART,'json:/assets/'+id)
        assets.append({'id':asset_id,'kind':'contextual_illustration','code_or_illustration_id':a['file'].removesuffix('.png'),'variant':id,
            'original':file(path),'bundled':file(path),'caption_id':id+'/illustration-caption','study_alt_text':a['alt_text'],'translation_status':'not_applicable',
            'reuse':[{'evidence':origin(CHAPTER+'review.md','whole-file'),'conditions':'Retain the approved contextual scene and production crop; no generated lettering or sign substitution. App resource packaging remains 9C4.','credit':'KörkortGo; built-in imagegen artwork.'}],
            'rendering':{'preserve_geometry_and_colours':True,'contain_without_crop':False,'maximum_print_size_mm':None,'notes':['Apply only the typed approved pixel window; aspect-fit the entire window. Source sheet is retained byte-for-byte.',f'Production effective resolution: {a["print_ppi"]} ppi.',f'Production placement width: {a.get("width_mm",170)} mm; not an app size or a print-size ceiling.']},
            'approval':[{'record':where,'reviewed_on':None},{'record':origin(CHAPTER+'review.md','whole-file'),'reviewed_on':None}]})
        image_payload={'type':'polygon_image' if a.get('polygon') else 'cropped_image','asset_id':asset_id,'region':{'left':left,'top':top,'right':right,'bottom':bottom,'source_width':width,'source_height':height},'caption':rich(a['caption'],lookup)}
        if a.get('polygon'):image_payload['polygon']=[{'x':x,'y':y} for x,y in a['polygon']]
        return block(id.replace('-cabin','/cabin')+'/illustration',image_payload,where)

    for id in IDS:
        d=copy.deepcopy(skeleton[id]);d['revision']='module-M02-9B3-v1';d['body_blocks']=[];d['answer_blocks']=[]
        body=d['body_blocks']
        if id=='M02':
            raw=sections[id][0];body.append(paragraph(id+'/introduction',raw,loc(raw)))
            body.append(heading(id+'/contents-heading','In this chapter'))
            links=[{'label':[{'type':'text','text':k+' · '+skeleton[k]['title']}],'target':{'type':'internal','target':{'content_id':k,'block_id':None}}} for k in IDS[1:]]
            body.append(block(id+'/contents',{'type':'related_links','links':links},prodloc('In this chapter')))
            disclaimer=pristine['documents'][1]['body_blocks'][1]
            body.append(paragraph(id+'/disclaimer',state['opening_text']['exact_disclaimer'],disclaimer['metadata']['origin'],'disclaimer'))
            note='Original sources checked 4 October 2026; G2 additions checked 12 October 2026. Consult current official guidance and the actual vehicle instructions.'
            body.append(paragraph(id+'/source-dates',note,prodloc(note),'source_limit'))
        else:
            paras=sections[id]
            if len(paras)!=len(PARAGRAPH_IDS[id]):raise ValueError('Paragraph inventory changed: '+id)
            for name,raw in zip(PARAGRAPH_IDS[id],paras):
                where=loc(raw);bid=id+'/'+name
                if name=='goal':
                    d['objectives']=[rich(raw.removeprefix('**Your goal:** '),lookup)]
                    body.append(paragraph(bid,raw,where));continue
                if name=='brake-circuits':body.append(heading(id+'/systems-heading','Brakes and protective circuits'))
                if name=='head-restraints':body.append(heading(id+'/systems-heading','How protection works'))
                if name=='reflection':body.append(heading(id+'/reflection-heading','Keep a practice record'))
                if name=='worked-decision':
                    if id=='M02-L04':body.append(image(id+'-cabin'))
                    body.append(heading(id+'/application-heading','Apply the learning'))
                    body.append(image(id))
                if name=='scenario':body.append(image(id))
                # Production places this practice example after the worked decision in L02.
                if name=='practice-example' and id=='M02-L02':continue
                if name in ('knowledge-check','review-check'):
                    marker=' **Answer:** ' if name=='knowledge-check' else ' **Review guide:** '
                    question,answer=raw.split(marker,1);answer_label='**Answer:** ' if name=='knowledge-check' else '**Review guide:** '
                    aid=bid+'/answer'
                    body.append(block(bid,{'type':'knowledge_check','prompts':[paragraph(bid+'/prompt',question,where)],'answer_id':aid},where))
                    d['answer_blocks'].append({'metadata':block(aid,{},where)['metadata'],'visibility':'after_deliberate_reveal','blocks':[paragraph(aid+'/text',answer_label+answer,where)]})
                elif name=='symptom-table':
                    rows=[[c.strip() for c in line.strip('|').split('|')] for line in raw.splitlines() if not re.fullmatch(r'[| :\-]+',line)]
                    body.append(block(bid,{'type':'table','caption':None,'columns':[{'heading':rich(c,lookup)} for c in rows[0]],'rows':[{'cells':[rich(c,lookup) for c in row]} for row in rows[1:]]},where,raw))
                elif name in ('worked-decision','scenario','practice-example'):
                    body.append(block(bid,{'type':'scenario','title':None,'blocks':[paragraph(bid+'/text',raw,where,'worked_example' if name!='scenario' else 'exercise_assumption')]},where))
                    if name=='worked-decision' and id=='M02-L02':
                        practice=paras[PARAGRAPH_IDS[id].index('practice-example')]
                        body.append(block(id+'/practice-example',{'type':'scenario','title':None,'blocks':[paragraph(id+'/practice-example/text',practice,loc(practice),'worked_example')]},loc(practice)))
                else:
                    role='summary' if name=='remember' else 'requirement' if name in ('tyre-requirements','restraint-requirements','movement-requirements') else 'recommendation' if name=='recommendations' else 'source_limit' if name=='vehicle-boundary' else 'explanation'
                    body.append(paragraph(bid,raw,where,role))
        def gather(value,key):
            if isinstance(value,dict):
                for k,v in value.items():
                    if k==key and v is not None:yield v
                    yield from gather(v,key)
            elif isinstance(value,list):
                for v in value:yield from gather(v,key)
        d['source_ids']=list(dict.fromkeys(gather(body,'source_id')))
        d['asset_bindings']=[key+'/illustration' for key in art if key==id or key==id+'-cabin']
        d['related_content']=[{'content_id':target,'block_id':None} for target in dict.fromkeys(gather(body,'content_id'))]
        if docs[id]['body_blocks'] and docs[id]!=d:raise ValueError('Refusing to overwrite edited M02 import: '+id)
        docs[id]=d
    payload['documents']=[docs[d['id']] for d in payload['documents']]
    for asset in assets:
        prior=next((a for a in payload['assets'] if a['id']==asset['id']),None)
        if prior is not None and prior!=asset:raise ValueError('Refusing to overwrite edited M02 illustration: '+asset['id'])
    existing=[a for a in payload['assets'] if a['id'] not in {a['id'] for a in assets}]
    payload['assets']=existing+assets
    state['step']='9B3';state['status']='opening_M01_and_M02_imported; remaining_modules_pending'
    state['pending_reading_nodes']=[r for r in state['pending_reading_nodes'] if r['id'] not in IDS]
    state['completed_module_imports']=[r for r in state['completed_module_imports'] if r['module_id']!='M02']+[{'module_id':'M02','step':'9B3','document_ids':IDS,'revision':'module-M02-9B3-v1','production_sources':[file(p) for p in required]}]
    return payload,state,merge_sources(source_payload)


def merge_sources(current):
    previous=read('docs/curriculum/app-migration/implementation-evidence/9B2/sources.json')
    result=copy.deepcopy(previous)
    for key in ['destinations','references']:
        rows={r['id']:r for r in result[key]}
        for incoming in current[key]:
            if incoming['id'] not in rows:result[key].append(incoming);rows[incoming['id']]=incoming;continue
            old=rows[incoming['id']]
            if key=='destinations':old['scoped_urls']+=incoming['scoped_urls']
            else:
                if old['url']!=incoming['url'] or old['classifications']!=incoming['classifications']:raise ValueError('Conflicting source evidence')
                old['original_evidence_ids']=list(dict.fromkeys(old['original_evidence_ids']+incoming['original_evidence_ids']))
                old['evidence']+=incoming['evidence']
    return result


def stage(payload):
    paths={'curriculum':CURRICULUM,**{k:EVIDENCE/(k+'.json') for k in ['questions','sources','legacy_aliases']}}
    inputs=[AUTHORITY,REGISTRY,BASELINE,ACTIONS,QUESTION_MAP,LINKS,*MODEL_PATHS,SOURCE,BUILDER,CHECKS,ART,CHAPTER+'navigation.json','tools/import_curriculum_m02.py','docs/curriculum/app-migration/implementation-evidence/9B2/sources.json',str((EVIDENCE/'incoming-curriculum.json').relative_to(ROOT)),str((EVIDENCE/'incoming-import-state.json').relative_to(ROOT)),str((EVIDENCE/'pdf-M02-text.json').relative_to(ROOT)),'tools/import_curriculum_m01.py','tools/import_curriculum_opening.py','tools/compile_curriculum.py','tools/content_schema.py','content/curriculum-import-state.json']
    previous_revisions={r['id']:r['revision'] for r in read('docs/curriculum/app-migration/implementation-evidence/9B2/staging-manifest.json')['canonical_revisions']}
    m={'schema_version':1,'identity':{'content_version':'staging-9B3-M02','manifest_sha256':'0'*64},'source_curriculum':payload['source_curriculum'],'inputs':[file(p) for p in inputs],
       'payloads':[{'kind':k,'file':file(str(v.relative_to(ROOT)))} for k,v in paths.items()]+[{'kind':'asset','file':file(p)} for p in dict.fromkeys(a['bundled']['path'] for a in payload['assets'])],
       'canonical_revisions':[{'id':d['id'],'revision':d['revision']} for d in payload['documents']]+[{'id':s['id'],'revision':'source-M02-9B3-v1' if any(b['scope_id']=='M02' for b in s['scoped_urls']) else previous_revisions[s['id']]} for s in read(str((EVIDENCE/'sources.json').relative_to(ROOT)))['destinations']], 'question_revisions':[],
       'source_bindings':[{'source_id':s['id'],**b} for s in read(str((EVIDENCE/'sources.json').relative_to(ROOT)))['destinations'] for b in s['scoped_urls']],
       'asset_bindings':[{'id':a['id'],'file':a['bundled']} for a in payload['assets']]}
    m['identity']['manifest_sha256']=manifest_digest(m);manifest=EVIDENCE/'staging-manifest.json';manifest.write_text(encoded(m))
    return compile_files(paths,manifest,EVIDENCE/'generated',EVIDENCE/'trace.json',profile='fixture',symbol='stagedCurriculum9B3')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');args=p.parse_args()
    try:
        payload,state,s=build(read('content/curriculum.json'),read('content/curriculum-import-state.json'))
        if args.check:
            if payload!=read('content/curriculum.json') or state!=read('content/curriculum-import-state.json') or s!=read(str((EVIDENCE/'sources.json').relative_to(ROOT))):raise ValueError('M02 import differs from approved production')
            print('PASS: M02 import reproduces without writes.');return 0
        EVIDENCE.mkdir(parents=True,exist_ok=True)
        backups={p:p.read_bytes() if p.exists() else None for p in [CURRICULUM,STATE,*[EVIDENCE/(k+'.json') for k in ['sources','questions','legacy_aliases']]]}
        try:
            CURRICULUM.write_text(encoded(payload));STATE.write_text(encoded(state))
            for k,v in {'sources':s,'questions':{'schema_version':1,'questions':[]},'legacy_aliases':{'schema_version':1,'aliases':[],'tombstones':[]}}.items():(EVIDENCE/(k+'.json')).write_text(encoded(v))
            result=stage(payload)
        except Exception:
            for path,data in backups.items():
                if data is None:path.unlink(missing_ok=True)
                else:path.write_bytes(data)
            raise
        print(json.dumps(result,sort_keys=True));return 0
    except (ValueError,OSError,KeyError,StopIteration) as e:print(str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
