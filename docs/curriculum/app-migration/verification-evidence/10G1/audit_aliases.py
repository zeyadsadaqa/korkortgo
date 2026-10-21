"""Independent 7E/registry oracle; no navigation emitter or resolver helper imported."""
import collections,hashlib,json,sys
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent
read=lambda p:json.loads((ROOT/p).read_text());sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
m=read('docs/curriculum/app-migration/link-and-progress-map.json');compiled=read(str(HERE.relative_to(ROOT)/'compiled-alias-observations.json'));raw=read('content/legacy-aliases.json');curr=read('content/curriculum.json');sources=read('content/sources.json');extra=read('content/legacy-sources.json');refs={r['id']:r for r in sources['references']+extra['references']};anchors={a['id']:a['target'] for a in curr['anchors']};namespace=m['legacy_namespace']['id'];bank={q['key']['question_id']:q for q in read('content/accepted-assessment-questions.json')['questions']};rows=[];checks=[]
def check(name,ok):checks.append({'case_id':f'10G1-{len(checks)+1:05}','name':name,'status':'pass' if ok else 'fail'})
def target(id):return {'content_id':id,'block_id':None}
def blockids(v):
 if isinstance(v,dict):
  if isinstance(v.get('metadata'),dict) and 'id' in v['metadata']:yield v['metadata']['id']
  for w in v.values():yield from blockids(w)
 elif isinstance(v,list):
  for w in v:yield from blockids(w)
entries={}
for group,kind in [(curr['documents'],'curriculum'),(curr['reference_groups'],'reference_group'),(curr['sign_entries'],'sign'),(sources['destinations'],'source')]:
 for e in group:entries[e['id']]={'id':e['id'],'title':e.get('title',e.get('english_label')),'kind':kind,'blocks':sorted(set(blockids(e)))}
actualentries={e['id']:{**e,'blocks':sorted(e['blocks'])} for e in compiled['entries']}
check('Fresh exact compiled canonical registry/anchors',actualentries==entries and compiled['anchors']==anchors)
check('Canonical destination parity remains exact against10B1', {r['id']:r['target'] for r in read('docs/curriculum/app-migration/verification-evidence/10B1/compiled-destinations.json')}=={**{id:target(id) for id in entries},**anchors})
check('Exact1921 unique aliases/no production tombstones',len(raw['aliases'])==len(compiled['aliases'])==1921 and raw['tombstones']==compiled['tombstones']==m['production_tombstones']==[])
check('Current accepted identity pinned',compiled['identity']==read('content/accepted-content-manifest.json')['identity'])
bylookup=lambda l:json.dumps(l,sort_keys=True)
observed={bylookup(a['lookup']):a for a in compiled['aliases']};authoring={bylookup(a['lookup']):a for a in raw['aliases']}
check('Distinct typed lookups',len(observed)==len(authoring)==1921)
gaps={g['legacy_code']:g for g in m['unresolved_destinations']};specs=[]
for i,r in enumerate(m['chapter_aliases']):specs.append(('chapter_aliases',i,{'type':'chapter','namespace':namespace,'title':r['legacy_title']},r['target_ids'],None))
for i,r in enumerate(m['legacy_page_aliases']):specs.append(('legacy_page_aliases',i,{'type':'page','namespace':namespace,'page':r['legacy_page']},r['target_ids'],None))
for i,r in enumerate(m['unused_topic_routes']):specs.append(('unused_topic_routes',i,{'type':'topic','namespace':namespace,'row_id':str(r['legacy_topic_index'])},[r['target_id']],None))
for i,r in enumerate(m['sign_routes']):specs.append(('sign_routes',i,{'type':'sign','namespace':namespace,'code':r['legacy_code']},[r['target_id']] if r['target_id'] else [],gaps.get(r['legacy_code'])))
for i,r in enumerate(m['question_routes']):specs.append(('question_routes',i,{'type':'question','question_id':r['question_id']},[r['target_id']],None))
for family,index,lookup,ids,gap in specs:
 start=len(checks);a=observed[bylookup(lookup)];j=authoring[bylookup(lookup)];out=a['actual'];origin={'file':{'path':'docs/curriculum/app-migration/link-and-progress-map.json','sha256':sha('docs/curriculum/app-migration/link-and-progress-map.json')},'locator':f'json:/{family}/{index}','evidence_ids':[],'pdf_evidence_page':None}
 check(str(lookup)+' exact accepted alias/provenance',a['origin']==j['origin']==origin and a['declared_outcome']==j['outcome'])
 targets=[anchors.get(id,target(id)) for id in ids]
 if len(ids)==1:
  check(str(lookup)+' exact scoped content target',out['type']=='found' and out['target']==targets[0] and out['entry']==actualentries[targets[0]['content_id']] and out['notice'] is None)
  expected={'type':'found','target':targets[0]}
 elif len(ids)>1:
  check(str(lookup)+' ordered chooser no automatic first target',out['type']=='choices' and [x['target'] for x in out['choices']]==targets and all(x['entry']==actualentries[x['target']['content_id']] and x['notice'] is None for x in out['choices']) and bool(out['notice']))
  expected={'type':'choices','targets':targets}
 else:
  check(str(lookup)+' explicit unavailable no guessed neighbour',out['type']=='unavailable' and out['message']==j['outcome']['message'] and bool(out['message']))
  if gap:check(str(lookup)+' exact official action/related teaching',refs[out['official_reference_id']]['url']==gap['legacy_external_url'] and out['message']==gap['learner_message'] and out['related']==[target(id) for id in gap['related_target_ids']])
  else:check(str(lookup)+' no invented external or related fallback',out['official_reference_id'] is None and out['related']==[])
  expected={'type':'unavailable','policy':'unavailable_exact_entry' if gap else 'unavailable_page_gap','official_url':gap['legacy_external_url'] if gap else None,'related':[target(id) for id in gap['related_target_ids']] if gap else []}
 rows.append({'family':family,'source_locator':f'json:/{family}/{index}','lookup':lookup,'expected':expected,'actual':out,'check_ids':[c['case_id'] for c in checks[start:]],'status':'pass' if all(c['status']=='pass' for c in checks[start:]) else 'fail'})
questionrows=[]
for i,r in enumerate(m['question_routes']):
 q=compiled['questions'][i];accepted=bank[r['question_id']];rel=q['relationship'];start=len(checks)
 check(r['question_id']+' exact current question routing/accepted revision',q['key']==accepted['key'] and q['accepted_status']=='accepted' and q['concept_id']==r['concept_id'] and rel==accepted['relationship'] and rel['primary_lesson_id']==r['target_id'] and rel['related_lesson_ids']==r['related_target_ids'] and rel['reference_ids']==r['reference_target_ids'] and rel['source_ids']==r['source_ids'])
 check(r['question_id']+' context overrides old page',q['legacy_page']==r['legacy_page'] and q['actual']==q['with_page_context'] and q['actual']['type']=='found' and q['actual']['target']==target(r['target_id']))
 for field,ids in [('related',r['related_target_ids']),('references',r['reference_target_ids']),('sources',r['source_ids'])]:check(r['question_id']+' exact '+field+' targets',[x['target'] for x in q[field] if x['type']=='found']==[anchors.get(id,target(id)) for id in ids] and all(x['type']=='found' for x in q[field]))
 questionrows.append({**q,'source_locator':f'json:/question_routes/{i}','check_ids':[c['case_id'] for c in checks[start:]],'status':'pass' if all(c['status']=='pass' for c in checks[start:]) else 'fail'})
report={'task':'10G1','status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','identity':compiled['identity'],'manifest_file_sha256':sha('content/accepted-content-manifest.json'),'oracle':'Frozen7E decisions plus canonical content and10B1 targets; not current alias outcomes alone or emitter parity.','counts':{'compatibility_records':len(rows),'families':dict(collections.Counter(r['family'] for r in rows)),'question_routes':len(questionrows),'checks':len(checks),'failed':sum(c['status']=='fail' for c in checks)},'aliases':rows,'questions':questionrows,'checks':checks,'limits':'Typed internal resolver/compiled bank proof; no public URI parser, new asset, external-link availability or platform runtime inferred.'}
(HERE/'complete-alias-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'counts':report['counts'],'failures':[c for c in checks if c['status']=='fail'][:12]},indent=2));sys.exit(0 if report['status']=='pass' else 1)
