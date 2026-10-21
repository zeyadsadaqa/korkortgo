package se.korkort
    internal fun teachingSegments10I(p:BlockPayload):List<String> = when(p) {
        is BlockPayload.Heading -> listOf(p.text.assessmentText())
        is BlockPayload.Paragraph -> listOf(p.text.assessmentText())
        is BlockPayload.Table -> p.columns.map{it.heading.assessmentText()} + p.rows.flatMap{it.cells.map{c->c.assessmentText()}} + listOfNotNull(p.caption?.assessmentText())
        is BlockPayload.ListItems -> p.items.flatten().flatMap{teachingSegments10I(it.payload)}
        is BlockPayload.Scenario -> listOfNotNull(p.title?.assessmentText())+p.blocks.flatMap{teachingSegments10I(it.payload)}
        is BlockPayload.Callout -> listOfNotNull(p.title?.assessmentText())+p.blocks.flatMap{teachingSegments10I(it.payload)}
        is BlockPayload.KnowledgeCheck -> p.prompts.flatMap{teachingSegments10I(it.payload)}
        is BlockPayload.Equation -> listOf(p.expression,p.assumptions.assessmentText())
        is BlockPayload.RelatedLinks -> p.links.map{it.label.assessmentText()}
        is BlockPayload.Image -> listOf(p.caption.assessmentText())
        is BlockPayload.CroppedImage -> listOf(p.caption.assessmentText())
        is BlockPayload.PolygonImage -> listOf(p.caption.assessmentText())
        is BlockPayload.CompositeImage -> listOf(p.caption.assessmentText())
        is BlockPayload.SignExamples -> p.entryIds.flatMap{id->val s=navigationSigns.single{it.id==id};listOf(s.caption.assessmentText(),readerAssets.single{it.id==s.assetId}.studyAltText)}
    }.filter{it.isNotBlank()}
