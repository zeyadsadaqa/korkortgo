"""Read-only source artwork rendering for 9D description inspection (requires Pillow/Poppler)."""
import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[5]; out=root/'docs/curriculum/app-migration/implementation-evidence/9D2/visual-review';out.mkdir(exist_ok=True)
r=json.loads((root/'docs/curriculum/app-migration/question-review/asset-review.json').read_text())['records']
selected=[x for x in r if x['approved_path'].endswith('.pdf') or x['code'] in ['T17','X8','X10','M12','M19','H23','F2','F27']]
canvas=Image.new('RGB',(1600, ((len(selected)+3)//4)*260),'#dddddd'); draw=ImageDraw.Draw(canvas)
for i,x in enumerate(selected):
 p=root/x['approved_path'];target=out/x['code']
 if p.suffix=='.pdf':
  subprocess.run(['pdftoppm','-singlefile','-scale-to','700','-png',str(p),str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);p=target.with_suffix('.png')
 im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im); im=bg.convert('RGB');im.thumbnail((380,225));left=(i%4)*400;top=(i//4)*260
 canvas.paste(im,(left+(400-im.width)//2,top+25+(225-im.height)//2));draw.text((left+8,top+5),x['code'],fill='black')
canvas.save(out/'vector-and-detail-review.png')
