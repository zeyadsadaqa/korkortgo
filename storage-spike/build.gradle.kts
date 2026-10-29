import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl

plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
    id("com.android.application")
    id("com.google.devtools.ksp")
    id("androidx.room3")
}

kotlin {
    androidTarget()
    jvm("desktop")
    iosArm64()
    iosSimulatorArm64 {
        binaries.executable {
            entryPoint = "se.korkort.storageprobe.main"
        }
    }
    @OptIn(ExperimentalWasmDsl::class)
    wasmJs {
        browser()
        binaries.executable()
    }
    sourceSets {
        commonMain.dependencies {
            implementation("androidx.room3:room3-runtime:3.0.3")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
        }
        commonTest.dependencies { implementation(kotlin("test")) }
        androidMain.dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1") }
        val androidInstrumentedTest by getting {
            dependencies {
                implementation("androidx.test:runner:1.6.1")
                implementation("androidx.test.ext:junit:1.2.1")
            }
        }
        iosMain.dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1") }
        val desktopMain by getting {
            dependencies { implementation("androidx.sqlite:sqlite-bundled:2.7.1") }
        }
        wasmJsMain.dependencies {
            implementation("androidx.sqlite:sqlite-web:2.7.1")
            implementation("org.jetbrains.kotlinx:kotlinx-browser:0.3")
        }
    }
}

dependencies {
    listOf("Android", "Desktop", "IosArm64", "IosSimulatorArm64", "WasmJs").forEach {
        add("ksp$it", "androidx.room3:room3-compiler:3.0.3")
    }
}

android {
    namespace = "se.korkort.storageprobe"
    compileSdk = 36
    defaultConfig {
        applicationId = "se.korkort.storageprobe"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
kotlin.targets.withType<org.jetbrains.kotlin.gradle.targets.jvm.KotlinJvmTarget>().configureEach {
    compilerOptions.jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
}
room3 { schemaDirectory("$projectDir/schemas") }

val installWebWorker by tasks.registering(Exec::class) {
    workingDir(layout.projectDirectory.dir("web"))
    commandLine("npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund")
    inputs.files("web/package.json", "web/package-lock.json")
    outputs.dir("web/node_modules")
}
val prepareWebWorker by tasks.registering(Sync::class) {
    dependsOn(installWebWorker)
    from("web/worker.js", "web/LICENSE-AndroidX.txt", "web/THIRD_PARTY.md")
    from("web/node_modules/@sqlite.org/sqlite-wasm/sqlite-wasm/jswasm") {
        include("sqlite3-bundler-friendly.mjs", "sqlite3-opfs-async-proxy.js", "sqlite3.wasm")
    }
    into(layout.buildDirectory.dir("generated/workerResources"))
}
kotlin.sourceSets.named("wasmJsMain") { resources.srcDir(prepareWebWorker) }

tasks.register<JavaExec>("runDesktopProbe") {
    dependsOn("desktopMainClasses")
    val compilation = kotlin.targets.getByName("desktop").compilations.getByName("main")
    classpath(compilation.output.allOutputs, configurations.getByName("desktopRuntimeClasspath"))
    mainClass.set("se.korkort.storageprobe.DesktopProbeKt")
    args(providers.gradleProperty("probeAction").getOrElse("verify"),
        layout.buildDirectory.file("proof/desktop.db").get().asFile.absolutePath)
}
