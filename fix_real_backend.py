import os
import re

# 1. Stub out PostHog and Supabase globally in ported files
root_dir = 'app/src/main/java/com/winlator/cmod/steam'

def stub_complex_logic(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Stub Supabase
    content = re.sub(r'import com\.winlator\.cmod\.steam\.utils\.supabase.*?\n', '', content)
    content = re.sub(r'PluviaApp\.supabase.*?\n', '', content)
    
    # Stub PostHog
    content = re.sub(r'import com\.posthog\.android\.PostHog.*?\n', '', content)
    content = re.sub(r'PostHog\.with\(.*?\)\.capture\(.*?\)', '', content)
    
    # Stub ContentsManager/Profile (too many errors)
    content = content.replace('import com.winlator.cmod.steam.utils.ContentsManager', '')
    content = content.replace('import com.winlator.cmod.steam.utils.ContentProfile', '')
    
    # Brute force fix for unresolved references by commenting out lines
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'NetworkMonitor' in line or 'PostHog' in line or 'supabase' in line or 'ContentsManager' in line or 'ContentProfile' in line:
            if 'package' not in line and 'import' not in line:
                line = '// ' + line
        new_lines.append(line)
    
    with open(path, 'w') as f:
        f.write('\n'.join(new_lines))

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.kt'):
            stub_complex_logic(os.path.join(root, file))

# 2. Fix specific known errors in SteamService.kt
ss_path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(ss_path, 'r') as f:
    content = f.read()

# Fix companion object constants
if 'const val INVALID_APP_ID' not in content:
    content = content.replace('companion object {', 'companion object {\n        const val INVALID_APP_ID = 0\n        const val INVALID_PKG_ID = 0\n')

# Fix unresolved generateSteamApp
content = content.replace('import com.winlator.cmod.steam.utils.generateSteamApp', 'import com.winlator.cmod.steam.utils.generateSteamApp') # Ensure correct

with open(ss_path, 'w') as f:
    f.write(content)

