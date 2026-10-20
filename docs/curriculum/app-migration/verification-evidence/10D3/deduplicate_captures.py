"""Package logical capture evidence without duplicate PNG bytes; preserve every original case/hash."""
import hashlib,json
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
index_path=HERE/'capture-index.json';index=json.loads(index_path.read_text());rows=index['captures'];groups=defaultdict(list)
protected={'captures/sign-recognise-S5-light-100-pre.png','captures/sign-recognise-S5-light-100-pending.png'}
for row in rows:
 p=HERE/row.get('stored_path',row['path']);assert sha(p)==row['sha256'],row['path'];groups[row['sha256']].append(row)
cleanup_path=HERE/'cleanup.json';previous=json.loads(cleanup_path.read_text()) if cleanup_path.exists() else {};actions={r['removed']:r for r in previous.get('actions',[])}
for digest,members in groups.items():
 # Keep the visible-defect before/after pair as explicit state evidence, even though it is identical.
 first=min(members,key=lambda r:(r['path'] not in protected,'-pre.png' not in r['path'],r['path']))
 retained=first.get('stored_path',first['path']);assert sha(HERE/retained)==digest
 for row in members:
  if row['path'] in protected:
   assert (HERE/row['path']).exists();row['stored_path']=row['path'];continue
  original=HERE/row['path'];row['stored_path']=retained
  if str(original.relative_to(HERE))!=retained and original.exists():
   assert sha(original)==digest
   actions[row['path']]={'removed':row['path'],'retained':retained,'sha256':digest,'bytes_removed':original.stat().st_size};original.unlink()
index['logical_capture_count']=len(rows);index['stored_capture_count']=len({r['stored_path'] for r in rows});index['path_resolution']='path is the original case capture name; stored_path is its retained physical PNG. Every logical record retains its original SHA-256.'
index_path.write_text(json.dumps(index,indent=2)+'\n')
cleanup={'task':'10D3 evidence packaging','scope':'Only byte-identical PNG captures are removed. Case observations, hashes, defect evidence, original artwork and historical tracked receipts are retained.','logical_captures':len(rows),'stored_captures':index['stored_capture_count'],'protected_distinct_state_paths':sorted(protected),'actions':sorted(actions.values(),key=lambda x:x['removed']),'reproduction':'After a fresh runtime run, reconcile_visual_results.py rebuilds the logical index; run deduplicate_captures.py to package identical captures again.'}
cleanup_path.write_text(json.dumps(cleanup,indent=2)+'\n')
print(json.dumps({'logical_captures':len(rows),'stored_captures':index['stored_capture_count'],'duplicates_removed':len(actions),'bytes_saved':sum(a['bytes_removed'] for a in actions.values())}))
