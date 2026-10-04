# KörkortGo design guide

**Version:** 1.0 · **Updated:** 2 October 2026.  
**Status:** Shared design direction accepted for documentation following the user's “Great, update the md files … to have a design guide”. This records the palette and typography direction; it does not implement an app theme or approve every book layout. Exact font rendering, component states and print output still require production verification.

## Identity and source of truth

KörkortGo is calm, clear and approachable: Scandinavian landscapes, forest-green actions, light surfaces, editorial serif headings and readable sans-serif supporting text. Always spell the name **KörkortGo**, with ö and capital K and G.

The visual references are [Learn and prepare](../mockups/01-learn-and-prepare.png) and [Practise and review](../mockups/02-practise-and-review.png). Their [original prompts](../mockups/prompts.md) explicitly specify forest and paper colours. Existing colour constants in [App.kt](../../composeApp/src/commonMain/kotlin/se/korkort/App.kt) supply the other core values. The mockups are visual references only: do not reuse their old platform name, source-book citations, page references or illustrative statistics.

Use [tokens.json](tokens.json) for exact sRGB values and type sizes, [Material roles](material-roles.md) for app mappings, and this guide for usage. The [visual board](palette-preview-v1.png) and [imagegen prompt](preview-prompt.md) illustrate the direction. Generated swatches and letterforms are approximate; the JSON values take precedence. The board's extra road logo, Swedish sample prose, progress counts and app components are illustrative, not approved content or a final logo. The book remains English-language.

## Core palette

| Colour | sRGB hex | Use |
|---|---|---|
| Forest | `#173E32` | Brand, cover title, primary actions, links and selected controls |
| Paper | `#F7F8F3` | App background and screen-reading book background |
| Sage | `#E7EEE5` | Selected surfaces, supporting panels and quiet emphasis |
| Ink | `#172C29` | Main text and informative icons |
| Muted | `#61706B` | Secondary text on Paper or white only |
| Line | `#D5DED5` | Decorative dividers and nonessential card boundaries |
| Ochre | `#E7BD4A` | Small highlights and learning-note accents, with dark text |
| Error | `#9A332F` | Error/incorrect text, paired with written feedback |
| Error container | `#FFEDEA` | Light error surface |

Let light surfaces dominate; use forest for hierarchy and actions, sage for grouping, and ochre sparingly. Avoid gradients, large saturated backgrounds and unnecessary shadows. Never recolour official road-sign illustrations to fit the brand.

## Book and editorial accents

These exact values are newly defined approximations of the preferred first-draft opening-page treatment, not recovered original source tokens.

| Colour | sRGB hex | Use |
|---|---|---|
| Navy | `#102B46` | Opening-page headings, body and icons; optional editorial heading treatment |
| Mist | `#C5D7DF` | Blue icon backgrounds and supporting illustration areas |
| Sand | `#E8DCCB` | Warm icon backgrounds and quiet callouts |
| Cream | `#F5EDDF` | Learning-aid disclaimer and editorial note panels |
| Gold | `#A47D3B` | Decorative outline of the cream panel; not small body text |

Retain the driving cover's forest-green identity and illustrated car on a Swedish lakeside road. The opening page uses navy, cream/gold and blue/sage/sand accents, as requested in [5B version 4](../../docs/curriculum/pdf-design/5b/review.md). These are compatible editorial accents, not a replacement app primary colour. Other page treatments remain subject to their planned previews.

For economical print editions, use white paper instead of printing a full ivory background. Keep coloured callouts restrained, check grayscale readability and proof actual-size pages. Hex values are sRGB; do not treat them as universal CMYK recipes. Use the printer's profile when preparing a print-specific export.

## Typography

The supplied mockups do not identify an exact font family. Their prompts specify serif headings and sans-serif body text; the current app uses generic `FontFamily.Serif` and default body typography. The following is a reproducible interpretation of that style, not an exact font identification.

- **Source Serif 4:** brand wordmark text, editorial display headings, module and lesson headings. Use semibold 600 and bold 700 for hierarchy; regular 400 is available for larger display roles.
- **Source Sans 3:** body text, captions, navigation, controls and data. Use regular 400 for reading and semibold 600 for labels and emphasis.

Adobe describes [Source Serif](https://github.com/adobe-fonts/source-serif) as a companion to Source Sans and [Source Sans](https://github.com/adobe-fonts/source-sans) as designed for user-interface environments. Preserve the font distribution's licence files when bundling fonts. Before production, pin actual font files and versions, verify their licence and PDF embedding, and test **KörkortGo · Å Ä Ö · å ä ö · 0123456789**. Imagegen is not proof of exact font rendering or glyph coverage. No font files have been installed or bundled by this documentation work.

| Book role | Family / weight | Size / line height |
|---|---|---|
| Cover title starting point | Source Serif 4 / 700 | 40 / 44 pt; scale to approved cover composition |
| Module heading | Source Serif 4 / 700 | 28 / 34 pt |
| Lesson heading | Source Serif 4 / 600 | 20 / 26 pt |
| Body | Source Sans 3 / 400 | 12 / 17 pt |
| Caption | Source Sans 3 / 400 | 10 / 14 pt |
| Source note | Source Sans 3 / 400 | 9.5 / 13 pt |

For apps, tokens.json defines all 15 Material typography roles in scalable sp. Display and headline roles use Source Serif 4; title, body and label roles use Source Sans 3. BodyLarge is 16/24 sp, BodyMedium 14/20 sp and LabelLarge 14/20 sp. Respect user font scaling and reflow; do not shrink text to prevent wrapping. For web implementations translate the scale into relative units, not fixed screenshot pixels. Book pt and app sp are separate scales.

## Material 3 usage

The [role table](material-roles.md) maps the palette to light and dark schemes following the role-based approach in [Material 3 for Compose](https://developer.android.com/develop/ui/compose/designsystems/material3). These are manually curated brand mappings, not an automatically generated tonal palette or an already integrated theme.

Use `primary` with `onPrimary` for filled actions; use container/on-container pairs together. Use `surface` and the surface-container levels for structure, `onSurface` for body text, and `onSurfaceVariant` for supporting text on tinted surfaces. Essential outlines use `outline`; pale `outlineVariant` is for decorative separators. Retain `surfaceVariant` only for compatible components that need it; prefer container roles for new surfaces.

Success, warning and info are custom semantic extensions in tokens.json, not standard Material ColorScheme fields. Selected answers use neutral sage before evaluation; correctness must include an icon and words such as “Correct” or “Review this answer”, never colour alone. Reserve red for errors and incorrect feedback, not ordinary selection. Use the dark scheme's paired values rather than placing light-theme forest text on a dark background.

Keep the documented brand scheme as the default. Dynamic colour, disabled-state opacity, hover/pressed/focus states and platform-specific behaviour require separate implementation checks; the static token report does not cover them. Use native Material component behaviour and accessible focus indicators during implementation.

## Contrast and permitted combinations

[Contrast checks](contrast-checks.json) record relative-luminance ratios for opaque sRGB pairs. Normal text targets 4.5:1; essential graphical boundaries target 3:1. This is palette validation, not whole-product accessibility certification.

**Known restricted pair:** Muted `#61706B` on Sage `#E7EEE5` is **4.40:1**, below the normal-text target. Do not use that combination for small text. Use `onSurfaceVariant` **`#495A52`** on Sage instead. The original check failure is retained in the report for transparency; the replacement pair is separately checked.

Use Ink on Ochre, Navy on Mist/Sand/Cream, and each theme's explicit on-colour with its corresponding background. Do not use white text on Ochre or pale accent colours as body text. Decorative Line and Gold are not universal accessible control outlines. Recheck any new pair, alpha blending or photographic background before use.

## Illustration and layout

Follow the mandatory [illustration instructions](illustration-guide.md) for lesson scenarios, self-assessment and signs. They define Swedish visual references, recurring cars/people/police, coverage checks and approval before book production.

Use calm editorial illustrations of cars, roads, lakes, rocks and conifers. Keep driving direction and geometry credible; a cover scene must not imply a verified traffic rule. Use official verified artwork for signs and independently reviewed diagrams for instruction. Keep the required non-official learning-aid disclaimer prominent.

Use clear hierarchy, generous whitespace, fine borders and restrained rounded cards. Avoid copying raster UI into the app or flattening text into the finished PDF. Real text, actual fonts, semantic structure, clickable references and verified image alternative text belong in implementation.

## Reuse and changes

1. Read this guide and tokens.json before creating another book or app preview.
2. Reference token names in specifications instead of choosing a similar-looking colour anew.
3. Save design revisions as new versions; obtain explicit approval before implementing new layouts.
4. Update the guide, tokens and contrast report together when values change.
5. Keep the saved mockups and previous previews as historical references.

The palette direction is documented for later reuse. This work does not start 5C, implement the app, complete the PDF or resolve the 13 required sign-image gaps.
