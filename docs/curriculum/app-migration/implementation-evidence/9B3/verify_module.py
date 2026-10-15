"""Read-only import checks; writes only this step's parity/verification evidence."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from import_curriculum_m02 import build, opening, source_parts, PARAGRAPH_IDS, IDS, SOURCE, ART
from compile_curriculum import compile_files, ContentError

def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(text):return ' '.join(text.split())
def plain(nodes):return ''.join(n['text'] if n['type']=='text' else n['expression'] if n['type']=='math' else plain(n.get('children',n.get('label',[]))) for n in nodes)
def mdplain(text):return re.sub(r'\[([^]]+)\]\[([^]]+)\]',r'\1',text.replace('**',''))
def leaves(blocks):
    for b in blocks:
        p=b['payload'];t=p['type']
        if t in ('heading','paragraph'):yield b['metadata']['id'],plain(p['text'])
        elif t=='scenario':yield from leaves(p['blocks'])
        elif t=='knowledge_check':yield from leaves(p['prompts'])
        elif t in ('cropped_image','polygon_image'):yield b['metadata']['id'],plain(p['caption'])
        elif t=='table':
            yield b['metadata']['id'],' '.join([plain(c['heading']) for c in p['columns']]+[plain(cell) for row in p['rows'] for cell in row['cells']])
        elif t=='related_links':
            for i,link in enumerate(p['links']):yield b['metadata']['id']+'/'+str(i),plain(link['label'])
        else:raise ValueError('Unexpected M02 block '+t)
checks=[];comparisons=[]
def check(name,passed,evidence):checks.append({'name':name,'passed':bool(passed),'evidence':evidence})
payload=read('content/curriculum.json');state=read('content/curriculum-import-state.json');docs={d['id']:d for d in payload['documents']}
expected,expected_state,sources=build(payload,state)
check('Bounded import reproduces exactly',expected==payload and state==expected_state and sources==read(str((HERE/'sources.json').relative_to(ROOT))),'No writes from build()')
base=read(str((HERE/'incoming-curriculum.json').relative_to(ROOT)));basestate=read(str((HERE/'incoming-import-state.json').relative_to(ROOT)))
check('Other 58 documents unchanged',[d for d in payload['documents'] if d['id'] not in IDS]==[d for d in base['documents'] if d['id'] not in IDS],'4 opening documents + all 6 M01 documents + 48 remaining skeletons')
for key in ['modules','reading_order','lesson_category_tags','reference_groups','anchors','sign_entries','source_curriculum']:
    check(key+' unchanged',payload[key]==base[key],len(payload[key]))
check('48 pending reading bodies; no fabricated completion',len(state['pending_reading_nodes'])==48 and not state['production_ready'] and all(not docs[r['id']]['body_blocks'] and not docs[r['id']]['answer_blocks'] for r in state['pending_reading_nodes']),state['status'])
old_identities= {a['path']:a['sha256'] for a in read('docs/curriculum/app-migration/implementation-evidence/9B2/verification.json')['artifacts']}
check('Incoming authoring snapshot matches completed 9B2',sha(HERE/'incoming-curriculum.json')==old_identities['content/curriculum.json'] and sha(HERE/'incoming-import-state.json')==old_identities['content/curriculum-import-state.json'],'Exact saved 9B2 bytes')
check('All four M01 illustration bindings unchanged',base['assets']==[a for a in payload['assets'] if a['id'].startswith('M01')],len(base['assets']))
check('Prior completed module and deferred ledger retained',state['completed_module_imports'][0]==basestate['completed_module_imports'][0] and state['deferred']==basestate['deferred'],'M01 completion and all deferred work retained')
source_text,sections,urls=source_parts()
# Independently read every paragraph back from the authored body/answer records.
for id,paras in sections.items():
    d=docs[id];leaf=dict(leaves(d['body_blocks']));answers={a['metadata']['id']:a for a in d['answer_blocks']}
    names=['introduction'] if id=='M02' else PARAGRAPH_IDS[id]
    for name,raw in zip(names,paras):
        bid=id+'/'+name
        if name in ('knowledge-check','review-check'):
            label='Answer:' if name=='knowledge-check' else 'Review guide:'
            actual=leaf[bid+'/prompt']+' '+next(leaves(answers[bid+'/answer']['blocks']))[1]
            check(bid+' answer is deliberately revealed',answers[bid+'/answer']['visibility']=='after_deliberate_reveal' and bid+'/answer' not in leaf,answers[bid+'/answer']['metadata']['origin'])
        else:actual=leaf.get(bid,leaf.get(bid+'/text'))
        wanted=norm(' '.join(c.strip() for line in raw.splitlines() if not re.fullmatch(r'[| :\-]+',line) for c in line.strip('|').split('|'))) if name=='symptom-table' else norm(mdplain(raw));ok=norm(actual)==wanted
        comparisons.append({'id':bid,'passed':ok,'source_normalized_sha256':hashlib.sha256(wanted.encode()).hexdigest(),'import_normalized_sha256':hashlib.sha256(norm(actual).encode()).hexdigest()})
        check(bid+' exact normalized paragraph',ok,len(wanted))
    if d['kind']=='lesson':check(id+' production objective exact',plain(d['objectives'][0])==mdplain(paras[0]).removeprefix('Your goal: '),'Uses final production goal, including G2 corrections')
# Consume all actual PDF teaching, captions, titles, prompts, answers and source labels/URLs.
# Only enumerated print navigation and page furniture are omitted.
pdf=ROOT/payload['source_curriculum']['pdf']['path'];reader=PdfReader(pdf)
check('Approved PDF unchanged and 578 pages',sha(pdf)==payload['source_curriculum']['pdf']['sha256'] and len(reader.pages)==578,sha(pdf))
fresh=[{'page':i+1,'text':reader.pages[i].extract_text()} for i in range(21,40)]
retained=read(str((HERE/'pdf-M02-text.json').relative_to(ROOT)))
check('Fresh PDF extraction equals retained M02 evidence',fresh==retained['pages'] and retained['pdf']==payload['source_curriculum']['pdf'],'Pages 22–40')
remaining={}
nav=read('docs/curriculum/pdf-production/chapters/M02/navigation.json')
for row in fresh:
    no=row['page'];text=norm(row['text']);header='KörkortGo · '+nav['page_labels'][str(no-21)];tail=f'Contents Sources Previous page {no} Next page'
    if not text.startswith(header) or not text.endswith(tail):raise ValueError('Unrecognised PDF chrome')
    remaining[no]=text[len(header):-len(tail)].strip()
def consume(value,pages,id):
    value=norm(value);matches=[p for p in pages if value in remaining[p]]
    ok=bool(matches)
    check(id+' complete in approved PDF',ok,{'pages':matches,'characters':len(value)})
    if matches:remaining[matches[0]]=remaining[matches[0]].replace(value,'',1).strip()
page_ranges={'M02':[22],'M02-L01':[23,24,25],'M02-L02':[26,27],'M02-L03':[28,29,30],'M02-L04':[31,32],'M02-R':[33,34]}
for id in IDS:
    pages=page_ranges[id]
    if id=='M02':consume('CHAPTER 02',pages,'chapter label')
    elif id!='M02-R':consume(id,[pages[0]],id+' printed ID')
    consume(docs[id]['title'],[pages[0]],id+' title')
    for bid,text in leaves(docs[id]['body_blocks']):
        if bid=='M02/source-dates':continue
        consume(text,pages,bid)
    for a in docs[id]['answer_blocks']:
        consume(id,[35],id+' answer label')
        for bid,text in leaves(a['blocks']):consume(text,[35],bid)
consume('Answers and review guidance',[22],'answer navigation')
consume('References and vehicle handbooks',[22],'reference navigation')
consume('Review after answering',[35],'answer section heading')
labels={}
for label,alias in re.findall(r'\[([^]]+)\]\[([^]]+)\]',source_text):labels.setdefault(alias,label)
for offset in range(0,len(urls),4):
    page=36+offset//4
    consume('References and vehicle handbooks',[page],f'reference heading {page}')
    consume(dict(leaves(docs['M02']['body_blocks']))['M02/source-dates'],[page],f'source check dates {page}')
    # PDF line wrapping can split URLs midword, so compare their exact non-whitespace bytes.
    for alias in list(urls)[offset:offset+4]:
        consume(labels[alias],[page],'reference label '+alias)
        compact=''.join(remaining[page].split());url=urls[alias]
        check('Exact PDF source URL '+alias,url in compact,url)
        compact=compact.replace(url,'',1)
        # Remove URL directly with whitespace-tolerant character matching, preserving remaining text spaces.
        remaining[page]=re.sub(r'\s*'.join(re.escape(c) for c in url),'',remaining[page],count=1).strip()
for no,text in remaining.items():check(f'PDF page {no} has no unmatched teaching',not text.strip(),text)
art=read(ART)['assets']
for id,a in art.items():
    parent=id.removesuffix('-cabin');image=next(b['payload'] for b in docs[parent]['body_blocks'] if b['payload'].get('asset_id')==id+'/illustration');asset=next(a for a in payload['assets'] if a['id']==image['asset_id']);region=image['region']
    check(id+' exact approved crop/caption/alt/hash',[region[k] for k in ['left','top','right','bottom']]==a['box'] and plain(image['caption'])==a['caption'] and asset['study_alt_text']==a['alt_text'] and asset['original']==asset['bundled'] and asset['original']['sha256']==a['sha256'] and image.get('polygon')==([{'x':x,'y':y} for x,y in a['polygon']] if a.get('polygon') else None),image)
check('No M02 first-aid expansion','1177' not in json.dumps([docs[i] for i in IDS]),'No 1177 references or new medical instructions; approved vehicle/restraint wording retained')
paths={'curriculum':ROOT/'content/curriculum.json',**{k:HERE/(k+'.json') for k in ['questions','sources','legacy_aliases']}};manifest=HERE/'staging-manifest.json'
with tempfile.TemporaryDirectory() as temp:
    out=Path(temp)/'generated';trace=Path(temp)/'trace.json'
    totals=compile_files(paths,manifest,out,trace,symbol='stagedCurriculum9B3')
    hashes={p.name:sha(p) for p in out.glob('*.kt')};tracehash=sha(trace)
    check('Saved Kotlin equals fresh generation',hashes=={p.name:sha(p) for p in (HERE/'generated').glob('*.kt')},len(hashes))
    check('Saved trace equals fresh trace',tracehash==sha(HERE/'trace.json'),tracehash)
    compile_files(paths,manifest,out,trace,symbol='stagedCurriculum9B3')
    check('Repeated generation byte-identical',hashes=={p.name:sha(p) for p in out.glob('*.kt')} and tracehash==sha(trace),totals)
    try:compile_files(paths,manifest,out,trace,profile='release',symbol='stagedCurriculum9B3')
    except ContentError as exc:check('Partial import cannot pass release',any(reason in str(exc) for reason in ['incomplete canonical','release assets must use curriculum Compose resources']),str(exc))
    else:check('Partial import cannot pass release',False,'Unexpected release success')
# Earlier evidence remains immutable; authoring payload and evolving compiler/model are expected to change.
previous=read('docs/curriculum/app-migration/implementation-evidence/9B2/verification.json')
protected=[a for a in previous['artifacts'] if '/implementation-evidence/9B2/' in a['path'] or a['path'] in ['tools/import_curriculum_opening.py','tools/import_curriculum_m01.py']]
changed=[a['path'] for a in protected if sha(ROOT/a['path'])!=a['sha256']]
check('Previous step evidence unchanged',not changed,changed)
authority=read('docs/curriculum/app-migration/implementation-evidence/9A1/input-baseline.json')
allowed={'tools/build_content.py','composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','docs/curriculum/implementation-plan.md'}
changed=[a['path'] for a in authority['input_manifest'] if a['path'] not in allowed and sha(ROOT/a['path'])!=a['sha256']]
check('Approved source/assets/live question bank unchanged',not changed,changed)
for name,count in [('QuizTest',6),('CurriculumContractTest',5),('M02ImportTest',4)]:
    xml=ET.parse(HERE/f'TEST-se.korkort.{name}.xml').getroot();result={k:int(xml.attrib[k]) for k in ['tests','failures','errors','skipped']}
    check(name+' passes',result=={'tests':count,'failures':0,'errors':0,'skipped':0},result)
report={'step':'9B3','module_id':'M02','status':'complete' if all(c['passed'] for c in checks) else 'failed','checks':checks,'totals':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'source_paragraphs':len(comparisons),'documents':6,'hidden_answers':5,'illustrations':6,'polygon_masks':2,'tables':1,'scoped_sources':19,'pending_reading_bodies':48,'jvm_tests':15,'python_tests':74,'generated_files':len(hashes)},'normalized_block_comparisons':comparisons,'normalization':'Markdown emphasis/reference markup becomes typed structure; whitespace collapses. Table headers/cells retain row order. Exact source labels, punctuation and complete answers retained. Every PDF teaching fragment consumed; only enumerated print chrome removed. Source URLs compared without line-wrap whitespace.','source_pdf':payload['source_curriculum']['pdf'],'next_step':'9B4 — M03; separately requested','scope_limits':['No live reader or source directory integration.','Asset sheets retain exact bytes and approved typed windows; Compose packaging/delivery remains 9C4.','No source-currency claim beyond retained 4/12 October checks.','No learner state, bank, score or official sign changes.']}
(HERE/'module-parity.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
artifacts=[ROOT/'content/curriculum.json',ROOT/'content/curriculum-import-state.json',ROOT/'tools/import_curriculum_m02.py',ROOT/'tools/test_import_curriculum_m02.py',ROOT/'tools/test_import_curriculum_m01.py',ROOT/'tools/test_compile_curriculum.py',ROOT/'tools/compile_curriculum.py',ROOT/'composeApp/src/commonMain/kotlin/se/korkort/Curriculum.kt']+[p for p in HERE.rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts]
verification={'step':'9B3','date':'2026-10-15','status':report['status'],'totals':report['totals'],'parity_report':{'path':str((HERE/'module-parity.json').relative_to(ROOT)),'sha256':sha(HERE/'module-parity.json')},'staging_identity':read(str(manifest.relative_to(ROOT)))['identity'],'artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(artifacts)],'next_step':report['next_step']}
(HERE/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':report['status'],'totals':report['totals'],'failures':[c for c in checks if not c['passed']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if report['status']=='complete' else 1)
