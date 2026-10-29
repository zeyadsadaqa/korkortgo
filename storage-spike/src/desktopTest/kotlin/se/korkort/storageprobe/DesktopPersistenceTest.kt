package se.korkort.storageprobe

import java.nio.file.Files
import kotlinx.coroutines.runBlocking
import org.junit.Test

class DesktopPersistenceTest {
    @Test fun fileSurvivesCloseAndReopen() = runBlocking {
        val directory = Files.createTempDirectory("korkort-storage-proof").toFile()
        try {
            val path = directory.resolve("proof.db").absolutePath
            val first = desktopProbe(path)
            try { writeProbe(first) } finally { first.close() }
            val second = desktopProbe(path)
            try { verifyProbe(second) } finally { second.close() }
        } finally { directory.deleteRecursively() }
    }
}
