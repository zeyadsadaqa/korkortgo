"""H0: bind unchanged inputs and retrieve exact official source/artwork evidence.

Run with PYTHONPATH=tmp/python. Network retrieval uses curl; --offline verifies
the saved canonical register and evidence hashes without requesting new pages.
This does not change teaching, question content, app assets, or PDFs.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, ROUND_HALF_EVEN
import hashlib
import gzip
import json
from pathlib import Path
import re
import struct
import subprocess
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/curriculum/question-book-review'
REGISTER = BASE / 'remaining-gap-h0-sources.json'
CACHE = ROOT / 'tmp/curriculum/remaining-gap-h0'
EVIDENCE = BASE / 'remaining-gap-source-evidence'
DATE = '2026-10-13'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def binding(path):
    return {'path': path, 'sha256': sha((ROOT / path).read_bytes())}


def retrieve(url, suffix='.html'):
    path = CACHE / (sha(url.encode())[:24] + suffix)
    raw = path.read_bytes() if path.exists() else subprocess.check_output(['curl', '--fail', '--silent', '--show-error',
                                   '--location', '--retry', '2', '--max-time', '45', url])
    path.write_bytes(raw)
    saved = EVIDENCE / (path.name + ('.gz' if suffix == '.html' else ''))
    stored = gzip.compress(raw, mtime=0) if suffix == '.html' else raw
    saved.write_bytes(stored)
    return raw, {'url': url, 'path': str(saved.relative_to(ROOT)), 'sha256': sha(stored), 'content_sha256':sha(raw),
                 'retrieved_on': DATE}


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--offline', action='store_true')
    args.add_argument('--allow-teaching-changes', action='store_true', help='For H1–H5: preserve book/bank/gaps and evidence checks while allowing canonical teaching registers/builders to advance.')
    opts = args.parse_args()
    if opts.offline:
        data = json.loads(REGISTER.read_text())
        frozen_inputs = data['baseline'] if not opts.allow_teaching_changes else {key:data['baseline'][key] for key in ['book','delivery_book','questions','gaps']}
        for item in frozen_inputs.values():
            assert binding(item['path']) == item, item['path']
        def walk(value):
            if isinstance(value, dict):
                if 'path' in value and 'sha256' in value:
                    assert sha((ROOT / value['path']).read_bytes()) == value['sha256'], value['path']
                    if 'content_sha256' in value:
                        raw = (ROOT / value['path']).read_bytes()
                        assert sha(gzip.decompress(raw) if value['path'].endswith('.gz') else raw) == value['content_sha256']
                for v in value.values(): walk(v)
            elif isinstance(value, list):
                for v in value: walk(v)
        walk({key:value for key,value in data.items() if key != 'baseline'})
        ids = [x['question_id'] for x in data['targets']]
        assert len(ids) == len(set(ids)) == 228
        assert len(data['signs']) == 79
        assert {step:sum(t['step']==step for t in data['targets']) for step in ['H1','H2','H3','H4','H5']} == {'H1':56,'H2':72,'H3':30,'H4':30,'H5':40}
        gaps = json.loads((BASE / 'question-coverage-gaps.json').read_text())['questions']
        assert set(ids) == {q['question_id'] for q in gaps}
        assert all(s['page_code_matches'] and s['swedish_name_matches'] and
                   s['question_artwork_matches_official'] for s in data['signs'])
        assert sum(not t.get('exact_arithmetic_matches', True) for t in data['targets']) == 4
        print('PASS: 228 unique targets, 79 exact official sign identities/artwork, all frozen hashes intact; four rounding qualifications retained')
        return

    if REGISTER.exists():
        raise SystemExit('H0 baseline already frozen. Use --offline to verify it; do not overwrite it for later execution steps.')
    from bs4 import BeautifulSoup
    CACHE.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    gaps = json.loads((BASE / 'question-coverage-gaps.json').read_text())
    bank = {q['id']: q for q in json.loads((ROOT / 'content/questions.json').read_text())}
    signs = {s['code']: s for s in json.loads((ROOT / 'content/signs.json').read_text())}
    codes = list(dict.fromkeys(q['sign_code'] for q in gaps['questions'] if q.get('sign_code')))
    assert len(codes) == 79 and len(gaps['questions']) == 228
    targets = []
    for q in gaps['questions']:
        code = q.get('sign_code')
        step = ('H1' if code[0] in 'ACDE' else 'H2' if code[0] in 'FGHJ' else 'H3') if code else ('H4' if q['question_id'].startswith('stopping-') else 'H5')
        item = {'question_id': q['question_id'], 'step': step, 'baseline_status': q['status']}
        bq = bank[q['question_id']]
        assert bq['options'][bq['correct']]['text'] == q['correct_answer']
        if code:
            item['sign_code'] = code
        else:
            parts = q['question_id'].split('-')
            id_v, id_t = map(Decimal, parts[-2:])
            if step == 'H4':
                match = re.search(r'At ([\d.]+) km/h and ([\d.]+) seconds', bq['prompt'])
                v, t = map(Decimal, match.groups())
            elif q['question_id'].startswith('fuel-saving-'):
                match = re.search(r'by ([\d.]+) litres per 100 km\. Over ([\d.]+) km', bq['prompt'])
                t, v = map(Decimal, match.groups())
            else:
                match = re.search(r'averages ([\d.]+) litres per 100 km over a ([\d.]+) km', bq['prompt'])
                t, v = map(Decimal, match.groups())
            assert (v, t) == (id_v, id_t), q['question_id']
            expected = v/10*t*3+(v/10)**2*Decimal('0.4') if step == 'H4' else v*t/100
            keyed = Decimal(re.search(r'[\d.]+', q['correct_answer'])[0])
            item.update(inputs_from_prompt={'speed_kmh' if step=='H4' else 'distance_km':str(v), 'reaction_seconds' if step=='H4' else 'litres_per_100_km':str(t)}, calculated_answer=str(expected), keyed_answer=q['correct_answer'], exact_arithmetic_matches=expected==keyed,
                        arithmetic_matches=expected.quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)==keyed)
            if expected != keyed:
                item['finding'] = 'Exact result differs from key: key uses one-decimal ties-to-even rounding; prompt does not state precision or convention. H5 must disclose/resolve, not silently assert exact equality.'
            assert item['arithmetic_matches'], item
        targets.append(item)
    assert len({x['question_id'] for x in targets}) == 228

    def inspect(code):
        s = signs[code]
        raw, page = retrieve(s['url'])
        soup = BeautifulSoup(raw, 'html.parser')
        main = soup.find('main')
        assert main, code
        c = main.find(id='PageCode')
        name = main.find(id='PageHeader')
        images = [{'url': urljoin(s['url'], i['src'].strip()), 'alt': i.get('alt', '')}
                  for i in main.select('img[src]') if 'vagmarken' in i['src'].lower()]
        downloads = list(dict.fromkeys(urljoin(s['url'], a['href'].strip()) for a in main.select('a[href]') if re.search(r'\.(png|eps|dwg)(?:$|\?)', a['href'], re.I)))
        alternatives = list(dict.fromkeys(urljoin(s['url'], a['href']) for a in main.select('a[href]') if urljoin(s['url'], a['href']).startswith(s['url']) and urljoin(s['url'], a['href']) != s['url'] and a['href'].endswith('/')))
        local = binding('composeApp/src/commonMain/composeResources/files/' + s['image'])
        evidence = []
        # The bank image link resolves to the official preferred variant. Check its
        # exact bytes against both the app asset and a current detail-page PNG.
        bank_raw, bank_image = retrieve(s['imageUrl'], Path(s['image']).suffix)
        for i in images:
            image_raw, ev = retrieve(i['url'], Path(urlparse(i['url']).path).suffix)
            assert image_raw.startswith(b'\x89PNG\r\n\x1a\n') or image_raw.startswith(b'\xff\xd8'), i
            ev.update(alt=i['alt'], format='png' if image_raw.startswith(b'\x89PNG') else 'jpeg', matches_question_image=sha(image_raw)==local['sha256'])
            if ev['format'] == 'png':
                ev.update(width=struct.unpack('>I', image_raw[16:20])[0], height=struct.unpack('>I', image_raw[20:24])[0])
            evidence.append(ev)
        variant_pages = []
        for url in alternatives:
            vr, ve = retrieve(url)
            vm = BeautifulSoup(vr, 'html.parser').find('main')
            ve['text'] = vm.get_text(' ', strip=True)
            ve['image_urls'] = [urljoin(url, i['src'].strip()) for i in vm.select('img[src]') if 'vagmarken' in i['src'].lower()]
            variant_pages.append(ve)
        text = main.get_text(' ', strip=True)
        meaning = ' '.join(p.get_text(' ', strip=True) for p in main.find_all('p') if not p.find_parent(class_='roadsign-mediadata'))
        result = {'code':code, 'official_name_sv':name.get_text(' ', strip=True) if name else '', 'editorial_english':s['label'], 'page':page, 'official_meaning_sv':meaning,
                  'page_code_matches':c is not None and c.get_text(strip=True)==code,
                  'swedish_name_matches':name is not None and name.get_text(' ', strip=True)==s['labelSv'],
                  'detail_images':evidence, 'download_urls':downloads, 'alternative_pages':variant_pages,
                  'question_asset':local, 'bank_image_link':bank_image,
                  'question_artwork_matches_official':sha(bank_raw)==local['sha256'] and any(x['matches_question_image'] for x in evidence),
                  'scope':'Identity/meaning/variant evidence for H1–H3; print quality and caption decisions remain for those steps.'}
        print(code, result['page_code_matches'], result['swedish_name_matches'], result['question_artwork_matches_official'], flush=True)
        return result

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(inspect, codes))
    urls = {
        'reuse':'https://www.transportstyrelsen.se/sv/om-oss/pressrum/pressbilder/',
        'stopping_principles':'https://www.trafikverket.se/resa-och-trafik/trafiksakerhet/sakerhet-pa-vag/hastighetsgranser-pa-vag/stoppstracka/',
        'approximate_model':'https://trafiko.se/faktabank/stoppstracka-reaktionsstracka-bromsstracka',
        'fuel_context':'https://www.transportstyrelsen.se/sv/vagtrafik/miljo/klimat-och-energi/sparsam-korning/'}
    sources = {}
    for key, url in urls.items():
        raw, item = retrieve(url)
        soup = BeautifulSoup(raw, 'html.parser')
        main = soup.find('main') or soup
        if key == 'reuse':
            item['text'] = next(p.get_text(' ', strip=True) for p in main.find_all('p') if 'Du kan ladda ner filer av vägmärken' in p.get_text())
        else:
            item['text'] = main.get_text(' ', strip=True)
        sources[key] = item
    sources['reuse']['scope'] = 'Road-sign-file paragraph only; use in proper context. Existing catalogue-family interpretation retained. No licence for press photographs or unrelated artwork.'
    sources['stopping_principles']['scope'] = 'Reaction plus braking; speed and conditions affect distance. Published example distances are different from the exercise shortcut; do not use as provenance for its constants.'
    sources['approximate_model']['scope'] = 'Commercial teaching provenance for one-second reaction shortcut and 0.4 braking shortcut with good brakes/tyres and dry asphalt. Variable time is editorial proportional arithmetic. No other claims on this page adopted.'
    sources['fuel_context']['scope'] = 'Agency economical-driving context only. Journey-use/savings formulas are editorial unit arithmetic; supplied reductions are exercise assumptions, not guaranteed technique benefits.'
    frozen = {'book': binding('docs/curriculum/pdf-production/korkortgo-curriculum-review.pdf'),
              'delivery_book':binding('output/pdf/korkortgo-curriculum-review.pdf'),
              'questions':binding('content/questions.json'),
              'gaps':binding('docs/curriculum/question-book-review/question-coverage-gaps.json')}
    for path in ['content/signs.json', 'docs/curriculum/manuscript.md', 'docs/curriculum/manuscript-sources.json',
                 'docs/curriculum/sign-sources.json', 'docs/curriculum/sign-asset-manifest.json', 'docs/curriculum/sign-captions.json',
                 'docs/curriculum/sign-placement-map.json', 'docs/curriculum/pdf-production/reference/reference-source.md',
                 'docs/curriculum/pdf-production/reference/build_reference.py', 'docs/curriculum/pdf-production/chapters/M03/build_chapter.py',
                 'docs/curriculum/pdf-production/chapters/M09/build_chapter.py', 'docs/curriculum/pdf-production/assembly/build_book.py',
                 'docs/curriculum/question-book-review/g-step-changes.json']:
        frozen[path] = binding(path)
    assert frozen['book']['sha256']==gaps['metadata']['book_sha256']
    assert frozen['questions']['sha256']==gaps['metadata']['questions_sha256']
    assert frozen['book']['sha256']==frozen['delivery_book']['sha256']
    data = {'schema_version':'1.0', 'verified_on':DATE, 'baseline':frozen, 'targets':targets, 'signs':results, 'scoped_sources':sources,
            'validation':{'target_count':len(targets), 'sign_count':len(results), 'step_counts':{step:sum(t['step']==step for t in targets) for step in ['H1','H2','H3','H4','H5']},
                          'official_detail_image_count':sum(len(s['detail_images']) for s in results), 'alternative_detail_page_count':sum(len(s['alternative_pages']) for s in results),
                          'calculation_exact_matches':sum(t.get('exact_arithmetic_matches', False) for t in targets), 'calculation_rounding_qualifications':sum(not t.get('exact_arithmetic_matches', True) for t in targets)},
            'findings':{'rounding': [t['question_id'] for t in targets if 'finding' in t],
                        'caption_precision':['A32','C12','C8','C9','C10','C11','C13','C14','C29','C34','D8','D9','D12','E23','F28','F31','F32','F33','H22','H25','M17','M28','S7','S11','S13','T23','T25'],
                        'white_symbol_contrast':['S5','S6','S7','S11','S13'], 'bank_changes':False, 'teaching_changes':False}}
    REGISTER.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    print('Saved', REGISTER.relative_to(ROOT))


if __name__ == '__main__':
    main()
