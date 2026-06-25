import os
from typing import Dict, Optional, Tuple

from . import constants
from .compat import BaseCompat
from .scene_names import get_suffix_if_elif


class PlaneVisibility:
  def __init__(self, holdout, holdout2, shadow, shadow2, blue, grey, ambient):
    self.holdout = holdout
    self.holdout2 = holdout2
    self.shadow = shadow
    self.shadow2 = shadow2
    self.blue = blue
    self.grey = grey
    self.ambient = ambient


VISIBILITY = {
  "CYCLES": {
    "Reset": PlaneVisibility(True, True, True, True, True, False, True),
    "Buildup": PlaneVisibility(True, False, True, True, True, True, True),
    "Object": PlaneVisibility(True, True, True, True, True, True, False),
    "Preview": PlaneVisibility(False, True, False, True, True, True, True),
    "Shadow": PlaneVisibility(False, True, False, True, True, True, True),
  },
  "EEVEE": {
    "Reset": PlaneVisibility(True, True, True, True, True, False, True),
    "Buildup": PlaneVisibility(True, False, True, True, True, True, True),
    "Object": PlaneVisibility(True, True, True, True, True, True, True),
    "Preview": PlaneVisibility(True, False, False, False, True, True, True),
    "Shadow": PlaneVisibility(True, True, False, True, True, True, True),
  },
}


def _render_type_booleans(render_type: str, engine_key: str) -> Dict[str, str]:
  is_object = "True" if render_type == "Object" else "False"
  is_buildup_cycles = "True" if render_type == "Buildup" and engine_key == "CYCLES" else "False"
  is_buildup_eevee = "True" if render_type == "Buildup" and engine_key != "CYCLES" else "False"
  is_shadow_cycles = "True" if render_type == "Shadow" and engine_key == "CYCLES" else "False"
  is_shadow_eevee = "True" if render_type == "Shadow" and engine_key != "CYCLES" else "False"
  is_preview_cycles = "True" if render_type == "Preview" and engine_key == "CYCLES" else "False"
  is_preview_eevee = "True" if render_type == "Preview" and engine_key != "CYCLES" else "False"
  return {
    "Object": is_object,
    "Buildup.Cycles": is_buildup_cycles,
    "Buildup.Eevee": is_buildup_eevee,
    "Shadow.Cycles": is_shadow_cycles,
    "Shadow.Eevee": is_shadow_eevee,
    "Preview.Cycles": is_preview_cycles,
    "Preview.Eevee": is_preview_eevee,
  }


def generate_render_script(compat: BaseCompat, engine_key: str, render_type: str) -> str:
  engine_str = compat.get_engine_string(engine_key)
  vis_key = "CYCLES" if engine_key == "CYCLES" else "EEVEE"
  vis = VISIBILITY[vis_key][render_type]

  cycles_filter = constants.CYCLES_FILTER_WIDTH if render_type != "Shadow" else 0.01
  eevee_filter = constants.EEVEE_NEXT_FILTER_SIZE if render_type != "Shadow" else 0.01
  if engine_key == "CYCLES" and compat.VERSION[0] < 4:
    eevee_filter = constants.EEVEE_FILTER_SIZE

  lines = [
    "import bpy",
    "",
    'bpy.context.scene.render.engine = "{}"'.format(engine_str),
    "",
    get_suffix_if_elif(),
    "",
    'bpy.data.objects["Plane.holdout." + suffix].hide_render = {}'.format(vis.holdout),
    'bpy.data.objects["Plane.holdout2." + suffix].hide_render = {}'.format(vis.holdout2),
    'bpy.data.objects["Plane.shadow." + suffix].hide_render = {}'.format(vis.shadow),
    'bpy.data.objects["Plane.shadow2." + suffix].hide_render = {}'.format(vis.shadow2),
    'bpy.data.objects["Plane.blue." + suffix].hide_render = {}'.format(vis.blue),
    'bpy.data.objects["Plane.grey." + suffix].hide_render = {}'.format(vis.grey),
    'bpy.data.objects["Plane.ambient." + suffix].hide_render = {}'.format(vis.ambient),
    'bpy.data.objects["Sun." + suffix].hide_render = {}'.format("True" if render_type == "Shadow" and engine_key != "CYCLES" else "False"),
    "",
    "bpy.context.scene.cycles.filter_width = {}".format(cycles_filter),
    "bpy.context.scene.render.filter_size = {}".format(eevee_filter),
    "bpy.context.scene.render.use_single_layer = {}".format(render_type not in ('Shadow',)),
  ]

  bools = _render_type_booleans(render_type, engine_key)
  for switch_name, value in bools.items():
    lines.append(compat.compositor_switch_toggle(switch_name, value))

  if render_type == "Reset":
    lines.append(compat.alpha_toggle(False))

  lines.append("")
  return "\n".join(lines)


def generate_alpha_scripts(compat: BaseCompat) -> Tuple[str, str]:
  disable = "\n".join([
    "import bpy",
    "",
    compat.alpha_toggle(False),
    "bpy.context.scene.render.image_settings.color_mode = 'RGB'",
    "",
  ])
  enable = "\n".join([
    "import bpy",
    "",
    compat.alpha_toggle(True),
    "bpy.context.scene.render.image_settings.file_format = 'PNG'",
    "bpy.context.scene.render.image_settings.color_mode = 'RGBA'",
    "",
  ])
  return disable, enable


RENDER_TYPES = ["Reset", "Buildup", "Object", "Preview", "Shadow"]
ENGINE_KEYS = ["CYCLES", "EEVEE"]


def generate_all_scripts(compat: BaseCompat, output_path: str, readme_path: Optional[str] = None) -> None:
  os.makedirs(output_path, exist_ok=True)

  for engine_key in ENGINE_KEYS:
    for render_type in RENDER_TYPES:
      script = generate_render_script(compat, engine_key, render_type)
      engine_str = compat.get_engine_string(engine_key)
      display_engine = "Cycles" if engine_str == "CYCLES" else "Eevee"
      filename = "{}.Render.{}.txt".format(display_engine, render_type)
      with open(os.path.join(output_path, filename), "w") as f:
        f.write(script)

  alpha_disable, alpha_enable = generate_alpha_scripts(compat)
  with open(os.path.join(output_path, "Alpha.Disable.txt"), "w") as f:
    f.write(alpha_disable)
  with open(os.path.join(output_path, "Alpha.Enable.txt"), "w") as f:
    f.write(alpha_enable)

  if readme_path and os.path.exists(readme_path):
    with open(readme_path, "r") as rf:
      with open(os.path.join(output_path, "Readme.txt"), "w") as f:
        f.write(rf.read())
