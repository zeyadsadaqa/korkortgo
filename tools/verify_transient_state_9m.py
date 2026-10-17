"""Report the exact 22 frozen 7E contracts without accepting the held 9J package."""
import argparse,hashlib,json
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'docs/curriculum/app-migration/implementation-evidence/9M/state-contract-results.json'
M='se.korkort.TransientQuizStateTest.'
D='se.korkort.TransientPractice9MTest.'
N='se.korkort.NavigationTest.'
L='se.korkort.LearningViewsTest.'
U='se.korkort.LearningViewsSemanticsTest.'
CHECKS={
'App.page':[N+'allEightStatesUseTheSameGuardAndPreservePendingTargets',M+'missingContextsNeverFabricateResultsAndSetupDoesNotAutoStart'],
'App.countText':[M+'setupPreflightsEveryQuotaAndRandomSlotWithoutWeakeningReleaseGate',M+'missingContextsNeverFabricateResultsAndSetupDoesNotAutoStart'],
'App.feedback':[M+'draftConfirmationAndBothFeedbackModesPinAuthoredIdentity',M+'setupPreflightsEveryQuotaAndRandomSlotWithoutWeakeningReleaseGate'],
'App.session':[M+'newSessionResetsReviewAndSnapshotScoresNeverConsultRevisedBank',D+'heldCandidateCannotStartProductionAndAllSupportedFixtureSizesPreserveIdentity'],
'App.chapter':[N+'allFrozenAliasesResolveWithoutGuessing'],
'App.category':[M+'missingContextsNeverFabricateResultsAndSetupDoesNotAutoStart',L+'canonicalLibraryContainsEveryLessonAndRetainsNumbersWhenFiltered'],
'App.search':[U+'libraryClearActionsPreserveTheOtherInput',M+'missingContextsNeverFabricateResultsAndSetupDoesNotAutoStart'],
'App.reviewFilter':[M+'reviewFilterPositionExpansionAndScoreSurviveTeachingAndSourceVisits',M+'newSessionResetsReviewAndSnapshotScoresNeverConsultRevisedBank'],
'App.quitTarget':[M+'unfinishedGuardsPreserveDraftAndBindTheExactPendingAttempt',N+'sessionReplacementInvalidatesPendingDiscardRatherThanDiscardingNewAnswers'],
'QuestionCard.selected':[M+'draftConfirmationAndBothFeedbackModesPinAuthoredIdentity',D+'reusedQuestionAndOrderCannotCarryUnconfirmedRadioSelectionIntoAnotherAttempt'],
'Review.open':[M+'reviewFilterPositionExpansionAndScoreSurviveTeachingAndSourceVisits',M+'newSessionResetsReviewAndSnapshotScoresNeverConsultRevisedBank'],
'QuizSession.questions':[D+'heldCandidateCannotStartProductionAndAllSupportedFixtureSizesPreserveIdentity',M+'newSessionResetsReviewAndSnapshotScoresNeverConsultRevisedBank'],
'QuizSession.feedback':[M+'setupPreflightsEveryQuotaAndRandomSlotWithoutWeakeningReleaseGate'],
'QuizSession.answers':[M+'draftConfirmationAndBothFeedbackModesPinAuthoredIdentity',D+'reusedQuestionAndOrderCannotCarryUnconfirmedRadioSelectionIntoAnotherAttempt'],
'QuizSession.index':[M+'draftConfirmationAndBothFeedbackModesPinAuthoredIdentity',D+'heldCandidateCannotStartProductionAndAllSupportedFixtureSizesPreserveIdentity'],
'QuizSession.finished':[D+'heldCandidateCannotStartProductionAndAllSupportedFixtureSizesPreserveIdentity'],
'QuizSession.current':[M+'missingContextsNeverFabricateResultsAndSetupDoesNotAutoStart',D+'heldCandidateCannotStartProductionAndAllSupportedFixtureSizesPreserveIdentity'],
'QuizSession.score':[M+'reviewFilterPositionExpansionAndScoreSurviveTeachingAndSourceVisits',M+'newSessionResetsReviewAndSnapshotScoresNeverConsultRevisedBank'],
}
CONDITIONAL={'bookmarks','completed_lessons','question_history','persistent_storage_schema'}
def generate(reports):
    source=ROOT/'docs/curriculum/app-migration/link-and-progress-map.json'
    rules=json.loads(source.read_text())['state_rules']
    assert len(rules)==22 and {r['field']for r in rules}==set(CHECKS)|CONDITIONAL
    passed=set();count=0
    for path in sorted(reports.glob('TEST-*.xml')):
        suite=ET.parse(path).getroot()
        assert int(suite.get('failures',0))==0 and int(suite.get('errors',0))==0,path
        for case in suite.findall('testcase'):
            count+=1
            assert case.find('failure') is None and case.find('error') is None,path
            if case.find('skipped') is None:
                passed.add(case.attrib['classname']+'.'+case.attrib['name'].split('[')[0])
    rows=[]
    for i,rule in enumerate(rules,1):
        checks=CHECKS.get(rule['field'],[])
        assert set(checks)<=passed,sorted(set(checks)-passed)
        rows.append(dict(id=f'7E-STATE-{i:02}',**rule,status='conditional_future_scope' if rule['field']in CONDITIONAL else 'passed_fixture_and_candidate_checks',tests=checks,
            acceptance_scope='No existing store or imported records. Future persistence/hot replacement needs separate authorisation and compatibility verification.' if rule['field']in CONDITIONAL else 'Current transient model and retained fixtures/candidate subset; integrated accepted-release rerun remains required.'))
    questions=json.loads((ROOT/'content/assessment-questions.json').read_text())['questions']
    held=sum(q['acceptance']['eligibility']=='held' for q in questions)
    # Do not turn a field-level pass into release acceptance or guess that a future package passed.
    assert held==616
    assert 'candidateReleaseAccepted9J: Boolean = false' in (ROOT/'composeApp/src/commonMain/kotlin/se/korkort/QuestionPackage9J.kt').read_text()
    return {'date':'2026-10-17','status':'9M1–9M2 model checks passed; 9M3 awaiting final release verification',
        'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'contracts':rows,'totals':{'recorded':22,'current_transient_checks_passed':18,'conditional_future_scope':4,'desktop_tests_in_run':count},
        'candidate':{'questions':len(questions),'accepted':len(questions)-held,'held':held,'production_start_allowed':False,'fixture_sizes_checked':[1,70]},
        'remaining':['9J accepted release required for final 9M3 rerun','9L14 production integration and integrated 9O acceptance'],
        'persistence_added':False,'production_activated':False}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--reports',type=Path,default=ROOT/'composeApp/build/test-results/desktopTest');args=parser.parse_args()
    text=json.dumps(generate(args.reports),ensure_ascii=False,indent=2)+'\n'
    if args.check:assert DEST.read_text()==text,'State report differs; review and regenerate from passing tests.'
    else:DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(text)
    print('9M: 22 contracts recorded; 18 current checks pass; 4 conditional future-store cases; awaiting final release verification against accepted 9J content.')
if __name__=='__main__':main()
