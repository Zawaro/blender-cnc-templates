from __future__ import annotations

from .compat import BaseCompat


class Compat500(BaseCompat):
  """Blender 5.0+ compatibility layer."""

  VERSION = (5, 0, 0)

  SEPARATE_COLOR_NODE = "CompositorNodeSeparateColor"
  COMBINE_COLOR_NODE = "CompositorNodeCombineColor"
  MIX_NODE = "ShaderNodeMix"
  SEPARATE_RGB_NODE = "ShaderNodeSeparateColor"

  def init_compositor(self, scene) -> None:
    import bpy
    node_tree = bpy.data.node_groups.new(name="Composition", type="CompositorNodeTree")
    scene.compositing_node_group = node_tree

  def get_compositor_tree(self, scene):
    return scene.compositing_node_group

  def get_render_layers_node(self, scene):
    tree = scene.compositing_node_group
    for node in tree.nodes:
      if node.type == "RLAYERS":
        return node
    return None

  def get_composite_output_node(self, scene):
    tree = scene.compositing_node_group
    for node in tree.nodes:
      if node.type == "OUTPUT_GROUP":
        return node
    return None

  def add_group_input(self, group, socket_type: str, name: str) -> None:
    group.interface.new_socket(name=name, in_out="INPUT", socket_type=socket_type)

  def add_group_output(self, group, socket_type: str, name: str) -> None:
    group.interface.new_socket(name=name, in_out="OUTPUT", socket_type=socket_type)

  def set_switch_value(self, node, value: bool) -> None:
    node.inputs[0].default_value = value

  def set_alpha_over_premultiply(self, node, value: bool) -> None:
    node.inputs[4].default_value = value

  def get_invert_color_input(self) -> int:
    return 0

  def get_mix_color_inputs(self) -> tuple[int, int]:
    return (6, 7)

  def get_mix_output(self) -> int:
    return 2

  def setup_mix_node(self, node) -> None:
    node.data_type = "RGBA"

  def set_material_transparency(self, material, blend: str = "BLEND", shadow: str = "NONE") -> None:
    material.surface_render_method = "BLENDED"

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
    sun_obj.data.cycles.use_multiple_importance_sampling = False

  def has_shadow_sun(self) -> bool:
    return False

  def add_shadow_sun(self, location, rotation, energy: float, angle: float) -> None:
    raise NotImplementedError("Blender 5.0 does not use a shadow sun")

  def configure_shadow_sun(self, shadow_sun, scene_settings) -> None:
    raise NotImplementedError("Blender 5.0 does not use a shadow sun")

  def camera_add_kwargs(self) -> dict:
    return {"enter_editmode": False, "align": "VIEW", "scale": (1, 1, 1)}

  def select_scene(self, scene_name: str) -> None:
    import bpy
    bpy.context.window.scene = bpy.data.scenes[scene_name]

  def set_eevee_settings(self, scene, settings: dict) -> None:
    scene.eevee.use_shadows = settings.get("use_shadows", True)

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
    return "BLACKMAN_HARRIS"

  def get_view_transform_default(self) -> str:
    return "Standard"

  def has_viewport_settings(self) -> bool:
    return True

  def get_sky_density_property(self) -> str:
    return "aerosol_density"

  def get_sky_type_value(self) -> str | None:
    return "SINGLE_SCATTERING"

  def compositor_switch_toggle(self, name: str, value: bool) -> str:
    return f'bpy.context.scene.compositing_node_group.nodes["{name}"].inputs[0].default_value = {value}'

  def alpha_toggle(self, value: bool) -> str:
    return f'bpy.context.scene.compositing_node_group.nodes["Alpha"].inputs[0].default_value = {value}'

  def get_engine_string(self, engine_key: str) -> str:
    if engine_key == "CYCLES":
      return "CYCLES"
    return "BLENDER_EEVEE"

  def has_collections(self) -> bool:
    return True
