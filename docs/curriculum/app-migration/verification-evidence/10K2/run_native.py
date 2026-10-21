"""Fresh isolated Android proof runs; retain each phase and restore initial connectivity."""
import hashlib,json,subprocess,sys,shlex
from pathlib import Path
R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;adb='/Users/zeyad/Library/Android/sdk/platform-tools/adb';device='emulator-5554';runner=OUT.parent/'10K1/run_logged.py'
def call(*args,check=True,raw=False):
 r=subprocess.run([adb,'-s',device,*args],capture_output=True,check=check);return r.stdout if raw else r.stdout.decode().strip()
def logged(label,cmd):return subprocess.run([sys.executable,str(runner),'10K2',label,*cmd],cwd=R).returncode
settings={k:call('shell','settings','get',namespace,k) for namespace,k in [('global','wifi_on'),('global','mobile_data'),('secure','enabled_accessibility_services'),('secure','accessibility_enabled'),('system','font_scale')]}
(OUT/'initial-device-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
methods=['librarySearchSurvivesLessonAndNativeSourceReturn','unknownQuestionAndLegacyChooserNeverGuessReading','referenceBackAndNativeModalPreserveContext','pendingCandidateSelectionSurvivesNativeZoom','nativeKnowledgeCheckRevealAndReadingNeighbours','productionPracticeAndReviewUseAcceptedPackage','heldQuestionNativeDeliveryMatrix']
rows=[]
try:
 call('shell','svc','wifi','disable');call('shell','svc','data','disable')
 for method in methods:
  call('shell','run-as','se.korkort.study.verification','rm','-rf','files/native-reader-step1',check=False)
  extras=['-e','questionGroup','replacements','-e','captureAll','true'] if method=='heldQuestionNativeDeliveryMatrix' else []
  cmd=[adb,'-s',device,'shell','am','instrument','-w','-r','-e','class','se.korkort.NativeReaderRouteTest#'+method,*extras,'se.korkort.study.verification.test/androidx.test.runner.AndroidJUnitRunner']
  logged(method,cmd)
  text=(OUT/'logs'/f'{method}.txt').read_text();dest=OUT/'native-evidence'/method;dest.mkdir(parents=True,exist_ok=True)
  listing=call('shell','run-as','se.korkort.study.verification','ls','files/native-reader-step1',check=False).splitlines()
  for name in listing:
   if '/' not in name and name.endswith(('.json','.png')):(dest/name).write_bytes(call('exec-out','run-as','se.korkort.study.verification','cat',shlex.quote('files/native-reader-step1/'+name),raw=True))
  passed='OK (' in text and 'FAILURES!!!' not in text and 'INSTRUMENTATION_FAILED' not in text
  rows.append({'method':method,'status':'pass' if passed else 'fail','log':'logs/'+method+'.txt','evidence':str(dest.relative_to(OUT)),'scope':'actual accepted production owner for production method; explicit unscored/route proof fixtures otherwise'})
  (OUT/'native-results.json').write_text(json.dumps({'cases':rows,'proof_only':True,'normal_build_matrix':'Separate normal offline launch; these proof runs do not close normal-build matrix cases.','connectivity':'wifi/data disabled throughout native phase; source pages not expected online','all_pass':all(x['status']=='pass' for x in rows)},indent=2)+'\n');print('METHOD',method,rows[-1]['status'],flush=True)
finally:
 for key,service in [('wifi_on','wifi'),('mobile_data','data')]:call('shell','svc',service,'enable' if settings[key]=='1' else 'disable',check=False)
 restored={key:call('shell','settings','get','global',key) for key in ['wifi_on','mobile_data']}
 (OUT/'connectivity-restored.json').write_text(json.dumps({'before':settings,'after':restored,'restored':all(restored[k]==settings[k] for k in restored)},indent=2)+'\n')
