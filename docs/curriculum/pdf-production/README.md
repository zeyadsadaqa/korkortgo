# KörkortGo PDF build

Step 6A completed on 4 October 2026. Four opening pages are built from the approved cover/navigation direction and unchanged manuscript introduction. This is a screen-review PDF; chapter production proceeds separately by module. Chapter 1 (6B) is now built and verified.

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
