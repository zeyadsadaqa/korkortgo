import http.server
import json
import os
import sys
from pathlib import Path

root=sys.argv[1] if len(sys.argv)>1 else '/tmp/korkort-step10-proof-r2'
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=root,**kwargs)
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
record={'origin':'http://127.0.0.1:'+str(server.server_port),'pid':os.getpid(),'root':root,'proof_only':True}
(Path(__file__).parent/(sys.argv[2] if len(sys.argv)>2 else 'proof-web-server.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
server.serve_forever()
