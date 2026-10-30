package se.korkort

import androidx.compose.material3.*
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.Box
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.*
import org.jetbrains.compose.resources.Font
import se.korkort.resources.*

/** The approved editorial/UI families, using pinned production font bytes. */
@Composable internal fun LearningTheme(content: @Composable ()->Unit) {
    val sans=FontFamily(Font(Res.font.SourceSans3_Regular),Font(Res.font.SourceSans3_Semibold,FontWeight.SemiBold))
    val serif=FontFamily(Font(Res.font.SourceSerif4_Semibold,FontWeight.SemiBold),Font(Res.font.SourceSerif4_Bold,FontWeight.Bold))
    val base=Typography()
    val type=base.copy(
        displayLarge=base.displayLarge.copy(fontFamily=serif),displayMedium=base.displayMedium.copy(fontFamily=serif),displaySmall=base.displaySmall.copy(fontFamily=serif),
        headlineLarge=base.headlineLarge.copy(fontFamily=serif,fontWeight=FontWeight.Bold),headlineMedium=base.headlineMedium.copy(fontFamily=serif,fontWeight=FontWeight.Bold),headlineSmall=base.headlineSmall.copy(fontFamily=serif,fontWeight=FontWeight.SemiBold),
        titleLarge=base.titleLarge.copy(fontFamily=sans,fontWeight=FontWeight.SemiBold),titleMedium=base.titleMedium.copy(fontFamily=sans),titleSmall=base.titleSmall.copy(fontFamily=sans),
        bodyLarge=base.bodyLarge.copy(fontFamily=sans),bodyMedium=base.bodyMedium.copy(fontFamily=sans),bodySmall=base.bodySmall.copy(fontFamily=sans),
        labelLarge=base.labelLarge.copy(fontFamily=sans,fontWeight=FontWeight.SemiBold),labelMedium=base.labelMedium.copy(fontFamily=sans),labelSmall=base.labelSmall.copy(fontFamily=sans))
    KorkortTheme { MaterialTheme(typography=type,colorScheme=MaterialTheme.colorScheme.copy(outline=Color(0xFF61706B),outlineVariant=Color(0xFFD5DED5),onSurfaceVariant=Color(0xFF495A52),error=Color(0xFF9A332F),errorContainer=Color(0xFFFFEDEA),onErrorContainer=Color(0xFF9A332F))){Surface(Modifier.fillMaxSize(),color=MaterialTheme.colorScheme.background){Box(Modifier.fillMaxSize(),contentAlignment=Alignment.TopCenter){content()}}} }
}
