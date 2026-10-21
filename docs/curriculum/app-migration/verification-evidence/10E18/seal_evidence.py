"""Create per-task artifact manifests after verification; check them without resealing via verify_evidence.py."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
for i in range(1,19):
 folder=BASE/f'10E{i}';rows=[{'path':str(p.relative_to(folder)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='artifacts.json' and '__pycache__' not in p.parts]
 (folder/'artifacts.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Sealed 18 task artifact manifests; run verify_evidence.py --check-manifests to check them.')
