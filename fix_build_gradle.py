import re

with open('app/build.gradle', 'r') as f:
    content = f.read()

# Remove versions from plugins
content = re.sub(r"id 'org.jetbrains.kotlin.android' version '2.1.10'", "id 'org.jetbrains.kotlin.android'", content)
content = re.sub(r"id 'org.jetbrains.kotlin.plugin.compose' version '2.1.10'", "id 'org.jetbrains.kotlin.plugin.compose'", content)
content = re.sub(r"id 'com.google.devtools.ksp' version '2.1.10-1.0.31'", "id 'com.google.devtools.ksp'", content)
content = re.sub(r"id 'com.google.dagger.hilt.android' version '2.55'", "id 'com.google.dagger.hilt.android'", content)
content = re.sub(r"id 'org.jetbrains.kotlin.plugin.serialization' version '2.1.10'", "id 'org.jetbrains.kotlin.plugin.serialization'", content)

with open('app/build.gradle', 'w') as f:
    f.write(content)
