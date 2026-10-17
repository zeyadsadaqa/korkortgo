package se.korkort

import kotlin.test.*

class LearningViewsTest {
    @Test fun canonicalLibraryContainsEveryLessonAndRetainsNumbersWhenFiltered() {
        assertEquals((1..10).toList(),readerModules.map{it.order})
        val ids=readerModules.flatMap{it.lessonIds}
        assertEquals(40,ids.distinct().size)
        val documents=readerDocuments.associateBy{it.id}
        listOf("M01-L01","M07-L04","M10-L03").forEach{id->assertTrue(ContentId(id) in ids);assertTrue(LibraryFilter().matches(documents.getValue(ContentId(id)),readerTags))}
        val module=readerModules.single{it.order==3}
        assertEquals(listOf("M03-L02","M03-L03","M03-L04"),module.lessonIds.map{documents.getValue(it)}.filter{LibraryFilter(category=Category.SAFETY).matches(it,readerTags)}.map{it.id.value})
        val filter=LibraryFilter("zzzxq",Category.SAFETY)
        assertTrue(ids.none{filter.matches(documents.getValue(it),readerTags)})
        assertEquals(Category.SAFETY,filter.clearQuery().category)
        assertEquals("zzzxq",filter.clearCategory().query)
    }
    @Test fun allSixtyReadingNodesHaveCompleteBodiesAndSymmetricNeighbours() {
        assertEquals(60,readerOrder.size)
        readerOrder.forEachIndexed { index,id ->
            assertTrue(readerDocuments.single{it.id==id}.bodyBlocks.isNotEmpty())
            assertEquals(readerOrder.getOrNull(index-1) to readerOrder.getOrNull(index+1),readingNeighbours(id))
        }
        val document=readerDocuments.single{it.id==ContentId("M03-L02")}
        assertTrue(document.searchText().contains("green"))
        assertTrue(document.searchText().contains("guard",ignoreCase=true))
        val checks=document.bodyBlocks.mapNotNull{it.payload as? BlockPayload.KnowledgeCheck}
        assertTrue(checks.isNotEmpty())
        checks.forEach{check->assertEquals(1,document.answerBlocks.count{it.metadata.id==check.answerId})}
        assertTrue(document.answerBlocks.any{it.blocks.joinToString(" "){b->b.searchText()}.contains("unsafe stop")})
    }
    @Test fun lessonSourcesUseExactEvidenceAndNeverGlobalExamples() {
        val document=readerDocuments.single{it.id==ContentId("M03-L02")}
        val sources=lessonSources(document)
        assertTrue(sources.isNotEmpty())
        assertTrue(sources.any{it.id==SourceReferenceId("REF-9f4b74a976fa03fb")})
        assertFalse(sources.any{it.id==SourceReferenceId("REF-8994a6a11921a063")})
    }
    @Test fun page46AndSignalRecoveryPreserveExactDecisions() {
        val namespace="legacy-app-4768933c3d9a"
        val page=canonicalResolver.legacy(LegacyLookup.Page(namespace,46)) as Resolution.Choices
        assertEquals(listOf("M04-L01","M04-L02","M04-L03","M05-L01"),page.choices.map{it.target.contentId.value})
        assertEquals("M04-L03",(canonicalResolver.lookup(questionId=QuestionId("situation-017")) as Resolution.Found).target.contentId.value)
        assertEquals("M04-L01",(canonicalResolver.lookup(questionId=QuestionId("situation-103")) as Resolution.Found).target.contentId.value)
        val urls=(16..18).map{code->val r=canonicalResolver.legacy(LegacyLookup.Sign(namespace,"SIG$code")) as Resolution.Unavailable
            assertEquals(listOf(ContentTarget(ContentId("M03-L02"))),r.related)
            navigationSources.references.single{it.id==r.officialReferenceId}.url
        }
        assertEquals(3,urls.distinct().size)
        assertIs<Resolution.Unavailable>(canonicalResolver.canonical(ContentTarget(ContentId("unknown"))))
    }
}
