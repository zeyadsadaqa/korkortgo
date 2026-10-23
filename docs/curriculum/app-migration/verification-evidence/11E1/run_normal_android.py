import hashlib,io,json,os,pathlib,subprocess,sys,tarfile
root=pathlib.Path.cwd();name=sys.argv[1];method=sys.argv[2] if len(sys.argv)>2 else "productionPracticeAndReviewUseAcceptedPackage";out=root/'docs/curriculum/app-migration/verification-evidence/11E1'/name;out.mkdir(exist_ok=False)
adb=['/Users/zeyad/Library/Android/sdk/platform-tools/adb','-s','emulator-5554']
def shell(*args):return subprocess.check_output(adb+['shell',*args],text=True).strip()
settings={'font_scale':shell('settings','get','system','font_scale'),'night':shell('cmd','uimode','night')}
(out/'entry-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
artifacts=[]
for p in [pathlib.Path('/tmp/korkort-step11-normal-build/outputs/apk/debug/composeApp-debug.apk'),pathlib.Path('/tmp/korkort-step11-normal-build/outputs/apk/androidTest/debug/composeApp-debug-androidTest.apk')]:
 subprocess.run(adb+['install','-r',str(p)],check=True);artifacts.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(out/'artifact-receipt.json').write_text(json.dumps(artifacts,indent=2)+'\n')
installed=shell('pm','path','se.korkort.study').removeprefix('package:');assert shell('sha256sum',installed).split()[0]==artifacts[0]['sha256']
command=adb+['shell','am','instrument','-w','-e','class','se.korkort.NormalJourneyStep11Test#'+method,'-e','evidenceRun',name,'se.korkort.study.test/androidx.test.runner.AndroidJUnitRunner']
for key,argument in [('TEST_SETTING','onlySetting'),('TEST_MODE','onlyMode')]:
 if key in os.environ:command[-1:-1]=['-e',argument,os.environ[key]]
try:
 result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'instrumentation.log').write_text(result.stdout);print(result.stdout,flush=True)
 raw=subprocess.check_output(adb+['exec-out','run-as','se.korkort.study','tar','-C','files/'+name,'-cf','-','.'])
 with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(out,filter='data')
 assert result.returncode==0 and 'OK (1 test)' in result.stdout and 'FAILURES' not in result.stdout
 rows=[json.loads(t) for t in (out/('production-journeys.jsonl' if method.startswith('production') else 'learning-journeys.jsonl')).read_text().splitlines()];assert len(rows)==int(os.environ.get("EXPECTED_CASES","8"))
 (out/'results.json').write_text(json.dumps({'status':'pass','rows':rows,'normal_apk_installed_byte_identity_verified':True,'artifacts':artifacts},indent=2)+'\n')
finally:
 shell('settings','put','system','font_scale',settings['font_scale'])
 shell('cmd','uimode','night',settings['night'].split(':')[-1].strip())
 (out/'restored-settings.json').write_text(json.dumps({'font_scale':shell('settings','get','system','font_scale'),'night':shell('cmd','uimode','night')},indent=2)+'\n')
print(f'PASS {len(rows)} normal Android journeys with restored settings.')
