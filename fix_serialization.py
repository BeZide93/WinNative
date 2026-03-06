import os
import re

data_dir = 'app/src/main/java/com/winlator/cmod/steam/data'

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    if 'data class' in content and '@Serializable' not in content:
        if 'import kotlinx.serialization.Serializable' not in content:
            content = re.sub(r'(package [^\n]+\n)', r'\1\nimport kotlinx.serialization.Serializable\n', content, 1)
        content = content.replace('data class', '@Serializable\ndata class')
        
    with open(path, 'w') as f:
        f.write(content)

for f in os.listdir(data_dir):
    if f.endswith('.kt'):
        fix_file(os.path.join(data_dir, f))
