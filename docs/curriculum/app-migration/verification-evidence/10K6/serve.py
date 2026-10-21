import argparse,http.server,json,functools
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['normal','proof'],required=True);a=p.parse_args();OUT=Path(__file__).parent;root=Path('/tmp/korkort-10k6-'+a.mode);assert root.is_dir()
class Handler(http.server.SimpleHTTPRequestHandler):
 def end_headers(self):self.send_header('Cache-Control','no-store');super().end_headers()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(root)));port=server.server_address[1];(OUT/f'{a.mode}-server.json').write_text(json.dumps({'origin':f'http://127.0.0.1:{port}','port':port,'root':str(root),'cache_control':'no-store','scope':'Temporary localhost-only static QA host; no publication or cold-offline/service-worker claim'},indent=2)+'\n');print('Serving',a.mode,'on',port,flush=True)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close();print('Server closed',flush=True)
