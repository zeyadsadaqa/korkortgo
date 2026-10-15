"""Verify opening import against the approved PDF, registry and reproducible staged output."""
from pathlib import Path
import hashlib
import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from compile_curriculum import compile_files, ContentError
from import_curriculum_opening import build


def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized(text):return ' '.join(text.split())
def plain(nodes):
    return ''.join(n['text'] if n['type']=='text' else n['expression'] if n['type']=='math' else plain(n.get('children',n.get('label',[]))) for n in nodes)
def leaves(blocks):
    result=[]
    for block in blocks:
        payload=block['payload']
        if payload['type'] in ('heading','paragraph'):result.append(plain(payload['text']))
        elif payload['type']=='list_items':
            for item in payload['items']:result.extend(leaves(item))
        else:raise ValueError('Unexpected opening payload type: '+payload['type'])
    return result
checks=[]
def check(name,ok,evidence):checks.append({'name':name,'passed':bool(ok),'evidence':evidence})
payload=read('content/curriculum.json');state=read('content/curriculum-import-state.json')
registry=read('docs/curriculum/app-migration/curriculum-map.json');links=read('docs/curriculum/app-migration/link-and-progress-map.json')
expected,expected_state=build()
check('Reproducible bounded import',payload==expected and state==expected_state,'Fresh source selection equals both authoring files')
check('Canonical ten modules',payload['modules']==registry['modules'],len(payload['modules']))
check('Exact sixty-node reading order',payload['reading_order']==links['reading_order'] and len(set(payload['reading_order']))==60,payload['reading_order'])
documents={d['id']:d for d in payload['documents']}
check('Unique 64 staged destinations',len(documents)==len(payload['documents'])==64,dict(Counter(d['kind'] for d in documents.values())))
for node in [n for n in registry['curriculum_nodes'] if n['id'] in payload['reading_order']]:
    doc=documents[node['id']];loc=node['source_location']
    lines=(ROOT/loc['path']).read_text().splitlines()
    check(node['id']+' exact title/order/production origin',doc['title']==node['title'] and doc['order']==node['order'] and doc['origin']['file']=={'path':loc['path'],'sha256':loc['sha256']} and doc['origin']['locator']==f'line:{loc["line"]}' and lines[loc['line']-1]==loc['heading'],doc['origin'])
check('Unimported bodies are not represented as complete',len(state['pending_reading_nodes'])==60 and all(r['status']=='structure_only' for r in state['pending_reading_nodes']) and all(not documents[id]['body_blocks'] and not documents[id]['answer_blocks'] for id in payload['reading_order']) and state['production_ready'] is False,'60 pending body records; no authored teaching stubs')
front=['cover','introduction','study-guide','contents']
check('Front matter excluded from top-level library and reading sequence',state['front_matter_ids']==front and not set(front)&set(payload['reading_order']) and state['library_policy']['top_level_card_ids']==[m['id'] for m in registry['modules']] and set(state['library_policy']['exclude_front_matter_ids'])==set(front),state['library_policy'])
expected_tags={t['lesson_id']:sorted(c.lower() for c in t['category_ids']) for t in links['lesson_category_tags']}
check('All forty exact category-tag records retained',payload['lesson_category_tags']==expected_tags and len(expected_tags)==40,'Includes the three zero-primary-question lessons')
release=read('docs/curriculum/pdf-production/final-review/screen-release.json')
pdf_path=ROOT/release['artifact'];reader=PdfReader(pdf_path)
check('Approved screen identity and 578 pages',sha(pdf_path)==release['sha256']==payload['source_curriculum']['pdf']['sha256'] and len(reader.pages)==578,release['sha256'])
stored=read(str((HERE/'pdf-opening-text.json').relative_to(ROOT)))
fresh=[reader.pages[i].extract_text() for i in range(4)]
check('Retained extraction matches fresh PDF text',stored['pdf']['sha256']==release['sha256'] and [p['text'] for p in stored['pages']]==fresh,'Fresh pypdf extraction of the four opening pages')
headers=['','KörkortGo · Before you begin','KörkortGo · How to use this book','KörkortGo · Contents']
for i,id in enumerate(front):
    body=normalized(fresh[i])
    if headers[i]:
        header=headers[i];tail=f'Contents Sources Previous page {i+1} Next page'
        assert body.startswith(header) and body.endswith(tail)
        body=body[len(header):-len(tail)].strip()
    if id=='contents':body=normalized(re.sub(r'\b\d+\b','',body))
    imported=normalized(' '.join(leaves(documents[id]['body_blocks'])))
    check(id+' full opening-text parity with approved PDF',imported==body,{'page':i+1,'imported_text_sha256':hashlib.sha256(imported.encode()).hexdigest(),'pdf_body_text_sha256':hashlib.sha256(body.encode()).hexdigest()})
disclaimer='This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.'
blocks=documents['introduction']['body_blocks']
exact=[b for b in blocks if b['metadata']['id']=='introduction/disclaimer']
check('Verbatim required disclaimer with dedicated role',len(exact)==1 and plain(exact[0]['payload']['text'])==disclaimer==state['opening_text']['exact_disclaimer'] and exact[0]['payload']['role']=='disclaimer',exact[0]['metadata'])
paths={'curriculum':ROOT/'content/curriculum.json',**{k:HERE/(k+'.json') for k in ['questions','sources','legacy_aliases']}}
manifest=HERE/'staging-manifest.json'
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)/'generated';trace=Path(tmp)/'trace.json'
    totals=compile_files(paths,manifest,out,trace,symbol='stagedCurriculum9B1')
    first={p.name:sha(p) for p in out.glob('*.kt')};first_trace=sha(trace)
    check('Saved Kotlin matches fresh generation',first=={p.name:sha(p) for p in (HERE/'generated').glob('*.kt')},len(first))
    check('Saved source/output trace matches fresh generation',first_trace==sha(HERE/'trace.json'),first_trace)
    compile_files(paths,manifest,out,trace,symbol='stagedCurriculum9B1')
    check('Repeated generation byte-identical',first=={p.name:sha(p) for p in out.glob('*.kt')} and first_trace==sha(trace),totals)
    try:compile_files(paths,manifest,out,trace,profile='release',symbol='stagedCurriculum9B1')
    except ContentError as exc:check('Partial import cannot pass release validation','incomplete canonical' in str(exc),str(exc))
    else:check('Partial import cannot pass release validation',False,'Unexpected release eligibility')
check('Staging placeholders are not live question/source imports',read(str((HERE/'questions.json').relative_to(ROOT)))['questions']==[] and read(str((HERE/'sources.json').relative_to(ROOT)))['references']==[] and read(str((HERE/'legacy_aliases.json').relative_to(ROOT)))['aliases']==[],'Live content/questions.json is independently protected below')
base=read('docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json')
allowed={'tools/build_content.py','composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','docs/curriculum/implementation-plan.md'}
bad=[r['path'] for r in base['input_manifest'] if r['path'] not in allowed and sha(ROOT/r['path'])!=r['sha256']]
check('Approved content/assets and baseline bank preserved',not bad,bad)
previous=read('docs/curriculum/app-migration/implementation-evidence/9A3/verification.json')
bad=[r['path'] for r in previous['artifacts']+previous['tool_files'] if not (ROOT/r['path']).exists() or sha(ROOT/r['path'])!=r['sha256']]
check('9A3 compiler and saved evidence unchanged',not bad,bad)
suites=[]
for name,count in [('QuizTest',6),('CurriculumContractTest',5),('OpeningImportTest',3)]:
    path=HERE/f'TEST-se.korkort.{name}.xml';tree=ET.parse(path).getroot()
    result={k:int(tree.attrib[k]) for k in ['tests','failures','errors','skipped']}
    check(name+' JVM tests pass',result=={'tests':count,'failures':0,'errors':0,'skipped':0},result)
    suites.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),**result})
for name in ['README.md','review.md']:
    missing=[]
    for link in re.findall(r'\]\(([^)]+)\)',(HERE/name).read_text()):
        if '://' in link or link.startswith('#') or link=='verification.json':continue
        if not (HERE/link.split('#')[0]).exists():missing.append(link)
    check(name+' links resolve',not missing,missing)
artifacts=[ROOT/'content/curriculum.json',ROOT/'content/curriculum-import-state.json',ROOT/'tools/import_curriculum_opening.py']+[p for p in HERE.rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts]
report={'step':'9B1','date':'2026-10-15','authorization':'User: “ok go ahead with next step” after 9A3','status':'complete' if all(c['passed'] for c in checks) else 'blocked','scope':'Approved opening text and canonical reading skeleton; chapter bodies, references/assets, runtime views and release acceptance remain later work.','checks':checks,'totals':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'front_matter_documents':4,'reading_nodes':60,'modules':10,'lessons':40,'module_reviews':10,'jvm_tests':14,'generated_files':len(first)},'staging_identity':read(str(manifest.relative_to(ROOT)))['identity'],'jvm_results':suites,'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(artifacts)],'visual_review':'Inspected the four approved PDF pages as a rendered contact sheet; no source PDF/layout edited.','deferred':state['deferred'],'next_step':'9B2 — import M01, separately requested'}
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':report['status'],'totals':report['totals'],'failures':[c for c in checks if not c['passed']]},indent=2))
raise SystemExit(0 if report['status']=='complete' else 1)
