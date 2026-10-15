# 9A3 — Deterministic generation and validation review

**Executed:** 15 October 2026. **Status:** Complete. **Authorization:** “ok go ahead with next step” following 9A2.

[Usage and validation boundary](README.md) · [Verification](verification.json) · [Exact trace](trace.json) · [Golden hashes](golden.json) · [Incoming review](incoming-review.json)

Implemented schema-1 validation and staged Kotlin generation through `tools/build_content.py compile`, supported by `tools/content_schema.py` and `tools/compile_curriculum.py`. Model fields/enums/variants come from the reviewed Kotlin declarations. Generation checks the complete typed shape and cross-record identities, sources, assets, module order/tags, separate answers, question/option/revision/eligibility bindings, manifests and legacy aliases before writing outputs. Source authority prevents rehashing changed approved inputs into apparent acceptance. Sources, payloads and output paths are explicit; there is no runtime loader or new dependency.

The historical generation code is now inside an explicit `legacy` command. Its AST is unchanged; importing the module or invoking it without a subcommand cannot rewrite the bank. No legacy generation was executed. No live app content, question bank, source registry, official artwork, PDF or production build configuration was edited.

The incoming Quiz.kt contains an explicit `JvmInline` import and annotation formatting from before this task. A bounded review confirms normalization gives exactly the accepted 9A2 source hash; the file is preserved unchanged. Earlier verification records and expected hashes remain intact. The [incoming review](incoming-review.json) records those facts and the preserved historical generator AST identity. Intentional tool/plan evolution is recorded separately from frozen teaching/design inputs.

## Fixture and acceptance evidence

Saved four schema-1 authoring files plus their manifest, a deterministic selection adapter and generated common Kotlin in this step's directory. The bounded fixture includes six M03 reading nodes with approved excerpts, the exact separate amber answer, an original structured table, RB02/B1 and its exact verified bytes, scoped source records and unchanged situation-001 text. Its ten imported destinations and one unreviewed question are expressly not a complete module/curriculum or accepted active pool. Option-ID assignment is explicit authoring metadata for this fixture only.

The final **44 Python tests pass**. They exercise golden manifest hashing, repeatable output, trace pointers/line numbers, invalid/duplicate canonical and option IDs, key/feedback associations, source scopes, source drift despite rehashing, table/answer structure, missing/unknown fields, paths/origins/dates, manifest coverage, retained wording, legacy choices/namespaces, output ownership and release rejection of this partial fixture. Saved log: [python-tests.log](python-tests.log).

The generated fixture was compiled and exercised using the project's configured Kotlin 2.2.20 compiler through a temporary desktop test source set. **All 12 tests pass:** six existing quiz regressions, five contract tests and one generated-value test calling [FixtureProbe.kt](FixtureProbe.kt). The probe checks exact M03 titles/IDs, requirements text, separate answer identity, source bindings, B1 caption/name/hash and the unchanged situation-001 key/options. Saved logs/reports: [Gradle build](gradle-tests.log), [generated fixture test](TEST-se.korkort.GeneratedFixtureTest.xml), [quiz tests](TEST-se.korkort.QuizTest.xml), [contract tests](TEST-se.korkort.CurriculumContractTest.xml). A standalone compile/run additionally checked the constructor output; it is not platform/device certification.

Repeated builds of the same saved inputs produce byte-identical Kotlin files and source/output trace. [verify_generator.py](verify_generator.py) independently regenerates into a temporary directory, compares the saved golden hashes, rechecks preserved inputs and reads the retained test evidence. It writes only this step's verification.json. Its checks do not rerun the Python/JVM suites; their saved reports are distinguished from the fresh deterministic-generation checks.

## Reproduction and handoff

The exact authoring/compile/test commands and source-authority policy are in the [README](README.md). The temporary test source set is configured only by the supplied init script for that invocation. Generated fixture files are not added to production source sets. The Kotlin models in Curriculum.kt remain handwritten; generated payload constructors use GeneratedCurriculum.kt and numbered parts.

No blocking generator issue remains. Text completeness/production corrections and full import parity remain 9B work; detailed source/asset import remains 9C; neutral descriptions and runtime identity/reveal integration remain 9D; per-ID acceptance and the 38 image holds remain 9E–9J/9F. Actual UI/state/navigation/platform verification remains in its existing tasks. Release-profile validation is structural closure and eligibility checking, not final app certification.

The next executable task is **9B1 — import introductions and reading structure**, only when separately requested. No 9B import was started by this fixture work.
