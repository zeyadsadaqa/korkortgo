"""Compare freshly compiled observations to frozen 7E, independent of Kotlin helpers."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
frozen=read(ROOT/'docs/curriculum/app-migration/link-and-progress-map.json')
actual=read(HERE/'navigation-transition-results.json')
edges=read(HERE/'reading-edge-results.json')['edges']
order=frozen['reading_order'];checks=[]
def check(name,condition):
 checks.append({'check':name,'pass':bool(condition)})
check('all eight states',len(actual['states'])==len(frozen['navigation_routes'])==8)
check('both complete state transition matrices',len(actual['transitions'])==128)
check('60 nodes in frozen exact order',[e['id'] for e in edges]==order and len(order)==60)
for i,e in enumerate(edges):
 check(e['id']+' previous',e['previous']==(order[i-1] if i else None))
 check(e['id']+' next',e['next']==(order[i+1] if i+1<len(order) else None))
for row in actual['validated_returns']:
 c=row['context'];r=row['restored']
 check(c['origin']['content_id']+'/'+c['position']['block_id'],c['position']==r['position'] and c['focus_id']==r['focus_id'])
entries=[]
evidence=[
 ('Navigation.kt','Transitions10HTest; 128 transitions'),
 ('Navigation.kt','10G1 all 1000 accepted question routes; unknown question denial'),
 ('LearningLibrary.kt','fresh routeRetainsLibrarySearchExpansionAndAccessibleFieldState'),
 ('LessonReader.kt','frozen 60-node / 120 neighbour comparison'),
 ('CurriculumApp.kt','10H3 fresh accepted production-owner review/source journeys'),
 ('LearningSources.kt','10G3 exact callback URLs; fresh 10H1 source return; OS dispatch pending10K'),
 ('LearningRoute.kt','10G1 exact343 aliases and10G3 gaps; fresh reading-sign return probe'),
 ('Assessment.kt','10F1 accepted selection /10F2 snapshot;10H3 fresh accepted snapshots'),
 ('TransientQuizState.kt','10H2 missing context and guards;10H3 accepted review snapshot'),
 ('ExactAssetImage.kt','10B14 manifest;10D shared assets; target delivery pending10K'),
 ('App.kt','10B14 deterministic generation; production accepted bank fixed; no old compiler execution'),
 ('App.kt','shared App() entry; native startup remains pending10K; no new parser/storage')]
for i,(e,(file,proof)) in enumerate(zip(frozen['entry_point_rules'],evidence),1):
 entries.append({'id':f'10H-ENTRY-{i:02}','entry':e['entry'],'rule':e['rule'],'implementation':file,'evidence':proof,'status':'audited_shared_or_inherited_scope','native_proof':False})
result={'status':'pass_compiled_and_frozen_scope' if all(c['pass'] for c in checks) else 'fail','checks':checks,'totals':{'checks':len(checks),'states':8,'transitions':128,'nodes':60,'edges':118,'null_boundaries':2,'valid_return_contexts':len(actual['validated_returns']),'entry_points':len(entries)},'entry_points':entries,'limits':'Entry points include content/generation/asset/platform contracts, not twelve public deep links. Referenced prior evidence is inherited; fresh shared/UI and failures are separate. Native focus/lifecycle/modal closure remains10K.'}
result['gate']='T07 open: DEF-10H-001 and fresh10K'
result['shared_sign_return']=read(HERE/'reading-sign-return-observations.json')
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'totals':result['totals']}))
assert all(c['pass'] for c in checks)
