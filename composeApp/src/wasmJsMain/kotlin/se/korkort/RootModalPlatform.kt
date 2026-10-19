package se.korkort

import kotlinx.browser.document

internal actual val singleLayerBrowserModals: Boolean = true
/** Keep the existing DOM subtree alive: Compose 1.9.3 cannot recreate hidden
 * semantics IDs after clearAndSetSemantics removes them from its web map. */
internal actual fun setBrowserModalAccessibility(active:Boolean) {
    document.body?.shadowRoot?.querySelector("#cmp_a11y_root [aria-label='Application content']")
        ?.setAttribute("aria-hidden",active.toString())
}
