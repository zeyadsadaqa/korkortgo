import hashlib,json,shutil,subprocess,sys
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[5];mode=sys.argv[1];assert mode in ['proof','normal'];dest=Path('/tmp/korkort-10l-h001-ios-'+mode);sdk='iphonesimulator26.5'
source=R/'composeApp/build/bin/iosSimulatorArm64/debugFramework/KorkortKit.framework';target=R/f'composeApp/build/xcode-frameworks/Debug/{sdk}/KorkortKit.framework'
if target.exists():shutil.rmtree(target)
target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,target)
cmd=['xcodebuild','-project','iosApp/Korkort.xcodeproj','-scheme','Korkort','-configuration','Debug','-sdk','iphonesimulator','-destination','id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C','-derivedDataPath',str(dest),'OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED=YES','CODE_SIGNING_ALLOWED=NO','build']
subprocess.run([sys.executable,str(OUT/'run.py'),mode+'-ios-app',*cmd],check=True,cwd=R)
app=dest/'Build/Products/Debug-iphonesimulator/Korkort.app';resources=R/'composeApp/build/generated/compose/resourceGenerator/assembledResources/iosSimulatorArm64Main/composeResources';target=app/'compose-resources/composeResources';target.parent.mkdir(exist_ok=True)
if target.exists():shutil.rmtree(target)
shutil.copytree(resources,target)
(OUT/(mode+'-ios-bundle.json')).write_text(json.dumps({'mode':mode,'proof_only':mode=='proof','app':str(app),'executable_sha256':hashlib.sha256((app/'Korkort').read_bytes()).hexdigest(),'resources_manually_copied_after_explicit_Xcode_Gradle_override':True},indent=2)+'\n');print(app)
