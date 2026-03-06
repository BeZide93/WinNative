import re

with open('app/build.gradle', 'r') as f:
    content = f.read()

# Update Kotlin version
content = content.replace("classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.0'", "classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:2.1.10'")

# Add compose plugin
content = content.replace("id 'org.jetbrains.kotlin.android' version '1.9.0'", "id 'org.jetbrains.kotlin.android' version '2.1.10'\n    id 'org.jetbrains.kotlin.plugin.compose' version '2.1.10'\n    id 'com.google.devtools.ksp' version '2.1.10-1.0.31'\n    id 'com.google.dagger.hilt.android' version '2.55'")

# Remove composeOptions
content = re.sub(r'composeOptions\s*\{\s*kotlinCompilerExtensionVersion[^}]+\}', '', content)

# Add dagger hilt classpath to buildscript
content = content.replace("classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:2.1.10'", "classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:2.1.10'\n        classpath 'com.google.dagger:hilt-android-gradle-plugin:2.55'")

# Add dependencies
deps = """
    // Room
    implementation 'androidx.room:room-ktx:2.6.1'
    implementation 'androidx.room:room-runtime:2.6.1'
    implementation 'androidx.room:room-paging:2.6.1'
    ksp 'androidx.room:room-compiler:2.6.1'

    // Hilt
    implementation 'com.google.dagger:hilt-android:2.55'
    ksp 'com.google.dagger:hilt-android-compiler:2.55'
    implementation 'androidx.hilt:hilt-navigation-compose:1.2.0'

    // Timber
    implementation 'com.jakewharton.timber:timber:5.0.1'

    // Coil
    implementation 'com.github.skydoves:landscapist-coil:2.4.7'
    implementation 'io.coil-kt:coil-compose:2.6.0'

    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1'
    
    // Preferences
    implementation 'androidx.datastore:datastore-preferences:1.1.3'
    
    // APNG
    implementation 'com.github.penfeizhou.android.animation:apng:3.0.2'
    
    // Activity / Lifecycle
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.8.7'
    
    // Serialization
    implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.8.0'
"""

content = content.replace('// JavaSteam', deps + '\n    // JavaSteam')

with open('app/build.gradle', 'w') as f:
    f.write(content)
