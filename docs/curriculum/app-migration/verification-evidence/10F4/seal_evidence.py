"""Seal current 10F evidence; checking manifests never rewrites observed failure receipts."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
for i in range(1,5):
 p=BASE/f'10F{i}';rows=[{'path':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='artifacts.json' and '__pycache__' not in f.parts]
 (p/'artifacts.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Sealed four 10F task manifests; T05 acceptance remains open.')
