"""Audit saved XCTest checkpoints without altering original run receipts."""
import hashlib, json, pathlib, re
from PIL import Image, ImageChops, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = pathlib.Path(__file__).resolve().parent
EVIDENCE = OUT.parent
RUNS = ['ios-152-r2', 'ios-light-large-resume-r3', 'ios-dark-default-r3', 'ios-dark-large-r3', 'ios-dark-s1-clean-r4']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, value): (OUT/name).write_text(json.dumps(value, indent=2)+'\n')
def rel(p): return str(p.relative_to(OUT))
def name(a):
    # xcresulttool inserts its UUID before the last dot, including decimal scales.
    s = re.sub(r'_\d+_[A-F0-9-]{36}', '', a['suggestedHumanReadableName'])
    return re.sub(r'\.(png|txt|json)$', '', s)
questions = json.loads((EVIDENCE/'11B2/current-replacements.json').read_text())
bank = {q['key']['question_id']: q for q in json.loads((ROOT/'content/accepted-assessment-questions.json').read_text())['questions']}
assert len(questions) == 38
for q in questions:
    b = bank[q['id']]
    assert b['key']['revision'] == q['revision']
    assert bool(b['image']) == q['stem']
    assert sum(bool(o['image']) for o in b['options']) == q['optionImages']
expected = {(q['id'], dark, scale): q for q in questions for dark in [False, True] for scale in ['1', '1.6']}
cases, runs, audit = {}, [], []
for run in RUNS:
    d = OUT/run; attachments = d/'attachments'
    summary = json.loads((d/'summary.json').read_text())
    entries = [a for t in json.loads((attachments/'manifest.json').read_text()) for a in t['attachments']]
    lookup = {name(a): a for a in entries}
    checkpoints = [a for a in entries if name(a).startswith('question-matrix-')]
    accepted = {}
    for a in sorted(checkpoints, key=lambda a:a['timestamp']):
        rows = json.loads((attachments/a['exportedFileName']).read_bytes())
        for row in rows:
            key = (row['question_id'], row['dark'], row['font_scale'])
            if key in accepted: assert accepted[key][0] == row
            accepted[key] = (row, a)
    assert len(checkpoints) == len(accepted)
    for key, (row, checkpoint) in accepted.items():
        assert key in expected
        if key in cases:
            assert run=='ios-dark-s1-clean-r4' and key==('sign-meaning-S1',True,'1')
            assert all(cases[key][field]==value for field,value in row.items())
        q = expected[key]
        assert row['revision'] == q['revision'] and row['native_selection_confirm']=='passed'
        assert row['native_pending_pixels_changed'] is True
        assert row['image_zoom_returns'] == int(q['stem'])+q['optionImages']
        prefix = f"question-{key[0]}-{str(key[1]).lower()}-{key[2]}"
        stages = ['inline', 'pending'] + (['Enlarge question image-zoom'] if q['stem'] else [f'Enlarge option {c} image-zoom' for c in 'ABCD'])
        captures = {}
        for stage in stages:
            png = attachments/lookup[prefix+'-'+stage]['exportedFileName']
            tree = attachments/lookup[prefix+'-'+stage+'-tree']['exportedFileName']
            with Image.open(png) as im:
                im.load(); assert im.size == (1206,2622)
            text = tree.read_text()
            assert 'Correct answer' not in text
            assert 'Image unavailable' not in text
            assert '{{0.0, 0.0}, {402.0, 874.0}}' in text
            if stage == 'pending':
                selected = re.findall(r"Button,[^\n]+label: '[^']*', value: Selected[^\n]*", text)
                assert len(selected)==1
                assert 'value: Not selected' in text
                m = re.search(r'\{\{([\d.-]+), ([\d.-]+)\}, \{([\d.-]+), ([\d.-]+)\}\}', selected[0])
                x,y,w,h=map(float,m.groups()); assert x>=0 and y>=198 and x+w<=402.1 and y+h<=839.1
                selected_bounds = [x,y,w,h]
            if stage.endswith('-zoom'):
                assert "label: 'Close'" in text and "label: 'Reset'" in text and '150%' in text
                assert 'value: Selected' not in text
            captures[stage] = {'png':rel(png),'png_sha256':sha(png),'tree':rel(tree),'tree_sha256':sha(tree)}
        # Whole-frame differences are supplementary only: native XCTest compares
        # the same radio's pixel buffer before/after tapping, without scrolling.
        with Image.open(OUT/captures['inline']['png']) as before, Image.open(OUT/captures['pending']['png']) as after:
            bounds=ImageChops.difference(before.convert('RGB'),after.convert('RGB')).getbbox()
            assert bounds
        setting=('dark' if key[1] else 'light')+('-160' if key[2]=='1.6' else '-100')
        case = dict(row, case_id=f'T03-ART-ios_simulator-{key[0]}-{setting}', setting=setting, status='pass', run=run,
                    checkpoint=rel(attachments/checkpoint['exportedFileName']), checkpoint_sha256=sha(attachments/checkpoint['exportedFileName']), captures=captures)
        if key in cases:
            case['supersedes_obscured_capture_from_run']=cases[key]['run']
            audit=[a for a in audit if a['case_id']!=case['case_id']]
        cases[key]=case
        audit.append({'case_id':case['case_id'],'selected_bounds_points':selected_bounds,'frame_change_bounds_pixels':bounds,'capture_count':len(captures),'native_pixel_assertion':True})
    runs.append({'run':run,'xctest_result':summary['result'],'completed_cases_retained':len(accepted),'summary_sha256':sha(d/'summary.json'),'manifest_sha256':sha(attachments/'manifest.json'),'device':summary['devicesAndConfigurations'][0]['device'],'test_failures':summary['testFailures']})
assert set(cases)==set(expected)
historical=(EVIDENCE/'10K7/platform-matrix.json').read_text()
assert all(c['case_id'] in historical for c in cases.values())
ordered=[cases[k] for k in expected]
save('ios-artwork-results.json',{'status':'pass_scoped_ios_simulator_artwork_matrix','cases':152,'questions':38,'image_zoom_returns':sum(c['image_zoom_returns'] for c in ordered),'settings':['light-100','light-160','dark-100','dark-160'],'runs':runs,'rows':ordered,'limitations':['Unscored accepted-artwork proof host; production journeys belong to 11E1.','Simulator native selection traits and control actions; no VoiceOver listening or physical-device runtime claim.','Original ios-152-r2 remains failed overall; only 49 fully completed checkpoints retained, remaining 27 light/large cases pass in r3.','No pan gesture assertion in this matrix; zoom/reset/close and return selection are exercised.']})
save('capture-audit.json',{'cases':len(cases),'captures':sum(x['capture_count'] for x in audit),'native_viewport_points':[402,874],'capture_pixels':[1206,2622],'rows':audit,'pixel_scope':'Cropped radio pixel assertions are in XCTest checkpoints. Full-frame differences alone are not proof of selection because scrolling may occur.','tree_scope':'All pending selected radios fit below fixture header and above bottom inset. All zoom trees contain 150%, Reset and Close, exclude answer cues and background selection.'})
# Contact sheets are navigation aids; retain original resolution attachments.
visual=OUT/'visual-review'; visual.mkdir(exist_ok=True)
index=[]
for setting in ['light-100','light-160','dark-100','dark-160']:
    subset=[c for c in ordered if c['setting']==setting]
    for stage in ['pending','artwork']:
        for part in range(2):
            group=subset[part*19:(part+1)*19]
            sheet=Image.new('RGB',(5*260,4*600),'#d8d8d8'); draw=ImageDraw.Draw(sheet)
            for i,c in enumerate(group):
                s='pending' if stage=='pending' else next(s for s in c['captures'] if s.endswith('-zoom'))
                p=OUT/c['captures'][s]['png']
                with Image.open(p) as im:
                    im=im.convert('RGB'); im.thumbnail((256,556)); sheet.paste(im,((i%5)*260,(i//5)*600+35))
                draw.text(((i%5)*260+3,(i//5)*600+2),c['question_id'],fill='black')
                index.append({'sheet':f'{setting}-{stage}-{part+1}.jpg','case_id':c['case_id'],'stage':s,'original':rel(p)})
            sheet.save(visual/f'{setting}-{stage}-{part+1}.jpg',quality=88)
save('visual-review/index.json',index)
print(f'Audited {len(cases)} cases, {sum(c["image_zoom_returns"] for c in ordered)} returns and {sum(x["capture_count"] for x in audit)} captures')
