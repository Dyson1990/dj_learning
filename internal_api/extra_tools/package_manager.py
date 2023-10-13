# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:59:59 2022

@author: Weave
"""
import re
from pathlib import Path
import importlib.metadata as im

proj_dir = Path(r'D:\scripts\ycy_rd')

mod_mapping = {
    'yaml': 'PyYAML'
    , 'docx': 'python-docx'
    , 'pywin32': 'win32'
    }

for dist0 in im.distributions():
    package_files = [p0 for p0 in dist0.files if p0.match('*.py')]
    root_dir_set = set([p0.parts[0] for p0 in package_files if len(p0.parts) > 1])
    
    if '..' in root_dir_set:
        root_dir_set.remove('..')
        
    if dist0.name in root_dir_set:
        root_dir_set = set([dist0.name])

    if len(root_dir_set) != 1 or '.' in dist0.name:
        print('mod_mapping ignore:', dist0.name)
        # print(dist0.files)
        continue
    
    mod_mapping[root_dir_set.pop()] = dist0.name

package_set = set({})
for fp in proj_dir.rglob('*.py'):
    with fp.open('r', encoding='utf-8') as fr:
        code = fr.read()
    
    import_line = re.findall(r'^import (\w+)', code, re.M)
    from_line = re.findall(r'^from ([\w\._]+) import [\w\._]+', code, re.M)
    package_set.update(import_line)
    package_set.update(from_line)
    
used_package = list(filter(lambda tup0: tup0[0] in package_set, mod_mapping.items()))
used_package_names = [tup0[-1] for tup0 in used_package]
version_dict = {dist0.name: dist0.version for dist0 in im.distributions() if dist0.name in used_package_names}

output_str = '\n'.join([f'{k0}=={v0}' for k0,v0 in version_dict.items()])
print(version_dict)
print(output_str)


if __name__ == "__main__":
    # from pip._internal.metadata import get_environment
    # print(list(get_environment(None).iter_installed_distributions(
    #     local_only=False,
    #     skip=(),
    #     user_only=False,
    # )
    # ))
    
    # print(installed)
    pass
    