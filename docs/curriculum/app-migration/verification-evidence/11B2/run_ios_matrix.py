import json,os,pathlib,plistlib,subprocess,sys
root=pathlib.Path.cwd();task,name,count=sys.argv[1:];out=root/'docs/curriculum/app-migration/verification-evidence'/task/name;out.mkdir(parents=True,exist_ok=False)
build=pathlib.Path('/tmp/korkort-step11-ios/Build/Products');source=next(build.glob('*.xctestrun'));data=plistlib.loads(source.read_bytes());questions=json.loads((root/'docs/curriculum/app-migration/verification-evidence/11B2/current-replacements.json').read_text())
def select(n):
 if isinstance(n,dict):
  if 'TestBundlePath' in n:
   n['OnlyTestIdentifiers']=['NativeRouteTests/testHeldQuestionNativeDeliveryMatrix']
   n['EnvironmentVariables']=dict(n.get('EnvironmentVariables',{}),QUESTION_GROUP='accepted-replacements',QUESTION_COUNT=count,CURRENT_QUESTIONS_JSON=json.dumps(questions,separators=(',',':')))
   n['EnvironmentVariables'].update({k:os.environ[k] for k in ['QUESTION_START','MATRIX_DARK','MATRIX_SCALE'] if k in os.environ})
  for v in n.values():select(v)
 elif isinstance(n,list):
  for v in n:select(v)
select(data);target=build/(name+'.xctestrun');target.write_bytes(plistlib.dumps(data));(out/'selected-xctestrun.plist').write_bytes(plistlib.dumps(data))
resultbundle='/tmp/korkort-step11-'+name+'.xcresult'
command=['xcodebuild','test-without-building','-xctestrun',str(target),'-destination','id='+os.environ.get('MATRIX_DEVICE','F6E93C4B-958D-4CBB-B95E-537B4FB8070C'),'-parallel-testing-enabled','NO','-resultBundlePath',resultbundle]
result=subprocess.run(command)
summary=json.loads(subprocess.check_output(['xcrun','xcresulttool','get','test-results','summary','--path',resultbundle]));(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
subprocess.run(['xcrun','xcresulttool','export','attachments','--path',resultbundle,'--output-path',str(out/'attachments')],check=True)
print('iOS summary',summary)
assert result.returncode==0 and summary['totalTestCount']==1 and summary['failedTests']==0
