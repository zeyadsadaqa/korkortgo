"""Start task-owned local verification independently of an interactive terminal."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

base = Path(__file__).resolve().parent
task, name, *command = sys.argv[1:]
out = base / task
out.mkdir(exist_ok=True)
with (out / (name + '-launch.log')).open('x') as log:
    process = subprocess.Popen(command, cwd=base.parents[3], stdout=log, stderr=subprocess.STDOUT,
                               start_new_session=True, stdin=subprocess.DEVNULL)
record = dict(pid=process.pid, command=command, started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(out / (name + '-process.json')).write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))
