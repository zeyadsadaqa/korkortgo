"""Run a named verification command, preserving logs and before/after input hashes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
task, name, *command = sys.argv[1:]
folder = BASE / task
folder.mkdir(exist_ok=True)
def fingerprint():
    paths = []
    for directory in ['composeApp/src', 'content', 'iosApp']:
        paths.extend(p for p in (ROOT / directory).rglob('*') if p.is_file() and '/build/' not in str(p) and p.name != '.DS_Store')
    paths.extend((BASE / '11B1').glob('*'))
    paths.append(ROOT / 'composeApp/build.gradle.kts')
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.is_file()}
before = fingerprint()
env = dict(os.environ, JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home')
env['STEP11_INPUT_FINGERPRINT'] = hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest()
checkpoint_reuse = None
if env.get('STEP11_CHECKPOINT_FROM'):
    previous = json.loads(Path(env['STEP11_CHECKPOINT_FROM']).read_text())['inputs']
    changed = [p for p in sorted(before.keys() | previous.keys()) if before.get(p) != previous.get(p)]
    assert all(p.startswith('docs/curriculum/app-migration/verification-evidence/11B1/') and Path(p).suffix in ['.md','.json'] for p in changed), changed
    identity = hashlib.sha256(json.dumps(previous,sort_keys=True).encode()).hexdigest()
    assert (BASE/'11D1/checkpoint-input.txt').read_text() == identity
    env['STEP11_INPUT_FINGERPRINT'] = identity
    checkpoint_reuse = dict(previous_input_record=env['STEP11_CHECKPOINT_FROM'], changed_nonruntime_metadata=changed, runtime_and_harness_inputs_identical=True)
(folder / (name + '-inputs.json')).write_text(json.dumps(before,indent=2)+'\n')
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
with (folder / (name + '.log')).open('x') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
after = fingerprint()
record = dict(checkpoint_reuse=checkpoint_reuse, command=command, started_utc=started, seconds=round(time.monotonic()-start, 2), exit_code=result.returncode,
              log=name+'.log', inputs=before, changed_inputs=[p for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)])
(folder / (name + '.json')).write_text(json.dumps(record, indent=2)+'\n')
print(task, name, 'exit', result.returncode)
print((folder / (name + '.log')).read_text()[-3000:])
sys.exit(result.returncode)
