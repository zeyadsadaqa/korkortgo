import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];runner=Path(__file__).parent.parent/'10K1/run_logged.py'
cmd=['./gradlew',':composeApp:linkDebugFrameworkIosArm64',':composeApp:assembleIosArm64MainResources','--offline','--no-daemon','--max-workers=1','-Pkotlin.compiler.execution.strategy=in-process','-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8']
raise SystemExit(subprocess.run([sys.executable,str(runner),'10K5','normal-device-framework',*cmd],cwd=R).returncode)
