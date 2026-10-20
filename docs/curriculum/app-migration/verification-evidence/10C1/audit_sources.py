"""10C1 independent source binding/classification audit; never changes accepted content."""
import hashlib,json,re,sys
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
@lru_cache(None)
def read(p):return json.loads((ROOT/p).read_text())
@lru_cache(None)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def pointer(v,p):
 for k in p.lstrip('/').split('/') if p else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
s=read('content/package-sources.json');refs={r['id']:r for r in s['references']};dest={r['id']:r for r in s['destinations']};registry=read('docs/curriculum/app-migration/curriculum-map.json');qm=read('docs/curriculum/app-migration/question-map.json');qmap={q['question_id']:q for q in qm['questions']};questions=read('content/accepted-assessment-questions.json')['questions'];actions={r['question_id']:r for r in read('docs/curriculum/app-migration/question-actions.json')['questions']};compiled=read(str((HERE/'compiled-source-bindings.json').relative_to(ROOT)))
checks=[];uses=[]
def check(name,ok,expected=None,observed=None):
 checks.append({'case_id':'10C1-'+str(len(checks)+1).zfill(5),'name':name,'status':'pass' if ok else 'fail','expected':expected,'observed':observed})
def origin(o,name):
 f=o['file'];check(name+' origin bytes',sha(f['path'])==f['sha256'],f['sha256'],sha(f['path']))
 if o['locator'].startswith('json:'):return pointer(read(f['path']),o['locator'][5:])
 return None
check('519 unique reference identities',len(refs)==len(s['references'])==519,519,len(refs))
check('116 unique canonical source destinations',len(dest)==len(s['destinations'])==116,116,len(dest))
check('Actual compiled source payload exact JSON parity',compiled['sources']==s,hashlib.sha256(canonical(s).encode()).hexdigest(),hashlib.sha256(canonical(compiled['sources']).encode()).hexdigest())
base=read('content/sources.json');legacy=read('content/legacy-sources.json');check('Package retains base records plus three explicit compatibility references',s['references']==base['references']+legacy['references'] and s['destinations']==base['destinations'],{'base':516,'compatibility':3},{'base':len(base['references']),'compatibility':len(legacy['references'])})
for old in qm['source_registry']:
 r=refs.get(old['id']);check(old['id']+' exact 7C URL identity',r is not None and r['url']==old['url'],old['url'],r['url'] if r else None)
 for row in old['source_checks']:
  actual=pointer(read(row['path']),row['json_pointer']);check(old['id']+' frozen 7C source-check locator',actual==row['record'],{'path':row['path'],'pointer':row['json_pointer']},'exact match' if actual==row['record'] else 'drift')
for d in registry['source_destinations']:
 actual=dest[d['id']];bindings={b['scope_id']:refs[b['reference_id']]['url'] for b in actual['scoped_urls']}
 check(d['id']+' exact scoped alias URLs',bindings==d['scoped_urls'],d['scoped_urls'],bindings)
for ref in refs.values():
 check(ref['id']+' stable exact URL hash identity',ref['id']=='REF-'+hashlib.sha256(ref['url'].encode()).hexdigest()[:16],ref['url'],ref['id'])
 check(ref['id']+' publisher/classification/scope present',bool(ref['publisher']) and bool(ref['classifications']) and bool(ref['classification_note']) and bool(ref['evidence']),True,{'publisher':ref['publisher'],'classifications':ref['classifications']})
 for i,e in enumerate(ref['evidence']):
  raw=origin(e['origin'],ref['id']+f' evidence {i}')
  if isinstance(raw,dict):
   for field,aliases in [('checked_on',['checked_on','reviewed_on']),('retrieved_on',['retrieved_on','retrieved']),('published_on',['published_on'])]:
    value=next((raw[k] for k in aliases if raw.get(k)),None)
    if value and re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(value)):
     # Earlier bounded imports may inherit checked dates from the owning chapter; explicit values are never replaced.
     check(ref['id']+f' evidence {i} retains explicit {field}',e['dates'][field]==value,value,e['dates'][field])
  check(ref['id']+f' evidence {i} preserves dated scope',bool(e['scope']) and all(v is None or re.fullmatch(r'\d{4}-\d{2}-\d{2}',v) for v in e['dates'].values()),'Recorded dates or null; passage scope retained',e['dates'])
compiled_q={r['key']['question_id']:r for r in compiled['questions']}
receipt_rows={}
for p in [*[f'docs/curriculum/app-migration/implementation-evidence/9E{n}/batch-acceptance.json' for n in range(1,13)],'docs/curriculum/app-migration/implementation-evidence/9G/question-acceptance.json',*[f'docs/curriculum/app-migration/implementation-evidence/9H/9H{n}/question-acceptance.json' for n in range(1,7)],*[f'docs/curriculum/app-migration/implementation-evidence/9I/9I{n}/question-acceptance.json' for n in range(1,6)]]:
 for row in read(p)['questions']:receipt_rows[row['question_id']]=(p,row)
def examine(use,owner,location):
 ref=refs.get(use['reference_id']);ok=ref is not None
 if use['source_id'] is not None:
  d=dest.get(use['source_id']);ok=ok and d is not None and any(b['scope_id']==use['scope_id'] and b['reference_id']==use['reference_id'] for b in d['scoped_urls'])
 else:ok=ok and use['scope_id'] is None
 check(owner+' '+location+' exact reference/scope resolves',ok,{'reference_id':use['reference_id'],'source_id':use['source_id'],'scope_id':use['scope_id']},ref['url'] if ref else None)
 uses.append({'owner':owner,'location':location,'binding':use,'resolved_url':ref['url'] if ref else None,'status':'pass' if ok else 'fail'})
for q in questions:
 qid=q['key']['question_id'];m=qmap[qid];rel=q['relationship'];cq=compiled_q[qid]
 check(qid+' actual compiled accepted source fields',cq=={'key':q['key'],'relationship':rel,'option_source_uses':{f['option_id']:f['source_uses'] for f in q['feedback']['option_feedback']}},q['key'],cq['key'])
 check(qid+' exact mapped reference order',[u['reference_id'] for u in rel['source_uses']]==m['source_reference_ids'],m['source_reference_ids'],[u['reference_id'] for u in rel['source_uses']])
 check(qid+' exact mapped source destination IDs',rel['source_ids']==m['source_ids'],m['source_ids'],rel['source_ids'])
 for i,use in enumerate(rel['source_uses']):
  examine(use,qid,'relationship/'+str(i));mapped=next((e for e in m['source_evidence'] if e['reference_id']==use['reference_id']),{})
  if mapped.get('source_id'):check(qid+' exact 7C source scope '+str(i),use['source_id']==mapped['source_id'] and use['scope_id']==mapped['scope'],{'source_id':mapped['source_id'],'scope':mapped['scope']},{'source_id':use['source_id'],'scope':use['scope_id']})
 for f in q['feedback']['option_feedback']:
  for i,use in enumerate(f['source_uses']):examine(use,qid,f['option_id']+'/'+str(i))
 disposition=actions[qid]['disposition']
 if disposition=='retain':
  check(qid+' retained option source bindings agree with mapped evidence',all(f['source_uses']==rel['source_uses'] for f in q['feedback']['option_feedback']),True,True if all(f['source_uses']==rel['source_uses'] for f in q['feedback']['option_feedback']) else False)
 elif qid in receipt_rows:
  path,row=receipt_rows[qid];assessment=row['after']['assessment'];expected={f['option_id']:f['source_uses'] for f in assessment['feedback']['option_feedback']};observed={f['option_id']:f['source_uses'] for f in q['feedback']['option_feedback']}
  check(qid+' exact per-ID approved feedback sources',expected==observed,{'receipt':path,'question_id':qid},'exact match' if expected==observed else observed)
 else:
  proposal=actions[qid]['proposed_changes'];expected={o['option_id']:[r['url'] for r in o['official_sources']] for o in proposal['options']};observed={f['option_id']:[refs[u['reference_id']]['url'] for u in f['source_uses']] for f in q['feedback']['option_feedback']}
  check(qid+' exact 7D replacement option source URLs',expected==observed,expected,observed)
# Independent classification decisions from retained named publisher/origin evidence, not the importer hostname fallback.
corrections={
 'REF-496b85361fc1b2c5':('swedish_public_service','Gagnefs kommun is Swedish municipal advice, not foreign guidance.'),
 'REF-2816f9478f49eea3':('swedish_public_service','Göteborgs Stad environmental guidance is Swedish municipal advice.'),
 'REF-56e38aa92cb10d3e':('swedish_authority_guidance','Named Swedish Energy Agency/municipal energy advice is domestic guidance.'),
 'REF-6ca8f251127184be':('swedish_authority_guidance','Named MFD guidance is from a Swedish public agency.'),
 'REF-b3162b40db29d9bd':('swedish_authority_guidance','Primary PDF identifies Trafikverket KRAV Grundvärden VGU, publication 2024:148, version 1.0; domestic infrastructure requirements, not foreign guidance, research, or general driver legislation.'),
 'REF-52a2a9e7d845ad8f':('manufacturer','Kia MQ4/2022 owner handbook is model-specific manufacturer guidance, not a public authority.')}
for rid,(expected,basis) in corrections.items():check(rid+' independent publisher/jurisdiction/type classification',expected in refs[rid]['classifications'],{'classification':expected,'basis':basis},{'classifications':refs[rid]['classifications'],'publisher':refs[rid]['publisher'],'url':refs[rid]['url']})
examples=read('docs/curriculum/app-migration/verification-evidence/10A3/runtime-matrix.json')['source_class_matrix']['frozen_examples']
for e in examples:
 r=refs[e['reference_id']];check(e['case_class']+' frozen representative scope/classification unchanged',r['url']==e['url'] and r['publisher']==e['publisher'] and r['classifications']==e['recorded_classifications'],e,{'reference_id':r['id'],'classifications':r['classifications']})
prepared=read('docs/curriculum/app-migration/verification-evidence/10A3/data-cases.json');cases=[]
for family in prepared['families']:
 if family['gate']!='T02':continue
 for member in family['members']:
  related=[c for c in checks if c['name'].startswith(member['subject']+' ')]
  cases.append({**member,'status':'fail' if any(c['status']=='fail' for c in related) else 'pass','evidence_checks':[c['case_id'] for c in related]})
report={'task':'10C1','candidate_manifest_sha256':sha('content/accepted-content-manifest.json'),'date':'2026-10-20','status':'fail' if any(c['status']=='fail' for c in checks) else 'pass','counts':{'references':len(refs),'canonical_sources':len(dest),'original_question_URLs':len(qm['source_registry']),'questions':len(questions),'uses':len(uses),'checks':len(checks),'passed':sum(c['status']=='pass' for c in checks),'failed':sum(c['status']=='fail' for c in checks)},'checks':checks,'prepared_cases':cases,'source_uses':uses,'classification_corrections':[{'reference_id':r,'expected_classification':v[0],'basis':v[1],'current_classifications':refs[r]['classifications'],'source_record':refs[r]} for r,v in corrections.items()]}
dump(HERE/'source-binding-audit.json',report)
print(json.dumps({'status':report['status'],'counts':report['counts'],'failures':[c for c in checks if c['status']=='fail'][:20]},ensure_ascii=False,indent=2))
sys.exit(0 if report['status']=='pass' else 1)
