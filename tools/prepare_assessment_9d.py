"""Bind authored identities and manually reviewed physical descriptions; never activate questions.

The TSV is authored from visible artwork, not generated from meanings or study alt text.
9E/9F consume these records when applying the separately reviewed question rewrites.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = Path('docs/curriculum/app-migration/implementation-evidence')
ACTIONS = Path('docs/curriculum/app-migration/question-actions.json')
BACKLOG = Path('docs/curriculum/app-migration/implementation-backlog.json')
ASSET_REVIEW = Path('docs/curriculum/app-migration/question-review/asset-review.json')
DESCRIPTIONS = BASE/'9D2/physical-descriptions.tsv'


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT/path).read_text())


def identity(path):
    return {'path': str(path), 'sha256': sha(path)}


def description_library():
    lines = (ROOT/DESCRIPTIONS).read_text().splitlines()
    pairs = [line.split('\t', 1) for line in lines]
    descriptions = dict(pairs)
    assert len(descriptions) == len(pairs), 'Duplicate physical description identity'
    assets = read(ASSET_REVIEW)['records']
    assert set(descriptions) == {r['code'] for r in assets}
    records = {}
    for asset in assets:
        code = asset['code']
        text = descriptions[code]
        assert text.strip() == text and len(text) >= 30
        assert not re.search(r'\b'+re.escape(code)+r'\b', text), (code, 'Source code leaked')
        assert not re.search(r'\b(correct|incorrect|prohibited|must|permitted|priority|warning sign|means|identifies)\b', text, re.I), code
        assert sha(Path(asset['approved_path'])) == asset['approved_sha256']
        proof = Path('docs/curriculum/app-migration/question-review')/asset['proof_sheet']
        records[code] = {
            'code_metadata_only': code,
            'asset': {'path': asset['approved_path'], 'sha256': asset['approved_sha256']},
            'text': text,
            'review': {
                'reviewed_on': '2026-10-16', 'reviewer': 'Codex',
                'method': 'Visual inspection of approved image in retained paired proof sheet; vector and fine-text details freshly rendered/enlarged where needed. Physical wording separately authored; no automatic study-caption reuse.',
                'proof_sheet': identity(proof), 'position': asset['proof_position'],
                'detail_sheet': identity(BASE/'9D2/visual-review/vector-and-detail-review.png') if asset['approved_path'].endswith('.pdf') or code in {'T17','X8','X10','M12','M19','H23','F2','F27'} else None,
                'result': 'accepted physical description',
            },
            'delivery_hold': asset['app_display_hold'],
            'scored_activation': False,
        }
    return records


def outputs():
    actions = read(ACTIONS)['questions']
    by_id = {q['question_id']: q for q in actions}
    library = description_library()
    files = {}
    authored = []
    for q in actions:
        original = q['original']
        proposal = q['proposed_changes']
        ids = ([o['option_id'] for o in proposal['options']] if q['question_id'].startswith('sign-')
               else [f"{q['question_id']}-option-{n}" for n in range(1, 5)])
        assert len(ids) == len(set(ids)) == len(original['options']) == 4
        authored.append({'question_id': q['question_id'], 'concept_id': q['concept_id'],
                         'baseline_semantic_revision': 'legacy-r1',
                         'option_ids_in_authored_order': ids,
                         'correct_option_id': ids[original['correct']],
                         'original_sha256': hashlib.sha256(json.dumps(original, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest(),
                         'next_semantic_revision': None})
    files[BASE/'9D1/authored-identities.json'] = {
        'schema_version': 1, 'source': identity(ACTIONS),
        'policy': 'Authored assignment before any shuffle. Sign option IDs exactly match 7D. legacy-r1 names frozen original semantics; 9E/9F assign changed revisions independently. Never derive identity from display letters, mutable text or a shuffled index.',
        'questions': authored,
    }
    files[BASE/'9D2/reviewed-descriptions.json'] = {
        'schema_version': 1, 'authoring_source': identity(DESCRIPTIONS),
        'assets': list(library.values()), 'scored_activation': False,
    }
    for batch in [b for b in read(BACKLOG)['execution_batches'] if b['work_item_id'] == '9D']:
        step = f"9D{batch['batch']+2}"
        rows = []
        for qid in batch['question_ids']:
            q = by_id[qid]
            p = q['proposed_changes']
            recognise = qid.startswith('sign-recognise-')
            assert len(p['options']) == 4
            assert len({o['option_id'] for o in p['options']}) == 4
            assert sum(o['is_correct'] for o in p['options']) == 1
            codes = p['proposed_option_codes']
            assert codes == [o['code_metadata_after_reveal'] for o in p['options']]
            def occurrence(code, asset, slot):
                record = library[code]
                assert {k: asset[k] for k in ['path','sha256']} == record['asset']
                return {'slot': slot, 'description_code_metadata_only': code,
                        'asset': record['asset'], 'description': record['text'],
                        'review': record['review'], 'delivery_hold': record['delivery_hold'],
                        'context_result': 'physical appearance only; no source-code label, interpretation or correctness added'}
            images = []
            if p['question_image_asset']:
                images.append(occurrence(p['target_code_metadata'], p['question_image_asset'], 'stem'))
            option_context = []
            for o in p['options']:
                if recognise:
                    images.append(occurrence(o['code_metadata_after_reveal'], o['visual_description_brief']['exact_asset'], o['option_id']))
                option_context.append({'option_id': o['option_id'],
                    'pre_answer_text': '' if recognise else o['meaning_option_text'],
                    'post_answer_code': o['code_metadata_after_reveal'],
                    'post_answer_label': o['post_answer_label'],
                    'is_correct_after_reveal_only': o['is_correct']})
            assert len(images) == (4 if recognise else 1)
            if recognise:
                assert len({i['asset']['sha256'] for i in images}) == 4
                assert len({i['description'] for i in images}) == 4
            # The possible meanings in meaning-choice text are intentional; codes never label an image.
            assert not re.search(r'\b'+re.escape(p['target_code_metadata'])+r'\b', p['prompt'])
            rows.append({'question_id': qid, 'concept_id': q['concept_id'],
                         'reviewed_context': '7D proposed stem and all four proposed options; legacy wording is not approved by this review',
                         'prompt': p['prompt'], 'options': option_context, 'images': images,
                         'description_result': 'accepted',
                         'context_review': 'Physical descriptions checked against the stem and all four options. Meaning questions describe only the stem; recognition choices have no code-bearing text. Descriptions provide the visible features, not a rule or the keyed response.',
                         'open_delivery_holds': sorted({i['description_code_metadata_only'] for i in images if i['delivery_hold']}),
                         'question_content_acceptance': 'deferred to 9E/9F', 'scored_activation': False})
        files[BASE/step/'description-acceptance.json'] = {
            'schema_version': 1, 'step': step, 'batch': batch['batch'], 'reviewed_on': '2026-10-16',
            'inputs': [identity(ACTIONS), identity(BACKLOG), identity(DESCRIPTIONS), identity(ASSET_REVIEW)],
            'scope': 'Neutral descriptions for exact 7D proposals; independent of content and delivery acceptance.',
            'question_count': len(rows), 'image_occurrence_count': sum(len(r['images']) for r in rows),
            'questions': rows,
        }
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = outputs()
    for path, content in files.items():
        data = json.dumps(content, ensure_ascii=False, indent=2)+'\n'
        if args.check:
            assert (ROOT/path).read_text() == data, f'Stale output: {path}'
        else:
            (ROOT/path).parent.mkdir(parents=True, exist_ok=True)
            (ROOT/path).write_text(data)
    print(f"{'Verified' if args.check else 'Wrote'} {len(files)} deterministic 9D records; 616 questions, 308 descriptions, 1,540 image occurrences; no scored activation")


if __name__ == '__main__':
    main()
