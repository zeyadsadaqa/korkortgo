"""Build ordered search/filter oracles from frozen7E tags and authored teaching, not Kotlin."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
content=json.loads((ROOT/'content/curriculum.json').read_text());frozen=json.loads((ROOT/'docs/curriculum/app-migration/link-and-progress-map.json').read_text())
def rich(nodes):
 return ''.join(n.get('text',n.get('spoken_text','')) if n['type'] in ['text','math'] else rich(n.get('children',n.get('label',[]))) for n in nodes)
signs={s['id']:s for s in content['sign_entries']}
def block(b):
 p=b['payload'];t=p['type']
 if t in ['heading','paragraph']:return rich(p['text'])
 if t=='list_items':return '\n'.join(block(x) for row in p['items'] for x in row)
 if t=='table':return '\n'.join([rich(p.get('caption') or []),' '.join(rich(c['heading']) for c in p['columns']),' '.join(rich(c) for row in p['rows'] for c in row['cells'])])
 if t=='equation':return ' '.join([p['expression'],p['spoken_text'],rich(p['assumptions'])])
 if t in ['callout','scenario']:return rich(p.get('title') or [])+' '+' '.join(block(x) for x in p['blocks'])
 if t=='knowledge_check':return ' '.join(block(x) for x in p['prompts'])
 if t in ['image','cropped_image','polygon_image','composite_image']:return rich(p['caption'])
 if t=='related_links':return ' '.join(rich(x['label']) for x in p['links'])
 if t=='sign_examples':return ' '.join(signs[x]['english_label'] for x in p['entry_ids'])
 raise ValueError(t)
docs={d['id']:d for d in content['documents']};order=[x for m in sorted(content['modules'],key=lambda m:m['order']) for x in m['lesson_ids']]
tags={r['lesson_id']:r['category_ids'] for r in frozen['lesson_category_tags']}
search={id:'\n'.join([docs[id]['title']]+[rich(o) for o in docs[id]['objectives']]+[block(b) for b in docs[id]['body_blocks']]) for id in order}
queries=['','green','guard','tyre','risk','  STOP  ','zzzxq10I','M01-L01']+[docs[id]['title'] for id in order]
rows=[]
for category in ['ALL']+[c['category_id'] for c in frozen['category_routes']]:
 for query in queries:
  expected=[id for id in order if (category=='ALL' or category in tags[id]) and (not query.strip() or query.strip().lower() in search[id].lower())]
  rows.append({'id':f'10I-SEARCH-{len(rows)+1:03}','query':query,'category':category,'expected_lesson_ids':expected})
(HERE/'search-inputs.tsv').write_text(''.join('\t'.join([r['id'],r['category'],r['query'],','.join(r['expected_lesson_ids'])])+'\n' for r in rows))
(HERE/'search-oracle.json').write_text(json.dumps({'scope':'Independent frozen7E tags/categories + authoredcontent search fields, only lesson membership; supporting material remains available separately.','lesson_order':order,'tags':tags,'queries':rows},indent=2)+'\n')
print('Prepared',len(rows),'ordered model/UI search cases;40 tags and5 categories.')
