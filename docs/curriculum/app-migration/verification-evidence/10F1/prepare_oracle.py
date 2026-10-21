"""Independent exact rational largest-remainder oracle; no production Kotlin helper imported."""
import json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
weights=[7,5,16,32,5,5];rows=[]
for n in range(1,71):
 shares=[Fraction(n*w,70) for w in weights];floor=[s.numerator//s.denominator for s in shares];left=n-sum(floor)
 ranking=sorted(range(6),key=lambda i:(-(shares[i]-floor[i]),i));counts=[floor[i]+int(i in ranking[:left]) for i in range(6)]
 rows.append({'size':n,'counts':counts,'fractions':[str(s) for s in shares],'remainder_rank':ranking,'tie_policy':'VEHICLE, ENVIRONMENT, SAFETY, RULES, PERSONAL, RANDOM'})
(HERE/'allocation-oracle.json').write_text(json.dumps({'weights':weights,'rows':rows},indent=2)+'\n')
(HERE/'allocation-oracle.tsv').write_text('\n'.join('\t'.join(map(str,[r['size'],*r['counts']])) for r in rows)+'\n')
print('70 rational allocations prepared, including full 7/5/16/32/5 +5 random.')
ROOT=next(p for p in HERE.parents if (p/'content/curriculum.json').exists())
questions=json.loads((ROOT/'content/accepted-assessment-questions.json').read_text())['questions']
(HERE.parent/'10F2').mkdir(exist_ok=True)
(HERE.parent/'10F2/authored-key-oracle.tsv').write_text('\n'.join('\t'.join([q['key']['question_id'],q['key']['revision'],q['feedback']['correct_option_id']]) for q in questions)+'\n')
