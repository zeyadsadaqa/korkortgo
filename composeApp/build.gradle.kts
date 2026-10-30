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
            implementation(project(":progress-data"))
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.ui)
        }
        commonTest.dependencies { implementation(kotlin("test")) }
        getByName("desktopTest").dependencies { implementation(compose.desktop.currentOs) }
        iosMain.dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1") }
        getByName("desktopMain").dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1") }
        wasmJsMain.dependencies { implementation("androidx.sqlite:sqlite-web:2.7.1"); implementation("org.jetbrains.kotlinx:kotlinx-browser:0.3") }
        androidMain.dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1"); implementation("androidx.activity:activity-compose:1.11.0") }
    }
}
android {
    namespace = "se.korkort"
    compileSdk = 36
    defaultConfig { applicationId = "se.korkort.study"; minSdk = 24; targetSdk = 36; versionCode = 1; versionName = "1.0" }
    // Separate installed data for destructive import/reset verification.
    buildTypes.create("verification") {
        initWith(buildTypes.getByName("debug"))
        applicationIdSuffix = ".verification"
        versionNameSuffix = "-verification"
        matchingFallbacks += listOf("debug")
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
}
kotlin.targets.withType<org.jetbrains.kotlin.gradle.targets.jvm.KotlinJvmTarget>().configureEach {
    compilerOptions.jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
}
compose.resources { packageOfResClass = "se.korkort.resources"; publicResClass = true }

// Bundle the pinned worker proven in phase 1; no runtime CDN dependency.
val installProgressWorker by tasks.registering(Exec::class) {
    workingDir(rootProject.layout.projectDirectory.dir("storage-spike/web"))
    commandLine("npm","ci","--ignore-scripts","--no-audit","--no-fund")
    inputs.files(rootProject.file("storage-spike/web/package.json"),rootProject.file("storage-spike/web/package-lock.json"))
    outputs.dir(rootProject.file("storage-spike/web/node_modules"))
}
val progressWorkerResources by tasks.registering(Sync::class) {
    dependsOn(installProgressWorker)
    from(rootProject.file("storage-spike/web")) { include("worker.js","LICENSE-AndroidX.txt","THIRD_PARTY.md") }
    from(rootProject.file("storage-spike/web/node_modules/@sqlite.org/sqlite-wasm/sqlite-wasm/jswasm")) {
        include("sqlite3-bundler-friendly.mjs","sqlite3-opfs-async-proxy.js","sqlite3.wasm")
    }
    into(layout.buildDirectory.dir("generated/progressWorker"))
}
kotlin.sourceSets.named("wasmJsMain") { resources.srcDir(progressWorkerResources) }
