import hashlib, json, pathlib, subprocess, sys, tarfile, io
root=pathlib.Path.cwd(); task, name, count=sys.argv[1:]; out=root/'docs/curriculum/app-migration/verification-evidence'/task/name;out.mkdir(parents=True,exist_ok=False)
adb=['/Users/zeyad/Library/Android/sdk/platform-tools/adb','-s','emulator-5554']
build=pathlib.Path('/tmp/korkort-step11-proof-build')
artifacts=[]
for path in [build/'outputs/apk/debug/composeApp-debug.apk',build/'outputs/apk/androidTest/debug/composeApp-debug-androidTest.apk']:
 subprocess.run(adb+['install','-r',str(path)],check=True)
 artifacts.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
command=adb+['shell','am','instrument','-w','-e','class','se.korkort.NativeReaderRouteTest#heldQuestionNativeDeliveryMatrix','-e','questionGroup','accepted-replacements','-e','questionCount',count,'-e','captureAll','true','-e','evidenceRun',name,'se.korkort.study.verification.test/androidx.test.runner.AndroidJUnitRunner']
result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(out/'instrumentation.log').write_text(result.stdout)
print(result.stdout,flush=True)
if result.returncode or 'FAILURES' in result.stdout or 'OK (1 test)' not in result.stdout:sys.exit(1)
raw=subprocess.check_output(adb+['exec-out','run-as','se.korkort.study.verification','tar','-C','files/'+name,'-cf','-','.'])
with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(out,filter='data')
rows=json.loads((out/('question-matrix-0-'+count+'.json')).read_text())
assert rows['complete'] and len(rows['rows'])==int(count)*4
(out/'artifacts.json').write_text(json.dumps(artifacts,indent=2)+'\n')
print('PASS',len(rows['rows']),'current accepted Android contexts')
