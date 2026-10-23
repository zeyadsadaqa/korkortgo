import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
b=Path(__file__).resolve().parent;rows=json.loads((b/'captures/rows.json').read_text());questions=json.loads((b.parent/'11B2/current-replacements.json').read_text());expected={(q['id'],q['revision'],t,s) for q in questions for t in ['light','dark'] for s in ['1','1.6']};assert len(rows)==152 and {(r['question_id'],r['revision'],r['theme'],r['font_scale']) for r in rows}==expected
out=[];samples=[]
for r in rows:
 key=r['question_id']+'-'+r['theme']+'-'+r['font_scale'];assert r['capture_position']
 paths=[b/'captures'/(key+s+'.png') for s in ['-pre-answer','-pending']];ims=[Image.open(p).convert('RGB') for p in paths];assert all(im.size==(390,844) for im in ims);box=ImageChops.difference(*ims).getbbox();assert box,key
 q=next(q for q in questions if q['id']==r['question_id']);slots=['Enlarge_question_image'] if q['stem'] else ['Enlarge_option_'+c+'_image' for c in 'ABCD'];zoom=[b/'captures'/(key+'-'+s+'-zoom.png') for s in slots];assert len(zoom)==r['image_zoom_returns']
 for p in zoom:
  with Image.open(p) as im: assert im.size==(390,844)
 out.append({'case':key,'revision':r['revision'],'pending_change_bounds':box,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+zoom}})
 if r['question_id'] in ['sign-recognise-S6','sign-recognise-S11','sign-meaning-T22','sign-meaning-X8']:samples.append((key,ims[1]))
keyboard=json.loads((b/'keyboard-results.json').read_text())
for r in keyboard:
 key=r['theme']+'-'+r['font_scale'];box=ImageChops.difference(Image.open(b/('keyboard-'+key+'-zoom.png')).convert('RGB'),Image.open(b/('keyboard-'+key+'-pan.png')).convert('RGB')).getbbox();assert box,key;r['observed_pan_change_bounds']=box
(b/'keyboard-results.json').write_text(json.dumps(keyboard,indent=2)+'\n');(b/'capture-audit.json').write_text(json.dumps({'cases':152,'capture_count':sum(2+r['image_zoom_returns'] for r in rows),'rows':out},indent=2)+'\n')
canvas=Image.new('RGB',(1560,3536),'#ddd');d=ImageDraw.Draw(canvas)
for i,(key,im) in enumerate(samples):x=i%4*390;y=i//4*884;canvas.paste(im,(x,y+40));d.text((x+2,y+5),key,fill='black')
canvas.save(b/'visual-sample.png');print('PASS152; all selected captures change; four keyboard pans change')
