"""Review all 9F candidates and record actual evidence without accepting missing delivery proof.
No question, official artwork, caption, source record or prior evidence is rewritten.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE=Path('docs/curriculum/app-migration/implementation-evidence')
CODES=[f'S{n}' for n in range(1,14)]+['T1','T2','T6','T8','T22','X8']
FAINT={'S5','S6','S7','S11','S12','S13','T1','T2','T6','T8','T22','X8'}
def read(p):return json.loads((ROOT/p).read_text())
def identity(p):return {'path':str(p),'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}
def dump(value):return json.dumps(value,ensure_ascii=False,indent=2)+'\n'
def build():
    curriculum=read(Path('content/curriculum.json'));actions=read(Path('docs/curriculum/app-migration/question-actions.json'))['questions'];live=read(Path('content/questions.json'))
    proposals={r['question_id']:r for r in actions};by_id={r['id']:r for r in live}
    descriptions={}
    for n in range(3,16):
        path=BASE/f'9D{n}/description-acceptance.json'
        for index,r in enumerate(read(path)['questions']):descriptions[r['question_id']]=(path,index,r)
    captures=read(BASE/'9F/android/complete.json')['captures']
    assert len(captures)==76 and all(r['exact_assets_loaded'] and r['pixel_copy_result']==0 for r in captures)
    files={};summary=[]
    for index,code in enumerate(CODES,1):
        step=f'9F{index}';folder=BASE/step;asset=next(a for a in curriculum['assets'] if a['id']=='official/'+code)
        assert identity(Path(asset['original']['path']))==asset['original']
        assert identity(Path(asset['bundled']['path']))==asset['bundled']
        pair=[f'sign-{direction}-{code}' for direction in ['meaning','recognise']];content=[];uses=[]
        for qid in pair:
            action=proposals[qid];p=action['proposed_changes'];path,loc,d=descriptions[qid]
            assert action['disposition']=='replace' and by_id[qid]==action['original'] and d['description_result']=='accepted'
            assert len(p['options'])==len({o['option_id'] for o in p['options']})==4
            assert sum(o['is_correct'] for o in p['options'])==1
            assert p['prompt']==d['prompt']
            for option,reviewed in zip(p['options'],d['options']):
                assert option['option_id']==reviewed['option_id']
                assert (option['meaning_option_text'] or '')==reviewed['pre_answer_text']
                assert option['code_metadata_after_reveal']==reviewed['post_answer_code']
                assert option['post_answer_label']==reviewed['post_answer_label']
                assert option['is_correct']==reviewed['is_correct_after_reveal_only']
                assert option['post_answer_explanation'] and option['official_sources']
            content.append({'question_id':qid,'content_review':'exact approved proposal, options, key, labels and feedback checked; application deferred','neutral_description_review':{'file':identity(path),'locator':f'json:/questions/{loc}'},'original_record_unchanged':True,'proposed_changes':p})
        assert content[0]['proposed_changes']['proposed_option_codes']==content[1]['proposed_changes']['proposed_option_codes']
        # Exhaustive displayed-image uses; meaning-option briefs are not images in the UI.
        for action in actions:
            p=action.get('proposed_changes') or {};slots=[('stem',p.get('question_image_asset'))]
            if action['question_id'].startswith('sign-recognise-'):
                slots += [(o['option_id'],(o.get('visual_description_brief') or {}).get('exact_asset')) for o in p.get('options',[])]
            for slot,exact in slots:
                if exact and exact['sha256']==asset['original']['sha256']:uses.append({'question_id':action['question_id'],'slot':slot})
        assert len(uses)==2
        android=[]
        for row in captures:
            if row['code']==code:
                android.append({**row,'screenshot':identity(BASE/'9F/android'/row['screenshot'])})
        assert len(android)==4
        simulator=BASE/'9F/ios-simulator'/f'{code}.png';web=BASE/'9F/wasm'/f'{code}.png'
        blockers=['Representative platform screen-reader and complete per-question zoom/return/focus acceptance has not been signed off.']
        if code in FAINT:blockers.append('Smallest 105dp preview retains visibly faint outline/detail. Exact geometry is preserved; do not thicken/recolour to force a pass.')
        proof={'schema_version':1,'step':step,'code':code,'checked_on':'2026-10-16','status':'open_delivery_hold','delivery_accepted':False,'scored_activation':False,'question_changes_applied':False,'question_pair':pair,'asset':{'id':asset['id'],'original':asset['original'],'bundled':asset['bundled'],'rendering':asset['rendering']},'all_proposed_image_uses':uses,'content_review':'passed for exact proposed content; not applied','neutral_description_review':'accepted existing 9D descriptions','platform_evidence':{'android':{'status':'captured, not final acceptance','records':android},'desktop':{'status':'renderer, keyboard, focus and geometry checks; not final reader/delivery acceptance','evidence':str(BASE/'9F/vector-fidelity.json')},'ios_simulator':{'status':'render captured, not final acceptance' if (ROOT/simulator).exists() else 'pending complete target evidence','screenshot':identity(simulator) if (ROOT/simulator).exists() else None},'wasm_js':{'status':'render captured, not final acceptance' if (ROOT/web).exists() else 'pending complete target evidence','screenshot':identity(web) if (ROOT/web).exists() else None},'ios_device':{'status':'out of this run scope: user explicitly selected simulator on 2026-10-16','evidence':[]}},'blockers':blockers,'content_id_decision':'Retain both authored IDs and their delivery holds. Do not apply replacements or release scoring until all target and legibility checks pass; faint previews require an official legible exact-code rendition or a separately approved presentation/content-ID decision.'}
        files[folder/'delivery-proof.json']=dump(proof)
        files[folder/'proposal-review.json']=dump({'step':step,'application':'deferred until delivery acceptance','question_ids':pair,'questions':content})
        files[folder/'README.md']=f'''# {step} — {code} delivery review\n\n**Open delivery hold.** Checked the exact asset bytes, both proposed directions, all four options, authored key/feedback and accepted 9D descriptions. The two legacy question records remain unchanged and are excluded from new scored sessions.\n\n[Delivery evidence and blockers](delivery-proof.json) · [Exact candidate content review](proposal-review.json) · [Shared implementation, verification and reproduction](../9F/README.md).\n\nAll four Android size/surface/text-scale captures are retained. Captures are not final acceptance. The user selected simulator scope; unresolved reader/delivery proof keeps this task open. {'The 105dp preview also remains faint; the recorded content/ID decision retains the hold without changing official geometry.' if code in FAINT else 'No final all-target delivery acceptance is claimed.'}\n'''
        summary.append({'step':step,'code':code,'question_ids':pair,'status':'open_delivery_hold','content_review':'passed proposed content; application deferred','android_captures':4,'faint_small_preview':code in FAINT})
    files[BASE/'9F/delivery-summary.json']=dump({'checked_on':'2026-10-16','steps_reviewed':19,'replacement_questions':38,'exact_asset_uses':38,'all_candidate_image_occurrences':95,'android_captures':76,'delivery_acceptances':0,'question_records_changed':0,'legacy_replacements_excluded_from_scoring':38,'steps':summary})
    return files

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    for path,value in build().items():
        if args.check:assert (ROOT/path).read_text()==value,path
        else:(ROOT/path).parent.mkdir(parents=True,exist_ok=True);(ROOT/path).write_text(value)
    print('9F1–9F19 reviewed: 38 unchanged replacements held; 76 Android captures; missing acceptance is not promoted to passed.')
if __name__=='__main__':main()
