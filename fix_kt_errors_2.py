import os
import re

root_dir = 'app/src/main/java/com/winlator/cmod/steam'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.kt') or file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # 1. Add PluviaApp import if missing and used
            if 'PluviaApp' in content and 'import com.winlator.cmod.PluviaApp' not in content:
                content = re.sub(r'(package [^\n]+\n)', r'\1import com.winlator.cmod.PluviaApp\n', content, 1)
            
            # 2. Fix ImageFs unresolved references
            if 'ImageFs' in content and 'import com.winlator.cmod.core.ImageFs' not in content:
                content = re.sub(r'(package [^\n]+\n)', r'\1import com.winlator.cmod.core.ImageFs\n', content, 1)
            
            # 3. Fix FileUtils
            if 'FileUtils' in content and 'import com.winlator.cmod.core.FileUtils' not in content:
                content = re.sub(r'(package [^\n]+\n)', r'\1import com.winlator.cmod.core.FileUtils\n', content, 1)

            # 4. Fix winlator package unresolved references (e.g. migrateDefaultDrives)
            if 'import com.winlator.cmod.steam.winlator' in content:
                content = content.replace('import com.winlator.cmod.steam.winlator.', 'import com.winlator.cmod.')
            
            # 5. Fix hideSystemUI call again (ensure it only has 1 arg)
            content = re.sub(r'AppUtils\.hideSystemUI\(this,\s*![^)]+\)', 'AppUtils.hideSystemUI(this)', content)

            with open(path, 'w') as f:
                f.write(content)

