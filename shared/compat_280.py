from typing import Optional, Tuple

from .compat import BaseCompat


class Compat280(BaseCompat):
  """Blender 2.80-2.92 (Eevee) compatibility layer."""

  VERSION = (2, 80, 0)

  SEPARATE_COLOR_NODE = "CompositorNodeSepHSVA"
  COMBINE_COLOR_NODE = "CompositorNodeCombHSVA"
  MIX_NODE = "CompositorNodeMixRGB"
  SEPARATE_RGB_NODE = "ShaderNodeSeparateRGB"

  def has_cryptomatte(self) -> bool:
    return False

  def has_shader_to_rgb(self) -> bool:
    return False

  def init_compositor(self, scene) -> None:
    scene.use_nodes = True

  def get_compositor_tree(self, scene):
    return scene.node_tree

  def get_render_layers_node(self, scene):
    return scene.node_tree.nodes["Render Layers"]

  def get_composite_output_node(self, scene):
    return scene.node_tree.nodes["Composite"]

  def add_group_input(self, group, socket_type: str, name: str) -> None:
    group.inputs.new(socket_type, name)

  def add_group_output(self, group, socket_type: str, name: str) -> None:
    group.outputs.new(socket_type, name)

  def set_switch_value(self, node, value: bool) -> None:
    node.check = value

  def set_alpha_over_premultiply(self, node, value: bool) -> None:
    node.use_premultiply = value

  def get_invert_color_input(self) -> int:
    return 1

  def get_mix_color_inputs(self) -> Tuple[int, int]:
    return (1, 2)

  def get_mix_output(self) -> int:
    return 0

  def setup_mix_node(self, node) -> None:
    pass

  def set_material_transparency(self, material, blend: str = "BLEND", shadow: str = "NONE") -> None:
    material.blend_method = blend
    material.shadow_method = shadow

  def set_shadow_catcher(self, obj, value: bool) -> None:
    if hasattr(obj, "is_shadow_catcher"):
      obj.is_shadow_catcher = value
    elif hasattr(obj, "cycles"):
      obj.cycles.is_shadow_catcher = value

  def set_glossy_visibility(self, obj, value: bool) -> None:
    obj.cycles_visibility.glossy = value

  def hide_object_viewport(self, obj, value: bool = True) -> None:
    obj.hide_viewport = value

  def hide_object_render(self, obj, value: bool = True) -> None:
    obj.hide_render = value

  def hide_object_select(self, obj, value: bool = True) -> None:
    obj.hide_select = value

  def plane_add_kwargs(self) -> dict:
    return {"size": 140, "enter_editmode": False, "align": "WORLD"}

  def add_sun_light(self, location, rotation, energy: float, angle: float) -> None:
    import bpy
    bpy.ops.object.light_add(type="SUN", radius=1, align="WORLD", location=location, rotation=rotation)

  def set_sun_shadow_properties(self, sun_obj, scene_settings) -> None:
    d = sun_obj.data
    d.cycles.use_multiple_importance_sampling = False
    d.shadow_buffer_bias = scene_settings.get("sun01_shadow_buffer_bias", 0.02)
    d.shadow_cascade_count = scene_settings.get("sun01_shadow_cascade_count", 2)
    d.shadow_cascade_fade = scene_settings.get("sun01_shadow_cascade_fade", 1)
    d.shadow_cascade_max_distance = scene_settings.get("sun01_shadow_cascade_max_distance", 1000)
    d.shadow_cascade_exponent = scene_settings.get("sun01_shadow_cascade_exponent", 0.8)
    d.use_contact_shadow = True
    d.contact_shadow_distance = scene_settings.get("sun01_contact_shadow_distance", 1000)
    d.contact_shadow_bias = scene_settings.get("sun01_contact_shadow_bias", 0.5)
    d.contact_shadow_thickness = scene_settings.get("sun01_contact_shadow_thickness", 0.7)

  def has_shadow_sun(self) -> bool:
    return True

  def add_shadow_sun(self, location, rotation, energy: float, angle: float) -> None:
    import bpy
    bpy.ops.object.light_add(type="SUN", radius=1, align="WORLD", location=location, rotation=rotation)

  def configure_shadow_sun(self, shadow_sun, scene_settings) -> None:
    d = shadow_sun.data
    d.cycles.use_multiple_importance_sampling = False
    d.shadow_buffer_bias = scene_settings.get("sun01_shadow_buffer_bias", 0.02)
    d.shadow_cascade_count = scene_settings.get("sun02_shadow_cascade_count", 4)
    d.shadow_cascade_fade = scene_settings.get("sun02_shadow_cascade_fade", 0.0)
    d.shadow_cascade_max_distance = scene_settings.get("sun02_shadow_cascade_max_distance", 1000)
    d.shadow_cascade_exponent = scene_settings.get("sun02_shadow_cascade_exponent", 1.0)
    d.use_contact_shadow = False

  def camera_add_kwargs(self) -> dict:
    return {"enter_editmode": False, "align": "VIEW"}

  def select_scene(self, scene_name: str) -> None:
    import bpy
    bpy.context.window.scene = bpy.data.scenes[scene_name]

  def set_eevee_settings(self, scene, settings: dict) -> None:
    e = scene.eevee
    e.gtao_factor = settings.get("eevee_gtao_factor", 0.5)
    e.gtao_distance = settings.get("eevee_gtao_distance", 100)
    e.shadow_cascade_size = settings.get("eevee_shadow_cascade_size", "1024")
    e.shadow_cube_size = settings.get("eevee_shadow_cube_size", "1024")
    e.taa_render_samples = settings.get("eevee_taa_render_samples", 64)
    e.taa_samples = settings.get("eevee_taa_samples", 8)
    e.use_gtao = settings.get("eevee_use_gtao", True)
    e.use_soft_shadows = settings.get("eevee_use_soft_shadows", True)
    e.use_ssr = settings.get("eevee_use_ssr", True)

  def set_cycles_film_transparent(self, scene, value: bool) -> None:
    scene.render.film_transparent = value

  def get_view_layer_name(self) -> str:
    return "View Layer"

  def set_view_layer_denoising(self, scene, enabled: bool = True) -> None:
    vl = scene.view_layers[self.get_view_layer_name()]
    vl.cycles.use_denoising = enabled
    vl.cycles.denoising_radius = 0.5
    vl.cycles.denoising_strength = 0.5
    vl.cycles.denoising_feature_strength = 0.5
    vl.cycles.denoising_glossy_direct = False

  def get_pixel_filter_type(self) -> str:
    return "GAUSSIAN"

  def get_view_transform_default(self) -> str:
    return "Standard"

  def has_viewport_settings(self) -> bool:
    return False

  def get_sky_density_property(self) -> str:
    return "dust_density"

  def get_sky_type_value(self) -> Optional[str]:
    return None

  def compositor_switch_toggle(self, name: str, value: bool) -> str:
    return 'bpy.context.scene.node_tree.nodes["{}"].check = {}'.format(name, value)

  def alpha_toggle(self, value: bool) -> str:
    return 'bpy.context.scene.node_tree.nodes["Alpha"].check = {}'.format(value)

  def get_engine_string(self, engine_key: str) -> str:
    if engine_key == "CYCLES":
      return "CYCLES"
    return "BLENDER_EEVEE"

  def has_collections(self) -> bool:
    return True

  def create_shadow_view_layer(self, scene, full_name):
    shadow_vl = scene.view_layers.new("ShadowLayer")
    root = shadow_vl.layer_collection
    template_key = full_name + " Template"
    shadow_key = full_name + " Shadow"
    for name in list(root.children.keys()):
      if name == template_key:
        template_lc = root.children[name]
        for child_name in list(template_lc.children.keys()):
          if child_name != shadow_key:
            template_lc.children[child_name].exclude = True
      else:
        root.children[name].exclude = True
    return "ShadowLayer"
