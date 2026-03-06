import re

with open('app/build.gradle', 'r') as f:
    content = f.read()

deps = """
    // Feature Delivery
    implementation 'com.google.android.play:feature-delivery:2.1.0'
    implementation 'com.google.android.play:feature-delivery-ktx:2.1.0'

    // MaterialKolor
    implementation 'com.materialkolor:materialkolor:1.7.0'
    
    // Accompanist
    implementation 'com.google.accompanist:accompanist-permissions:0.34.0'
"""

if "feature-delivery" not in content:
    content = content.replace('// JavaSteam', deps + '\n    // JavaSteam')

with open('app/build.gradle', 'w') as f:
    f.write(content)
