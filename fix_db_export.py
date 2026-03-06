path = 'app/src/main/java/com/winlator/cmod/steam/db/PluviaDatabase.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('exportSchema = true', 'exportSchema = false')

with open(path, 'w') as f:
    f.write(content)
