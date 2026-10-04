import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl
plugins {
    kotlin("multiplatform")
    id("org.jetbrains.kotlin.plugin.compose")
    id("org.jetbrains.compose")
    id("com.android.application")
}
kotlin {
    androidTarget()
    jvm("desktop")
    iosArm64 { binaries.framework { baseName = "KorkortKit"; isStatic = true } }
    iosSimulatorArm64 { binaries.framework { baseName = "KorkortKit"; isStatic = true } }
    @OptIn(ExperimentalWasmDsl::class)
    wasmJs { browser(); binaries.executable() }
    sourceSets {
        commonMain.dependencies {
            implementation(compose.components.resources)
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.ui)
        }
        commonTest.dependencies { implementation(kotlin("test")) }
        androidMain.dependencies { implementation("androidx.activity:activity-compose:1.11.0") }
    }
}
android {
    namespace = "se.korkort"
    compileSdk = 36
    defaultConfig { applicationId = "se.korkort.study"; minSdk = 24; targetSdk = 36; versionCode = 1; versionName = "1.0" }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
}
kotlin.targets.withType<org.jetbrains.kotlin.gradle.targets.jvm.KotlinJvmTarget>().configureEach {
    compilerOptions.jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
}
compose.resources { packageOfResClass = "se.korkort.resources"; publicResClass = true }
