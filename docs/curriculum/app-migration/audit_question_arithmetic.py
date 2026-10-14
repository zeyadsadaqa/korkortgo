"""Independently parse all calculation prompts and recalculate with Decimal."""
from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_EVEN
import json,re,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
p=ROOT/'content/questions.json';bank=json.loads(p.read_text());rows=[]
for q in bank:
 text=q['prompt'];family=q['id'].split('-')[0]
 if family in ['situation','sign']:continue
 current=q['options'][q['correct']]['text']
 if family=='reaction':
  speed,delay=re.search(r'At (\d+) km/h, with a reaction time of ([\d.]+) seconds',text).groups();exact=D(speed)/D('3.6')*D(delay);method='constant-speed conversion; supplied delay; braking excluded';inputs={'speed_kmh':speed,'reaction_seconds':delay}
 elif family=='stopping':
  speed,delay=re.search(r'At (\d+) km/h and ([\d.]+) seconds reaction time',text).groups();v=D(speed)/10;exact=v*D(delay)*3+v*v*D('.4');method='supplied rough exercise: reaction plus braking, not actual stopping prediction';inputs={'speed_kmh':speed,'reaction_seconds':delay}
 elif family=='braking':
  distance,factor=re.search(r'braking distance of (\d+) m.*speed becomes (\d+) times',text).groups();exact=D(distance)*D(factor)**2;method='constant-model squared-speed scaling; braking only';inputs={'initial_braking_metres':distance,'speed_factor':factor}
 elif family=='gap':
  speed,seconds=re.search(r'At (\d+) km/h.*a (\d+)-second following gap',text).groups();exact=D(speed)/D('3.6')*D(seconds);method='constant-speed distance for supplied time; not universal safe gap';inputs={'speed_kmh':speed,'gap_seconds':seconds}
 elif family=='disc':
  hour,minute=re.search(r'parking at (\d\d):(\d\d)',text).groups();minutes=int(hour)*60+int(minute);rounded=((minutes+29)//30)*30;expected=f'{(rounded//60)%24:02}:{rounded%60:02}';assert current==expected
  assert sum(o['text']==expected for o in q['options'])==1
  rows.append({'question_id':q['id'],'input_time':f'{hour}:{minute}','expected_key':expected,'current_key':current,'status':'pass','scope':'disc restriction explicitly in force; not an exact-boundary arrival example'});continue
 elif family=='load':
  total,ready=re.search(r'total weight (\d+) kg and unladen weight (\d+) kg',text).groups();exact=D(total)-D(ready);method='totalvikt minus defined tjänstevikt; English ready-weight convention needs prompt definition';inputs={'total_kg':total,'ready_kg':ready}
 elif q['id'].startswith('fuel-saving-'):
  rate,distance=re.search(r'by ([\d.]+) litres per 100 km\. Over (\d+) km',text).groups();exact=D(distance)*D(rate)/100;method='supplied measured rate reduction × distance / 100; no guaranteed eco-driving saving';inputs={'distance_km':distance,'reduction_l_per_100km':rate}
 else:
  rate,distance=re.search(r'averages (\d+) litres per 100 km over a (\d+) km',text).groups();exact=D(distance)*D(rate)/100;method='supplied journey-average rate × distance / 100';inputs={'distance_km':distance,'rate_l_per_100km':rate}
 values=[D(re.match(r'([\d.]+)',o['text'])[1]) for o in q['options']];expected=exact.quantize(D('.1'),rounding=ROUND_HALF_EVEN);assert values[q['correct']]==expected,(q['id'],exact,current)
 assert sum(v==expected for v in values)==1
 qualified=q['id'].startswith('fuel-saving-') and exact!=expected
 rows.append({'question_id':q['id'],'inputs':inputs,'method':method,'exact_result':str(exact),'one_decimal_half_even':str(expected),'current_key':current,'distinct_numeric_options':len(set(values))==4,'status':'qualified rounding convention; rewrite exact-answer task' if qualified else 'pass','exact_working_not_equal_to_key':exact!=expected})
assert len(rows)==206
out={'checked_on':'2026-10-14','questions_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'Independent regex parsing of displayed prompt inputs; Decimal arithmetic, half-even display check and all four option values inspected. Question IDs are not used to obtain numeric inputs.','total':206,'passed_without_fuel_qualification':sum(r['status']=='pass' for r in rows),'fuel_rounding_qualified':[r['question_id'] for r in rows if r['status'].startswith('qualified')],'incorrect_keys_under_printed_model':0,'records':rows}
(HERE/'question-review/arithmetic.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['records','method']})
