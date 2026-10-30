package se.korkort

import kotlin.test.*
import se.korkort.progress.LessonProgress

class NavigationLearningTest {
    @Test fun allDestinationsBelongToTheExpectedTab() {
        assertEquals(StudyTab.HOME,tabFor(AppDestination.Home))
        assertEquals(StudyTab.LEARNING,tabFor(AppDestination.Library))
        assertEquals(StudyTab.LEARNING,tabFor(AppDestination.Content(ContentTarget(ContentId("M03-L03")))))
        assertEquals(StudyTab.LEARNING,tabFor(AppDestination.SignCatalogue))
        assertEquals(StudyTab.EXERCISE,tabFor(AppDestination.QuizSetup))
        assertEquals(StudyTab.EXERCISE,tabFor(AppDestination.Quiz("session")))
        assertEquals(StudyTab.EXERCISE,tabFor(AppDestination.Results("session")))
    }
    @Test fun onlyCurrentTeachingLessonRevisionsCountAsRead() {
        val lesson=readerDocuments.first{it.kind==DocumentKind.LESSON}
        val review=readerDocuments.first{it.kind==DocumentKind.MODULE_REVIEW}
        fun row(id:ContentId,revision:String,read:Boolean=true)=LessonProgress("profile",id.value,revision,read)
        assertEquals(setOf(lesson.id),readLessonIds(listOf(row(lesson.id,lesson.revision.value),row(review.id,review.revision.value)),readerDocuments))
        assertTrue(readLessonIds(listOf(row(lesson.id,"old")),readerDocuments).isEmpty())
        assertTrue(readLessonIds(listOf(row(lesson.id,lesson.revision.value,false)),readerDocuments).isEmpty())
    }
    @Test fun learningSourceBackRestoresTheReadingOrigin() {
        val route=LearningRouteState()
        val target=ContentTarget(ContentId("M03-L03"))
        route.target.value=target
        route.origin.value=ReturnContext(target,null,null)
        route.source.value=navigationSources.references.first().id
        assertTrue(route.canBack)
        route.back();assertTrue(route.directory.value);assertNull(route.source.value)
        route.back();assertFalse(route.directory.value);assertEquals(target,route.target.value)
        route.back();assertNull(route.target.value);assertFalse(route.canBack)
    }
}
