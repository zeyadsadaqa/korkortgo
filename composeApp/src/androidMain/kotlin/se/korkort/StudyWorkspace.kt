package se.korkort

import android.content.ContextWrapper
import androidx.activity.ComponentActivity
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider

internal class StudyViews:ViewModel() {var generation:String?=null;var workspace:CurriculumWorkspace?=null}
@Composable internal actual fun rememberStudyWorkspace(generation:String,notice:String?):CurriculumWorkspace {
    var context=LocalContext.current
    while(context !is ComponentActivity && context is ContextWrapper)context=context.baseContext
    val activity=context as? ComponentActivity
    if(activity==null)return remember(generation){CurriculumWorkspace(notice)}
    val model=ViewModelProvider(activity)[StudyViews::class.java]
    if(model.generation!=generation || model.workspace==null){model.generation=generation;model.workspace=CurriculumWorkspace(notice)}
    return checkNotNull(model.workspace)
}
