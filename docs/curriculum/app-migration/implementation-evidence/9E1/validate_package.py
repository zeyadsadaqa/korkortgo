"""Validate the 9E1 typed questions against the complete approved reading/source/asset package."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools'))
from compile_curriculum import Validator,manifest_digest
HERE=Path(__file__).resolve().parent
base=HERE.parent/'9B17'
paths={'curriculum':ROOT/'content/curriculum.json','questions':HERE/'questions.json','sources':ROOT/'content/sources.json','legacy_aliases':base/'legacy_aliases.json'}
payloads={k:json.loads(p.read_text()) for k,p in paths.items()}
manifest=json.loads((base/'staging-manifest.json').read_text())
for r in manifest['inputs']:
    if r['path'] in {'composeApp/src/commonMain/kotlin/se/korkort/Quiz.kt','tools/build_content.py','tools/compile_curriculum.py','tools/content_schema.py'}:
        r['sha256']=hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()
for k,p in paths.items():
    next(r for r in manifest['payloads'] if r['kind']==k)['file']={'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
manifest['identity']['content_version']='staging-9E1-held-rewrites'
manifest['question_revisions']=[{'key':q['key'],'eligibility':q['acceptance']['eligibility']} for q in payloads['questions']['questions']]
for p in [ROOT/'tools/apply_sign_rewrite_9e1.py',HERE/'content-review.json',HERE/'incoming-questions.json']:
    manifest['inputs'].append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest['identity']['manifest_sha256']=manifest_digest(manifest)
totals=Validator().package(payloads,manifest,'fixture')
(HERE/'validation-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(HERE/'package-validation.json').write_text(json.dumps({'status':'passed','totals':totals,'question_eligibility':'50 held; none accepted'},indent=2)+'\n')
print(totals)
