# 9B3 — M02 production import

M02’s introduction, four complete lessons and review are imported into [the cumulative payload](../../../../../content/curriculum.json). All 58 other documents, including M01 and the opening text, retain their incoming data. The [ledger](../../../../../content/curriculum-import-state.json) leaves 48 reading bodies pending.

The import retains 46 source blocks (including a three-column, four-row symptom/action table), four lesson objectives, five hidden answers/review guides, six illustrations and 19 M02 source scopes. The cumulative package contains 33 source destinations/references and ten illustration bindings. [Module parity](module-parity.json) records 243 passing checks across approved PDF pages 22–40. All 74 Python regression tests and 15 configured Kotlin/desktop tests pass.

## Reproduce

From the repository root:

```sh
python3 tools/import_curriculum_m02.py --check
python3 -m unittest discover -s tools -p 'test_*curriculum*.py'
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' ./gradlew :composeApp:desktopTest --offline --no-daemon --init-script docs/curriculum/app-migration/implementation-evidence/9B3/jvm-test-init.gradle
/Users/zeyad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 docs/curriculum/app-migration/implementation-evidence/9B3/verify_module.py
```

`--check` is read-only. `--write` regenerates this bounded import, [manifest](staging-manifest.json), [Kotlin](generated/GeneratedCurriculum.kt) and [trace](trace.json); it rejects edited M02 documents/illustrations and rolls authoring data back if staging fails. The incoming payload/state snapshots match the saved 9B2 artifact hashes. Previous evidence is preserved. The M01 regression harness uses these exact pre-M02 bytes and temporary in-memory manifest identities, so cumulative imports do not invalidate historical content tests.

## Structure and rendering contract

Every block retains a stable authored ID and exact production origin. All five answers are outside body blocks with `after_deliberate_reveal`. Worked decisions and practice examples remain visible teaching. Production order is retained, including M02-L02’s practice example after its worked decision. Table headers and cells retain their row order and the M02-L02 link.

Four images use the existing rectangular `CroppedImage` contract. Two require the additive `PolygonImage` contract to reproduce approved clipping without exposing surrounding lettering or panels. It carries the original sheet identity, `ApprovedImageRegion`, an ordered list of absolute `SourcePixelPoint` vertices and the exact caption. Coordinates have a top-left origin. Close the polygon, mask pixels outside it to transparency, then aspect-fit the full region without distortion or further cropping. Validation requires three or more distinct vertices within the region and nonzero area, and rejects use on official signs. Original image bytes, alt text, production widths/resolution and clipping provenance remain bound. App resource packaging and actual rendering/device checks remain 9C4/later work.

All M01 source scopes and evidence remain. Shared URLs accumulate M02 scope/evidence without losing earlier dates. Manufacturer handbooks, foreign authorities, hosted VTI research, Swedish legislation and authority advice remain distinct. Source checks dated 4 and 12 October remain separate; unknown publication dates are null. The Volvo example is model-specific, and the maritime fuse page supports only the electrical principle. No new source-currency claim is made.

PDF running headers, folios, blank writing lines and print navigation are presentation furniture. Chapter contents use canonical links. Document titles are metadata, the repeated source-date notice is retained once in the module introduction, and complete print answers/references become separate typed records. The parity checker accounts for all remaining PDF text, captions and exact URLs.

This is a staged data import. No live screen, bank, learner state, official sign or source PDF was changed. Next: **9B4 — M03**, separately requested.
