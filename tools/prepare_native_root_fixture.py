"""Write deterministic black-box XCTest expectations from the accepted manifest payload."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14'
def plain(nodes):
 assert all(n['type']=='text' for n in nodes)
 return ''.join(n['text'] for n in nodes)
def build():
 questions=json.loads((ROOT/'content/accepted-assessment-questions.json').read_text())['questions']
 documents={d['id']:d for d in json.loads((ROOT/'content/curriculum.json').read_text())['documents']}
 rows=[]
 for q in questions:
  labels={o['id']:(o['image']['neutral_description']['text'] if o['image'] else plain(o['text'])) for o in q['options']}
  wrong=next(o for o in q['options'] if o['id']!=q['feedback']['correct_option_id'] and list(labels.values()).count(labels[o['id']])==1)
  rows.append({'id':q['key']['question_id'],'revision':q['key']['revision'],'prompt':plain(q['prompt']),'stem':q['image']['neutral_description']['text'] if q['image'] else None,'wrong_label':labels[wrong['id']],'lesson':documents[q['relationship']['primary_lesson_id']]['title']})
 manifest=json.loads((ROOT/'content/accepted-content-manifest.json').read_text())
 return {'identity':manifest['identity'],'questions':rows}
if __name__=='__main__':
 out=BASE/'accepted-root-fixtures.json';out.write_text(json.dumps(build(),ensure_ascii=False,separators=(',',':'))+'\n');print('Native root fixture:',out)
