import importlib.util,json,pathlib,shutil,subprocess
r=pathlib.Path.cwd(); proof=pathlib.Path('/tmp/korkort-step11-proof-build'); dest=pathlib.Path('/tmp/korkort-step11-ios'); sdk=subprocess.check_output(['xcrun','--sdk','iphonesimulator','--show-sdk-version'],text=True).strip()
source=proof/'bin/iosSimulatorArm64/debugFramework/KorkortKit.framework';target=r/('composeApp/build/xcode-frameworks/Debug/iphonesimulator'+sdk+'/KorkortKit.framework')
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,target)
subprocess.run(['xcodebuild','-project','iosApp/Korkort.xcodeproj','-scheme','NativeRouteTests','-configuration','Debug','-sdk','iphonesimulator','-destination','id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C','-derivedDataPath',str(dest),'OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED=YES','CODE_SIGNING_ALLOWED=NO','build-for-testing'],check=True)
resources=proof/'generated/compose/resourceGenerator/assembledResources/iosSimulatorArm64Main/composeResources';app=dest/'Build/Products/Debug-iphonesimulator/Korkort.app';target=app/'compose-resources/composeResources'
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(resources,target)
spec=importlib.util.spec_from_file_location('fixtures',r/'tools/prepare_native_root_fixture.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);fixture=module.build()
bundle=next((dest/'Build/Products/Debug-iphonesimulator').glob('**/NativeRouteTests.xctest'));(bundle/'accepted-root-fixtures.json').write_text(json.dumps(fixture,separators=(',',':'))+'\n')
(r/'docs/curriculum/app-migration/verification-evidence/11B2/ios-bundle.json').write_text(json.dumps({'app':str(app),'framework_source':str(source),'resources':str(resources),'sdk':sdk,'proof_only':True},indent=2)+'\n')
print('Prepared simulator test bundle',app)
