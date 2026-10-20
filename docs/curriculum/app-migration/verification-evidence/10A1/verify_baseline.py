"""Freeze/verify 10A1 inputs without rewriting historical acceptance receipts."""
import argparse
import collections
import hashlib
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
INDEX = 'docs/curriculum/app-migration/implementation-evidence/evidence-index.json'
HANDOFF = '4270d58'
DOCS = {'docs/curriculum/implementation-plan.md', 'docs/curriculum/progress.md'}
CACHE = {}

def sha(path):
    p = ROOT / path
    if path not in CACHE:
        with p.open('rb') as f:
            CACHE[path] = hashlib.file_digest(f, 'sha256').hexdigest()
    return CACHE[path]

def load(path):
    return json.loads((ROOT / path).read_text())

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True)

def pairs(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            yield value['path'], value['sha256']
        for child in value.values():
            yield from pairs(child)
    elif isinstance(value, list):
        for child in value:
            yield from pairs(child)

def collect():
    index = load(INDEX)
    manifest = load('content/accepted-content-manifest.json')
    curriculum = load('content/curriculum.json')
    questions = load('content/accepted-assessment-questions.json')['questions']
    registry = load('docs/curriculum/app-migration/curriculum-map.json')
    current = []
    drift = []
    for record in index['files']:
        path = record['path']
        actual = sha(path) if (ROOT / path).is_file() else None
        row = {'path': path, 'handoff_sha256': record['sha256'], 'current_sha256': actual}
        row['status'] = 'pass' if actual == record['sha256'] else 'expected_documentation_drift' if path in DOCS else 'fail'
        current.append(row)
        if actual != record['sha256']:
            historical = subprocess.check_output(['git','show',f'{HANDOFF}:{path}'],cwd=ROOT)
            row['handoff_commit_blob_sha256'] = hashlib.sha256(historical).hexdigest()
            row['historical_blob_matches_index'] = row['handoff_commit_blob_sha256'] == record['sha256']
            row['subsequent_commits'] = git('log','--format=%H %s',f'{HANDOFF}..HEAD','--',path).splitlines()
            drift.append(row)
    bound = set(pairs(manifest))
    for payload in manifest['payloads']:
        path = payload['file']['path']
        if path.endswith('.json'):
            bound.update(pairs(load(path)))
    bound_checks = [{'path':p,'expected_sha256':s,'actual_sha256':sha(p), 'status':'pass' if sha(p)==s else 'fail'} for p,s in sorted(bound)]
    artwork = []
    for asset in curriculum['assets']:
        for role in ('original','bundled'):
            item=asset[role]
            artwork.append({'asset_id':asset['id'],'role':role,'path':item['path'],'expected_sha256':item['sha256'],'actual_sha256':sha(item['path']),'status':'pass' if sha(item['path'])==item['sha256'] else 'fail'})
    tracked = [p for p in git('ls-files','-z').split('\0') if p and not p.startswith('docs/curriculum/app-migration/verification-evidence/')]
    files = [{'path':p,'sha256':sha(p),'bytes':(ROOT/p).stat().st_size} for p in tracked]
    candidate_paths=[p for p in tracked if p.startswith(('composeApp/','content/','iosApp/','tools/','gradle/','kotlin-js-store/')) or p in {'build.gradle.kts','settings.gradle.kts','gradle.properties','gradlew','gradlew.bat'}]
    fingerprint=hashlib.sha256(json.dumps([(p,sha(p)) for p in sorted(candidate_paths)],separators=(',',':')).encode()).hexdigest()
    changed_since=git('diff','--name-only',f'{HANDOFF}..HEAD').splitlines()
    counts={
        'questions':len(questions),'concepts':len({q['concept_id'] for q in questions}),
        'accepted':sum(q['acceptance']['eligibility']=='accepted' for q in questions),
        'active_holds':sum(len(q['acceptance']['open_holds']) for q in questions),
        'dispositions':dict(collections.Counter(q['relationship']['disposition'] for q in questions)),
        'modules':len(curriculum['modules']), 'lessons':sum(len(m['lesson_ids']) for m in curriculum['modules']),
        'reading_nodes':len(curriculum['reading_order']), 'reviews':sum(d['id'].endswith('-R') for d in curriculum['documents']),
        'appendices':sum(d['id'].startswith('appendix-') for d in curriculum['documents']),
        'reference_groups':len(curriculum['reference_groups']), 'canonical_destinations':len(manifest['canonical_revisions']),
        'official_entries':len(curriculum['sign_entries']), 'artwork_bindings':len(curriculum['assets']),
        'artwork_files':len({a['bundled']['path'] for a in curriculum['assets']})}
    expected={'questions':1000,'concepts':500,'accepted':1000,'active_holds':0,'dispositions':{'retain':336,'rewrite':626,'replace':38},'modules':10,'lessons':40,'reading_nodes':60,'reviews':10,'appendices':4,'reference_groups':24,'canonical_destinations':1123,'official_entries':400,'artwork_bindings':484,'artwork_files':419}
    checks=[]
    def check(id,expected,observed,evidence):
        checks.append({'id':id,'status':'pass' if expected==observed else 'fail','expected':expected,'observed':observed,'evidence':evidence})
    check('10A1-HANDOFF',0,sum(x['status']=='fail' for x in current),'candidate-baseline.json#/handoff_file_comparison')
    check('10A1-DOC-DRIFT',True,all(r['path'] in DOCS and r['historical_blob_matches_index'] for r in drift),'candidate-baseline.json#/documented_drift')
    check('10A1-COMMITTED-SCOPE',True,set(changed_since)<=DOCS,'candidate-baseline.json#/git/changed_since_handoff')
    check('10A1-MANIFEST',index['accepted_manifest']['file']['sha256'],sha('content/accepted-content-manifest.json'),'candidate-baseline.json#/accepted_manifest')
    check('10A1-IDENTITY',index['accepted_manifest']['identity'],manifest['identity'],'candidate-baseline.json#/accepted_manifest')
    check('10A1-BOUND-FILES',0,sum(x['status']=='fail' for x in bound_checks),'candidate-baseline.json#/accepted_bound_file_checks')
    check('10A1-ARTWORK',0,sum(x['status']=='fail' for x in artwork),'candidate-baseline.json#/artwork_origin_checks')
    check('10A1-COUNTS',expected,counts,'candidate-baseline.json#/observed_counts')
    check('10A1-PDF',manifest['source_curriculum']['pdf']['sha256'],sha(manifest['source_curriculum']['pdf']['path']),'candidate-baseline.json#/approved_pdf')
    data={'schema_version':1,'task':'10A1','recorded_at':datetime.now(ZoneInfo('Europe/Stockholm')).isoformat(),
          'git':{'commit':git('rev-parse','HEAD').strip(),'branch':git('branch','--show-current').strip(),'handoff_commit':git('rev-parse',HANDOFF).strip(),'changed_since_handoff':changed_since,'status_at_collection':git('status','--short'),'tracked_diff':git('diff','HEAD','--stat')},
          'environment':{'platform':platform.platform(),'python':platform.python_version()},
          'accepted_manifest':{'file':{'path':'content/accepted-content-manifest.json','sha256':sha('content/accepted-content-manifest.json')},'identity':manifest['identity']},
          'approved_pdf':manifest['source_curriculum']['pdf'], 'policy':load('content/delivery-targets.json'),
          'candidate_source_fingerprint':fingerprint,'candidate_source_paths':sorted(candidate_paths),
          'observed_counts':counts,'handoff_file_comparison':current,'documented_drift':drift,'accepted_bound_file_checks':bound_checks,'artwork_origin_checks':artwork,'tracked_input_fingerprints':files,
          'self':{'path':str(Path(__file__).relative_to(ROOT)),'sha256':sha(str(Path(__file__).relative_to(ROOT)))},
          'exclusions':'Ignored local caches/build outputs are not immutable inputs. Installed binaries and runtime checks are later 10K work; snapshot hashes do not prove functional correctness. Task-generated evidence is separately hash-bound.'}
    return data,checks

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        baseline=load(str((OUT/'candidate-baseline.json').relative_to(ROOT)))
        failed=[];doc_changes=[]
        for row in baseline['tracked_input_fingerprints']:
            actual=sha(row['path']) if (ROOT/row['path']).exists() else None
            if actual!=row['sha256']:
                (doc_changes if row['path'] in DOCS else failed).append(row['path'])
        extras=[p for p in git('ls-files','--others','--exclude-standard','-z').split('\0') if p and not p.startswith('docs/curriculum/app-migration/verification-evidence/')]
        print(json.dumps({'status':'pass' if not failed and not extras else 'fail','changed_baseline_inputs':failed,'documentation_updates_require_review':doc_changes,'unexpected_untracked_files':extras,'historical_receipts_modified':False},indent=2))
        raise SystemExit(bool(failed or extras))
    data,checks=collect()
    (OUT/'candidate-baseline.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    status='pass' if all(c['status']=='pass' for c in checks) else 'fail'
    result={'task':'10A1','status':status,'candidate':data['accepted_manifest'],'source_fingerprint':data['candidate_source_fingerprint'],'checks':checks,'counts':{'handoff_files':len(data['handoff_file_comparison']),'matching_handoff_files':sum(c['status']=='pass' for c in data['handoff_file_comparison']),'expected_documentation_differences':len(data['documented_drift']),'accepted_file_hash_pairs':len(data['accepted_bound_file_checks']),'artwork_origin_checks':len(data['artwork_origin_checks']),'tracked_inputs_fingerprinted':len(data['tracked_input_fingerprints'])},'functional_verification':'T01–T10 remain not_run; this task establishes input identity only.'}
    (OUT/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(status!='pass')

if __name__=='__main__':main()
