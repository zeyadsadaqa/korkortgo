import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];runner=R/'docs/curriculum/app-migration/verification-evidence/10K1/run_logged.py'
assert json.loads((runner.parent/'common-results.json').read_text())['status']=='pass_common_checks'
cmd=['./gradlew',':composeApp:assembleDebug','--rerun-tasks','--offline','--no-daemon','--max-workers=1','-Pkotlin.compiler.execution.strategy=in-process','-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8']
raise SystemExit(subprocess.run([sys.executable,str(runner),'10K2','normal-apk-build',*cmd],cwd=R).returncode)
