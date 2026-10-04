"""Compile auditable, offline content into common Kotlin code. No runtime generation.
Each situation has one authored answer and three misconception-specific rationales.
Sign identification runs in both directions, with a common concept ID to prevent repetition.
Numerical scenarios state the model and assumptions; no physical guarantee is implied.
"""
from pathlib import Path
import json, re, random, collections, math
ROOT=Path(__file__).resolve().parent.parent
bank=[]; topics=[]
RULE='https://www.transportstyrelsen.se/sv/vagtrafik/trafikregler-och-vagmarken/trafikregler/'
url_by_page={8:'',26:'generella-trafikregler/hogerregeln/',28:'generella-trafikregler/hogerregeln/',30:'generella-trafikregler/hogerregeln/',46:'generella-trafikregler/overgangsstalle/',50:'generella-trafikregler/cykeloverfart/',52:'generella-trafikregler/cykeloverfart/',58:'generella-trafikregler/cirkulationsplats/',70:'generella-trafikregler/stanna-och-parkera/',116:'generella-trafikregler/gagata-cykelgata-och-gangfartsomrade/',117:'generella-trafikregler/gagata-cykelgata-och-gangfartsomrade/',143:'i-fordonet/regler-for-mobilanvandning-och-kommunikationsutrustning/',232:'i-fordonet/baltesregler/',235:'i-fordonet/sa-skyddar-du-barnen---regler-och-tips/',238:'i-fordonet/sa-skyddar-du-barnen---regler-och-tips/',247:'lasta-dra/lastsakring/',252:'lasta-dra/lastsakring/',262:'generella-trafikregler/fordonsbelysning/',264:'generella-trafikregler/fordonsbelysning/'}
def add(id,concept,cat,prompt,answer,why,wrong,page,url='',image='',answerImage='',wrongImages=None):
 options=[{'text':answer,'explanation':why,'image':answerImage}]+[{'text':t,'explanation':r,'image':(wrongImages or ['','',''])[i]} for i,(t,r) in enumerate(wrong)]
 assert len(options)==4 and len({o['text'] for o in options})==4,(id,options)
 bank.append(dict(id=id,concept=concept,category=cat,prompt=prompt,options=options,correct=0,explanation=why,page=page,source=url,image=image))
for i,line in enumerate((ROOT/'content/concepts.tsv').read_text().splitlines()):
 if not line or line.startswith('#'): continue
 fields=line.split('|'); assert len(fields)==9,(i,len(fields))
 cat,page,title,prompt,answer,why,*wrong=fields; page=int(page)
 url=RULE+url_by_page[page] if url_by_page.get(page) else ''
 add(f'situation-{i:03}',f'situation-{i:03}',cat,prompt,answer,why,[w.split('~',1) for w in wrong],page,url)
 topics.append(dict(title=title,category=cat,text=answer+'\n\n'+why+'\n\n'+'\n\n'.join('Remember: '+w.split('~',1)[1] for w in wrong),page=page))
signs=json.loads((ROOT/'content/signs.json').read_text())
translations={'F31a':'Route for long vehicle combinations','P1':'Stop','P2':'Stop','P3':'Stop','P4':'Drive forward','P5':'Reduce speed','P6':'Checkpoint','P7':'Advance notice of checkpoint','P8':'Reduce speed','P9':'Reduce speed','P10':'Follow and stop behind the police vehicle','P11':'Pull over and stop in front of the police vehicle','V1':'Stop','V2':'Drive forward','V3':'Identification mark','Y1':'Red flashing light','Y2':'Sound signal','Y3':'Barrier','Y4':'Level crossing marker'}
for s in signs:
 s['label']=translations.get(s['code'],s['label'])
 if s['code'].startswith(('P','V','Y')): s['page']={'P':356,'V':355,'Y':354}[s['code'][0]]
 if s['code']=='F31a': s['page']=339
eligible=[s for s in signs if re.match('[A-Z]+',s['code'])[0] not in ['SIG','P','Y','V']]
rng=random.Random(2026)
for s in eligible:
 family=re.match('[A-Z]+',s['code'])[0]
 candidates=[x for x in eligible if x['label']!=s['label'] and re.match('[A-Z]+',x['code'])[0]==family]
 candidates+= [x for x in eligible if x['label']!=s['label'] and x not in candidates]
 distractors=[]
 for x in rng.sample(candidates,len(candidates)):
  if x['label'] not in [y['label'] for y in distractors]: distractors.append(x)
  if len(distractors)==3: break
 why=f"The official {s['code']} illustration identifies: {s['label']}. Read any supplementary panel together with the sign."
 add('sign-meaning-'+s['code'],'sign-'+s['code'],'RULES',f"What does the illustrated Swedish sign or marking mean? ({s['code']})",s['label'],why,[(x['label'],f"That is {x['code']} ({x['label']}), a different official illustration. The one shown here is {s['code']}: {s['label']}.") for x in distractors],s['page'],s['url'],s['image'])
 add('sign-recognise-'+s['code'],'sign-'+s['code'],'RULES',f"Which illustration is '{s['label']}' ({s['code']})?",'Illustration '+s['code'],why,[(f"Illustration {x['code']}",f"This is {x['code']}: {x['label']}. It does not represent {s['label']}.") for x in distractors],s['page'],s['url'],answerImage=s['image'],wrongImages=[x['image'] for x in distractors])
def numeric(id,concept,cat,prompt,value,unit,why,page,wrongValues=None):
 vals=wrongValues or [value*.5,value*1.5,value*2]
 fmt=lambda v:f'{v:.1f}'.rstrip('0').rstrip('.')
 correct=fmt(value)+' '+unit
 texts=[]
 for v in vals:
  t=fmt(v)+' '+unit
  if t!=correct and t not in texts: texts.append(t)
 for k in range(1,10):
  if len(texts)>=3: break
  t=fmt(value+k*7)+' '+unit
  if t!=correct and t not in texts: texts.append(t)
 add(id,concept,cat,prompt,correct,why,[(t,f"{t} is not the result of the stated calculation. {why}") for t in texts[:3]],page)
# 36 reaction scenarios; variants share a concept by reaction time to limit repetition in tests.
for speed in range(20,131,10):
 for rt in [0.5,1,1.5]:
  value=speed/3.6*rt
  numeric(f'reaction-{speed}-{rt}',f'reaction-time-{rt}','SAFETY',f'At {speed} km/h, with a reaction time of {rt:g} seconds, approximately how far do you travel before braking? Use speed ÷ 3.6 × time.',value,'m',f'{speed} ÷ 3.6 × {rt:g} = {value:.1f} m. This is reaction distance only; braking distance comes afterwards.',197)
# 30 stopping calculations, explicit textbook estimation rather than promised real braking.
for speed in range(20,111,10):
 for rt in [0.5,1,2]:
  reaction=speed/10*rt*3; brake=(speed/10)**2*.4; value=reaction+brake
  numeric(f'stopping-{speed}-{rt}',f'stopping-estimate-{rt}','SAFETY',f'Use the book’s rough dry-road model: reaction = (speed ÷ 10) × time × 3; braking = (speed ÷ 10)² × 0.4. At {speed} km/h and {rt:g} seconds reaction time, what is the estimated total stopping distance?',value,'m',f'Reaction: {reaction:g} m. Braking: {brake:g} m. Total: {value:g} m. Real stopping distances depend on grip, slope, tyres, brakes and other conditions.',200,[reaction,brake,value*2])
# 20 quadratic braking scenarios.
for base in [5,8,10,12,15,18,20,25,30,35]:
 for factor in [2,3]:
  numeric(f'braking-{base}-{factor}',f'braking-factor-{factor}','SAFETY',f'A car has a braking distance of {base} m. Under the same model and surface conditions, speed becomes {factor} times as high. What is the estimated new braking distance?',base*factor**2,'m',f'Braking distance scales with speed squared: {base} × {factor}² = {base*factor**2} m. Reaction distance is not included.',198,[base*factor,base,base*factor**3])
# 20 time-gap calculations, not universal safe-distance claims.
for speed in [30,40,50,60,70,80,90,100,110,120]:
 for seconds in [3,4]:
  numeric(f'gap-{speed}-{seconds}',f'following-gap-{seconds}','SAFETY',f'At {speed} km/h, how many metres does a {seconds}-second following gap represent? Round to one decimal place.',speed/3.6*seconds,'m',f'{speed} ÷ 3.6 × {seconds} = {speed/3.6*seconds:.1f} m. Poor visibility or grip may require a larger gap.',81)
# 30 parking-disc situations; restrictions are explicitly in force.
for hour in range(8,18):
 for minute in [7,24,43]:
  rounded=((hour*60+minute+29)//30)*30
  time=lambda m:f'{(m//60)%24:02d}:{m%60:02d}'
  add(f'disc-{hour}-{minute}','parking-disc-rounding','RULES',f'You start parking at {hour:02d}:{minute:02d} while a parking-disc requirement is in force. To what time should you set the disc?',time(rounded),f'Set the start time to the next half-hour: {time(rounded)}. Do not set your intended return time.',[(time(rounded-30),'That rounds down instead of up to the next half-hour.'),(time(rounded+30),'That adds an extra half-hour beyond the correct rounded arrival.'),(f'{hour:02d}:{minute:02d}','The disc rule uses the next half-hour rather than the exact arrival minute.')],71)
# 30 load calculations.
for unladen in [1200,1350,1500,1650,1800,1950,2100,2250,2400,2550]:
 for payload in [350,450,550]:
  numeric(f'load-{unladen}-{payload}','registered-payload','VEHICLE',f'A car has registered total weight {unladen+payload} kg and unladen weight {unladen} kg. What is its maximum permitted load according to these figures?',payload,'kg',f'Maximum load = total weight − unladen weight = {unladen+payload} − {unladen} = {payload} kg. Count passengers and luggage within the applicable load allowance.',252,[unladen,unladen+payload,unladen+payload+payload])
# 40 fuel calculations: 20 trip totals and 20 savings scenarios.
for distance in [40,60,80,100,120]:
 for rate in [5,6,7,8]:
  numeric(f'fuel-{distance}-{rate}','fuel-trip-consumption','ENVIRONMENT',f'A car averages {rate} litres per 100 km over a {distance} km journey. Approximately how much fuel does the journey use?',distance*rate/100,'litres',f'{distance} × {rate} ÷ 100 = {distance*rate/100:g} litres. Actual use depends on driving and conditions.',312)
for distance in [100,150,200,250,300]:
 for reduction in [0.5,1,1.5,2]:
  numeric(f'fuel-saving-{distance}-{reduction}','fuel-saving-calculation','ENVIRONMENT',f'Smoother driving reduces measured consumption by {reduction:g} litres per 100 km. Over {distance} km, how much fuel is saved?',distance*reduction/100,'litres',f'{distance} × {reduction:g} ÷ 100 = {distance*reduction/100:g} litres saved. Never compromise safety to achieve a fuel saving.',314)
assert len(bank)>=1000,len(bank)
assert len({q['prompt'] for q in bank})==len(bank)
# Kotlin literals are generated from reviewed source data; split functions avoid JVM method limits.
def ks(s): return json.dumps(s,ensure_ascii=False).replace('$','\\$')
out=ROOT/'composeApp/src/commonMain/kotlin/se/korkort/Bank.kt'
lines=['package se.korkort','', 'val questionBank: List<Question> by lazy { '+ ' + '.join(f'bank{i}()' for i in range(math.ceil(len(bank)/35)))+' }']
for chunk in range(math.ceil(len(bank)/35)):
 lines.append(f'private fun bank{chunk}(): List<Question> = listOf(')
 for q in bank[chunk*35:(chunk+1)*35]:
  opts=', '.join('Option('+ks(o['text'])+', '+ks(o['explanation'])+', '+ks(o['image'])+')' for o in q['options'])
  lines.append('Question('+', '.join([ks(q['id']),ks(q['concept']),'Category.'+q['category'],ks(q['prompt']),'listOf('+opts+')','0',ks(q['explanation']),str(q['page']),ks(q['source']),ks(q['image'])])+'),')
 lines.append(')')
lines.append('val studyTopics = listOf(')
for t in topics: lines.append('Topic('+', '.join([ks(t['title']),'Category.'+t['category'],ks(t['text']),str(t['page'])])+'),')
lines.append(')')
lines.append('data class RoadSign(val code: String, val title: String, val image: String, val url: String)')
lines.append('val roadSigns = listOf(')
for s in signs: lines.append('RoadSign('+', '.join(ks(s[k]) for k in ['code','label','image','url'])+'),')
lines.append(')')
out.write_text('\n'.join(lines)+'\n')
(ROOT/'content/questions.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2))
(ROOT/'content/signs.json').write_text(json.dumps(signs,ensure_ascii=False,indent=2))
summary={'total':len(bank),'categories':dict(collections.Counter(q['category'] for q in bank)),'situationalQuestions':len(topics),'signQuestions':len(eligible)*2,'calculationQuestions':206,'distinctConcepts':len({q['concept'] for q in bank}),'officialSignAssets':len(signs)}
(ROOT/'content/quality-report.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
