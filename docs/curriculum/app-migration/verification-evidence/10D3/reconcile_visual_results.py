"""Reconcile fresh shared observations and pixel evidence; do not convert them into 10K/native/visual passes."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent;BASE=HERE.parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,d):(HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
source=read(HERE/'shared-artwork-observations.json');observed={r['case_id']:r for r in source['rows']};matrix=read(BASE/'10D2/artwork-platform-cases.json');contexts=[];image_count=0
assert len(observed)==2464
for c in matrix['contexts']:
 r=observed.get(c['case_id']);status='not_run_pending_10K' if r is None else 'shared_behaviour_pass_visual_pending'
 if r:
  assert c['target']=='desktop' and c['revision']==r['revision'] and r['shared_runtime_status']=='pass'
  assert len(r['images'])==len(c['zoom_slots']);image_count+=len(r['images'])
  assert all(x['frame']['height_px']>=220 and x['resource_loaded'] for x in r['images'])
  if len(r['images'])==4:assert len({(x['frame']['width_px'],x['frame']['height_px']) for x in r['images']})==1
 contexts.append({'case_id':c['case_id'],'target':c['target'],'question_id':c['question_id'],'revision':c['revision'],'setting':c['setting'],'status':status,'shared_observation':r,'visual_signoff':'pending_fresh_10K_and_review'})
# Exact visible counterexample: selected B is fully shown in the inspected S5 light-100 viewport.
pre=HERE/'captures/sign-recognise-S5-light-100-pre.png';post=HERE/'captures/sign-recognise-S5-light-100-pending.png';a=Image.open(pre).convert('RGB');b=Image.open(post).convert('RGB');bbox=ImageChops.difference(a,b).getbbox();assert bbox is None
case=next(c for c in contexts if c['case_id']=='T03-ART-desktop-sign-recognise-S5-light-100');assert case['shared_observation']['selected_option_id']==case['shared_observation']['displayed_option_ids'][1];case['visual_signoff']='fail_no_visible_pending_selection';case['defect_id']='DEF-10D-001'
pixel={'case_id':case['case_id'],'expected':'Persistent neutral visible selection indication on selected option B; selected state is not correctness feedback.','observed':'Selected B is visible in the shared 390x844 light-100 capture, yet full pre/pending images are pixel-identical; semantic selection and later confirmation still work.','pre_capture':str(pre.relative_to(HERE)),'pending_capture':str(post.relative_to(HERE)),'pre_file_sha256':sha(pre),'pending_file_sha256':sha(post),'pixel_changed_bounds':bbox,'selected_authored_option_id':case['shared_observation']['selected_option_id'],'supporting_code':'composeApp/src/commonMain/kotlin/se/korkort/AssessmentCard.kt:47–53: selected passed to selectable semantics, no persistent selection rendering in Surface/card.','defect_id':'DEF-10D-001','limits':'An accessible selected property and enabling Confirm do not supply a visible selected-choice indicator. Other cases require affected-surface retests; not all were independently pixel-reviewed.'}
dump('selection-visual-finding.json',pixel)
out=HERE/'reviewed-contact-sheets';out.mkdir(exist_ok=True);sheet=Image.new('RGB',(780,880),'white');draw=ImageDraw.Draw(sheet);draw.text((8,8),'S5 light-100: pre-answer',fill='black');draw.text((398,8),'S5 light-100: B pending; no visible change',fill='black');sheet.paste(a,(0,32));sheet.paste(b,(390,32));sheet.save(out/'S5-visible-selection-failure.png')
# Capture manifest pins the exact observations even where final platform visual review is pending.
prior_index=read(HERE/'capture-index.json') if (HERE/'capture-index.json').exists() else {'captures':[]}
prior_paths={r['path']:r.get('stored_path',r['path']) for r in prior_index['captures']}
logical_paths=sorted({p for r in source['rows'] for p in r['captures']} | {p for r in source['rows'] for image in r['images'] for p in image['faint_captures']})
captures=[]
for logical in logical_paths:
 stored=logical if (HERE/logical).exists() else prior_paths[logical]
 captures.append({'path':logical,'stored_path':stored,'sha256':sha(HERE/stored)})
dump('capture-index.json',{'viewport':{'width_logical_px':390,'height_logical_px':844,'density':1,'insets':'headless scene, no OS insets'},'captures':captures,'scope':'Pre/pending viewport captures for all 38 replacements at four settings; fit/150% views for each faint slot. These do not stitch or certify unseen question portions.'})
assert len(captures)==496,len(captures)
dump('visual-delivery-results.json',{'task':'10D3','status':'open_visual_defect_and_pending_10K','manifest_sha256':sha(ROOT/'content/accepted-content-manifest.json'),'counts':{'prepared_artwork_contexts':len(contexts),'shared_behaviour_passes':len(observed),'image_zoom_returns':image_count,'fresh_native_browser_contexts':0,'native_browser_contexts_pending_10K':len(contexts)-len(observed),'pre_pending_replacement_captures':304,'faint_fit_zoom_captures':192,'visual_counterexamples_reviewed':1,'final_visual_passes':0},'capture_resolution':'capture-index.json maps each original logical capture path to its retained stored_path; original hashes/case identities are preserved.','contexts':contexts,'findings':[pixel],'remaining_requirements':['Resolve DEF-10D-001 in bounded 10L workflow and retest visible/accessible selected state across supported targets.','Reconcile fresh 10K platform captures, executable hashes, actual native insets/density, approved frame/zoom and assistive method.','Review complete question/scroll/zoom contexts; captures and semantics do not independently certify all fine strokes or copy.','Keep 390x844 as replay size, not an approved minimum; 320 diagnostic/narrow cases remain in 10J2/10K.','The eight representative native question contexts at four settings per target are supplementary to the 456 replacement contexts.'],'no_new_design_or_artwork_change':True})
print(json.dumps({'shared_contexts':len(observed),'zoom_returns':image_count,'captures':len(captures),'visual_defect':pixel['defect_id'],'native_browser_pending':len(contexts)-len(observed)}))
