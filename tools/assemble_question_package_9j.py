"""Assemble a complete held candidate; never promote unresolved delivery holds to release acceptance."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from compile_curriculum import Validator, manifest_digest, ContentError
from content_schema import Schema, MODEL_PATHS
from build_navigation import SharedEmitter, blocks
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('docs/curriculum/app-migration/implementation-evidence/9J')
ACTIONS=Path('docs/curriculum/app-migration/question-actions.json')
MAP=Path('docs/curriculum/app-migration/question-map.json')
DEST=Path('composeApp/src/commonMain/kotlin/se/korkort')
def read(p):return json.loads((ROOT/p).read_text())
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def identity(p):return {'path':str(p),'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}
def origin(p,loc):return {'file':identity(p),'locator':loc,'evidence_ids':[],'pdf_evidence_page':None}
def review(p,loc):return {'record':origin(p,loc),'reviewed_on':'2026-10-16'}
def text(s):return [{'type':'text','text':s}] if s else []
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def prepare():
 c=read(Path('content/curriculum.json'));s=read(Path('content/sources.json'));s['references']+=read(Path('content/legacy-sources.json'))['references']
 mappings=read(MAP)['questions'];actions=read(ACTIONS)['questions'];by_action={a['question_id']:(i,a) for i,a in enumerate(actions)}
 bank=read(Path('content/questions.json'));assert [q['id'] for q in bank]==[m['question_id'] for m in mappings]
 identities={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/implementation-evidence/9D1/authored-identities.json'))['questions']}
 descriptions={q['question_id']:(i,q,Path(f'docs/curriculum/app-migration/implementation-evidence/9D{n}/description-acceptance.json')) for n in range(3,16) for i,q in enumerate(read(Path(f'docs/curriculum/app-migration/implementation-evidence/9D{n}/description-acceptance.json'))['questions'])}
 assets={a['original']['sha256']:a for a in c['assets']};refs={r['id']:r for r in s['references']};url_refs={r['url']:r['id'] for r in s['references']}
 known={r['id'] for key in ['documents','reference_groups','sign_entries','anchors'] for r in c[key]}|{r['id'] for r in s['destinations']}
 lessons={r['id'] for r in c['documents'] if r['kind']=='lesson'};source_ids={r['id'] for r in s['destinations']}
 def use(ref,locator,inference=False,preferred=None,scope=None):
  assert ref in refs
  bindings=[(d['id'],b['scope_id']) for d in s['destinations'] for b in d['scoped_urls'] if b['reference_id']==ref]
  exact=next((b for b in bindings if b==(preferred,scope)),None)
  chosen=exact or next((b for b in bindings if b[0]==preferred),None) or next(iter(bindings),None)
  return {'reference_id':ref,'source_id':chosen[0] if chosen else None,'scope_id':chosen[1] if chosen else None,'locator':locator,'editorial_inference':inference}
 receipts={}
 for path in [*[BASE.parent/f'9E{n}/batch-acceptance.json' for n in range(1,13)],BASE.parent/'9G/question-acceptance.json',*[BASE.parent/f'9H/9H{n}/question-acceptance.json' for n in range(1,7)],*[BASE.parent/f'9I/9I{n}/question-acceptance.json' for n in range(1,6)]]:
  for record in read(path)['questions']:receipts[record['question_id']]=(record,path)
 relationships={};questions=[];audit=[];retain_reviews=[]
 for row,m in zip(bank,mappings):
  qid=row['id'];idx,a=by_action[qid];old=a['original'];disposition=a['disposition']
  uses=[]
  for ref in m['source_reference_ids']:
   evidence=next((e for e in m['source_evidence'] if e['reference_id']==ref),{})
   uses.append(use(ref,evidence.get('locator','Exact mapped source URL; scope remains limited to retained question-map evidence.'),any('editorial' in claim.get('classification','') for claim in m['retained_claims']),evidence.get('source_id'),evidence.get('scope')))
  rel={**{k:copy.deepcopy(m[k]) for k in ['primary_lesson_id','related_lesson_ids','reference_ids','source_ids','content_version']},'disposition':disposition,'source_uses':uses}
  assert rel['primary_lesson_id'] in lessons and set(rel['related_lesson_ids'])<=lessons
  assert set(rel['reference_ids'])<=known and set(rel['source_ids'])<=source_ids
  relationships[qid]=rel
  if row.get('assessment'):
   assert receipts[qid][0]['after']==row,(qid,'drift from exact per-ID acceptance receipt')
   q=copy.deepcopy(row['assessment']);q['relationship']=rel
  elif disposition=='retain':
   assert row==old and not row['image'] and not any(o['image'] for o in row['options'])
   ids=identities[qid]['option_ids_in_authored_order'];ri=len(retain_reviews)
   retain_reviews.append({'question_id':qid,'result':'accepted unchanged retained text assessment','review_basis':origin(ACTIONS,f'json:/questions/{idx}'),'fields_preserved':['prompt','four option texts','key','question explanation','four option explanations','concept','category'],'limitations':'Retains the 7D full-question review and source limits; not a new source-currency certification.'})
   q={'key':{'question_id':qid,'revision':'legacy-r1'},'concept_id':row['concept'],'category':row['category'].lower(),'prompt':text(row['prompt']),'image':None,'options':[{'id':oid,'text':text(o['text']),'image':None} for oid,o in zip(ids,row['options'])],
   'feedback':{'target_sign_code':None,'english_label':None,'correct_option_id':ids[row['correct']],'explanation':text(row['explanation']),'option_feedback':[{'option_id':oid,'explanation':text(o['explanation']),'sign_code':None,'english_label':None,'source_uses':uses} for oid,o in zip(ids,row['options'])]},'relationship':rel,
   'acceptance':{'eligibility':'accepted','content_review':None,'description_reviews':[],'delivery_proof':[],'open_holds':[]},'origin':origin(ACTIONS,f'json:/questions/{idx}/original')}
   # Bind review once the aggregate evidence exists, without a circular file digest.
   q['acceptance']['content_review']={'pending_retained_review_index':ri}
  else:
   assert disposition=='replace' and row==old
   p=a['proposed_changes'];di,d,dp=descriptions[qid];assert d['description_result']=='accepted'
   def image(slot):
    pic=next(i for i in d['images'] if i['slot']==slot);asset=assets[pic['asset']['sha256']]
    return {'asset_id':asset['id'],'neutral_description':{'text':pic['description'],'review':review(dp,f'json:/questions/{di}/images/{d["images"].index(pic)}')}}
   options=[{'id':o['option_id'],'text':text(o['meaning_option_text'] or ''),'image':image(o['option_id']) if qid.startswith('sign-recognise-') else None} for o in p['options']]
   q={'key':{'question_id':qid,'revision':'replacement-candidate-r2'},'concept_id':row['concept'],'category':row['category'].lower(),'prompt':text(p['prompt']),'image':image('stem') if p['question_image_asset'] else None,'options':options,
    'feedback':{'target_sign_code':p['target_code_metadata'],'english_label':p['post_answer_english_label'],'correct_option_id':next(o['option_id'] for o in p['options'] if o['is_correct']),'explanation':text(p['post_answer_explanation']),'option_feedback':[{'option_id':o['option_id'],'explanation':text(o['post_answer_explanation']),'sign_code':o['code_metadata_after_reveal'],'english_label':o['post_answer_label'],'source_uses':[use(url_refs[r['url']],'Exact approved 7D proposed sign explanation.') for r in o['official_sources']]} for o in p['options']]},'relationship':rel,
    'acceptance':{'eligibility':'held','content_review':review(ACTIONS,f'json:/questions/{idx}'),'description_reviews':[review(dp,f'json:/questions/{di}')],'delivery_proof':[],'open_holds':[{'id':qid+'/delivery','reason':'9F exact-artwork delivery acceptance remains open. This proposed record has not replaced the original bank question.','release_condition':'Complete the exact-code 9F delivery and reader checks before applying and activating the replacement.'}]},'origin':origin(ACTIONS,f'json:/questions/{idx}/proposed_changes')}
  questions.append(q)
  audit.append({'question_id':qid,'concept_id':row['concept'],'disposition':disposition,'revision':q['key']['revision'],'eligibility':q['acceptance']['eligibility'],'candidate_only':disposition=='replace','live_record_unchanged':not row.get('assessment'),'open_holds':q['acceptance']['open_holds'],'content_review':None})
 return c,s,bank,relationships,questions,audit,retain_reviews

def assemble(check=False):
 files={}
 def output(p,value):
  value=dump(value) if not isinstance(value,str) else value
  if check:assert (ROOT/p).read_text()==value,p
  else:(ROOT/p).parent.mkdir(parents=True,exist_ok=True);(ROOT/p).write_text(value)
  files[p]=value
 c,s,bank,rels,questions,audit,retained=prepare()
 original_authority=Path('docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json')
 authority={'schema_version':1,'original_authority':identity(original_authority),'input_manifest':copy.deepcopy(read(original_authority)['input_manifest'])}
 authority['step']='9J candidate source authority'
 authority['scope']='Revalidates only the evolved content/questions.json against exact 9E–9I per-ID receipts, retaining unchanged originals for 336 retained and 38 held replacements. All other original source-authority identities remain frozen.'
 for record in authority['input_manifest']:
  if record['path']=='content/questions.json':record['sha256']=identity(Path(record['path']))['sha256']
 authority['input_manifest_sha256']=hashlib.sha256(canonical(authority['input_manifest']).encode()).hexdigest()
 output(BASE/'source-authority.json',authority)
 output(BASE/'retained-review.json',{'schema_version':1,'reviewed_on':'2026-10-16','questions':retained})
 for q,a in zip(questions,audit):
  review_data=q['acceptance']['content_review']
  if review_data and 'pending_retained_review_index' in review_data:q['acceptance']['content_review']=review(BASE/'retained-review.json',f'json:/questions/{review_data["pending_retained_review_index"]}')
  a['content_review']=q['acceptance']['content_review']
 output(Path('content/question-relationships.json'),{'schema_version':1,'relationships':rels})
 output(Path('content/assessment-questions.json'),{'schema_version':1,'questions':questions})
 output(Path('content/package-sources.json'),s)
 output(BASE/'relationship-parity.json',{'status':'passed','question_count':len(rels),'exact_mapped_primary_related_reference_source_ids':True,'exact_source_reference_order':True,'all_targets_resolve':True,'retained_assessment_fields_unchanged':True,'replacement_originals_unchanged':38,'map':identity(MAP),'relationships':identity(Path('content/question-relationships.json'))})
 eligible=Counter(a['eligibility'] for a in audit);assert eligible=={'accepted':384,'held':616}
 assert Counter(a['disposition'] for a in audit)=={'retain':336,'rewrite':626,'replace':38}
 assert len({q['concept_id'] for q in questions})==500
 output(BASE/'eligibility-audit.json',{'status':'held candidate; release acceptance blocked','release_accepted':False,'total_questions':1000,'total_concepts':500,'dispositions':dict(Counter(a['disposition'] for a in audit)),'eligibility':dict(eligible),'blockers':['578 rewritten sign assessments still require delivery/route acceptance.','38 replacement proposals remain unapplied and require exact-code 9F delivery acceptance.'],'questions':audit})
 manifest={'schema_version':1,'identity':{'content_version':c['source_curriculum']['content_version']+'-candidate-9j','manifest_sha256':''},'source_curriculum':c['source_curriculum'],
 'inputs':[identity(p) for p in [BASE/'source-authority.json',Path('docs/curriculum/app-migration/curriculum-map.json'),Path('docs/curriculum/app-migration/baseline.json'),ACTIONS,MAP,Path('docs/curriculum/app-migration/link-and-progress-map.json'),*[Path(p) for p in MODEL_PATHS],Path('tools/assemble_question_package_9j.py'),Path('tools/compile_curriculum.py'),Path('tools/content_schema.py'),Path('content/legacy-sources.json'),BASE/'retained-review.json',Path('content/question-relationships.json'),Path('content/questions.json')] ],
 'payloads':[{'kind':kind,'file':identity(Path(p))} for kind,p in [('curriculum','content/curriculum.json'),('questions','content/assessment-questions.json'),('sources','content/package-sources.json'),('legacy_aliases','content/legacy-aliases.json')]]+[{'kind':'asset','file':f} for f in {a['bundled']['path']:a['bundled'] for a in c['assets']}.values()],
 'canonical_revisions':[{'id':r['id'],'revision':r.get('revision','screen-r1')} for key in ['documents','reference_groups','sign_entries','anchors'] for r in c[key]]+[{'id':r['id'],'revision':'screen-r1'} for r in s['destinations']],
 'question_revisions':[{'key':q['key'],'eligibility':q['acceptance']['eligibility']} for q in questions],
 'source_bindings':[dict(source_id=d['id'],**b) for d in s['destinations'] for b in d['scoped_urls']], 'asset_bindings':[{'id':a['id'],'file':a['bundled']} for a in c['assets']]}
 manifest['identity']['manifest_sha256']=manifest_digest(manifest);output(Path('content/content-manifest.json'),manifest)
 # A compact companion keeps the historical bank and existing rewrite metadata intact.
 emitter=SharedEmitter(Schema(ROOT),'package9J');rel_calls={qid:emitter.emit(r,'QuestionRelationship',qid+'/relationship') for qid,r in rels.items()}
 missing={q['key']['question_id']:emitter.emit(q,'AssessmentQuestion',q['key']['question_id']) for q,row in zip(questions,bank) if not row.get('assessment')}
 from compile_curriculum import kotlin_string as ks
 entries=[f'{ks(qid)} to {call}' for qid,call in rel_calls.items()]
 rel_chunks=[]
 for n in range(0,len(entries),20):rel_chunks.append(emitter.function('Map<String, QuestionRelationship>','mapOf('+', '.join(entries[n:n+20])+')','relationship map',None))
 m_entries=[f'{ks(qid)} to {call}' for qid,call in missing.items()];m_chunks=[]
 for n in range(0,len(m_entries),20):m_chunks.append(emitter.function('Map<String, AssessmentQuestion>','mapOf('+', '.join(m_entries[n:n+20])+')','missing map',None))
 header='// Generated by tools/assemble_question_package_9j.py; held candidate, not an accepted release.\npackage se.korkort\n\n'
 top=header+'internal val questionRelationships9J: Map<String, QuestionRelationship> by lazy { '+' + '.join(rel_chunks)+' }\n'
 top+='internal val Question.canonicalRelationship: QuestionRelationship get() = questionRelationships9J.getValue(id)\n'
 top+='private val additionalQuestions9J: Map<String, AssessmentQuestion> by lazy { '+' + '.join(m_chunks)+' }\n'
 top+='internal val candidateQuestions9J: List<AssessmentQuestion> by lazy { questionBank.map { row -> (row.assessment ?: additionalQuestions9J.getValue(row.id)).copy(relationship = questionRelationships9J.getValue(row.id)) } }\n'
 top+='internal val candidateIdentity9J = ContentPackageIdentity('+ks(manifest['identity']['content_version'])+', Sha256('+ks(manifest['identity']['manifest_sha256'])+'))\ninternal const val candidateReleaseAccepted9J: Boolean = false\n'
 output(DEST/'QuestionPackage9J.kt',top)
 for n in range(0,len(emitter.functions),200):output(DEST/f'QuestionPackage9JPart{n//200:03}.kt',header+''.join(f'internal fun {name}(): {kind} = {expr}\n' for name,kind,expr in emitter.functions[n:n+200]))
 output(BASE/'question-parity.tsv',''.join(q['key']['question_id']+'\t'+hashlib.sha256(canonical(q).encode()).hexdigest()+'\n' for q in questions))
 payloads={'curriculum':c,'questions':{'schema_version':1,'questions':questions},'sources':s,'legacy_aliases':read(Path('content/legacy-aliases.json'))}
 validator=Validator(source_authority=str(BASE/'source-authority.json'));result=validator.package(payloads,manifest,'fixture')
 try:validator.package(payloads,manifest,'release')
 except ContentError as e:release_error=str(e)
 else:raise AssertionError('Unresolved holds must block release validation')
 output(BASE/'package-validation.json',{'structural_validation':result,'release_validation':'blocked','reason':release_error,'candidate_only':True,'manifest':identity(Path('content/content-manifest.json'))})
 return files
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args();assemble(args.check);print('9J: 1000 mapped candidate questions; 384 accepted, 616 held; release remains blocked.')
