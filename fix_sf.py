import re

path = 'app/src/main/java/com/winlator/cmod/steam/data/SteamFriend.kt'
with open(path, 'r') as f:
    content = f.read()

# Fix package
content = content.replace('package com.OxGames.Pluvia.data', 'package com.winlator.cmod.steam.data\n\nimport com.winlator.cmod.steam.*')

# Comment out UI unresolved references
content = re.sub(r'import com.OxGames.Pluvia.ui.*?\n', '', content)
content = re.sub(r'val statusColor: Color.*?\n\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'val statusIcon: ImageVector\?.*?\n\s*\}', '', content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)

