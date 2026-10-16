"""Create analytical contact sheets from retained Android window captures; never edit artwork."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
codes=[f'S{n}' for n in range(1,14)]+['T1','T2','T6','T8','T22','X8']
metadata=json.loads((HERE.parent/'9L10/vector-decoding.json').read_text())['records']
sizes={r['code']:r['page_dimensions_pt'] for r in metadata}
a=json.loads((ROOT/'content/curriculum.json').read_text());x=next(a for a in a['assets'] if a['id']=='official/X8');sizes['X8']=Image.open(ROOT/x['bundled']['path']).size
out=HERE/'android-review';out.mkdir(exist_ok=True)
for scale in [1.0,1.6]:
    probe=Image.open(HERE/'android'/f'S1-dark-{scale}.png').convert('RGB');w,h=probe.size
    bands=[];start=None
    for y in range(h):
        pixels=[probe.getpixel((x,y)) for x in range(40,w-40,8)]
        white=sum(min(p)>235 for p in pixels)/len(pixels)>.8
        if white and start is None:start=y
        if (not white or y==h-1) and start is not None:
            end=y if not white else y+1
            bands.append((start,end))
            start=None
    merged=[]
    for top,bottom in bands:
        if merged and top-merged[-1][1]<=12:merged[-1]=(merged[-1][0],bottom)
        else:merged.append((top,bottom))
    bands=[b for b in merged if b[1]-b[0]>180]
    assert len(bands)==2,(scale,bands)
    for dark in [False,True]:
        mode='dark' if dark else 'light'
        for part in range(math.ceil(len(codes)/6)):
            group=codes[part*6:part*6+6];sheet=Image.new('RGB',(1140,1040),'#eee');pen=ImageDraw.Draw(sheet)
            for offset,code in enumerate(group):
                im=Image.open(HERE/'android'/f'{code}-{mode}-{scale}.png').convert('RGB');x=(offset%3)*380;y=(offset//3)*520
                pen.text((x+12,y+8),f'{code} / {mode} / text {scale}',fill='black')
                sw,sh=sizes[code]
                for slot,(top,bottom) in enumerate(bands):
                    height=bottom-top;width=min(w-80,height*sw/sh);left=(w-width)/2
                    actual=im.crop((int(left),top,int(left+width),bottom))
                    actual.thumbnail((350,250 if slot==0 else 170))
                    sheet.paste(actual,(x+(380-actual.width)//2,y+35 if slot==0 else y+315))
                    pen.text((x+12,y+290 if slot==0 else y+495),('180dp stem' if slot==0 else '105dp option'),fill='black')
            sheet.save(out/f'{mode}-{scale}-part-{part+1}.png')
print('16 contact sheets created from the 76 actual Android captures.')
