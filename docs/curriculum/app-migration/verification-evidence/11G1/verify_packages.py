import hashlib,json,pathlib,zipfile
root=pathlib.Path.cwd();out=root/'docs/curriculum/app-migration/verification-evidence/11G1';build=pathlib.Path('/tmp/korkort-step11-normal-build');ios=pathlib.Path('/tmp/korkort-step11-normal-ios/Build/Products/Debug-iphonesimulator/Korkort.app')
source=root/'composeApp/src/commonMain/composeResources';prefix='composeResources/se.korkort.resources/'
paths={str(p.relative_to(source)):p for p in source.rglob('*') if p.is_file() and not p.name.startswith('.')}
targets={'desktop':build/'processedResources/desktop/main','wasm_js':build/'dist/wasmJs/productionExecutable','ios_simulator':ios/'compose-resources','ios_device_resources':build/'generated/compose/resourceGenerator/assembledResources/iosArm64Main'}
rows=[]
apk=build/'outputs/apk/debug/composeApp-debug.apk'
with zipfile.ZipFile(apk) as archive:
 for relative,path in sorted(paths.items()):
  expected=hashlib.sha256(path.read_bytes()).hexdigest(); checks={'android':hashlib.sha256(archive.read('assets/'+prefix+relative)).hexdigest()==expected}
  for name,folder in targets.items():checks[name]=hashlib.sha256((folder/prefix/relative).read_bytes()).hexdigest()==expected
  assert all(checks.values()),(relative,checks)
  rows.append({'resource':relative,'sha256':expected,'parity':checks})
 dex=[archive.read(n) for n in archive.namelist() if n.endswith('.dex')]
 for token in [b'Step10Candidate',b'DeliveryProofActivity',b'Step10CorrectionProof']:assert not any(token in data for data in dex),token
jar=build/'libs/composeApp-desktop.jar'
with zipfile.ZipFile(jar) as archive:
 forbidden=[n for n in archive.namelist() if any(token in n for token in ['Step10Candidate','DeliveryProof','Step10CorrectionProof'])];assert not forbidden,forbidden
website=targets['wasm_js'];executables=[p for p in website.iterdir() if p.suffix in ['.js','.wasm']]
for path in executables:
 data=path.read_bytes()
 for token in [b'Unscored accepted artwork fixture',b'Exact question images ready']:assert token not in data,(path,token)
artifacts=[apk,jar,build/'bin/iosSimulatorArm64/debugFramework/KorkortKit.framework/KorkortKit',build/'bin/iosArm64/debugFramework/KorkortKit.framework/KorkortKit',ios/'Korkort']+executables
result={'status':'pass','resource_count':len(rows),'resources':rows,'normal_artifacts_exclude_verification_hosts':True,'artifacts':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in artifacts],'scope':'Normal package/resources only; runtime acceptance and screen-reader listening are separately recorded.'}
(out/'resource-parity.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(rows),'exact resource files on five package/resource targets; normal Android/JVM/Wasm exclude proof hosts.')
