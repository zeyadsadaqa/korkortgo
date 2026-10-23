import json,os,pathlib,subprocess,time
b=pathlib.Path(__file__).resolve().parent
p=b/'ios-light-large-resume-r3/summary.json'
while not p.exists():time.sleep(10)
s=json.loads(p.read_text());assert s['failedTests']==0 and s['totalTestCount']==1,s
# Wait for the attachment exporter as well; its summary appears first.
while not (b/'ios-light-large-resume-r3/attachments/manifest.json').exists():time.sleep(5)
env=dict(os.environ,MATRIX_DARK='true',MATRIX_SCALE='1.6');result=subprocess.run(['python3',str(b.parent/'11B2/run_ios_matrix.py'),'11D3','ios-dark-large-r3','38'],env=env);raise SystemExit(result.returncode)
