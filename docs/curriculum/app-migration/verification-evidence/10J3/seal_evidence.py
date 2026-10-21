import hashlib,json
from pathlib import Path
for n in [1,2,3]:
 task=Path(__file__).parent.parent/f'10J{n}'
 files=[{'path':str(p.relative_to(task)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(task.rglob('*')) if p.is_file() and p.name!='artifacts.json' and '__pycache__' not in p.parts]
 (task/'artifacts.json').write_text(json.dumps({'task':task.name,'scope':'unchanged candidate independent audit; hashes do not grant acceptance','files':files},indent=2)+'\n')
 print(task.name,len(files),'sealed files')
