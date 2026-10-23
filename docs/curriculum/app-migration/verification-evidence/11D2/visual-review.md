# Android artwork visual review

Inspected the following current native captures directly:

- [View](android-152-r2/question-sign-recognise-S12-dark-1.6-pending.png) — question-sign-recognise-S12-dark-1.6-pending.png
- [View](android-152-r2/question-sign-recognise-T22-light-1.0-pending.png) — question-sign-recognise-T22-light-1.0-pending.png
- [View](android-152-r2/question-sign-meaning-X8-dark-1.0-Enlarge question image-zoom.png) — question-sign-meaning-X8-dark-1.0-Enlarge question image-zoom.png
- [View](android-152-r2/question-sign-meaning-S5-light-1.6-inline.png) — question-sign-meaning-S5-light-1.6-inline.png

The selected card has a persistent neutral border/tint and visible Selected label in both themes and large/default text; it gives no correctness feedback. Official artwork remains on white backing, thin S5 outlines are present, and the X8 enlarged viewport shows the expected 150% cropped view with available reset/close controls. The capture audit is sampled; all152 contexts separately assert actual native pending-region pixel changes, checked/selection retention, exact image readiness, each image zoom/reset/close and focus return. Fixture banners/system chrome are identified separately from normal App presentation. This does not certify normal production journeys or spoken assistive traversal.
