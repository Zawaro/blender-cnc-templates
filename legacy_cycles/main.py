import sys
import os
import bpy

# Hack to import modules from current script path
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

from constants import TEMPLATE_VERSION, TEMPLATE_PREFIX
from scenes import BaseScene, RA2, RA2_INF, RA2_FX, TS, TS_FX, TS_INF, RW, RW_INF, RW_FX, RA1, RA1_INF, RA1_FX, RM, RM_INF, RM_FX, D2K, D2K_INF, D2K_FX

# 1. Create scenes
base_scene = BaseScene()
ra2_scene = RA2()
ra2_fx_scene = RA2_FX()
ra2_inf_scene = RA2_INF()
ts_scene = TS()
ts_fx_scene = TS_FX()
ts_inf_scene = TS_INF()
rw_scene = RW()
rw_fx_scene = RW_FX()
rw_inf_scene = RW_INF()
ra1_scene = RA1()
ra1_fx_scene = RA1_FX()
ra1_inf_scene = RA1_INF()
rm_scene = RM()
rm_fx_scene = RM_FX()
rm_inf_scene = RM_INF()
d2k_scene = D2K()
d2k_fx_scene = D2K_FX()
d2k_inf_scene = D2K_INF()

# 2. Remove default scene
base_scene.cleanup()
ra2_scene.select_scene()

# 3. Add template scripts
scripts = os.listdir(os.path.join(current_path, 'scripts'))
for file in range(len(scripts)):
  filename = scripts[file]
  script_name = filename.replace('.txt', '')
  print(script_name)
  with open(os.path.join(current_path, 'scripts', scripts[file]), 'r') as script:
    bpy.ops.text.new()
    text = bpy.data.texts["Text"]
    text.name = script_name
    text.write(script.read())

# 4. Pack assets
bpy.ops.file.pack_all()

# 5. Remove previous .blender file
save_path = os.path.join(current_path, "{}_{}.blend".format(TEMPLATE_PREFIX, TEMPLATE_VERSION))
if os.path.exists(save_path):
  os.remove(save_path)

# 6. Output .blend file
bpy.ops.wm.save_as_mainfile(filepath=save_path)

# 7. Compress .blend file
zip_path = os.path.join(current_path, "{}_{}.zip".format(TEMPLATE_PREFIX, TEMPLATE_VERSION))
if os.path.exists(zip_path):
  os.remove(zip_path)
os.system("bash -c 'zip -r {} {}'".format(zip_path, save_path))
