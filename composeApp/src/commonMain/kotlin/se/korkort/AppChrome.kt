package se.korkort

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.key.*
import androidx.compose.ui.semantics.*
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp

internal enum class StudyTab(val label: String) { HOME("Home"), LEARNING("Learning"), EXERCISE("Exercise") }
internal fun tabFor(destination: AppDestination): StudyTab = when(destination) {
    AppDestination.Home -> StudyTab.HOME
    AppDestination.Library,AppDestination.SignCatalogue,is AppDestination.Content -> StudyTab.LEARNING
    else -> StudyTab.EXERCISE
}
@Composable internal fun TabIcon(tab: StudyTab) {
    val ink=LocalContentColor.current
    Canvas(Modifier.size(24.dp)) {
        val w=size.width;val h=size.height;val stroke=Stroke(2.dp.toPx())
        when(tab) {
            StudyTab.HOME -> {
                val path=androidx.compose.ui.graphics.Path().apply {moveTo(2f,h*.45f);lineTo(w*.5f,2f);lineTo(w-2,h*.45f);lineTo(w-2,h-2);lineTo(w*.62f,h-2);lineTo(w*.62f,h*.65f);lineTo(w*.38f,h*.65f);lineTo(w*.38f,h-2);lineTo(2f,h-2);close()}
                drawPath(path,ink,style=stroke)
            }
            StudyTab.LEARNING -> {
                drawRect(ink,Offset(2f,3f),androidx.compose.ui.geometry.Size(w-4,h-6),style=stroke)
                drawLine(ink,Offset(w/2,3f),Offset(w/2,h-3),2.dp.toPx())
            }
            StudyTab.EXERCISE -> {
                drawRect(ink,Offset(3f,2f),androidx.compose.ui.geometry.Size(w-6,h-4),style=stroke)
                for(y in listOf(.3f,.55f,.8f))drawLine(ink,Offset(w*.3f,h*y),Offset(w*.75f,h*y),2.dp.toPx())
            }
        }
    }
}
@Composable internal expect fun PlatformStudyBack(enabled: Boolean,onBack:()->Unit)
@Composable internal fun AppChrome(destination: AppDestination,onTab:(StudyTab)->Unit,canBack:Boolean,onBack:()->Unit,showBack:Boolean=canBack,content:@Composable ColumnScope.()->Unit) {
    PlatformStudyBack(canBack,onBack)
    BoxWithConstraints(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing.union(WindowInsets.ime)).onPreviewKeyEvent { event->
        if(canBack && event.type==KeyEventType.KeyDown && event.key==Key.Escape) {onBack();true} else false
    }) {
        val wide=maxWidth>=840.dp
        val showBadge=maxWidth>=360.dp && androidx.compose.ui.platform.LocalDensity.current.fontScale<1.4f
        Row(Modifier.fillMaxSize()) {
            if(wide) NavigationRail(containerColor=MaterialTheme.colorScheme.surface) {
                Spacer(Modifier.height(24.dp))
                StudyTab.entries.forEach {tab->NavigationRailItem(tabFor(destination)==tab,{onTab(tab)},icon={TabIcon(tab)},label={Text(tab.label)})}
            }
            Column(Modifier.weight(1f)) {
                Row(Modifier.fillMaxWidth().padding(horizontal=20.dp,vertical=12.dp),verticalAlignment=androidx.compose.ui.Alignment.CenterVertically) {
                    if(showBack) IconButton(onBack,modifier=Modifier.semantics{contentDescription="Back"}) {
                        val color=LocalContentColor.current
                        Canvas(Modifier.size(24.dp)) {
                            drawLine(color,Offset(size.width*.65f,size.height*.2f),Offset(size.width*.35f,size.height*.5f),2.dp.toPx())
                            drawLine(color,Offset(size.width*.35f,size.height*.5f),Offset(size.width*.65f,size.height*.8f),2.dp.toPx())
                        }
                    }
                    Text("KörkortGo",modifier=Modifier.weight(1f),style=MaterialTheme.typography.headlineSmall,color=MaterialTheme.colorScheme.primary)
                    if(showBadge)Text("CATEGORY B",style=MaterialTheme.typography.labelSmall)
                }
                Column(Modifier.weight(1f).fillMaxWidth(),content=content)
                if(!wide) NavigationBar(containerColor=MaterialTheme.colorScheme.surface) {
                    StudyTab.entries.forEach {tab->NavigationBarItem(tabFor(destination)==tab,{onTab(tab)},icon={TabIcon(tab)},label={Text(tab.label)})}
                }
            }
        }
    }
}
