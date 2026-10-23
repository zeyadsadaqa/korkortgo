"""Stage reviewed step10 source/description amendments without activating a release.

The original accepted package and historical generators/receipts remain intact.
Changed question descriptions receive new revisions and delivery holds, never copied
acceptance decisions. Generated Kotlin is a separate unaccepted verification candidate.
"""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path

from build_navigation import SharedEmitter
from compile_curriculum import ROOT, Validator, manifest_digest, kotlin_string
from content_schema import Schema

AUTHOR = Path('docs/curriculum/app-migration/verification-evidence/10L1/content-corrections/amendments.json')
OUT = Path('docs/curriculum/app-migration/verification-evidence/10L2/content-corrections/candidate')
load = lambda p: json.loads((ROOT / p).read_text())
dump = lambda x: json.dumps(x, indent=2, ensure_ascii=False) + '\n'
sha = lambda p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
identity = lambda p: {'path': str(p), 'sha256': sha(p)}


def reviewed_origin(pointer):
    return {'file': identity(AUTHOR), 'locator': 'json:' + pointer, 'evidence_ids': [], 'pdf_evidence_page': None}


def build():
    amendments = load(AUTHOR)
    base_path = Path(amendments['base_release']['path'])
    assert sha(base_path) == amendments['base_release']['sha256'], 'Frozen base changed'
    base = json.loads(gzip.decompress((ROOT / base_path).read_bytes()))
    data = copy.deepcopy(base['files'])
    c = data['content/curriculum.json']
    questions = data['content/accepted-assessment-questions.json']['questions']
    changed = set()
    for source_path in ('content/sources.json', 'content/package-sources.json'):
        refs = {r['id']: r for r in data[source_path]['references']}
        for correction in amendments['classifications']:
            row = refs[correction['reference_id']]
            assert row['url'] == correction['url'] and row['publisher'] == correction['publisher']
            assert row['classifications'] == correction['before']
            row['classifications'] = correction['after']
            row['classification_note'] += ' ' + correction['basis']
    assets = {r['id']: r for r in c['assets']}
    signs = {r['code']: r for r in c['sign_entries']}
    for code, correction in amendments['captions'].items():
        asset = assets[correction['asset_id']]
        sign = signs[code]
        assert asset['original'] == correction['original']
        assert asset['variant'] == correction['before_variant']
        assert asset['study_alt_text'] == correction['before_study_alt_text']
        assert sign['caption'] == correction['before_caption']
        asset['variant'] = correction['after_variant']
        asset['study_alt_text'] = correction['after_study_alt_text']
        asset['approval'].append({'record': reviewed_origin('/captions/' + code), 'reviewed_on': amendments['reviewed_on']})
        sign['caption'] = correction['after_caption']
        sign['origin'] = reviewed_origin('/captions/' + code)
    correction = amendments['descriptions']['X9']
    for q in questions:
        images = [i for i in [q['image'], *[o['image'] for o in q['options']]] if i and i['asset_id'] == correction['asset_id']]
        if not images:
            continue
        assert q['key']['question_id'] in correction['question_ids']
        for image in images:
            assert image['neutral_description']['text'] == correction['before']
            image['neutral_description'] = {'text': correction['after'], 'review': {'record': reviewed_origin('/descriptions/X9'), 'reviewed_on': amendments['reviewed_on']}}
        q['key']['revision'] += '-step10-description-r1'
        q['acceptance']['eligibility'] = 'held'
        q['acceptance']['description_reviews'] = [{'record': reviewed_origin('/descriptions/X9'), 'reviewed_on': amendments['reviewed_on']}]
        q['acceptance']['delivery_proof'] = []
        q['acceptance']['open_holds'] = [{'id': q['key']['question_id'] + '/step10-description-delivery', 'reason': 'Corrected neutral description needs fresh exact-revision target delivery acceptance.', 'release_condition': 'Retain new approved description/revision, complete affected configured-target delivery and record renewed acceptance before activation.'}]
        changed.add(q['key']['question_id'])
    assert changed == set(correction['image_question_ids']) and len(changed) == 7
    # Independently constrain the change: no identity, key, prompt or feedback substitution.
    originals = {q['key']['question_id']: q for q in base['files']['content/accepted-assessment-questions.json']['questions']}
    for q in questions:
        original = originals[q['key']['question_id']]
        assert q['concept_id'] == original['concept_id'] and q['feedback'] == original['feedback']
        assert q['prompt'] == original['prompt'] and [o['id'] for o in q['options']] == [o['id'] for o in original['options']]
        if q['key']['question_id'] not in changed:
            assert q == original
    assert len(questions) == 1000 and len({q['concept_id'] for q in questions}) == 500
    for asset in c['assets']:
        original = next(a for a in base['files']['content/curriculum.json']['assets'] if a['id'] == asset['id'])
        assert asset['original'] == original['original'] and asset['bundled'] == original['bundled']
    validator = Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json')
    validator.typed(c, 'CurriculumPayload', 'corrected curriculum')
    validator.typed({'schema_version': 1, 'questions': questions}, 'QuestionPayload', 'corrected questions')
    validator.typed(data['content/package-sources.json'], 'SourcePayload', 'corrected sources')
    return amendments, base, data, changed


def outputs():
    amendments, base, data, changed = build()
    files = {}
    for source in ('content/curriculum.json', 'content/sources.json', 'content/package-sources.json', 'content/accepted-assessment-questions.json', 'content/legacy-aliases.json'):
        files[OUT / source] = dump(data[source])
    # A separate identity is bound to exact staged payload bytes, not the old accepted release.
    manifest = copy.deepcopy(data['content/accepted-content-manifest.json'])
    manifest['identity']['content_version'] += '-step10-unaccepted-r1'
    for row in manifest['payloads']:
        source = row['file']['path']
        if OUT / source in files:
            row['file'] = {'path': str(OUT / source), 'sha256': hashlib.sha256(files[OUT / source].encode()).hexdigest()}
    manifest['inputs'] += [identity(AUTHOR), identity(Path(__file__).resolve().relative_to(ROOT)), identity(Path(amendments['base_release']['path']))]
    manifest['question_revisions'] = [{'key': q['key'], 'eligibility': q['acceptance']['eligibility']} for q in data['content/accepted-assessment-questions.json']['questions']]
    manifest['identity']['manifest_sha256'] = manifest_digest(manifest)
    files[OUT / 'candidate-manifest.json'] = dump(manifest)
    emitter = SharedEmitter(Schema(ROOT), 'step10Candidate')
    questions = [q for q in data['content/accepted-assessment-questions.json']['questions'] if q['key']['question_id'] in changed]
    call = emitter.emit(questions, 'List<AssessmentQuestion>', 'step10 changed-description fixtures')
    source_ids = {r['reference_id'] for r in amendments['classifications']}
    sources = emitter.emit([r for r in data['content/package-sources.json']['references'] if r['id'] in source_ids], 'List<SourceReference>', 'step10 corrected-source fixtures')
    signs = emitter.emit([r for r in data['content/curriculum.json']['sign_entries'] if r['code'] in amendments['captions']], 'List<SignEntry>', 'step10 corrected-sign fixtures')
    asset_ids = {r['asset_id'] for r in amendments['captions'].values()}
    assets = emitter.emit([r for r in data['content/curriculum.json']['assets'] if r['id'] in asset_ids], 'List<CurriculumAsset>', 'step10 corrected-asset fixtures')
    header = '// Generated by tools/stage_step10_corrections.py; unaccepted verification candidate.\npackage se.korkort\n\n'
    top = header + 'internal val step10CandidateQuestions: List<AssessmentQuestion> by lazy { ' + call + ' }\n'
    top += 'internal val step10CandidateIdentity = ContentPackageIdentity(' + kotlin_string(manifest['identity']['content_version']) + ', Sha256(' + kotlin_string(manifest['identity']['manifest_sha256']) + '))\n'
    top += 'internal val step10CandidateBank by lazy { PracticeBank(step10CandidateIdentity, step10CandidateQuestions, false) }\n'
    top += 'internal val step10CorrectedSources: List<SourceReference> by lazy { ' + sources + ' }\n'
    top += 'internal val step10CorrectedSigns: List<SignEntry> by lazy { ' + signs + ' }\n'
    top += 'internal val step10CorrectedAssets: List<CurriculumAsset> by lazy { ' + assets + ' }\n'
    files[OUT / 'kotlin/Step10Candidate.kt'] = top
    for i in range(0, len(emitter.functions), 200):
        files[OUT / f'kotlin/Step10CandidatePart{i//200:03}.kt'] = header + ''.join(f'internal fun {fn}(): {kind} = {expr}\n' for fn, kind, expr in emitter.functions[i:i+200])
    files[OUT / 'review-status.json'] = dump({'status': 'staged_unaccepted', 'active_release_changed': False, 'source_classification_corrections': 6, 'caption_corrections': ['C18', 'M8'], 'new_description_revisions': sorted(changed), 'accepted_unchanged_questions': 993, 'held_new_description_revisions': 7, 'related_description_audit_contexts': 12, 'official_artwork_bytes_changed': False, 'description_delivery_acceptance': 'pending; old delivery proof was not copied', 'candidate_identity': manifest['identity']})
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--stage', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = outputs()
    for stale in (ROOT / OUT / 'kotlin').glob('Step10CandidatePart*.kt'):
        if stale.relative_to(ROOT) not in files:
            assert stale.read_text().startswith('// Generated by tools/stage_step10_corrections.py;')
            if args.check:
                raise AssertionError('Stale staged generated file: ' + str(stale))
            stale.unlink()
    for path, text in files.items():
        if args.check:
            assert (ROOT / path).read_text() == text, path
        else:
            (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / path).write_text(text)
    manifest = load(OUT / 'candidate-manifest.json')
    payloads = {r['kind']: load(Path(r['file']['path'])) for r in manifest['payloads'] if r['kind'] != 'asset'}
    result = Validator(source_authority='docs/curriculum/app-migration/implementation-evidence/9J/source-authority.json').package(payloads, manifest, 'fixture')
    validation = dump({'status': 'pass_fixture_structure_not_release_acceptance', 'result': result})
    path = ROOT / OUT / 'validation.json'
    if args.check:
        assert path.read_text() == validation
    else:
        path.write_text(validation)
    print('PASS: six source classifications and three descriptions staged; 7 new description revisions held; active release unchanged.')


if __name__ == '__main__':
    main()
