import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

from shared import constants

output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts')

print(output_path)

render_types = ['Reset', 'Buildup', 'Object', 'Preview', 'Shadow']
render_engines = ['CYCLES', 'BLENDER_EEVEE']

def generate_scripts():
  # - Create main scripts
  for render_type in render_types:
    for render_engine in render_engines:
      props = get_render_properties(render_type, render_engine)
      base = get_base_scripts(render_engine)

      sun_hide_render = 'True' if render_engine == 'BLENDER_EEVEE' and render_type == 'Shadow' else 'False'
      sun_shadow_hide_render = 'False' if render_engine == 'BLENDER_EEVEE' and render_type == 'Shadow' else 'True'

      base += 'bpy.data.objects["Plane.holdout." + suffix].hide_render = ' + str(bool(props[0])) + '\r\n'
      base += 'bpy.data.objects["Plane.holdout2." + suffix].hide_render = ' + str(bool(props[1])) + '\r\n'
      base += 'bpy.data.objects["Plane.shadow." + suffix].hide_render = ' + str(bool(props[2])) + '\r\n'
      base += 'bpy.data.objects["Plane.shadow2." + suffix].hide_render = ' + str(bool(props[3])) + '\r\n'
      base += 'bpy.data.objects["Plane.blue." + suffix].hide_render = ' + str(bool(props[4])) + '\r\n'
      base += 'bpy.data.objects["Plane.grey." + suffix].hide_render = ' + str(bool(props[5])) + '\r\n'
      base += 'bpy.data.objects["Plane.ambient." + suffix].hide_render = ' + str(bool(props[6])) + '\r\n'
      base += 'bpy.data.objects["Sun." + suffix].hide_render = ' + sun_hide_render + '\r\n'
      base += 'bpy.data.objects["Sun.shadow." + suffix].hide_render = ' + sun_shadow_hide_render + '\r\n'

      cycles_filter_width = str(constants.CYCLES_FILTER_WIDTH if render_type != 'Shadow' else 0.01)
      eevee_filter_size = str(constants.EEVEE_FILTER_SIZE if render_type != 'Shadow' else 0.01)

      base += 'bpy.context.scene.cycles.filter_width = ' + cycles_filter_width + '\r\n'
      base += 'bpy.context.scene.render.filter_size = ' + eevee_filter_size + '\r\n'
      base += 'bpy.context.scene.world.use_nodes = ' + sun_shadow_hide_render + '\r\n'
      base += 'bpy.context.scene.eevee.use_gtao = ' + sun_shadow_hide_render + '\r\n'
      # base += "bpy.context.window.view_layer = bpy.context.scene.view_layers['ViewLayer']"
      base += 'bpy.context.scene.render.use_single_layer = ' + str(bool(props[7])) + '\r\n'

      # is_preview = 'True' if render_type == 'Preview' else 'False'
      is_object = 'True' if render_type == 'Object' else 'False'
      is_buildupCycles = 'True' if render_type == 'Buildup' and render_engine == 'CYCLES' else 'False'
      is_buildupEevee = 'True' if render_type == 'Buildup' and render_engine == 'BLENDER_EEVEE' else 'False'
      is_shadowCycles = 'True' if render_type == 'Shadow' and render_engine == 'CYCLES' else 'False'
      is_shadowEevee = 'True' if render_type == 'Shadow' and render_engine == 'BLENDER_EEVEE' else 'False'
      is_previewCycles = 'True' if render_type == 'Preview' and render_engine == 'CYCLES' else 'False'
      is_previewEevee = 'True' if render_type == 'Preview' and render_engine == 'BLENDER_EEVEE' else 'False'

      # TODO: Add preview backgrounds
      # base += 'bpy.context.scene.node_tree.nodes["Preview.Background"].check = ' + is_preview + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Object"].check = ' + is_object + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Buildup.Cycles"].check = ' + is_buildupCycles + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Buildup.Eevee"].check = ' + is_buildupEevee + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Shadow.Cycles"].check = ' + is_shadowCycles + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Shadow.Eevee"].check = ' + is_shadowEevee + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Preview.Cycles"].check = ' + is_previewCycles + '\r\n'
      base += 'bpy.context.scene.node_tree.nodes["Preview.Eevee"].check = ' + is_previewEevee + '\r\n'
      if render_type == 'Reset':
        base += 'bpy.context.scene.node_tree.nodes["Alpha"].check = False\r\n'

      filename = '{}.Render.{}.txt'.format(get_engine_output_str(render_engine), render_type)
      output = os.path.join(output_path, filename)

      print(output)

      with open(output, 'w') as f:
        f.write(base)

  # - Create toggle Alpha scripts
  alpha_disable = '''import bpy

bpy.context.scene.node_tree.nodes["Alpha"].check = False
bpy.context.scene.render.image_settings.color_mode = 'RGB'
'''
  alpha_enable = '''import bpy

bpy.context.scene.node_tree.nodes["Alpha"].check = True
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
'''

  with open(os.path.join(output_path, 'Alpha.Disable.txt'), 'w') as f:
    f.write(alpha_disable)

  with open(os.path.join(output_path, 'Alpha.Enable.txt'), 'w') as f:
    f.write(alpha_enable)

  # - Readme
  
  with open(os.path.join(current_path, 'README.md'), 'r') as readme:
    with open(os.path.join(output_path, 'Readme.txt'), 'w') as f:
      f.write(readme.read())

def get_base_scripts(render_engine):
  return f'''import bpy

bpy.context.scene.render.engine = "{render_engine}"

suffix = "RA2.INF"

scenename = bpy.context.scene.name
if scenename == "Red Alert 2": suffix = "RA2"
elif scenename == "Red Alert 2 - Infantry": suffix = "RA2.INF"
elif scenename == "Red Alert 2 - Effects": suffix = "RA2.FX"
elif scenename == "Tiberian Sun": suffix = "TS"
elif scenename == "Tiberian Sun - Infantry": suffix = "TS.INF"
elif scenename == "Tiberian Sun - Effects": suffix = "TS.FX"
elif scenename == "ReWire": suffix = "RW"
elif scenename == "ReWire - Infantry": suffix = "RW.INF"
elif scenename == "ReWire - Effects": suffix = "RW.FX"
elif scenename == "Red Alert / Tiberian Dawn": suffix = "RA1"
elif scenename == "Red Alert / Tiberian Dawn - Infantry": suffix = "RA1.INF"
elif scenename == "Red Alert / Tiberian Dawn - Effects": suffix = "RA1.FX"
elif scenename == "Dune 2000": suffix = "D2K"
elif scenename == "Dune 2000 - Infantry": suffix = "D2K.INF"
elif scenename == "Dune 2000 - Effects": suffix = "D2K.FX"
elif scenename == "C&C Remastered": suffix = "RM"
elif scenename == "C&C Remastered - Infantry": suffix = "RM.INF"
elif scenename == "C&C Remastered - Effects": suffix = "RM.FX"

'''

def get_render_properties(render_type, render_engine):
  if render_engine == 'CYCLES':
    if render_type == "Reset":     return [1, 1, 1, 1, 1, 0, 1,  1]
    elif render_type == "Buildup": return [1, 0, 1, 1, 1, 1, 1,  1]
    elif render_type == "Object":  return [1, 1, 1, 1, 1, 1, 0,  1]
    elif render_type == "Preview": return [0, 1, 0, 1, 1, 1, 1,  1]
    elif render_type == "Shadow":  return [0, 1, 0, 1, 1, 1, 1,  0]
  else:
    if render_type == "Reset":     return [1, 1, 1, 1, 1, 0, 1,  1]
    elif render_type == "Buildup": return [1, 0, 1, 1, 1, 1, 1,  1]
    elif render_type == "Object":  return [1, 1, 1, 1, 1, 1, 1,  1]
    elif render_type == "Preview": return [1, 0, 0, 0, 1, 1, 1,  1]
    elif render_type == "Shadow":  return [1, 1, 0, 1, 1, 1, 1,  0]

def get_engine_output_str(render_engine):
  if render_engine == 'CYCLES': 
    return 'Cycles'
  elif render_engine == 'BLENDER_EEVEE': 
    return 'Eevee'
  else: 
    return 'Cycles'

generate_scripts()
