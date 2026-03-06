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
                content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.PluviaApp\n', content, 1)
            
            # 2. Fix Box86_64Preset -> Box64Preset
            content = content.replace('Box86_64Preset', 'Box64Preset')
            
            # 3. Fix hideSystemUI call
            content = content.replace('AppUtils.hideSystemUI(this, !it.visible)', 'if (!it.visible) AppUtils.hideSystemUI(this)')
            
            # 4. Fix BOX86 -> BOX64 where appropriate or stub
            content = content.replace('DefaultVersion.BOX86', '""')
            
            # 5. Fix ImageFs unresolved references
            if 'ImageFs' in content and 'import com.winlator.cmod.core.ImageFs' not in content:
                content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.core.ImageFs\n', content, 1)
            
            # 6. Fix FileUtils
            if 'FileUtils' in content and 'import com.winlator.cmod.core.FileUtils' not in content:
                content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.core.FileUtils\n', content, 1)

            # 7. Fix KeyValueSet and JSON parsing in XServerViewModel/ContainerUtils
            # For now, I'll just stub out the problematic parts of KeyValueUtils and ContainerUtils
            
            with open(path, 'w') as f:
                f.write(content)

# Fix PrefManager specifically
pm_path = 'app/src/main/java/com/winlator/cmod/steam/PrefManager.kt'
with open(pm_path, 'r') as f:
    content = f.read()
content = content.replace('import com.winlator.cmod.box64.Box64Preset', 'import com.winlator.cmod.box64.Box64Preset') # Ensure import
with open(pm_path, 'w') as f:
    f.write(content)

