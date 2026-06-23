from typing import Optional, Tuple

from .compat import BaseCompat


class Compat300(BaseCompat):
  """Blender 3.0+ (CyclesX) compatibility layer."""

  VERSION = (3, 0, 0)

  SEPARATE_COLOR_NODE = "CompositorNodeSepHSVA"
  COMBINE_COLOR_NODE = "CompositorNodeCombHSVA"
  MIX_NODE = "CompositorNodeMixRGB"
  SEPARATE_RGB_NODE = "ShaderNodeSeparateRGB"

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
    obj.is_shadow_catcher = value

  def set_glossy_visibility(self, obj, value: bool) -> None:
    obj.visible_glossy = value

  def hide_object_viewport(self, obj, value: bool = True) -> None:
    obj.hide_viewport = value

  def hide_object_render(self, obj, value: bool = True) -> None:
    obj.hide_render = value

  def hide_object_select(self, obj, value: bool = True) -> None:
    obj.hide_select = value

  def plane_add_kwargs(self) -> dict:
    return {"size": 140, "enter_editmode": False, "align": "WORLD", "scale": (1, 1, 1)}

  def add_sun_light(self, location, rotation, energy: float, angle: float) -> None:
    import bpy
    bpy.ops.object.light_add(type="SUN", radius=1, align="WORLD", location=location, rotation=rotation, scale=(1, 1, 1))

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
    return False

  def add_shadow_sun(self, location, rotation, energy: float, angle: float) -> None:
    raise NotImplementedError("CyclesX does not use a shadow sun")

  def configure_shadow_sun(self, shadow_sun, scene_settings) -> None:
    raise NotImplementedError("CyclesX does not use a shadow sun")

  def camera_add_kwargs(self) -> dict:
    return {"enter_editmode": False, "align": "VIEW", "scale": (1, 1, 1)}

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
    return "ViewLayer"

  def set_view_layer_denoising(self, scene, enabled: bool = True) -> None:
    vl = scene.view_layers["ViewLayer"]
    vl.cycles.denoising_store_passes = enabled
    vl.use_pass_cryptomatte_asset = True
    vl.pass_cryptomatte_depth = 2

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
