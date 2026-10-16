"""Complete the approved 9B data import and its 9C source/artwork prerequisites.
No PDF builder, legacy generator, network request or assessment acceptance is invoked.
"""
import argparse,copy,hashlib,json,re,shutil,struct,sys
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse
from import_curriculum_opening import ROOT,read,sha,file,origin,encoded,build as opening
from compile_curriculum import AUTHORITY,REGISTRY,BASELINE,ACTIONS,MODEL_PATHS,manifest_digest,compile_files,pointer
HERE=ROOT/'docs/curriculum/app-migration/implementation-evidence/9B17'
PDF='docs/curriculum/pdf-production/korkortgo-curriculum.pdf'
CAPS='docs/curriculum/sign-captions.json';PLACEMENT='docs/curriculum/sign-placement-map.json'
MS='docs/curriculum/manuscript-sources.json';QM='docs/curriculum/app-migration/question-map.json'
RESOURCE='composeApp/src/commonMain/composeResources/files/curriculum/'

@lru_cache(maxsize=None)
def file(path):return {'path':path,'sha256':sha(path)}
def origin(path,locator,page=None):return {'file':file(path),'locator':locator,'evidence_ids':[],'pdf_evidence_page':page}


def rid(url):return 'REF-'+hashlib.sha256(url.encode()).hexdigest()[:16]
def plain_md(text):
    text=re.sub(r'\[([^]]+)\]\[([^]]+)\]',r'\1',text).replace('**','')
    return re.sub(r'(?<!\w)\*([^*\n]+)\*(?!\w)',r'\1',text)
def norm(text):return ' '.join(text.split())
def table_rows(raw):return [[c.strip() for c in l.strip().strip('|').split('|')] for l in raw.splitlines() if l.startswith('|') and not re.fullmatch(r'[| :\-]+',l)]
def printable(raw):
    if raw.startswith('|'):return norm(plain_md(' '.join(c for row in table_rows(raw) for c in row)))
    if raw.startswith('### '):raw=raw[4:]
    if raw.startswith('- '):raw='\n'.join(line.removeprefix('- ') for line in raw.splitlines())
    return norm(plain_md(raw))
def all_values(value,key):
    if isinstance(value,dict):
        for k,v in value.items():
            if k==key:yield v
            yield from all_values(v,key)
    elif isinstance(value,list):
        for v in value:yield from all_values(v,key)

class Import:
    def __init__(self):
        self.registry=read(REGISTRY);self.known={r['id']:r for k in ['curriculum_nodes','supporting_destinations','source_destinations','sign_entries'] for r in self.registry[k]}
        self.authority={r['path']:r['sha256'] for r in read(AUTHORITY)['input_manifest']}
        self.payload=read(str((HERE/'incoming-curriculum.json').relative_to(ROOT)));self.state=read(str((HERE/'incoming-import-state.json').relative_to(ROOT)))
        predecessor=read('docs/curriculum/app-migration/implementation-evidence/9B3/verification.json')
        identities={r['path']:r['sha256'] for r in predecessor['artifacts']}
        for name,original in [('incoming-curriculum.json','content/curriculum.json'),('incoming-import-state.json','content/curriculum-import-state.json')]:
            if sha(str((HERE/name).relative_to(ROOT)))!=identities[original]:raise ValueError('Incoming 9B3 snapshot drift')
        self.sources=read('docs/curriculum/app-migration/implementation-evidence/9B3/sources.json')
        self.documents={d['id']:d for d in self.payload['documents']};self.assets={a['id']:a for a in self.payload['assets']}
        self.captions=read(CAPS)['captions'];self.cap={c['code']:c for c in self.captions}
        self.binds={b['code']:b for b in read(PLACEMENT)['asset_caption_bindings']}
        self.pages=read(str((HERE/'pdf-text.json').relative_to(ROOT)))
        self.remaining={r['page']:norm(r['body']) for r in self.pages}
        self.events={};self.sign_counts={};self.parity=[];self.claims=[];self.inputs=set([PDF,REGISTRY,QM,MS,CAPS,PLACEMENT])
        self.allocations={};self.omissions=[];self.sign_spans=[];self.coverage=[];self.matches=[];self.missing=[];self.url_info={};self.raw_cache={};self.checked_files=set();self.aliases={};self.used_pages={}
        self.page_owner={};self.page_target={};self.references={r['id']:r for r in self.sources['references']}
        self.build_source_catalog()
    def frozen(self,path):
        if path in self.checked_files:return
        self.checked_files.add(path)
        expected=self.authority.get(path) or next((r['source']['sha256'] for r in self.state['deferred'] if isinstance(r.get('source'),dict) and r['source']['path']==path),None)
        if sha(path)!=expected:raise ValueError('Frozen source drift: '+path)
        self.inputs.add(path)
    def source_evidence(self,path,ptr,rec):
        parent=self.raw_cache.setdefault(path,read(path)) if path not in self.raw_cache else self.raw_cache[path];dates={'checked_on':rec.get('checked_on') or rec.get('reviewed_on'),'retrieved_on':rec.get('retrieved_on') or rec.get('retrieved'),'published_on':rec.get('published_on')}
        if not dates['checked_on'] and '/chapters/' in path:
            group=ptr.split('/')[1];dates['checked_on']=parent.get(group.split('_')[0]+'_checked_on') if group.startswith(('G','H')) else parent.get('checked_on')
        for key,val in dates.items():
            if val and not re.fullmatch(r'\d{4}-\d{2}-\d{2}',val):dates[key]=None
        return {'origin':origin(path,'json:'+ptr),'dates':dates,'scope':rec.get('scope_limits') or rec.get('locator') or ('Retained evidence '+ptr),
            'finding':str(rec.get('finding') or rec.get('supports') or rec.get('basis') or rec.get('locator') or rec.get('status') or 'Retained source binding; no new factual review.'),
            'limitations':[str(rec[k]) for k in ['fallback_reason','scope_limits','version'] if rec.get(k)]}
    def build_source_catalog(self):
        info={}
        def add(url,path,ptr,rec,title=None,publisher=None,note=''):
            if not url:return
            self.frozen(path);row=info.setdefault(url,{'records':[],'title':None,'publisher':None,'note':note})
            row['records'].append((path,ptr,rec))
            row['title']=row['title'] or rec.get('title') or title
            row['publisher']=row['publisher'] or rec.get('publisher') or publisher
            row['note']=row['note'] or note
        for r in read(QM)['source_registry']:
            info.setdefault(r['url'],{'records':[],'title':None,'publisher':None,'note':r['classification']})
            for e in r['source_checks']:add(r['url'],e['path'],e['json_pointer'],e['record'],note=r['classification'])
        for i,r in enumerate(read(MS)['sources']):
            add(r['url'],MS,f'/sources/{i}',r)
            for j,rec in enumerate(r.get('additional_checks',[])):add(rec.get('url',r['url']),MS,f'/sources/{i}/additional_checks/{j}',rec)
        for i,c in enumerate(self.captions):
            for j,rec in enumerate(c['sources']):add(rec['url'],CAPS,f'/captions/{i}/sources/{j}',rec,c['official_name_sv'],'Transportstyrelsen' if 'transportstyrelsen.se' in rec['url'] else 'Sveriges riksdag')
        for m in range(1,11):
            path=f'docs/curriculum/pdf-production/chapters/M{m:02d}/source-checks.json'
            def walk(value,ptr=''):
                if isinstance(value,dict):
                    if isinstance(value.get('url'),str):add(value['url'],path,ptr,value)
                    for k,v in value.items():walk(v,ptr+'/'+k.replace('~','~0').replace('/','~1'))
                elif isinstance(value,list):
                    for i,v in enumerate(value):walk(v,ptr+'/'+str(i))
            walk(read(path))
        destinations={r['id']:r for r in self.sources['destinations']}
        for i,r in enumerate(self.registry['source_destinations']):
            for scope,url in r['scoped_urls'].items():self.aliases[(scope,r['alias'])]=(r['id'],rid(url))
            row=destinations.get(r['id'])
            bindings=[{'scope_id':scope,'reference_id':rid(url)} for scope,url in r['scoped_urls'].items()]
            if row:
                for b in bindings:
                    if b not in row['scoped_urls']:row['scoped_urls'].append(b)
            else:
                record=info.get(r['url'],{})
                row={'id':r['id'],'original_alias':r['alias'],'title':record.get('title') or r['alias'],'scoped_urls':bindings,'origin':origin(REGISTRY,f'json:/source_destinations/{i}')}
                self.sources['destinations'].append(row);destinations[r['id']]=row
        required_urls={r['url'] for r in read(QM)['source_registry']} | {u for r in self.registry['source_destinations'] for u in [r['url'],*r['scoped_urls'].values()]} | {r['url'] for n in self.registry['sign_entries'] for r in self.cap[n['code']]['sources']} | {self.binds[n['code']]['official_url'] for n in self.registry['sign_entries']}
        for url,meta in info.items():
            if url not in required_urls:continue
            if not meta['records']:raise ValueError('No retained URL evidence: '+url)
            host=urlparse(url).hostname
            publisher=meta['publisher'] or host
            classification=('commercial_teaching' if 'trafiko.se' in host else 'manufacturer' if any(s in host for s in ['volvocars','fordservice','toyota']) else
                'swedish_public_service' if any(s in host for s in ['1177.se','polisen.se','krisinformation.se','smhi.se','naturvardsverket.se']) else
                'swedish_parliamentary_material' if '/proposition/' in url else 'swedish_legislation' if host=='www.riksdagen.se' or '/TSFS/' in url else
                'research' if 'vti-rapport' in url or (publisher and 'VTI' in publisher) else
                'swedish_authority_guidance' if any(s in host for s in ['trafikverket.se','transportstyrelsen.se']) else 'foreign_public_authority')
            row=self.references.get(rid(url))
            if not row:
                row={'id':rid(url),'url':url,'title':meta['title'] or url,'publisher':publisher,'classifications':[classification],
                    'classification_note':meta['note'] or 'Retained passage-specific evidence; not a new currency check.',
                    'editorial_inference':not bool(meta['publisher']),'original_evidence_ids':[],'evidence':[]}
                if not meta['publisher']:row['classification_note']+=' Publisher attribution inferred from retained URL hostname.'
                self.sources['references'].append(row);self.references[row['id']]=row
            existing={(e['origin']['file']['path'],e['origin']['locator']) for e in row['evidence']}
            for path,ptr,rec in meta['records']:
                if (path,'json:'+ptr) not in existing:
                    row['evidence'].append(self.source_evidence(path,ptr,rec));existing.add((path,'json:'+ptr))
                sid=rec.get('source_id')
                if sid and sid not in row['original_evidence_ids']:row['original_evidence_ids'].append(sid)
        self.url_info=info
    def rich(self,text,scope=None):
        result=[];offset=0
        sign_pattern='|'.join(re.escape(c) for c in sorted((r['code'] for r in self.registry['sign_entries']),key=len,reverse=True))
        pattern=r'\*\*(.+?)\*\*|(?<!\w)\*([^*\n]+)\*(?!\w)|\[([^]]+)\]\[([^]]+)\]|\bM\d{2}(?:-L\d{2}(?:/L\d{2})*)?\b|https://[^\s<>]+'
        pattern+=r'|(?<![\w-])(?:'+sign_pattern+r')(?![\w-])'
        for m in re.finditer(pattern,text):
            if m.start()>offset:result.append({'type':'text','text':text[offset:m.start()]})
            if m[1] or m[2]:result.append({'type':'strong' if m[1] else 'emphasis','children':self.rich(m[1] or m[2],scope)})
            elif m[4]:
                sid,ref=self.aliases[(scope,m[4])];result.append({'type':'link','label':[{'type':'text','text':m[3]}],'target':{'type':'external_source','reference_id':ref}})
            elif m[0].startswith('M'):
                tokens=m[0].split('/');module=tokens[0][:3]
                for i,token in enumerate(tokens):
                    if i:result.append({'type':'text','text':'/'})
                    target=token if i==0 else module+'-'+token
                    if target not in self.known and 'sign-'+target in self.known:target='sign-'+target
                    result.append({'type':'link','label':[{'type':'text','text':token}],'target':{'type':'internal','target':{'content_id':target,'block_id':None}}})
            elif 'sign-'+m[0] in self.known:
                result.append({'type':'link','label':[{'type':'text','text':m[0]}],'target':{'type':'internal','target':{'content_id':'sign-'+m[0],'block_id':None}}})
            else:
                url=m[0]
                if rid(url) in self.references:result.append({'type':'link','label':[{'type':'text','text':url}],'target':{'type':'external_source','reference_id':rid(url)}})
                else:result.append({'type':'text','text':url})
            offset=m.end()
        if offset<len(text):result.append({'type':'text','text':text[offset:]})
        return result
    def metadata(self,id,loc,raw='',scope=None):
        uses=[]
        for alias in dict.fromkeys(re.findall(r'\]\[([^]]+)\]',raw)):
            sid,ref=self.aliases[(scope,alias)];uses.append({'reference_id':ref,'source_id':sid,'scope_id':scope if scope.startswith('M') else next(b['scope_id'] for r in self.sources['destinations'] if r['id']==sid for b in r['scoped_urls'] if b['reference_id']==ref),'locator':loc['locator'],'editorial_inference':bool(re.search(r'hypothetical|approximate|worked.*example|exercise model',raw,re.I))})
        return {'id':id,'origin':loc,'source_uses':uses,'related_content':[]}
    def block(self,id,raw,loc,scope=None):
        # PDF line wrapping may split a URL midword. Restore only exact annotation URLs.
        if loc['file']['path']==PDF and loc.get('pdf_evidence_page') and 'https://' in raw:
            for url in self.pages[loc['pdf_evidence_page']-1]['urls']:
                raw=re.sub(r'\s*'.join(re.escape(c) for c in url),lambda m:url,raw)
        if raw.startswith('|'):
            rows=table_rows(raw);payload={'type':'table','caption':None,'columns':[{'heading':self.rich(v,scope)} for v in rows[0]],'rows':[{'cells':[self.rich(v,scope) for v in row]} for row in rows[1:]]}
        elif raw.startswith('### '):payload={'type':'heading','level':2,'text':self.rich(raw[4:],scope)}
        elif raw.startswith('- ') or re.match(r'1\. ',raw):
            ordered=not raw.startswith('- ');items=[]
            for i,line in enumerate(raw.splitlines()):
                text=re.sub(r'^\d+\. ' if ordered else r'^- ','',line)
                items.append([self.block(id+f'/item-{i+1}',text,loc,scope)])
            payload={'type':'list_items','ordered':ordered,'start':1,'items':items}
        elif raw.startswith(('**Worked','**Practice example','**Scenario')):
            child={'metadata':self.metadata(id+'/text',loc,raw,scope),'payload':{'type':'paragraph','text':self.rich(raw,scope),'role':'exercise_assumption' if raw.startswith('**Scenario') else 'worked_example'}}
            payload={'type':'scenario','title':None,'blocks':[child]}
        else:
            role='requirement' if raw.startswith(('**Requirement','**Legal ')) else 'recommendation' if raw.startswith(('**Official recommendation','**Safety advice')) else 'summary' if raw.startswith('**Remember') else 'worked_example' if raw.startswith(('**Worked','**Practice')) else 'explanation'
            payload={'type':'paragraph','text':self.rich(raw,scope),'role':role}
        return {'metadata':self.metadata(id,loc,raw,scope),'payload':payload}
    def document(self,node,blocks=None):
        loc=node['source_location'];path=loc['path']
        locator='line:'+str(loc['line']) if 'line' in loc else 'json:'+loc['json_pointer']
        return {'id':node['id'],'kind':'module_introduction' if node['kind']=='module' else node['kind'],'module_id':node.get('module_id'),'title':node['title'],'order':node['order'],'objectives':[],
                'body_blocks':blocks or [],'answer_blocks':[],'source_ids':[],'asset_bindings':[],'related_content':[],'content_version':self.payload['source_curriculum']['content_version'],'revision':'complete-9B-v1','origin':origin(path,locator,node.get('pdf_evidence_page'))}
    def add_event(self,page,offset,parent,block,answer=None):
        self.events.setdefault(page,[]).append((offset,parent,block,answer));self.used_pages.setdefault(parent,set()).add(page)
    def locate(self,value,pages,id,required=True):
        value=norm(value)
        found=[(p,self.remaining[p].find(value)) for p in pages if value in self.remaining[p]]
        if not found:
            if required:self.missing.append({'id':id,'text':value,'pages':list(pages)})
            return None
        p,index=found[0];self.remaining[p]=self.remaining[p][:index]+' '*len(value)+self.remaining[p][index+len(value):]
        self.matches.append({'id':id,'page':p,'offset':index,'normalized_sha256':hashlib.sha256(value.encode()).hexdigest(),'characters':len(value)})
        return p,index
    def bundle(self,path):
        self.frozen(path);target=RESOURCE+Path(path).name
        self.copies[target]=path
        return {'path':target,'sha256':sha(path)}
    def sign_assets(self):
        self.copies={};self.payload['sign_entries']=[]
        for i,node in enumerate(self.registry['sign_entries']):
            c=self.cap[node['code']];a=node['asset'];asset_id='official/'+node['code'];bundled=self.bundle(a['path'])
            original=file(a['path']);loc=origin(CAPS,f'json:/captions/{self.captions.index(c)}')
            maximum=a.get('max_size_mm_at_300ppi')
            asset={'id':asset_id,'kind':'official_sign','code_or_illustration_id':node['code'],'variant':c.get('variant_description_en') or node['code'],'original':original,'bundled':bundled,'caption_id':node['caption_id'],
                   'study_alt_text':c['alt_text_en'],'translation_status':'editorial_english','reuse':[{'evidence':origin('docs/curriculum/sign-reuse.md','whole-file'),'conditions':'Retain exact official artwork and attribution, teaching context and recorded source-specific limits.','credit':'Transportstyrelsen; English labels and explanations are editorial translations.'}],
                   'rendering':{'preserve_geometry_and_colours':True,'contain_without_crop':True,'maximum_print_size_mm':{'width':str(maximum[0]),'height':str(maximum[1])} if maximum else None,'notes':[a.get('reason','Exact official artwork.'),'Minimum reviewed width (if retained): '+str(a.get('minimum_reviewed_width_mm','not specified'))+' mm; app delivery acceptance remains pending.']},
                   'approval':[{'record':loc,'reviewed_on':c['reviewed_on']},{'record':origin(REGISTRY,f'json:/sign_entries/{i}'),'reviewed_on':None}]}
            self.assets[asset_id]=asset
            url=self.binds[node['code']]['official_url']
            use={'reference_id':rid(url),'source_id':None,'scope_id':None,'locator':c['sources'][0].get('locator','Official sign description'),'editorial_inference':False}
            self.payload['sign_entries'].append({'id':node['id'],'code':node['code'],'official_name_sv':node['official_name_sv'],'english_label':c['label_en'],'caption_id':node['caption_id'],
                'caption':self.rich(c['teaching_caption_en']+(' '+c['variant_description_en'] if c.get('variant_description_en') else '')),'asset_id':asset_id,'translation_status':'editorial_english','source_uses':[use],
                'limitations':c.get('hold_notes',[]),'origin':loc})
        self.frozen('docs/curriculum/sign-reuse.md')
    def illustration(self,key,a,path,parent):
        image='docs/curriculum/pdf-design/gap-resolution/'+a['file'];bundled=self.bundle(image)
        if sha(image)!=a['sha256']:raise ValueError('Art binding drift')
        w,h=struct.unpack('>II',(ROOT/image).read_bytes()[16:24]);l,t,r,b=a['box'];asset_id=key+'/illustration';loc=origin(path,'json:/assets/'+key)
        self.assets[asset_id]={'id':asset_id,'kind':'contextual_illustration','code_or_illustration_id':Path(image).stem,'variant':key,'original':file(image),'bundled':bundled,'caption_id':key+'/illustration-caption','study_alt_text':a['alt_text'],'translation_status':'not_applicable',
            'reuse':[{'evidence':origin(path,'json:/assets/'+key),'conditions':'Approved production crop/mask/overlays only; preserve exact sheet bytes.','credit':'KörkortGo; built-in imagegen artwork.'}],
            'rendering':{'preserve_geometry_and_colours':True,'contain_without_crop':False,'maximum_print_size_mm':None,'notes':[f'Production width: {a.get("width_mm",170)} mm; resolution: {a["print_ppi"]} ppi. Clip approved region, apply retained overlays/mask, then contain without distortion.']},
            'approval':[{'record':loc,'reviewed_on':None}]}
        payload={'type':'composite_image' if a.get('overlays') else 'polygon_image' if a.get('polygon') else 'cropped_image','asset_id':asset_id,'region':{'left':l,'top':t,'right':r,'bottom':b,'source_width':w,'source_height':h},'caption':self.rich(a['caption'])}
        if a.get('polygon'):payload['polygon']=[{'x':x,'y':y} for x,y in a['polygon']]
        if a.get('overlays'):
            payload['overlays']=[]
            for overlay in a['overlays']:
                ol,ot,orr,ob=overlay['rect'];payload['overlays'].append({'left':ol,'top':ot,'right':orr,'bottom':ob,'asset_id':'official/'+overlay['code'] if 'code' in overlay else None,'label':self.rich(overlay.get('label','')),'inset_pixels':2})
        return {'metadata':self.metadata(parent+'/illustration/'+key,loc),'payload':payload}
    def modules(self):
        for n in range(3,11):
            module=f'M{n:02d}';step='9B'+str(n+1);chapter=f'docs/curriculum/pdf-production/chapters/{module}/';source=chapter+'chapter-source.md'
            for p in [source,chapter+'build_chapter.py',chapter+'illustrations.json',chapter+'navigation.json']:self.frozen(p)
            text=(ROOT/source).read_text();teaching=re.split(r'^\[[^]]+\]: ',text,1,flags=re.M)[0].strip()
            parts=re.split(r'^### (M\d+-\S+) · (.+)\n',teaching,flags=re.M)
            sections={module:[parts[0].split('\n\n',1)[1].strip()]}
            for i in range(1,len(parts),3):sections[parts[i]]=parts[i+2].strip().split('\n\n')
            nodes=[r for r in self.registry['curriculum_nodes'] if r['id'] in sections];start=min(r['pdf_evidence_page'] for r in nodes);end=next((r['pdf_evidence_page']-1 for r in self.registry['curriculum_nodes'] if r['id']==f'M{n+1:02d}'),343)
            nav=read(chapter+'navigation.json');answer_start=nav['destinations'][module+'-answers']+start-1;ref_start=nav['destinations'][module+'-references']+start-1
            sortednodes=sorted(nodes,key=lambda r:r['pdf_evidence_page'])
            for j,node in enumerate(sortednodes):
                d=self.document(node);self.documents[d['id']]=d;begin=node['pdf_evidence_page'];finish=sortednodes[j+1]['pdf_evidence_page']-1 if j+1<len(nodes) else answer_start-1
                for page in range(begin,finish+1):self.page_owner[page]=d['id']
                self.import_paragraphs(d,sections[d['id']],source,module,range(begin,finish+1),range(answer_start,ref_start))
            self.support_document(module+'-references',nav['page_labels'][str(ref_start-start+1)])
            for page in range(ref_start,end+1):self.page_owner[page]=module+'-references'
            # Answer pages carry only hidden answers plus print headings/labels.
            for page in range(answer_start,ref_start):self.page_owner[page]=module
            art=read(chapter+'illustrations.json')['assets']
            for key,a in art.items():
                parent=max((id for id in sections if key==id or key.startswith(id+'-')),key=len,default=None)
                if parent is None:raise ValueError('Unbound illustration '+key)
                block=self.illustration(key,a,chapter+'illustrations.json',parent)
                pages=[p for p in range(start,end+1) if self.page_owner.get(p)==parent]
                match=self.locate(a['caption'],pages,block['metadata']['id'])
                if match:self.add_event(*match,parent,block)
            self.state['completed_module_imports'].append({'module_id':module,'step':step,'document_ids':list(sections),'revision':'complete-9B-v1','production_sources':[file(source),file(chapter+'illustrations.json')]})
    def import_paragraphs(self,d,paras,source,scope,pages,answer_pages=()):
        full=(ROOT/source).read_text();parent=d['id']
        for i,raw in enumerate(paras):
            id=parent+'/teaching-'+str(i+1).zfill(3);line=full[:full.index(raw)].count('\n')+1;loc=origin(source,f'line:{line}-{line+raw.count(chr(10))}')
            if raw.startswith('**Your goal:'):
                d['objectives']=[self.rich(raw.removeprefix('**Your goal:** '),scope)]
            marker=' **Answer:** ' if ' **Answer:** ' in raw else ' **Review guide:** ' if ' **Review guide:** ' in raw else None
            if marker:
                prompt,answer=raw.split(marker,1);label='**Answer:** ' if 'Answer' in marker else '**Review guide:** ';aid=id+'/answer'
                block={'metadata':self.metadata(id,loc,scope=scope),'payload':{'type':'knowledge_check','prompts':[self.block(id+'/prompt',prompt,loc,scope)],'answer_id':aid}}
                answerblock={'metadata':self.metadata(aid,loc,scope=scope),'visibility':'after_deliberate_reveal','blocks':[self.block(aid+'/text',label+answer,loc,scope)]}
                match=self.locate(printable(prompt),pages,id)
                if match:self.add_event(*match,parent,block)
                amatch=self.locate(printable(label+answer),answer_pages,aid)
                if amatch:self.add_event(*amatch,parent,answerblock,True)
            else:
                block=self.block(id,raw,loc,scope)
                if raw.startswith('|'):
                    match=self.locate(printable(raw),pages,id,False)
                    if match:self.add_event(*match,parent,block)
                    else:
                        rows=table_rows(raw);header=printable(' '.join(rows[0]));starts=[]
                        for page in pages:
                            found=self.locate(header,[page],id+'/header',False)
                            if not found and parent=='appendix-D':found=self.locate('Prompt · Your record',[page],id+'/header',False)
                            if found:starts.append(found)
                        for ri,row in enumerate(rows[1:]):
                            found=self.locate(norm(plain_md(' '.join(row))),pages,id+'/row-'+str(ri+1))
                            if found:starts.append(found)
                        if starts:self.add_event(*min(starts),parent,block)
                else:
                    match=self.locate(printable(raw),pages,id)
                    if match:self.add_event(*match,parent,block)
            self.parity.append({'id':id,'source':loc,'normalized_text_sha256':hashlib.sha256(printable(raw).encode()).hexdigest(),'step':('9B'+str(int(scope[1:])+1)) if scope and scope.startswith('M') else '9B'+str(12+ord(parent[-1])-65)})
    def appendices(self):
        source='docs/curriculum/pdf-production/reference/reference-source.md';self.frozen(source)
        full=(ROOT/source).read_text();parts=re.split(r'^## (.+)\n',full,flags=re.M)
        for n in range(4):
            title=parts[n*2+1];raw=parts[n*2+2].strip();id='appendix-'+chr(65+n);node=self.known[id];d=self.document(node);self.documents[id]=d
            start=node['pdf_evidence_page'];end=[346,351,542,544][n]
            # The family lookup follows the sign groups, but belongs to Appendix B.
            for page in range(start,end+1):self.page_owner[page]=id
            if n==1:
                for page in range(533,536):self.page_owner[page]=id
            # Appendix sources use the retained global URL; choose its exact owning module scope.
            for alias in re.findall(r'\]\[([^]]+)\]',raw):
                row=next(r for r in self.registry['source_destinations'] if r['alias']==alias)
                url=row['url'];binding=next((x for x in row['scoped_urls'].items() if x[1]==url),next(iter(row['scoped_urls'].items())))
                self.aliases[(id,alias)]=(row['id'],rid(binding[1]))
            self.import_paragraphs(d,raw.split('\n\n'),source,id,range(start,end+1))
        # A real published supporting destination owns the reference opening and credits.
        for id,start,end,title in [('reference-contents',344,344,'Keep learning, checking and practising'),('official-references',545,577,'Sources and references'),('artwork-credits',578,578,'Artwork and source credits')]:
            node=self.known[id]
            d={'id':id,'kind':'front_matter','module_id':None,'title':title,'order':1,'objectives':[],'body_blocks':[],'answer_blocks':[],'source_ids':[],'asset_bindings':[],'related_content':[],'content_version':self.payload['source_curriculum']['content_version'],'revision':'complete-9B-v1','origin':origin(REGISTRY,'json:/supporting_destinations/'+str(self.registry['supporting_destinations'].index(node)),start)}
            self.documents[id]=d
            for page in range(start,end+1):self.page_owner[page]=id
    def groups(self):
        self.payload['reference_groups']=[];placements=read(PLACEMENT)['reference_groups'];records=read('docs/curriculum/pdf-production/reference/assets.json')['official_sign_placements'];self.frozen('docs/curriculum/pdf-production/reference/assets.json')
        ordered=sorted([r for r in self.registry['curriculum_nodes'] if r['kind']=='sign_reference_group'],key=lambda r:r['order'])
        for i,node in enumerate(ordered):
            start=node['pdf_evidence_page'];end=ordered[i+1]['pdf_evidence_page']-1 if i<23 else 532
            members=[r['code'] for r in records if r['group']==node['id']]
            if len(set(members))!=len(members):raise ValueError('Duplicate primary group member')
            self.payload['reference_groups'].append({'id':node['id'],'title':node['title'],'order':node['order'],'body_blocks':[],'entry_ids':['sign-'+code for code in members],'origin':origin(PLACEMENT,f'json:/reference_groups/{i}'),'revision':'complete-9B-v1'})
            for p in range(start,end+1):self.page_owner[p]=node['id']
    def strip_sign_examples(self):
        # Consume each displayed official example through shared canonical sign data.
        for code,c in self.cap.items():
            label=code+' · '+c['label_en'];caption=norm(c['teaching_caption_en']+(' '+c['variant_description_en'] if c.get('variant_description_en') else ''))
            for page in range(41,579):
                if label not in self.remaining[page]:continue
                # Complete sign cards contain these four consecutive text components.
                text=self.remaining[page];start=text.find(label);cursor=start+len(label)
                components=[c['official_name_sv'],caption,'Transportstyrelsen · official description']
                spans=[(start,cursor)]
                valid=True
                for value in components:
                    value=norm(value);index=text.find(value,cursor)
                    if index<0 or text[cursor:index].strip():valid=False;break
                    spans.append((index,index+len(value)));cursor=index+len(value)
                if not valid:continue # A cross-link is not a duplicated sign card.
                for a,b in reversed(spans):text=text[:a]+' '*(b-a)+text[b:]
                self.sign_spans.extend({'page':page,'offset':a,'characters':b-a,'code':code} for a,b in spans)
                self.remaining[page]=text
                parent=self.page_owner[page];counter=self.sign_counts.get((parent,code),0)+1;self.sign_counts[(parent,code)]=counter;id=parent+'/official-example-'+code+'-'+str(counter)
                block={'metadata':self.metadata(id,origin(CAPS,'json:/captions/'+str(self.captions.index(c)),page)), 'payload':{'type':'sign_examples','entry_ids':['sign-'+code]}}
                self.add_event(page,start,parent,block)
                self.claims.append({'page':page,'id':id,'code':code,'caption_sha256':hashlib.sha256(caption.encode()).hexdigest()})
    def finish_pages(self):
        # Keep all remaining actual production teaching, captions, labels and links.
        # IDs are authored allocations retained in allocation-ledger.json, not routes based on folios.
        for page in range(41,579):
            parent=self.page_owner[page];text=self.remaining[page]
            # Metadata titles/IDs and standard print controls are not duplicated as teaching.
            node=self.known.get(parent,{});title=self.documents[parent]['title'] if parent in self.documents else node['title']
            for value in [f'CHAPTER {parent[1:]}' if re.fullmatch(r'M\d{2}',parent) else '',parent if re.fullmatch(r'M\d{2}-L\d{2}|RB\d{2}',parent) else '',title if page==node.get('pdf_evidence_page') else '']:
                if value and norm(value) in text:
                    at=text.index(norm(value));self.omissions.append({'page':page,'offset':at,'characters':len(norm(value)),'text':norm(value),'reason':'document title/printed ID is metadata'});text=text[:at]+' '*len(norm(value))+text[at+len(norm(value)):]
            # Printed answer headings/IDs are navigation; answer text was consumed separately.
            if any(e[3] for e in self.events.get(page,[])):
                stripped=text
                for value in ['Review after answering','Continue the learning','Check your understanding',*[f'M{n:02d}-L{k:02d}' for n in range(3,11) for k in range(1,5)],*[f'M{n:02d}-R' for n in range(3,11)]]:
                    for match in re.finditer(re.escape(value),text):self.omissions.append({'page':page,'offset':match.start(),'characters':len(value),'text':value,'reason':'answer-page heading/ID'})
                    stripped=stripped.replace(value,'')
                if stripped.strip():self.missing.append({'id':'unmatched-answer-page','page':page,'text':stripped.strip()})
                text=''
            # Span boundaries are retained around removed source blocks/sign cards.
            count=0
            for m in re.finditer(r'\S(?:.*?\S)?(?= {2,}|$)',text):
                value=norm(m[0])
                if not value:continue
                count+=1;index=self.allocations.get(parent,0)+1;self.allocations[parent]=index;id=parent+'/production-'+str(index).zfill(4)
                loc=origin(PDF,'whole-file',page);block=self.block(id,value,loc)
                self.add_event(page,m.start(),parent,block)
                self.matches.append({'id':id,'page':page,'offset':m.start(),'normalized_sha256':hashlib.sha256(value.encode()).hexdigest(),'characters':len(value),'production_extra':True})
            events=sorted(self.events.get(page,[]),key=lambda e:e[0])
            for offset,target,block,answer in events:
                destination=self.documents.get(target) or next(r for r in self.payload['reference_groups'] if r['id']==target)
                if answer:destination['answer_blocks'].append(block)
                else:destination['body_blocks'].append(block)
            visible=[e for e in events if not e[3]]
            if visible:self.page_target[page]={'content_id':visible[0][1],'block_id':visible[0][2]['metadata']['id']}
            elif events:
                self.page_target[page]={'content_id':events[0][1],'block_id':events[0][2]['metadata']['id']}
            else:self.page_target[page]={'content_id':parent,'block_id':None}
    def support_document(self,id,title):
        node=self.known[id];loc=node['source_location']
        doc={'id':id,'kind':'front_matter','module_id':None,'title':title,'order':1,'objectives':[],'body_blocks':[],'answer_blocks':[],'source_ids':[],'asset_bindings':[],'related_content':[],'content_version':self.payload['source_curriculum']['content_version'],'revision':'complete-9B-v1','origin':origin(loc['path'],'json:'+loc['json_pointer'],node['pdf_evidence_page'])}
        self.documents[id]=doc
        return doc
    def supporting_hubs(self):
        for n in range(1,11):
            module=f'M{n:02d}';id=module+'-answers';d=self.support_document(id,'Answers and review guidance');links=[]
            for parent in [module+f'-L{k:02d}' for k in range(1,5)]+[module+'-R']:
                answer=self.documents[parent]['answer_blocks'][0]
                links.append({'label':[{'type':'text','text':parent+' · '+('Review guide' if parent.endswith('-R') else 'Answer')}],'target':{'type':'internal','target':{'content_id':parent,'block_id':answer['metadata']['id']}}})
            d['body_blocks']=[{'metadata':self.metadata(id+'/review-links',d['origin']),'payload':{'type':'related_links','links':links}}]
            if n<=2:
                id=module+'-references';d=self.support_document(id,'Official references' if n==1 else 'References and vehicle handbooks')
                source=read('docs/curriculum/app-migration/implementation-evidence/'+('9B2' if n==1 else '9B3')+'/sources.json')
                bindings=[r for r in source['destinations'] if any(b['scope_id']==module for b in r['scoped_urls'])]
                for i in range(0,len(bindings),4):
                    loc=copy.deepcopy(d['origin']);loc['pdf_evidence_page']+=i//4
                    links=[{'label':[{'type':'text','text':r['title']}],'target':{'type':'external_source','reference_id':next(b['reference_id'] for b in r['scoped_urls'] if b['scope_id']==module)}} for r in bindings[i:i+4]]
                    d['body_blocks'].append({'metadata':self.metadata(id+'/sources-'+str(i//4+1),loc),'payload':{'type':'related_links','links':links}})
            self.documents[module]['related_content']+=[{'content_id':module+'-answers','block_id':None},{'content_id':module+'-references','block_id':None}]

    def cover(self):
        path='docs/curriculum/pdf-design/5b/cover-opening-v4.png';bundled=self.bundle(path)
        loc=origin('docs/curriculum/pdf-production/build.py','line:99-106',1);self.frozen(loc['file']['path'])
        self.assets['cover/illustration']={'id':'cover/illustration','kind':'contextual_illustration','code_or_illustration_id':'cover-opening-v4','variant':'approved landscape window','original':file(path),'bundled':bundled,'caption_id':'cover/illustration-caption','study_alt_text':'Cover landscape','translation_status':'not_applicable','reuse':[{'evidence':loc,'conditions':'Retain the exact approved production polygon; generated typography stays outside the visible region.','credit':'KörkortGo; built-in imagegen artwork.'}],'rendering':{'preserve_geometry_and_colours':True,'contain_without_crop':False,'maximum_print_size_mm':None,'notes':['Decorative cover landscape; title and subtitle remain editable text. Polygon derived exactly from the approved PDF template transform.']},'approval':[{'record':loc,'reviewed_on':None}]}
        w,h=struct.unpack('>II',(ROOT/path).read_bytes()[16:24])
        payload={'type':'polygon_image','asset_id':'cover/illustration','region':{'left':25,'top':295,'right':735,'bottom':1040,'source_width':w,'source_height':h},'polygon':[{'x':x,'y':y} for x,y in [(25,1040),(735,1040),(735,295),(600,390),(25,390)]],'caption':[]}
        self.documents['cover']['body_blocks'].append({'metadata':self.metadata('cover/illustration',loc),'payload':payload});self.documents['cover']['asset_bindings']=['cover/illustration']

    def check_coverage(self):
        for row in self.pages[40:]:
            page=row['page'];text=norm(row['body']);counts=[0]*len(text)
            spans=[r for r in self.matches+self.sign_spans+self.omissions if r['page']==page]
            for span in spans:
                for i in range(span['offset'],span['offset']+span['characters']):counts[i]+=1
            missing=sum(not c.isspace() and counts[i]==0 for i,c in enumerate(text));duplicates=sum(not c.isspace() and counts[i]>1 for i,c in enumerate(text))
            self.coverage.append({'page':page,'missing_characters':missing,'duplicate_characters':duplicates,'normalized_text_sha256':hashlib.sha256(text.encode()).hexdigest()})
            if missing or duplicates:self.missing.append({'id':'production-coverage','page':page,'text':f'missing={missing}; duplicate={duplicates}'})

    def anchors(self):
        existing=set(self.documents)|{r['id'] for r in self.payload['reference_groups']}
        self.payload['anchors']=[]
        # Original M01/M02 supporting pages resolve to the preserved typed block that owns the passage.
        for node in self.registry['supporting_destinations']:
            if node['id'] in existing:continue
            page=node['pdf_evidence_page']
            if page<=40:
                id=node['id'];parent=id.split('-')[0] if 'references' in id or 'answers' in id else id[:7] if re.match(r'M\d{2}-L',id) else id[:3]+'-R'
                d=self.documents[parent];candidates=[b for b in d['body_blocks'] if b['metadata']['origin'].get('pdf_evidence_page')==page]
                if not candidates:
                    if 'answers' in id:target={'content_id':id[:3]+'-L01','block_id':self.documents[id[:3]+'-L01']['answer_blocks'][0]['metadata']['id']}
                    elif 'references' in id:
                        hub=self.documents[id[:3]+'-references'];block=next(b for b in hub['body_blocks'] if b['metadata']['origin']['pdf_evidence_page']==page);target={'content_id':hub['id'],'block_id':block['metadata']['id']}
                    elif 'reflection' in id:target={'content_id':id[:3]+'-R','block_id':id[:3]+'-R/reflection-heading'}
                    elif 'sleep' in id:target={'content_id':parent,'block_id':parent+'/sleep-heading'}
                    elif 'systems' in id:target={'content_id':parent,'block_id':parent+'/systems-heading'}
                    else:target={'content_id':parent,'block_id':parent+'/application-heading'}
                else:target={'content_id':parent,'block_id':candidates[0]['metadata']['id']}
            else:
                target=self.page_target[page]
                if node['id'].startswith('LP'):
                    placement=next((r for r in read(PLACEMENT)['lesson_placements'] if r['placement_id']==node['id']),None)
                    if placement:
                        first='sign-'+placement['items'][0]['code'];event=next((e for e in self.events.get(page,[]) if e[2].get('payload',{}).get('type')=='sign_examples' and first in e[2]['payload']['entry_ids']),None)
                        if event:target={'content_id':event[1],'block_id':event[2]['metadata']['id']}
            loc=node['source_location'];self.payload['anchors'].append({'id':node['id'],'target':target,'origin':origin(loc['path'],'json:'+loc['json_pointer'],page)})
    def run(self):
        for p in [PDF,REGISTRY,QM,MS,CAPS,PLACEMENT]:self.frozen(p)
        self.sign_assets();self.modules();self.appendices();self.groups();self.cover()
        # Rebind existing contextual sheets without changing their teaching/identity metadata.
        for a in self.assets.values():
            if a['kind']=='contextual_illustration' and not a['bundled']['path'].startswith(RESOURCE):a['bundled']=self.bundle(a['original']['path'])
        self.strip_sign_examples();self.finish_pages();self.check_coverage();self.supporting_hubs();self.anchors()
        self.payload['documents']=list(self.documents.values());self.payload['assets']=list(self.assets.values())
        for d in self.payload['documents']:
            if d['id'] in [r['id'] for r in read(str((HERE/'incoming-curriculum.json').relative_to(ROOT)))['documents'] if r['body_blocks']]:continue
            d['source_ids']=list(dict.fromkeys(v for v in all_values(d['body_blocks'],'source_id') if v))
            d['asset_bindings']=list(dict.fromkeys(v for v in all_values(d['body_blocks'],'asset_id') if v))
            d['related_content']=[]
        self.state['step']='9B17';self.state['status']='complete_teaching_import; source_and_artwork_prerequisites_imported';self.state['pending_reading_nodes']=[]
        self.state['completed_appendix_imports']=[{'id':'appendix-'+chr(65+i),'step':'9B'+str(12+i)} for i in range(4)]
        self.state['prerequisites']={'9C1':'imported','9C2':'imported','9C3':'bundled_exact_bytes','9C4':'bundled_exact_bytes; runtime_delivery_pending'}
        self.state['deferred']=[r for r in self.state['deferred'] if r['id']=='question-bank']
        return self.payload,self.state,self.sources
    def stage(self):
        paths={'curriculum':ROOT/'content/curriculum.json','sources':ROOT/'content/sources.json',**{k:HERE/(k+'.json') for k in ['questions','legacy_aliases']}}
        inputs=[AUTHORITY,REGISTRY,BASELINE,ACTIONS,QM,'docs/curriculum/app-migration/link-and-progress-map.json',*MODEL_PATHS,'tools/import_curriculum_remaining.py','tools/compile_curriculum.py','tools/content_schema.py','content/curriculum-import-state.json',*sorted(self.inputs-{REGISTRY,QM})]
        inputs=list(dict.fromkeys(inputs))
        manifest={'schema_version':1,'identity':{'content_version':'staging-9B17-complete-reading','manifest_sha256':'0'*64},'source_curriculum':self.payload['source_curriculum'],'inputs':[file(p) for p in inputs],
            'payloads':[{'kind':k,'file':file(str(v.relative_to(ROOT)))} for k,v in paths.items()]+[{'kind':'asset','file':file(p)} for p in dict.fromkeys(a['bundled']['path'] for a in self.payload['assets'])],
            'canonical_revisions':[{'id':d['id'],'revision':d['revision']} for d in self.payload['documents']+self.payload['reference_groups']]+[{'id':r['id'],'revision':'complete-9B-v1'} for r in self.payload['anchors']+self.payload['sign_entries']+self.sources['destinations']],
            'question_revisions':[],'source_bindings':[{'source_id':s['id'],**b} for s in self.sources['destinations'] for b in s['scoped_urls']],
            'asset_bindings':[{'id':a['id'],'file':a['bundled']} for a in self.payload['assets']]}
        manifest['identity']['manifest_sha256']=manifest_digest(manifest);path=HERE/'staging-manifest.json';path.write_text(encoded(manifest))
        return compile_files(paths,path,HERE/'generated',HERE/'trace.json',symbol='stagedCurriculum9B17')

def main():
    p=argparse.ArgumentParser(description=__doc__);mode=p.add_mutually_exclusive_group();mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true');args=p.parse_args()
    job=Import();payload,state,sources=job.run()
    if args.check:
        if payload!=read('content/curriculum.json') or state!=read('content/curriculum-import-state.json') or sources!=read('content/sources.json') or job.missing:raise ValueError('Complete import differs from frozen production inputs')
        for target,source in job.copies.items():
            if sha(target)!=sha(source):raise ValueError('Bundled byte drift: '+target)
        print('PASS: complete import and bundled artwork reproduce without writes.');return 0
    (HERE/'import-diagnostics.json').write_text(encoded({'missing':job.missing,'source_blocks':job.parity,'matches':job.matches,'sign_examples':job.claims,'coverage':job.coverage,'print_metadata':job.omissions}))
    print(json.dumps({'missing':len(job.missing),'source_blocks':len(job.parity),'production_fragments':len(job.matches),'sign_examples':len(job.claims),'documents':len(payload['documents'])}))
    if job.missing:
        print(json.dumps(job.missing[:10],ensure_ascii=False,indent=2));return 1
    if args.write:
        previous=read(str((HERE/'staging-manifest.json').relative_to(ROOT))) if (HERE/'staging-manifest.json').exists() else None
        for key,live in [('curriculum','content/curriculum.json'),('sources','content/sources.json')]:
            if (ROOT/live).exists():
                allowed={hashlib.sha256(encoded(payload if key=='curriculum' else sources).encode()).hexdigest()}
                if key=='curriculum':allowed.add(sha(str((HERE/'incoming-curriculum.json').relative_to(ROOT))))
                if previous:allowed.update(r['file']['sha256'] for r in previous['payloads'] if r['kind']==key)
                if sha(live) not in allowed:raise ValueError('Refusing to overwrite edited authoring payload: '+live)
        for path,source in job.copies.items():
            dest=ROOT/path
            if dest.exists() and sha(path)!=sha(source):raise ValueError('Resource collision: '+path)
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():shutil.copyfile(ROOT/source,dest)
        (ROOT/'content/curriculum.json').write_text(encoded(payload));(ROOT/'content/curriculum-import-state.json').write_text(encoded(state));(ROOT/'content/sources.json').write_text(encoded(sources))
        for key,value in {'questions':{'schema_version':1,'questions':[]},'legacy_aliases':{'schema_version':1,'aliases':[],'tombstones':[]}}.items():(HERE/(key+'.json')).write_text(encoded(value))
        (HERE/'allocation-ledger.json').write_text(encoded({'production_block_counts':job.allocations,'origins':job.matches}))
        print(job.stage())
    return 0
if __name__=='__main__':raise SystemExit(main())
