import os
import bpy

current_path = os.path.dirname(os.path.realpath(__file__))

BASE_COLOR = (0, 0, 0)

def RA2_World(world_texture_path, world_texture_name, suffix):
  tex_dir = os.path.join(os.path.dirname(current_path), world_texture_path)
  
  world = bpy.data.worlds.new('World.' + suffix)
  bpy.context.scene.world = world
  bpy.context.scene.world.color = BASE_COLOR
  bpy.context.scene.world.use_nodes = True
  output_node = bpy.data.worlds["World."+suffix].node_tree.nodes["World Output"]
  world.node_tree.links.remove(output_node.inputs[0].links[0])
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node01.inputs[2].default_value[2] = -1.22173
  mapping_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node02.inputs[1].default_value[2] = 0.3
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(world_texture_name)
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node.inputs[1].default_value = 0.25
  huesat_node.inputs[2].default_value = 1.0
  gamma_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeGamma")
  gamma_node01.inputs[1].default_value = 1.0
  gamma_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeGamma")
  gamma_node02.inputs[1].default_value = 0.9
  background_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixrbg_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixRGB")
  mixrbg_node.blend_type = 'MULTIPLY'
  mixrbg_node.inputs[0].default_value = 0.3
  colorramp_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeValToRGB")
  colorramp_node.color_ramp.elements[0].position = 0.25
  colorramp_node.color_ramp.elements[1].position = 0.327273
  separate_rgb_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeSeparateRGB")

  world.node_tree.links.new(mixshader_node01.outputs[0], output_node.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node01.inputs[2])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node02.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node01.inputs[0])
  world.node_tree.links.new(background_node01.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(gamma_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(gamma_node02.outputs[0], background_node02.inputs[0])
  world.node_tree.links.new(huesat_node.outputs[0], gamma_node02.inputs[0])
  world.node_tree.links.new(mixrbg_node.outputs[0], gamma_node01.inputs[0])
  world.node_tree.links.new(mixrbg_node.outputs[0], huesat_node.inputs[0])

  world.node_tree.links.new(tex_env_node.outputs[0], mixrbg_node.inputs[1])
  world.node_tree.links.new(mapping_node01.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node01.inputs[0])

  world.node_tree.links.new(colorramp_node.outputs[0], mixrbg_node.inputs[2])
  world.node_tree.links.new(separate_rgb_node.outputs[2], colorramp_node.inputs[0])
  world.node_tree.links.new(mapping_node02.outputs[0], separate_rgb_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node02.inputs[0])

  return world

def RA1_World(world_texture_path, world_texture_name, suffix):
  tex_dir = os.path.join(os.path.dirname(current_path), world_texture_path)
  
  world = bpy.data.worlds.new('World.' + suffix)
  bpy.context.scene.world = world
  bpy.context.scene.world.color = BASE_COLOR
  bpy.context.scene.world.use_nodes = True
  output_node = bpy.data.worlds["World."+suffix].node_tree.nodes["World Output"]
  world.node_tree.links.remove(output_node.inputs[0].links[0])
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node01.inputs[2].default_value[2] = -1.22173
  mapping_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node02.inputs[1].default_value[2] = 0.3
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(world_texture_name)
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node.inputs[1].default_value = 0.25
  huesat_node.inputs[2].default_value = 1.0
  gamma_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeGamma")
  gamma_node01.inputs[1].default_value = 1.0
  gamma_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeGamma")
  gamma_node02.inputs[1].default_value = 0.9
  background_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixrbg_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixRGB")
  mixrbg_node.blend_type = 'MULTIPLY'
  mixrbg_node.inputs[0].default_value = 0.3
  colorramp_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeValToRGB")
  colorramp_node.color_ramp.elements[0].position = 0.25
  colorramp_node.color_ramp.elements[1].position = 0.327273
  separate_rgb_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeSeparateRGB")

  world.node_tree.links.new(mixshader_node01.outputs[0], output_node.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node01.inputs[2])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node02.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node01.inputs[0])
  world.node_tree.links.new(background_node01.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(gamma_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(gamma_node02.outputs[0], background_node02.inputs[0])
  world.node_tree.links.new(huesat_node.outputs[0], gamma_node02.inputs[0])
  world.node_tree.links.new(mixrbg_node.outputs[0], gamma_node01.inputs[0])
  world.node_tree.links.new(mixrbg_node.outputs[0], huesat_node.inputs[0])

  world.node_tree.links.new(tex_env_node.outputs[0], mixrbg_node.inputs[1])
  world.node_tree.links.new(mapping_node01.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node01.inputs[0])

  world.node_tree.links.new(colorramp_node.outputs[0], mixrbg_node.inputs[2])
  world.node_tree.links.new(separate_rgb_node.outputs[2], colorramp_node.inputs[0])
  world.node_tree.links.new(mapping_node02.outputs[0], separate_rgb_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node02.inputs[0])

  return world

def RW_World(world_texture_path, world_texture_name, suffix):
  tex_dir = os.path.join(os.path.dirname(current_path), world_texture_path)
  
  world = bpy.data.worlds.new('World.' + suffix)
  bpy.context.scene.world = world
  bpy.context.scene.world.color = (0.0998987, 0.0684781, 0.0318961)
  bpy.context.scene.world.use_nodes = True
  output_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["World Output"]
  output_node01.target = 'EEVEE'
  world.node_tree.links.remove(output_node01.inputs[0].links[0])
  output_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeOutputWorld")
  output_node02.target = 'CYCLES'
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node.inputs[2].default_value[2] = -1.22173
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(world_texture_name)
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node01.inputs[1].default_value = 0.5
  huesat_node01.inputs[2].default_value = 0.35
  huesat_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node02.inputs[1].default_value = 0.5
  huesat_node02.inputs[2].default_value = 0.25
  background_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  background_node04 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")

  world.node_tree.links.new(mixshader_node01.outputs[0], output_node01.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], output_node02.inputs[0])
  world.node_tree.links.new(mixshader_node03.outputs[0], mixshader_node01.inputs[2])
  world.node_tree.links.new(mixshader_node03.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node01.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  world.node_tree.links.new(background_node01.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node03.inputs[1])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node03.inputs[2])
  world.node_tree.links.new(background_node04.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(huesat_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(huesat_node02.outputs[0], background_node04.inputs[0])
  world.node_tree.links.new(tex_env_node.outputs[0], background_node02.inputs[0])

  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node01.inputs[0])
  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node02.inputs[0])
  world.node_tree.links.new(mapping_node.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node.inputs[0])

  return world

def TS_World(world_texture_path, world_texture_name, suffix):
  tex_dir = os.path.join(os.path.dirname(current_path), world_texture_path)
  
  world = bpy.data.worlds.new('World.' + suffix)
  bpy.context.scene.world = world
  bpy.context.scene.world.color = (0.191202, 0.191202, 0.191202)
  bpy.context.scene.world.use_nodes = True
  output_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["World Output"]
  output_node01.target = 'EEVEE'
  world.node_tree.links.remove(output_node01.inputs[0].links[0])
  output_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeOutputWorld")
  output_node02.target = 'CYCLES'
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node.inputs[2].default_value[2] = -1.22173
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(world_texture_name)
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node01.inputs[1].default_value = 0.5
  huesat_node01.inputs[2].default_value = 1.2
  huesat_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node02.inputs[1].default_value = 0.5
  huesat_node02.inputs[2].default_value = 1.3
  background_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  background_node04 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")

  world.node_tree.links.new(mixshader_node01.outputs[0], output_node01.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], output_node02.inputs[0])
  world.node_tree.links.new(mixshader_node03.outputs[0], mixshader_node01.inputs[2])
  world.node_tree.links.new(mixshader_node03.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node01.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  world.node_tree.links.new(background_node01.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node03.inputs[1])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node03.inputs[2])
  world.node_tree.links.new(background_node04.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(huesat_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(huesat_node02.outputs[0], background_node04.inputs[0])
  world.node_tree.links.new(tex_env_node.outputs[0], background_node02.inputs[0])

  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node01.inputs[0])
  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node02.inputs[0])
  world.node_tree.links.new(mapping_node.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node.inputs[0])

  return world

def D2K_World(world_texture_path, world_texture_name, suffix):
  tex_dir = os.path.join(os.path.dirname(current_path), world_texture_path)
  
  world = bpy.data.worlds.new('World.' + suffix)
  bpy.context.scene.world = world
  bpy.context.scene.world.color = BASE_COLOR
  bpy.context.scene.world.use_nodes = True
  output_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["World Output"]
  output_node01.target = 'EEVEE'
  world.node_tree.links.remove(output_node01.inputs[0].links[0])
  output_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeOutputWorld")
  output_node02.target = 'CYCLES'
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node.inputs[2].default_value[2] = -1.22173
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(world_texture_name)
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node01.inputs[1].default_value = 0.5
  huesat_node01.inputs[2].default_value = 1.4
  huesat_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node02.inputs[1].default_value = 0.5
  huesat_node02.inputs[2].default_value = 1.5
  background_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  background_node04 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")

  world.node_tree.links.new(mixshader_node01.outputs[0], output_node01.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], output_node02.inputs[0])
  world.node_tree.links.new(mixshader_node03.outputs[0], mixshader_node01.inputs[2])
  world.node_tree.links.new(mixshader_node03.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node01.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  world.node_tree.links.new(background_node01.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node03.inputs[1])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node03.inputs[2])
  world.node_tree.links.new(background_node04.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(huesat_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(huesat_node02.outputs[0], background_node04.inputs[0])
  world.node_tree.links.new(tex_env_node.outputs[0], background_node02.inputs[0])

  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node01.inputs[0])
  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node02.inputs[0])
  world.node_tree.links.new(mapping_node.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node.inputs[0])

  return world

def RM_World(world_texture_path, world_texture_name, suffix):
  tex_dir = os.path.join(os.path.dirname(current_path), world_texture_path)
  
  world = bpy.data.worlds.new('World.' + suffix)
  bpy.context.scene.world = world
  bpy.context.scene.world.color = BASE_COLOR
  bpy.context.scene.world.use_nodes = True
  output_node = bpy.data.worlds["World."+suffix].node_tree.nodes["World Output"]
  world.node_tree.links.remove(output_node.inputs[0].links[0])
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node01.inputs[2].default_value[2] = -1.22173
  mapping_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node02.inputs[1].default_value[2] = 0.3
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(world_texture_name)
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node.inputs[1].default_value = 0.25
  huesat_node.inputs[2].default_value = 1.0
  gamma_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeGamma")
  gamma_node01.inputs[1].default_value = 1.0
  gamma_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeGamma")
  gamma_node02.inputs[1].default_value = 0.9
  background_node01 = bpy.data.worlds["World."+suffix].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixrbg_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixRGB")
  mixrbg_node.blend_type = 'MULTIPLY'
  mixrbg_node.inputs[0].default_value = 0.3
  colorramp_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeValToRGB")
  colorramp_node.color_ramp.elements[0].position = 0.25
  colorramp_node.color_ramp.elements[1].position = 0.327273
  separate_rgb_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeSeparateRGB")

  world.node_tree.links.new(mixshader_node01.outputs[0], output_node.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node01.inputs[2])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node02.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[3], mixshader_node01.inputs[0])
  world.node_tree.links.new(background_node01.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(gamma_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(gamma_node02.outputs[0], background_node02.inputs[0])
  world.node_tree.links.new(huesat_node.outputs[0], gamma_node02.inputs[0])
  world.node_tree.links.new(mixrbg_node.outputs[0], gamma_node01.inputs[0])
  world.node_tree.links.new(mixrbg_node.outputs[0], huesat_node.inputs[0])

  world.node_tree.links.new(tex_env_node.outputs[0], mixrbg_node.inputs[1])
  world.node_tree.links.new(mapping_node01.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node01.inputs[0])

  world.node_tree.links.new(colorramp_node.outputs[0], mixrbg_node.inputs[2])
  world.node_tree.links.new(separate_rgb_node.outputs[2], colorramp_node.inputs[0])
  world.node_tree.links.new(mapping_node02.outputs[0], separate_rgb_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node02.inputs[0])

  return world
