import hashlib,json,shutil,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[4];reports=OUT/'test-reports';reports.mkdir(exist_ok=True);suites=[]
for f in sorted((R/'composeApp/build/test-results/desktopTest').glob('TEST-*.xml')):
 shutil.copy2(f,reports/f.name);e=ET.parse(f).getroot();suites.append({**{k:e.get(k) for k in ['name','tests','failures','errors','skipped','timestamp']},'failed_methods':[n.get('name') for n in e.findall('testcase') if n.find('failure') is not None]})
jar=R/'composeApp/build/libs/composeApp-desktop.jar'
with zipfile.ZipFile(jar) as z:
 names=z.namelist();normal=not any('DeliveryProof' in name or 'Presentation10JTest' in name or 'Copy10JTest' in name for name in names);manifest=z.read('META-INF/MANIFEST.MF').decode()
result={'task':'10K3','status':'required_inherited_regressions_fail' if any(int(x['failures'] or 0)+int(x['errors'] or 0) for x in suites) else 'pass_configured_harness','suites':suites,'totals':{k:sum(int(x[k] or 0) for x in suites) for k in ['tests','failures','errors','skipped']},'normal_jar':{'path':str(jar.relative_to(R)),'sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'manifest':manifest,'no_proof_or_audit_classes':normal},'configured_scope':'JVM library/resource package and real Compose/Skia scenes; no configured desktop launcher, installer/native-window accessibility or OS browser-launch claim','fresh_artwork_reuse':'../10K1/test-reports/desktop-artwork-observations.json;2464 current functional renderer cases, not pixel/readability acceptance','candidate_inputs':'Unchanged fingerprint in environment.json; audit test sources are isolated under10K3','inherited_failures_expected':['DEF-10F-001','DEF-10H-001'],'T10':'open until relevant defects/required cases are repaired and re-executed'}
(OUT/'desktop-results.json').write_text(json.dumps(result,indent=2)+'\n');print(result['totals'])
