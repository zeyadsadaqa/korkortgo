"""Arrange actual shared-render captures at 1:1 pixels; no resampling or artwork modification."""
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
codes=['S5','S6','S7','S11','S12','S13','T1','T2','T6','T8','T22','X8'];out=HERE/'comparison-sheets';out.mkdir(exist_ok=True)
for i in range(0,len(codes),2):
 sheet=Image.new('RGB',(780,1160),'#eeeeee');draw=ImageDraw.Draw(sheet)
 for col,code in enumerate(codes[i:i+2]):
  x=col*390;draw.text((x+8,8),code+' | shared frame 354x236 at 1:1 pixels',fill='black')
  sheet.paste(Image.open(HERE/f'comparisons/{code}-frame.png'),(x+18,32));draw.text((x+8,280),'Shared viewer 390x844; 150%, cropped viewport',fill='black')
  sheet.paste(Image.open(HERE/f'comparisons/{code}-viewer150.png'),(x,308))
 sheet.save(out/f'pair-{i//2+1:02}.png')
