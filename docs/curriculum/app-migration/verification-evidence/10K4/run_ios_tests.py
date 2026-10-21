import json,plistlib,subprocess,sys
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[4];runner=OUT.parent/'10K1/run_logged.py';build=Path('/tmp/korkort-10k4-proof/Build/Products');source=next(build.glob('*.xctestrun'));data=plistlib.loads(source.read_bytes())
methods=['testAcceptedProductionPracticeAndReview','testLibrarySearchAndSourceReturn','testExactReferenceModalAndCatalogueBack','testUnknownQuestionAndLegacyChooser','testDeliberateAnswerAndNextReading','testPendingCandidateSelectionAndNeutralModal']
# Preserve the generated test host and inject only an explicit test list in the new copy.
def select(node):
 if isinstance(node,dict):
  if 'TestBundlePath' in node:
   node['OnlyTestIdentifiers']=['NativeRouteTests/'+x for x in methods];node['EnvironmentVariables']=dict(node.get('EnvironmentVariables',{}),QUESTION_GROUP='replacements')
  for v in node.values():select(v)
 elif isinstance(node,list):
  for v in node:select(v)
select(data);target=build/'10K4.xctestrun';target.write_bytes(plistlib.dumps(data));(OUT/'selected-tests.json').write_text(json.dumps({'tests':methods,'input_xctestrun':str(source),'selected_xctestrun':str(target),'proof_only':True,'replacement_matrix':'152 contexts require selection visibility repair/retest; initial native run is six routes/owner checks, not a matrix pass','scope':'Fresh native route/accepted owner unscored modal fixture;152 replacement contexts are not run by this command; native descriptions/traits are not VoiceOver listening.'},indent=2)+'\n')
cmd=['xcodebuild','test-without-building','-xctestrun',str(target),'-destination','id=F6E93C4B-958D-4CBB-B95E-537B4FB8070C','-parallel-testing-enabled','NO','-resultBundlePath','/tmp/korkort-10k4-native.xcresult']
raise SystemExit(subprocess.run([sys.executable,str(runner),'10K4','native-tests',*cmd],cwd=R).returncode)
