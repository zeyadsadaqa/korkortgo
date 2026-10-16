"""Independent final 9B parity, identity and staged-generation checks."""
from pathlib import Path
import hashlib,json,re,sys,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from import_curriculum_remaining import Import,plain_md,printable,norm
from compile_curriculum import compile_files,ContentError

def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rich(nodes):return ''.join(n['text'] if n['type']=='text' else n['expression'] if n['type']=='math' else rich(n.get('children',n.get('label',[]))) for n in nodes)
def blocktext(b):
    p=b['payload'];t=p['type']
    if t in ('paragraph','heading'):return rich(p['text'])
    if t=='table':return ' '.join([rich(c['heading']) for c in p['columns']]+[rich(c) for row in p['rows'] for c in row['cells']])
    if t=='list_items':return ' '.join((str(p['start']+i)+'. ' if p['ordered'] else '')+' '.join(blocktext(b) for b in item) for i,item in enumerate(p['items']))
    if t in ('scenario','callout'):return ' '.join(blocktext(b) for b in p['blocks'])
    if t=='knowledge_check':return ' '.join(blocktext(b) for b in p['prompts'])
    raise ValueError(t)
def walk(blocks):
    for b in blocks:
        yield b
        p=b.get('payload',{})
        if p.get('type') in ('scenario','callout'):yield from walk(p['blocks'])
        if p.get('type')=='knowledge_check':yield from walk(p['prompts'])
        if p.get('type')=='list_items':
            for item in p['items']:yield from walk(item)
checks=[]
def check(name,ok,evidence=None):checks.append({'name':name,'passed':bool(ok),'evidence':evidence})
fresh_pdf=read(str((HERE/'pdf-extraction-verification.json').relative_to(ROOT)))
check('All 578 pages match fresh approved-PDF extraction',fresh_pdf['passed'] and len(fresh_pdf['pages'])==578 and fresh_pdf['pdf']['sha256']==sha(ROOT/fresh_pdf['pdf']['path']),578)
p=read('content/curriculum.json');s=read('content/sources.json');state=read('content/curriculum-import-state.json');registry=read('docs/curriculum/app-migration/curriculum-map.json')
job=Import();expected,expected_state,expected_sources=job.run()
check('Complete import reproduces exactly',p==expected and s==expected_sources and state==expected_state,'Fresh import from frozen production inputs and saved incoming data')
check('No unmatched source block or production range',not job.missing,job.missing)
allids=[r['id'] for k in ['documents','reference_groups','sign_entries','anchors'] for r in p[k]]+[r['id'] for r in s['destinations']]
known=[r['id'] for k in ['curriculum_nodes','source_destinations','sign_entries','supporting_destinations'] for r in registry[k]]
check('All 1123 exact published identities resolve uniquely',len(allids)==len(set(allids))==1123 and set(allids)==set(known),{'curriculum':88,'signs':400,'sources':116,'supporting':519})
check('All 60 reading bodies imported',len(p['reading_order'])==60 and all(next(d for d in p['documents'] if d['id']==id)['body_blocks'] for id in p['reading_order']),len(p['reading_order']))
check('No pending bodies or invented learner completion',not state['pending_reading_nodes'] and state['production_ready'] is False,'Import ledger is build state, not learner progress or release acceptance')
check('All 40 objectives and tags retained',len([d for d in p['documents'] if d['kind']=='lesson' and d['objectives']])==40 and len(p['lesson_category_tags'])==40,40)
docs={d['id']:d for d in p['documents']};blocks={b['metadata']['id']:b for d in p['documents'] for b in walk(d['body_blocks'])}
answers={a['metadata']['id']:a for d in p['documents'] for a in d['answer_blocks']}
check('50 answers remain separately revealed',len(answers)==50 and all(a['visibility']=='after_deliberate_reveal' for a in answers.values()),50)
for row in job.parity:
    id=row['id'];b=blocks[id];text=blocktext(b)
    if b['payload']['type']=='knowledge_check':text+=' '+' '.join(blocktext(x) for x in answers[b['payload']['answer_id']]['blocks'])
    digest=hashlib.sha256(norm(text).encode()).hexdigest()
    check(id+' full normalized source parity',digest==row['normalized_text_sha256'],{'source_sha256':row['normalized_text_sha256'],'import_sha256':digest})
for row in job.matches:
    if not row.get('production_extra'):continue
    raw=norm(job.pages[row['page']-1]['body'])[row['offset']:row['offset']+row['characters']]
    actual=blocktext(blocks[row['id']]) if row['id'] in blocks else blocktext(next(b for g in p['reference_groups'] for b in walk(g['body_blocks']) if b['metadata']['id']==row['id']))
    check(row['id']+' actual production fragment parity',''.join(raw.split())==''.join(actual.split()),{'page':row['page'],'normalization':'Only presentation whitespace, including annotation-bound URL wraps'})
for row in job.coverage:
    check('PDF '+str(row['page'])+' complete once',row['missing_characters']==row['duplicate_characters']==0,row)
check('All 729 production sign examples use shared entries',len(job.claims)==729,729)
# Exact final membership comes from production, not the old selection shortlist.
records=read('docs/curriculum/pdf-production/reference/assets.json')['official_sign_placements']
for g in p['reference_groups']:
    wanted=['sign-'+r['code'] for r in records if r['group']==g['id']]
    check(g['id']+' exact production membership/order',g['entry_ids']==wanted,wanted)
check('All 400 primary reference entries',sum(len(g['entry_ids']) for g in p['reference_groups'])==400 and len({id for g in p['reference_groups'] for id in g['entry_ids']})==400,400)
for a in p['assets']:
    check(a['id']+' exact bundled identity',a['original']['sha256']==a['bundled']['sha256']==sha(ROOT/a['original']['path'])==sha(ROOT/a['bundled']['path']),a['bundled'])
check('All 484 asset bindings retained',len(p['assets'])==484,{'official_signs':400,'contextual_including_cover':84})
check('All 404 question URL identities retained',all(any(ref['id']==old['id'] and ref['url']==old['url'] for ref in s['references']) for old in read('docs/curriculum/app-migration/question-map.json')['source_registry']),{'required_question_urls':404,'all_retained_references':len(s['references'])})
for old in registry['source_destinations']:
    actual=next(r for r in s['destinations'] if r['id']==old['id']);refs={r['id']:r for r in s['references']}
    check(old['id']+' all exact scopes',all(any(b['scope_id']==scope and refs[b['reference_id']]['url']==url for b in actual['scoped_urls']) for scope,url in old['scoped_urls'].items()),actual['scoped_urls'])
check('Case-sensitive F31a and signal exclusions',any(r['code']=='F31a' for r in p['sign_entries']) and not any(r['code'] in ['SIG16','SIG17','SIG18'] for r in p['sign_entries']),'No fabricated unavailable signal entries')
wild=[r for r in job.matches if r['page']==193 and r['id'].startswith('M06-L01/teaching-')]
check('Page 193 wildlife correction retained',len(wild)>=5 and any('small waterways' in blocktext(blocks[r['id']]) for r in wild),'Final approved passage: small waterways, not drains; matches frozen chapter source and PDF')
firstaid=docs['M10-L02'];text=' '.join(blocktext(b) for b in firstaid['body_blocks'] if b['payload']['type'] in ['paragraph','heading'])
check('1177 remains a limited reference',any('1177' in richtext for richtext in [text]) and 'No clinical procedure is reproduced' in norm(job.pages[-1]['body']),'No added clinical procedure; exact approved M10 teaching and credits retained')
prior=read(str((HERE/'incoming-curriculum.json').relative_to(ROOT)))
for d in prior['documents']:
    actual=docs[d['id']]
    if not d['body_blocks']:continue
    check(d['id']+' prior teaching unchanged',actual['body_blocks'][:len(d['body_blocks'])]==d['body_blocks'] and actual['answer_blocks']==d['answer_blocks'] and actual['objectives']==d['objectives'],'Only cover artwork/related hub navigation are additions')
base=read('docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json')
allowed={'tools/build_content.py','composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','docs/curriculum/implementation-plan.md'}
changed=[r['path'] for r in base['input_manifest'] if r['path'] not in allowed and sha(ROOT/r['path'])!=r['sha256']]
check('Frozen teaching/PDF/official originals/live bank unchanged',not changed,changed)
for step in ['9B1','9B2','9B3']:
    report=read('docs/curriculum/app-migration/implementation-evidence/'+step+'/verification.json')
    artifacts=[r for r in report['artifacts'] if '/implementation-evidence/'+step+'/' in r['path']]
    changed=[r['path'] for r in artifacts if sha(ROOT/r['path'])!=r['sha256']]
    check(step+' saved evidence untouched',not changed,changed)
manifest=HERE/'staging-manifest.json';paths={'curriculum':ROOT/'content/curriculum.json','sources':ROOT/'content/sources.json',**{k:HERE/(k+'.json') for k in ['questions','legacy_aliases']}}
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)/'generated';trace=Path(tmp)/'trace.json';totals=compile_files(paths,manifest,out,trace,symbol='stagedCurriculum9B17')
    hashes={x.name:sha(x) for x in out.glob('*.kt')};tracehash=sha(trace)
    check('Saved Kotlin/trace equals fresh generation',hashes=={x.name:sha(x) for x in (HERE/'generated').glob('*.kt')} and tracehash==sha(HERE/'trace.json'),len(hashes))
    compile_files(paths,manifest,out,trace,symbol='stagedCurriculum9B17')
    check('Repeated output byte-identical',hashes=={x.name:sha(x) for x in out.glob('*.kt')} and tracehash==sha(trace),totals)
    try:compile_files(paths,manifest,out,trace,profile='release',symbol='stagedCurriculum9B17')
    except ContentError as exc:check('Unimported/unaccepted assessments still block release','baseline question coverage' in str(exc),str(exc))
    else:check('Unimported/unaccepted assessments still block release',False)
for name,count in [('QuizTest',6),('CurriculumContractTest',5),('CompleteReadingImportTest',4)]:
    node=ET.parse(HERE/f'TEST-se.korkort.{name}.xml').getroot();result={k:int(node.attrib[k]) for k in ['tests','failures','errors','skipped']}
    check(name+' configured Kotlin tests pass',result=={'tests':count,'failures':0,'errors':0,'skipped':0},result)
log=(HERE/'python-tests.txt').read_text();check('83 Python regression tests pass','Ran 83 tests' in log and log.rstrip().endswith('OK'),log[-150:])
status='complete' if all(r['passed'] for r in checks) else 'failed'
report={'step':'9B17','status':status,'completed_steps':['9B'+str(n) for n in range(1,18)],'prerequisites':['9C1','9C2','9C3','9C4'],'totals':{'checks':len(checks),'passed':sum(r['passed'] for r in checks),'published_destinations':1123,'reading_nodes':60,'module_lessons':40,'separate_answers':50,'reference_groups':24,'signs':400,'source_destinations':116,'source_references':len(s['references']),'supporting_destinations':519,'assets':484,'source_blocks_this_batch':388,'production_pages_this_batch':538,'production_sign_examples':729,'generated_files':len(hashes),'python_tests':83,'jvm_tests':15},'checks':checks,'source_authority': 'Immutable 9A1 plus verified 9B3 incoming snapshot/cover binding','limitations':['Reading import is complete; this is not an accepted assessment/release package.','Question acceptance, 38 faint-artwork delivery holds, actual reader semantics, source currency and configured-device tests remain later work.','No learner history/completion, UI design, question rewrite or source PDF edit.']}
(HERE/'import-parity.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
for n in range(4,17):
    step='9B'+str(n);out=HERE.parent/step;out.mkdir(exist_ok=True)
    entries=[r for r in checks if (r['name'].startswith(f'M{n-1:02d}') if n<=11 else r['name'].startswith('appendix-'+chr(65+n-12)) if n<=15 else r['name'].startswith('RB'))]
    filename='module-parity.json' if n<=11 else 'appendix-parity.json' if n<=15 else 'reference-group-parity.json'
    data={'step':step,'status':status,'records':entries,'generated_package':'../9B17/staging-manifest.json','full_parity':'../9B17/import-parity.json'}
    (out/filename).write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    (out/'review.md').write_text(f'# {step} execution review\n\nCompleted in the user-authorized remaining 9B batch. Exact production text, structure, origins and bindings are retained in the cumulative payload.\n\nSee [{filename}]({filename}), [complete independent parity](../9B17/import-parity.json) and [shared generated Kotlin/trace](../9B17/README.md). Assessment/runtime/device acceptance remains later work.\n')
artifact_paths=[ROOT/p for p in ['content/curriculum.json','content/sources.json','content/curriculum-import-state.json','tools/import_curriculum_remaining.py','tools/test_import_curriculum_remaining.py','tools/test_import_curriculum_m02.py','tools/compile_curriculum.py','composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt','docs/curriculum/implementation-plan.md','docs/curriculum/progress.md']]
for step in ['9B'+str(n) for n in range(4,18)]+['9C'+str(n) for n in range(1,5)]:
    artifact_paths += [p for p in (HERE.parent/step).rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts]
receipt={'step':'9B17','status':status,'date':'2026-10-15','totals':report['totals'],'authorization':'User authorized all remaining 9B steps; 9C1–9C4 are explicit 9B17 prerequisites.','staging_identity':read(str(manifest.relative_to(ROOT)))['identity'],'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(set(artifact_paths))],'next_step':'9D1; assessment/runtime/device acceptance remains later work'}
(HERE/'verification.json').write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':status,'totals':report['totals'],'failures':[r for r in checks if not r['passed']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if status=='complete' else 1)
