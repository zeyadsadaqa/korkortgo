import json,hashlib
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
b=Path('/Users/zeyad/Desktop/korkort/docs/curriculum/app-migration/verification-evidence/11D1'); result=json.loads((b/'result.json').read_text()); rows=result['rows']; assert len(rows)==2464
seen=set(); out=[];samples=[]
for r in rows:
 key=f"{r['question_id']}-390-{str(r['dark']).lower()}-{r['font_scale']:.1f}";assert key not in seen;seen.add(key)
 paths=[b/'captures'/(key+s+'.png') for s in ['-pre-answer','-pending']]
 images=[Image.open(p).convert('RGB') for p in paths];assert all(im.size==(390,844) for im in images)
 diff=ImageChops.difference(*images);box=diff.getbbox();assert box,key
 slots=['Enlarge_question_image'] if r['image_occurrences']==1 else ['Enlarge_option_'+c+'_image' for c in 'ABCD']
 zoom=[b/'captures'/(key+'-'+s+'-zoom.png') for s in slots]
 for p in zoom:
  with Image.open(p) as im: assert im.size==(390,844)
 out.append({'case':key,'revision':r['revision'],'pending_change_bounds':box,'zoom_captures':len(zoom),'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+zoom}})
 if r['question_id'] in ['sign-recognise-S6','sign-meaning-C18','sign-meaning-M8','sign-recognise-X9']: samples.append((key,images[1]))
(b/'capture-audit.json').write_text(json.dumps({'cases':len(out),'captures':sum(2+x['zoom_captures'] for x in out),'rows':out},indent=2)+'\n')
canvas=Image.new('RGB',(390*4,884*4),'#ddd');d=ImageDraw.Draw(canvas)
for i,(key,im) in enumerate(samples):x=i%4*390;y=i//4*884;canvas.paste(im,(x,y+40));d.text((x+2,y+5),key,fill='black')
canvas.save(b/'visual-sample.png');print('Audited',len(out),'cases; sample',len(samples))
