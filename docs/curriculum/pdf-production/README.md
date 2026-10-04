# KörkortGo PDF production

**Step 6A started:** 3 October 2026. **Status:** Readiness checked; production blocked.

The execution request authorises 6A. Its saved entry requirements are not yet satisfied, so no finished opening PDF, renderer or reusable page templates are claimed here. The approved cover and navigation remain approved; this check does not request their approval again.

## Files prepared

- [Readiness review](readiness-review.md): current entry requirements and unfinished 6A work.
- [Build manifest](build-manifest.json): ten original chapter titles, 40 lesson IDs, ten review IDs, appendix destinations, shared page/font settings and dated input hashes.
- [Preflight](preflight.py): validate chapter coverage and input hashes; report the saved production hold. Run `python3 docs/curriculum/pdf-production/preflight.py` from the repository root. Exit 2 means the documented readiness hold remains, 1 means integrity failure, and 0 is reserved for a future cleared implementation.

This is a production preparation package, not the editable PDF renderer promised by 6A. Chapter content continues to come from the manuscript, with official image bindings supplied by the sign package. Do not copy teaching text or sign artwork from generated preview boards.

## Resume 6A

Resolve the outstanding requirements in the readiness review, then pin the actual Source Serif 4 and Source Sans 3 font files and licences. Implement the approved opening pages and shared templates using the PDF workflow. Save `front-matter.pdf`, editable build source, exact build commands and dependency versions; render and inspect every opening page, verify embedded fonts/selectable text and the full disclaimer. Record actual results before marking 6A complete. Final book folios are assigned in 6M; the manifest deliberately has no invented page numbers.
