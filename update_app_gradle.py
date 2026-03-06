import re

with open('app/build.gradle', 'r') as f:
    content = f.read()

# 1. Update Plugins
plugin_block = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' version '2.1.10'
    id 'org.jetbrains.kotlin.plugin.compose' version '2.1.10'
    id 'com.google.devtools.ksp' version '2.1.10-1.0.31'
    id 'com.google.dagger.hilt.android' version '2.55'
    id 'org.jetbrains.kotlin.plugin.serialization' version '2.1.10'
}"""
content = re.sub(r'plugins\s*\{[^}]+\}', plugin_block, content)

# 2. Update Android Block
# Ensure buildFeatures and compileOptions are correct
android_block_additions = """
    buildFeatures {
        compose true
        buildConfig true
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }
"""

if 'buildFeatures' not in content:
    content = content.replace('android {', 'android {' + android_block_additions)

# 3. Update Dependencies
# We need to add all Pluvia deps
deps = """
    // Hilt
    implementation 'com.google.dagger:hilt-android:2.55'
    ksp 'com.google.dagger:hilt-android-compiler:2.55'
    implementation 'androidx.hilt:hilt-navigation-compose:1.2.0'

    // Room
    implementation 'androidx.room:room-ktx:2.6.1'
    implementation 'androidx.room:room-runtime:2.6.1'
    implementation 'androidx.room:room-paging:2.6.1'
    ksp 'androidx.room:room-compiler:2.6.1'

    // Compose
    implementation platform('androidx.compose:compose-bom:2025.02.00')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    implementation 'androidx.compose.material:material-icons-extended'
    implementation 'androidx.activity:activity-compose:1.10.1'
    implementation 'androidx.navigation:navigation-compose:2.8.8'
    implementation 'androidx.lifecycle:lifecycle-runtime-compose:2.8.7'

    // Coil & Landscapist
    implementation 'com.github.skydoves:landscapist-coil:2.4.7'
    implementation 'io.coil-kt:coil-compose:2.6.0'
    implementation 'io.coil-kt:coil-gif:2.6.0'

    // Serialization & Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.8.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.1'

    // Timber & Others
    implementation 'com.jakewharton.timber:timber:5.0.1'
    implementation 'com.github.penfeizhou.android.animation:apng:3.0.2'
    implementation 'com.materialkolor:material-kolor:2.0.2'
    implementation 'androidx.datastore:datastore-preferences:1.1.3'
    implementation 'com.google.zxing:core:3.5.3'
    implementation 'commons-io:commons-io:2.18.0'
    implementation 'org.apache.commons:commons-lang3:3.17.0'
    implementation 'commons-validator:commons-validator:1.9.0'
    implementation 'io.ktor:ktor-client-cio:3.0.3'
    implementation 'com.google.protobuf:protobuf-java:4.30.2'
    implementation 'com.github.luben:zstd-jni:1.5.6-9'
    implementation 'org.bouncycastle:bcprov-jdk18on:1.80'

    // Feature Delivery
    implementation 'com.google.android.play:feature-delivery:2.1.0'
    implementation 'com.google.android.play:feature-delivery-ktx:2.1.0'
"""

# Replace existing dependency block or just append? 
# Let's find implementation 'androidx.appcompat:appcompat' and insert before it
content = content.replace("dependencies {", "dependencies {\n" + deps)

with open('app/build.gradle', 'w') as f:
    f.write(content)
