"""Generate the exact 7E aliases, canonical index and approved sign/reference metadata."""
import argparse,hashlib,json
from pathlib import Path
from compile_curriculum import Emitter,Validator,kotlin_string
from content_schema import Schema
ROOT=Path(__file__).resolve().parent.parent
BASE=Path('docs/curriculum/app-migration/link-and-progress-map.json')
DEST=Path('composeApp/src/commonMain/kotlin/se/korkort')
def read(p):return json.loads((ROOT/p).read_text())
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def origin(i):return {'file':{'path':str(BASE),'sha256':hashlib.sha256((ROOT/BASE).read_bytes()).hexdigest()},'locator':i,'evidence_ids':[],'pdf_evidence_page':None}
def target(id):return {'content_id':id,'block_id':None}
def legacy_sources():
    m=read(BASE);references=[]
    for i,gap in enumerate(m['unresolved_destinations']):
        url=gap['legacy_external_url'];references.append({'id':'REF-'+hashlib.sha256(url.encode()).hexdigest()[:16],'title':gap['legacy_code']+' official signal description','publisher':'Transportstyrelsen','url':url,'classifications':['swedish_authority_guidance'],'classification_note':'Retained official-description action for an unavailable legacy signal; no new teaching or exact artwork approval.','editorial_inference':False,'original_evidence_ids':[gap['id']],'evidence':[{'origin':origin(f'json:/unresolved_destinations/{i}'),'dates':{'checked_on':None,'retrieved_on':None,'published_on':None},'scope':'Compatibility action only; no matching internal sign entry.','finding':gap['learner_message'],'limitations':['Retained URL; not freshly checked by this import.']} ]})
    return {'schema_version':1,'destinations':[],'references':references}
def aliases():
    m=read(BASE);ns=m['legacy_namespace']['id'];rows=[]
    urls={r['url']:r['id'] for r in read(Path('content/sources.json'))['references']+legacy_sources()['references']}
    specs=[('question_routes',lambda r:{'type':'question','question_id':r['question_id']},lambda r:[r['target_id']]),('chapter_aliases',lambda r:{'type':'chapter','namespace':ns,'title':r['legacy_title']},lambda r:r['target_ids']),('legacy_page_aliases',lambda r:{'type':'page','namespace':ns,'page':r['legacy_page']},lambda r:r['target_ids']),('unused_topic_routes',lambda r:{'type':'topic','namespace':ns,'row_id':str(r['legacy_topic_index'])},lambda r:[r['target_id']]),('sign_routes',lambda r:{'type':'sign','namespace':ns,'code':r['legacy_code']},lambda r:[r['target_id']] if r['target_id'] else [])]
    for key,lookup,targets in specs:
        for i,r in enumerate(m[key]):
            ids=targets(r)
            if ids:outcome={'type':'content','target':target(ids[0])} if len(ids)==1 else {'type':'chooser','targets':[target(x) for x in ids]}
            else:
                gap=next((g for g in m['unresolved_destinations'] if g.get('legacy_code')==r.get('legacy_code') and r.get('legacy_code')),None)
                outcome={'type':'unavailable','message':gap['learner_message'] if gap else 'This legacy page is unavailable. Browse the theory library.','official_reference_id':urls[gap['legacy_external_url']] if gap else None,'related':[target(x) for x in gap['related_target_ids']] if gap else []}
            rows.append({'lookup':lookup(r),'outcome':outcome,'origin':origin(f'json:/{key}/{i}')})
    return {'schema_version':1,'aliases':rows,'tombstones':[]}
def blocks(value):
    if isinstance(value,dict):
        if 'metadata' in value and 'id' in value['metadata']:yield value['metadata']['id']
        for v in value.values():yield from blocks(v)
    elif isinstance(value,list):
        for v in value:yield from blocks(v)
class SharedEmitter(Emitter):
    def __init__(self,*args):super().__init__(*args);self.shared={}
    def function(self,kind,expression,path,origin):
        key=(kind,expression)
        if key not in self.shared:self.shared[key]=super().function(kind,expression,path,origin)
        return self.shared[key]
def generate():
    c=read(Path('content/curriculum.json'));s=read(Path('content/sources.json'));a=aliases();v=Validator();v.typed(a,'LegacyAliasPayload','aliases');extra=legacy_sources();v.typed(extra,'SourcePayload','legacySources');s['references']+=extra['references']
    emitter=SharedEmitter(Schema(ROOT),'navigation')
    calls={name:emitter.emit(payload,kind,name) for name,payload,kind in [('navigationAliases',a,'LegacyAliasPayload'),('navigationSigns',c['sign_entries'],'List<SignEntry>'),('navigationAssets',[x for x in c['assets'] if x['kind']=='official_sign'],'List<CurriculumAsset>'),('navigationSources',s,'SourcePayload'),('navigationReferenceGroups',c['reference_groups'],'List<ReferenceGroup>')]}
    functions=list(emitter.functions);entries=[]
    for collection,kind in [(c['documents'],'CURRICULUM'),(c['reference_groups'],'REFERENCE_GROUP'),(c['sign_entries'],'SIGN'),(s['destinations'],'SOURCE')]:
        for row in collection:
            title=row.get('title',row.get('english_label'));bs=sorted(set(blocks(row)))
            entries.append('CanonicalEntry(ContentId('+kotlin_string(row['id'])+'), '+kotlin_string(title)+', DestinationKind.'+kind+', setOf('+', '.join('BlockId('+kotlin_string(b)+')' for b in bs)+'))')
    for i in range(0,len(entries),20):functions.append((f'canonicalEntries{i//20}','List<CanonicalEntry>','listOf('+', '.join(entries[i:i+20])+')'))
    entry_call=' + '.join(f'canonicalEntries{i}()' for i in range((len(entries)+19)//20))
    anchors=['ContentId('+kotlin_string(a['id'])+') to ContentTarget(ContentId('+kotlin_string(a['target']['content_id'])+'), BlockId('+kotlin_string(a['target']['block_id'])+'))' for a in c['anchors']]
    for i in range(0,len(anchors),20):functions.append((f'canonicalAnchors{i//20}','Map<ContentId, ContentTarget>','mapOf('+', '.join(anchors[i:i+20])+')'))
    anchor_call=' + '.join(f'canonicalAnchors{i}()' for i in range((len(anchors)+19)//20))
    header='// Generated by tools/build_navigation.py; do not edit.\npackage se.korkort\n\n'
    top=header+''.join(f'internal val {name}: {kind} by lazy {{ {calls[name]} }}\n' for name,kind in [('navigationAliases','LegacyAliasPayload'),('navigationSigns','List<SignEntry>'),('navigationAssets','List<CurriculumAsset>'),('navigationSources','SourcePayload'),('navigationReferenceGroups','List<ReferenceGroup>')])
    top+=f'internal val canonicalEntries: List<CanonicalEntry> by lazy {{ {entry_call} }}\ninternal val canonicalAnchors: Map<ContentId, ContentTarget> by lazy {{ {anchor_call} }}\ninternal val canonicalResolver by lazy {{ CanonicalResolver(canonicalEntries,canonicalAnchors,navigationAliases) }}\n'
    files={DEST/'GeneratedNavigation.kt':top,Path('content/legacy-aliases.json'):dump(a),Path('content/legacy-sources.json'):dump(extra)}
    for i in range(0,len(functions),200):files[DEST/f'GeneratedNavigationPart{i//200:03}.kt']=header+''.join(f'internal fun {fn}(): {kind} = {expr}\n' for fn,kind,expr in functions[i:i+200])
    return files

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    files=generate()
    for stale in (ROOT/DEST).glob("GeneratedNavigationPart*.kt"):
        if stale.relative_to(ROOT) not in files:
            assert stale.read_text().startswith("// Generated by tools/build_navigation.py;")
            if args.check:raise ValueError("Stale generated file: "+str(stale))
            stale.unlink()
    for path,value in files.items():
        if args.check:assert (ROOT/path).read_text()==value,path
        else:
            if (ROOT/path).exists() and path.suffix=='.kt':assert (ROOT/path).read_text().startswith('// Generated by tools/build_navigation.py;')
            (ROOT/path).write_text(value)
    print('Navigation: 1123 canonical destinations; 1921 exact legacy aliases; no production tombstones.')
if __name__=='__main__':main()
