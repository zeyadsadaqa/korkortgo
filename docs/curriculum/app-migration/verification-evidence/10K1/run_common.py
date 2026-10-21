"""Run fresh common checks without overwriting historical evidence receipts."""
import datetime,json,os,platform,shutil,subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[4]
java='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home'
commands=[['python3',f'tools/{tool}.py','--check'] for tool in ['import_curriculum_remaining','build_navigation','build_reader','assemble_question_package_9j','review_question_delivery_9j','finalize_question_package_9j']]
commands += [['python3','-m','unittest','discover','-s','tools','-p','test_*.py'],['./gradlew',':composeApp:desktopTest','--rerun-tasks','--offline','--no-daemon','--max-workers=1','-Pkotlin.compiler.execution.strategy=in-process','-Dorg.gradle.jvmargs=-Xmx6g -Dfile.encoding=UTF-8']]
rows=[];env=dict(os.environ,JAVA_HOME=java)
for n,cmd in enumerate(commands,1):
 name=f'{n:02d}-'+(Path(cmd[1]).stem if n<=6 else 'python-unittest' if n==7 else 'fresh-desktop-tests')+'.txt'
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();begin=time.monotonic();print('RUN',n,' '.join(cmd),flush=True)
 with (OUT/'logs'/name).open('w') as f:
  result=subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 rows.append({'argv':cmd,'environment':{'JAVA_HOME':java},'started_utc':start,'duration_seconds':round(time.monotonic()-begin,2),'exit_code':result.returncode,'log':'logs/'+name,'status':'pass' if result.returncode==0 else 'fail'})
 (OUT/'commands.json').write_text(json.dumps(rows,indent=2)+'\n');print('RESULT',n,result.returncode,flush=True)
suites=[]
for p in sorted((R/'composeApp/build/test-results/desktopTest').glob('TEST-*.xml')):
 shutil.copy2(p,OUT/'test-reports'/p.name);e=ET.parse(p).getroot();suites.append({k:e.get(k) for k in ['name','tests','failures','errors','skipped','timestamp']})
result={'task':'10K1','status':'pass_common_checks' if all(x['exit_code']==0 for x in rows) else 'required_common_check_failed','candidate_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'host':platform.platform(),'python':platform.python_version(),'jvm_suites':suites,'jvm_totals':{k:sum(int(x[k] or 0) for x in suites) for k in ['tests','failures','errors','skipped']},'forced_fresh':True,'gradle_cache_policy':'--rerun-tasks forces execution; dependency resolution offline from existing cache','historical_vs_accepted':'Assembler historical384 accepted/616 held; finalizer production1000 accepted/zeroheld. No historical receipt rewritten.'}
(OUT/'common-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
