package se.korkort

import androidx.compose.runtime.Composable
import androidx.compose.runtime.key

/** Resets unconfirmed radio/viewer state when session, revision, package or order changes. */
@Composable internal fun PinnedAssessmentCard(practice: PinnedPractice, onConfirm: (PracticeQuestionToken,OptionId)->Unit) {
    val token=practice.token
    key(token) {
        AssessmentWithImageViewer(practice.assessment.presentation(),{onConfirm(token,it)},navigationAssets)
    }
}
