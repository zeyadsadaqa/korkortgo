"""Compare independently prepared expected sets with fresh compiled/UI observations."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());checks=[]
def check(label,test):checks.append({'check':label,'pass':bool(test)})
frozen=read(ROOT/'docs/curriculum/app-migration/link-and-progress-map.json');expected=read(HERE/'search-oracle.json');actual=read(HERE/'compiled-search-observations.json');returned=read(HERE/'search-return-observations.json')
check('all288orderedcases',len(actual['cases'])==len(expected['queries'])==288)
for e,a in zip(expected['queries'],actual['cases']):
 check(e['id'],e['id']==a['id'] and e['category']==a['category'] and e['query']==a['query'] and e['expected_lesson_ids']==a['model']==a['ui'] and a['status']=='pass')
check('all40tagrecords',set(actual['tags'])==set(expected['tags']) and len(actual['tags'])==40)
for id,tags in expected['tags'].items():check(id+' frozen tags',set(actual['tags'][id])=={t.lower() for t in tags})
for category in frozen['category_routes']:
 row=next(r for r in actual['cases'] if r['category']==category['category_id'] and r['query']=='')
 check(category['category_id']+' frozen ordered membership',row['model']==row['ui']==category['lesson_ids'])
 check(category['category_id']+' displayedtitle',actual['category_titles'][category['category_id']]==category['display_title'])
check('clear only owninput',actual['clear_actions_preserve_other_input'])
check('allchips keepquery',actual['chips_preserve_query'])
check('emptystate neverautoopens',actual['empty_never_opens_content'])
check('combinedroundtrip querycategoryexpansion',returned['status']=='pass' and returned['filter']=={'query':'Your route into driving','category':'personal'} and set(returned['expanded'])=={'M01','M07'})
result={'task':'10I2','status':'pass_compiled_and_shared_scope' if all(c['pass'] for c in checks) else 'fail','identity':actual['identity'],'totals':{'search_cases':288,'category_filters':5,'tag_records':40,'checks':len(checks)},'checks':checks,'input':'search-oracle.json / frozen7E plus authored teaching search fields','observations':['compiled-search-observations.json','search-return-observations.json'],'empty_state_recovery':'No matching lessons. plus existing Clear search/Clear filters controls; no unrelated lesson opens. Supporting/front-matter/appendix links remain available separately under filters.','limits':['Semantic button/set-text actions and state-backed render checks, not native pointer/IME traversal.','Library search covers title/objectives/body fields, not hidden answers, asset metadata or arbitrary IDs; no full-text search feature was invented.']}
(HERE/'library-search-filter-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ['status','totals']}))
for c in checks:
 if not c['pass']:print('FAILED',c['check'])
assert all(c['pass'] for c in checks)
