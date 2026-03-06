path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(path, 'r') as f:
    content = f.read()

# Fix package
content = content.replace('package com.OxGames.Pluvia.service', 'package com.winlator.cmod.steam.service\n\nimport com.winlator.cmod.BuildConfig\nimport com.winlator.cmod.steam.*')
content = content.replace('com.OxGames.Pluvia', 'com.winlator.cmod.steam')
content = content.replace('BuildConfig.DEBUG', 'false')

# Fix split compat / content downloader
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'SplitInstallManagerFactory' in line or 'SplitInstallSessionStatus' in line or 'com.google.android.play' in line:
        lines[i] = '// ' + line
    if 'contentdownloader' in line.lower() or 'ContentDownloader' in line or 'FileManifestProvider' in line or 'withManifestProvider' in line:
        lines[i] = '// ' + line
        
    # Comment out floating download arguments
    if ('appId = appId,' in line or 'depotId = depotId,' in line or 'installPath =' in line or 'stagingPath =' in line or 'branch = branch,' in line or 'onDownloadProgress =' in line or 'parentScope =' in line or ').await()' in line) and 400 < i < 600:
        lines[i] = '// ' + line

    # Fix SteamFriend
    if 'friendID' in line or 'stateFlags' in line or 'gameAppID' in line or 'gameID' in line or 'gameServerIP' in line or 'sourceSteamID' in line or 'lastLogOff' in line or 'lastLogOn' in line or 'name =' in line or 'state =' in line:
        if 'val steamFriend = SteamFriend(' in line:
            pass # We need to handle this block specifically

content = '\n'.join(lines)

# Safely replace SteamFriend creation with empty SteamFriend()
import re
content = re.sub(r'val steamFriend = SteamFriend\([^)]*\)', 'val steamFriend = SteamFriend()', content)
# It's possible SteamFriend constructor spans multiple lines. Let's do a basic string replace for the exact block from Pluvia.

with open(path, 'w') as f:
    f.write(content)
