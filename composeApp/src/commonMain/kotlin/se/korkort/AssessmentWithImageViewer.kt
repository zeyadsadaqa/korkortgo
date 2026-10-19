package se.korkort

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.Modifier
import androidx.compose.runtime.*
import androidx.compose.ui.focus.FocusRequester

/** Modal zoom never changes the session or disposes its pending radio selection. */
@Composable
fun AssessmentWithImageViewer(
    presentation: AssessmentPresentation,
    onConfirm: (OptionId) -> Unit,
    assets: List<CurriculumAsset>,
    onImageLoaded: (AssetId, Boolean) -> Unit = { _, _ -> },
    trailingContent: @Composable () -> Unit = {},
    viewerHost: @Composable (ImageViewerContent, () -> Unit) -> Unit = {content,close->AccessibleImageViewer(content,close)},
) {
    var picture by remember(presentation.key) {mutableStateOf<AssessmentImagePresentation?>(null)}
    var originFocus by remember(presentation.key) {mutableStateOf<FocusRequester?>(null)}
    var restore by remember(presentation.key) {mutableStateOf(false)}
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
        AssessmentCard(presentation,onConfirm,image={image,modifier->
            ExactAssetImage(assets.single {it.id==image.assetId},image.description,modifier,onLoaded={onImageLoaded(image.assetId,it)})
        },onEnlargeImage={image,focus->originFocus=focus;picture=image})
        trailingContent()
        }
        picture?.let { image ->
            viewerHost(ImageViewerContent.assessment(image,assets)) {picture=null;restore=true}
        }
    }
    LaunchedEffect(picture,restore) {
        if(picture==null && restore) {withFrameNanos {};originFocus?.requestFocus();restore=false}
    }
}
