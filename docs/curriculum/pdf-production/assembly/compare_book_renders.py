"""Compare every assembled page body with its component at the same render scale.

The contents page is intentionally replaced and footers are intentionally
renumbered. All other pixels above the footer region must match exactly.
"""
import hashlib
import json
from pathlib import Path
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageChops
ROOT = Path(__file__).resolve().parents[4]
HERE = ROOT / 'docs/curriculum/pdf-production'
OUT = HERE / 'assembly'
TMP = ROOT / 'tmp/pdfs/h6/rendered'
SCALE = 1000

def render(item):
    folder = TMP / item['id']
    folder.mkdir(parents=True, exist_ok=True)
    for previous in folder.glob('page-*.png'):
        previous.unlink()
    subprocess.run(['pdftoppm', '-scale-to', str(SCALE), '-png',
                    str(HERE / item['path']), str(folder / 'page')],
                   check=True, capture_output=True)
    pages = sorted(folder.glob('page-*.png'))
    print('Rendered', item['id'], len(pages), 'pages', flush=True)
    return item['id'], pages

def main():
    inputs = json.loads((OUT / 'inputs.json').read_text())
    book = {'id':'book', 'path':'korkortgo-curriculum-review.pdf'}
    with ThreadPoolExecutor(max_workers=3) as pool:
        rendered = dict(pool.map(render, [book] + inputs))
    actual = rendered['book']
    assert len(actual) == sum(i['pages'] for i in inputs)
    failures = []
    matched = 0
    for item in inputs:
        assert len(rendered[item['id']]) == item['pages']
        for local, source in enumerate(rendered[item['id']]):
            index = item['offset'] + local
            if index == 3:
                continue
            with Image.open(source) as a, Image.open(actual[index]) as b:
                assert a.size == b.size
                # Exclude bottom 25 mm (A4 height 297 mm); retain header and body.
                box = (0, 0, a.width, int(a.height * 272 / 297))
                diff = ImageChops.difference(a.convert('RGB').crop(box), b.convert('RGB').crop(box))
                if diff.getbbox():
                    failures.append({'page':index+1, 'part':item['id'], 'local_page':local+1, 'difference_box':diff.getbbox()})
                else:
                    matched += 1
    result = {'status':'passed' if not failures else 'failed', 'rendered_pages':len(actual),
              'source_page_body_pixel_matches':matched, 'replaced_contents_page':4,
              'unexpected_body_differences':failures, 'render_scale':SCALE,
              'pdf_sha256':hashlib.sha256((HERE / book['path']).read_bytes()).hexdigest(),
              'scope':'Every source page body including original artwork/header; contents and replaced footer excluded. Human review recorded in remaining-gap-execution-plan.md.'}
    (OUT / 'render-comparison.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'unexpected_body_differences'}, indent=2), flush=True)
    assert not failures, failures[:10]

if __name__ == '__main__':
    main()
