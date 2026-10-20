"""Run authorized 10B tasks one at a time; retain failures and stop for diagnosis."""
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=Path(__file__).resolve().parent.parent
FILENAMES={1:'opening-parity.json',12:'appendix-parity.json',13:'reference-parity.json',14:'complete-import-parity.json'}
def output(task):
 n=int(task[3:]);return FILENAMES.get(n,f'M{n-1:02d}-parity.json')
def close(task):
 n=int(task[3:]);folder=BASE/task;report=json.loads((folder/output(task)).read_text());assert report['status']=='pass'
 runtime=json.loads((folder/'reader-runtime.json').read_text()) if (folder/'reader-runtime.json').exists() else None
 checks=report['totals']['checks'];blocks=report['totals']['blocks_recursive']
 (folder/'review.md').write_text(f'# {task} — verification review\n\n**20 October 2026 — passed.** {checks} checks pass for the unchanged accepted candidate; {blocks} recursive teaching blocks inspected.\n\n[Detailed parity]({output(task)}) records independent expected and observed content from approved source locators and freshly checked PDF text. [Execution log](commands.json) records this task’s commands.\n\n'+(f'Actual shared `LessonReader` visited all {len(runtime["observations"])} top-level body blocks, checked visible teaching/captions/table cells and deliberately revealed answers. [Reader observations](reader-observations.md), [per-block runtime results](reader-runtime.json).\n\n' if runtime else '')+'This is content/import verification. Cross-platform rendering, accessibility and source currency retain their separately assigned step-10 owners. Historical acceptance receipts and production outputs were not rewritten.\n')
 if runtime:
  (folder/'reader-observations.md').write_text(f'# {task} reader observations\n\nFresh desktop shared CanvasLayersComposeScene; actual production `LessonReader` at 1280×4096 logical pixels, light/default text. All {len(runtime["observations"])} top-level blocks were visited with the real lazy-list scroll action. Every text segment/caption/table cell and knowledge-check answer was found in semantics. Full compiled document objects are independently compared to authoring JSON, whose content is checked against approved origins.\n\nPer-block observations include missing segments and a semantics fingerprint. No missing segment or revealed-answer omission remains. Captures show one final reader position per document; they are supporting observations, not full-platform visual acceptance. Artwork pixels/size/accessibility across targets are deferred to 10D/10K. No speech listening was performed here.\n')
 plan=ROOT/'docs/curriculum/implementation-plan.md';s=plan.read_text()
 marker='#### '+task+'.';start=s.index(marker);end=s.find('\n#### ',start+len(marker));end=len(s) if end<0 else end
 section=s[start:end]
 status=f'**Status — 20 October 2026: Complete.** [{task} verification](app-migration/verification-evidence/{task}/review.md): {checks} checks pass; independent approved-source/PDF/compiled-content parity'+('; actual shared reader content and answer checks pass.' if runtime else '.')+'\n\n'
 if '**Status — 20 October 2026: Complete.**' not in section:
  at=s.index('\n\n',start)+2;s=s[:at]+status+s[at:];plan.write_text(s)
 progress=ROOT/'docs/curriculum/progress.md';s=progress.read_text();s=s.replace(f'| {task} |',f'| {task} |',1)
 import re
 s=re.sub(r'(\| '+task+r' \|[^\n]*?\| )Not started( \|)',r'\g<1>Completed; ['+str(checks)+r' checks pass](app-migration/verification-evidence/'+task+r'/review.md)\2',s)
 entry=f'**20 October — {task} completed:** {checks} independent content/import checks passed; {blocks} recursive blocks accounted for. '+(f'Fresh shared-reader observations cover {len(runtime["observations"])} top-level blocks and answer reveals. ' if runtime else '')+f'[Evidence](app-migration/verification-evidence/{task}/review.md). Continuing within the requested 10B sequence.\n'
 if f'**20 October — {task} completed:**' not in s:s+='\n'+entry
 progress.write_text(s)
 print(f'{task} CLOSED: {checks} checks; {blocks} blocks',flush=True)
def run(task,argv,label):
 folder=BASE/task;folder.mkdir(exist_ok=True);log=folder/(label+'.txt');log.parent.mkdir(parents=True,exist_ok=True)
 attempt=1
 while log.exists():
  attempt+=1;log=folder/(label+f'-run-{attempt:02d}.txt')
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 env=os.environ.copy();env['JAVA_HOME']='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home'
 with log.open('w') as f:p=subprocess.run(argv,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
 record={'argv':argv,'cwd':str(ROOT),'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'log':str(log.relative_to(folder)),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256((BASE/'10B1/verify_10b.py').read_bytes()).hexdigest(),'reader_harness_sha256':hashlib.sha256((BASE/'10B1/ImportVerification10BTest.kt').read_bytes()).hexdigest()}
 path=folder/'commands.json';rows=json.loads(path.read_text()) if path.exists() else [];rows.append(record);path.write_text(json.dumps(rows,indent=2)+'\n')
 print(task,label,p.returncode,flush=True)
 if p.returncode:print(log.read_text()[-8000:],flush=True);sys.exit(p.returncode)
 if label=='reader-gradle':
  xml=ROOT/'composeApp/build/test-results/desktopTest/TEST-se.korkort.ImportVerification10BTest.xml'
  shutil.copy(xml,folder/xml.name)
def main():
 p=argparse.ArgumentParser();p.add_argument('start',type=int);p.add_argument('end',type=int);a=p.parse_args()
 for n in range(a.start,a.end+1):
  task=f'10B{n}';print('START',task,flush=True)
  if n<=12:run(task,['./gradlew',':composeApp:desktopTest','--offline','--no-daemon','--init-script',str((BASE/'10B1/jvm-test-init.gradle').relative_to(ROOT)),f'-PverificationTask={task}','--tests','se.korkort.ImportVerification10BTest'],'reader-gradle')
  run(task,['python3',str((BASE/'10B1/verify_10b.py').relative_to(ROOT)),task],'audit-run')
  close(task)
if __name__=='__main__':main()
