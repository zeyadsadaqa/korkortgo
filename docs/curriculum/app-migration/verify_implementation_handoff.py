"""Validate only the 7F handoff; does not execute the independent 7G audit."""
import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
checks = []
def check(name, condition, detail=None):
    checks.append(dict(name=name,passed=bool(condition),detail=detail))
def load(name): return json.loads((OUT/name).read_text())
def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def pointer(document, value):
    for part in value.strip('/').split('/'):
        part=part.replace('~1','/').replace('~0','~')
        document=document[int(part)] if isinstance(document,list) else document[part]
    return document

x=load('implementation-backlog.json'); p=load('preview-content.json')
a=load('question-actions.json'); c=load('curriculum-map.json'); l=load('link-and-progress-map.json'); q=load('question-map.json'); b=load('baseline.json')
check('frozen 7A–7E planning identities',all(sha(i['path'])==i['sha256'] for i in x['inputs']) and x['inputs']==p['inputs'])
# Baseline source and bundled assets are protected; no mutation is allowed in 7F.
protected=b['frozen_inputs']+b['bundled_assets']
bad=[i['path'] for i in protected if not (ROOT/i['path']).is_file() or sha(i['path'])!=i['sha256']]
check('protected baseline inputs and 343 app assets unchanged',not bad,bad)
check('400 exact approved sign asset hashes',all(sha(s['asset']['path'])==s['asset']['sha256'] for s in c['sign_entries']))
ids=[i['id'] for i in x['work_items']]; known=set(ids)
check('15 bounded unique work items',len(ids)==len(known)==15)
seen=set(); dependency_ok=True
for i in x['work_items']:
    dependency_ok &= all(dep in seen for dep in i['dependencies'])
    seen.add(i['id'])
check('acyclic dependency graph in executable order',dependency_ok)
check('each work item has files output and acceptance',all(i['affected_files'] and i['output'] and i['acceptance'] for i in x['work_items']))
assign=x['question_assignments']; original=a['questions']
check('all 1000 baseline IDs once in original order',[z['question_id'] for z in assign]==b['question_ids_in_order'] and len({z['question_id'] for z in assign})==1000)
check('exact original dispositions and evidence pointers',all(z['disposition']==r['disposition'] and z['work_item_id'] in known and pointer(a,z['acceptance_pointer'].split('#')[1])==r and pointer(q,z['link_pointer'].split('#')[1])['question_id']==z['question_id'] for z,r in zip(assign,original)))
counts=dict(collections.Counter(z['disposition'] for z in assign))
check('336 retain / 626 rewrite / 38 replace / zero remove',counts==dict(retain=336,rewrite=626,replace=38),counts)
owners=dict(collections.Counter(z['work_item_id'] for z in assign))
check('bounded question owners',owners=={'9J':336,'9E':578,'9F':38,'9G':8,'9H':30,'9I':10},owners)
for task in ['9D','9E','9F','9G','9H','9I','9J']:
    batches=[z for z in x['execution_batches'] if z['work_item_id']==task]
    actual=[qid for z in batches for qid in z['question_ids']]
    expected=[z['question_id'] for z in assign if (z['question_id'].startswith('sign-') if task=='9D' else z['work_item_id']==task)]
    check('exact bounded batches '+task,actual==expected and all(0<len(z['question_ids'])<=50 for z in batches))
registry=[]
for k in ['curriculum_nodes','sign_entries','source_destinations','supporting_destinations']:
    expected=[r['id'] for r in c[k]]; registry+=expected
    check('all '+k+' owned',x['coverage']['7B/'+k]['record_ids']==expected)
check('all 1123 published IDs unique',len(registry)==len(set(registry))==1123)
for issue,count in a['issue_counts'].items():
    entry=x['coverage'].get('7D/'+issue,{})
    check('issue coverage '+issue,entry.get('record_count')==count and bool(entry.get('work_item_ids')))
check('shared 7D dependencies owned',all('7D/'+z['id'] in x['coverage'] for z in a['shared_implementation_dependencies']))
check('all three coverage gap briefs owned',all(x['coverage'].get('7D/coverage/'+z['lesson_id'],{}).get('brief')==z for z in a['coverage_backlog']))
for key in ['category_routes','lesson_category_tags','navigation_routes','reading_order','chapter_aliases','legacy_page_aliases','question_routes','unused_topic_routes','sign_routes','source_routes','state_rules','entry_point_rules','labels_to_replace','supporting_document_updates','resolution_policy','version_transition','unresolved_destinations']:
    entry=x['coverage'].get('7E/'+key,{})
    check('7E ownership '+key,entry.get('record_count')==(len(l[key]) if isinstance(l[key],list) else 1) and bool(entry.get('work_item_ids')))
check('every coverage owner is a known work item',all(set(z['work_item_ids'])<=known for z in x['coverage'].values()))
check('all work items have step10 verification',set(t for z in x['verification_cases'] for t in z['work_item_ids'])==known)
check('signal fallback decision no new destinations',all(z['target_id'] is None and z['resolution']=='unavailable_exact_entry' for z in p['signal_unavailable_cases']) and p['signal_unavailable_cases']==l['unresolved_destinations'] and 'No approved destination or asset is added' in x['signal_decision'])
lesson=p['lesson_reader']; source=(ROOT/lesson['source_path']).read_text()
check('exact complete approved lesson fixture',lesson['approved_markdown'] in source and sha(lesson['source_path'])==lesson['sha256'])
check('canonical module titles and order',p['library']['module'] in c['modules'] and all(z in c['curriculum_nodes'] for z in p['library']['children']))
check('all 40 filter tags preserved',p['library']['lesson_tags']==l['lesson_category_tags'] and len(p['library']['lesson_tags'])==40)
for r in p['answer_reviews']:
    file,ptr=r['origin'].split('#'); expected=pointer(load(file),ptr)
    check('exact question fixture '+r['question_id'],r['question']==expected)
    order=r['display_option_order']
    check('shuffle identity and key fixture '+r['question_id'],sorted(order)==list(range(4)) and order[r['correct_display_index']]==r['question']['correct'] and order[r['selected_display_index']]==r['selected_original_option']!=r['question']['correct'])
check('fuel proposed and not scored status explicit','proposed revision' in p['answer_reviews'][1]['status'] and 'not live' in p['answer_reviews'][1]['status'])
for s in p['sources']:
    file,ptr=s['origin'].split('#'); expected=pointer(load(file),ptr)
    check('exact source classification '+s['id'],s['url']==expected['url'] and s['classification']==expected['classification'] and s['source_checks']==[dict(path=z['path'],json_pointer=z['json_pointer'],record={k:v for k,v in z['record'].items() if k not in ['text','html']}) for z in expected['source_checks']])
sign=p['sign_reference']['entry']
check('exact B1 reference asset/caption',sign in c['sign_entries'] and sign['code']=='B1' and sign['caption_id']==p['sign_reference']['caption']['caption_id'] and sha(sign['asset']['path'])==sign['asset']['sha256'])
check('all 7E legacy fixtures preserved',p['legacy_examples']==l['examples'])
# Determinism also confirms regeneration does not touch protected files.
artifacts=['implementation-backlog.json','implementation-backlog.md','preview-content.json','preview-handoff.md']
before={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in artifacts}
subprocess.run([sys.executable,str(OUT/'build_implementation_handoff.py')],check=True,capture_output=True)
after={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in artifacts}
check('byte-identical 7F rebuild',before==after)
check('protected inputs unchanged after rebuild',all((ROOT/i['path']).is_file() and sha(i['path'])==i['sha256'] for i in protected))
report=dict(step='7F',scope='handoff checks only; 7G and app/device tests not executed',passed=all(z['passed'] for z in checks),checks=checks,artifact_sha256=after)
(OUT/'handoff-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(passed=report['passed'],checks=len(checks),failures=[z for z in checks if not z['passed']]),indent=2))
raise SystemExit(0 if report['passed'] else 1)
