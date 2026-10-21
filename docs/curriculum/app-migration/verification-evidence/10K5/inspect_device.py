import hashlib,json,re,subprocess
from collections import Counter
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[4];framework=R/'composeApp/build/bin/iosArm64/debugFramework/KorkortKit.framework';binary=framework/'KorkortKit'
arch=subprocess.check_output(['lipo','-archs',str(binary)],text=True).strip();meta=subprocess.check_output(['otool','-l',str(binary)],text=True);platforms=re.findall(r'^\s*platform\s+(\S+)',meta,re.M);assert arch=='arm64' and set(platforms)=={'2'},(arch,set(platforms))
result={'task':'10K5','status':'pass_required_device_build_and_metadata_physical_runtime_excluded','normal_framework':str(framework.relative_to(R)),'framework_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'architecture':arch,'format':'Static framework archive as configured','object_build_platforms':dict(Counter(platforms)),'platform_definition':'Mach-O2=iOS device;7=simulator','sample_build_metadata':meta[meta.find('LC_BUILD_VERSION')-40:meta.find('LC_BUILD_VERSION')+220],'proof_flag':False,'resources':'device-resource-parity.json must pass490 independent byte checks','physical_runtime':'excluded_unperformed by existing simulator-only policy; no signing,install,VoiceOver or physical legibility pass','publication':False}
(OUT/'ios-device-build-results.json').write_text(json.dumps(result,indent=2)+'\n');print(arch,len(platforms),'device platform objects')
