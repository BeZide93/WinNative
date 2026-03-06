import re
import os

# 1. Fix PrefManager.kt
pm_path = 'app/src/main/java/com/winlator/cmod/steam/PrefManager.kt'
with open(pm_path, 'r') as f:
    pm = f.read()

# Completely remove BOX64_PRESET and BOX86_PRESET properties
pm = re.sub(r'private val BOX64_PRESET.*?\n\s*var box64Preset.*?\n.*?\n.*?\n\s*\}', '', pm, flags=re.DOTALL)
pm = re.sub(r'private val BOX86_PRESET.*?\n\s*var box86Preset.*?\n.*?\n.*?\n\s*\}', '', pm, flags=re.DOTALL)

with open(pm_path, 'w') as f:
    f.write(pm)


# 2. Fix SteamService.kt "it" instead of "callback"
ss_path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(ss_path, 'r') as f:
    ss = f.read()

# Reverse the "callback" -> "it" from my previous script inside the callback method
# Actually, just replace `it.` back to `callback.` where applicable or just fix the block.
lines = ss.split('\n')
for i, line in enumerate(lines):
    if 'Unresolved reference \'it\'' in line or 'it.' in line and 'friendDao.update' in ss or 'callback' in ss:
        pass

# Safest way: copy SteamService from Pluvia again, apply minimal fixes.
