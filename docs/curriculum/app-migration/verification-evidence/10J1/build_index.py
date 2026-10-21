"""Read exact approved records; do not infer approval from a historical package status."""
import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[5]; OUT=Path(__file__).parent
load=lambda p:json.loads((R/p).read_text())
def ref(p):
 return {'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()}
package=load('docs/curriculum/app-design/8n/package-index.json')
boards=[]
approval_input_checks=[]
for task in package['approved_preview_tasks']:
 for item in [task['binding'],task['review']]+task['prompts']:
  actual=ref(item['path']);assert actual['sha256']==item['sha256'],actual
  approval_input_checks.append(dict(actual,pass_identity=True))
 for b in task['outputs']:
  actual=ref(b['path']);assert actual['sha256']==b['sha256'],actual
  boards.append(dict(actual,step=task['step'],revision=task['revision'],approval=task['approval'],review=ref(task['review']['path'])))
faint='docs/curriculum/app-design/faint-assets-v1/'
boards.append(dict(ref(faint+'preview.png'),step='faint-assets',revision='v1',approval={'date':'2026-10-17','user_statement':'approved','scope':'larger original-artwork presentation only; no content/eligibility waiver'},review=ref(faint+'review.md')))
# Independent state inventory against the explicit state table and production route branches.
rows=[
 ('home','retained','CurriculumApp.kt','existing home plus migrated attribution/counts'),
 ('setup','retained','CurriculumApp.kt','count, feedback, allocation, deliberate start'),
 ('quiz-unanswered','retained','CurriculumApp.kt','both feedback modes and neutral option selection'),
 ('quiz-confirmed','8G','CurriculumApp.kt','immediate feedback; deferred remains hidden'),
 ('results','retained','CurriculumApp.kt','valid pinned score and category breakdown'),
 ('library-overview','8B','LearningLibrary.kt','ten modules, forty lessons, ten reviews; separate supporting links'),
 ('library-filter','8C','LearningLibrary.kt','intersection, full tags, ordered results, independent reset'),
 ('library-empty','8C','LearningLibrary.kt','no auto-open; query/category recovery'),
 ('reader-opening','8D','LessonReader.kt','canonical title, goal, full content and navigation'),
 ('reader-moved','8K','LessonReader.kt','known parent with exact moved notice'),
 ('knowledge-hidden','8E','LessonReader.kt','answer absent from reading until reveal'),
 ('knowledge-revealed','8E','LessonReader.kt','answer visible and toggle focus restored on hide'),
 ('reader-long','8F','LessonReader.kt','same viewport/font at 100/160%; full equations/tables'),
 ('review-standard','8G','LearningAnswerReview.kt','all four shuffled choices and explanations, related/source return'),
 ('review-calculation','8H','LearningAnswerReview.kt','current accepted fuel revision; historical preview question is layout fixture only'),
 ('review-filter-empty','8G','CurriculumApp.kt','retained filter and expansion; empty-state text is not separately previewed'),
 ('source-destination','8I','LearningRoute.kt','canonical source landing; no separate exact landing board'),
 ('missing-source','8L','LearningSources.kt','missing reference recovery; no separate exact source-recovery board'),
 ('setup-invalid-count','retained','CurriculumApp.kt','validation errors and disabled start; no separate exact validation board'),
 ('source-directory','8I','LearningSources.kt','global or lesson-scoped publishers/classifications'),
 ('source-detail','8I','LearningSources.kt','exact dates/scope/limitations and return'),
 ('source-failure','8I','LearningSources.kt','failure text and usable return; no separate exact failure board'),
 ('reference-catalogue','8J','LearningRoute.kt','typed catalogue and 24 groups; no separate exact catalogue board'),
 ('reference-group','8J','LearningRoute.kt','full group teaching/membership; no separate exact group board'),
 ('reference-detail','8J','SignReferenceDetail.kt','B1 identity, editorial notice, unchanged bytes'),
 ('reference-credits','8J','SignReferenceDetail.kt','actual publishers, dates and artwork reuse'),
 ('viewer','8J','AccessibleImageViewer.kt','fit/zoom/reset/pan/close with neutral assessment titles'),
 ('legacy-chooser','8K','LearningRecovery.kt','page46 four exact validated choices; deliberate activation'),
 ('generic-unavailable','8L','LearningRecovery.kt','unknown parent no guessed replacement'),
 ('signal-unavailable','8L','LearningRecovery.kt','three distinct official URLs; no internal substitute'),
 ('signal-failure','8L','LearningRecovery.kt','external failure retains internal recovery'),
 ('missing-results','8M','LearningRecovery.kt','no saved result; deliberate setup; no score invention'),
 ('missing-quiz','8M','CurriculumApp.kt','missing session recovery reuses existing policy, no separate board'),
 ('unfinished-guard','8G','CurriculumApp.kt','existing cancel/discard guard; no separate exact guard board'),
 ('source-root-failure','8I','CurriculumApp.kt','existing modal failure; no separate exact modal board'),
 ('faint-question-stem','faint-assets','AssessmentCard.kt','full-width3:2 frame;220dp minimum;white backing'),
 ('faint-image-options','faint-assets','AssessmentCard.kt','same rule all four options independent of correctness'),
 ('faint-review-reader','faint-assets','LearningAnswerReview.kt','reuse frame for reader/review; wide reference380dp minimum')]
source_root=R/'composeApp/src/commonMain/kotlin/se/korkort'
for state,step,owner,contract in rows:
 if not (source_root/owner).exists():
  print('Owner locator requires refinement:',owner)
states=[]
for state,step,owner,contract in rows:
 references=[b['path'] for b in boards if b['step']==step]
 unresolved=('no separate' in contract or step=='retained')
 states.append({'state_id':state,'implementation_locator':str(Path('composeApp/src/commonMain/kotlin/se/korkort')/owner),'approved_references':references,'approval_basis':'app-design-spec.md retained-existing-behaviour policy' if step=='retained' else step,'contract':contract,'approval_limit':'No standalone exact board; retained behaviour or related-state policy only. Exact visual match unresolved.' if unresolved else 'Exact copy/bindings govern raster approximations; compare full current state.','approved_deviations':['8O: state-specific chip/icon variants retained; unsupported menu/language/OS/crop annotations excluded','8F: reflow illustration, not measured font/viewport proof','17Oct: approved common artwork frames supersede earlier candidate dimensions'],'required_captures':['normal and labelled proof builds on configured10K targets','390/conceptual narrow and wide natural reflow;100%/160% text','production light; actual dark capability/disposition, not a diagnostic override','full scroll/selected/feedback/focus/return states as applicable'],'status':'mapped_pending_current_target_comparison'})
assert len(boards)==17 and len(states)==len({s['state_id'] for s in states})
assert set(b['path'] for b in boards)<=set(p for s in states for p in s['approved_references'])
result={'task':'10J1','status':'complete_index_not_visual_acceptance','entry_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'approval_authority':[ref('docs/curriculum/app-design-review.md'),ref('docs/curriculum/app-design-spec.md'),ref(faint+'review.md')],'approved_boards':boards,'approval_input_checks':approval_input_checks,'states':states,'unresolved_exact_board_states':[s['state_id'] for s in states if 'No standalone' in s['approval_limit']],'no_new_design':True,'gate':'T09 remains open; fresh10K observations not present'}
(OUT/'design-comparison-index.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(f'Indexed {len(boards)} exact boards across {len(states)} states')
