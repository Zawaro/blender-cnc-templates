import os

import bpy

BASE_COLOR = (0, 0, 0)


def Base_World(props, compat):
  project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  tex_dir = os.path.join(project_root, props["world_texture_path"])

  world = bpy.data.worlds.new("World." + props["suffix"])
  world.use_nodes = True
  bpy.context.scene.world = world
  if hasattr(world, "color"):
    world.color = BASE_COLOR
  elif hasattr(bpy.context.scene, "world") and hasattr(bpy.context.scene.world, "horizon_color"):
    bpy.context.scene.world.horizon_color = BASE_COLOR

  tree = world.node_tree
  nodes = tree.nodes
  links = tree.links

  output01 = nodes["World Output"]
  output01.target = "CYCLES"
  output02 = nodes.new("ShaderNodeOutputWorld")
  output02.target = "EEVEE"
  links.remove(output01.inputs[0].links[0])

  tex_coord = nodes.new("ShaderNodeTexCoord")
  lightpath = nodes.new("ShaderNodeLightPath")
  mapping01 = nodes.new("ShaderNodeMapping")
  mapping01.inputs[1].default_value[2] = 0.3
  mapping02 = nodes.new("ShaderNodeMapping")
  mapping02.inputs[2].default_value[2] = -1.5708

  data_image = bpy.data.images.get(props["world_texture_name"])
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env = nodes.new("ShaderNodeTexEnvironment")
  tex_env.image = data_image
  tex_env.image.use_fake_user = True

  huesat01 = nodes.new("ShaderNodeHueSaturation")
  huesat01.inputs[0].default_value = props["huesat_node01_input0"]
  huesat01.inputs[1].default_value = props["huesat_node01_input1"]
  huesat01.inputs[2].default_value = props["huesat_node01_input2"]
  huesat02 = nodes.new("ShaderNodeHueSaturation")
  huesat02.inputs[0].default_value = props["huesat_node02_input0"]
  huesat02.inputs[1].default_value = props["huesat_node02_input1"]
  huesat02.inputs[2].default_value = props["huesat_node02_input2"]

  bg01 = nodes["Background"]
  bg02 = nodes.new("ShaderNodeBackground")
  bg02.inputs[0].default_value = (1, 1, 1, 1)
  bg03 = nodes.new("ShaderNodeBackground")
  bg03.inputs[0].default_value = (0, 0, 1, 1)
  bg04 = nodes.new("ShaderNodeBackground")

  mix01 = nodes.new("ShaderNodeMixShader")
  mix02 = nodes.new("ShaderNodeMixShader")
  mix03 = nodes.new("ShaderNodeMixShader")
  mixrgb = nodes.new("ShaderNodeMixRGB")
  mixrgb.inputs[1].default_value = (0, 0, 0, 1)

  cr01 = nodes.new("ShaderNodeValToRGB")
  cr01.color_ramp.elements[0].position = 0.25
  cr01.color_ramp.elements[1].position = 0.327273
  cr02 = nodes.new("ShaderNodeValToRGB")
  cr02.color_ramp.interpolation = "EASE"
  cr02.color_ramp.elements[0].position = 0.5
  cr02.color_ramp.elements[1].position = 1.0

  sep_rgb = nodes.new(compat.SEPARATE_RGB_NODE)

  tex_sky = nodes.new("ShaderNodeTexSky")
  tex_sky.sun_size = props["tex_sky_node_sun_size"]
  tex_sky.sun_intensity = props["tex_sky_node_sun_intensity"]
  tex_sky.sun_elevation = props["tex_sky_node_sun_elevation"]
  tex_sky.sun_rotation = props["tex_sky_node_sun_rotation"]
  tex_sky.altitude = props["tex_sky_node_altitude"]
  tex_sky.air_density = props["tex_sky_node_air_density"]
  density_prop = compat.get_sky_density_property()
  setattr(tex_sky, density_prop, props["tex_sky_node_dust_density"])
  tex_sky.ozone_density = props["tex_sky_node_ozone_density"]
  sky_type = compat.get_sky_type_value()
  if sky_type is not None:
    tex_sky.sky_type = sky_type

  tex_noise = nodes.new("ShaderNodeTexNoise")
  tex_noise.inputs[2].default_value = props["tex_noise_node_input2"]
  tex_noise.inputs[3].default_value = props["tex_noise_node_input3"]
  tex_noise.inputs[5].default_value = props["tex_noise_node_input5"]

  # Cycles output
  links.new(mix01.outputs[0], output01.inputs[0])
  links.new(lightpath.outputs[0], mix01.inputs[0])
  links.new(mix02.outputs[0], mix01.inputs[1])
  links.new(mixrgb.outputs[0], mix02.inputs[0])
  links.new(cr01.outputs[0], mixrgb.inputs[0])
  links.new(sep_rgb.outputs[2], cr01.inputs[0])
  links.new(mapping01.outputs[0], sep_rgb.inputs[0])
  links.new(tex_coord.outputs[0], mapping01.inputs[0])
  links.new(bg01.outputs[0], mix02.inputs[1])
  links.new(huesat01.outputs[0], bg01.inputs[0])
  links.new(tex_sky.outputs[0], huesat01.inputs[4])
  links.new(bg02.outputs[0], mix02.inputs[2])
  links.new(bg03.outputs[0], mix01.inputs[2])
  links.new(cr02.outputs[0], mixrgb.inputs[2])
  links.new(tex_noise.outputs[0], cr02.inputs[0])
  links.new(mapping01.outputs[0], tex_noise.inputs[0])

  # Eevee output
  links.new(mix03.outputs[0], output02.inputs[0])
  links.new(lightpath.outputs[0], mix03.inputs[0])
  links.new(bg03.outputs[0], mix03.inputs[2])
  links.new(bg04.outputs[0], mix03.inputs[1])
  links.new(tex_env.outputs[0], huesat02.inputs[4])
  links.new(huesat02.outputs[0], bg04.inputs[0])
  links.new(mapping02.outputs[0], tex_env.inputs[0])
  links.new(tex_coord.outputs[0], mapping02.inputs[0])

  return world


WORLD_DATA = {
  "RA2": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.933751,
    "tex_sky_node_sun_rotation": 3.54302,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
  "RA2_INF": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 1.5708,
    "tex_sky_node_sun_rotation": 3.54302,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
  "RA1": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 1.37881,
    "tex_sky_node_sun_rotation": 5.29184,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
  "RW": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.942478,
    "tex_sky_node_sun_rotation": 3.20966,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.0,
    "huesat_node01_input1": 0.5,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.0,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
  "TS": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.942478,
    "tex_sky_node_sun_rotation": 3.20966,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.0,
    "huesat_node01_input1": 0.5,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.0,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
  "D2K": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.884882,
    "tex_sky_node_sun_rotation": 3.92874,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.0,
    "huesat_node01_input1": 0.5,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.0,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
  "RM": {
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 1.37881,
    "tex_sky_node_sun_rotation": 5.29184,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_dust_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  },
}

# RA2_INF has a different sun_elevation (top-down view)
WORLD_DATA["RA2_INF"] = {
  **WORLD_DATA["RA2"],
  "tex_sky_node_sun_elevation": 1.5708,
}


def RA2_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["RA2"]}
  return Base_World(data, compat)


def RA2_INF_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["RA2_INF"]}
  return Base_World(data, compat)


def RA1_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["RA1"]}
  return Base_World(data, compat)


def RW_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["RW"]}
  return Base_World(data, compat)


def TS_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["TS"]}
  return Base_World(data, compat)


def D2K_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["D2K"]}
  return Base_World(data, compat)


def RM_World(suffix, props, compat):
  data = {**props, "suffix": suffix, **WORLD_DATA["RM"]}
  return Base_World(data, compat)


WORLD_CLASS_MAP = {
  "RA2": RA2_World,
  "RA2_INF": RA2_INF_World,
  "RA1": RA1_World,
  "RW": RW_World,
  "TS": TS_World,
  "D2K": D2K_World,
  "RM": RM_World,
}
