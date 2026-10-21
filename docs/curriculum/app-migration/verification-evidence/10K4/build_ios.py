"""Build normal or explicitly labelled proof simulator artifacts without altering sources."""
import json,os,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;runner=OUT.parent/'10K1/run_logged.py';mode=sys.argv[1];assert mode in ['normal','proof','restore-normal'];proof=mode=='proof';sdk='iphonesimulator26.5';dest='/tmp/korkort-10k4-'+mode
args=['./gradlew',':composeApp:linkDebugFrameworkIosSimulatorArm64',':composeApp:assembleIosSimulatorArm64MainResources','--offline','--no-daemon','--max-workers=1','-Pkotlin.compiler.execution.strategy=in-process','-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8']+(['-PreferenceProof'] if proof else [])
def run(label,cmd):
 rc=subprocess.run([sys.executable,str(runner),'10K4',label,*cmd],cwd=R).returncode
 if rc:raise SystemExit(rc)
run(mode+'-framework-build',args)
source=R/'composeApp/build/bin/iosSimulatorArm64/debugFramework/KorkortKit.framework';target=R/f'composeApp/build/xcode-frameworks/Debug/{sdk}/KorkortKit.framework'
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,target)
cmd=['xcodebuild','-project','iosApp/Korkort.xcodeproj','-scheme','NativeRouteTests' if proof else 'Korkort','-configuration','Debug','-sdk','iphonesimulator','-destination','id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C','-derivedDataPath',dest,'OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED=YES','CODE_SIGNING_ALLOWED=NO','build-for-testing' if proof else 'build']
run(mode+'-app-build',cmd)
app=Path(dest)/'Build/Products/Debug-iphonesimulator/Korkort.app'
# Explicit CLI override skips Xcode's normal Gradle phase; copy assembled resources.
resources=R/'composeApp/build/generated/compose/resourceGenerator/assembledResources/iosSimulatorArm64Main/composeResources'
if not resources.exists():
 found=list((R/'composeApp/build/generated/compose/resourceGenerator').glob('**/iosSimulatorArm64*/**/composeResources'))
 assert found, 'Find actual assembled simulator resource path before claiming parity'
 resources=found[0]
target=app/'compose-resources/composeResources'
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(resources,target)
if proof:
 import importlib.util
 spec=importlib.util.spec_from_file_location('fixture10K',R/'tools/prepare_native_root_fixture.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 fixture=module.build();(OUT/'accepted-root-fixtures.json').write_text(json.dumps(fixture,ensure_ascii=False,separators=(',',':'))+'\n')
 bundles=list((Path(dest)/'Build/Products/Debug-iphonesimulator').glob('**/NativeRouteTests.xctest'));assert bundles
 shutil.copy2(OUT/'accepted-root-fixtures.json',bundles[0]/'accepted-root-fixtures.json')
(OUT/f'{mode}-bundle.json').write_text(json.dumps({'mode':mode,'app':str(app),'framework':str(source),'resource_source':str(resources),'proof_only':proof,'xcode_kotlin_phase':'Explicitly skipped; prebuilt framework and assembled resources copied as recorded'},indent=2)+'\n')
print(app)
