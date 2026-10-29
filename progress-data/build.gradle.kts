import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization") version "2.3.20"
    id("com.android.library")
    id("com.google.devtools.ksp") version "2.3.12"
    id("androidx.room3") version "3.0.3"
}
kotlin {
    androidTarget()
    jvm("desktop")
    iosArm64()
    iosSimulatorArm64()
    @OptIn(ExperimentalWasmDsl::class) wasmJs { browser() }
    sourceSets {
        commonMain.dependencies {
            api("androidx.room3:room3-runtime:3.0.3")
            implementation("androidx.sqlite:sqlite-async:2.7.1")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
        }
        commonTest.dependencies { implementation(kotlin("test")) }
        getByName("desktopTest").dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1") }
    }
}
android {
    namespace = "se.korkort.progress"
    compileSdk = 36
    defaultConfig { minSdk = 24 }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
}
kotlin.targets.withType<org.jetbrains.kotlin.gradle.targets.jvm.KotlinJvmTarget>().configureEach {
    compilerOptions.jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
}
dependencies {
    listOf("Android", "Desktop", "IosArm64", "IosSimulatorArm64", "WasmJs").forEach {
        add("ksp$it", "androidx.room3:room3-compiler:3.0.3")
    }
}
room3 { schemaDirectory("$projectDir/schemas") }
