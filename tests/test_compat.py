import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.compat import BaseCompat, get_compat


EXPECTED_METHODS = [
  "init_compositor", "get_compositor_tree", "get_render_layers_node",
  "get_composite_output_node", "add_group_input", "add_group_output",
  "set_switch_value", "set_alpha_over_premultiply", "get_invert_color_input",
  "get_mix_color_inputs", "get_mix_output", "setup_mix_node",
  "set_material_transparency", "set_shadow_catcher", "set_glossy_visibility",
  "hide_object_viewport", "hide_object_render", "hide_object_select",
  "plane_add_kwargs", "add_sun_light", "set_sun_shadow_properties",
  "has_shadow_sun", "add_shadow_sun", "configure_shadow_sun",
  "camera_add_kwargs", "select_scene", "set_eevee_settings",
  "set_cycles_film_transparent", "get_view_layer_name", "set_view_layer_denoising",
  "get_pixel_filter_type", "get_view_transform_default", "has_viewport_settings",
  "get_sky_density_property", "get_sky_type_value",
  "compositor_switch_toggle", "alpha_toggle", "get_engine_string", "has_collections",
]

EXPECTED_PROPERTIES = [
  "SEPARATE_COLOR_NODE", "COMBINE_COLOR_NODE", "MIX_NODE", "SEPARATE_RGB_NODE", "VERSION",
]

COMPAT_VERSIONS = [(2, 79), (2, 80), (3, 0), (4, 2), (5, 0)]


def test_get_compat_returns_correct_type():
  for ver in COMPAT_VERSIONS:
    compat = get_compat(*ver)
    assert isinstance(compat, BaseCompat)


def test_all_compat_implement_interface():
  for ver in COMPAT_VERSIONS:
    compat = get_compat(*ver)
    for method in EXPECTED_METHODS:
      assert hasattr(compat, method), f"compat_{ver[0]}{ver[1]:03d} missing method: {method}"
      assert callable(getattr(compat, method)), f"compat_{ver[0]}{ver[1]:03d}.{method} is not callable"
    for prop in EXPECTED_PROPERTIES:
      assert hasattr(compat, prop), f"compat_{ver[0]}{ver[1]:03d} missing property: {prop}"


def test_version_tuples_are_set():
  for ver in COMPAT_VERSIONS:
    compat = get_compat(*ver)
    assert compat.VERSION[:2] == ver


def test_node_type_names_are_strings():
  for ver in COMPAT_VERSIONS:
    compat = get_compat(*ver)
    assert isinstance(compat.SEPARATE_COLOR_NODE, str)
    assert isinstance(compat.COMBINE_COLOR_NODE, str)
    assert isinstance(compat.MIX_NODE, str)
    assert isinstance(compat.SEPARATE_RGB_NODE, str)
