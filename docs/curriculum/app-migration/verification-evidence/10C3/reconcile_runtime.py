"""Prepare the frozen 72 source cases and reconcile fresh desktop observations, without inventing platform runs."""
import hashlib,json
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists()); HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
m=read(ROOT/'docs/curriculum/app-migration/verification-evidence/10A3/runtime-matrix.json')['source_class_matrix']
observed_path=HERE/'desktop-source-observations.json'; observations=read(observed_path)['observations'] if observed_path.exists() else []
index={(o['case_class'],o['state']):o for o in observations if 'case_class' in o}
content=read(ROOT/'content/curriculum.json');questions=read(ROOT/'content/accepted-assessment-questions.json')['questions'];cases=[]
def documents(value):
 if isinstance(value,dict):
  if 'body_blocks' in value and 'id' in value:yield value
  else:
   for v in value.values():yield from documents(v)
 elif isinstance(value,list):
  for v in value:yield from documents(v)
docs=list(documents(content))
steps={
 'details_return':['Open the exact source detail using a supplied origin below.','Compare title, publisher, classifications, original dates, scope and limitations against frozen record.','Use Back and Return controls; verify origin identity, position and focus; for answer review preserve revision, displayed options, answer, filter and row.'],
 'external_dispatch':['Open exact source detail; activate Open source.','Observe exact original URL handed to platform URI handler. Desktop uses injected dispatch only.','Record launcher success/failure separately from third-party content availability; return to unchanged originating reader/review.'],
 'unreachable_return':['Open exact source detail; exercise controlled URI-launch failure and recoverable offline/unreachable third-party response separately where supported.','Record actual platform error/recovery UI, keyboard/focus and retained context. Desktop callback rejection proves shared recovery only.','Return to origin, verify context and retry; do not claim a launched browser reports its remote HTTP status back to the app.']}
for target in m['targets']:
 for e in m['frozen_examples']:
  for state in m['states']:
   cid=f"10C3-{target}-{e['case_class']}-{state}";o=index.get((e['case_class'],state)) if target=='desktop' else None
   origins={'lesson_ids':[d['id'] for d in docs if e['reference_id'] in json.dumps(d)],'question_ids':[q['key']['question_id'] for q in questions if any(u['reference_id']==e['reference_id'] for u in q['relationship']['source_uses'])]}
   if e['case_class']=='editorial_arithmetic':origins['preferred_question_id']='reaction-20-0.5'
   cases.append({'case_id':cid,'target':target,'case_class':e['case_class'],'state':state,'reference_id':e['reference_id'],'url':e['url'],'source_oracle':e['oracle'],'expected_scope':e['expected_scope'],'available_origins':origins,'steps':steps[state],'status':'pass_shared_desktop_harness' if o else 'not_run_pending_10K','observation':o,'observation_path':observed_path.name if o else None,'remaining_closure_requirement':'Fresh 10K platform/production-owner observation; shared results do not prove native/browser behaviour.'})
assert len(cases)==72 and len({x['case_id'] for x in cases})==72
assert len(index) in (0,18)
dump(HERE/'source-cases.json',{'task':'10C3','source':'../10A3/runtime-matrix.json#/source_class_matrix','cases':[{k:v for k,v in c.items() if k not in ['observation','observation_path']} for c in cases],'expected_cases':72})
dump(HERE/'source-runtime-results.json',{'task':'10C3','status':'partial_pending_10K','candidate_manifest_sha256':hashlib.sha256((ROOT/'content/accepted-content-manifest.json').read_bytes()).hexdigest(),'counts':{'required_matrix_cases':72,'passed_shared_desktop_harness':len(index),'not_run_pending_10K':72-len(index),'supplemental_shared_checks':len([o for o in observations if 'case_id' in o])},'cases':cases,'supplemental_observations':[o for o in observations if 'case_id' in o],'closure_blocked_by':['Fresh Android, iOS simulator and Wasm/JS observations (54 cases).','Fresh 10K production-owner integration, URI handler/offline and return observations; desktop uses agreed injected dispatch policy.','Six source classification defects and one selected source-currency blocker; see defects.json.'],'limits':['No browser/OS launch or HTTP success inferred from callback success.','Simulated callback rejection is not an actual offline browser result.','Missing-source recovery and reader focus use actual shared components. Review test uses a verification owner; production CurriculumApp owner remains 10K.','No physical-device, TalkBack or speech claim.']})
print(json.dumps({'prepared':len(cases),'desktop_matrix_passes':len(index),'supplemental':len(observations)-len(index),'pending_platform':72-len(index)}))
