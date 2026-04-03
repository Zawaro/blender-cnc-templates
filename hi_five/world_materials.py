import os
import bpy
from typing import TypedDict

current_path = os.path.dirname(os.path.realpath(__file__))

BASE_COLOR = (0, 0, 0)


class WorldProperties(TypedDict):
  world_texture_path: str
  world_texture_name: str


class BaseProperties(WorldProperties):
  # Cycles HueSat Node for Sky
  huesat_node01_input0: float
  huesat_node01_input1: float
  huesat_node01_input2: float

  # Eevee HueSat Node for Environment Texture
  huesat_node02_input0: float
  huesat_node02_input1: float
  huesat_node02_input2: float

  # Cycles Sky Texture Node
  tex_sky_node_sun_size: float
  tex_sky_node_sun_intensity: float
  tex_sky_node_sun_elevation: float
  tex_sky_node_sun_rotation: float
  tex_sky_node_altitude: float
  tex_sky_node_air_density: float
  tex_sky_node_aerosol_density: float
  tex_sky_node_ozone_density: float

  # Cycles Noise Texture Node for
  tex_noise_node_input2: float
  tex_noise_node_input3: float
  tex_noise_node_input5: float


def Base_World(props: WorldProperties):
  tex_dir = os.path.join(os.path.dirname(current_path), props["world_texture_path"])

  world = bpy.data.worlds.new("World." + props["suffix"])
  bpy.context.scene.world = world
  bpy.context.scene.world.color = BASE_COLOR

  node_tree = world.node_tree
  output_node01 = node_tree.nodes["World Output"]
  output_node01.target = "CYCLES"
  output_node02 = node_tree.nodes.new("ShaderNodeOutputWorld")
  output_node02.target = "EEVEE"
  world.node_tree.links.remove(output_node01.inputs[0].links[0])
  tex_coord_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexCoord")
  lightpath_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeLightPath")
  mapping_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node01.inputs[1].default_value[2] = 0.3
  mapping_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMapping")
  mapping_node02.inputs[2].default_value[2] = -1.5708
  # Recycle the same world texture file instead of loading new one again and again
  data_image = bpy.data.images.get(props["world_texture_name"])
  if not data_image:
    data_image = bpy.data.images.load(tex_dir)
  tex_env_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env_node.image = data_image
  tex_env_node.image.use_fake_user = True
  huesat_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node01.inputs[0].default_value = props["huesat_node01_input0"]
  huesat_node01.inputs[1].default_value = props["huesat_node01_input1"]
  huesat_node01.inputs[2].default_value = props["huesat_node01_input2"]
  huesat_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeHueSaturation")
  huesat_node02.inputs[0].default_value = props["huesat_node02_input0"]
  huesat_node02.inputs[1].default_value = props["huesat_node02_input1"]
  huesat_node02.inputs[2].default_value = props["huesat_node02_input2"]
  background_node01 = bpy.data.worlds["World." + props["suffix"]].node_tree.nodes["Background"]
  background_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node02.inputs[0].default_value = (1, 1, 1, 1)
  background_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  background_node03.inputs[0].default_value = (0, 0, 1, 1)
  background_node04 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeBackground")
  mixshader_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixshader_node03 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixShader")
  mixrbg_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeMixRGB")
  mixrbg_node.inputs[1].default_value = (0, 0, 0, 1)
  colorramp_node01 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeValToRGB")
  colorramp_node01.color_ramp.elements[0].position = 0.25
  colorramp_node01.color_ramp.elements[1].position = 0.327273
  colorramp_node02 = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeValToRGB")
  colorramp_node02.color_ramp.interpolation = "EASE"
  colorramp_node02.color_ramp.elements[0].position = 0.5
  colorramp_node02.color_ramp.elements[1].position = 1.0
  separate_rgb_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeSeparateColor")
  tex_sky_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexSky")
  tex_sky_node.sun_size = props["tex_sky_node_sun_size"]
  tex_sky_node.sun_intensity = props["tex_sky_node_sun_intensity"]
  tex_sky_node.sun_elevation = props["tex_sky_node_sun_elevation"]
  tex_sky_node.sun_rotation = props["tex_sky_node_sun_rotation"]
  tex_sky_node.altitude = props["tex_sky_node_altitude"]
  tex_sky_node.air_density = props["tex_sky_node_air_density"]
  tex_sky_node.aerosol_density = props["tex_sky_node_aerosol_density"]
  tex_sky_node.ozone_density = props["tex_sky_node_ozone_density"]
  tex_sky_node.sky_type = "SINGLE_SCATTERING"
  tex_noise_node = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexNoise")
  tex_noise_node.inputs[2].default_value = props["tex_noise_node_input2"]
  tex_noise_node.inputs[3].default_value = props["tex_noise_node_input3"]
  tex_noise_node.inputs[5].default_value = props["tex_noise_node_input5"]

  ## World Materials are linked from right to left and top to bottom
  # Cycles Output
  world.node_tree.links.new(mixshader_node01.outputs[0], output_node01.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node01.inputs[0])
  world.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node01.inputs[1])
  world.node_tree.links.new(mixrbg_node.outputs[0], mixshader_node02.inputs[0])
  world.node_tree.links.new(colorramp_node01.outputs[0], mixrbg_node.inputs[0])
  world.node_tree.links.new(separate_rgb_node.outputs[2], colorramp_node01.inputs[0])
  world.node_tree.links.new(mapping_node01.outputs[0], separate_rgb_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node01.inputs[0])

  world.node_tree.links.new(background_node01.outputs[0], mixshader_node02.inputs[1])
  world.node_tree.links.new(huesat_node01.outputs[0], background_node01.inputs[0])
  world.node_tree.links.new(tex_sky_node.outputs[0], huesat_node01.inputs[4])
  world.node_tree.links.new(background_node02.outputs[0], mixshader_node02.inputs[2])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node01.inputs[2])

  world.node_tree.links.new(colorramp_node02.outputs[0], mixrbg_node.inputs[2])
  world.node_tree.links.new(tex_noise_node.outputs[0], colorramp_node02.inputs[0])
  world.node_tree.links.new(mapping_node01.outputs[0], tex_noise_node.inputs[0])

  # Eevee Output
  world.node_tree.links.new(mixshader_node03.outputs[0], output_node02.inputs[0])
  world.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  world.node_tree.links.new(background_node03.outputs[0], mixshader_node03.inputs[2])
  world.node_tree.links.new(background_node04.outputs[0], mixshader_node03.inputs[1])
  world.node_tree.links.new(tex_env_node.outputs[0], huesat_node02.inputs[4])
  world.node_tree.links.new(huesat_node02.outputs[0], background_node04.inputs[0])
  world.node_tree.links.new(mapping_node02.outputs[0], tex_env_node.inputs[0])
  world.node_tree.links.new(tex_coord_node.outputs[0], mapping_node02.inputs[0])

  return world


def RA2_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.933751,
    "tex_sky_node_sun_rotation": 3.54302,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)


def RA2_INF_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 1.5708,
    "tex_sky_node_sun_rotation": 3.54302,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)


def RA1_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 1.37881,
    "tex_sky_node_sun_rotation": 5.29184,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)


def RW_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.942478,
    "tex_sky_node_sun_rotation": 3.20966,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.0,
    "huesat_node01_input1": 0.5,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.0,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)


def TS_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.942478,
    "tex_sky_node_sun_rotation": 3.20966,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.0,
    "huesat_node01_input1": 0.5,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.0,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)


def D2K_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 0.884882,
    "tex_sky_node_sun_rotation": 3.92874,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.0,
    "huesat_node01_input1": 0.5,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.0,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)


def RM_World(suffix: str, props: WorldProperties):
  properties: BaseProperties = {
    **props,
    "suffix": suffix,
    # Cycles Sky Texture Node
    "tex_sky_node_sun_size": 0,
    "tex_sky_node_sun_intensity": 0.1,
    "tex_sky_node_sun_elevation": 1.37881,
    "tex_sky_node_sun_rotation": 5.29184,
    "tex_sky_node_altitude": 20000,
    "tex_sky_node_air_density": 1,
    "tex_sky_node_aerosol_density": 0.05,
    "tex_sky_node_ozone_density": 0.05,
    # Cycles Noise Texture Node for Sky
    "tex_noise_node_input2": 4,
    "tex_noise_node_input3": 5,
    "tex_noise_node_input5": 0.5,
    # Cycles HueSat Node for Sky
    "huesat_node01_input0": 0.5,
    "huesat_node01_input1": 0.75,
    "huesat_node01_input2": 0.9,
    # Eevee HueSat Node for Environment Texture
    "huesat_node02_input0": 0.5,
    "huesat_node02_input1": 0.5,
    "huesat_node02_input2": 0.6,
  }

  return Base_World(properties)
