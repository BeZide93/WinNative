path = 'app/src/main/java/com/winlator/cmod/steam/service/SteamService.kt'
with open(path, 'r') as f:
    lines = f.read().split('\n')

for i in range(491, 502):
    if i < len(lines):
        if not lines[i].strip().startswith('//'):
            lines[i] = '// ' + lines[i]

with open(path, 'w') as f:
    f.write('\n'.join(lines))
