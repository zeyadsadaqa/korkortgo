#!/usr/bin/env python3
"""Verify the local 4A–4E package. Requires Pillow; run from any directory.
Exit 0: ready; 2: verification ran, but required image gaps remain; 1: integrity failure.
Does not fetch sources, approve designs, change artwork or clear quality holds.
"""
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return json.loads((BASE / name).read_text())

checks = []
def check(name, condition, details=None):
    checks.append({'check': name, 'passed': bool(condition), 'details': details})

def verify():
    sources = read('sign-sources.json')
    assets = read('sign-asset-manifest.json')
    captions = read('sign-captions.json')
    placement = read('sign-placement-map.json')
    source_list = [x['page'] for x in sources['selected_signs']] + sources['alternative_pages']
    pages = {x['source_id']: x for x in source_list}
    ap = {x['source_id']: x for x in assets['pages']}
    aa = {x['asset_id']: x for x in assets['assets']}
    derived = {x['asset_id']: x for x in assets.get('derived_assets', [])}
    documents = {x['source_id']: x for x in assets.get('official_documents', [])}
    cc = {x['code']: x for x in captions['captions']}
    bb = {x['code']: x for x in placement['asset_caption_bindings']}
    selected = {x['code'] for x in sources['selected_signs']}
    selection_rows = re.findall(r'^\| ([A-Z]+\d+(?:-\d+)?) \| [\d, ]+ \|', (BASE/'sign-selection.md').read_text(), re.M)
    check('selection_263_unique_matching_register', len(selection_rows) == len(set(selection_rows)) == 263 and set(selection_rows) == selected)
    check('page_and_caption_ids_unique_and_complete', len(pages) == len(source_list) == len(ap) == len(assets['pages']) == len(cc) == len(captions['captions']) == 498 and set(pages) == set(ap))
    check('asset_ids_and_paths_unique', len(aa) == len(assets['assets']) == len({a['path'] for a in aa.values()}) == 993)
    source_errors = []
    for p in source_list + [sources['policy']]:
        path = ROOT / p['cache_path']
        if not path.is_file() or digest(path) != p['sha256']:
            source_errors.append(p['url'])
        if urlparse(p['url']).hostname != 'www.transportstyrelsen.se':
            source_errors.append('Non-agency source: ' + p['url'])
    check('498_source_snapshots_and_reuse_evidence_hashes', not source_errors, source_errors)
    policy_id = sources['policy']['id']
    check('all_asset_and_page_reuse_records_resolve', all(a['reuse_policy_id'] == policy_id for a in aa.values()) and all(p['reuse_policy_id'] == policy_id and p['reuse_status'] == 'supported_for_catalogue_artwork_in_context' for p in source_list))
    errors, raster_count, render_count, byte_groups = [], 0, 0, defaultdict(list)
    expected_files = set()
    for a in aa.values():
        path = ROOT / a['path']; expected_files.add(path.resolve())
        try:
            if path.stat().st_size != a['bytes'] or digest(path) != a['sha256']:
                errors.append(a['asset_id'] + ': original size/hash mismatch')
            byte_groups[a['sha256']].append(a['asset_id'])
            if any(urlparse(a[k]).hostname != 'www.transportstyrelsen.se' for k in ['url', 'resolved_url']):
                errors.append(a['asset_id'] + ': unexpected download domain')
            for sid in a['source_ids']:
                p = pages[sid]
                official_urls = {p['main_image']['url']} | {x['url'] for x in p['downloads']}
                if a['url'] not in official_urls:
                    errors.append(a['asset_id'] + ': URL not bound to source page')
            if a['role'] == 'displayed_raster':
                with Image.open(path) as im:
                    if im.size != (a['width_px'], a['height_px']) or getattr(im, 'n_frames', 1) != a['frames']:
                        errors.append(a['asset_id'] + ': dimensions/frames mismatch')
                    for frame in range(getattr(im, 'n_frames', 1)):
                        im.seek(frame); im.load()
                raster_count += 1
            else:
                data = path.read_bytes(); offset = a['postscript_header_offset']
                if not data[offset:].startswith(b'%!PS-Adobe'):
                    errors.append(a['asset_id'] + ': EPS header mismatch')
                box = a['bounding_box_points']
                if not (box[2] > box[0] and box[3] > box[1]):
                    errors.append(a['asset_id'] + ': invalid EPS bounding box')
                r = a['rendered_image']; rp = ROOT/r['path']; expected_files.add(rp.resolve())
                if digest(rp) != r['sha256']:
                    errors.append(a['asset_id'] + ': render hash mismatch')
                with Image.open(rp) as im:
                    im.load()
                    if im.size != (r['width_px'], r['height_px']):
                        errors.append(a['asset_id'] + ': render dimensions mismatch')
                render_count += 1
        except Exception as exc:
            errors.append(a['asset_id'] + ': ' + str(exc))
    check('993_originals_498_rasters_495_renders_integrity', not errors and raster_count == 498 and render_count == 495, errors)
    disk = {p.resolve() for directory in ['originals', 'rendered'] for p in (BASE/'sign-assets'/directory).iterdir() if p.is_file()}
    check('no_missing_or_unmanifested_asset_files', disk == expected_files, [str(p.relative_to(ROOT)) for p in disk ^ expected_files])
    vector_errors = []
    from pypdf import PdfReader
    for doc in documents.values():
        if digest(ROOT/doc['path']) != doc['sha256'] or urlparse(doc['url']).hostname != 'www.transportstyrelsen.se' or doc['reuse_policy_id'] != policy_id:
            vector_errors.append(doc['source_id'])
    for item in derived.values():
        doc = documents.get(item['source_document_id'])
        if not doc or item['source_document_sha256'] != doc['sha256'] or digest(ROOT/item['path']) != item['sha256']:
            vector_errors.append(item['asset_id'] + ': provenance/hash mismatch')
            continue
        pdf = PdfReader(ROOT/item['path'])
        if len(pdf.pages) != 1 or item['minimum_reviewed_width_mm'] < 80 or item['status'] != 'visually_reviewed_at_recorded_size':
            vector_errors.append(item['asset_id'] + ': invalid vector/review record')
    check('official_document_and_vector_extract_integrity', len(derived) == 13 and not vector_errors, vector_errors)
    relation_errors = []
    for sid, p in ap.items():
        code = p['title'].split()[0]; c = cc.get(code)
        if not c or c['official_name_sv'] != pages[sid]['title'].split(' ', 1)[1] or c['sources'][0]['source_id'] != sid:
            relation_errors.append(code + ': name/caption/source mismatch'); continue
        if c['preferred_asset'] != p['preferred_for_layout'] or c['eligible_for_placement'] != bool(p['preferred_for_layout']):
            relation_errors.append(code + ': eligibility mismatch')
        for aid in [p['raster_asset_id']] + p['eps_asset_ids']:
            if aid not in aa or sid not in aa[aid]['source_ids']:
                relation_errors.append(code + ': asset/page mismatch')
        for proof in ['original_proof', 'render_proof']:
            value = p['visual_review'].get(proof)
            if value and not (BASE/value).is_file():
                relation_errors.append(code + ': missing proof')
        preferred = p['preferred_for_layout']
        if preferred:
            source_asset = (aa | derived)[preferred['source_asset_id']]
            choices = [source_asset] + ([source_asset['rendered_image']] if 'rendered_image' in source_asset else [])
            if not any(x['path'] == preferred['path'] and x['sha256'] == preferred['sha256'] and x['max_size_mm_at_300ppi'] == preferred['max_size_mm_at_300ppi'] for x in choices):
                relation_errors.append(code + ': invalid preferred-file binding')
        for ref in c['sources']:
            if urlparse(ref['url']).hostname not in {'www.transportstyrelsen.se', 'www.riksdagen.se'}:
                relation_errors.append(code + ': nonofficial caption source')
            if ref['source_id'] in documents:
                doc = documents[ref['source_id']]
                if ref['url'] != doc['url'] or ref['document_sha256'] != doc['sha256']:
                    relation_errors.append(code + ': poster citation mismatch')
            elif ref['source_id'].startswith('TS-'):
                source = pages.get(ref['source_id'], {})
                if ref['url'] != source.get('url') or ref['html_sha256'] != source.get('sha256'):
                    relation_errors.append(code + ': caption citation mismatch')
    check('page_asset_caption_source_and_proof_relationships', not relation_errors, relation_errors)
    check('all_usable_captions_have_editorial_labels_and_alt', all(c['label_en'] and c['teaching_caption_en'] and 'editorial' in c['translation_status'] and (c['alt_text_en'] if c['eligible_for_placement'] else c['alt_text_en'] is None) for c in cc.values()))
    md = (BASE/'sign-captions.md').read_text()
    check('readable_captions_match_structured_content', all('## '+c['code']+' — '+c['official_name_sv'] in md and c['teaching_caption_en'] in md and (not c['alt_text_en'] or c['alt_text_en'] in md) for c in cc.values()))
    bindings = {'source_register_sha256': digest(BASE/'sign-sources.json') == assets['source_register_sha256']}
    for entry in ['asset_manifest', 'source_register']:
        b = captions[entry]; bindings[entry] = digest(BASE/b['path']) == b['sha256']
    bindings.update({f: digest(BASE/f) == value for f, value in placement['input_bindings'].items()})
    check('upstream_hash_bindings_unchanged', all(bindings.values()), bindings)
    manuscript = (BASE/'manuscript.md').read_text().splitlines()
    locations = [x['location'] for key in ['reference_groups', 'lesson_placements', 'contextual_diagram_briefs', 'image_gaps'] for x in placement[key]]
    anchor_errors = []
    for a in locations:
        i = a['line']-1
        h = next((j for j,l in enumerate(manuscript) if l.lstrip('# ') == a['heading']), None)
        if h is None or i <= h or manuscript[i] != a['exact_quote'] or any(l.startswith('##') for l in manuscript[h+1:i]):
            anchor_errors.append(a['section_id'])
    check('all_passage_anchors_resolve', not anchor_errors, anchor_errors)
    primary = [c for g in placement['reference_groups'] for c in g['primary_codes']]
    check('all_263_selected_have_one_primary_reference', len(primary) == len(set(primary)) == 263 and set(primary) == selected)
    held = {c for c,x in cc.items() if not x['eligible_for_placement']}
    check('current_holds_retained_in_map', held == {x['code'] for x in placement['image_gaps']} == {'A29-17', 'C45-7', 'C45-8', 'C45-9'})
    bad_placements = []
    for b in bb.values():
        c = cc[b['code']]
        if b['caption_id'] != c['caption_id'] or b['preferred_asset'] != c['preferred_asset'] or b['eligibility'] != c['eligible_for_placement']:
            bad_placements.append(b['code'])
    for pl in placement['lesson_placements']:
        for it in pl['items']:
            b = bb[it['code']]
            if (it['status'] == 'ready_for_editorial_placement') != b['eligibility'] or pl['placement_id'] not in b['lesson_placement_ids']:
                bad_placements.append(pl['placement_id']+':'+it['code'])
    check('placement_bindings_and_no_held_image_leakage', not bad_placements, bad_placements)
    check('all_catalogue_dispositions_present', len(placement['catalogue_dispositions']) == len({x['code'] for x in placement['catalogue_dispositions']}) == 498 and {x['code'] for x in placement['catalogue_dispositions']} == set(cc))
    check('reuse_credit_disclaimer_and_pending_design_retained', 'Transportstyrelsen' in (BASE/'sign-reuse.md').read_text() and 'not an official source' in placement['disclaimer'] and all('awaits_step_5' in b['status'] for b in placement['contextual_diagram_briefs']))
    groups = []
    for h,ids in byte_groups.items():
        if len(ids) > 1:
            groups.append({'sha256': h, 'asset_ids': ids, 'page_codes': sorted({ap[sid]['title'].split()[0] for aid in ids for sid in aa[aid]['source_ids']}), 'interpretation': 'Identical bytes do not prove interchangeable sign meaning; retain each source/variant identity and all holds.'})
    required_gaps = [x for x in placement['image_gaps'] if x['is_selected']]
    integrity = all(c['passed'] for c in checks)
    result = {'checked_on': '2026-10-03', 'status': 'integrity_failure' if not integrity else 'review_performed_completion_blocked', 'integrity_checks_passed': integrity, 'package_ready': integrity and not required_gaps, 'scope': 'Local package integrity, provenance, reuse linkage, captions and editorial placement reconciliation. Earlier visual/source review retained; no new full legal review, EPS re-render or PDF approval.', 'summary': {'selected_codes': len(selected), 'source_pages': len(pages), 'original_files': len(aa), 'decoded_rasters': raster_count, 'decoded_eps_renders': render_count, 'usable_catalogue_images': len(cc)-len(held), 'held_catalogue_images': len(held), 'selected_image_blockers': len(required_gaps), 'optional_held_variants_excluded': len(held)-len(required_gaps), 'placement_bindings': len(bb), 'eligible_placement_bindings': sum(x['eligibility'] for x in bb.values()), 'lesson_placements': len(placement['lesson_placements']), 'reference_groups': len(placement['reference_groups'])}, 'checks': checks, 'duplicate_original_byte_groups': groups, 'blocking_gaps': required_gaps, 'input_sha256': {f: digest(BASE/f) for f in ['implementation-plan.md','sign-selection.md','sign-sources.json','sign-reuse.md','sign-asset-manifest.json','sign-captions.json','sign-captions.md','sign-placement-map.json','sign-placement-map.md','manuscript.md']}, 'verifier_sha256': digest(Path(__file__))}
    if result['package_ready']: result['status'] = 'ready_for_next_stage'
    (BASE/'sign-verification-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'summary':result['summary'], 'failed_checks':[x for x in checks if not x['passed']], 'duplicate_groups':len(groups)}, indent=2))
    return 1 if not integrity else 0 if result['package_ready'] else 2

if __name__ == '__main__':
    sys.exit(verify())
