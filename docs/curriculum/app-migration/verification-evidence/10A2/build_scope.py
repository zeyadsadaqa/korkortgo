"""Build the required-check matrix from recorded environment observations; no app tests."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
BASE=OUT.parent

def read(p):return json.loads((ROOT/p).read_text())
def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def binding(p):return {'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}
assert json.loads((BASE/'10A1/results.json').read_text())['status']=='pass'
commands=json.loads((OUT/'environment-commands.json').read_text())
cmds={r['id']:r for r in commands}
for id in ['host','python','jdk','xcode','sdk','simulators-host','adb-host','android-sdk','gradle','android-target','android-size','android-density','android-talkback-package']:
    assert cmds[id]['exit_code']==0,id
simdata=json.loads((OUT/'simulators-host.txt').read_text())
simulator=next(dict(d,runtime=runtime) for runtime,devices in simdata['devices'].items() for d in devices if d['udid']=='F6E93C4B-958D-4CBB-B95E-537B4FB8070C')
assert simulator['isAvailable']
assert 'emulator-5554' in (OUT/'adb-host.txt').read_text()
browser={'tool':'cua.getState()','observation_date':'2026-10-20','result':'ChatGPT in-app browser is available; provider id 2, type iab, zero tabs. No tab created or app loaded.','status':'available','privacy':'Unrelated application/tab inventory omitted.'}
dump('browser-readiness.json',browser)
policy=read('content/delivery-targets.json')
assert policy['ios_scope']=='simulator'
scopes=[]

def row(target,dimension,method,oracle,availability='available',requirement='required',reason=None):
    scopes.append({'id':f'SCOPE-{target}-{dimension}','target':target,'dimension':dimension,'requirement':requirement,'availability':availability,'execution_status':'not_run' if requirement=='required' else 'excluded_by_policy','method':method,'expected_evidence':oracle,'basis':reason or f'10A2/10K scope; retained 9O platform boundary for {target}','owner':{'common':'10K1','android':'10K2','desktop':'10K3','ios_simulator':'10K4','ios_device':'10K5','wasm_js':'10K6'}[target]})
for target in ['common','android','desktop','ios_simulator','ios_device','wasm_js']:
    available='available_requires_boot' if target=='ios_simulator' else 'available'
    row(target,'build',{'common':'Python checks and forced fresh desktopTest, six --check generation commands','android':'assembleDebug normal APK; labelled native proof build when needed','desktop':'desktopJar and desktopTest; configured library/Compose harness','ios_simulator':'normal iosSimulatorArm64 framework and shared Korkort Xcode scheme; labelled native proof build','ios_device':'normal iosArm64 framework and device resource aggregation; platform/ARM64 metadata','wasm_js':'wasmJsBrowserDistribution normal production executable'}[target],'Commands, versions, exit codes, build identity; successful compilation is not runtime acceptance.',available)
    row(target,'packaged_bytes','Compare all manifest asset bindings, fonts and both licences in target output; common checks repository/compiled parity.','484 binding outcomes / 419 distinct artwork files; four fonts and two licences; exact source and package hashes.',available)
    if target in ('common','ios_device'):
        for dimension in ['runtime','offline_delivery','external_links','visual_legibility','keyboard','semantics_focus','screen_reader_listening']:
            reason='Physical runtime/signing/install/VoiceOver excluded by content/delivery-targets.json and 9O6; build/resource checks remain required.' if target=='ios_device' else 'Common is data/model/integration checks; surface execution is explicitly owned by configured platform rows, not omitted.'
            row(target,dimension,'See required platform rows; no independent surface for this row.','Explicit non-pass scope record.',requirement='excluded_by_policy',availability='not_applicable_existing_scope',reason=reason)
        continue
    row(target,'runtime','Real accepted-bank production feedback/review/reader/library/reference/recovery flows; desktop uses labelled fixture UI plus separate full-bank model/parity execution.','Normal root identity, expected/observed cases, captures, no fixture-as-production claim.',available)
    row(target,'offline_delivery',{'android':'Temporarily disable emulator Wi-Fi/data; local teaching/images/fonts and source failure; record and restore connectivity.','desktop':'Load from packaged local classpath; mock unreachable external URI handler. No host-wide network-isolation claim.','ios_simulator':'Verify bundle-local teaching/assets and explicit offline/unreachable failure fixtures. Do not disable host networking or call local resources a network-isolated run.','wasm_js':'Serve complete distribution at fresh localhost origin; isolate external-source failure while host remains reachable. No unsupported cold-offline reload guarantee.'}[target],'Local resource identity/observed use, documented network conditions and external failure handling.',available)
    row(target,'external_links','Invoke actual Open source callback and verify external destination plus return; simulate unreachable external source. Desktop verifies exact URI dispatch with a mocked URI handler because no desktop launcher is configured.','Exact URL/publisher/scope, launch/dispatch versus website availability distinguished, retained source/review context.',available)
    row(target,'visual_legibility','Fresh 38-replacement/faint-artwork and representative production/teaching matrix: light/dark × text 1.0/1.6; fit/zoom/scroll/return.','Full-question inline evidence, actual viewport/image bounds, fine-stroke/code/variant correspondence; 220 dp frame requirement; no source-art alteration.',available)
    row(target,'keyboard','Tab/Shift-Tab, activation, Escape or supported dismiss, zoom/reset/close and focus return. Desktop/browser use real key events; native uses supported keyboard/input bridge and records unavailable controls.','Per-control focus/activation observations and preserved selection; unsupported required input becomes a blocker.',available)
    row(target,'semantics_focus','Inspect neutral pre-answer descriptions, selection/feedback, answer reveal, focus/order, modal background exclusion and return. iOS audits description/trait separately from announcement/listening.','Native nodes/Compose semantics/browser AX; before/after snapshots and expected accessible labels.',available)
    if target=='android':
        row(target,'screen_reader_listening','Fresh representative TalkBack traversal, selection, modal/return and feedback; capture observation separately from instrumentation.','Observed spoken/navigation behaviour on emulator; original service setting restored; prior recording is supporting evidence only.','available_requires_enable_and_restore',reason='T03 supported assistive interaction; TalkBack package exists, service currently disabled (null).')
    else:
        row(target,'screen_reader_listening','No listening pass claimed; execute required semantics/focus row.','Explicit exclusion; no fabricated speech or native bridge evidence.',requirement='excluded_by_policy',availability='not_applicable_existing_scope',reason={'desktop':'Configured harness has no native desktop accessibility bridge/launcher (9O4).','ios_simulator':'Existing simulator scope records description/trait audit only; no VoiceOver listening or physical device claim (9O5/9O6).','wasm_js':'Existing one-browser scope excludes screen-reader listening/cross-engine certification (9O7).'}[target])
state=read('docs/curriculum/app-migration/link-and-progress-map.json')['state_rules']
conditional=[{'id':f'7E-STATE-{i+1:02d}','field':r['field'],'status':'conditional_future_scope','reason':r['migration_rule']} for i,r in enumerate(state) if r['baseline'].startswith('no implementation')]
assert len(conditional)==4
basis=['content/delivery-targets.json','composeApp/build.gradle.kts','docs/curriculum/app-design-spec.md','docs/curriculum/app-design/faint-assets-v1/review.md']+[f'docs/curriculum/app-migration/implementation-evidence/9O{i}/README.md' for i in [3,4,5,7]]+['docs/curriculum/app-migration/implementation-evidence/9O6/results.json']
matrix={'schema_version':1,'task':'10A2','date':'2026-10-20','candidate':json.loads((BASE/'10A1/results.json').read_text())['candidate'],'policy':policy,'basis':[binding(p) for p in basis],
'environment':{'host':'macOS 26.3 (25D125), arm64','python':'3.14.7','jdk':'Microsoft OpenJDK 17.0.16','gradle':'8.14.3','xcode':'26.6 (17F113)','ios_sdk':'26.5','android_sdk':'API 36; Build Tools 36.0.0; adb 37.0.1','android_target':'emulator-5554, API 36, running; 1280x2856 physical pixels, density override 408 dpi; logical size must be measured per fresh run','ios_simulator':{k:simulator[k] for k in ['name','udid','state','isAvailable','runtime']},'browser':browser},
'rows':scopes,'conditional_state_contracts':conditional,'required_unavailable_checks':[],
'viewport_policy':{'authority':'docs/curriculum/app-design-spec.md:61','interpretation':'Approved preview widths are conceptual, not minimum supported sizes or fixed breakpoints. Do not label 390 px as an approved minimum.','replay_baseline':'390x844 logical shared/browser viewport, plus actual native target dimensions; measure and record effective viewport, density, image bounds and insets.','narrow_reflow_probe':'320 logical-pixel width diagnostic in shared/browser runtime, plus 1280-wide desktop/library check. This is test coverage, not a new breakpoint/design approval.','artwork_minimum':'Approved assessment/lesson/review frame height at least 220 dp; wide-reference minimum 380 dp. Equal option sizing and unchanged aspect/white backing; verify actual bounds at target width.','text_and_themes':'light/dark x 1.0/1.6 font scale; never widen viewport or shrink body text to hide overflow.'},
'fresh_runtime_tests_executed':False,'scope_changes':[]}
dump('scope-matrix.json',matrix)
checks=[{'id':'10A2-ENV','status':'pass','expected':'required toolchains and runtime targets available or bootable','observed':'recorded versions; running Android emulator; original iOS simulator available/shutdown; IAB available','evidence':'environment-commands.json'}, {'id':'10A2-SCOPE','status':'pass','expected':54,'observed':len(scopes),'evidence':'scope-matrix.json#/rows'}, {'id':'10A2-POLICY','status':'pass','expected':'simulator-only iOS plus configured harness/static web','observed':'preserved without scope mutation','evidence':'scope-matrix.json#/basis'}, {'id':'10A2-CONDITIONAL','status':'pass','expected':4,'observed':len(conditional),'evidence':'scope-matrix.json#/conditional_state_contracts'}, {'id':'10A2-UNAVAILABLE','status':'pass','expected':0,'observed':0,'evidence':'scope-matrix.json#/required_unavailable_checks'}]
assert len(scopes)==54
assert all(r['execution_status']!='pass' for r in scopes)
dump('results.json',{'task':'10A2','status':'pass','candidate':matrix['candidate'],'checks':checks,'rows':len(scopes),'required_rows':sum(r['requirement']=='required' for r in scopes),'excluded_rows':sum(r['requirement']=='excluded_by_policy' for r in scopes),'conditional_future_cases':4,'runtime_passes_claimed':0,'sandbox_retry':'Initial simctl/adb service queries failed under sandbox; host-permitted read-only retries succeeded. Both phases retained.','readiness_limits':'iOS simulator must be booted at execution; TalkBack currently disabled and requires scoped enable/restore; browser app/build and external callbacks are not yet exercised.'})
print(json.dumps({'rows':len(scopes),'required':sum(r['requirement']=='required' for r in scopes),'excluded':sum(r['requirement']=='excluded_by_policy' for r in scopes),'conditional':len(conditional)}))
