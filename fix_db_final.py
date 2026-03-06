import re
path = 'app/src/main/java/com/winlator/cmod/steam/db/PluviaDatabase.kt'
with open(path, 'r') as f:
    content = f.read()

# Remove autoMigrations
content = re.sub(r'autoMigrations = \[.*?\]', '', content, flags=re.DOTALL)
# Ensure exportSchema is false
content = content.replace('exportSchema = true', 'exportSchema = false')

with open(path, 'w') as f:
    f.write(content)
