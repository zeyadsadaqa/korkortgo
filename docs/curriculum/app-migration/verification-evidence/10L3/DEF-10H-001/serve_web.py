import argparse,functools,http.server,json,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('label',choices=['proof','normal']);a=p.parse_args();OUT=Path(__file__).parent;root=Path('/tmp/korkort-10l-h001-web-'+a.label)
class Handler(http.server.SimpleHTTPRequestHandler):
 def end_headers(self):self.send_header('Cache-Control','no-store');super().end_headers()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(root)));(OUT/(a.label+'-web-server.json')).write_text(json.dumps({'origin':'http://127.0.0.1:'+str(server.server_port),'pid':os.getpid(),'root':str(root),'scope':'Temporary localhost QA only'},indent=2)+'\n');print(server.server_port,flush=True);server.serve_forever()
