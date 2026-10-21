import argparse,json,shlex,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--folder',default='native-10k-additional');p.add_argument('--output',required=True);p.add_argument('--prefix',default='');a=p.parse_args();OUT=Path(__file__).parent/'native-evidence'/a.output;OUT.mkdir(parents=True,exist_ok=True)
cmd=['/Users/zeyad/Library/Android/sdk/platform-tools/adb','-s','emulator-5554'];folder='files/'+a.folder;names=subprocess.check_output(cmd+['shell','run-as','se.korkort.study.verification','ls',folder],text=True).splitlines();saved=[]
for name in names:
 if '/' not in name and name.endswith(('.png','.json')) and (not a.prefix or name.startswith(a.prefix) or name=='signal-actions.json'):
  data=subprocess.check_output(cmd+['exec-out','run-as','se.korkort.study.verification','cat',shlex.quote(folder+'/'+name)]);(OUT/name).write_bytes(data);saved.append(name)
(OUT/'collected-files.json').write_text(json.dumps({'device_folder':folder,'prefix':a.prefix,'files':saved,'scope':'Copied named current device outputs; no claim that an old failure file is freshly emitted by a later retry.'},indent=2)+'\n');print(len(saved),'files collected to',OUT)
