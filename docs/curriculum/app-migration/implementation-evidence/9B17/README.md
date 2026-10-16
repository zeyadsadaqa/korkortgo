# Complete 9B import and required 9C data prerequisites

The user authorized all remaining 9B steps after 9B3. M03–M10, all four appendices, 24 reference groups and all supporting destinations are imported. Because 9B17 explicitly requires 9C1–9C4, the source metadata, sign captions/bindings and exact artwork bundles were completed as prerequisites in the same batch.

The [curriculum](../../../../../content/curriculum.json) and [source payload](../../../../../content/sources.json) contain exactly **1,123 published destinations**: 88 curriculum destinations, 400 signs, 116 sources and 519 supporting destinations. The technical representation has 91 documents, 24 groups, 400 sign entries, 116 source destinations and 492 anchors; 27 supporting destinations are actual front-matter/source/answer-hub documents. All 60 reading nodes have complete bodies, all 40 lessons retain objectives/tags and all 50 answers/review guides remain separate and deliberately revealed.

All **2,538 independent checks, 83 Python tests and 15 configured Kotlin/desktop tests pass**. See [independent parity](import-parity.json), [production extraction check](pdf-extraction-verification.json), [source/block allocations](allocation-ledger.json), [diagnostics/range coverage](import-diagnostics.json), [manifest](staging-manifest.json), [generated Kotlin](generated/GeneratedCurriculum.kt) and [trace](trace.json). Each remaining 9B step has a bounded report in its sibling evidence directory; all use this same cumulative generated package.

## Reproduce

From the repository root:

```sh
/Users/zeyad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/import_curriculum_remaining.py --check
python3 -m unittest discover -s tools -p 'test_*curriculum*.py'
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/implementation-evidence/9B17/jvm-test-init.gradle
/Users/zeyad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 docs/curriculum/app-migration/implementation-evidence/9B17/verify_import.py
```

`--check` reproduces the complete payload and checks bundled bytes without writing. `--write` rebuilds from the hash-verified incoming 9B3 snapshot and frozen production inputs, rejects edited authoring payloads and refuses resource collisions. Running with neither flag writes diagnostic evidence only. Previous step verifiers describe historical payloads and must not be used to overwrite prior reports. The M01/M02 regression harnesses now use their exact retained snapshots and refreshed in-memory tool/model identities.

## Fidelity and representation

- This batch retains 388 complete source blocks, including complete tables/lists, and 946 additional actual production text fragments. Source paragraphs retain rich emphasis, exact source links, shorthand lesson relationships, scenarios and checks. Table headers/cells and list item order remain structured. Approved chapter additions and the final page-193 wildlife correction are retained.
- Every non-whitespace character of production pages 41–578 is accounted for once as teaching, shared sign-card content or explicitly listed printed metadata. All 578 pages were freshly extracted and compared with the retained extraction. PDF navigation controls, running headers/folios and blank writing space are presentation furniture. Original document titles remain metadata. All additional production text retains a source PDF identity and physical evidence page.
- The 729 official examples use `SignExamples` and shared canonical sign records rather than copied artwork/captions. Reference membership/order comes from final production records, not the older selection shortlist. `entryIds` describes membership/search; body `SignExamples` retains production placement. A renderer must not append a second copy of the same cards after rendering those placements. F31a remains case-sensitive. No SIG16–18 sign entries were invented.
- Sources retain all 404 question URL identities plus other required curriculum/caption evidence: 516 exact URL records in total. All 116 source destinations retain exact module scopes. Original and subsequent evidence dates remain distinct; unknown dates remain null. Commercial, manufacturer, foreign, public-service, research, legislation and parliamentary material stay distinguished. Hostname-based attribution is marked as inference when retained publisher text is absent. No fresh source-currency claim is made.
- All 484 asset bindings point to byte-identical bundled originals: 400 signs and 84 contextual placements including the approved cover landscape. These reuse 419 physical files. Crops/polygon masks retain absolute original-pixel coordinates. `CompositeImage` retains white-backed overlays with exact official artwork or editable labels, in production order. Clip the original region, apply the recorded overlays and contain without distortion; do not render generated placeholder signs. Approval/reuse records, captions, alt text and size/resolution constraints remain attached.
- Supporting continuation anchors point to actual content blocks. Module answer hubs expose links to all five separate answers, and source hubs retain scoped references. These are published support destinations, excluded from top-level module cards. No learner history or completion storage was introduced.

The complete reading package is staged and compiles, but assessments are empty in this staging fixture. Live questions and all acceptance/delivery holds remain untouched. Runtime reader semantics, actual platform legibility, source currency and release acceptance remain later work. Next: **9D1**, when requested.
