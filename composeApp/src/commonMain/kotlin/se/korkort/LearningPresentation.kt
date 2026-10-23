package se.korkort

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.unit.dp

/** Shared approved outline actions; icon and chevron are decorative, the label is the action. */
@Composable internal fun LearningAction(label:String,onClick:()->Unit,modifier:Modifier=Modifier,detail:String?=null) {
    OutlinedButton(onClick,modifier.fillMaxWidth().heightIn(min=52.dp),shape=RoundedCornerShape(8.dp),contentPadding=PaddingValues(16.dp)) {
        Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically,horizontalArrangement=Arrangement.spacedBy(12.dp)) {
            DocumentMark()
            Column(Modifier.weight(1f)) {
                detail?.let { Text(it,style=MaterialTheme.typography.labelMedium) }
                Text(label,style=MaterialTheme.typography.titleMedium)
            }
            Text("›",Modifier.clearAndSetSemantics {})
        }
    }
}

@Composable internal fun DocumentMark() {
    val color=MaterialTheme.colorScheme.primary
    Canvas(Modifier.size(20.dp,24.dp).clearAndSetSemantics {}) {
        val stroke=Stroke(width=1.5.dp.toPx())
        drawRect(color,topLeft=Offset(size.width*.2f,size.height*.1f),size=androidx.compose.ui.geometry.Size(size.width*.65f,size.height*.8f),style=stroke)
        for(y in listOf(.35f,.5f,.65f))drawLine(color,Offset(size.width*.35f,size.height*y),Offset(size.width*.7f,size.height*y),strokeWidth=1.5.dp.toPx())
    }
}

@Composable internal fun LearningInfoPanel(content:@Composable ColumnScope.()->Unit) {
    Surface(color=MaterialTheme.colorScheme.secondaryContainer,shape=RoundedCornerShape(8.dp),modifier=Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp),verticalArrangement=Arrangement.spacedBy(10.dp),content=content)
    }
}
