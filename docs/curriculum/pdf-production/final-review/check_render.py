"""Render the final book and compare all bodies to the already-rendered component PDFs."""
from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[4];P=R/'docs/curriculum/pdf-production';TMP=R/'tmp/pdfs/h6/rendered';OUT=Path(__file__).resolve().parent
inputs=json.loads((P/'assembly/inputs.json').read_text());before=hashlib.sha256((P/'korkortgo-curriculum-review.pdf').read_bytes()).hexdigest()
# Run only after all PDF authoring/rebuilding has finished.
subprocess.run(['pdftoppm','-scale-to','1000','-png',str(P/'korkortgo-curriculum-review.pdf'),str(TMP/'book/page')],check=True)
assert hashlib.sha256((P/'korkortgo-curriculum-review.pdf').read_bytes()).hexdigest()==before
actual=sorted((TMP/'book').glob('page-*.png'));assert len(actual)==578
fail=[];matches=0
for item in inputs:
 source=sorted((TMP/item['id']).glob('page-*.png'));assert len(source)==item['pages']
 for local,path in enumerate(source):
  idx=item['offset']+local
  if idx==3:continue
  with Image.open(path) as a,Image.open(actual[idx]) as b:
   assert a.size==b.size;box=(0,0,a.width,int(a.height*272/297));diff=ImageChops.difference(a.convert('RGB').crop(box),b.convert('RGB').crop(box))
   if diff.getbbox():fail.append({'page':idx+1,'difference_box':diff.getbbox()})
   else:matches+=1
report={'reviewed_on':'2026-10-14','pdf_sha256':before,'status':'passed' if not fail else 'failed','rendered_pages':578,'source_page_body_pixel_matches':matches,'replaced_contents_page':4,'unexpected_body_differences':fail,'render_scale':1000,'scope':'Fresh final-book render versus current rendered source components. Body/header/artwork retained; assembled contents and folio footer treated separately.'}
(OUT/'render-comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True);assert not fail
