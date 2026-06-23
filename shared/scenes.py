import bpy
from typing import Dict

from . import constants
from .node_arrange import arrange_nodes
from .compat import BaseCompat

# World material classes are registered by each version's main.py
# before instantiating scenes.  Lookup: suffix -> world_class.
_WORLD_REGISTRY = {}


def register_world(suffix: str, world_cls: type) -> None:
  _WORLD_REGISTRY[suffix] = world_cls


def _get_world(suffix: str, world_cls_args: tuple, compat) -> object:
  cls = _WORLD_REGISTRY.get(suffix)
  if cls is None:
    raise RuntimeError("No world class registered for suffix '{}'".format(suffix))
  return cls(*world_cls_args, compat)


def _create_plane(compat, name, location, material, hide_render=True, hide_viewport=True):
  bpy.ops.mesh.primitive_plane_add(**compat.plane_add_kwargs(), location=location)
  obj = bpy.context.active_object
  obj.name = name
  compat.hide_object_render(obj, hide_render)
  compat.hide_object_viewport(obj, hide_viewport)
  compat.set_glossy_visibility(obj, False)
  obj.data.materials.append(material)
  return obj


class BaseScene:
  name = "Scene"
  type = ""
  full_name = "Scene"
  suffix = "SC"

  cycles_device = "GPU"
  cycles_filter_width = constants.CYCLES_FILTER_WIDTH
  cycles_max_bounces = 4
  cycles_pixel_filter_type = "BLACKMAN_HARRIS"
  cycles_preview_samples = 10
  cycles_samples = 64
  cycles_adaptive_min_samples = 32
  cycles_sample_clamp_indirect = 0.05
  cycles_transmission_bounces = 8
  cycles_volume_bounces = 1
  cycles_use_denoising = True
  cycles_denoising_use_gpu = True
  cycles_film_transparent = True

  eevee_gtao_factor = 0.5
  eevee_gtao_distance = 100
  eevee_shadow_cascade_size = "1024"
  eevee_shadow_cube_size = "1024"
  eevee_taa_render_samples = 64
  eevee_taa_samples = 8
  eevee_use_gtao = True
  eevee_use_soft_shadows = True
  eevee_use_ssr = True
  eevee_shadow_pool_size = "32"
  eevee_use_shadows = True

  frame_start = 0
  render_fps = 10
  render_dither_intensity = 0
  render_film_transparent = True
  render_filter_size = constants.EEVEE_FILTER_SIZE
  render_image_settings_compression = 90
  render_image_settings_color_mode = "RGB"
  render_resolution_x = 640
  render_resolution_y = 480
  render_use_single_layer = True
  unit_settings_system = "NONE"
  view_settings_view_transform = "Standard"
  view_settings_look = "None"
  view_settings_exposure = 0

  camera_location = [110.039, -110.039, 89.84670]
  camera_rotation = [1.0472, 0, 0.785398]
  camera_name = "Camera." + suffix
  camera_type = "ORTHO"
  camera_ortho_scale = 29.92
  camera_clip_end = 2000.0

  sun01_location = [-4.14, -10, 12.27]
  sun01_rotation = [0.633555, 0.0726057, 5.79449]
  sun01_energy = 7.5
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

  colorramp_position01 = 0.717273
  colorramp_position02 = 0.722727
  colorramp_color01 = (0, 0, 1, 0)
  colorramp_color02 = (0, 0, 0.250158, 1)

  world_texture_path = "shared/generic_hdri.exr"
  world_texture_name = "generic_hdri.exr"
  world_class_suffix = None

  def __init__(self, compat: BaseCompat):
    self.compat = compat
    self.set_full_name()
    self.create_scene()
    self.compat.select_scene(self.full_name)

    self.set_cycles_settings()
    self.set_eevee_settings()
    self.set_render_settings()
    if self.compat.has_viewport_settings():
      self.set_viewport_settings()
    if self.compat.has_collections():
      self.create_collections()
    self.create_camera(
      self.camera_name,
      self.camera_location,
      self.camera_rotation,
      self.camera_type,
      self.camera_ortho_scale,
    )
    self.create_light()
    self._create_world()
    self.create_planes()
    self.create_composite_nodes()

  def _create_world(self):
    world_suffix = self.world_class_suffix or self.suffix
    props = {"world_texture_path": self.world_texture_path, "world_texture_name": self.world_texture_name}
    world = _get_world(world_suffix, (self.suffix, props), self.compat)
    arrange_nodes([world.node_tree])

  def set_full_name(self):
    if self.type:
      self.full_name = "{} - {}".format(self.name, self.type)

  def create_scene(self):
    bpy.ops.scene.new(type="NEW")
    bpy.context.scene.name = self.full_name

  def cleanup(self):
    self.compat.select_scene(self.full_name)
    bpy.ops.scene.delete()

  def set_cycles_settings(self):
    c = bpy.context.scene.cycles
    c.device = self.cycles_device
    c.filter_width = self.cycles_filter_width
    c.max_bounces = self.cycles_max_bounces
    c.pixel_filter_type = self.compat.get_pixel_filter_type()
    c.preview_samples = self.cycles_preview_samples
    c.samples = self.cycles_samples
    c.adaptive_min_samples = self.cycles_adaptive_min_samples
    c.sample_clamp_indirect = self.cycles_sample_clamp_indirect
    c.transmission_bounces = self.cycles_transmission_bounces
    c.use_denoising = self.cycles_use_denoising
    c.volume_bounces = self.cycles_volume_bounces
    try:
      c.denoising_use_gpu = self.cycles_denoising_use_gpu
    except AttributeError:
      pass

  def set_eevee_settings(self):
    self.compat.set_eevee_settings(bpy.context.scene, {
      "eevee_gtao_factor": self.eevee_gtao_factor,
      "eevee_gtao_distance": self.eevee_gtao_distance,
      "eevee_shadow_cascade_size": self.eevee_shadow_cascade_size,
      "eevee_shadow_cube_size": self.eevee_shadow_cube_size,
      "eevee_taa_render_samples": self.eevee_taa_render_samples,
      "eevee_taa_samples": self.eevee_taa_samples,
      "eevee_use_gtao": self.eevee_use_gtao,
      "eevee_use_soft_shadows": self.eevee_use_soft_shadows,
      "eevee_use_ssr": self.eevee_use_ssr,
      "eevee_shadow_pool_size": self.eevee_shadow_pool_size,
      "eevee_use_shadows": self.eevee_use_shadows,
    })

  def set_render_settings(self):
    scene = bpy.context.scene
    scene.name = self.full_name
    scene.frame_start = self.frame_start
    scene.render.fps = self.render_fps
    scene.render.dither_intensity = self.render_dither_intensity
    self.compat.set_cycles_film_transparent(scene, self.render_film_transparent)
    scene.render.filter_size = self.render_filter_size
    scene.render.image_settings.compression = self.render_image_settings_compression
    scene.render.image_settings.color_mode = self.render_image_settings_color_mode
    scene.render.resolution_x = self.render_resolution_x
    scene.render.resolution_y = self.render_resolution_y
    scene.render.use_single_layer = self.render_use_single_layer
    self.compat.set_view_layer_denoising(scene)
    scene.unit_settings.system = self.unit_settings_system
    scene.view_settings.view_transform = self.compat.get_view_transform_default()
    scene.view_settings.look = self.view_settings_look
    scene.view_settings.exposure = self.view_settings_exposure

  def set_viewport_settings(self):
    for workspace in bpy.data.workspaces:
      for screen in workspace.screens:
        for area in screen.areas:
          if area.type == "VIEW_3D":
            for space in area.spaces:
              if space.type == "VIEW_3D":
                space.shading.use_scene_lights = True
                space.shading.use_scene_world = True

  def create_collections(self):
    scene = bpy.data.scenes[self.full_name]
    collection = bpy.data.collections.new(self.full_name)
    bpy.context.scene.collection.children.link(collection)

    template_collection = bpy.data.collections.new(self.full_name + " Template")
    bpy.context.scene.collection.children.link(template_collection)

    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[self.full_name + " Template"]
    shadow_collection = bpy.data.collections.new(self.full_name + " Shadow")
    template_collection.children.link(shadow_collection)
    holdout_collection = bpy.data.collections.new(self.full_name + " Holdout")
    template_collection.children.link(holdout_collection)

    default_vl_name = self.compat.get_view_layer_name()
    default_vl = scene.view_layers[default_vl_name]
    default_root = default_vl.layer_collection
    default_root.children[self.full_name + " Template"].children[self.full_name + " Shadow"].exclude = True

    self.compat.create_shadow_view_layer(scene, self.full_name)

  def create_camera(self, name=None, location=None, rotation=None, camera_type=None, ortho_scale=None, clip_end=None):
    name = name or self.camera_name
    location = location or self.camera_location
    rotation = rotation or self.camera_rotation
    camera_type = camera_type or self.camera_type
    ortho_scale = ortho_scale or self.camera_ortho_scale
    clip_end = clip_end or self.camera_clip_end

    bpy.ops.object.camera_add(**self.compat.camera_add_kwargs(), location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    self.compat.hide_object_viewport(obj)
    obj.data.name = name
    obj.data.type = camera_type
    if camera_type == "PERSP":
      obj.data.lens_unit = "FOV"
      obj.data.angle = 1.0472
    else:
      obj.data.ortho_scale = ortho_scale
      if clip_end:
        bpy.context.object.data.clip_end = clip_end
    bpy.context.scene.camera = bpy.data.objects[name]
    for area in bpy.context.screen.areas:
      if area.type == "VIEW_3D":
        area.spaces[0].region_3d.view_perspective = "CAMERA"
        break

  def create_light(self):
    self.compat.add_sun_light(self.sun01_location, self.sun01_rotation, self.sun01_energy, self.sun01_angle)
    sun = bpy.context.active_object
    sun.name = "Sun." + self.suffix
    sun.data.name = "Sun." + self.suffix
    sun.data.energy = self.sun01_energy
    if hasattr(sun.data, "angle"):
      sun.data.angle = self.sun01_angle
    elif hasattr(sun.data, "shadow_soft_size"):
      sun.data.shadow_soft_size = self.sun01_angle
    self.compat.set_sun_shadow_properties(sun, {
      "sun01_shadow_buffer_bias": self.sun01_shadow_buffer_bias,
      "sun01_shadow_cascade_count": self.sun01_shadow_cascade_count,
      "sun01_shadow_cascade_fade": self.sun01_shadow_cascade_fade,
      "sun01_shadow_cascade_max_distance": self.sun01_shadow_cascade_max_distance,
      "sun01_shadow_cascade_exponent": self.sun01_shadow_cascade_exponent,
      "sun01_contact_shadow_distance": self.sun01_contact_shadow_distance,
      "sun01_contact_shadow_bias": self.sun01_contact_shadow_bias,
      "sun01_contact_shadow_thickness": self.sun01_contact_shadow_thickness,
      "sun01_angle": self.sun01_angle,
      "sun02_energy": self.sun02_energy,
    })
    self.compat.hide_object_select(sun)
    self.compat.hide_object_render(sun)

    if self.compat.has_shadow_sun():
      self.compat.add_shadow_sun(self.sun01_location, self.sun01_rotation, self.sun01_energy, self.sun01_angle)
      shadow_sun = bpy.context.active_object
      shadow_sun.name = "Sun.shadow." + self.suffix
      shadow_sun.data.name = "Sun.shadow." + self.suffix
      shadow_sun.data.energy = self.sun02_energy
      self.compat.configure_shadow_sun(shadow_sun, {
        "sun01_shadow_buffer_bias": self.sun01_shadow_buffer_bias,
        "sun01_angle": self.sun01_angle,
        "sun02_shadow_cascade_count": self.sun02_shadow_cascade_count,
        "sun02_shadow_cascade_fade": self.sun02_shadow_cascade_fade,
        "sun02_shadow_cascade_max_distance": self.sun02_shadow_cascade_max_distance,
        "sun02_shadow_cascade_exponent": self.sun02_shadow_cascade_exponent,
        "sun02_energy": self.sun02_energy,
      })
      self.compat.hide_object_select(shadow_sun)
      self.compat.hide_object_render(shadow_sun)
      self.compat.hide_object_viewport(shadow_sun)

  def create_planes(self):
    from .plane_materials import Plane_Ambient, Plane_Blue, Plane_Grey, Plane_Holdout, Plane_Shadow

    ambient_mat = Plane_Ambient(self.suffix)
    _create_plane(self.compat, "Plane.ambient." + self.suffix, (0, 0, -20), ambient_mat)

    blue_mat = Plane_Blue(self.suffix)
    _create_plane(self.compat, "Plane.blue." + self.suffix, (0, 0, -0.01), blue_mat)

    grey_mat = Plane_Grey(self.suffix)
    _create_plane(self.compat, "Plane.grey." + self.suffix, (0, 0, -0.01), grey_mat, hide_render=False)

    holdout_mat = Plane_Holdout(self.suffix)
    holdout2_obj = _create_plane(self.compat, "Plane.holdout2." + self.suffix, (0, 0, -0.01), holdout_mat)
    self.compat.set_material_transparency(holdout2_obj.active_material)

    shadow_mat = Plane_Shadow(self.suffix)
    shadow2_obj = _create_plane(self.compat, "Plane.shadow2." + self.suffix, (0, 0, -0.01), shadow_mat)
    self.compat.set_shadow_catcher(shadow2_obj, True)
    self.compat.set_material_transparency(shadow2_obj.active_material)
    shadow2_obj.pass_index = self.compat.get_shadow_pass_index()

    if self.compat.has_collections():
      bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Shadow"]

    shadow_obj = _create_plane(self.compat, "Plane.shadow." + self.suffix, (0, 0, -0.01), shadow_mat)
    self.compat.set_shadow_catcher(shadow_obj, True)
    self.compat.set_material_transparency(shadow_obj.active_material)
    shadow_obj.pass_index = self.compat.get_shadow_pass_index()

    if self.compat.has_collections():
      bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Holdout"]

    holdout_obj = _create_plane(self.compat, "Plane.holdout." + self.suffix, (0, 0, -0.015), holdout_mat)
    self.compat.set_material_transparency(holdout_obj.active_material)

    if self.compat.has_collections():
      bpy.context.view_layer.layer_collection.children[self.full_name + " Template"].children[self.full_name + " Holdout"].exclude = True

    arrange_nodes([ambient_mat.node_tree, blue_mat.node_tree, grey_mat.node_tree, holdout_mat.node_tree, shadow_mat.node_tree])

  def create_composite_nodes(self):
    scene = bpy.data.scenes[self.full_name]
    scene.render.engine = "CYCLES"

    self.compat.init_compositor(scene)
    tree = self.compat.get_compositor_tree(scene)
    nodes = tree.nodes
    links = tree.links

    rl_node = self.compat.get_render_layers_node(scene)
    if rl_node is None:
      rl_node = nodes.new("CompositorNodeRLayers")
      rl_node.name = "Render Layers"

    out_node = self.compat.get_composite_output_node(scene)
    if out_node is None:
      out_node = nodes.new("NodeGroupOutput")
      out_node.name = "Group Output"
      self.compat.add_group_output(tree, "NodeSocketColor", "Image")

    switch_names = ["Object", "Buildup.Cycles", "Buildup.Eevee", "Shadow.Cycles", "Shadow.Eevee", "Preview.Cycles", "Preview.Eevee", "Alpha"]
    switches = {}
    for sn in switch_names:
      sw = nodes.new("CompositorNodeSwitch")
      sw.name = sn
      sw.label = sn
      switches[sn] = sw

    alpha_group = bpy.data.node_groups.new(type="CompositorNodeTree", name="Alpha Convert")
    self.compat.add_group_input(alpha_group, "NodeSocketColor", "Image")
    self.compat.add_group_output(alpha_group, "NodeSocketColor", "Image")
    self.compat.add_group_output(alpha_group, "NodeSocketFloat", "Alpha")

    ag_input = alpha_group.nodes.new("NodeGroupInput")
    ag_input.location = (-400, 0)
    ag_output = alpha_group.nodes.new("NodeGroupOutput")
    ag_output.location = (400, 0)

    sep_col_type = self.compat.SEPARATE_COLOR_NODE
    comb_col_type = self.compat.COMBINE_COLOR_NODE

    ag_sep = alpha_group.nodes.new(sep_col_type)
    if hasattr(ag_sep, "mode"):
      ag_sep.mode = "HSV"
    ag_sep.location = (-200, 200)

    ag_comb = alpha_group.nodes.new(comb_col_type)
    if hasattr(ag_comb, "mode"):
      ag_comb.mode = "HSV"
    ag_comb.location = (200, 200)

    ag_math = alpha_group.nodes.new(self.compat.COMPOSITOR_MATH_NODE)
    ag_math.location = (0, 0)
    ag_math.operation = "GREATER_THAN"
    ag_math.inputs[1].default_value = 0.325

    alpha_group.links.new(ag_input.outputs[0], ag_sep.inputs[0])
    alpha_group.links.new(ag_sep.outputs[0], ag_comb.inputs[0])
    alpha_group.links.new(ag_sep.outputs[1], ag_comb.inputs[1])
    alpha_group.links.new(ag_sep.outputs[2], ag_comb.inputs[2])
    alpha_group.links.new(ag_sep.outputs[3], ag_math.inputs[0])
    alpha_group.links.new(ag_math.outputs[0], ag_comb.inputs[3])
    alpha_group.links.new(ag_math.outputs[0], ag_output.inputs[1])
    alpha_group.links.new(ag_comb.outputs[0], ag_output.inputs[0])

    alpha_convert = nodes.new("CompositorNodeGroup")
    alpha_convert.node_tree = alpha_group

    if self.compat.has_collections():
      shadow_rl_node = nodes.new("CompositorNodeRLayers")
      shadow_rl_node.name = "ShadowLayer"
      shadow_rl_node.layer = "ShadowLayer"
    else:
      idmask = nodes.new("CompositorNodeIDMask")
      idmask.index = self.compat.get_shadow_pass_index()
      idmask.use_antialiasing = True

    sep_hsva = nodes.new(sep_col_type)
    if hasattr(sep_hsva, "mode"):
      sep_hsva.mode = "HSV"

    invert = nodes.new("CompositorNodeInvert")

    mix_type = self.compat.MIX_NODE

    multiply = nodes.new(mix_type)
    self.compat.setup_mix_node(multiply)
    multiply.blend_type = "MULTIPLY"
    multiply.inputs[0].default_value = 1

    colorramp = nodes.new(self.compat.COMPOSITOR_VALUATORGB_NODE)
    colorramp.color_ramp.elements[0].position = self.colorramp_position01
    colorramp.color_ramp.elements[0].color = self.colorramp_color01
    colorramp.color_ramp.elements[1].position = self.colorramp_position02
    colorramp.color_ramp.elements[1].color = self.colorramp_color02

    rgb01 = nodes.new("CompositorNodeRGB")
    rgb01.outputs[0].default_value = (0, 0, 1, 1)
    rgb01.name = "BackgroundRGB"
    rgb01.label = "BackgroundRGB"

    rgb02 = nodes.new("CompositorNodeRGB")
    rgb02.outputs[0].default_value = (0, 0, 0, 0)
    rgb02.name = "BackgroundAlpha"
    rgb02.label = "BackgroundAlpha"

    ao01 = nodes.new("CompositorNodeAlphaOver")
    ao02 = nodes.new("CompositorNodeAlphaOver")
    self.compat.set_alpha_over_premultiply(ao01, True)
    self.compat.set_alpha_over_premultiply(ao02, True)

    invert_input = self.compat.get_invert_color_input()
    mix_a, mix_b = self.compat.get_mix_color_inputs()
    mix_out = self.compat.get_mix_output()

    links.new(switches["Preview.Eevee"].outputs[0], out_node.inputs[0])
    links.new(switches["Preview.Cycles"].outputs[0], switches["Preview.Eevee"].inputs[0])
    links.new(switches["Shadow.Eevee"].outputs[0], switches["Preview.Cycles"].inputs[0])
    links.new(switches["Shadow.Cycles"].outputs[0], switches["Shadow.Eevee"].inputs[0])
    links.new(switches["Buildup.Eevee"].outputs[0], switches["Shadow.Cycles"].inputs[0])
    links.new(switches["Buildup.Cycles"].outputs[0], switches["Buildup.Eevee"].inputs[0])
    links.new(switches["Object"].outputs[0], switches["Buildup.Cycles"].inputs[0])

    links.new(rl_node.outputs[0], switches["Object"].inputs[0])
    links.new(rl_node.outputs[0], alpha_convert.inputs[0])
    links.new(alpha_convert.outputs[0], ao01.inputs[2])

    if self.compat.has_collections():
      links.new(shadow_rl_node.outputs[1], sep_hsva.inputs[0])
    else:
      links.new(rl_node.outputs[self.compat.get_indexob_output_index()], idmask.inputs[0])
      links.new(idmask.outputs[0], sep_hsva.inputs[0])
    links.new(sep_hsva.outputs[1], invert.inputs[invert_input])
    links.new(invert.outputs[0], multiply.inputs[mix_b])
    links.new(alpha_convert.outputs[1], multiply.inputs[mix_a])
    links.new(multiply.outputs[mix_out], colorramp.inputs[0])
    links.new(colorramp.outputs[0], ao02.inputs[1])

    links.new(rgb01.outputs[0], switches["Alpha"].inputs[0])
    links.new(rgb02.outputs[0], switches["Alpha"].inputs[1])
    links.new(switches["Alpha"].outputs[0], ao01.inputs[2])
    links.new(switches["Alpha"].outputs[0], ao02.inputs[2])

    links.new(ao01.outputs[0], switches["Object"].inputs[1])
    links.new(ao01.outputs[0], switches["Buildup.Cycles"].inputs[1])
    links.new(ao01.outputs[0], switches["Buildup.Eevee"].inputs[1])
    links.new(ao02.outputs[0], switches["Shadow.Cycles"].inputs[1])
    links.new(ao02.outputs[0], switches["Shadow.Eevee"].inputs[1])
    links.new(ao01.outputs[0], switches["Preview.Cycles"].inputs[1])
    links.new(ao01.outputs[0], switches["Preview.Eevee"].inputs[1])

    arrange_nodes([tree])


# ── Game scene classes ──────────────────────────────────────────────────────


class RA2(BaseScene):
  name = "Red Alert 2"
  type = ""
  full_name = "Red Alert 2"
  suffix = "RA2"
  camera_name = "Camera." + suffix
  world_class_suffix = "RA2"


class RA2_INF(BaseScene):
  name = "Red Alert 2"
  type = "Infantry"
  full_name = "Red Alert 2"
  suffix = "RA2.INF"
  render_resolution_x = 320
  render_resolution_y = 240
  camera_name = "Camera." + suffix
  camera_ortho_scale = 14.96
  sun01_location = [0, 0, 12.27]
  sun01_rotation = [0, 0, 0]
  world_class_suffix = "RA2_INF"


class RA2_FX(RA2):
  name = "Red Alert 2"
  type = "Effects"
  full_name = "Red Alert 2"
  suffix = "RA2.FX"
  camera_name = "Camera." + suffix


class TS(BaseScene):
  name = "Tiberian Sun"
  type = ""
  full_name = "Tiberian Sun"
  suffix = "TS"
  camera_name = "Camera." + suffix
  camera_ortho_scale = 37.4
  sun01_location = [-0.800477, -10.1766, 12.27]
  sun01_rotation = [0.633555, 0.0726057, 6.10865]
  sun01_energy = 5
  sun01_contact_shadow_bias = 1
  sun01_contact_shadow_thickness = 0.9
  world_class_suffix = "TS"


class TS_INF(TS):
  name = "Tiberian Sun"
  type = "Infantry"
  full_name = "Tiberian Sun"
  suffix = "TS.INF"
  render_resolution_x = 320
  render_resolution_y = 240
  camera_name = "Camera." + suffix
  camera_ortho_scale = 18.7


class TS_FX(TS):
  name = "Tiberian Sun"
  type = "Effects"
  full_name = "Tiberian Sun"
  suffix = "TS.FX"
  camera_name = "Camera." + suffix


class RW(BaseScene):
  name = "ReWire"
  type = ""
  full_name = "ReWire"
  suffix = "RW"
  camera_name = "Camera." + suffix
  render_resolution_x = 1280
  render_resolution_y = 960
  camera_ortho_scale = 37.4
  sun01_location = [-0.800477, -10.1766, 12.27]
  sun01_rotation = [0.633555, 0.0726057, 6.10865]
  sun01_energy = 7.5
  world_class_suffix = "RW"


class RW_INF(RW):
  name = "ReWire"
  type = "Infantry"
  full_name = "ReWire"
  suffix = "RW.INF"
  camera_name = "Camera." + suffix


class RW_FX(RW):
  name = "ReWire"
  type = "Effects"
  full_name = "ReWire"
  suffix = "RW.FX"
  camera_name = "Camera." + suffix


class RA1(BaseScene):
  name = "Red Alert / Tiberian Dawn"
  type = ""
  full_name = "Red Alert / Tiberian Dawn"
  suffix = "RA1"
  camera01_name = "Camera." + suffix
  camera01_type = "PERSP"
  camera01_ortho_scale = 1.0472
  camera01_location = [0, -36.2837, 30.4457]
  camera01_rotation = [0.872665, 0, 0]
  camera02_name = "Camera." + suffix + ".isometric"
  camera02_type = "ORTHO"
  camera02_ortho_scale = 53.37
  camera02_location = [0, -31.96573, 26.8228]
  camera02_rotation = [0.872665, 0, 0]
  sun01_location = [-4.0, 4.0, 16.0]
  sun01_rotation = [-0.10472, -0.179769, 0.00762709]
  sun01_energy = 6.5
  world_class_suffix = "RA1"

  def __init__(self, compat):
    super().__init__(compat)
    self.create_camera(
      self.camera02_name, self.camera02_location, self.camera02_rotation,
      self.camera02_type, self.camera02_ortho_scale,
    )


class RA1_INF(RA1):
  name = "Red Alert / Tiberian Dawn"
  type = "Infantry"
  full_name = "Red Alert / Tiberian Dawn"
  suffix = "RA1.INF"
  camera01_name = "Camera." + suffix


class RA1_FX(RA1):
  name = "Red Alert / Tiberian Dawn"
  type = "Effects"
  full_name = "Red Alert / Tiberian Dawn"
  suffix = "RA1.FX"
  render_resolution_x = 240
  render_resolution_y = 240
  camera01_name = "Camera." + suffix
  camera01_location = [0.0, -13.6064, 11.4174]
  camera02_ortho_scale = 53.37


class RM(BaseScene):
  name = "C&C Remastered"
  type = ""
  full_name = "C&C Remastered"
  suffix = "RM"
  camera01_name = "Camera." + suffix
  camera01_type = "PERSP"
  camera01_ortho_scale = 1.0472
  camera01_location = [0, -36.2837, 30.4457]
  camera01_rotation = [0.872665, 0, 0]
  camera02_name = "Camera." + suffix + ".isometric"
  camera02_type = "ORTHO"
  camera02_ortho_scale = 20.0138
  camera02_location = [0, -31.9657, 26.8228]
  camera02_rotation = [0.872665, 0, 0]
  sun01_location = [-4.0, 4.0, 16.0]
  sun01_rotation = [-0.10472, -0.179769, 0.00762709]
  sun01_energy = 6.5
  world_class_suffix = "RM"

  def __init__(self, compat):
    super().__init__(compat)
    self.create_camera(
      self.camera02_name, self.camera02_location, self.camera02_rotation,
      self.camera02_type, self.camera02_ortho_scale,
    )


class RM_INF(RM):
  name = "C&C Remastered"
  type = "Infantry"
  full_name = "C&C Remastered"
  suffix = "RM.INF"
  camera_name = "Camera." + suffix


class RM_FX(RM):
  name = "C&C Remastered"
  type = "Effects"
  full_name = "C&C Remastered"
  suffix = "RM.FX"
  camera_name = "Camera." + suffix


class D2K(BaseScene):
  name = "Dune 2000"
  type = ""
  full_name = "Dune 2000"
  suffix = "D2K"
  camera01_name = "Camera." + suffix
  camera01_type = "PERSP"
  camera01_ortho_scale = 1.0472
  camera01_location = [0, -28.3854, 23.8179]
  camera01_rotation = [0.872665, 0, 0]
  camera02_name = "Camera." + suffix + ".isometric"
  camera02_type = "ORTHO"
  camera02_ortho_scale = 39.4299
  camera02_location = [0, -37.8463, 31.7564]
  camera02_rotation = [0.872665, 0, 0]
  sun01_location = [-4.0, 4.0, 16.0]
  sun01_rotation = [-0.698132, 0, 2.35619]
  sun01_energy = 6.5
  world_class_suffix = "D2K"

  def __init__(self, compat):
    super().__init__(compat)
    self.create_camera(
      self.camera02_name, self.camera02_location, self.camera02_rotation,
      self.camera02_type, self.camera02_ortho_scale,
    )


class D2K_INF(D2K):
  name = "Dune 2000"
  type = "Infantry"
  full_name = "Dune 2000"
  suffix = "D2K.INF"
  camera_name = "Camera." + suffix


class D2K_FX(D2K):
  name = "Dune 2000"
  type = "Effects"
  full_name = "Dune 2000"
  suffix = "D2K.FX"
  camera_name = "Camera." + suffix


ALL_SCENE_CLASSES = [
  RA2, RA2_INF, RA2_FX,
  TS, TS_INF, TS_FX,
  RW, RW_INF, RW_FX,
  RA1, RA1_INF, RA1_FX,
  RM, RM_INF, RM_FX,
  D2K, D2K_INF, D2K_FX,
]
