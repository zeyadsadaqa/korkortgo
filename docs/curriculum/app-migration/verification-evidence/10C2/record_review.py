import json,hashlib,re
from pathlib import Path
root=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists()); base=root/'docs/curriculum/app-migration/verification-evidence'; out=base/'10C2'
def read(p):return json.loads(Path(p).read_text())
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
claims=read(out/'risk-selection.json')['claims'];fetches=read(out/'primary-fetch-observations.json');byurl={r['url']:r for r in fetches}
# Curated observations from actual primary-page content, not HTTP success alone.
notes=[
('Eligibility / supervised practice','First B: permit, residence/study, 18, risk training and both tests; EEA entitlement needs its own route. Car practice 16, light goods/light trailer 17½; approved supervisor is legally driver.', '2026-07-31'),
('Övningsköra / new rules','Introduction course ended 1 August 2026. Permit, vehicle-specific age, ID and learner-specific private-supervisor approval remain; school practice is distinguished.',None),
('Riskutbildning bil','Both car parts precede tests; validity ends on licence issue or after five years. Motorcycle training does not substitute.', '2026-08-07'),
('TSFS 2026:47 chapter 5 §1 and transition','One year for passes from 19 August 2026; earlier passes retain earlier provisions. This is a dated amendment, not retroactive permission.', '2026-04-13'),
('Theory-test validity','Agency test guide distinguishes earlier four-month results from passes under the August change. Use actual individual result/extension records.',None),
('TSFS 2011:20 chapters 4–5 §§1–3','Journey planning, stress/fatigue, personal/social influences and self-assessment support the briefs. Their proposed rubrics are editorial, not an official exam threshold.', None),
('3 kap. 1 §','Unsafe driving due to illness, fatigue or other impairment is prohibited.',None),
('3 kap. 14 §','Speed follows conditions, control and stopping within visible foreseeable space.',None),
('3 kap. 2 §','Following distance must avoid rear collision when the vehicle ahead slows or stops.',None),
('3 kap. 22 §','Entering traffic yields to vehicles already circulating.',None),
('3 kap. 32, 36 §§','Overtaking requires safety, sufficient clear path and safe return; a generic bend is insufficient scene information.',None),
('3 kap. 50, 53(1) §§','Exit must avoid danger; stopping is prohibited on or within ten metres before a crossing. A future scene must supply distance and direction.',None),
('2 kap. 2–3 §§','Traffic instructions override general rules; police directions have priority. Steady signals override signed stop/yield.',None),
('Vinterdäck: light vehicles / studded tyres','Winter tyres required 1 December–31 March in winter conditions, normally at least 3 mm for light vehicles. Studded window 1 October–15 April with winter-condition exception. Vehicle/trailer and local restrictions remain separate.', '2026-05-27'),
('Ordinary inspection schedule ≤3500 kg','First inspection within 36 months, next within 24, then within 14; month of actual inspection matters. Check the vehicle record; special categories are outside this claim.', '2025-10-08'),
('Child restraints / exceptions','Under 135 cm needs suitable child restraint as the ordinary rule. Limited transport exceptions are not a general permission; follow vehicle/restraint instructions.', '2025-04-17'),
('V60 Twin Engine 18w46 / Temporary Spare','Exact original model-specific URL could not be inspected: direct HTTP 403 and web cache miss. Do not renew the handbook claim or silently substitute a different model.',None),
('MQ4 2022 maintenance / coolant warning','Kia handbook warns against opening hot coolant cap and unexpected fan operation. Model-specific manufacturer caution, not public-authority or universal maintenance procedure.',None),
('NIOSH nurse training / microsleeps','Involuntary brief sleep can occur without awareness; physiological US guidance does not establish Swedish legal thresholds.', '2020-03-31'),
('VTI report 980 (2020), sections 4.2–4.3','Section 4.2 discusses stopping-distance factors; 4.3 explains shared braking/steering friction and ABS within available grip. Research context, not law or a guaranteed distance for every vehicle/road.', '2020'),
('Rough reaction and braking calculations','Commercial page gives speed shortcut ×3 and dry-asphalt braking factor 0.4 with assumptions. Neither is Swedish law or a universal physical guarantee.',None),
('reaction-20-0.5: supplied values','Independently recomputed (20/3.6)×0.5 = 2.777… m, rounded 2.8 m. Editorial exercise; VTI context is not agency endorsement of its chosen values.',None),
('1177 acute advice / first aid index','Swedish public-health service index provides first-aid topic navigation. This check does not freshly certify any treatment procedure or create clinical instructions.',None),
('Municipal energy-advice service','Gagnef identifies Swedish municipal, free impartial advice funded by Energimyndigheten. Domestic public service, not foreign government guidance.',None),
('Tvätta bilen rätt / Göteborgs Stad','Municipal page advises wash facilities that collect/treat wastewater. Swedish public-service environmental advice; do not turn a local warning into an unconditional national offence claim.',None),
('Sparsam körning / service ownership','Page footer identifies Energimyndigheten with Swedish municipalities; fuel-saving advice remains scoped guidance, not foreign law.',None),
('Fakta om ledarhundar / MFD','Swedish agency describes its guide-dog service and working-dog caution. Domestic authority guidance, not foreign public authority.', '2026-04-30'),
('KRAV Grundvärden VGU, 2024:148, v1.0, title/imprint','PDF explicitly names Trafikverket as publisher; Swedish infrastructure requirements. DiVA host does not make it foreign authority, research or general road-user legislation.', '2024-11-01'),
('Kia MQ4/2022 Swedish handbook identity','Official Kia owner-manual page is manufacturer material for a specific model/edition. Foreign-public-authority classification is incorrect.',None)
]
assert len(notes)==len(claims)==29
for i,(c,(locator,note,date)) in enumerate(zip(claims,notes),1):
 f=byurl[c['url']];c.update(status='blocked_unreachable' if i==17 else 'defect_confirmed' if i>=24 else 'supported_with_scope',checked_on='2026-10-20',locator=locator,observation=note,source_date=date,fetch_observation=f,production_source_dates_changed=False)
 if f['status']!='fetched_for_content_review' and i!=17:c['fallback_review']={'mechanism':'web primary-page open','url':c['url'],'date':'2026-10-20','note':'Content inspected through web tool; direct TLS/access failure retained. No certificate bypass.'}
 if i==14:c['supplemental_primary_review']={'url':'https://www.transportstyrelsen.se/sv/vagtrafik/fordon/fordonsregler/dack/vinterdack/','date':'2026-10-20','heading':'Personbilar och lätta lastbilar; Dubbade vinterdäck','mechanism':'web primary-page follow of original hub Vinterdäck link'}
 if i==17:c['indexed_primary_evidence']={'url':c['url'],'search_date':'2026-10-20','index_crawled':'3 weeks before search, per web result','source_updated_on':'2020-03-19','observation':'Exact original Volvo model/edition indexed article supports temporary use, 80 km/h and manufacturer pressure; no numerical distance supplied. Direct current open remains unavailable, so this is corroboration of earlier evidence, not fresh live-page verification.'}
 if i==22:c['independent_arithmetic']={'speed_kmh':20,'time_seconds':0.5,'metres':20/3.6*0.5,'rounded_1dp':round(20/3.6*0.5,1),'numeric_check':round(20/3.6*0.5,1)==2.8}
q=read(root/'content/accepted-assessment-questions.json')['questions'];briefs=[]
for bid,lid,primary,related,checks in [('9N1','M01-L01',0,0,list(range(1,7))),('9N2','M07-L04',0,1,[6,7,8]),('9N3','M10-L03',0,0,[6,7,8,9,10,11,12])]:
 pr=[x['key']['question_id'] for x in q if lid == x['relationship']['primary_lesson_id']]
 rel=[x['key']['question_id'] for x in q if lid in x['relationship']['related_lesson_ids']]
 briefs.append({'brief_id':bid,'lesson_id':lid,'primary_question_ids':pr,'related_question_ids':rel,'expected_counts':{'primary':primary,'related':related},'coverage_matches':len(pr)==primary and len(rel)==related,'claim_cases':['10C2-CLAIM-'+str(n).zfill(2) for n in checks],'status':'pass' if len(pr)==primary and len(rel)==related else 'fail','authoring_boundary':'Unscored future brief only; no IDs, quotas, scored content or approval changed. Supplied unknowns and concrete scenario evidence remain required.'})
assert all(b['coverage_matches'] for b in briefs), briefs
dump(out/'checked-claims.json',{'task':'10C2','checked_on':'2026-10-20','selection':'risk-selection.json','counts':{'selected':29,'supported_with_scope':22,'defect_confirmed':6,'blocked_unreachable':1},'claims':claims,'briefs':briefs,'unchecked_claims':'Original dates/limits retained; no blanket currency claim.','status':'executed_with_findings'})
