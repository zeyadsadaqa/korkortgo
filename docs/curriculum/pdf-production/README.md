# KörkortGo PDF build

Step 6A completed on 4 October 2026. Four opening pages are built from the approved cover/navigation direction and unchanged manuscript introduction. This is a screen-review PDF; chapter production proceeds separately by module. All ten chapters (6B–6K) and the reference material (6L) are now built and verified.

## Reproduce

Run from the repository root with Python 3.12 and the pinned packages in `requirements.txt`:

```sh
python3 docs/curriculum/pdf-production/preflight.py
python3 docs/curriculum/pdf-production/build.py
python3 docs/curriculum/pdf-production/verify.py
pdftoppm -scale-to 1600 -png docs/curriculum/pdf-production/front-matter.pdf tmp/pdfs/6a/page
```

The available bundled interpreter is `/Users/zeyad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. Fonts and licences are local, so the build does not need a network connection. If Poppler on macOS needs font configuration, set `FONTCONFIG_FILE` to a local configuration containing `/System/Library/Fonts` and `/Library/Fonts`.

`build.py` writes [front-matter.pdf](front-matter.pdf) and the identical delivery copy at `../../../output/pdf/korkortgo-front-matter.pdf`. Its invariant build produces identical bytes on rerun with the pinned dependencies. `verify.py` checks that property, full introductory paragraphs, exact disclaimer, all chapter/appendix titles, embedded Unicode fonts, Swedish glyphs, internal links, bookmarks, page bounds and approved-preview hashes.

## Editable inputs and reusable components

- [Manuscript](../manuscript.md): authoritative teaching text; introductory prose is extracted directly, not copied from imagegen.
- [Build source](build.py): A4 page frame, token-based colours, registered font families, heading/body/caption/reference styles, automatic-height panels, lesson-heading component and repeated-header reference tables. Text overflow raises an error instead of shrinking the type.
- [Font manifest](fonts/manifest.json): Adobe Source Sans 3 release 3.052R and Source Serif 4 release 4.005R, source URLs, hashes and bundled OFL licences.
- [Asset bindings](asset-bindings.json): exact approved cover reference plus canonical chapter/sign bindings. The cover uses native PDF clipping; its generated text is excluded and replaced with selectable typography.
- [Navigation](navigation.json): actual opening-page destinations plus reserved chapter, lesson, review, appendix and reference IDs. Chapter links and contents folios are attached only when target pages exist in 6M. No fictitious page numbers or broken chapter links appear in this partial PDF.
- [Build manifest](build-manifest.json): source hashes and per-chapter production status.

## Later chapter builds

Reuse the shared page frame, fonts, styles and panels. Add all manuscript content, exact official signs and approved scene crops. Keep questions and answers on separate, non-facing pages; verify parity again after assembly. Do not publish whole raster preview boards as lesson pages. Render every newly built page and inspect scenario meaning and actual-size legibility. Caption and alternative text must describe the actual final illustration.

## Review and limits

See [readiness/render review](readiness-review.md) and [machine checks](verification.json). This is not a print-ready release: the approved cover raster is approximately 95 ppi at this size. Final tagged-PDF accessibility, chapter sign placement, cross-book navigation and final folios remain in their planned production stages. No chapter or app migration was executed in 6A.

## Completed chapters

- [Chapter 1 review](chapters/M01/review.md): 6B complete, 15 pages, four lessons and one self-assessment. Build with `python3 docs/curriculum/pdf-production/chapters/M01/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 2 review](chapters/M02/review.md): 6C complete, 15 pages, four lessons and one self-assessment. Build with `python3 docs/curriculum/pdf-production/chapters/M02/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 3 review](chapters/M03/review.md): 6D complete, 50 pages, four lessons, self-assessment, seven approved scene placements and 100 exact official sign/signal/marking placements. Build with `python3 docs/curriculum/pdf-production/chapters/M03/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 4 review](chapters/M04/review.md): 6E complete, 42 pages, four lessons, self-assessment, 20 approved scene placements and 46 exact official reference placements plus nine scene sign insertions. Build with `python3 docs/curriculum/pdf-production/chapters/M04/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 5 review](chapters/M05/review.md): 6F complete, 44 pages, four lessons, self-assessment, nine scene placements, separate parking-time exercise/worked review and 62 official reference placements. Build with `python3 docs/curriculum/pdf-production/chapters/M05/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 6 review](chapters/M06/review.md): 6G complete, 48 pages, four lessons, self-assessment, 13 approved scene placements and 76 exact official reference assets. Build with `python3 docs/curriculum/pdf-production/chapters/M06/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 7 review](chapters/M07/review.md): 6H complete, 23 pages, four lessons, self-assessment, eight approved scene placements and six exact official reference assets. Build with `python3 docs/curriculum/pdf-production/chapters/M07/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 8 review](chapters/M08/review.md): 6I complete, 29 pages, four lessons, self-assessment, four approved scenes, nineteen official reference assets and eight official marker-face insertions. Build with `python3 docs/curriculum/pdf-production/chapters/M08/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 9 review](chapters/M09/review.md): 6J complete, 22 pages, four lessons, self-assessment, four approved scenes, ten official reference assets and one exact official zone-sign insertion. Build with `python3 docs/curriculum/pdf-production/chapters/M09/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

- [Chapter 10 review](chapters/M10/review.md): 6K complete, 23 pages, four lessons, eight approved scenes, five native review frames, ten official reference assets and two exact official scene insertions. Build with `python3 docs/curriculum/pdf-production/chapters/M10/build_chapter.py`; verify with the adjacent `verify_chapter.py`.

## Completed reference material (6L)

[Reference review](reference-material-review.md): 183 pages containing appendices A–D, all 24 sign groups with 321 unique official entries, glossary, practice record and 66 official references. The editable [builder](reference/build_reference.py) extracts the manuscript appendices and writes a [source snapshot](reference/reference-source.md), asset bindings and navigation records.

```sh
python3 docs/curriculum/pdf-production/reference/build_reference.py
python3 docs/curriculum/pdf-production/reference/verify_reference.py
mkdir -p tmp/pdfs/6l
pdftoppm -scale-to 1400 -png docs/curriculum/pdf-production/reference-material.pdf tmp/pdfs/6l/page
```

The builder writes `reference-material.pdf` and an identical delivery copy at `output/pdf/korkortgo-reference-material.pdf` from the repository root. [Source checks](reference/source-checks.json) and [link checks](reference/link-checks.json) distinguish historic factual checks from link availability on 7 October 2026. Final book navigation and folios remain 6M work; final accessibility and publication verification remain 6N.

## Complete book assembly (6M)

The [complete review PDF](korkortgo-curriculum-review.pdf) combines 498 pages with continuous printed folios, clickable contents, nested bookmarks, lesson/sign cross-links and Contents/Sources access on every interior page. See the [assembly review](assembly/assembly-review.md), [verification](assembly/verification.json) and [render comparison](assembly/render-comparison.json).

```sh
python3 docs/curriculum/pdf-production/assembly/build_book.py
python3 docs/curriculum/pdf-production/assembly/verify_book.py
```

The editable builder imports the verified standalone parts, preserves their artwork and text, and replaces the contents/footer navigation. `assembly/inputs.json` records component hashes and offsets; `assembly/navigation.json` records final destinations and folios. `assembly/cross-link-candidates.json` caches text geometry against all input hashes; pass `--refresh-navigation` to regenerate it, and it regenerates automatically when inputs change. No source PDF is modified. The delivery copy is `output/pdf/korkortgo-curriculum-review.pdf`.

The assembly check verifies preserved text, every original body link, all new navigation, fonts, question/answer separation and deterministic output. All pages were rendered and their body regions compared with source renders; the contents and section boundaries were inspected visually. Final whole-book publication and accessibility verification remain step 6N.
