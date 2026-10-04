from pathlib import Path
import json,hashlib,io
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import RectangleObject
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
folder=Path('docs/curriculum/sign-assets/official-poster')
boxes={'S1':[197.6,1883.7,270.3,1928.6],'S2':[283.5,1883.6,355.6,1928],'S3':[367.7,1883.7,440.4,1928.5],'S4':[452.5,1883.7,524.8,1928.3],'S8':[791.6,1882.8,863.8,1927.4],'S9':[877,1882,950,1927],'S10':[962.1,1873.7,1034.7,1934.8],'S12':[1131,1881.9,1203.9,1926.8],'T1':[1304.3,1869.2,1364.8,1945.5],'T2':[1388.1,1893.3,1458.2,1921.2],'T6':[1719.4,1877.5,1795.4,1934],'T8':[114.9,2015.8,181.6,2050.2],'T22':[1307,2018,1365,2046]}
# Refine T22 bounds using its complete outer frame.
import pdfplumber
with pdfplumber.open(folder/'sveriges-vagmarken-2021.pdf') as d:
 cand=[c for c in d.pages[0].curves+d.pages[0].rects if 1300<c['x0']<1340 and 1995<c['top']<2070 and c['x1']-c['x0']>30 and c['bottom']-c['top']>15]
 if cand:
  boxes['T22']=[min(c['x0'] for c in cand)-1,min(c['top'] for c in cand)-1,max(c['x1'] for c in cand)+1,max(c['bottom'] for c in cand)+1]
rows=[];proof=PdfWriter();source=folder/'sveriges-vagmarken-2021.pdf'
for code,(x0,top,x1,bottom) in boxes.items():
 src=PdfReader(source).pages[0]; h=float(src.mediabox.height); y0=h-bottom;y1=h-top
 src.cropbox=RectangleObject([x0,y0,x1,y1]);src.mediabox=RectangleObject([x0,y0,x1,y1])
 target_w=(110 if code in ['S12','T1','T2','T8','T22'] else 80)*mm
 scale=target_w/(x1-x0); target_h=(bottom-top)*scale
 w=PdfWriter();p=w.add_blank_page(width=target_w,height=target_h)
 p.merge_transformed_page(src,Transformation((scale,0,0,scale,-x0*scale,-y0*scale)))
 name=code+'-official-vector.pdf';w.remove_text();w.write(folder/name)
 buff=io.BytesIO();c=canvas.Canvas(buff,pagesize=(210*mm,297*mm));c.setFont('Helvetica-Bold',14);c.drawString(20*mm,277*mm,code+' - official poster vector proof');c.setFont('Helvetica',10);c.drawString(20*mm,268*mm,f'Width {target_w/mm:.0f} mm. Exact artwork; no redrawing or recolouring.');c.drawString(20*mm,258*mm,'Technical asset review, not a proposed book page.');c.save();buff.seek(0)
 page=PdfReader(buff).pages[0];page.merge_translated_page(w.pages[0],20*mm,240*mm-target_h);proof.add_page(page)
 rows.append({'code':code,'path':str(folder/name),'sha256':hashlib.sha256((folder/name).read_bytes()).hexdigest(),'poster_box_top_origin_points':[x0,top,x1,bottom],'review_width_mm':target_w/mm,'status':'pending_visual_review'})
proof.write(folder/'vector-legibility-proof.pdf')
(folder/'vector-extraction.json').write_text(json.dumps({'date':'2026-10-03','source_url':'https://www.transportstyrelsen.se/globalassets/global/publikationer-och-rapporter/vag/vagmarken/ts_poster70x100_2021-10-01_webb.pdf','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'pypdf crop and affine scale; outside poster text removed; sign vector paths and colours unchanged','assets':rows},indent=2)+'\n')
print('Saved 13 exact vector extracts and 13-page proof.')
