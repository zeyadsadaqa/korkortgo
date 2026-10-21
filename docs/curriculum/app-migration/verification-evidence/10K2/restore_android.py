import hashlib,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;runner=OUT.parent/'10K1/run_logged.py';adb='/Users/zeyad/Library/Android/sdk/platform-tools/adb';device='emulator-5554'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proof_inputs={str(p.relative_to(R)):sha(p) for p in [R/'composeApp/build/outputs/apk/debug/composeApp-debug.apk',R/'composeApp/build/outputs/apk/androidTest/debug/composeApp-debug-androidTest.apk',OUT/'AdditionalNative10KTest.kt',R/'composeApp/src/verificationAndroidTest/kotlin/se/korkort/NativeReaderRouteTest.kt']}
(OUT/'final-proof-inputs.json').write_text(json.dumps(proof_inputs,indent=2)+'\n')
cmd=['./gradlew',':composeApp:assembleDebug','--offline','--no-daemon','--max-workers=1','-Pkotlin.compiler.execution.strategy=in-process','-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8']
rc=subprocess.run([sys.executable,str(runner),'10K2','restore-normal-build',*cmd],cwd=R).returncode
original=json.loads((OUT/'original-device-environment.json').read_text())
def call(*args):return subprocess.check_output([adb,'-s',device,*args],text=True).strip()
for key,service in [('wifi_on','wifi'),('mobile_data','data')]:call('shell','svc',service,'enable' if original[key]=='1' else 'disable')
if rc:raise SystemExit(rc)
apk=R/'composeApp/build/outputs/apk/debug/composeApp-debug.apk';subprocess.run([sys.executable,str(runner.parent/'verify_packaged_resources.py'),'--package',str(apk),'--prefix','assets/composeResources/se.korkort.resources/','--label','android-restored-normal','--output',str(OUT/'restored-package-resource-parity.json')],check=True)
call('install','-r',str(apk));call('shell','am','force-stop','se.korkort.study.verification');call('shell','am','force-stop','se.korkort.study');call('shell','am','start','-W','-n','se.korkort.study/se.korkort.MainActivity')
path=call('shell','pm','path','se.korkort.study').removeprefix('package:');installed=Path('/tmp/korkort-10k-installed-normal.apk');call('pull',path,str(installed));assert sha(installed)==sha(apk)
aapt=next((Path('/Users/zeyad/Library/Android/sdk/build-tools')).glob('36.0.0/aapt2'))
manifest=subprocess.check_output([str(aapt),'dump','xmltree',str(apk),'--file','AndroidManifest.xml'],text=True);(OUT/'restored-normal-manifest.txt').write_text(manifest);assert 'DeliveryProofActivity' not in manifest
current={key:call('shell','settings','get',ns,key) for ns,key in [('global','wifi_on'),('global','mobile_data'),('system','font_scale'),('secure','enabled_accessibility_services'),('secure','accessibility_enabled')]}
result={'status':'pass' if all(current[k]==original[k] for k in current) else 'settings_restore_mismatch','normal_apk_sha256':sha(apk),'installed_apk_sha256':sha(installed),'proof_activity_in_normal_manifest':False,'original_settings':original,'restored_settings':current,'normal_app_launched':True,'publication':False}
(OUT/'runtime-restored.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
