import hashlib,json,urllib.request,urllib.parse
from pathlib import Path
OUT=Path(__file__).parent;x=json.loads((OUT/'normal-distribution.json').read_text());origin=json.loads((OUT/'normal-server.json').read_text())['origin'];rows=[]
for record in x['files']:
 url=origin+'/'+urllib.parse.quote(record['path']);req=urllib.request.Request(url,headers={'Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=15) as response:
  data=response.read();digest=hashlib.sha256(data).hexdigest();rows.append({'path':record['path'],'status_code':response.status,'content_type':response.headers.get('Content-Type'),'cache_control':response.headers.get('Cache-Control'),'expected_sha256':record['sha256'],'actual_sha256':digest,'pass':digest==record['sha256']})
result={'origin':origin,'status':'pass' if all(x['pass'] for x in rows) else 'fail','served_files':len(rows),'checks':rows,'scope':'Actual HTTP responses for every production distribution file, including executable,Wasm,all artwork/fonts/licences; not a claim each file was visually reviewed.'};(OUT/'http-parity.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(rows),'HTTP byte checks')
