import re

path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(path, 'r') as f:
    content = f.read()

# 1. Package and imports
content = content.replace('package com.OxGames.Pluvia.service', 'package com.winlator.cmod.steam.service\n\nimport com.winlator.cmod.BuildConfig\nimport com.winlator.cmod.steam.*')
content = content.replace('com.OxGames.Pluvia', 'com.winlator.cmod.steam')
content = content.replace('BuildConfig.DEBUG', 'false')

# 2. SplitInstallManager and ImageFs
content = re.sub(r'val splitManager = SplitInstallManagerFactory\.create\(instance!!\)', 'val splitManager: Any? = null', content)
content = content.replace('splitManager.installedModules.contains("ubuntufs")', 'true')
content = content.replace('val moduleInstallSessionId = splitManager.requestInstall(listOf("ubuntufs"))', 'val moduleInstallSessionId = 0')
content = content.replace('val sessionState = splitManager.requestSessionState(moduleInstallSessionId)', 'val sessionState: Any? = null; break')
content = content.replace('ImageFs.find(instance!!).rootDir.exists()', 'true')
content = re.sub(r'downloadImageFs\([^)]*\)\.await\(\)', '', content)

# 3. ContentDownloader
content = re.sub(r'ContentDownloader\(.*?\)\.downloadApp\([^)]*\)\.await\(\)', '', content, flags=re.DOTALL)
content = content.replace('import com.winlator.cmod.steam.service.ContentDownloader', '')

# 4. AuthPollResult nullability
content = content.replace('authSession.pollAuthSessionStatus()', 'authSession!!.pollAuthSessionStatus()')
content = content.replace('result.accountName', 'result?.accountName')
content = content.replace('result.newClientId', 'result?.newClientId')
content = content.replace('result.refreshToken', 'result?.refreshToken')
content = content.replace('result.accessToken', 'result?.accessToken')

# 5. Fix friendID issues in onPersonaStateReceived
# Just wipe the body of onPersonaStateReceived
content = re.sub(r'private fun onPersonaStateReceived\(callback: PersonaStateCallback\) \{.*?\n    \}', 'private fun onPersonaStateReceived(callback: PersonaStateCallback) { }', content, flags=re.DOTALL)
content = re.sub(r'private fun onFriendsList\(callback: FriendsListCallback\) \{.*?\n    \}', 'private fun onFriendsList(callback: FriendsListCallback) { }', content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)
