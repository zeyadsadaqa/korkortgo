import hashlib,json,re,shutil,subprocess
from pathlib import Path
OUT=Path(__file__).parent;bundle='/tmp/korkort-10k4-native.xcresult';export=Path('/tmp/korkort-10k4-export')
summary=json.loads(subprocess.check_output(['xcrun','xcresulttool','get','test-results','summary','--path',bundle]));(OUT/'native-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
subprocess.run(['xcrun','xcresulttool','export','attachments','--path',bundle,'--output-path',str(export)],check=True)
mapping=[];dest=OUT/'native-evidence';dest.mkdir(exist_ok=True)
for test in json.loads((export/'manifest.json').read_text()):
 for attachment in test['attachments']:
  source=export/attachment['exportedFileName'];name=attachment['suggestedHumanReadableName'];name=re.sub(r'_0_[0-9A-Fa-f]{8}(?:-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}','',name)
  if not name.endswith(source.suffix):name+=source.suffix
  name=name.replace('/','_')
  target=dest/name
  if target.exists() and target.read_bytes()!=source.read_bytes():name=source.name;target=dest/name
  shutil.copy2(source,target);mapping.append({'test':test.get('testName',test.get('testIdentifier')),'suggested_name':attachment['suggestedHumanReadableName'],'saved':'native-evidence/'+name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'associated_with_failure':attachment.get('isAssociatedWithFailure'),'device_id':attachment.get('deviceId')})
(OUT/'attachment-map.json').write_text(json.dumps(mapping,indent=2)+'\n');print('Native result',summary.get('result'),summary.get('totalTestCount'),'tests;',len(mapping),'attachments')
assert summary['totalTestCount']==6,'Do not call an empty/partial suite a six-test pass'
