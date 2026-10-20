"""Prepare modality-specific requirements; listening, semantics and platform modality are separate outcomes."""
import json
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());HERE=Path(__file__).resolve().parent;BASE=HERE.parent
read=lambda p:json.loads(p.read_text())
scope=read(BASE/'10A2/scope-matrix.json');runtime=read(BASE/'10A3/runtime-matrix.json')
states={
 'pre_answer_projection':'Inspect visible text and native accessibility nodes before selection and confirmation; neutral descriptions only, no metadata/answer/key leak.',
 'selection_confirmation':'Traverse prompt/options in order; select without confirming; identify selection visibly and accessibly; confirm exactly the selected authored ID.',
 'feedback_modes':'Immediate mode reveals only after confirmation; end mode saves without revealing until finish. Check disabled choices, polite announcement and deliberate focus.',
 'viewer_modal_exclusion':'Open each supplied slot. Inspect native/browser modal tree, hide background, trap keyboard/assistive focus and ensure labels remain neutral.',
 'viewer_controls_return':'Use actual keyboard/touch/accessibility controls for fit,150%,pan,Reset,Close; preserve selected authored ID/revision/order and return to exact trigger.',
 'large_text_geometry':'Use all four 10A3 settings, actual viewport/insets/density and approved >=220dp equal option frames; scroll to every required control without shrinking text.'}
rows=[]
for target in ['android','desktop','ios_simulator','wasm_js']:
 method=next(x for x in scope['rows'] if x['target']==target and x['dimension']=='screen_reader_listening')
 for state,expected in states.items():rows.append({'case_id':f'10D4-{target}-{state}','target':target,'interaction':state,'expected':expected,'required_question_contexts':'../10D2/artwork-platform-cases.json: target cases plus eight 10A3 representative IDs at four settings','status':'not_run_pending_10K','shared_support':'../10D3/shared-artwork-observations.json and shared-accessibility-observations.json (when executed); no native modal or speech inference','method':'Actual target keyboard/native or browser accessibility-node observations, with separate real TalkBack traversal on Android.'})
 rows.append({'case_id':f'10D4-{target}-listening','target':target,'interaction':'screen_reader_listening','scope_requirement':method['requirement'],'method':method['method'],'status':'not_run_pending_10K' if method['requirement']=='required' else 'excluded_by_existing_scope','expected_evidence':'Actual listening/traversal observation if required; accessibility nodes alone do not prove speech.'})
(HERE/'accessibility-platform-cases.json').write_text(json.dumps({'task':'10D4','scope':'../10A2/scope-matrix.json','cases':rows,'source_representatives':runtime['representative_native_questions'],'settings':runtime['settings'],'physical_iOS':'excluded_by_existing_user_simulator_policy'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'required_platform_interactions':24,'required_listening_targets':['android'],'no_listening_pass_claimed':True}))
