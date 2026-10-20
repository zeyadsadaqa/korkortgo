"""Execute 10B14 only after successful 10B1–10B13 prerequisites."""
import json,sys
from pathlib import Path
import run_sequence as r
for n in range(1,14):
 task=f'10B{n}';report=json.loads((r.BASE/task/r.output(task)).read_text());assert report['status']=='pass',task
out=r.BASE/'10B14';out.mkdir(exist_ok=True)
commands=[['python3','tools/import_curriculum_remaining.py','--check'],['python3','tools/build_navigation.py','--check'],['python3','tools/build_reader.py','--check'],['python3','tools/assemble_question_package_9j.py','--check'],['python3','tools/review_question_delivery_9j.py','--check'],['python3','tools/finalize_question_package_9j.py','--check']]
for i,argv in enumerate(commands,1):r.run('10B14',argv,'logs/'+str(i).zfill(2)+'-'+Path(argv[1]).stem)
rows=json.loads((out/'commands.json').read_text());(out/'generation-commands.json').write_text(json.dumps(rows,indent=2)+'\n')
r.run('10B14',['python3','docs/curriculum/app-migration/verification-evidence/10B1/verify_10b.py','10B14'],'audit-run')
r.run('10B14',['python3','docs/curriculum/app-migration/verification-evidence/10B1/verify_closure.py'],'closure-run')
r.close('10B14')
