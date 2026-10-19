"""Reconcile exact question revisions with exhaustive shared and representative native proof.

Native coverage is stated explicitly: all 38 replacements at four settings, plus
raster regression and native reader/route evidence. It is not 616 native recordings.
"""
import argparse,hashlib,json
from pathlib import Path
from compile_curriculum import canonical
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14'
FAINT={'S5','S6','S7','S11','S12','S13','T1','T2','T6','T8','T22','X8'}
def read(path):return json.loads(path.read_text())
def identity(path):return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def rows_by_context(rows):
 result={}
 for row in rows:
  key=(row['question_id'],row['dark'],float(row['font_scale']))
  assert key not in result,key
  result[key]=row
 return result
def build():
 questions=read(ROOT/'content/assessment-questions.json')['questions'];held=[q for q in questions if q['acceptance']['eligibility']=='held']
 assert len(held)==616
 shared=read(BASE/'shared-question-delivery.json');shared_rows=rows_by_context(shared['rows'])
 android=read(BASE/'android-question-matrix.json');ios=read(BASE/'ios-question-matrix.json')
 assert android['complete'] and ios['complete']
 native={p:rows_by_context(proof['rows']) for p,proof in [('android',android),('ios_simulator',ios)]}
 replacements={q['key']['question_id'] for q in held if q['key']['revision']=='replacement-candidate-r2'}
 expected={(qid,dark,scale) for qid in replacements for dark in [False,True] for scale in [1.0,1.6]}
 for platform,index in native.items():
  assert set(index)==expected,platform
  assert sum(r['image_zoom_returns'] for r in index.values())==380
 for name in ['normal-light','normal-dark','large-light','large-dark']:
  summary=read(BASE/(name+'-test-summary.json'))
  assert summary['result']=='Passed' and summary['passedTests']==1 and summary['failedTests']==0,name
 raster=read(BASE/'android-large-raster-matrix.json');assert raster['complete'] and len(raster['rows'])==8
 assert {r['question_id'] for r in raster['rows']}=={'sign-meaning-M17a','sign-recognise-M17a'}
 inventory=read(BASE/'resource-inventory.json');assert inventory['status']=='passed' and inventory['asset_count']==484
 packaged={a['asset_id']:a for a in inventory['assets']}
 visual=read(BASE/'asset-legibility-review.json');assert visual['status']=='passed'
 assert {a['code'] for a in visual['assets']}==FAINT and all(a['status']=='passed' for a in visual['assets'])
 for item in visual['inputs']:assert identity(ROOT/item['path'])==item,item['path']
 candidate=read(ROOT/'content/assessment-questions.json')['questions']
 assets={a['id']:a for a in read(ROOT/'content/curriculum.json')['assets']}
 used=sorted({image['asset_id'] for q in held for image in [q['image'],*[o['image'] for o in q['options']]] if image})
 asset_rows=[]
 for asset_id in used:
  a=assets[asset_id];assert a['original']['sha256']==a['bundled']['sha256']
  assert identity(ROOT/a['bundled']['path'])==a['bundled']
  assert packaged[asset_id]['asset_sha256']==a['bundled']['sha256']
  assert set(packaged[asset_id]['packaged_byte_parity'])=={'android','desktop','ios_simulator','wasm_js'}
  asset_rows.append({'asset_id':asset_id,'asset_sha256':a['bundled']['sha256'],'status':'passed','platforms':['android','desktop','ios_simulator','wasm_js'],
   'coverage':'Exact resource byte parity on four platforms; exhaustive shared per-question resource/semantics/zoom proof; native decoder and accessible-viewer representative coverage. Twelve contour sources additionally have exact full-question native matrices and recorded visual decisions.',
   'legibility_review': 'asset-legibility-review.json' if asset_id.removeprefix('official/') in FAINT else 'Existing exact-artwork review retained; current shared/native rendering and packaging regression checks pass.'})
 rows=[]
 for q in held:
  qid=q['key']['question_id'];images=list(filter(None,[q['image']]+[o['image'] for o in q['options']]))
  for dark in [False,True]:
   for scale in [1.0,1.6]:
    row=shared_rows[(qid,dark,scale)];assert row['revision']==q['key']['revision'] and row['zoom_returns']==len(images)
    if qid in replacements:
     for platform,index in native.items():
      row=index[(qid,dark,scale)];assert row['revision']==q['key']['revision'] and row['image_zoom_returns']==len(images)
  rows.append({'question_id':qid,'revision':q['key']['revision'],'status':'passed','assessment_sha256':hashlib.sha256(canonical({k:v for k,v in q.items() if k!='acceptance'})).hexdigest(),
   'shared_question_runs':4,'native_context_evidence':'Exact question at all four settings on Android and iOS simulator.' if qid in replacements else 'Representative native shared renderer/PNG/selection/focus coverage; exact per-revision four-setting shared run and exact platform package resource parity. No claim of a separate full native recording for this revision.',
   'native_question_runs_per_platform':4 if qid in replacements else 0,
   'route_evidence':'native-reader-routes checkpoint and passing CurriculumAppFlowTest production-owner guard/results/review/teaching/source/reset flows with existing accepted fixtures, before activation.',
   'prior_holds_resolved':q['acceptance']['open_holds']})
 assert len(shared_rows)==2464
 inputs=[ROOT/'content/assessment-questions.json',BASE/'shared-question-delivery.json',BASE/'android-question-matrix.json',BASE/'ios-question-matrix.json',BASE/'android-large-raster-matrix.json',BASE/'resource-inventory.json',BASE/'asset-legibility-review.json',BASE/'tests-preintegration/TEST-se.korkort.CurriculumAppFlowTest.xml',ROOT/'content/delivery-targets.json']
 inputs += [ROOT/'composeApp/src/commonMain/kotlin/se/korkort'/n for n in ['AssessmentCard.kt','ExactAssetImage.kt','AssessmentWithImageViewer.kt','AccessibleImageViewer.kt','ImageViewport.kt','RootModalHost.kt']]
 inputs += [ROOT/'composeApp/src/androidMain/kotlin/se/korkort/ExactRaster.kt',ROOT/'composeApp/src/wasmJsMain/kotlin/se/korkort/RootModalPlatform.kt',ROOT/'tools/review_question_delivery_9j.py']
 return {'date':'2026-10-19','status':'passed','ios_scope':'simulator','acceptance_basis':'The binding 9E hold asks for supported-platform exact-artwork delivery and representative accessibility navigation. Shared coverage is exhaustive per revision; native full-question coverage is the 38 high-risk replacements, not a fabricated 616-question native replay. Production activation remains after accepted-package 9M3 verification.',
  'scope_limits':['This accepts delivery under the approved full-width/neutral-description/accessible-zoom presentation, not new artwork or source-currency claims.','Physical iOS was explicitly excluded by the user; no ios_device pass is recorded.','Broader integrated platform/release verification remains the planned 9O/10 work.'],
  'inputs':[identity(p) for p in inputs],'totals':{'held_revisions_resolved':616,'shared_question_runs':2464,'native_question_runs_per_platform':152,'native_zoom_returns_per_platform':380,'faint_affected_questions':24,'replacement_records_ready_for_activation':38},'assets':asset_rows,'questions':rows}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args();text=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';out=BASE/'delivery-acceptance.json'
 if args.check:assert out.read_text()==text
 else:out.write_text(text)
 print('9J: 616 exact-revision delivery holds reconciled; native/shared coverage and simulator scope recorded explicitly.')
