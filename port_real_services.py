import os
import shutil
import re

REF_DIR = '/home/max/Build/Emulator/Reference/GameNative-Performance/app/src/main/java/app/gamenative'
DEST_DIR = 'app/src/main/java/com/winlator/cmod/steam'

packages_to_port = [
    'service',
    'db',
    'data',
    'events',
    'di',
    'utils',
    'ui/model',
    'ui/data',
    'ui/screen/login', # Port real login screen
    'ui/theme',
    'ui/component',
]

def fix_content(content):
    content = content.replace('package app.gamenative', 'package com.winlator.cmod.steam')
    content = content.replace('import app.gamenative', 'import com.winlator.cmod.steam')
    content = content.replace('import com.winlator.core', 'import com.winlator.cmod.core')
    content = content.replace('import com.winlator.container', 'import com.winlator.cmod.container')
    content = content.replace('import com.winlator.box86_64', 'import com.winlator.cmod.box64')
    content = content.replace('import com.winlator.xserver', 'import com.winlator.cmod.xserver')
    content = content.replace('import com.winlator.xenvironment', 'import com.winlator.cmod.xenvironment')
    content = content.replace('import com.winlator.MainActivity', 'import com.winlator.cmod.MainActivity')
    content = content.replace('import com.winlator.cmod.steam.PluviaApp', 'import com.winlator.cmod.PluviaApp')
    content = content.replace('import com.winlator.cmod.steam.BuildConfig', 'import com.winlator.cmod.BuildConfig')
    content = content.replace('import com.winlator.cmod.steam.R', 'import com.winlator.cmod.R')
    
    # Fix "in" keyword in imports
    content = content.replace('import in.dragonbra', 'import `in`.dragonbra')
    
    # Fix hideSystemUI call
    content = re.sub(r'AppUtils\.hideSystemUI\(this,\s*![^)]+\)', 'AppUtils.hideSystemUI(this)', content)
    
    return content

for pkg in packages_to_port:
    src_pkg_dir = os.path.join(REF_DIR, pkg)
    dest_pkg_dir = os.path.join(DEST_DIR, pkg)
    if not os.path.exists(dest_pkg_dir):
        os.makedirs(dest_pkg_dir)
    
    for root, dirs, files in os.walk(src_pkg_dir):
        for file in files:
            if file.endswith('.kt') or file.endswith('.java'):
                src_file = os.path.join(root, file)
                # Calculate relative path from src_pkg_dir
                rel_path = os.path.relpath(src_file, src_pkg_dir)
                dest_file = os.path.join(dest_pkg_dir, rel_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                
                with open(src_file, 'r') as f:
                    content = f.read()
                
                content = fix_content(content)
                
                with open(dest_file, 'w') as f:
                    f.write(content)

# Also port top-level files
top_level_files = ['Constants.kt', 'PrefManager.kt']
for file in top_level_files:
    src_file = os.path.join(REF_DIR, file)
    dest_file = os.path.join(DEST_DIR, file)
    with open(src_file, 'r') as f:
        content = f.read()
    content = fix_content(content)
    with open(dest_file, 'w') as f:
        f.write(content)

