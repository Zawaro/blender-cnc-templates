import sys
import os
import bpy

# Hack to import modules from current script path
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

from scenes import BaseScene, RA2, RA2_INF, RA2_FX, TS, TS_FX, TS_INF, RW, RW_INF, RW_FX, RA1, RA1_INF, RA1_FX, RM, RM_INF, RM_FX, D2K, D2K_INF, D2K_FX

TEMPLATE_VERSION = "1_00_alpha1"

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

# 4. Output .blend file
save_path = os.path.join(current_path, "CnC_CyclesX_{}.blend".format(TEMPLATE_VERSION))
bpy.ops.wm.save_as_mainfile(filepath=save_path)

# CS = bpy.context.scene
# C = bpy.context

# renderEngine = CS.cnc_tools.render_engine
# renderType = CS.cnc_tools.render_type
# suffix = getSuffix(CS.name)
# props = getRenderProperties(renderType, renderEngine)

# CS.render.engine = renderEngine

# def getRenderProperties(self, renderType, renderEngine):
#   if renderEngine == 'CYCLES':
#     if renderType == "Reset":     return [1, 1, 1, 1, 1, 0, 1,  1]
#     elif renderType == "Buildup": return [1, 0, 1, 1, 1, 1, 1,  1]
#     elif renderType == "Object":  return [1, 1, 1, 1, 1, 1, 0,  1]
#     elif renderType == "Preview": return [0, 1, 0, 1, 1, 1, 1,  1]
#     elif renderType == "Shadow":  return [0, 1, 0, 1, 1, 1, 1,  0]
#   else:
#     if renderType == "Reset":     return [1, 1, 1, 1, 1, 0, 1,  1]
#     elif renderType == "Buildup": return [1, 0, 1, 1, 1, 1, 1,  1]
#     elif renderType == "Object":  return [1, 1, 1, 1, 1, 1, 1,  1]
#     elif renderType == "Preview": return [1, 0, 0, 0, 1, 1, 1,  1]
#     elif renderType == "Shadow":  return [1, 1, 0, 1, 1, 1, 1,  0]