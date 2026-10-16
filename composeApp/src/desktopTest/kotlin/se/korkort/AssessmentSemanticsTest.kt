@file:OptIn(androidx.compose.ui.InternalComposeUiApi::class)
package se.korkort

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.Snapshot
import androidx.compose.ui.focus.FocusDirection
import androidx.compose.ui.graphics.asComposeCanvas
import androidx.compose.ui.input.key.*
import androidx.compose.ui.platform.PlatformContext
import androidx.compose.ui.scene.CanvasLayersComposeScene
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.IntSize
import org.jetbrains.skia.Surface
import kotlin.test.*

/** Headless rendering uses the installed Compose scene, semantics tree and real key events. */
class AssessmentSemanticsTest {
    @Test fun keyboardConfirmationAndReadingOrderObeyBothFeedbackModes() {
        Feedback.entries.forEach { mode ->
            val q = AssessmentTest().question()
            val packageId = ContentPackageIdentity("ui-fixture", Sha256("c".repeat(64)))
            var session by mutableStateOf(AssessmentSession(listOf(q.snapshot(packageId)), mode))
            var owner: SemanticsOwner? = null
            val listener = object : PlatformContext.SemanticsOwnerListener {
                override fun onSemanticsOwnerAppended(semanticsOwner: SemanticsOwner) { owner = semanticsOwner }
                override fun onSemanticsOwnerRemoved(semanticsOwner: SemanticsOwner) { owner = null }
                override fun onSemanticsChange(semanticsOwner: SemanticsOwner) {}
                override fun onLayoutChange(semanticsOwner: SemanticsOwner, semanticsNodeId: Int) {}
            }
            val platform = object : PlatformContext by PlatformContext.Empty {
                override val semanticsOwnerListener = listener
            }
            val scene = CanvasLayersComposeScene(size = IntSize(800, 2000), platformContext = platform)
            val surface = Surface.makeRasterN32Premul(800, 2000)
            var frame = 0L
            fun render() {
                Snapshot.sendApplyNotifications()
                repeat(3) { scene.render(surface.canvas.asComposeCanvas(), ++frame * 16_666_667) }
            }
            fun nodes(): List<SemanticsNode> {
                fun walk(node: SemanticsNode): List<SemanticsNode> = listOf(node) + node.children.flatMap { walk(it) }
                return walk(requireNotNull(owner).rootSemanticsNode)
            }
            fun texts(): String = nodes().joinToString(" | ") { node ->
                node.config.getOrNull(SemanticsProperties.Text)?.joinToString { it.text }.orEmpty() +
                    node.config.getOrNull(SemanticsProperties.ContentDescription)?.joinToString().orEmpty()
            }
            fun key(key: Key) {
                scene.sendKeyEvent(KeyEvent(key, KeyEventType.KeyDown))
                scene.sendKeyEvent(KeyEvent(key, KeyEventType.KeyUp))
                render()
            }
            try {
                scene.setContent { MaterialTheme {
                    AssessmentCard(session.presentation(), onConfirm = { session = session.answer(it) },
                        image = { _, _ -> Text("UNSAFE-STUDY-CAPTION") })
                } }
                render()
                assertFalse(texts().contains("SECRET"))
                assertFalse(texts().contains("UNSAFE-STUDY-CAPTION"))
                val radios = nodes().filter { it.config.getOrNull(SemanticsProperties.Role) == Role.RadioButton }
                assertEquals(4, radios.size)
                assertEquals(listOf("A", "B", "C", "D"), radios.map { radio ->
                    radio.config[SemanticsProperties.Text].first().text
                })
                assertEquals(radios.map { it.boundsInRoot.top }.sorted(), radios.map { it.boundsInRoot.top })
                assertTrue(radios.all { it.config.getOrNull(SemanticsProperties.ContentDescription)?.any { t -> t.startsWith("Circle with") } == true })
                val reading = texts()
                assertTrue(reading.indexOf("Which picture?") < reading.indexOf("Circle with"))
                assertTrue(scene.focusManager.takeFocus(FocusDirection.Next))
                key(Key.Spacebar)
                assertNull(session.currentAnswer) // Selection is not confirmation.
                assertFalse(texts().contains("SECRET"))
                assertEquals(1, nodes().count { it.config.getOrNull(SemanticsProperties.Selected) == true })
                // The other three choices remain ahead of Confirm in keyboard traversal order.
                repeat(4) { key(Key.Tab) }
                key(Key.Enter)
                assertNotNull(session.currentAnswer)
                assertNotNull(scene.focusManager.getFocusRect())
                assertTrue(nodes().any { it.config.getOrNull(SemanticsProperties.Focused) == true })
                assertEquals(mode == Feedback.IMMEDIATE, texts().contains("SECRET"))
                if (mode == Feedback.AT_END) {
                    session = session.next()
                    render()
                    assertTrue(texts().contains("SECRET"))
                }
                assertTrue(nodes().any { it.config.getOrNull(SemanticsProperties.LiveRegion) == LiveRegionMode.Polite })
                assertTrue(nodes().filter { it.config.getOrNull(SemanticsProperties.Role) == Role.RadioButton }.all {
                    it.config.contains(SemanticsProperties.Disabled)
                })
            } finally {
                scene.close()
                surface.close()
            }
        }
    }
}
