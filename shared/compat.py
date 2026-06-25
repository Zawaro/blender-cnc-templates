from abc import ABC, abstractmethod
from typing import Optional, Tuple


class BaseCompat(ABC):
  """Version-specific Blender API abstraction.

  Each Blender version folder gets a compat subclass that implements
  the exact API calls for that version. scenes.py, plane_materials.py,
  world_materials.py, and script_gen.py all go through this interface
  instead of calling bpy directly for version-varying operations.
  """

  VERSION = (0, 0, 0)

  # -- Node type names (class name strings for nodes.new()) --

  @property
  @abstractmethod
  def SEPARATE_COLOR_NODE(self) -> str: ...

  @property
  @abstractmethod
  def COMBINE_COLOR_NODE(self) -> str: ...

  @property
  @abstractmethod
  def MIX_NODE(self) -> str: ...

  # -- Shader node type for SeparateRGB in world materials --

  @property
  @abstractmethod
  def SEPARATE_RGB_NODE(self) -> str: ...

  # -- Compositor node types (some nodes differ between shader/compositor trees) --

  @property
  def COMPOSITOR_MATH_NODE(self) -> str:
    """Math node type for compositor node trees."""
    return "CompositorNodeMath"

  @property
  def COMPOSITOR_VALUATORGB_NODE(self) -> str:
    """ColorRamp node type for compositor node trees."""
    return "CompositorNodeValToRGB"

  # -- Compositor access --

  @abstractmethod
  def init_compositor(self, scene) -> None:
    """Enable the compositor on *scene*. Creates node tree or group as needed."""

  @abstractmethod
  def get_compositor_tree(self, scene):
    """Return the active compositor node tree for *scene*."""

  @abstractmethod
  def get_render_layers_node(self, scene):
    """Return the Render Layers node from the compositor."""

  @abstractmethod
  def get_composite_output_node(self, scene):
    """Return the Composite / Group Output node from the compositor."""

  # -- Node group interface (inputs.new vs interface.new_socket) --

  @abstractmethod
  def add_group_input(self, group, socket_type: str, name: str) -> None: ...

  @abstractmethod
  def add_group_output(self, group, socket_type: str, name: str) -> None: ...

  # -- Compositor node property access --

  @abstractmethod
  def set_switch_value(self, node, value: bool) -> None: ...

  @abstractmethod
  def set_alpha_over_premultiply(self, node, value: bool) -> None: ...

  @abstractmethod
  def get_invert_color_input(self) -> int:
    """Return the input index for the color channel on CompositorNodeInvert."""

  @abstractmethod
  def get_mix_color_inputs(self) -> Tuple[int, int]:
    """Return (input_a, input_b) indices for the two color inputs on the mix node."""

  @abstractmethod
  def get_mix_output(self) -> int:
    """Return the output index for the mixed color result."""

  def setup_mix_node(self, node) -> None:
    """Additional setup after creating a mix node (e.g. data_type='RGBA' for 5.0)."""

  # -- Material properties --

  @abstractmethod
  def set_material_transparency(self, material, blend: str = "BLEND", shadow: str = "NONE") -> None:
    """Set blend method / shadow method on a material."""

  # -- Object properties --

  @abstractmethod
  def set_shadow_catcher(self, obj, value: bool) -> None: ...

  @abstractmethod
  def set_glossy_visibility(self, obj, value: bool) -> None: ...

  @abstractmethod
  def hide_object_viewport(self, obj, value: bool = True) -> None: ...

  @abstractmethod
  def hide_object_render(self, obj, value: bool = True) -> None: ...

  @abstractmethod
  def hide_object_select(self, obj, value: bool = True) -> None: ...

  # -- Plane creation kwargs --

  @abstractmethod
  def plane_add_kwargs(self) -> dict:
    """Extra kwargs for bpy.ops.mesh.primitive_plane_add()."""

  # -- Light creation --

  @abstractmethod
  def add_sun_light(self, location, rotation, energy: float, angle: float) -> None:
    """Create a sun light and configure it. Also sets bpy.context.active_object."""

  @abstractmethod
  def set_sun_shadow_properties(self, sun_obj, scene_settings) -> None:
    """Set shadow buffer, cascade, and contact shadow properties on a sun light."""

  @abstractmethod
  def has_shadow_sun(self) -> bool:
    """Whether this version creates a separate shadow sun object."""

  @abstractmethod
  def add_shadow_sun(self, location, rotation, energy: float, angle: float) -> None:
    """Create the secondary shadow sun (if applicable)."""

  @abstractmethod
  def configure_shadow_sun(self, shadow_sun, scene_settings) -> None:
    """Configure the secondary shadow sun after creation."""

  # -- Camera creation --

  @abstractmethod
  def camera_add_kwargs(self) -> dict:
    """Extra kwargs for bpy.ops.object.camera_add()."""

  # -- Scene management --

  @abstractmethod
  def select_scene(self, scene_name: str) -> None:
    """Make the scene with *scene_name* the active scene."""

  # -- Eevee settings --

  @abstractmethod
  def set_eevee_settings(self, scene, settings: dict) -> None:
    """Apply Eevee settings that are valid for this version."""

  # -- Cycles settings --

  @abstractmethod
  def set_cycles_film_transparent(self, scene, value: bool) -> None:
    """Set film_transparent in the correct location (cycles vs render)."""

  # -- View layer settings --

  @abstractmethod
  def get_view_layer_name(self) -> str:
    """Return the view layer name ('View Layer' or 'ViewLayer')."""

  @abstractmethod
  def set_view_layer_denoising(self, scene, enabled: bool = True) -> None:
    """Configure denoising on the view layer."""

  # -- Render settings --

  @abstractmethod
  def get_pixel_filter_type(self) -> str:
    """Return the Cycles pixel filter type."""

  @abstractmethod
  def get_view_transform_default(self) -> str:
    """Return the default view transform name."""

  @abstractmethod
  def has_viewport_settings(self) -> bool:
    """Whether set_viewport_settings() should be called."""

  # -- World materials --

  @abstractmethod
  def get_sky_density_property(self) -> str:
    """Return the sky texture density property name."""

  @abstractmethod
  def get_sky_type_value(self) -> Optional[str]:
    """Return the sky_type value, or None if not applicable."""

  # -- Generate scripts --

  @abstractmethod
  def compositor_switch_toggle(self, name: str, value: bool) -> str:
    """Return a Python code string that toggles a compositor switch node."""

  @abstractmethod
  def alpha_toggle(self, value: bool) -> str:
    """Return a Python code string that toggles the Alpha switch node."""

  @abstractmethod
  def get_engine_string(self, engine_key: str) -> str:
    """Map an engine key like 'BLENDER_EEVEE' to the version-specific engine id."""

  # -- Collections --

  @abstractmethod
  def has_collections(self) -> bool:
    """Whether this version creates collections."""

  @abstractmethod
  def create_shadow_view_layer(self, scene, full_name):
    """Create and configure a ShadowLayer view layer for shadow-only rendering.

    Returns the name of the shadow view layer, or None if not supported.
    """

  # -- Compositor node availability --

  def has_cryptomatte(self) -> bool:
    """Whether CompositorNodeCryptomatteV2 is available."""
    return True

  def has_shader_to_rgb(self) -> bool:
    """Whether ShaderNodeShaderToRGB is available."""
    return True

  def get_shadow_pass_index(self) -> int:
    """Return the Object Index pass value used for the shadow plane."""
    return 1

  def get_indexob_output_index(self) -> int:
    """Return the Render Layers output index for IndexOB."""
    return 2


def get_compat(major: int, minor: int) -> BaseCompat:
  """Return the compat instance for the given Blender version."""
  if major == 2 and minor <= 79:
    from .compat_279 import Compat279
    return Compat279()
  elif major == 2 and minor >= 80 and minor < 93:
    from .compat_280 import Compat280
    return Compat280()
  elif major == 2 and minor >= 93:
    from .compat_293 import Compat293
    return Compat293()
  elif major == 3:
    from .compat_300 import Compat300
    return Compat300()
  elif major == 4:
    from .compat_420 import Compat420
    return Compat420()
  elif major >= 5:
    from .compat_500 import Compat500
    return Compat500()
  raise ValueError("No compat class for Blender {}.{}".format(major, minor))
