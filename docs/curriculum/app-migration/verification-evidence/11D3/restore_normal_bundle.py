import importlib.util,json,pathlib,shutil,subprocess
r=pathlib.Path.cwd(); proof=pathlib.Path('/tmp/korkort-step11-normal-build'); dest=pathlib.Path('/tmp/korkort-step11-11d3-normal-ios'); sdk=subprocess.check_output(['xcrun','--sdk','iphonesimulator','--show-sdk-version'],text=True).strip()
source=proof/'bin/iosSimulatorArm64/debugFramework/KorkortKit.framework';target=r/('composeApp/build/xcode-frameworks/Debug/iphonesimulator'+sdk+'/KorkortKit.framework')
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,target)
subprocess.run(['xcodebuild','-project','iosApp/Korkort.xcodeproj','-scheme','Korkort','-configuration','Debug','-sdk','iphonesimulator','-destination','id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C','-derivedDataPath',str(dest),'OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED=YES','CODE_SIGNING_ALLOWED=NO','build'],check=True)
resources=proof/'generated/compose/resourceGenerator/assembledResources/iosSimulatorArm64Main/composeResources';app=dest/'Build/Products/Debug-iphonesimulator/Korkort.app';target=app/'compose-resources/composeResources'
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(resources,target)
(r/'docs/curriculum/app-migration/verification-evidence/11D3/normal-bundle-restored.json').write_text(json.dumps({'app':str(app),'framework_source':str(source),'resources':str(resources),'sdk':sdk,'proof_only':False},indent=2)+'\n')
print('Prepared normal simulator bundle',app)
