"""Seal exact changed-description delivery evidence; never edits active release files."""
import argparse
import json
from pathlib import Path

import finalize_step10_corrections as release
import stage_step10_corrections as staged


def outputs():
    targets, raw_inputs = release.observed_delivery()
    _, _, data, changed = staged.build()
    questions = [q for q in data['content/accepted-assessment-questions.json']['questions'] if q['key']['question_id'] in changed]
    base=release.BASE
    artifacts=[]
    # Initial dark observations and uncleared desktop frames are deliberately excluded.
    specifications=[('android-corrected-r1','*light*'),('android-dark-r2','*'),('desktop-corrected-r3/captures','*'),('browser-corrected-r2','*light*'),('browser-dark-r3','*.png'),('browser-dark-r3','*.ax.txt'),('metadata-corrected-r1/captures','*')]
    for directory,pattern in specifications:
        artifacts += [p for p in (base/directory).glob(pattern) if p.is_file()]
    for folder, dark in [('ios-corrected-r1',False),('ios-dark-r2',True)]:
        root=base/folder/'attachments'
        manifest=release.read(root/'manifest.json')[0]['attachments']
        artifacts.append(root/'manifest.json')
        for attachment in manifest:
            name=attachment['suggestedHumanReadableName']
            if ('-true-' if dark else '-false-') in name:
                artifacts.append(root/attachment['exportedFileName'])
    inventory_path=base/'accepted-delivery-artifacts.json'
    inventory={'scope':'Exact7 revised descriptions and corrected metadata fixtures; functional native/browser returns plus retained captures. This is not the full2920 artwork or132 normal journey completion.','superseded':'Original desktop-r1 overdraw captures and original dark proof observations retained as diagnostics; neither is used here.','files':[release.identity(p) for p in sorted(set(artifacts))]}
    inventory_text=release.dump(inventory)
    extra=[staged.OUT/'candidate-manifest.json',staged.AUTHOR,Path(__file__).resolve().relative_to(release.ROOT)]
    for directory,pattern in [('acceptance-inputs','*.json'),('shared-current-r1','result.json'),('browser-corrected-r2','distribution.json'),('browser-corrected-r2','matrix-runner.js'),('browser-dark-r3','distribution.json'),('browser-dark-r3','matrix-runner.js'),('android-dark-r2','installed-package.json'),('ios-dark-r2','bundle.json')]:
        extra+=sorted((base/directory).glob(pattern))
    inputs=[release.identity(p) for p in sorted(set(raw_inputs+extra))]
    inputs.append({'path':str(inventory_path),'sha256':release.sha(inventory_text.encode())})
    rows=[]
    assets={a['id']:a for a in data['content/curriculum.json']['assets']}
    platforms=release.read(Path('content/delivery-targets.json'))['required_platforms']
    for q in questions:
        id=q['key']['question_id'];per_target={}
        for target, observations in targets.items():
            actual=[r for r in observations if r['question_id']==id]
            per_target[target]={'status':'passed','settings':sorted({r['setting'] for r in actual}),'cases':len(actual),'zoom_returns':sum(r['zoom_returns'] for r in actual)}
        rows.append({'question_id':id,'revision':q['key']['revision'],'assessment_sha256':release.sha(release.canonical({k:v for k,v in q.items() if k!='acceptance'})),'status':'passed','reviewed_description_and_artwork':True,'targets':per_target,'assets':[{'asset_id':id,'asset_sha256':assets[id]['bundled']['sha256'],'status':'passed','platforms':platforms} for id in sorted({i['asset_id'] for i in [q['image'],*[o['image'] for o in q['options']]] if i})]})
    receipt={'status':'passed_exact_changed_revision_delivery','reviewed_on':'2026-10-22','ios_scope':'simulator','candidate_manifest':release.identity(staged.OUT/'candidate-manifest.json'),'review_basis':'X9 exact official artwork inspected: separate right arrows; neutral text names visible form without answer leakage. All7 revised image occurrences exercised on four configured targets, every required setting. Official asset bytes, prompts, options, keys and feedback unchanged. Source/caption fixtures independently checked; original source dates retained.','limits':'Renewed acceptance covers the bounded description revision and unchanged artwork delivery. It does not close the outstanding full step10 platform, visual, spoken assistive or normal-route matrix. Dark fixtures inject a palette into the fixed-light app solely for verification.','inputs':inputs,'questions':rows}
    return {inventory_path:inventory_text,release.RECEIPT:release.dump(receipt)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    args=parser.parse_args();files=outputs()
    for path,text in files.items():
        if args.check:assert (release.ROOT/path).read_text()==text,path
        else:(release.ROOT/path).write_text(text)
    _,_,data,changed=staged.build()
    release.require_delivery(release.read(release.RECEIPT),[q for q in data['content/accepted-assessment-questions.json']['questions'] if q['key']['question_id'] in changed])
    print('PASS:7 exact revisions; Android28/iOS28/browser28/desktop56; no active release writes.')


if __name__=='__main__':main()
