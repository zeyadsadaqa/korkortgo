# 9L10 — shared accessible image viewer

Implemented Fit, labelled Zoom in / Zoom out / Reset, bounded keyboard/pointer pan and Close, with focus restoration and preserved reference scroll/pending assessment choice. The viewer fits initially, uses one uniform scale, clamps panning and never changes the underlying geometry or stroke. Controls reflow/scroll at large text sizes. Study titles/captions stay separate from assessment projections; pre-answer viewers use only the reviewed neutral description and “Question illustration”.

All 18 retained official PDFs are decoded into exact path/clip/stroke/fill commands by pinned PyMuPDF 1.28.2. Their source PDFs remain unchanged and bundled bytes are verified at runtime. The 19th held asset, X8, uses its unchanged registered PNG. The decoder rejects unsupported source constructs. [Decoder provenance](vector-decoding.json) and [independent PDF/Compose geometry comparisons](../9F/vector-fidelity.json) retain antialiasing differences; neither artifact accepts legibility or delivery.

Actual Android verification found a zero-height Canvas inside scrolling assessment cards. The renderer now supplies a fixed drawing height when the scroll constraint is unbounded; the regression test requires painted pixels in the 105px image box. The assessment host retains its pending selection while the modal viewer is open. Focus return waits for the destination to be laid out.

[Full target evidence, replay commands and remaining acceptance requirements](../9F/README.md). Renderer/fixture implementation is ready; reader/delivery acceptance (user selected iOS simulator scope) and integrated route activation remain outstanding. No question hold is released by these implementation checks.
