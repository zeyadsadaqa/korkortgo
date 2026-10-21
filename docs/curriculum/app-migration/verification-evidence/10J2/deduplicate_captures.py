"""Retain every logical observation while storing byte-identical captures once."""
import hashlib,json
from collections import defaultdict
from pathlib import Path
OUT=Path(__file__).parent
load=lambda name:json.loads((OUT/name).read_text())
previous={x['path']:x.get('stored_path',x['path']) for x in load('capture-index.json')['captures']} if (OUT/'capture-index.json').exists() else {}
logical=[x['capture'] for name in ['shared-presentation-observations.json','shared-production-observations.json'] for x in load(name)['cases']]
assert len(logical)==len(set(logical))==96
by_hash=defaultdict(list)
for name in logical:
 path=OUT/name if (OUT/name).exists() else OUT/previous[name]
 by_hash[hashlib.sha256(path.read_bytes()).hexdigest()].append((name,path))
records=[];duplicates=[]
for digest,items in by_hash.items():
 # Keep the ordinary home/detail names; aliases still describe distinct observations.
 preferred=sorted(items,key=lambda x:(x[0]!='captures/home.png',x[0]))[0]
 canonical=OUT/preferred[0] if (OUT/preferred[0]).exists() else preferred[1]
 for name,path in items:
  records.append({'path':name,'stored_path':str(canonical.relative_to(OUT)),'sha256':digest})
  if name!=str(canonical.relative_to(OUT)):
   duplicates.append({'logical_path':name,'stored_path':str(canonical.relative_to(OUT)),'sha256':digest,'bytes':canonical.stat().st_size,'reason':'Byte-identical render; retain logical observation/semantics and share original PNG bytes.'})
 # Only remove files after an exact byte comparison; never remove the canonical file.
 for name,path in items:
  candidate=OUT/name
  if candidate.exists() and candidate!=canonical:
   assert candidate.read_bytes()==canonical.read_bytes()
   candidate.unlink()
(OUT/'capture-index.json').write_text(json.dumps({'scope':'fresh shared only; logical capture paths resolve through stored_path','captures':sorted(records,key=lambda x:x['path'])},indent=2)+'\n')
(OUT/'cleanup.json').write_text(json.dumps({'logical_captures':len(logical),'physical_png_files':len(by_hash),'removed_duplicate_files':len(duplicates),'duplicate_bytes_removed':sum(x['bytes'] for x in duplicates),'duplicates':duplicates,'retained':'Baseline entry/exit and diagnostic receipts record distinct audit events; no historical/product file deleted.'},indent=2)+'\n')
print(f'Capture cleanup: {len(logical)} logical observations, {len(by_hash)} stored PNGs, {len(duplicates)} byte-identical aliases')
