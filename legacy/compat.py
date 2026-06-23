from typing import Optional, Tuple

from shared.compat import BaseCompat


class CompatLegacy(BaseCompat):
  """Blender 2.79 BLENDER_RENDER compatibility layer."""

  VERSION = (2, 79, 0)

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
    material.use_transparency = True
    material.transparency_method = "Z_TRANSPARENCY"

  def set_shadow_catcher(self, obj, value: bool) -> None:
    pass

  def set_glossy_visibility(self, obj, value: bool) -> None:
    pass

  def hide_object_viewport(self, obj, value: bool = True) -> None:
    obj.hide = value

  def hide_object_render(self, obj, value: bool = True) -> None:
    obj.hide_render = value

  def hide_object_select(self, obj, value: bool = True) -> None:
    obj.hide_select = value

  def plane_add_kwargs(self) -> dict:
    return {"enter_editmode": False}

  def add_sun_light(self, location, rotation, energy: float, angle: float) -> None:
    import bpy
    bpy.ops.object.lamp_add(type="SUN", location=location, rotation=rotation)

  def set_sun_shadow_properties(self, sun_obj, scene_settings) -> None:
    pass

  def has_shadow_sun(self) -> bool:
    return False

  def add_shadow_sun(self, location, rotation, energy: float, angle: float) -> None:
    pass

  def configure_shadow_sun(self, shadow_sun, scene_settings) -> None:
    pass

  def camera_add_kwargs(self) -> dict:
    return {"enter_editmode": False}

  def select_scene(self, scene_name: str) -> None:
    import bpy
    bpy.context.window.screen.scene = bpy.data.scenes[scene_name]

  def set_eevee_settings(self, scene, settings: dict) -> None:
    pass

  def set_cycles_film_transparent(self, scene, value: bool) -> None:
    pass

  def get_view_layer_name(self) -> str:
    return "RenderLayer"

  def set_view_layer_denoising(self, scene, enabled: bool = True) -> None:
    pass

  def get_pixel_filter_type(self) -> str:
    return "GAUSSIAN"

  def get_view_transform_default(self) -> str:
    return "Default"

  def has_viewport_settings(self) -> bool:
    return False

  def get_sky_density_property(self) -> str:
    return "dust_density"

  def get_sky_type_value(self) -> Optional[str]:
    return None

  def compositor_switch_toggle(self, name: str, value: bool) -> str:
    return 'bpy.context.scene.node_tree.nodes["Switch"].check = {}'.format(value)

  def alpha_toggle(self, value: bool) -> str:
    return 'bpy.context.scene.node_tree.nodes["Switch"].check = {}'.format(value)

  def get_engine_string(self, engine_key: str) -> str:
    return "BLENDER_RENDER"

  def has_collections(self) -> bool:
    return False

  def create_shadow_view_layer(self, scene, full_name):
    return None

  def has_cryptomatte(self) -> bool:
    return False

  def has_shader_to_rgb(self) -> bool:
    return False

  def get_shadow_pass_index(self) -> int:
    return 1

  def get_indexob_output_index(self) -> int:
    return 14
