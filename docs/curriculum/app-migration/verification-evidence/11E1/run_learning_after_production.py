import json,pathlib,subprocess,time
b=pathlib.Path(__file__).resolve().parent;p=b/'normal-android-r6/results.json'
while not p.exists():time.sleep(10)
assert json.loads(p.read_text())['status']=='pass'
raise SystemExit(subprocess.run(['python3',str(b/'run_normal_android.py'),'normal-android-learning-r1','normalLibraryAndReferenceJourneys']).returncode)
