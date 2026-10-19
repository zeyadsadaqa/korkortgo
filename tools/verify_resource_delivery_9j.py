import json,hashlib,zipfile,pathlib
import argparse
root=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Verify all exact curriculum resource bytes in the four platform bundles.')
parser.add_argument('--ios-bundle',type=pathlib.Path,required=True)
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
c=json.loads((root/'content/curriculum.json').read_text())
apk=root/'composeApp/build/outputs/apk/debug/composeApp-debug.apk'
ios=args.ios_bundle/'compose-resources'
wasm=root/'composeApp/build/dist/wasmJs/developmentExecutable'
desktop=root/'composeApp/build/processedResources/desktop/main'
rows=[]
with zipfile.ZipFile(apk) as z:
 for a in c['assets']:
  suffix='composeResources/se.korkort.resources/'+a['bundled']['path'].removeprefix('composeApp/src/commonMain/composeResources/')
  expected=a['bundled']['sha256']
  targets={'android':z.read('assets/'+suffix),'ios_simulator':(ios/suffix).read_bytes(),'wasm_js':(wasm/suffix).read_bytes(),'desktop':(desktop/suffix).read_bytes()}
  assert all(hashlib.sha256(data).hexdigest()==expected for data in targets.values()),a['id']
  rows.append({'asset_id':a['id'],'asset_sha256':expected,'packaged_byte_parity':{p:'passed' for p in targets}})
out=root/'docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14/resource-inventory.json'
text=json.dumps({'date':'2026-10-19','status':'passed','scope':'All exact resources present with original bytes in the four tested platform resource bundles. This is package byte parity, not a claim that each asset was independently viewed on each native target.','asset_count':len(rows),'assets':rows},indent=2)+'\n'
if args.check: assert out.read_text()==text
else: out.write_text(text)
print(len(rows),'resource hashes match on all four platforms')
