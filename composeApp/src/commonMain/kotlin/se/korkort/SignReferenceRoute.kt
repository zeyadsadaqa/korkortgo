package se.korkort

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

/** A renderer can be exercised before release integration without activating held assessments. */
@Composable
fun SignReferenceRoute(
    target: ContentTarget,
    origin: ReturnContext,
    validOriginFocusIds: Set<String>,
    onReturn: (RestoredContext) -> Unit,
    onReferenceGroup: (ContentId) -> Unit,
    onExternal: (SourceReference) -> Boolean,
) {
    val result=canonicalResolver.canonical(target)
    if(result !is Resolution.Found || result.entry.kind!=DestinationKind.SIGN) {
        Text("This sign reference is unavailable.")
        return
    }
    val sign=navigationSigns.single {it.id==result.target.contentId}
    val asset=navigationAssets.single {it.id==sign.assetId}
    val groups=navigationReferenceGroups.filter {sign.id in it.entryIds}.map {group->group.title to {onReferenceGroup(group.id)}}
    SignReferenceDetail(sign,asset,navigationSources.references,
        onBack={onReturn(canonicalResolver.restore(origin,validOriginFocusIds))},
        onExternal=onExternal,referenceGroups=groups)
}
