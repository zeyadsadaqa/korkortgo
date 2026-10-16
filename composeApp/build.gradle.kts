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
        getByName("desktopTest").dependencies { implementation(compose.desktop.currentOs) }
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

// Opt-in verification binaries contain held renderer fixtures, never scored content/routes.
val referenceProof = providers.gradleProperty("referenceProof").isPresent
if (referenceProof) {
    require(gradle.startParameter.taskNames.none {it.contains("release",ignoreCase=true)}) {"Verification fixtures must not be included in a release build"}
    gradle.taskGraph.whenReady {
        require(allTasks.none {it.name.contains("release",ignoreCase=true) || it.name.contains("publish",ignoreCase=true)}) {"Verification fixtures must not be released or published"}
    }
    kotlin.sourceSets.getByName("commonMain").kotlin.srcDir("src/verificationCommonMain/kotlin")
    kotlin.targets.getByName("android").compilations.configureEach {
        if (name == "debug") defaultSourceSet.kotlin.srcDir("src/verificationAndroidMain/kotlin")
    }
    kotlin.sourceSets.getByName("wasmJsMain").kotlin.apply {
        srcDir("src/verificationWasmMain/kotlin")
        exclude { it.file == project.file("src/wasmJsMain/kotlin/se/korkort/main.kt") }
    }
    kotlin.sourceSets.configureEach {
        if (name == "iosMain") kotlin.apply {
            srcDir("src/verificationIosMain/kotlin")
            exclude { it.file == project.file("src/iosMain/kotlin/se/korkort/MainViewController.kt") }
        }
    }
    android.sourceSets.getByName("debug").manifest.srcFile("src/verificationAndroidMain/AndroidManifest.xml")
    android.buildTypes.getByName("debug").applicationIdSuffix = ".verification"
}
