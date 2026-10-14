"""Acceptance checks and synthetic resolver examples for the 7E plan only."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,collections,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def read(p):return json.loads(p.read_text())
@lru_cache(maxsize=None)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(HERE/'link-and-progress-map.json');base=read(HERE/'baseline.json');cm=read(HERE/'curriculum-map.json');qm=read(HERE/'question-map.json');qa=read(HERE/'question-actions.json');bank=read(ROOT/'content/questions.json');signs=read(ROOT/'content/signs.json')
for v in m['inputs']:assert sha(ROOT/v['path'])==v['sha256'],v['path']
for v in base['frozen_inputs']+base['bundled_assets']:assert sha(ROOT/v['path'])==v['sha256'],v['path']
assert read(HERE/'question-actions-checks.json')['question_actions_sha256']==sha(HERE/'question-actions.json')
targets={v['id'] for key in ['curriculum_nodes','sign_entries','source_destinations','supporting_destinations'] for v in cm[key]};lessons={v['id'] for v in cm['curriculum_nodes'] if v['kind']=='lesson'};assert len(targets)==1123
chaps=m['chapter_aliases'];assert len(chaps)==39 and len({c['normalized_title_key'] for c in chaps})==39
for c,old in zip(chaps,base['legacy_chapters']):
 assert [c['legacy_title'],c['legacy_category'],*c['legacy_page_range']]==[old['title'],old['category'],old['page'],old['end_page']]
 assert c['target_ids'] and len(set(c['target_ids']))==len(c['target_ids']) and set(c['target_ids'])<=targets
 assert c['resolution']==('content' if len(c['target_ids'])==1 else 'topic_chooser')
page_rows=m['legacy_page_aliases'];assert [r['legacy_page'] for r in page_rows]==list(range(6,367))
for r in page_rows:
 hits=[c for c in chaps if c['legacy_page_range'][0]<=r['legacy_page']<=c['legacy_page_range'][1]];assert len(hits)<=1
 if hits:assert r['target_ids']==hits[0]['target_ids'] and r['chapter_alias_id']==hits[0]['legacy_id']
 else:assert r['resolution']=='unavailable' and not r['target_ids']
qrows=m['question_routes'];assert len(qrows)==1000 and [r['question_id'] for r in qrows]==[q['id'] for q in bank]
for r,q,mp,act in zip(qrows,bank,qm['questions'],qa['questions']):
 assert r['target_id']==mp['primary_lesson_id'] and r['target_id'] in lessons
 assert r['legacy_page']==q['page'] and r['legacy_source_url']==q['source'] and r['concept_id']==q['concept']
 assert r['source_ids']==mp['source_ids'] and r['source_reference_ids']==mp['source_reference_ids']
 assert set(r['related_target_ids']+r['reference_target_ids'])<=targets
 assert r['disposition']==act['disposition']
 assert r['target_id'] in next(p['target_ids'] for p in page_rows if p['legacy_page']==q['page'])
assert len(m['unused_topic_routes'])==178
qindex={r['question_id']:r for r in qrows}
for r in m['unused_topic_routes']:assert r['target_id']==qindex[r['question_id']]['target_id'] and r['legacy_page']==qindex[r['question_id']]['legacy_page']
assert len(m['sign_routes'])==343 and [r['legacy_code'] for r in m['sign_routes']]==[s['code'] for s in signs]
missing=[]
for r,s in zip(m['sign_routes'],signs):
 assert r['legacy_source_url']==s['url'] and r['legacy_image']==s['image']
 if r['target_id']:assert r['target_id']=='sign-'+s['code'] and r['target_id'] in targets
 else:missing.append(s['code']);assert r['resolution']=='unavailable_exact_entry' and r['fallback_rule_id']
assert missing==['SIG16','SIG17','SIG18'];assert {x['legacy_code'] for x in m['unresolved_destinations']}==set(missing)
assert len(m['reading_order'])==len(set(m['reading_order']))==60 and set(m['reading_order'])<=targets
assert m['reading_order']==[x for mod in cm['modules'] for x in [mod['id'],*mod['lesson_ids'],mod['review_id']]]
tags={x['lesson_id']:set(x['category_ids']) for x in m['lesson_category_tags']};assert set(tags)==lessons
cats={r['category_id'] for r in m['category_routes']};assert cats=={'VEHICLE','ENVIRONMENT','SAFETY','RULES','PERSONAL'}
assert sum(c['baseline_quota_per_70'] for c in m['category_routes'])==65
for row in m['category_routes']:assert set(row['lesson_ids'])=={lid for lid,v in tags.items() if row['category_id'] in v}
for q,r in zip(bank,qrows):assert q['category'] in tags[r['target_id']]
assert {r['legacy'] for r in m['navigation_routes']}=={'Page.'+v for v in ['HOME','LIBRARY','READER','SETUP','QUIZ','RESULTS','REVIEW','SIGNS']}
app=(ROOT/'composeApp/src/commonMain/kotlin/se/korkort/App.kt').read_text();fields=set(re.findall(r'^        var (\w+) by remember',app,re.M));state={s['field'] for s in m['state_rules']}
assert {'App.'+f for f in fields}<=state
assert {'QuestionCard.selected','Review.open','QuizSession.questions','QuizSession.feedback','QuizSession.answers','QuizSession.index','QuizSession.finished','QuizSession.current','QuizSession.score','bookmarks','completed_lessons','question_history','persistent_storage_schema'}<=state
assert len(state)==len(m['state_rules'])==22
for row in m['labels_to_replace']:
 for line in row['lines']:assert row['legacy_pattern'] in app.splitlines()[line-1]
assert len(m['entry_point_rules'])==12 and not m['production_tombstones']
# Model the documented resolution precedence without adding it to the app.
namespace=m['legacy_namespace']['id'];by_page={r['legacy_page']:r for r in page_rows};sign_index={r['legacy_code']:r for r in m['sign_routes']}
def resolve(kind,**v):
 if kind=='content':
  if v['id'] not in targets:return ('unavailable',None)
  return ('content',v['id'])
 if kind=='question':return ('content',qindex[v['id']]['target_id']) if v['id'] in qindex else ('unavailable',None)
 if kind=='legacy_page':
  if v.get('namespace')!=namespace or type(v.get('page')) is not int:return ('unavailable',None)
  r=by_page.get(v['page']);return (r['resolution'],tuple(r['target_ids'])) if r else ('unavailable',None)
 if kind=='legacy_chapter':
  if v.get('namespace')!=namespace:return ('unavailable',None)
  r=next((c for c in chaps if c['legacy_id']==v['id']),None);return (r['resolution'],tuple(r['target_ids'])) if r else ('unavailable',None)
 if kind=='legacy_sign':
  r=sign_index.get(v['code']);return (r['resolution'],r['target_id']) if r else ('unavailable',None)
 return ('unavailable',None)
cases=[]
def check(name,actual,expected):assert actual==expected,(name,actual,expected);cases.append({'id':name,'status':'passed'})
check('known-question-overrides-old-folio',resolve('question',id='situation-001',page=8),('content','M03-L02'))
check('same-old-page-first-context',resolve('question',id='situation-017',page=46),('content','M04-L03'))
check('same-old-page-other-context',resolve('question',id='situation-103',page=46),('content','M04-L01'))
check('unknown-question-does-not-fall-through',resolve('question',id='fixture-retired-question',page=46),('unavailable',None))
check('changed-answer-teaching-route',resolve('question',id='fuel-saving-150-1.5'),('content','M09-L02'))
check('replacement-hold-does-not-remove-teaching',resolve('question',id='sign-meaning-S1'),('content',qindex['sign-meaning-S1']['target_id']))
check('gap-page',resolve('legacy_page',namespace=namespace,page=13),('unavailable',()))
check('unknown-legacy-namespace',resolve('legacy_page',namespace='other-book',page=46),('unavailable',None))
check('noninteger-page',resolve('legacy_page',namespace=namespace,page='46'),('unavailable',None))
check('out-of-range-page',resolve('legacy_page',namespace=namespace,page=578),('unavailable',None))
check('unknown-canonical-not-first-module',resolve('content',id='fixture-unknown'),('unavailable',None))
check('removed-block-known-parent',resolve('content',id='M03-L04',block_id='fixture-removed-block'),('content','M03-L04'))
check('removed-block-unknown-parent',resolve('content',id='fixture-unknown',block_id='fixture-removed-block'),('unavailable',None))
check('exact-sign',resolve('legacy_sign',code='F31a'),('content','sign-F31a'))
for code in missing:check('no-similar-signal-alias-'+code,resolve('legacy_sign',code=code),('unavailable_exact_entry',None))
# Retirement fixtures are hypothetical: zero real tombstones or removals exist.
retirement_fixtures=[{'id':'fixture-retired-none','replacement_ids':[],'expected':'unavailable'},{'id':'fixture-retired-one','replacement_ids':['M03-L04'],'expected':'offer_replacement_with_notice'},{'id':'fixture-retired-many','replacement_ids':['M03-L04','M07-L04'],'expected':'topic_chooser'}]
for r in retirement_fixtures:
 result='unavailable' if not r['replacement_ids'] else 'offer_replacement_with_notice' if len(r['replacement_ids'])==1 else 'topic_chooser';assert result==r['expected'] and set(r['replacement_ids'])<=targets;cases.append({'id':r['id'],'status':'passed; synthetic only'})
# Versioned score fixture: index zero in an old shuffle can be wrong even while
# source-bank key zero was correct. Do not reinterpret either as a current key.
old_order=['wrong-option','old-key'];old_selected=0;old_key=1;new_key=0
assert (old_selected==old_key) is False and (old_selected==new_key) is True
cases.append({'id':'shuffled-index-cannot-be-regraded-with-current-key','status':'passed'})
checks={'checked_on':'2026-10-14','step':'7E','status':'passed; three exact sign gaps explicitly recorded','map_sha256':sha(HERE/'link-and-progress-map.json'),'question_links_checked':1000,'legacy_chapters_checked':39,'numeric_pages_checked':361,'unused_topics_checked':178,'legacy_sign_routes_checked':343,'exact_sign_routes':340,'unresolved_exact_sign_codes':missing,'navigation_states_checked':8,'state_fields_checked':22,'all_targets_resolve_or_have_explicit_gap_policy':True,'upstream_frozen_app_bank_assets_and_pdf_unchanged':True,'production_question_removals':0,'production_tombstones':0,'compatibility_examples':cases,'step_7F_started':False}
(HERE/'link-and-progress-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({k:v for k,v in checks.items() if k!='compatibility_examples'},indent=2))
