"""Run one target command with a fresh log and retained argv/exit/time record."""
import datetime,json,os,subprocess,sys,time
from pathlib import Path
args=sys.argv[1:];task,label=args[:2];cmd=args[2:];R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent.parent/task;OUT.mkdir(exist_ok=True);(OUT/'logs').mkdir(exist_ok=True)
log=OUT/'logs'/f'{label}.txt';assert not log.exists(),f'Retain prior receipt: choose a new label, {log}'
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();env=dict(os.environ,JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home')
print('RUN',task,label,flush=True)
with log.open('w') as f:result=subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
index=OUT/'commands.json';rows=json.loads(index.read_text()) if index.exists() else [];rows.append({'argv':cmd,'JAVA_HOME':env['JAVA_HOME'],'started_utc':start,'duration_seconds':round(time.monotonic()-t,2),'exit_code':result.returncode,'log':str(log.relative_to(OUT))});index.write_text(json.dumps(rows,indent=2)+'\n');print('RESULT',result.returncode,flush=True);raise SystemExit(result.returncode)
