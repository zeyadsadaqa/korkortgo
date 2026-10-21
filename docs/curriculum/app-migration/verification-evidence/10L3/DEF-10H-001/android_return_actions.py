"""One native touch retest; first tap is grounded in the saved inspected1440x3120 screenshot."""
import json,re,subprocess
from pathlib import Path
OUT=Path(__file__).parent;adb=['/Users/zeyad/Library/Android/sdk/platform-tools/adb','-s','emulator-5554'];actions=[]
def layout(name):
 p=OUT/(name+'.json');subprocess.run(['/usr/local/bin/android','layout','--device','emulator-5554','--pretty','-o',str(p)],check=True,stdout=subprocess.DEVNULL);return json.loads(p.read_text())
def tap(x,y):subprocess.run(adb+['shell','input','tap',str(x),str(y)],check=True);actions.append({'tap':[x,y]})
def button(rows,label):
 row=next(r for r in rows if r.get('text')==label);return [int(x) for x in re.findall(r'\d+',row['center'])]
tap(500,2526);sign=layout('android-after-sign');assert any(r.get('text')=='Give way' for r in sign)
tap(*button(sign,'‹ Road signs and reference'));catalogue=layout('android-after-catalogue');assert any(r.get('text')=='Road signs and signals' for r in catalogue)
tap(*button(catalogue,'Return to reading'));returned=layout('android-after-return');texts=[r.get('text','') for r in returned];passed=any(t.startswith('Requirements. B1') for t in texts) and 'Road signs and signals' not in texts
(OUT/'android-route-result.json').write_text(json.dumps({'status':'pass' if passed else 'fail','proof_only':True,'actual_native_touch_actions':actions,'observed':['B1 sign detail','catalogue Return to reading','original B1 teaching passage restored'],'scope':'One actual native Android route; broader font/theme/TalkBack matrix remains open.'},indent=2)+'\n');assert passed;print('Android actual native reader→sign→catalogue→passage: PASS')
