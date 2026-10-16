"""Compile the retained unscored 9A3 question through the evolved identity validator."""
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT/'tools'))
from compile_curriculum import compile_files, manifest_digest
from content_schema import MODEL_PATHS
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'9A3/fixture'
manifest = json.loads((SOURCE/'manifest.json').read_text())
# Refresh implementation inputs only. Approved content, fixture payloads, source authority,
# semantic revision, key and original source/artwork bytes remain exactly as retained.
mutable = {*MODEL_PATHS, 'tools/compile_curriculum.py', 'tools/content_schema.py', 'tools/build_content.py'}
for record in manifest['inputs']:
    if record['path'] in mutable:
        record['sha256'] = hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()
for path in [HERE/'authored-identities.json', ROOT/'tools/prepare_assessment_9d.py']:
    manifest['inputs'].append({'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
manifest['identity']['manifest_sha256'] = manifest_digest(manifest)
(HERE/'staging-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
paths = {k: SOURCE/(k+'.json') for k in ['curriculum','questions','sources','legacy_aliases']}
print(compile_files(paths, HERE/'staging-manifest.json', HERE/'generated', HERE/'trace.json', symbol='identityFixture9D1'))
