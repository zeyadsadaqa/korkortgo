"""Apply only the exact first 9E batch, retaining full typed assessment metadata and delivery gates."""
import argparse
import copy
import difflib
import hashlib
import json
from pathlib import Path
from compile_curriculum import Emitter, Validator, kotlin_string
from content_schema import Schema
ROOT=Path(__file__).resolve().parent.parent
BASE=Path('docs/curriculum/app-migration/implementation-evidence/9E1')
ACTIONS=Path('docs/curriculum/app-migration/question-actions.json')

def read(p):return json.loads((ROOT/p).read_text())
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def origin(p,locator):return {'file':{'path':str(p),'sha256':digest(p)},'locator':locator,'evidence_ids':[],'pdf_evidence_page':None}
def review(p,locator):return {'record':origin(p,locator),'reviewed_on':'2026-10-16'}
def text(v):return [{'type':'text','text':v}] if v else []
def ids():return next(b['question_ids'] for b in read(Path('docs/curriculum/app-migration/implementation-backlog.json'))['execution_batches'] if b['work_item_id']=='9E' and b['batch']==1)

def guard_current(current, before, after):
    if current not in (before,after):
        raise ValueError('Refusing to overwrite edits outside the exact saved 9E1 before/after states')

def build():
    incoming=read(BASE/'incoming-questions.json')
    actions=read(ACTIONS)['questions']; by_id={q['question_id']:(n,q) for n,q in enumerate(actions)}
    descriptions={q['question_id']:(n,q) for n,q in enumerate(read(Path('docs/curriculum/app-migration/implementation-evidence/9D3/description-acceptance.json'))['questions'])}
    curriculum=read(Path('content/curriculum.json'));sources=read(Path('content/sources.json'))
    assets={a['original']['sha256']:a for a in curriculum['assets'] if a['kind']=='official_sign'}
    mappings={q['question_id']:q for q in read(Path('docs/curriculum/app-migration/question-map.json'))['questions']}
    references={r['url']:r['id'] for r in sources['references']}
    def use(url):
        ref=references[url]
        match=next(((s,b) for s in sources['destinations'] for b in s['scoped_urls'] if b['reference_id']==ref),None)
        return {'source_id':match[0]['id'] if match else None,'scope_id':match[1]['scope_id'] if match else None,'reference_id':ref,'locator':'Exact 7D proposal source and approved caption/artwork.','editorial_inference':False}
    selected=set(ids());bank=copy.deepcopy(incoming);typed=[];results=[];diffs=[]
    for index,row in enumerate(bank):
        if row['id'] not in selected:continue
        before=copy.deepcopy(row);action_index,action=by_id[row['id']];p=action['proposed_changes'];desc_index,desc=descriptions[row['id']]
        assert before==action['original'];assert action['disposition']=='rewrite';assert desc['description_result']=='accepted'
        mapping=mappings[row['id']];recognise=row['id'].startswith('sign-recognise-')
        def image(slot,exact):
            d=next(i for i in desc['images'] if i['slot']==slot);a=assets[exact['sha256']]
            assert a['original']=={k:exact[k] for k in ['path','sha256']}
            assert digest(Path(a['bundled']['path']))==exact['sha256']==d['asset']['sha256']
            binding={'asset_id':a['id'],'neutral_description':{'text':d['description'],'review':review(Path('docs/curriculum/app-migration/implementation-evidence/9D3/description-acceptance.json'),f'json:/questions/{desc_index}/images/{desc["images"].index(d)}')}}
            return binding,a['bundled']['path'].split('composeResources/files/',1)[1]
        stem,stem_path=image('stem',p['question_image_asset']) if p['question_image_asset'] else (None,'')
        options=[];feedback=[];legacy_options=[]
        for o in p['options']:
            binding,path=image(o['option_id'],o['visual_description_brief']['exact_asset']) if recognise else (None,'')
            options.append({'id':o['option_id'],'text':text(o['meaning_option_text'] or ''),'image':binding})
            feedback.append({'option_id':o['option_id'],'explanation':text(o['post_answer_explanation']),'sign_code':o['code_metadata_after_reveal'],'english_label':o['post_answer_label'],'source_uses':[use(s['url']) for s in o['official_sources']]})
            legacy_options.append({'text':o['meaning_option_text'] or '', 'explanation':o['code_metadata_after_reveal']+' · '+o['post_answer_label']+'. '+o['post_answer_explanation'],'image':path})
        key=next(o['option_id'] for o in p['options'] if o['is_correct'])
        q={'key':{'question_id':row['id'],'revision':'rewrite-r2'},'concept_id':row['concept'],'category':row['category'].lower(),'prompt':text(p['prompt']),'image':stem,'options':options,
           'feedback':{'target_sign_code':p['target_code_metadata'],'english_label':p['post_answer_english_label'],'correct_option_id':key,'explanation':text(p['post_answer_explanation']),'option_feedback':feedback},
           'relationship':{k:copy.deepcopy(mapping[k]) for k in ['primary_lesson_id','related_lesson_ids','reference_ids','source_ids','content_version']},
           'acceptance':{'eligibility':'held','content_review':review(BASE/'content-review.json',f'json:/questions/{len(results)}'),'description_reviews':[review(Path('docs/curriculum/app-migration/implementation-evidence/9D3/description-acceptance.json'),f'json:/questions/{desc_index}')],'delivery_proof':[],
                         'open_holds':[{'id':row['id']+'/delivery','reason':'Exact image delivery at intended size, zoom, light/dark and representative accessibility navigation has not passed 9L/9O.','release_condition':'Record exact-asset delivery proof on supported platforms and complete assessment route integration before scored activation.'}]},
           'origin':origin(ACTIONS,f'json:/questions/{action_index}/proposed_changes')}
        q['relationship']['disposition']='rewrite';q['relationship']['source_uses']=[use(sources_ref['url']) for ref in mapping['source_reference_ids'] for sources_ref in sources['references'] if sources_ref['id']==ref]
        row.update(prompt=p['prompt'],options=legacy_options,correct=[o['id'] for o in options].index(key),explanation=p['post_answer_explanation'],image=stem_path,assessment=q)
        assert row['id']==before['id'] and row['concept']==before['concept']
        assert len({o['id'] for o in options})==4 and sum(o['is_correct'] for o in p['options'])==1
        if recognise:assert len({o['image']['asset_id'] for o in options})==4
        else:assert len({o['text'] for o in legacy_options})==4
        typed.append(q)
        results.append({'question_id':row['id'],'before_revision':'legacy-r1','after_revision':'rewrite-r2','content_key_feedback':'passed','neutral_description':'accepted in 9D3','eligibility':'held','delivery_acceptance':'pending 9L/9O','scored_activation':False,
                        'old_option_codes':p['original_option_codes'],'new_option_codes':p['proposed_option_codes'],'distractors_changed':p['original_option_codes']!=p['proposed_option_codes'],
                        'before':before,'after':row})
        diffs.extend(difflib.unified_diff(dump(before).splitlines(True),dump(row).splitlines(True),fromfile=row['id']+'/before',tofile=row['id']+'/after'))
    assert len(results)==len(selected)==50
    for code in range(1,26):
        pair=[q for q in typed if q['concept_id']==f'sign-A{code}'];assert len(pair)==2
        assert [o['sign_code'] for o in pair[0]['feedback']['option_feedback']]==[o['sign_code'] for o in pair[1]['feedback']['option_feedback']]
    emitter=Emitter(Schema(ROOT),'rewrite9E1');calls={q['key']['question_id']:emitter.emit(q,'AssessmentQuestion',q['key']['question_id']) for q in typed}
    lines=(ROOT/BASE/'incoming-bank.kt.txt').read_text().splitlines(True)
    for i,line in enumerate(lines):
        for row in bank:
            if row['id'] in selected and line.startswith('Question('+kotlin_string(row['id'])+','):
                options=', '.join('Option('+', '.join(kotlin_string(o[k]) for k in ['text','explanation','image'])+')' for o in row['options'])
                args=[kotlin_string(row['id']),kotlin_string(row['concept']),'Category.'+row['category'],kotlin_string(row['prompt']),'listOf('+options+')',str(row['correct']),kotlin_string(row['explanation']),str(row['page']),kotlin_string(row['source']),kotlin_string(row['image']),calls[row['id']]]
                lines[i]='Question('+', '.join(args)+'),\n'
                break
    lines.append('\n// 9E1: generated typed assessment metadata; delivery-held questions are excluded from scoring.\n')
    lines.extend(f'private fun {name}(): {kind} = {expression}\n' for name,kind,expression in emitter.functions)
    acceptance={'schema_version':1,'step':'9E1','question_ids':ids(),'content_checks':'passed','scored_activation':False,'questions':results}
    return bank,''.join(lines),{'schema_version':1,'questions':typed},acceptance,''.join(diffs)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    bank,kotlin,payload,acceptance,diffs=build()
    guard_current((ROOT/'content/questions.json').read_text(),(ROOT/BASE/'incoming-questions.json').read_text(),dump(bank))
    guard_current((ROOT/'composeApp/src/commonMain/kotlin/se/korkort/Bank.kt').read_text(),(ROOT/BASE/'incoming-bank.kt.txt').read_text(),kotlin)
    outputs={Path('content/questions.json'):dump(bank),Path('composeApp/src/commonMain/kotlin/se/korkort/Bank.kt'):kotlin,BASE/'questions.json':dump(payload),BASE/'batch-acceptance.json':dump(acceptance),BASE/'before-after.diff':diffs}
    for path,value in outputs.items():
        if args.check:assert (ROOT/path).read_text()==value,path
        else:(ROOT/path).write_text(value)
    print('9E1: 50 exact rewrites; 950 other questions unchanged; 50 held from scored selection.')
if __name__=='__main__':main()
