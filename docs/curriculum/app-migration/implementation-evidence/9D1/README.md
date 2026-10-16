# 9D — Assessment identity, reveal semantics and neutral descriptions

User authorization: all 9D steps, 16 October 2026. Execution review: [review.md](review.md).

## Deliverables

- **9D1:** [authored identity ledger](authored-identities.json) assigns option IDs to all 1,000 frozen original questions before any display shuffle. Sign IDs match the exact 7D proposals. `legacy-r1` identifies baseline semantics in this ledger; rewrites receive their separately reviewed revisions in 9E/9F. `AssessmentEngine`, `SessionQuestionSnapshot` and `AssessmentSession` select, shuffle, confirm and score using authored IDs and exact semantic revisions. The compiler rejects replacement display-based IDs even if the key/feedback are changed to agree. Equal learner labels are allowed; distinct visual assets are checked independently.
- **9D2:** `AssessmentCard` consumes the session's restricted presentation. Code, labels, correctness and explanations are absent before reveal. Each image has a dedicated physical description; its parent clears renderer-provided accessibility semantics. Radio controls use Foundation selection/focus behavior and stable option keys. Focus moves to the saved-answer status or feedback after confirmation. The feedback block is announced politely. Immediate feedback requires confirmation; end feedback requires finishing the session. Interim score is unavailable.
- **9D3–9D15:** exact backlog batches, each with `description-acceptance.json`. The [separate authored description library](../9D2/physical-descriptions.tsv) covers 308 images and all 1,540 occurrences across 616 proposed questions. Records include each stem, all four options, exact image hashes and visual-review evidence. Meaning options intentionally contain possible meanings; recognition choices use position letters and physical descriptions. Actual printed text, such as STOP, E4 or R1, remains part of the visible picture; it is distinct from the sign's source code. No interpretation is appended to that text.

These are assessment components and review inputs, not bank activation. The app's existing routes continue to use the legacy bank until the planned 9J/9L integration. The existing 38 faint-artwork question holds remain open. Desktop headless keyboard/semantics checks do not establish Android, iOS, web, screen-reader-device or intended-size image delivery acceptance. The component's default text renderer provides equivalent description access; platform image rendering and zoom are later 9L work. No new UI design or preview approval is claimed.

## Reproduce

From the repository root:

```sh
python3 tools/prepare_assessment_9d.py --check
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 docs/curriculum/app-migration/implementation-evidence/9D1/build_fixture.py
JAVA_HOME='/Users/zeyad/Library/Java/JavaVirtualMachines/ms-17.0.16/Contents/Home' \
  ./gradlew :composeApp:desktopTest --offline --no-daemon \
  --init-script docs/curriculum/app-migration/implementation-evidence/9D1/jvm-test-init.gradle
python3 docs/curriculum/app-migration/implementation-evidence/9D1/verify_assessment.py --check
```

`prepare_assessment_9d.py` writes records only when `--check` is omitted. It never changes the question bank, curriculum, source art, histories or acceptance state. It does not author descriptions automatically: wording comes from the separately reviewed TSV.

`build_fixture.py` uses the exact retained 9A3 fixture and source authority, refreshes only implementation input hashes, and stages a new manifest, Kotlin package and trace under 9D1. The question stays unreviewed. Compile this fixture separately from older generated packages that share Kotlin file basenames.

For fresh PDF/detail inspection, run `../9D2/render_review.py` with Python/Pillow and Poppler installed. It renders source files without changing their bytes. Retained paired sheets were inspected for all 308 approved images; vector/fine-text details are saved in [visual-review](../9D2/visual-review/). No generated replacement artwork was used.

Next group: 9E, separately authorized.
