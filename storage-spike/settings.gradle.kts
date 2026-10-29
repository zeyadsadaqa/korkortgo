pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
    val probeKotlinVersion = providers.gradleProperty("probeKotlinVersion").getOrElse("2.3.20")
    plugins {
        kotlin("multiplatform") version probeKotlinVersion
        kotlin("plugin.serialization") version probeKotlinVersion
        id("com.android.application") version "8.13.2"
        id("com.google.devtools.ksp") version "2.3.12"
        id("androidx.room3") version "3.0.3"
    }
}
dependencyResolutionManagement { repositories { google(); mavenCentral() } }
rootProject.name = "KorkortStorageSpike"
