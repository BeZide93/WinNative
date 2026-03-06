import os
import re

root_dir = 'app/src/main/java/com/winlator/cmod/steam'

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Standard replacements
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
    content = content.replace('com.winlator.cmod.steam.PluviaApp', 'com.winlator.cmod.PluviaApp')
    content = content.replace('com.winlator.cmod.steam.BuildConfig', 'com.winlator.cmod.BuildConfig')
    content = content.replace('com.winlator.cmod.steam.R', 'com.winlator.cmod.R')
    content = content.replace('import in.dragonbra', 'import `in`.dragonbra')
    
    # Redirect to STUBS
    content = content.replace('import com.winlator.cmod.steam.utils.NetworkMonitor', 'import com.winlator.cmod.steam.stubs.NetworkMonitor')
    content = content.replace('import com.winlator.cmod.steam.utils.BestConfigService', 'import com.winlator.cmod.steam.stubs.BestConfigService')
    content = content.replace('import com.winlator.cmod.steam.utils.SupportersUtils', 'import com.winlator.cmod.steam.stubs.SupportersUtils')
    content = content.replace('import com.winlator.cmod.steam.utils.UpdateChecker', 'import com.winlator.cmod.steam.stubs.UpdateChecker')
    content = content.replace('import com.winlator.cmod.steam.utils.GameFeedbackUtils', 'import com.winlator.cmod.steam.stubs.GameFeedbackUtils')
    content = content.replace('import com.winlator.cmod.steam.utils.ContentsManager', 'import com.winlator.cmod.steam.stubs.ContentsManager')
    content = content.replace('import com.winlator.cmod.steam.utils.ContentProfile', 'import com.winlator.cmod.steam.stubs.ContentProfile')
    
    # Stub Supabase/PostHog inline
    content = re.sub(r'import com\.posthog\.android\.PostHog', 'import com.winlator.cmod.steam.stubs.PostHog', content)
    content = re.sub(r'import io\.github\.jan_tennert\.supabase.*?\n', '', content)
    content = re.sub(r'PluviaApp\.supabase.*?\n', '', content)

    # Brute force fix missing R and BuildConfig
    if 'R.' in content and 'import com.winlator.cmod.R' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.R\n', content, 1)
    if 'BuildConfig' in content and 'import com.winlator.cmod.BuildConfig' not in content:
        content = re.sub(r'(package [^\n]+\n)', r'\1\nimport com.winlator.cmod.BuildConfig\n', content, 1)

    with open(path, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.kt') or file.endswith('.java'):
            fix_file(os.path.join(root, file))
