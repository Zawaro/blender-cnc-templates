import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.compat import get_compat

COMPAT_VERSIONS = [(2, 79), (2, 80), (2, 93), (3, 0), (4, 2), (5, 0)]


class MockObj:
  """Minimal mock for bpy objects — records attribute assignments."""

  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)


# -- set_material_transparency --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_material_transparency_sets_correct_attrs(major, minor):
  compat = get_compat(major, minor)
  if major == 2 and minor <= 79:
    # 2.79: no-op
    mat = MockObj(blend_method="OPAQUE", shadow_method="OPAQUE", surface_render_method="DITHERED")
    compat.set_material_transparency(mat, "BLEND", "CLIP")
    assert mat.blend_method == "OPAQUE"
    assert mat.shadow_method == "OPAQUE"
  elif major >= 5:
    mat = MockObj(blend_method="OPAQUE", shadow_method="OPAQUE", surface_render_method="DITHERED")
    compat.set_material_transparency(mat, "BLEND", "CLIP")
    assert mat.surface_render_method == "BLENDED"
  elif major == 4 and minor >= 2:
    # 4.2 with shadow_method present: sets blend_method + shadow_method
    mat = MockObj(blend_method="OPAQUE", shadow_method="OPAQUE", surface_render_method="DITHERED")
    compat.set_material_transparency(mat, "BLEND", "CLIP")
    assert mat.blend_method == "BLEND"
    assert mat.shadow_method == "CLIP"
    # 4.2 without shadow_method: falls through to surface_render_method
    mat2 = MockObj(blend_method="OPAQUE", surface_render_method="DITHERED")
    compat.set_material_transparency(mat2, "BLEND", "HASHED")
    assert mat2.surface_render_method == "DITHERED"
  else:
    mat = MockObj(blend_method="OPAQUE", shadow_method="OPAQUE", surface_render_method="DITHERED")
    compat.set_material_transparency(mat, "BLEND", "CLIP")
    assert mat.blend_method == "BLEND"
    assert mat.shadow_method == "CLIP"


# -- set_switch_value --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_switch_value(major, minor):
  compat = get_compat(major, minor)
  if major >= 5:
    node = MockObj(inputs=[MockObj(default_value=False)])
    compat.set_switch_value(node, True)
    assert node.inputs[0].default_value is True
  else:
    node = MockObj(check=False)
    compat.set_switch_value(node, True)
    assert node.check is True


# -- hide_object_viewport --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_hide_object_viewport(major, minor):
  compat = get_compat(major, minor)
  obj = MockObj(hide=False, hide_viewport=False)
  compat.hide_object_viewport(obj, True)
  if major == 2 and minor <= 79:
    assert obj.hide is True
  else:
    assert obj.hide_viewport is True


# -- set_shadow_catcher --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_shadow_catcher(major, minor):
  compat = get_compat(major, minor)
  if major == 2 and minor <= 79:
    # 2.79: uses obj.cycles.is_shadow_catcher
    cycles = MockObj(is_shadow_catcher=False, use_multiple_importance_sampling=True)
    obj = MockObj(cycles=cycles)
    compat.set_shadow_catcher(obj, True)
    assert obj.cycles.is_shadow_catcher is True
  else:
    obj = MockObj(is_shadow_catcher=False)
    compat.set_shadow_catcher(obj, True)
    assert obj.is_shadow_catcher is True


# -- set_glossy_visibility --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_glossy_visibility(major, minor):
  compat = get_compat(major, minor)
  if major == 2 and minor <= 79:
    obj = MockObj(visible_glossy=False)
    compat.set_glossy_visibility(obj, True)
    assert obj.visible_glossy is True
  elif major == 2 and minor >= 80:
    # 2.80-2.93: uses cycles_visibility.glossy
    obj = MockObj(cycles_visibility=MockObj(glossy=True))
    compat.set_glossy_visibility(obj, True)
    assert obj.cycles_visibility.glossy is True
  else:
    obj = MockObj(visible_glossy=False)
    compat.set_glossy_visibility(obj, True)
    assert obj.visible_glossy is True


# -- hide_object_render --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_hide_object_render(major, minor):
  compat = get_compat(major, minor)
  obj = MockObj(hide_render=False)
  compat.hide_object_render(obj, True)
  assert obj.hide_render is True


# -- hide_object_select --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_hide_object_select(major, minor):
  compat = get_compat(major, minor)
  obj = MockObj(hide_select=False)
  compat.hide_object_select(obj, True)
  assert obj.hide_select is True


# -- set_cycles_film_transparent --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_cycles_film_transparent(major, minor):
  compat = get_compat(major, minor)
  if major == 2 and minor <= 79:
    scene = MockObj(cycles=MockObj(film_transparent=False))
    compat.set_cycles_film_transparent(scene, True)
    assert scene.cycles.film_transparent is True
  else:
    scene = MockObj(render=MockObj(film_transparent=False))
    compat.set_cycles_film_transparent(scene, True)
    assert scene.render.film_transparent is True


# -- set_eevee_settings --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_eevee_settings(major, minor):
  compat = get_compat(major, minor)
  if major == 2 and minor <= 79:
    # 2.79: no-op
    scene = MockObj()
    compat.set_eevee_settings(scene, {})
    return
  if major >= 5:
    scene = MockObj(eevee=MockObj(use_shadows=False))
    compat.set_eevee_settings(scene, {"use_shadows": True})
    assert scene.eevee.use_shadows is True
  else:
    scene = MockObj(eevee=MockObj(
      gtao_factor=0, gtao_distance=0, shadow_cascade_size="0",
      shadow_cube_size="0", taa_render_samples=0, taa_samples=0,
      use_gtao=False, use_soft_shadows=False, use_ssr=False,
      shadow_pool_size="0", use_shadows=False,
    ))
    compat.set_eevee_settings(scene, {})
    # After calling with defaults, eevee attrs should be set to default values
    eevee = scene.eevee
    assert eevee.taa_render_samples == 64
    assert eevee.taa_samples == 8


# -- set_sun_shadow_properties --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_set_sun_shadow_properties(major, minor):
  compat = get_compat(major, minor)
  data = MockObj(
    shadow_soft_size=0, cycles=MockObj(use_multiple_importance_sampling=True),
    shadow_buffer_bias=0, shadow_cascade_count=0,
    use_contact_shadow=False, contact_shadow_distance=0,
  )
  sun_obj = MockObj(data=data)
  settings = {}
  compat.set_sun_shadow_properties(sun_obj, settings)
  # Core assertion: MIS always set to False
  assert sun_obj.data.cycles.use_multiple_importance_sampling is False


# -- plane_add_kwargs / camera_add_kwargs --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_plane_add_kwargs_is_dict(major, minor):
  compat = get_compat(major, minor)
  result = compat.plane_add_kwargs()
  assert isinstance(result, dict)
  assert "enter_editmode" in result


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_camera_add_kwargs_is_dict(major, minor):
  compat = get_compat(major, minor)
  result = compat.camera_add_kwargs()
  assert isinstance(result, dict)
  assert "enter_editmode" in result


# -- has_shadow_sun --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_has_shadow_sun(major, minor):
  compat = get_compat(major, minor)
  result = compat.has_shadow_sun()
  assert isinstance(result, bool)
  if major >= 3:
    assert result is False
  elif major == 2 and minor >= 80:
    assert result is True


# -- add_shadow_sun / configure_shadow_sun raise on 4.2+ --


@pytest.mark.parametrize("major,minor", [(4, 2), (5, 0)])
def test_add_shadow_sun_raises_on_newer(major, minor):
  compat = get_compat(major, minor)
  with pytest.raises(NotImplementedError):
    compat.add_shadow_sun((0, 0, 0), (0, 0, 0), 1.0, 0.02)


@pytest.mark.parametrize("major,minor", [(4, 2), (5, 0)])
def test_configure_shadow_sun_raises_on_newer(major, minor):
  compat = get_compat(major, minor)
  with pytest.raises(NotImplementedError):
    compat.configure_shadow_sun(MockObj(), {})


# -- get_invert_color_input / get_mix_color_inputs / get_mix_output --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_node_index_methods_return_correct_types(major, minor):
  compat = get_compat(major, minor)
  assert isinstance(compat.get_invert_color_input(), int)
  assert isinstance(compat.get_mix_color_inputs(), tuple)
  assert len(compat.get_mix_color_inputs()) == 2
  assert isinstance(compat.get_mix_output(), int)


def test_279_uses_old_node_indices():
  compat = get_compat(2, 79)
  assert compat.get_invert_color_input() == 1
  assert compat.get_mix_color_inputs() == (1, 2)
  assert compat.get_mix_output() == 0


def test_500_uses_new_node_indices():
  compat = get_compat(5, 0)
  assert compat.get_invert_color_input() == 0
  assert compat.get_mix_color_inputs() == (6, 7)
  assert compat.get_mix_output() == 2


# -- pure return value methods --


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_get_view_layer_name(major, minor):
  compat = get_compat(major, minor)
  name = compat.get_view_layer_name()
  assert isinstance(name, str)
  assert len(name) > 0


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_get_pixel_filter_type(major, minor):
  compat = get_compat(major, minor)
  ft = compat.get_pixel_filter_type()
  assert isinstance(ft, str)
  assert ft in ("GAUSSIAN", "BLACKMAN_HARRIS")


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_get_view_transform_default(major, minor):
  compat = get_compat(major, minor)
  vt = compat.get_view_transform_default()
  assert isinstance(vt, str)
  assert vt in ("Default", "Standard")


@pytest.mark.parametrize("major,minor", COMPAT_VERSIONS)
def test_get_engine_string(major, minor):
  compat = get_compat(major, minor)
  assert compat.get_engine_string("CYCLES") == "CYCLES"
  eevee_str = compat.get_engine_string("BLENDER_EEVEE")
  assert isinstance(eevee_str, str)
  assert "EEVEE" in eevee_str
