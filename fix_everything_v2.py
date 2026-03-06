import os
import re

root_dir = 'app/src/main/java/com/winlator/cmod/steam'

def fix_content(content):
    # Fix imports
    content = content.replace('import app.gamenative', 'import com.winlator.cmod.steam')
    content = content.replace('import com.winlator.core', 'import com.winlator.cmod.core')
    content = content.replace('import com.winlator.container', 'import com.winlator.cmod.container')
    content = content.replace('import com.winlator.box86_64', 'import com.winlator.cmod.box64')
    content = content.replace('import com.winlator.xserver', 'import com.winlator.cmod.xserver')
    content = content.replace('import com.winlator.xenvironment', 'import com.winlator.cmod.xenvironment')
    content = content.replace('import com.winlator.inputcontrols', 'import com.winlator.cmod.inputcontrols')
    content = content.replace('import com.winlator.widget', 'import com.winlator.cmod.widget')
    content = content.replace('import com.winlator.winhandler', 'import com.winlator.cmod.winhandler')
    
    # Fix specific missing imports
    if 'PluviaApp' in content and 'import com.winlator.cmod.PluviaApp' not in content and 'package com.winlator.cmod' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.PluviaApp\n', content, 1)
    if 'BuildConfig' in content and 'import com.winlator.cmod.BuildConfig' not in content and 'package com.winlator.cmod' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.BuildConfig\n', content, 1)
    if 'R.' in content and 'import com.winlator.cmod.R' not in content and 'package com.winlator.cmod' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.R\n', content, 1)

    # Fix JavaSteam "in" keyword
    content = content.replace('import in.dragonbra', 'import `in`.dragonbra')
    
    # Fix hideSystemUI call
    content = re.sub(r'AppUtils\.hideSystemUI\(this,\s*![^)]+\)', 'AppUtils.hideSystemUI(this)', content)
    
    # Stub out Supabase and PostHog in files
    content = re.sub(r'import io\.github\.jan_tennert\.supabase.*?\n', '', content)
    content = re.sub(r'import com\.posthog\.android\.PostHog.*?\n', '', content)
    
    return content

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.kt') or file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            content = fix_content(content)
            with open(path, 'w') as f:
                f.write(content)

