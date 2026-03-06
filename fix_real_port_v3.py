import os
import re

root_dir = 'app/src/main/java/com/winlator/cmod/steam'

def fix_content(content):
    content = content.replace('package app.gamenative', 'package com.winlator.cmod.steam')
    content = content.replace('import app.gamenative', 'import com.winlator.cmod.steam')
    content = content.replace('import com.winlator.core', 'import com.winlator.cmod.core')
    content = content.replace('import com.winlator.container', 'import com.winlator.cmod.container')
    content = content.replace('import com.winlator.box86_64', 'import com.winlator.cmod.box64')
    content = content.replace('import com.winlator.MainActivity', 'import com.winlator.cmod.MainActivity')
    content = content.replace('com.winlator.cmod.steam.PluviaApp', 'com.winlator.cmod.PluviaApp')
    content = content.replace('com.winlator.cmod.steam.BuildConfig', 'com.winlator.cmod.BuildConfig')
    content = content.replace('com.winlator.cmod.steam.R', 'com.winlator.cmod.R')
    content = content.replace('import in.dragonbra', 'import `in`.dragonbra')
    
    # Fix nested app.gamenative imports
    content = content.replace('app.gamenative', 'com.winlator.cmod.steam')
    
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
