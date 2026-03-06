import xml.etree.ElementTree as ET
import os

def merge_xml(base_file, ref_file, output_file):
    if not os.path.exists(ref_file): return
    if not os.path.exists(base_file):
        base_tree = ET.Element('resources')
    else:
        try:
            base_tree = ET.parse(base_file).getroot()
        except:
            base_tree = ET.Element('resources')
    
    ref_tree = ET.parse(ref_file).getroot()
    base_names = {child.get('name') for child in base_tree if child.get('name')}
    
    for child in ref_tree:
        name = child.get('name')
        if name and name not in base_names:
            base_tree.append(child)
            base_names.add(name)
            
    with open(output_file, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(ET.tostring(base_tree, encoding='utf-8'))

# Merge arrays
merge_xml('app/src/main/res/values/arrays.xml', 
          '/home/max/Build/Emulator/Reference/GameNative-Performance/app/src/main/res/values/arrays.xml',
          'app/src/main/res/values/merged_arrays.xml')
if os.path.exists('app/src/main/res/values/merged_arrays.xml'):
    os.replace('app/src/main/res/values/merged_arrays.xml', 'app/src/main/res/values/arrays.xml')

# Merge dimens
merge_xml('app/src/main/res/values/dimens.xml', 
          '/home/max/Build/Emulator/Reference/GameNative-Performance/app/src/main/res/values/dimens.xml',
          'app/src/main/res/values/merged_dimens.xml')
if os.path.exists('app/src/main/res/values/merged_dimens.xml'):
    os.replace('app/src/main/res/values/merged_dimens.xml', 'app/src/main/res/values/dimens.xml')
