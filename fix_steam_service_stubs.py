import re

path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(path, 'r') as f:
    content = f.read()

# Add constants to SteamService companion object
if 'const val INVALID_APP_ID' not in content:
    content = content.replace('companion object {', 'companion object {\n        const val INVALID_APP_ID = 0\n        const val INVALID_PKG_ID = 0\n')

with open(path, 'w') as f:
    f.write(content)
