"""Compare Compose/Skia output with independent direct PDF rendering; no delivery acceptance."""
import hashlib,json
from pathlib import Path
import pymupdf as pdf
from PIL import Image,ImageChops,ImageStat,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
records=[];sheet=Image.new('RGB',(1200,6*230),'#eee');pen=ImageDraw.Draw(sheet)
for index,r in enumerate(json.loads((HERE.parent/'9L10/vector-decoding.json').read_text())['records']):
    page=pdf.open(ROOT/r['source']['path'])[0];pix=page.get_pixmap(matrix=pdf.Matrix(4,4))
    reference=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    rendered=ROOT/f"composeApp/build/verification/9L10/{r['code'].lower()}-compose-4x.png"
    actual=Image.open(rendered).convert('RGB');assert actual.size==reference.size
    mean=sum(ImageStat.Stat(ImageChops.difference(actual,reference)).mean)/3
    ref_mask=reference.convert('L').point(lambda v:255 if v<220 else 0)
    got_mask=actual.convert('L').point(lambda v:255 if v<220 else 0)
    reference_pixels=ref_mask.histogram()[255]
    actual_pixels=got_mask.histogram()[255]
    assert mean<2.0,(r['code'],mean)
    # Different engines antialias subpixel strokes differently. Check location independently
    # of intensity, and retain intensity differences for the required legibility review.
    ref_near=ref_mask.filter(ImageFilter.MaxFilter(3));got_near=got_mask.filter(ImageFilter.MaxFilter(3))
    missing_ref=ImageChops.subtract(ref_mask,got_near).histogram()[255]
    missing_got=ImageChops.subtract(got_mask,ref_near).histogram()[255]
    assert missing_ref/reference_pixels<.005 and missing_got/actual_pixels<.005,(r['code'],missing_ref,missing_got)
    def ink(im):return sum((255-v)*n for v,n in enumerate(im.convert('L').histogram()))
    records.append({'code':r['code'],'source':r['source'],'compose_render_sha256':hashlib.sha256(rendered.read_bytes()).hexdigest(),'dimensions':list(actual.size),'mean_absolute_rgb_difference_0_255':mean,'dark_pixel_count_ratio':actual_pixels/reference_pixels,'integrated_ink_ratio':ink(actual)/ink(reference),'source_pixels_without_compose_neighbour':missing_ref,'compose_pixels_without_source_neighbour':missing_got,'result':'passed decoder-fidelity check; not platform delivery acceptance'})
    x=(index%3)*400;y=(index//3)*230;pen.text((x+8,y+4),r['code']+' · PDF left / Compose right',fill='black')
    for col,img in enumerate([reference,actual]):
        img.thumbnail((185,195));sheet.paste(img,(x+col*200+5,y+25))
sheet.save(HERE/'vector-comparison-sheet.png')
(HERE/'vector-fidelity.json').write_text(json.dumps({'decoder':'PyMuPDF '+pdf.VersionBind,'renderer':'Compose/Skia desktop','records':records,'acceptance_scope':'Decoder geometry only, with antialiasing differences recorded; no intended-size legibility, device/reader acceptance or scoring activation.'},indent=2)+'\n')
print('18 vector comparisons passed. Maximum mean pixel difference:',max(r['mean_absolute_rgb_difference_0_255'] for r in records))
