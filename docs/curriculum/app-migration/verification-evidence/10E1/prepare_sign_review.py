"""Prepare exact assigned review packets/analytical artwork sheets. No correctness inferred from receipt parity."""
import gzip,hashlib,html,json,re,subprocess,sys,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());BASE=Path(__file__).resolve().parent.parent;TMP=Path('/tmp/korkort-10e-review');TMP.mkdir(exist_ok=True)
read=lambda p:json.loads((ROOT/p).read_text());sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
q={x['key']['question_id']:x for x in read('content/accepted-assessment-questions.json')['questions']};assets={x['id']:x for x in read('content/curriculum.json')['assets']};captions={x['code']:x for x in read('docs/curriculum/sign-captions.json')['captions'] if x['is_selected']};batch=read('docs/curriculum/app-migration/verification-evidence/10A3/question-batches.json');source=read('docs/curriculum/sign-sources.json');pages={}
def walk(v):
 if isinstance(v,dict):
  if 'url' in v and 'cache_path' in v:pages[v['url']]=v
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(source)
def source_content(c):
 for s in c['sources']:
  name=s.get('evidence_path') or pages.get(s['url'],{}).get('cache_path')
  if not name or not (ROOT/name).exists():continue
  b=gzip.decompress((ROOT/name).read_bytes()) if name.endswith('.gz') else (ROOT/name).read_bytes()
  expected=s.get('html_sha256') or pages.get(s['url'],{}).get('sha256');actual=hashlib.sha256(b).hexdigest()
  if expected and expected!=actual:continue
  t=b.decode('utf-8',errors='replace');i=t.find('<h1');t=t[i:] if i>=0 else t;t=t.split('roadsign-files-header')[0];t=re.sub(r'<script\b.*?</script>','',t,flags=re.S|re.I);t=re.sub('<[^>]*>',' ',t);t=' '.join(html.unescape(t).split())
  return {'url':s['url'],'file':name,'sha256':actual,'retrieved_on':s.get('retrieved_on') or pages.get(s['url'],{}).get('retrieved_on'),'locator':'Official h1 and explanation preceding artwork downloads','content':t}
 return {'url':c['sources'][0]['url'],'file':None,'sha256':c['sources'][0].get('html_sha256'),'retrieved_on':c['sources'][0].get('retrieved_on'),'locator':'Dated approved source/caption record; raw page unavailable locally','content':None}
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14)
task=sys.argv[1];members=next((r['question_ids'] for r in batch['sign_rewrite_batches'] if r['owner']==task),None)
if task=='10E14':members=[qid for r in batch['replacement_pairs'] for qid in r['question_ids']]
assert members
codes=list(dict.fromkeys(q[x]['feedback']['target_sign_code'] for x in members));packet=[]
for code in codes:
 c=captions[code];meaning=q['sign-meaning-'+code];recognise=q['sign-recognise-'+code];src=source_content(c)
 packet.append({'code':code,'question_ids':['sign-meaning-'+code,'sign-recognise-'+code],'label':c['label_en'],'official_sv':c['official_name_sv'],'caption':c['teaching_caption_en'],'variant':c['variant_description_en'],'neutral':meaning['image']['neutral_description']['text'],'options':[(f['sign_code'],f['english_label']) for f in meaning['feedback']['option_feedback']],'official_source':src})
(TMP/(task+'-packet.json')).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
# 25 target assets normally produce one review board; no AI-generated art and no app/device delivery claim.
for offset in range(0,len(codes),25):
 subset=codes[offset:offset+25];board=Image.new('RGB',(1300,330*((len(subset)+4)//5)),'#e8e8e8');draw=ImageDraw.Draw(board)
 for i,code in enumerate(subset):
  row=packet[codes.index(code)];asset=assets[q['sign-meaning-'+code]['image']['asset_id']];p=ROOT/asset['original']['path'];assert sha(asset['original']['path'])==asset['original']['sha256']
  if p.suffix.lower()=='.pdf':
   image_path=TMP/(code+'-exact.png')
   if not image_path.exists():subprocess.run(['pdftoppm','-singlefile','-scale-to','900','-png',str(p),str(image_path.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  else:image_path=p
  im=Image.open(image_path).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg=bg.convert('RGB');bg.thumbnail((246,182));x=(i%5)*260;y=(i//5)*330
  draw.text((x+5,y+3),code+' | '+row['label'][:25],font=font,fill='black');board.paste(bg,(x+(260-bg.width)//2,y+25+(182-bg.height)//2))
  for k,line in enumerate(textwrap.wrap(row['neutral'],width=34)):draw.text((x+5,y+210+15*k),line,font=font,fill='black')
 board.save(TMP/f'{task}-assets-{offset//25+1}.png')
print(json.dumps({'task':task,'IDs':len(members),'target_assets':len(codes),'raw_primary_pages':sum(x['official_source']['content'] is not None for x in packet),'packet':str(TMP/(task+'-packet.json'))}))
for r in packet:
 print(r['code']+' | '+r['label']+' | '+r['caption']+' | VAR '+(r['variant'] or '(no separate variant text)'))
 print('  neutral: '+r['neutral'])
 print('  choices: '+', '.join(c+' '+l for c,l in r['options']))
 print('  SV: '+(r['official_source']['content'] or '[raw unavailable; dated caption evidence]')[:650])
