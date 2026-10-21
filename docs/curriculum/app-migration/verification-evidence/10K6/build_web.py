import hashlib,json,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;runner=OUT.parent/'10K1/run_logged.py';mode=sys.argv[1];assert mode in ['normal','proof','restore-normal'];proof=mode=='proof'
task=':composeApp:wasmJsBrowserDevelopmentExecutableDistribution' if proof else ':composeApp:wasmJsBrowserDistribution'
cmd=['./gradlew',task,'--offline','--no-daemon','--max-workers=1','-Pkotlin.compiler.execution.strategy=in-process','-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8']+(['-PreferenceProof'] if proof else [])
rc=subprocess.run([sys.executable,str(runner),'10K6',mode+'-web-build',*cmd],cwd=R).returncode
if rc:raise SystemExit(rc)
source=R/('composeApp/build/dist/wasmJs/developmentExecutable' if proof else 'composeApp/build/dist/wasmJs/productionExecutable');target=Path('/tmp/korkort-10k6-'+mode);assert source.exists()
if target.exists():raise AssertionError('Retain prior distribution: choose a new run path')
shutil.copytree(source,target)
files=[{'path':str(p.relative_to(target)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(target.rglob('*')) if p.is_file()]
(OUT/f'{mode}-distribution.json').write_text(json.dumps({'mode':mode,'source':str(source.relative_to(R)),'served_copy':str(target),'proof_only':proof,'files':files,'policy':'Serve entire current distribution from a new localhost origin; proof resources/executable remain labelled and are not release artifacts.'},indent=2)+'\n');print(target)
