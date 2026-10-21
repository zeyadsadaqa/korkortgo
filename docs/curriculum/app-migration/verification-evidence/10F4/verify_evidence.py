"""Evidence integrity passes only when required failures/non-passes remain truthfully classified."""
import collections,hashlib,json,re,sys,xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'content/curriculum.json').exists());BASE=Path(__file__).resolve().parent.parent;HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(name,ok):checks.append({'name':name,'status':'pass' if ok else 'fail'})
bank=read(ROOT/'content/accepted-assessment-questions.json')['questions'];byid={q['key']['question_id']:q for q in bank};manifest=read(ROOT/'content/accepted-content-manifest.json');a=read(BASE/'10F1/length-quota-capacity-results.json');b=read(BASE/'10F2/shuffle-feedback-scoring-results.json');c=read(BASE/'10F3/snapshot-identity-results.json');d=read(HERE/'production-quiz-results.json');ledger=read(HERE/'defects.json');summary=read(HERE/'results.json')
check('Unchanged exact accepted identity and1000 accepted/zero held',a['identity']==b['identity']==d['identity']==manifest['identity'] and len(bank)==1000 and all(q['acceptance']['eligibility']=='accepted' and q['acceptance']['open_holds']==[] for q in bank))
weights=[7,5,16,32,5,5];oracle={}
for n in range(1,71):
 shares=[Fraction(n*w,70) for w in weights];floor=[int(v) for v in shares];rank=sorted(range(6),key=lambda i:(-(shares[i]-floor[i]),i));oracle[n]=[floor[i]+int(i in rank[:n-sum(floor)]) for i in range(6)]
check('Every length/20seed and independent tie oracle',len(a['cases'])==1400 and {(r['size'],r['seed']) for r in a['cases']}=={(n,s) for n in range(1,71) for s in range(20)} and all(r['quota']==oracle[r['size']] for r in a['cases']) and oracle[70]==weights)
for r in a['cases']:
 selected=r['selected'];counts=collections.Counter(q['category'] for q in selected);expected=r['quota'];cats=['vehicle','environment','safety','rules','personal'];cap=[counts[x] for x in cats]
 check(f"allocation-{r['size']}-{r['seed']}",len(selected)==len({q['id'] for q in selected})==len({q['concept'] for q in selected})==r['size'] and cap==r['actual_categories'] and all(cap[i]>=expected[i] for i in range(5)) and sum(cap[i]-expected[i] for i in range(5))==expected[5] and all(q['revision']==byid[q['id']]['key']['revision'] and q['concept']==byid[q['id']]['concept_id'] and set(q['option_ids'])=={o['id'] for o in byid[q['id']]['options']} for q in selected))
check('15 explicit boundaries and mixed-held exclusion',len(a['rejections'])==15 and all(r['status']=='rejected' for r in a['rejections']) and a['mixed_held_exclusion']=='pass')
keyrows=read(BASE/'10F2/all-question-key-position-observations.json')['observations'];groups=collections.defaultdict(list)
for r in keyrows:groups[r['id']].append(r)
check('Every accepted ID in all4 key positions/both modes',set(groups)==set(byid) and len(keyrows)==8000 and all(len(rs)==8 and {(r['key_position'],r['mode']) for r in rs}=={(p,m) for p in range(4) for m in ['immediate','at_end']} for rs in groups.values()))
check('Keys and scores independently match accepted JSON',all(r['score']==int(r['selected']==byid[r['id']]['feedback']['correct_option_id']) and r['revision']==byid[r['id']]['key']['revision'] and r['status']=='pass' for r in keyrows))
expectedCases={(n,s,m) for n in range(1,71) for s in range(20) for m in ['immediate','at_end']};check('Full2800 session Cartesian matrix',len(b['sessions'])==2800 and {(r['size'],r['seed'],r['mode']) for r in b['sessions']}==expectedCases)
for r in b['sessions']:
 n=r['size'];seed=r['seed'];correct=[i for i in range(n) if seed%3==0 or seed%3==2 and i%2==0];incorrect=[i for i in range(n) if i not in correct]
 check(f"scoring-{n}-{seed}-{r['mode']}",r['expected_score']==r['actual_score']==len(correct) and r['filter_positions']=={'ALL':list(range(n)),'CORRECT':correct,'INCORRECT':incorrect} and r['status']=='pass' and bool(re.fullmatch('[0-9a-f]{64}',r['snapshot_and_answer_sha256'])))
check('99400 answers/198800 review rows',b['answered_transitions']==99400 and b['reviewed_rows']==198800)
check('All4 exact fuel IDs/current revisions included',all(len(groups[q])==8 and all(r['revision']=='fuel-exact-r2' for r in groups[q]) for q in ['fuel-saving-150-0.5','fuel-saving-150-1.5','fuel-saving-250-0.5','fuel-saving-250-1.5']))
fixtures=read(BASE/'10F3/historical-fuel-fixtures.json')['questions'];historic=read(BASE/'10F3/historical-snapshot-observations.json')['cases'];hm={r['question_id']:r for r in fixtures}
check('Historical4 receipts unchanged and8 conditional cases preserve old values',len(fixtures)==4 and len(historic)==8 and all(sha(ROOT/r['source'])==r['source_sha256'] for r in fixtures) and all(set(r['old_option_text'])=={o['text'] for o in hm[r['id']]['before']['options']} and r['score_before']==r['score_after_newer_teaching_and_conditional_key']==1 and r['old_revision']==hm[r['id']]['before_revision'] for r in historic))
invalid=read(BASE/'10F3/invalid-input-observations.json')['cases'];failed=[r for r in invalid if r['status']=='fail'];check('Exactly3 required failure observations,10 actual rejections',len(invalid)==13 and len(failed)==3 and {r['case'] for r in failed}=={'missing_content_version','wrong_content_version','wrong_manifest_digest'} and all(r['observed']=='accepted' for r in failed) and sum(r['observed']=='rejected' for r in invalid)==10 and c['status']=='fail_required_identity_rejection')
check('4 full-bank supplemental production flows/both modes and1/3 sizes',len(d['shared_production_journeys'])==4 and {(r['size'],r['mode']) for r in d['shared_production_journeys']}=={(n,m) for n in [1,3] for m in ['immediate','at_end']} and all(r['bank_count']==1000 and r['held_count']==0 and r['status']=='pass' for r in d['shared_production_journeys']))
for r in d['shared_production_journeys']:
 check('shared-'+r['mode']+'-'+str(r['size']),len(r['questions'])==r['size'] and r['expected_score']==sum(q['selected']==byid[q['id']]['feedback']['correct_option_id'] for q in r['questions']) and all(set(q['display_order'])=={o['id'] for o in byid[q['id']]['options']} and q['revision']==byid[q['id']]['key']['revision'] for q in r['questions']))
check('Forty70-question engine runs distinct from32 pending original platform journeys',len(d['separate_engine_70_question_runs'])==40 and len(d['required_platform_journeys'])==32 and all(c['status']=='not_run_pending_10K' and c['observation'] is None for c in d['required_platform_journeys']) and d['counts']['credited_original_platform_passes']==0)
index=read(HERE/'capture-index.json');check('All44 logical captures resolve to36 exact retained PNGs',len(index['captures'])==index['logical_count']==44 and len({c['stored_path'] for c in index['captures']})==index['stored_count']==36 and all(sha(HERE/c['stored_path'])==c['sha256'] for c in index['captures']))
check('Ten inherited and1 new P2 finding; T05 open',len(ledger['inherited_open_product_defects'])==10 and len(ledger['open_product_defects'])==11 and ledger['findings'][0]['severity']=='P2' and ledger['findings'][0]['state']=='open' and all(k in ledger['findings'][0] for k in ledger['required_record_fields']) and summary['T05']=='open')
for i,cls,tests,failures in [(1,'Allocation10FTest',1,0),(2,'Scoring10FTest',2,0),(3,'Snapshot10FTest',2,1),(4,'ProductionJourney10FTest',1,0)]:
 task=f'10F{i}';p=BASE/task;x=ET.parse(p/f'TEST-se.korkort.{cls}.xml').getroot();check(task+' actual JVM outcome',int(x.get('tests'))==tests and int(x.get('failures'))==failures and x.get('errors')=='0')
 for c in read(p/'commands.json'):check(task+' command log '+c['log'],sha(p/c['log'])==c['log_sha256'] and (c['exit_code']==1 if i==3 else c['exit_code']==0))
 if '--check-manifests' in sys.argv:
  for a in read(p/'artifacts.json'):check(task+' artifact '+a['path'],sha(p/a['path'])==a['sha256'])
base=read(HERE/'baseline-exit.json');check('Protected inputs/historical receipts unchanged',base['status']=='pass' and not base['changed_baseline_inputs'] and base['historical_receipts_modified'] is False and sha(ROOT/'content/accepted-content-manifest.json')=='ba91c96975c39b5f6db552c6bead17c0e0474c11dd590f811a7eeb1e1ae54a21')
report={'status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','meaning':'Evidence integrity, not acceptance closure','T05':'open','counts':{'checks':len(checks),'failed':sum(c['status']=='fail' for c in checks)},'checks':checks}
if '--check-manifests' not in sys.argv:(HERE/'evidence-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}|{'failures':[c for c in checks if c['status']=='fail']},indent=2));sys.exit(0 if report['status']=='pass' else 1)
