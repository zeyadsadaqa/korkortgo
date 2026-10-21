import html,json,os,subprocess,sys
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[4]
load=lambda p:json.loads(p.read_text())
subprocess.run([sys.executable,str(OUT/'deduplicate_captures.py')],check=True)
capture_paths={x['path']:x['stored_path'] for x in load(OUT/'capture-index.json')['captures']}
index=load(OUT.parent/'10J1/design-comparison-index.json')
shared=load(OUT/'shared-presentation-observations.json')['cases'];production=load(OUT/'shared-production-observations.json')['cases']
# Explicit visual-inspection subset; never claim every generated frame has been visually reviewed.
inspected={'library-overview':'1280-1.0','library-empty':'390-1.6','reader-opening':'390-1.6','knowledge-revealed':'390-1.6','reader-long':'390-1.6','review-standard':'390-1.6','source-detail':'390-1.6','reference-detail':'1280-1.0','legacy-chooser':'390-1.6','signal-failure':'390-1.6'}
findings={
 'DEF-10J-001':(['library-overview','library-filter','library-empty'],'Library badge/chevron/document-row grouping and empty-state control hierarchy differ from approved8B/8C.'),
 'DEF-10J-002':(['reader-opening','knowledge-hidden','knowledge-revealed','reader-long'],'Goal/Requirements/check/answer hierarchy reduced to inline body labels and generic text button; approved panel/heading treatment absent.'),
 'DEF-10J-003':(['source-directory','source-detail','source-failure'],'Source detail Scope/Limits/host/return hierarchy absent; exact record text is independently checked in10J3.'),
 'DEF-10J-004':(['reference-detail','reference-credits'],'SignReferenceDetail overrides approved font with FontFamily.Serif; use bundled SourceSerif4 requirement.'),
 'DEF-10J-005':(['legacy-chooser','generic-unavailable','signal-unavailable','signal-failure'],'Informational group/action framing differs from8K/8L; no new route behavior is proposed.'),
 'DEF-10J-006':(['review-standard','review-calculation'],'Distinct Explanation and related/source grouping absent; retain all required option feedback.')}
rows=[]
for s in index['states']:
 captures=[x['capture'] for x in shared+production if x['state_id']==s['state_id']]
 ds=[k for k,(states,_) in findings.items() if s['state_id'] in states]
 rows.append({'state_id':s['state_id'],'approved_references':s['approved_references'],'current_shared_captures':captures,'visually_inspected_capture':f"captures/{s['state_id']}-{inspected[s['state_id']]}.png" if s['state_id'] in inspected else None,'findings':ds,'status':'open_fidelity_finding' if ds else 'captured_pending_detailed_visual_and_target_review' if captures else 'pending_fresh_capture','remaining':['fresh10K configured normal/proof builds and platform semantics','all theme/font/scroll/focus/interaction combinations; existing open defects not waived'],'comparison_note':'; '.join(findings[x][1] for x in ds) or s['approval_limit']})
result={'task':'10J2','status':'executed_shared_scope_gate_open','counts':{'states':len(rows),'shared_component_captures':len(shared),'actual_app_captures':len(production),'explicit_visual_pairs_reviewed':len(inspected),'new_product_findings':len(findings)},'states':rows,'fresh10K_captures_available':False,'fixed_light_is_not_os_dark_proof':True}
(OUT/'comparison-results.json').write_text(json.dumps(result,indent=2)+'\n')
page=['<!doctype html><html lang="en"><meta charset="utf-8"><title>10J approved/current comparisons</title><style>body{font:16px system-ui;margin:32px;color:#172c29}article{border-top:2px solid #173e32;padding:24px 0}figure{margin:8px}img{max-width:100%;height:auto} .pair{display:grid;grid-template-columns:1fr 1fr;gap:24px} .note{background:#fff3df;padding:16px}details{margin:16px 0}</style><h1>10J presentation audit</h1><p>Unmodified approved/current images; annotations are audit text, not new design proposals. Shared components omit the app shell. No pixel-to-dp comparison or native acceptance is implied.</p>']
for row in rows:
 page.append('<article><h2>'+html.escape(row['state_id'])+'</h2><p class="note">'+html.escape(row['status']+': '+row['comparison_note'])+'</p>')
 page.append('<p>Explicit visual inspection: '+html.escape(row['visually_inspected_capture'] or 'pending detailed visual review')+'</p><div class="pair"><div>')
 for p in row['approved_references']:
  path=os.path.relpath(R/p,OUT/'annotated-comparisons');page.append(f'<figure><figcaption>Approved: {html.escape(p)}</figcaption><a href="{path}"><img loading="lazy" src="{path}" alt="Approved reference"></a></figure>')
 page.append('</div><div>')
 for p in row['current_shared_captures']:
  path='../'+capture_paths[p];page.append(f'<details><summary>{html.escape(p)}</summary><a href="{path}"><img loading="lazy" src="{path}" alt="Current shared render"></a></details>')
 page.append('</div></div><p>Required final target comparisons remain open.</p></article>')
page.append('</html>');(OUT/'annotated-comparisons/index.html').write_text('\n'.join(page))
print(result['counts'])
