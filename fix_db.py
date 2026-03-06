import re
path = 'app/src/main/java/com/winlator/cmod/steam/db/PluviaDatabase.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('exportSchema = true', 'exportSchema = false')
content = re.sub(r'autoMigrations = \[.*?\]', '', content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)
