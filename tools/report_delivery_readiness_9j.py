"""Join actual per-question delivery checks to held candidate revisions, without waiving holds."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'docs/curriculum/app-migration/implementation-evidence/9J-followup'
FAINT={'S5','S6','S7','S11','S12','S13','T1','T2','T6','T8','T22','X8'}
def read(path):return json.loads(path.read_text())
def fingerprint(path):return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def build(delivery):
    bank_path=ROOT/'content/assessment-questions.json'
    questions=read(bank_path)['questions']
    held={q['key']['question_id']:q for q in questions if q['acceptance']['eligibility']=='held'}
    manifest_path=ROOT/'content/content-manifest.json'
    identity=read(manifest_path)['identity']
    proof=read(delivery)
    assert proof['package']==f"ContentPackageIdentity(contentVersion={identity['content_version']}, manifestSha256=Sha256(value={identity['manifest_sha256']}))",'Delivery proof belongs to another package'
    runs=proof['rows'];index={}
    for row in runs:
        key=(row['question_id'],row['dark'],row['font_scale'])
        assert key not in index,key
        assert row['question_id'] in held,key
        q=held[row['question_id']]
        assert row['revision']==q['key']['revision'],key
        images=list(filter(None,[q['image']]+[o['image'] for o in q['options']]))
        assert row['image_occurrences']==row['zoom_returns']==len(images),key
        index[key]=row
    expected={(qid,dark,scale) for qid in held for dark in [False,True] for scale in [1.0,1.6]}
    assert set(index)==expected,'Incomplete or extra per-question surface/text delivery runs'
    rows=[]
    for qid,q in sorted(held.items()):
        images=[('stem',q['image'])]+[(o['id'],o['image']) for o in q['options']]
        uses=[{'slot':slot,'asset_id':image['asset_id'],'known_faint_preview':image['asset_id'].removeprefix('official/') in FAINT} for slot,image in images if image]
        rows.append({'question_id':qid,'revision':q['key']['revision'],'images':uses,
            'desktop_semantics_loading_zoom_selection_return':'passed all four surface/text combinations',
            'known_faint_image_dependency':any(u['known_faint_preview'] for u in uses),
            'native_reader_acceptance':'pending','native_complete_question_matrix':'pending',
            'integrated_route_acceptance':'pending isolated route proof; production activation is not a prerequisite',
            'eligibility':'held','original_holds':q['acceptance']['open_holds']})
    return {'date':'2026-10-17','status':'additional delivery evidence; release acceptance remains open',
        'inputs':[fingerprint(bank_path),fingerprint(manifest_path),fingerprint(delivery)],
        'totals':{'held_questions':len(held),'desktop_question_runs':len(runs),'desktop_image_zoom_returns':sum(r['zoom_returns'] for r in runs),'questions_using_known_faint_assets':sum(r['known_faint_image_dependency'] for r in rows),'questions_without_known_faint_assets':sum(not r['known_faint_image_dependency'] for r in rows)},
        'dependency_order':'Run isolated delivery/route and 9M candidate checks together; accept content, rerun 9M3, then activate 9L14 and run integrated 9O.',
        'scope_limits':['Desktop semantics and exact-byte image loading do not certify visual legibility or native screen-reader operation.','No original 9F or 9J acceptance receipt is replaced.','No artwork, question revision, eligibility or release flag is changed.'],
        'questions':rows}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--delivery',type=Path,default=DEST/'desktop-delivery.json');p.add_argument('--check',action='store_true');args=p.parse_args()
    text=json.dumps(build(args.delivery),ensure_ascii=False,indent=2)+'\n';out=DEST/'readiness.json'
    if args.check:assert out.read_text()==text
    else:out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
    print('9J delivery readiness: complete desktop matrix recorded; native, route and legibility acceptance remain explicit.')
if __name__=='__main__':main()
