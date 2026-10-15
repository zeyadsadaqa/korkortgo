# 9B2 — M01 production import

M01’s introduction, four lessons and module review are now complete in [the cumulative curriculum](../../../../../content/curriculum.json). The other 58 documents retain their exact 9B1 data. [The ledger](../../../../../content/curriculum-import-state.json) leaves 54 reading bodies pending; this staged package is not release-ready.

The import preserves 41 production paragraphs, four production objectives, five separate answers/review guides, four approved illustrations and 16 exact M01 source scopes. The [parity report](module-parity.json) accounts for every teaching fragment, caption, answer, reference label and URL across approved PDF pages 5–21. It records 216 passing checks. All 59 Python regression tests and 14 configured Kotlin/desktop tests pass.

## Reproduce

From the repository root:

```sh
python3 tools/import_curriculum_m01.py --check
python3 -m unittest discover -s tools -p 'test_*curriculum*.py'
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/implementation-evidence/9B2/jvm-test-init.gradle
```

Use the bundled Python with `pypdf` for the final check:

```sh
/Users/zeyad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 docs/curriculum/app-migration/implementation-evidence/9B2/verify_module.py
```

`--check` is read-only. `--write` reproduces this bounded import and its [manifest](staging-manifest.json), [generated Kotlin](generated/GeneratedCurriculum.kt) and [trace](trace.json). It refuses to replace edited M01 documents. Earlier step verifiers/manifests describe their frozen historical payloads; do not rewrite them to match this cumulative import.

## Retained structure and limits

- Source origins use exact production file hashes and paragraph lines. Block IDs are explicitly assigned in the importer, independently of wording and PDF pagination.
- All four lesson checks and the module review guide use `after_deliberate_reveal`, outside teaching body blocks. Worked decisions remain visible teaching. Runtime semantics/focus verification belongs to the reader implementation.
- The source payload is a bounded staging dependency, with 16 M01 scopes. Four licensing URLs are curriculum-only and absent from the question registry; the compiler requires their deterministic URL identity, exact 7B scope, and a frozen source-check record. Dates remain 4/12 October 2026; unknown publication dates stay null. Foreign authorities retain their limitations. Historical parliamentary material is classified separately from legislation. The hypothetical microsleep arithmetic is explicitly marked editorial inference.
- Original artwork bytes are retained. `BlockPayload.CroppedImage` carries an `ApprovedImageRegion` in source pixels: top-left origin, right/bottom exclusive, including original sheet dimensions. Clip that window, then contain it without stretching or further cropping. The validator rejects invalid bounds and use on official signs. Compose resource bundling, rendered delivery and device checks remain 9C4/later work.
- PDF running headers, folios, blank writing lines and print navigation are not teaching blocks. Chapter contents are canonical links; document titles are metadata. The repeated reference-date notice is retained once on the module introduction; exact sources are staged rather than duplicating four print reference pages. The answer-page heading is presentation furniture; complete answers remain separate records.

No app screen, learner progress, question bank, official sign or PDF source was changed. No new design was requested or generated. Next: **9B3 — M02**, separately requested.
