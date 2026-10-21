import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;adb='/Users/zeyad/Library/Android/sdk/platform-tools/adb';device='emulator-5554'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def call(*args):return subprocess.check_output([adb,'-s',device,*args],text=True).strip()
original=json.loads((OUT/'original-device-environment.json').read_text());apk=R/'composeApp/build/outputs/apk/debug/composeApp-debug.apk'
call('shell','am','start','-W','-n','se.korkort.study/se.korkort.MainActivity')
path=call('shell','pm','path','se.korkort.study').removeprefix('package:');installed=Path('/tmp/korkort-10k-installed-normal.apk');call('pull',path,str(installed));assert sha(installed)==sha(apk)
aapt=next((Path('/Users/zeyad/Library/Android/sdk/build-tools')).glob('36.0.0/aapt2'))
manifest=subprocess.check_output([str(aapt),'dump','xmltree',str(apk),'--file','AndroidManifest.xml'],text=True);(OUT/'restored-normal-manifest.txt').write_text(manifest);assert 'DeliveryProofActivity' not in manifest
current={key:call('shell','settings','get',ns,key) for ns,key in [('global','wifi_on'),('global','mobile_data'),('system','font_scale'),('secure','enabled_accessibility_services'),('secure','accessibility_enabled')]}
result={'status':'pass' if all(current[k]==original[k] for k in current) else 'settings_restore_mismatch','normal_apk_sha256':sha(apk),'installed_apk_sha256':sha(installed),'proof_activity_in_normal_manifest':False,'original_settings':original,'restored_settings':current,'normal_app_launched':True,'publication':False}
(OUT/'runtime-restored.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
