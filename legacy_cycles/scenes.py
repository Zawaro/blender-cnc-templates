import os
import sys
import bpy

# Hack to import modules from current script path
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(current_path)
sys.path.append(parent_path)

from shared import constants
from shared.node_arrange import arrange_nodes

from world_materials import D2K_World, RA1_World, RA2_World, RM_World, RW_World, TS_World
from plane_materials import Plane_Ambient, Plane_Blue, Plane_Grey, Plane_Holdout, Plane_Shadow

# Base values uses Red Alert 2 scene values
class BaseScene():
  # - Info
  name = "Scene"
  type = ""
  full_name = "Scene"
  suffix = "SC"

  # - Scene settings
  cycles_device = 'GPU'
  cycles_filter_width = constants.CYCLES_FILTER_WIDTH
  cycles_max_bounces = 4
  cycles_pixel_filter_type = 'GAUSSIAN'
  cycles_preview_samples = 10
  cycles_samples = 64
  cycles_adaptive_min_samples = 32
  cycles_sample_clamp_indirect = 0.05
  cycles_transmission_bounces = 8
  cycles_use_denoising = False # Disabled in Blender 3.x, using nodes instead
  cycles_volume_bounces = 1
  cycles_film_transparent = True

  frame_start = 0
  render_fps = 10
  render_dither_intensity = 0 # Important, prevents bg noise
  render_image_settings_compression = 90
  render_image_settings_color_mode = 'RGB'
  render_resolution_x = 640
  render_resolution_y = 480
  render_use_single_layer = True
  unit_settings_system = 'NONE'
  view_settings_view_transform = 'Standard'
  view_settings_look = 'None'
  view_settings_exposure = 0

  # - Camera
  camera_location = [110.039, -110.039, 89.84670]
  camera_rotation = [1.0472, 0, 0.785398]
  camera_name = 'Camera.' + suffix
  camera_type = 'ORTHO'
  camera_ortho_scale = 29.92

  # - Light
  sun01_location = [-4.14, -10, 12.27]
  sun01_rotation = [0.633555, 0.0726057, 5.79449]
  sun01_energy = 6.5
  sun01_angle = 0.00392699
  sun01_shadow_buffer_bias = 0.02
  sun01_shadow_cascade_count = 2
  sun01_shadow_cascade_fade = 1
  sun01_shadow_cascade_max_distance = 1000
  sun01_shadow_cascade_exponent = 0.8
  sun01_contact_shadow_distance = 1000
  sun01_contact_shadow_bias = 0.5
  sun01_contact_shadow_thickness = 0.7

  sun02_energy = 2.3
  sun02_shadow_cascade_count = 4
  sun02_shadow_cascade_fade = 0.0
  sun02_shadow_cascade_max_distance = 1000
  sun02_shadow_cascade_exponent = 1.0

  # - Compose
  colorramp_position01 = 0.717273
  colorramp_position02 = 0.722727
  colorramp_color01 = (0, 0, 1, 0)
  colorramp_color02 = (0, 0, 0.250158, 1)

  # Create a new scene and make it active
  def create_scene(self):
    bpy.ops.scene.new(type='NEW')
    bpy.context.scene.name = self.full_name

  # Original default scene is no longer needed acter creating all the template scenes
  def cleanup(self):
    self.select_scene()
    bpy.ops.scene.delete()

  # Sets current scene active
  def select_scene(self):
    bpy.context.window.screen.scene = bpy.data.scenes[self.full_name]

  def set_full_name(self):
    if self.type:
      self.full_name = "{} - {}".format(self.name, self.type)

  def set_cycles_settings(self):
    bpy.context.scene.cycles.device = self.cycles_device
    bpy.context.scene.cycles.filter_width = self.cycles_filter_width
    bpy.context.scene.cycles.max_bounces = self.cycles_max_bounces
    bpy.context.scene.cycles.pixel_filter_type = self.cycles_pixel_filter_type
    bpy.context.scene.cycles.preview_samples = self.cycles_preview_samples
    bpy.context.scene.cycles.samples = self.cycles_samples
    bpy.context.scene.cycles.adaptive_min_samples = self.cycles_adaptive_min_samples
    bpy.context.scene.cycles.sample_clamp_indirect = self.cycles_sample_clamp_indirect
    bpy.context.scene.cycles.transmission_bounces = self.cycles_transmission_bounces
    bpy.context.scene.cycles.use_denoising = self.cycles_use_denoising
    bpy.context.scene.cycles.volume_bounces = self.cycles_volume_bounces
    bpy.context.scene.cycles.film_transparent = self.cycles_film_transparent

  def set_render_settings(self):
    bpy.context.scene.name = self.full_name
    bpy.context.scene.frame_start = self.frame_start
    bpy.context.scene.render.fps = self.render_fps
    bpy.context.scene.render.dither_intensity = self.render_dither_intensity
    bpy.context.scene.render.image_settings.compression = self.render_image_settings_compression
    bpy.context.scene.render.image_settings.color_mode = self.render_image_settings_color_mode
    bpy.context.scene.render.resolution_x = self.render_resolution_x
    bpy.context.scene.render.resolution_y = self.render_resolution_y
    bpy.context.scene.render.use_single_layer = self.render_use_single_layer
    bpy.context.scene.view_layers['ViewLayer'].cycles.denoising_store_passes = True
    bpy.context.scene.unit_settings.system = self.unit_settings_system
    bpy.context.scene.view_settings.view_transform = self.view_settings_view_transform
    bpy.context.scene.view_settings.look = self.view_settings_look
    bpy.context.scene.view_settings.exposure = self.view_settings_exposure

  def create_collections(self):
    collection = bpy.data.collections.new(self.full_name)
    bpy.context.scene.collection.children.link(collection)
    
    template_collection = bpy.data.collections.new(self.full_name + " Template")
    bpy.context.scene.collection.children.link(template_collection)
    
    bpy.context.view_layer.active_layer_collection = \
      bpy.context.view_layer.layer_collection.children[self.full_name + " Template"]
    shadow_collection = bpy.data.collections.new(self.full_name + " Shadow")
    template_collection.children.link(shadow_collection)
    holdout_collection = bpy.data.collections.new(self.full_name + " Holdout")
    template_collection.children.link(holdout_collection)

  def create_camera(self, name=camera_name, location=camera_location, rotation=camera_rotation, camera_type=camera_type, ortho_scale=camera_ortho_scale):
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=location, rotation=rotation, scale=(1, 1, 1))
    bpy.context.active_object.name = name
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.data.name = name
    bpy.context.active_object.data.type = camera_type
    if (camera_type == 'PERSP'):
      bpy.context.active_object.data.lens_unit = 'FOV'
      bpy.context.active_object.data.angle = 1.0472
    else:
      bpy.context.active_object.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = bpy.data.objects[name]
    for area in bpy.context.screen.areas:
      if area.type == 'VIEW_3D':
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        break

  def create_light(self):
    # - Normal Sun
    bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=self.sun01_location, rotation=self.sun01_rotation, scale=(1, 1, 1))
    bpy.context.active_object.name = 'Sun.' + self.suffix
    bpy.context.active_object.data.name = "Sun." + self.suffix
    bpy.context.active_object.data.energy = self.sun01_energy
    bpy.context.active_object.data.angle = self.sun01_angle
    bpy.context.active_object.data.cycles.use_multiple_importance_sampling = False
    bpy.context.active_object.data.shadow_buffer_bias = self.sun01_shadow_buffer_bias
    bpy.context.active_object.data.shadow_cascade_count = self.sun01_shadow_cascade_count
    bpy.context.active_object.data.shadow_cascade_fade = self.sun01_shadow_cascade_fade
    bpy.context.active_object.data.shadow_cascade_max_distance = self.sun01_shadow_cascade_max_distance
    bpy.context.active_object.data.shadow_cascade_exponent = self.sun01_shadow_cascade_exponent
    bpy.context.active_object.data.use_contact_shadow = True
    bpy.context.active_object.data.contact_shadow_distance = self.sun01_contact_shadow_distance
    bpy.context.active_object.data.contact_shadow_bias = self.sun01_contact_shadow_bias
    bpy.context.active_object.data.contact_shadow_thickness = self.sun01_contact_shadow_thickness
    bpy.context.active_object.hide_select = True

    # - Sun for rendering shadows with Shadow script
    bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=self.sun01_location, rotation=self.sun01_rotation, scale=(1, 1, 1))
    bpy.context.active_object.name = 'Sun.shadow.' + self.suffix
    bpy.context.active_object.data.name = "Sun.shadow." + self.suffix
    bpy.context.active_object.data.energy = self.sun02_energy
    bpy.context.active_object.data.angle = self.sun01_angle
    bpy.context.active_object.data.cycles.use_multiple_importance_sampling = False
    bpy.context.active_object.data.shadow_buffer_bias = self.sun01_shadow_buffer_bias
    bpy.context.active_object.data.shadow_cascade_count = self.sun02_shadow_cascade_count
    bpy.context.active_object.data.shadow_cascade_fade = self.sun02_shadow_cascade_fade
    bpy.context.active_object.data.shadow_cascade_max_distance = self.sun02_shadow_cascade_max_distance
    bpy.context.active_object.data.shadow_cascade_exponent = self.sun02_shadow_cascade_exponent
    bpy.context.active_object.data.use_contact_shadow = False
    bpy.context.active_object.hide_select = True
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True

  def create_planes(self):
    ambient_mat = Plane_Ambient(self.suffix)
    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -20), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.ambient.' + self.suffix
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.data.materials.append(ambient_mat)

    blue_mat = Plane_Blue(self.suffix)
    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -0.01), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.blue.' + self.suffix
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.data.materials.append(blue_mat)

    grey_mat = Plane_Grey(self.suffix)
    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -0.01), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.grey.' + self.suffix
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.data.materials.append(grey_mat)

    holdout_mat = Plane_Holdout(self.suffix)
    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -0.01), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.holdout2.' + self.suffix
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.data.materials.append(holdout_mat)
    bpy.context.active_object.data.materials[0].blend_method = 'BLEND'
    bpy.context.active_object.data.materials[0].shadow_method = 'NONE'

    shadow_mat = Plane_Shadow(self.suffix)
    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -0.01), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.shadow2.' + self.suffix
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.is_shadow_catcher = True
    bpy.context.active_object.data.materials.append(shadow_mat)
    bpy.context.active_object.data.materials[0].blend_method = 'BLEND'
    bpy.context.active_object.data.materials[0].shadow_method = 'NONE'

    bpy.context.view_layer.active_layer_collection = \
    bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Shadow"]

    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -0.01), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.shadow.' + self.suffix
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.is_shadow_catcher = True
    bpy.context.active_object.data.materials.append(shadow_mat)
    bpy.context.active_object.data.materials[0].blend_method = 'BLEND'
    bpy.context.active_object.data.materials[0].shadow_method = 'NONE'

    bpy.context.view_layer.active_layer_collection = \
    bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Holdout"]

    bpy.ops.mesh.primitive_plane_add(size=140, enter_editmode=False, align='WORLD', location=(0, 0, -0.015), scale=(1, 1, 1))
    bpy.context.active_object.name = 'Plane.holdout.' + self.suffix
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_viewport = True
    bpy.context.active_object.visible_glossy = False
    bpy.context.active_object.data.materials.append(holdout_mat)
    bpy.context.active_object.data.materials[0].blend_method = 'BLEND'
    bpy.context.active_object.data.materials[0].shadow_method = 'NONE'

    bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Holdout"].exclude = True

    # Arrange material nodes
    arrange_nodes([ambient_mat.node_tree, blue_mat.node_tree, grey_mat.node_tree, holdout_mat.node_tree, shadow_mat.node_tree])

  def create_shadow_layer(self):
    bpy.ops.scene.view_layer_add(type='NEW')
    bpy.context.view_layer.name = "ShadowLayer"
    bpy.context.window.view_layer = bpy.context.scene.view_layers['ShadowLayer']
    bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Shadow"].exclude = True
    bpy.context.window.view_layer = bpy.context.scene.view_layers['ViewLayer']

  def create_composite_nodes(self):
    # Required in order to connect Render Layer node to Denoise node
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.use_nodes = True
    renderlayers_node01 = bpy.data.scenes[self.full_name].node_tree.nodes["Render Layers"]
    renderlayers_node02 = bpy.context.scene.node_tree.nodes.new("CompositorNodeRLayers")
    renderlayers_node02.layer = "ShadowLayer"
    composite_node01 = bpy.data.scenes[self.full_name].node_tree.nodes["Composite"]

    switch_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeSwitch")
    switch_node01.name = "Object"
    switch_node01.label = "Object"
    switch_node02 = bpy.context.scene.node_tree.nodes.new("CompositorNodeSwitch")
    switch_node02.name = "Buildup"
    switch_node02.label = "Buildup"
    switch_node03 = bpy.context.scene.node_tree.nodes.new("CompositorNodeSwitch")
    switch_node03.name = "Shadow"
    switch_node03.label = "Shadow"
    switch_node04 = bpy.context.scene.node_tree.nodes.new("CompositorNodeSwitch")
    switch_node04.name = "Preview"
    switch_node04.label = "Preview"
    switch_node05 = bpy.context.scene.node_tree.nodes.new("CompositorNodeSwitch")
    switch_node05.name = "Alpha"
    switch_node05.label = "Alpha"

    alpha_group01 = bpy.data.node_groups.new(type="CompositorNodeTree", name="Alpha Convert")
    alpha_group01.inputs.new("NodeSocketColor", "Image")
    alpha_group01_input = alpha_group01.nodes.new("NodeGroupInput")
    alpha_group01_input.location = (-400, 0)
    alpha_group01.outputs.new("NodeSocketColor", "Image")
    alpha_group01.outputs.new("NodeSocketFloat", "Alpha")
    alpha_group01_output = alpha_group01.nodes.new("NodeGroupOutput")
    alpha_group01_output.location = (400, 0)
    alpha_group01_sHSVA = alpha_group01.nodes.new("CompositorNodeSepHSVA")
    alpha_group01_sHSVA.location = (-200, 200)
    alpha_group01_cHSVA = alpha_group01.nodes.new("CompositorNodeCombHSVA")
    alpha_group01_cHSVA.location = (200, 200)
    alpha_group01_math = alpha_group01.nodes.new("CompositorNodeMath")
    alpha_group01_math.location = (0, 0)
    alpha_group01_math.operation = "GREATER_THAN"
    alpha_group01_math.inputs[1].default_value = 0.325
    alpha_group01.links.new(alpha_group01_input.outputs[0], alpha_group01_sHSVA.inputs[0])
    alpha_group01.links.new(alpha_group01_sHSVA.outputs[0], alpha_group01_cHSVA.inputs[0])
    alpha_group01.links.new(alpha_group01_sHSVA.outputs[1], alpha_group01_cHSVA.inputs[1])
    alpha_group01.links.new(alpha_group01_sHSVA.outputs[2], alpha_group01_cHSVA.inputs[2])
    alpha_group01.links.new(alpha_group01_sHSVA.outputs[3], alpha_group01_math.inputs[0])
    alpha_group01.links.new(alpha_group01_math.outputs[0], alpha_group01_cHSVA.inputs[3])
    alpha_group01.links.new(alpha_group01_math.outputs[0], alpha_group01_output.inputs[1])
    alpha_group01.links.new(alpha_group01_cHSVA.outputs[0], alpha_group01_output.inputs[0])
    alpha_convert_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeGroup")
    alpha_convert_node01.node_tree = alpha_group01
    alpha_convert_node02 = bpy.context.scene.node_tree.nodes.new("CompositorNodeGroup")
    alpha_convert_node02.node_tree = alpha_group01

    denoise_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeDenoise")
    denoise_node01.prefilter = 'NONE'
    subtract_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeMixRGB")
    subtract_node01.blend_type = 'SUBTRACT'
    subtract_node01.inputs[0].default_value = 1
    colorramp_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeValToRGB")
    colorramp_node01.color_ramp.elements[0].position = self.colorramp_position01
    colorramp_node01.color_ramp.elements[0].color = self.colorramp_color01
    colorramp_node01.color_ramp.elements[1].position = self.colorramp_position02
    colorramp_node01.color_ramp.elements[1].color = self.colorramp_color02
    rgb_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeRGB")
    rgb_node01.outputs[0].default_value = (0, 0, 1, 1)
    rgb_node01.name = 'BackgroundRGB'
    rgb_node01.label = 'BackgroundRGB'
    rgb_node02 = bpy.context.scene.node_tree.nodes.new("CompositorNodeRGB")
    rgb_node02.outputs[0].default_value = (0, 0, 0, 0)
    rgb_node02.name = 'BackgroundAlpha'
    rgb_node02.label = 'BackgroundAlpha'
    alphaover_node01 = bpy.context.scene.node_tree.nodes.new("CompositorNodeAlphaOver")
    alphaover_node01.use_premultiply = True
    alphaover_node02 = bpy.context.scene.node_tree.nodes.new("CompositorNodeAlphaOver")
    alphaover_node02.use_premultiply = True

    bpy.context.scene.node_tree.links.new(switch_node04.outputs[0], composite_node01.inputs[0])
    bpy.context.scene.node_tree.links.new(switch_node03.outputs[0], switch_node04.inputs[0])
    bpy.context.scene.node_tree.links.new(switch_node02.outputs[0], switch_node03.inputs[0])
    bpy.context.scene.node_tree.links.new(switch_node01.outputs[0], switch_node02.inputs[0])

    bpy.context.scene.node_tree.links.new(renderlayers_node01.outputs[0], denoise_node01.inputs[0])
    bpy.context.scene.node_tree.links.new(renderlayers_node01.outputs[2], denoise_node01.inputs[1])
    bpy.context.scene.node_tree.links.new(renderlayers_node01.outputs[3], denoise_node01.inputs[2])
    bpy.context.scene.node_tree.links.new(denoise_node01.outputs[0], switch_node01.inputs[0])
    bpy.context.scene.node_tree.links.new(denoise_node01.outputs[0], alpha_convert_node01.inputs[0])
    bpy.context.scene.node_tree.links.new(alpha_convert_node01.outputs[0], alphaover_node01.inputs[2])

    bpy.context.scene.node_tree.links.new(renderlayers_node02.outputs[0], alpha_convert_node02.inputs[0])
    bpy.context.scene.node_tree.links.new(alpha_convert_node02.outputs[1], subtract_node01.inputs[2])
    bpy.context.scene.node_tree.links.new(alpha_convert_node01.outputs[1], subtract_node01.inputs[1])
    bpy.context.scene.node_tree.links.new(subtract_node01.outputs[0], colorramp_node01.inputs[0])
    bpy.context.scene.node_tree.links.new(colorramp_node01.outputs[0], alphaover_node02.inputs[2])

    bpy.context.scene.node_tree.links.new(rgb_node01.outputs[0], switch_node05.inputs[0])
    bpy.context.scene.node_tree.links.new(rgb_node02.outputs[0], switch_node05.inputs[1])
    bpy.context.scene.node_tree.links.new(switch_node05.outputs[0], alphaover_node01.inputs[1])
    bpy.context.scene.node_tree.links.new(switch_node05.outputs[0], alphaover_node02.inputs[1])

    bpy.context.scene.node_tree.links.new(alphaover_node01.outputs[0], switch_node01.inputs[1])
    bpy.context.scene.node_tree.links.new(alphaover_node01.outputs[0], switch_node02.inputs[1])
    bpy.context.scene.node_tree.links.new(alphaover_node01.outputs[0], switch_node03.inputs[1])
    bpy.context.scene.node_tree.links.new(alphaover_node02.outputs[0], switch_node04.inputs[1])
    bpy.context.scene.node_tree.links.new(alphaover_node02.outputs[0], switch_node05.inputs[1])

    # Arrange composite nodes
    arrange_nodes([bpy.context.scene.node_tree])

#######################
## -- Red Alert 2 -- ##
#######################

class RA2(BaseScene):
  name = "Red Alert 2"
  type = ""
  full_name = "Red Alert 2"
  suffix = "RA2"
  camera_name = 'Camera.' + suffix

  world_texture_name = 'generic_hdri.exr'
  world_texture_path = 'shared/generic_hdri.exr'

  def __init__(self):
    self.set_full_name()
    self.create_scene()
    self.select_scene()
    
    self.set_cycles_settings()
    self.set_render_settings()
    self.create_collections()
    self.create_camera(self.camera_name, self.camera_location, self.camera_rotation, self.camera_type, self.camera_ortho_scale)
    self.create_light()
    world = RA2_World(self.world_texture_path, self.world_texture_name, self.suffix)
    self.create_planes()
    self.create_shadow_layer()
    self.create_composite_nodes()
    arrange_nodes([world.node_tree])


class RA2_INF(RA2):
  name = "Red Alert 2"
  type = "Infantry"
  full_name = "Red Alert 2"
  suffix = "RA2.INF"

  # - Render
  render_resolution_x = 320
  render_resolution_y = 240

  # - Camera
  camera_name = 'Camera.' + suffix
  camera_ortho_scale = 14.96

  # - Light
  sun01_location = [0, 0, 12.27]
  sun01_rotation = [0, 0, 0]

  sun02_energy = 2.3

class RA2_FX(RA2):
  name = "Red Alert 2"
  type = "Effects"
  full_name = "Red Alert 2"
  suffix = "RA2.FX"
  camera_name = 'Camera.' + suffix

########################
## -- Tiberian Sun -- ##
########################

class TS(BaseScene):
  name = "Tiberian Sun"
  type = ""
  full_name = "Tiberian Sun"
  suffix = "TS"
  camera_name = 'Camera.' + suffix

  world_texture_name = 'desolated_hdri.exr'
  world_texture_path = 'shared/desolated_hdri.exr'

  # - Camera
  camera_ortho_scale = 37.4

  # - Light
  sun01_location = [-0.800477, -10.1766, 12.27]
  sun01_rotation = [0.633555, 0.0726057, 6.10865]
  sun01_energy = 4
  sun01_angle = 0.00392699
  sun01_shadow_buffer_bias = 0.02
  sun01_shadow_cascade_count = 2
  sun01_shadow_cascade_fade = 1
  sun01_shadow_cascade_max_distance = 1000
  sun01_contact_shadow_distance = 1000
  sun01_contact_shadow_bias = 1
  sun01_contact_shadow_thickness = 0.9
  
  sun02_energy = 1.0

  # - Compose
  colorramp_position01 = 0.717273
  colorramp_position02 = 0.722727
  colorramp_color01 = (0, 0, 1, 0)
  colorramp_color02 = (0, 0, 0.250158, 1)

  def __init__(self):
    self.set_full_name()
    self.create_scene()
    
    self.set_cycles_settings()
    self.set_render_settings()
    self.create_collections()
    self.create_camera(self.camera_name, self.camera_location, self.camera_rotation, self.camera_type, self.camera_ortho_scale)
    self.create_light()
    world = TS_World(self.world_texture_path, self.world_texture_name, self.suffix)
    self.create_planes()
    self.create_shadow_layer()
    self.create_composite_nodes()
    arrange_nodes([world.node_tree])

class TS_INF(TS):
  name = "Tiberian Sun"
  type = "Infantry"
  full_name = "Tiberian Sun"
  suffix = "TS.INF"

  # - Render
  render_resolution_x = 320
  render_resolution_y = 240

  # - Camera
  camera_name = 'Camera.' + suffix
  camera_ortho_scale = 18.7
  
class TS_FX(TS):
  name = "Tiberian Sun"
  type = "Effects"
  full_name = "Tiberian Sun"
  suffix = "TS.FX"
  camera_name = 'Camera.' + suffix

##################
## -- ReWire -- ##
##################

class RW(BaseScene):
  name = "ReWire"
  type = ""
  full_name = "ReWire"
  suffix = "RW"
  camera_name = 'Camera.' + suffix

  # - Render settings
  render_resolution_x = 1280
  render_resolution_y = 960

  world_texture_name = 'desolated_hdri.exr'
  world_texture_path = 'shared/desolated_hdri.exr'

  # - Camera
  camera_ortho_scale = 37.4

  # - Light
  sun01_location = [-0.800477, -10.1766, 12.27]
  sun01_rotation = [0.633555, 0.0726057, 6.10865]
  sun01_energy = 6.5
  sun01_angle = 0.00392699
  sun01_shadow_buffer_bias = 0.02
  sun01_shadow_cascade_count = 2
  sun01_shadow_cascade_fade = 1
  sun01_shadow_cascade_max_distance = 1000
  sun01_contact_shadow_distance = 1000
  sun01_contact_shadow_bias = 0.5
  sun01_contact_shadow_thickness = 0.7
  
  sun02_energy = 2.1

  def __init__(self):
    self.set_full_name()
    self.create_scene()
    
    self.set_cycles_settings()
    self.set_render_settings()
    self.create_collections()
    self.create_camera(self.camera_name, self.camera_location, self.camera_rotation, self.camera_type, self.camera_ortho_scale)
    self.create_light()
    world = RW_World(self.world_texture_path, self.world_texture_name, self.suffix)
    self.create_planes()
    self.create_shadow_layer()
    self.create_composite_nodes()
    arrange_nodes([world.node_tree])

class RW_INF(RW):
  name = "ReWire"
  type = "Infantry"
  full_name = "ReWire"
  suffix = "RW.INF"
  camera_name = 'Camera.' + suffix
  
class RW_FX(RW):
  name = "ReWire"
  type = "Effects"
  full_name = "ReWire"
  suffix = "RW.FX"
  camera_name = 'Camera.' + suffix

#####################################
## -- Red Alert / Tiberian Dawn -- ##
#####################################

class RA1(BaseScene):
  name = "Red Alert / Tiberian Dawn"
  type = ""
  full_name = "Red Alert / Tiberian Dawn"
  suffix = "RA1"

  world_texture_name = 'generic_hdri.exr'
  world_texture_path = 'shared/generic_hdri.exr'

  # - Camera
  camera01_name = 'Camera.' + suffix
  camera01_type = 'PERSP'
  camera01_ortho_scale = 1.0472
  camera01_location = [0, -36.2837, 30.4457]
  camera01_rotation = [0.872665, 0, 0]
  camera02_name = 'Camera.' + suffix + '.isometric'
  camera02_type = 'ORTHO'
  camera02_ortho_scale = 53.37
  camera02_location = [0, -31.96573, 26.8228]
  camera02_rotation = [0.872665, 0, 0]

  # - Light
  sun01_location = [-4.0, 4.0, 16.0]
  sun01_rotation = [-0.10472, -0.179769, 0.00762709]
  sun01_energy = 5.5

  sun02_energy = 2.3

  def __init__(self):
    self.set_full_name()
    self.create_scene()
    
    self.set_cycles_settings()
    self.set_render_settings()
    self.create_collections()
    self.create_camera(self.camera01_name, self.camera01_location, self.camera01_rotation, self.camera01_type, self.camera01_ortho_scale)
    self.create_camera(self.camera02_name, self.camera02_location, self.camera02_rotation, self.camera02_type, self.camera02_ortho_scale)
    self.create_light()
    world = RA1_World(self.world_texture_path, self.world_texture_name, self.suffix)
    self.create_planes()
    self.create_shadow_layer()
    self.create_composite_nodes()
    arrange_nodes([world.node_tree])

class RA1_INF(RA1):
  name = "Red Alert / Tiberian Dawn"
  type = "Infantry"
  full_name = "Red Alert / Tiberian Dawn"
  suffix = "RA1.INF"
  camera01_name = 'Camera.' + suffix
  
class RA1_FX(RA1):
  name = "Red Alert / Tiberian Dawn"
  type = "Effects"
  full_name = "Red Alert / Tiberian Dawn"
  suffix = "RA1.FX"

  # - Render
  render_resolution_x = 240
  render_resolution_y = 240

  # - Camera
  camera01_name = 'Camera.' + suffix
  camera01_location = [0.0, -13.6064, 11.4174]
  camera02_ortho_scale = 53.37

###########################################################
## -- Red Alert / Tiberian Dawn Remastered Collection -- ##
###########################################################

class RM(BaseScene):
  name = "C&C Remastered"
  type = ""
  full_name = "C&C Remastered"
  suffix = "RM"

  world_texture_name = 'generic_hdri.exr'
  world_texture_path = 'shared/generic_hdri.exr'

  # - Camera
  camera01_name = 'Camera.' + suffix
  camera01_type = 'PERSP'
  camera01_ortho_scale = 1.0472
  camera01_location = [0, -36.2837, 30.4457]
  camera01_rotation = [0.872665, 0, 0]
  camera02_name = 'Camera.' + suffix + '.isometric'
  camera02_type = 'ORTHO'
  camera02_ortho_scale = 20.0138
  camera02_location = [0, -31.9657, 26.8228]
  camera02_rotation = [0.872665, 0, 0]

  # - Light
  sun01_location = [-4.0, 4.0, 16.0]
  sun01_rotation = [-0.10472, -0.179769, 0.00762709]
  sun01_energy = 5.5

  sun02_energy = 2.3

  def __init__(self):
    self.set_full_name()
    self.create_scene()
    
    self.set_cycles_settings()
    self.set_render_settings()
    self.create_collections()
    self.create_camera(self.camera01_name, self.camera01_location, self.camera01_rotation, self.camera01_type, self.camera01_ortho_scale)
    self.create_camera(self.camera02_name, self.camera02_location, self.camera02_rotation, self.camera02_type, self.camera02_ortho_scale)
    self.create_light()
    world = RM_World(self.world_texture_path, self.world_texture_name, self.suffix)
    self.create_planes()
    self.create_shadow_layer()
    self.create_composite_nodes()
    arrange_nodes([world.node_tree])

class RM_INF(RM):
  name = "C&C Remastered"
  type = "Infantry"
  full_name = "C&C Remastered"
  suffix = "RM.INF"
  camera_name = 'Camera.' + suffix
  
class RM_FX(RM):
  name = "C&C Remastered"
  type = "Effects"
  full_name = "C&C Remastered"
  suffix = "RM.FX"
  camera_name = 'Camera.' + suffix

#####################
## -- Dune 2000 -- ##
#####################

class D2K(BaseScene):
  name = "Dune 2000"
  type = ""
  full_name = "Dune 2000"
  suffix = "D2K"

  world_texture_name = 'desolated_hdri.exr'
  world_texture_path = 'shared/desolated_hdri.exr'

  # - Camera
  camera01_name = 'Camera.' + suffix
  camera01_type = 'PERSP'
  camera01_ortho_scale = 1.0472
  camera01_location = [0, -28.3854, 23.8179]
  camera01_rotation = [0.872665, 0, 0]
  camera02_name = 'Camera.' + suffix + '.isometric'
  camera02_type = 'ORTHO'
  camera02_ortho_scale = 39.4299
  camera02_location = [0, -37.8463, 31.7564]
  camera02_rotation = [0.872665, 0, 0]

  # - Light
  sun01_location = [-4.0, 4.0, 16.0]
  sun01_rotation = [-0.698132, 0, 2.35619]
  sun01_energy = 5.5
  sun01_angle = 0.00392699
  sun01_shadow_buffer_bias = 0.02
  sun01_shadow_cascade_count = 2
  sun01_shadow_cascade_fade = 1
  sun01_shadow_cascade_max_distance = 1000
  sun01_contact_shadow_distance = 1000
  sun01_contact_shadow_bias = 0.5
  sun01_contact_shadow_thickness = 0.7
  
  sun02_energy = 2.3

  def __init__(self):
    self.set_full_name()
    self.create_scene()
    
    self.set_cycles_settings()
    self.set_render_settings()
    self.create_collections()
    self.create_camera(self.camera01_name, self.camera01_location, self.camera01_rotation, self.camera01_type, self.camera01_ortho_scale)
    self.create_camera(self.camera02_name, self.camera02_location, self.camera02_rotation, self.camera02_type, self.camera02_ortho_scale)
    self.create_light()
    world = D2K_World(self.world_texture_path, self.world_texture_name, self.suffix)
    self.create_planes()
    self.create_shadow_layer()
    self.create_composite_nodes()
    arrange_nodes([world.node_tree])

class D2K_INF(D2K):
  name = "Dune 2000"
  type = "Infantry"
  full_name = "Dune 2000"
  suffix = "D2K.INF"
  camera_name = 'Camera.' + suffix
  
class D2K_FX(D2K):
  name = "Dune 2000"
  type = "Effects"
  full_name = "Dune 2000"
  suffix = "D2K.FX"
  camera_name = 'Camera.' + suffix