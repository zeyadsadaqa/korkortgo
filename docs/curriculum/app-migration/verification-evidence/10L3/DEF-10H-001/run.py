import datetime,json,os,subprocess,sys,time
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[5];label=sys.argv[1];cmd=sys.argv[2:];(OUT/'logs').mkdir(exist_ok=True);log=OUT/'logs'/f'{label}.txt';assert not log.exists(),log
env=dict(os.environ,JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home');start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with log.open('w') as f:result=subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
p=OUT/'commands.json';rows=json.loads(p.read_text()) if p.exists() else [];rows.append(dict(argv=cmd,started_utc=start,seconds=round(time.monotonic()-t,2),exit_code=result.returncode,log=str(log.relative_to(OUT))));p.write_text(json.dumps(rows,indent=2)+'\n');print(label,result.returncode);raise SystemExit(result.returncode)
