package se.korkort

import kotlinx.browser.document

internal actual val singleLayerBrowserModals: Boolean = true
/** Keep the existing DOM subtree alive: Compose 1.9.3 cannot recreate hidden
 * semantics IDs after clearAndSetSemantics removes them from its web map. */
internal actual fun setBrowserModalAccessibility(active:Boolean) {
    document.body?.shadowRoot?.querySelector("#cmp_a11y_root [aria-label='Application content']")
        ?.setAttribute("aria-hidden",active.toString())
}

internal actual fun updateBrowserAssessmentChoices(selectedLetter:String?,enabled:Boolean) = projectAssessmentChoices(selectedLetter,enabled,true)
internal actual fun clearBrowserAssessmentChoices() = projectAssessmentChoices(null,false,false)

/** Project state onto Compose's existing controls; never replace nodes or click handlers.
 * Observe rerenders because the bundled bridge rewrites role=button asynchronously.
 * Only a letter and enabled flag live here; no question data, correctness or persistence.
 */
private fun projectAssessmentChoices(selectedLetter:String?,enabled:Boolean,active:Boolean):Unit = js("""{
    const body = document.body;
    if (!body) return;
    const key = '__korkortChoiceProjection';
    if (!active) {
        if (body[key]) body[key].observer?.disconnect();
        delete body[key];
        return;
    }
    let state = body[key];
    if (!state) {
        state = {selectedLetter:null,enabled:true,observer:null};
        body[key] = state;
        state.apply = () => {
            if (body[key] !== state) return;
            const shadow = body.shadowRoot;
            if (!shadow) return;
            if (!state.observer) {
                state.observer = new MutationObserver(state.apply);
                state.observer.observe(shadow,{childList:true,subtree:true,attributes:true,attributeFilter:['role','aria-checked','aria-disabled']});
            }
            const group = shadow.querySelector('#cmp_a11y_root [aria-label="Answer choices"]');
            if (!group) return;
            for (const node of group.querySelectorAll('[role="button"],[role="radio"]')) {
                const match = (node.textContent || '').trim().match(/^([A-D])/);
                if (!match) continue;
                const values = {role:'radio','aria-checked':String(match[1]===state.selectedLetter),'aria-disabled':String(!state.enabled)};
                for (const [name,value] of Object.entries(values)) {
                    if (node.getAttribute(name)!==value) node.setAttribute(name,value);
                }
            }
            for (const node of shadow.querySelectorAll('#cmp_a11y_root [role="button"]')) {
                if ((node.textContent || '').trim().replace(/\s+/g,' ')==='Confirm answer >') {
                    const value=String(!state.enabled || state.selectedLetter===null);
                    if (node.getAttribute('aria-disabled')!==value) node.setAttribute('aria-disabled',value);
                }
            }
        };
    }
    state.selectedLetter = selectedLetter;
    state.enabled = enabled;
    state.apply();
    requestAnimationFrame(state.apply);
}""")
