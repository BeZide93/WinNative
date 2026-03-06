import os
import shutil
import re

REF_DIR = '/home/max/Build/Emulator/Reference/GameNative-Performance/app/src/main/java/app/gamenative'
DEST_DIR = 'app/src/main/java/com/winlator/cmod/steam'

def fix_content(content):
    content = content.replace('package app.gamenative', 'package com.winlator.cmod.steam')
    content = content.replace('import app.gamenative', 'import com.winlator.cmod.steam')
    content = content.replace('import com.winlator.core', 'import com.winlator.cmod.core')
    content = content.replace('import com.winlator.container', 'import com.winlator.cmod.container')
    content = content.replace('import com.winlator.box86_64', 'import com.winlator.cmod.box64')
    content = content.replace('import com.winlator.xserver', 'import com.winlator.cmod.xserver')
    content = content.replace('import com.winlator.xenvironment', 'import com.winlator.cmod.xenvironment')
    content = content.replace('import com.winlator.inputcontrols', 'import com.winlator.cmod.inputcontrols')
    content = content.replace('import com.winlator.widget', 'import com.winlator.cmod.widget')
    content = content.replace('import com.winlator.winhandler', 'import com.winlator.cmod.winhandler')
    content = content.replace('import com.winlator.MainActivity', 'import com.winlator.cmod.MainActivity')
    content = content.replace('import com.winlator.cmod.steam.PluviaApp', 'import com.winlator.cmod.PluviaApp')
    content = content.replace('import com.winlator.cmod.steam.BuildConfig', 'import com.winlator.cmod.BuildConfig')
    content = content.replace('import com.winlator.cmod.steam.R', 'import com.winlator.cmod.R')
    content = content.replace('import in.dragonbra', 'import `in`.dragonbra')
    content = re.sub(r'AppUtils\.hideSystemUI\(this,\s*![^)]+\)', 'AppUtils.hideSystemUI(this)', content)
    
    # Ensure R and BuildConfig imports are present if needed
    if 'BuildConfig' in content and 'import com.winlator.cmod.BuildConfig' not in content and 'package com.winlator.cmod' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.BuildConfig\n', content, 1)
    if 'R.' in content and 'import com.winlator.cmod.R' not in content and 'package com.winlator.cmod' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.R\n', content, 1)
        
    return content

for root, dirs, files in os.walk(REF_DIR):
    for file in files:
        if file.endswith('.kt') or file.endswith('.java'):
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, REF_DIR)
            
            # Skip PluviaApp as we have our own in com.winlator.cmod
            if rel_path == 'PluviaApp.kt': continue
            
            dest_file = os.path.join(DEST_DIR, rel_path)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            
            with open(src_file, 'r') as f:
                content = f.read()
            
            content = fix_content(content)
            
            with open(dest_file, 'w') as f:
                f.write(content)

