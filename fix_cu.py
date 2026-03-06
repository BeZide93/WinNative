path = 'app/src/main/java/com/winlator/cmod/steam/utils/ContainerUtils.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('null /*', 'null //')

with open(path, 'w') as f:
    f.write(content)
