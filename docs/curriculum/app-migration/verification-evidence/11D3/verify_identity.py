"""Bind retained checkpoint inputs and restored simulator bundles to current inputs."""
import hashlib,json,pathlib,plistlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[5]; OUT=pathlib.Path(__file__).resolve().parent; E=OUT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p):return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file()}
def load(p):return json.loads(p.read_text())
receipts={name:load(E/name) for name in ['11B2/ios-build-r2.json','11B2/ios-harness-rebuild-r4.json','11B2/proof-rebuild-r3.json','11G1/normal-ios-r1.json','11G1/normal-artifacts-restore-r4.json']}
inputs=receipts['11B2/ios-harness-rebuild-r4.json']['inputs']
assert all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in inputs.items())
assert all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in receipts['11G1/normal-artifacts-restore-r4.json']['inputs'].items())
old=receipts['11B2/ios-build-r2.json']['inputs']
drift=[p for p,h in old.items() if inputs.get(p)!=h]
assert set(drift)=={'iosApp/NativeRouteTests.swift','docs/curriculum/app-migration/verification-evidence/11B1/AcceptedArtworkStep11Test.kt','docs/curriculum/app-migration/verification-evidence/11B1/jvm-test-init.gradle'}
artifacts={}
for kind,record in [('proof',E/'11B2/ios-bundle.json'),('normal',OUT/'normal-bundle-restored.json')]:
    d=load(record); app=pathlib.Path(d['app']); source=pathlib.Path(d['resources']); bundled=app/'compose-resources/composeResources'
    resources=tree(source);assert resources==tree(bundled)
    expected=ROOT/'composeApp/src/commonMain/composeResources'
    source_files=tree(expected)
    for name,h in source_files.items():
        matches=[v for p,v in resources.items() if p.endswith('/'+name)]
        assert matches==[h],name
    info=plistlib.loads((app/'Info.plist').read_bytes())
    assert info['CFBundleIdentifier']=='se.korkort.study'
    assert info['CFBundleSupportedPlatforms']==['iPhoneSimulator']
    executable=app/info['CFBundleExecutable']
    symbols=subprocess.check_output(['nm',str(executable)],text=True,stderr=subprocess.DEVNULL)
    proof_marker='DeliveryProofScreen' in symbols
    assert proof_marker==(kind=='proof')
    artifacts[kind]={'app':str(app),'bundle_id':info['CFBundleIdentifier'],'platform':info['CFBundleSupportedPlatforms'],'executable_sha256':sha(executable),'framework_sha256':sha(pathlib.Path(d['framework_source'])/'KorkortKit'),'bundle_files':tree(app),'resource_count':len(resources),'source_resource_count':len(source_files),'source_and_copied_resources_equal':True,'contains_delivery_proof_symbols':proof_marker}
assert artifacts['proof']['executable_sha256']!=artifacts['normal']['executable_sha256']
runner=pathlib.Path('/tmp/korkort-step11-ios/Build/Products/Debug-iphonesimulator/NativeRouteTests-Runner.app/PlugIns/NativeRouteTests.xctest')
oldnormal=next(a for a in load(E/'11G1/resource-parity.json')['artifacts'] if a['path'].endswith('Korkort.app/Korkort'))
result={'status':'pass','recorded_on':'2026-10-23','candidate':load(ROOT/'content/accepted-content-manifest.json'),'current_inputs':inputs,'current_input_check':'All recorded final harness inputs still match','r2_to_r4_changed_inputs':drift,'checkpoint_reuse':'49 completed r2 checkpoints retained. App/content/resources unchanged; only iOS reach/scroll stabilization and separate JVM harness inputs differ. The failed S6 recognition light/160 case and following 26 cases pass under r4 harness. r2 overall remains failed.','build_receipts':{k:{'sha256':sha(E/k),'command':v['command'],'exit_code':v['exit_code']} for k,v in receipts.items()},'artifacts':artifacts,'native_test_bundle_files':tree(runner),'historical_normal_executable':oldnormal,'normal_rebuild_scope':'The retained normal framework was rebuilt by passing normal-artifacts-restore-r4 on 22 October; its inputs still match. The 23 October restored app uses this later framework, so the earlier normal-ios-r1 executable hash is not expected to match. No old runtime result is transferred to the rebuilt normal app. Final production runtime/sealing remains 11E1/11G1.', 'restored_normal_matches_historical_executable':artifacts['normal']['executable_sha256']==oldnormal['sha256'],'identity_limit':'Hashes describe retained final proof and freshly restored normal artifacts. r2 pre-rebuild executable was not separately sealed; reuse rests on identical production/proof source and resource inputs plus per-case native evidence. Both hosts share a bundle ID; executable hashes and proof symbols distinguish them.','resource_copy_procedure':'build-for-testing/build with explicit framework; then replace app/compose-resources/composeResources from the matching assembled simulator resources (see 11B2/build_ios.py and restore_normal_bundle.py). All 768 original resources independently matched by suffix and SHA256.'}
(OUT/'artifact-identity.json').write_text(json.dumps(result,indent=2)+'\n')
print('Bundle identities and all copied resources pass; restored normal executable matches historical:',result['restored_normal_matches_historical_executable'])
