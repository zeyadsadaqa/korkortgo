@file:OptIn(org.jetbrains.compose.resources.ExperimentalResourceApi::class)
package se.korkort

import androidx.compose.ui.graphics.painter.BitmapPainter
import androidx.compose.ui.graphics.painter.Painter
import org.jetbrains.compose.resources.decodeToImageBitmap

internal actual fun decodeExactRaster(bytes: ByteArray): Painter = BitmapPainter(bytes.decodeToImageBitmap())
