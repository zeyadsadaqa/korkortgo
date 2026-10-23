"""Reproduce the bounded step10 release from frozen base, amendments and renewed delivery.

Never rewrites the historical 9J/9L receipts or authoring candidate. Release activation
requires exact revised-question delivery on every configured target and setting.
"""
import argparse
import copy
import hashlib
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import build_navigation
import build_reader
import stage_step10_corrections as staged
from build_navigation import SharedEmitter
from compile_curriculum import ROOT, Validator, kotlin_string, manifest_digest
from content_schema import Schema

BASE = Path('docs/curriculum/app-migration/verification-evidence/10L3/content-corrections')
RECEIPT = BASE / 'renewed-delivery-acceptance.json'
RELEASE = BASE / 'release'
DEST = Path('composeApp/src/commonMain/kotlin/se/korkort')
SCRIPT = Path(__file__).resolve().relative_to(ROOT)
AUTHORITY = 'docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json'
canonical = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
dump = lambda x: json.dumps(x, ensure_ascii=False, indent=2) + '\n'
sha = lambda data: hashlib.sha256(data).hexdigest()
read = lambda p: json.loads((ROOT / p).read_text())
identity = lambda p: {'path': str(p), 'sha256': sha((ROOT / p).read_bytes())}



def observed_delivery():
    """Normalize retained raw rows; flags in the acceptance receipt cannot replace cases."""
    paths = {
        'android': [('android-corrected-r1/question-matrix-0-7.json', False), ('android-dark-r2/question-matrix-0-7.json', True)],
        'ios_simulator': [('ios-corrected-r1/rows.json', False), ('ios-dark-r2/rows.json', True)],
        'browser': [('browser-corrected-r2/rows.json', False), ('browser-dark-r3/rows.json', True)],
        'desktop': [('desktop-corrected-r3/result.json', None)],
    }
    inputs=[]; targets={}
    for target, sources in paths.items():
        result=[]
        for suffix, selected_dark in sources:
            path=BASE/suffix;inputs.append(path)
            payload=read(path)
            rows=payload['rows'] if isinstance(payload,dict) else payload
            for row in rows:
                dark=row.get('dark',row.get('theme')=='dark')
                if selected_dark is not None and dark != selected_dark: continue
                result.append({'question_id':row['question_id'],'revision':row['revision'],
                    'setting':('dark' if dark else 'light')+'/'+format(float(row['font_scale']),'g'),
                    'width':row.get('width'), 'zoom_returns':row.get('image_zoom_returns',row.get('zoom_returns'))})
        assert len(result)==(56 if target=='desktop' else 28), target
        keys={(r['question_id'],r['revision'],r['setting'],r['width']) for r in result}
        assert len(keys)==len(result), 'Duplicate delivery cases: '+target
        assert sum(r['zoom_returns'] for r in result)==(200 if target=='desktop' else 100), target
        targets[target]=result
    metadata=BASE/'metadata-corrected-r1/results.json';inputs.append(metadata)
    assert len(read(metadata)['cases'])==32
    return targets,inputs


def require_delivery(receipt, questions):
    assert receipt['status'] == 'passed_exact_changed_revision_delivery'
    assert receipt['ios_scope'] == 'simulator'
    assert receipt['candidate_manifest'] == identity(staged.OUT / 'candidate-manifest.json')
    for file in receipt['inputs']:
        assert file == identity(Path(file['path'])), file['path']
    observed,raw_inputs=observed_delivery()
    bound={f['path'] for f in receipt['inputs']}
    assert {str(p) for p in raw_inputs}.issubset(bound), 'Missing raw delivery input'
    expected = {q['key']['question_id']: q for q in questions}
    assets={a['id']:a for a in read(staged.OUT/'content/curriculum.json')['assets']}
    platforms=set(read(Path('content/delivery-targets.json'))['required_platforms'])
    rows = receipt['questions']
    assert len(rows) == len(expected) == 7
    assert {r['question_id'] for r in rows} == set(expected)
    for row in rows:
        q = expected[row['question_id']]
        assert row['revision'] == q['key']['revision']
        assert row['assessment_sha256'] == sha(canonical({k:v for k,v in q.items() if k!='acceptance'}))
        assert row['status'] == 'passed'
        assert row['reviewed_description_and_artwork'] is True
        image_ids={i['asset_id'] for i in [q['image'],*[o['image'] for o in q['options']]] if i}
        assert {a['asset_id'] for a in row['assets']}==image_ids and len(row['assets'])==len(image_ids)
        for a in row['assets']:
            assert a['status']=='passed' and a['asset_sha256']==assets[a['asset_id']]['bundled']['sha256']
            assert set(a['platforms'])==platforms
        assert set(row['targets']) == {'android', 'desktop', 'ios_simulator', 'browser'}
        for name,target in row['targets'].items():
            assert set(target['settings']) == {'light/1', 'light/1.6', 'dark/1', 'dark/1.6'}
            assert target['status'] == 'passed'
            actual=[r for r in observed[name] if r['question_id']==row['question_id']]
            assert len(actual)==(8 if name=='desktop' else 4), name
            assert {r['revision'] for r in actual}=={row['revision']}
            assert {r['setting'] for r in actual}==set(target['settings'])
            if name=='desktop': assert {r['width'] for r in actual}=={390,1280}
    return {r['question_id']: i for i,r in enumerate(rows)}


def outputs():
    amendments, base, data, changed = staged.build()
    questions = data['content/accepted-assessment-questions.json']['questions']
    receipt = read(RECEIPT)
    positions = require_delivery(receipt, [q for q in questions if q['key']['question_id'] in changed])
    for q in questions:
        if q['key']['question_id'] not in changed:
            continue
        index=positions[q['key']['question_id']]
        q['acceptance'].update(eligibility='accepted', open_holds=[], delivery_proof=[{
            'record': {'file': identity(RECEIPT), 'locator': 'json:/questions/'+str(index)+'/assets/'+str(asset_index), 'evidence_ids': [], 'pdf_evidence_page': None},
            'reviewed_on': receipt['reviewed_on']} for asset_index in range(len(receipt['questions'][index]['assets']))])
    files = {Path(p): dump(data[p]) for p in ('content/curriculum.json','content/sources.json','content/package-sources.json','content/accepted-assessment-questions.json')}
    manifest = copy.deepcopy(base['files']['content/accepted-content-manifest.json'])
    manifest['identity']['content_version'] += '-step10-r1'
    for row in manifest['payloads']:
        p = Path(row['file']['path'])
        if p in files:
            row['file']['sha256'] = sha(files[p].encode())
    for p in (staged.AUTHOR, Path(amendments['base_release']['path']), RECEIPT, SCRIPT, Path('docs/curriculum/app-migration/verification.json')):
        manifest['inputs'].append(identity(p))
    for row in manifest['canonical_revisions']:
        if row['id'] in {'sign-C18','sign-M8'}: row['revision'] += '-step10-caption-r1'
    manifest['question_revisions'] = [{'key':q['key'],'eligibility':q['acceptance']['eligibility']} for q in questions]
    manifest['identity']['manifest_sha256'] = manifest_digest(manifest)
    files[Path('content/accepted-content-manifest.json')] = dump(manifest)
    # Pure emitter APIs with explicit corrected authoring; historical output receipts are redirected.
    original_read = build_navigation.read
    def corrected_read(path):
        return copy.deepcopy(data[str(path)]) if str(path) in data else original_read(path)
    with patch.object(build_navigation,'read',side_effect=corrected_read), patch.object(build_reader,'read',side_effect=corrected_read):
        files.update(build_navigation.generate())
        reader = build_reader.generate()
        old_parity = Path('docs/curriculum/app-migration/implementation-evidence/9L/reader-parity.tsv')
        files[RELEASE/'reader-parity.tsv'] = reader.pop(old_parity)
        files.update(reader)
    emitter = SharedEmitter(Schema(ROOT),'accepted9J')
    decision_ids = {r['question_id'] for r in read(Path('docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14/delivery-acceptance.json'))['questions']}
    original_questions = base['files']['content/accepted-assessment-questions.json']['questions']
    entries=[]
    for q in original_questions:
        if q['key']['question_id'] in decision_ids:
            call=emitter.emit(q['acceptance'],'AssessmentAcceptance',q['key']['question_id']+'/accepted')
            entries.append(kotlin_string(q['key']['question_id'])+' to '+call)
    chunks=[emitter.function('Map<String, AssessmentAcceptance>','mapOf('+', '.join(entries[i:i+20])+')','original acceptance map',None) for i in range(0,len(entries),20)]
    replacements=[]
    for q in questions:
        if q['key']['question_id'] in changed:
            call=emitter.emit(q,'AssessmentQuestion',q['key']['question_id']+'/corrected')
            replacements.append(kotlin_string(q['key']['question_id'])+' to '+call)
    header='// Generated by tools/finalize_step10_corrections.py; bounded corrected accepted release.\npackage se.korkort\n\n'
    top=header+'private val acceptedDecisions9J by lazy { '+' + '.join(chunks)+' }\n'
    top+='private val correctedQuestionsStep10 by lazy { mapOf('+', '.join(replacements)+') }\n'
    top+='internal val acceptedQuestions9J: List<AssessmentQuestion> by lazy { candidateQuestions9J.map { q -> correctedQuestionsStep10[q.key.questionId.value] ?: q.copy(acceptance = acceptedDecisions9J[q.key.questionId.value] ?: q.acceptance) } }\n'
    top+='internal val acceptedIdentity9J = ContentPackageIdentity('+kotlin_string(manifest['identity']['content_version'])+', Sha256('+kotlin_string(manifest['identity']['manifest_sha256'])+'))\n'
    top+='internal val acceptedPracticeBank9J by lazy { PracticeBank(acceptedIdentity9J, acceptedQuestions9J, true) }\ninternal const val acceptedQuestionCount9J = 1000\n'
    c=data['content/curriculum.json']
    top+='internal val acceptedCurriculumSummary9J = CurriculumSummary("2026 curriculum", '+str(len(c['modules']))+', '+str(sum(len(m['lesson_ids']) for m in c['modules']))+', 1000, '+str(len(c['sign_entries']))+')\n'
    files[DEST/'AcceptedQuestionPackage9J.kt']=top
    for n in range(0,len(emitter.functions),200):
        files[DEST/f'AcceptedQuestionPackage9JPart{n//200:03}.kt']=header+''.join(f'internal fun {name}(): {kind} = {expr}\n' for name,kind,expr in emitter.functions[n:n+200])
    files[RELEASE/'accepted-question-parity.tsv']=''.join(q['key']['question_id']+'\t'+sha(canonical(q))+'\n' for q in questions)
    files[RELEASE/'release-validation.json']=dump({'status':'passed_release_structure_and_renewed_delivery','identity':manifest['identity'],'questions':1000,'concepts':500,'accepted':1000,'held':0,'changed_revisions':sorted(changed),'historical_candidate_unchanged':True,'ios_scope':'simulator'})
    return files


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    args=parser.parse_args()
    files=outputs() # All receipt/precondition checks precede any mutation.
    # Validate future payload bytes in an isolated filesystem view before activation.
    with tempfile.TemporaryDirectory(prefix='korkort-step10-release-') as directory:
        sandbox=Path(directory)
        # Copy only referenced evidence. Symlinks are rejected by the validator;
        # independent files also avoid changing original inode metadata with hard links.
        prospective=json.loads(files[Path('content/accepted-content-manifest.json')])
        payloads={r['kind']:json.loads(files[Path(r['file']['path'])]) if Path(r['file']['path']) in files else read(Path(r['file']['path'])) for r in prospective['payloads'] if r['kind']!='asset'}
        def references(value):
            if isinstance(value,dict):
                if isinstance(value.get('path'),str) and 'sha256' in value: yield Path(value['path'])
                for child in value.values(): yield from references(child)
            elif isinstance(value,list):
                for child in value: yield from references(child)
        paths=set(references([prospective,payloads]))|{Path(AUTHORITY)}
        for path in paths:
            destination=sandbox/path;destination.parent.mkdir(parents=True,exist_ok=True)
            if path in files:destination.write_text(files[path])
            else:shutil.copy2(ROOT/path,destination)
        for p,text in files.items():
            if p.parts[0]=='content': (sandbox/p).parent.mkdir(parents=True,exist_ok=True); (sandbox/p).write_text(text)
        prospective=json.loads(files[Path('content/accepted-content-manifest.json')])
        payloads={r['kind']:json.loads((sandbox/r['file']['path']).read_text()) for r in prospective['payloads'] if r['kind']!='asset'}
        Validator(root=sandbox,source_authority=AUTHORITY).package(payloads,prospective,'release')
    base=staged.build()[1]
    for p,text in files.items():
        if str(p) in base['sha256']:
            assert sha((ROOT/p).read_bytes()) in {base['sha256'][str(p)],sha(text.encode())}, 'Unexpected active edits: '+str(p)
    for p,text in files.items():
        if args.check: assert (ROOT/p).read_text()==text,p
        else: (ROOT/p).parent.mkdir(parents=True,exist_ok=True);(ROOT/p).write_text(text)
    manifest=read(Path('content/accepted-content-manifest.json'))
    payloads={r['kind']:read(Path(r['file']['path'])) for r in manifest['payloads'] if r['kind']!='asset'}
    result=Validator(source_authority=AUTHORITY).package(payloads,manifest,'release')
    print('PASS: bounded step10 corrected release; exact renewed delivery; '+str(result))


if __name__=='__main__':main()
