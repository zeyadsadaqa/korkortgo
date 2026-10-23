import http.server
import json
import os
from pathlib import Path

root = '/tmp/korkort-step11-proof-build/dist/wasmJs/developmentExecutable'
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=root, **kwargs)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *args):
        pass
server = http.server.ThreadingHTTPServer(('127.0.0.1',51109), Handler)
record = dict(pid=os.getpid(),origin='http://127.0.0.1:51109',root=root,proof_only=True)
Path(__file__).with_name('server-resumed.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
server.serve_forever()
