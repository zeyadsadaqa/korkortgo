package se.korkort

/** Runs only against the staged compiler fixture; it is not part of the app source set. */
fun main() {
    val p = fixture9A3
    check(p.manifest.identity.contentVersion == "fixture-9A3-unscored")
    check(p.curriculum.modules.single().lessonIds.map { it.value } == listOf("M03-L01", "M03-L02", "M03-L03", "M03-L04"))
    check(p.curriculum.documents.size == 6)
    val lesson = p.curriculum.documents.single { it.id.value == "M03-L02" }
    val knowledgeCheck = lesson.bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.KnowledgeCheck>().single()
    check(lesson.answerBlocks.single().metadata.id == knowledgeCheck.answerId)
    check(lesson.bodyBlocks.none { it.metadata.id == knowledgeCheck.answerId })
    val requirement = lesson.bodyBlocks.map { it.payload }.filterIsInstance<BlockPayload.Paragraph>().single { it.role == TeachingRole.REQUIREMENT }
    check((requirement.text.single() as InlineContent.Text).text.startsWith("Follow the traffic instructions that apply to you."))
    val sign = p.curriculum.signEntries.single()
    check(sign.code == "B1" && sign.officialNameSv == "Väjningsplikt")
    val asset = p.curriculum.assets.single()
    check(asset.original.sha256 == asset.bundled.sha256)
    check(asset.original.sha256.value == "4c006030d1ffaa641df7e62f23b08187d545f9f777e1fe99afb2e98a6f5b6f5b")
    check(p.sources.destinations.map { it.id.value } == listOf("source-traffic-law", "source-sign-law"))
    val q = p.questions.questions.single()
    check(q.key.questionId.value == "situation-001" && q.acceptance.eligibility == ScoringEligibility.UNREVIEWED)
    check(q.options.single { it.id == q.feedback.correctOptionId }.text == listOf(InlineContent.Text("Stop as directed by the officer.")))
    check(q.options.map { it.id }.distinct().size == 4)
    check(p.legacyAliases.aliases.single().outcome == AliasOutcome.Content(ContentTarget(ContentId("M03-L02"))))
    println("PASS: generated Kotlin constructs the exact unscored M03/B1/question/source fixture.")
}
