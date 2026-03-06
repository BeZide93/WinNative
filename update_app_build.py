import re

with open('app/build.gradle', 'r') as f:
    content = f.read()

# Add essential auth libraries
libs = """
    // Network & JSON
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.12.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.8.0'
    
    // Supabase (Real backend from GameNative)
    implementation "io.github.jan-tennert.supabase:postgrest-kt:3.1.1"
    implementation "io.github.jan-tennert.supabase:realtime-kt:3.1.1"
    implementation "io.github.jan-tennert.supabase:gotrue-kt:3.1.1"
    implementation "io.ktor:ktor-client-android:3.1.0"
    
    // Auth
    implementation 'com.auth0.android:jwtdecode:2.0.2'
    implementation 'androidx.browser:browser:1.8.0'
"""

if 'supabase' not in content:
    content = content.replace("dependencies {", "dependencies {\n" + libs)

with open('app/build.gradle', 'w') as f:
    f.write(content)
