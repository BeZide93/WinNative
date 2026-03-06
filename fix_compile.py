import os
import re

for root, _, files in os.walk('app/src/main/java/com/winlator/cmod/steam'):
    for f in files:
        if f.endswith('.kt'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Remove bad R imports
            content = content.replace('import com.winlator.cmod.steam.R\n', '')
            content = content.replace('import com.winlator.cmod.steam.BuildConfig\n', '')
            
            with open(path, 'w') as file:
                file.write(content)

# Fix SteamService.kt issues
ss_path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(ss_path, 'r') as f:
    ss = f.read()

# Fix downloadApp too many arguments
ss = re.sub(r'downloadApp\([^)]*\)', 'null', ss)
ss = ss.replace('downloadImageFs(', '// downloadImageFs(')
ss = ss.replace('onDownloadProgress = {', '//')
ss = ss.replace('parentScope = this,', '//')
ss = ss.replace(').await()', '//')
ss = ss.replace('return downloadInfo', 'return true')

with open(ss_path, 'w') as f:
    f.write(ss)

