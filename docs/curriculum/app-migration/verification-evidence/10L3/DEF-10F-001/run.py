"""Run a new named check with durable logs; refuse to overwrite a prior run."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
root = out.parents[5]
name, *argv = sys.argv[1:]
log = out / (name + '.txt')
env = dict(os.environ, JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home')
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
def inputs():
    previous=json.loads((root/'docs/curriculum/app-migration/verification-evidence/10L2/DEF-10H-001/candidate-fingerprint.json').read_text())['source_files']
    paths={root/p for p in previous}
    paths.update((root/'composeApp/src').rglob('*.kt'))
    paths.update((root/'docs/curriculum/app-migration/verification-evidence/10L2/content-corrections/candidate/kotlin').glob('*.kt'))
    paths.update((root/'docs/curriculum/app-migration/verification-evidence/10L3/content-corrections').glob('*.kt'))
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.is_file()}
before=inputs()
fingerprint=hashlib.sha256(json.dumps(sorted(before.items()),separators=(',',':')).encode()).hexdigest()
snapshots=out/'input-snapshots';snapshots.mkdir(exist_ok=True)
snapshot=snapshots/(fingerprint+'.json')
if not snapshot.exists():snapshot.write_text(json.dumps({'source_runtime_fingerprint':fingerprint,'recipe':'Previous1273 protected inputs plus all current Kotlin source, staged correction Kotlin and new correction test harnesses','source_files':before},indent=2)+'\n')
t = time.monotonic()
with log.open('x') as handle:
    result = subprocess.run(argv, cwd=root, env=env, stdout=handle, stderr=subprocess.STDOUT)
after=inputs()
p = out / 'commands.json'
rows = json.loads(p.read_text()) if p.exists() else []
rows.append({'name': name, 'argv': argv, 'JAVA_HOME': env['JAVA_HOME'], 'started_utc': started,
             'seconds': round(time.monotonic() - t, 2), 'exit_code': result.returncode, 'log': log.name,
             'input_snapshot':str(snapshot.relative_to(out)), 'source_runtime_fingerprint':fingerprint,
             'inputs_changed_during_run':[p for p in sorted(set(before)|set(after)) if before.get(p)!=after.get(p)]})
p.write_text(json.dumps(rows, indent=2) + '\n')
print(name, 'exit', result.returncode, 'log', log)
print(log.read_text()[-2500:])
sys.exit(result.returncode)
