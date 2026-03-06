import os
import re

root_dir = 'app/src/main/java/com/winlator/cmod/steam'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.kt') or file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Fix imports
            content = content.replace('import com.winlator.cmod.steam.winlator.core.AppUtils', 'import com.winlator.cmod.core.AppUtils')
            content = content.replace('import com.winlator.cmod.steam.winlator.container.Container', 'import com.winlator.cmod.container.Container')
            content = content.replace('import com.winlator.cmod.steam.winlator.container.ContainerManager', 'import com.winlator.cmod.container.ContainerManager')
            content = content.replace('import com.winlator.cmod.steam.winlator.box86_64.Box86_64Preset', 'import com.winlator.cmod.box64.Box64Preset')
            content = content.replace('import com.winlator.cmod.steam.winlator.core.DefaultVersion', 'import com.winlator.cmod.core.DefaultVersion')
            
            # Fix R and BuildConfig
            content = re.sub(r'import com\.winlator\.cmod\.steam\.R', 'import com.winlator.cmod.R', content)
            content = re.sub(r'import com\.winlator\.cmod\.steam\.BuildConfig', 'import com.winlator.cmod.BuildConfig', content)
            
            # If no R import exists but R is used, add it
            if 'R.' in content and 'import com.winlator.cmod.R' not in content and 'package com.winlator.cmod' not in content:
                content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.R\n', content, 1)

            # If no BuildConfig import exists but BuildConfig is used, add it
            if 'BuildConfig' in content and 'import com.winlator.cmod.BuildConfig' not in content and 'package com.winlator.cmod' not in content:
                 content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.BuildConfig\n', content, 1)

            with open(path, 'w') as f:
                f.write(content)

# Also fix PluviaApp.kt
app_path = 'app/src/main/java/com/winlator/cmod/PluviaApp.kt'
with open(app_path, 'r') as f:
    content = f.read()
content = content.replace('import com.winlator.cmod.steam.PrefManager', 'import com.winlator.cmod.steam.PrefManager') # ensure correct
with open(app_path, 'w') as f:
    f.write(content)
