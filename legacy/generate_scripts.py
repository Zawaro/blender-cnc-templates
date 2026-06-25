import os
import sys
from pathlib import Path

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(current_path)
sys.path.append(parent_path)

from shared.scene_names import get_suffix_if_elif

output_path = os.path.join(current_path, "scripts")

SCENE_NAMES = [
  "Red Alert 2", "Red Alert 2 - Infantry", "Red Alert 2 - Effects",
  "Tiberian Sun", "Tiberian Sun - Infantry", "Tiberian Sun - Effects",
  "ReWire", "ReWire - Infantry", "ReWire - Effects",
  "Red Alert / Tiberian Dawn", "Red Alert / Tiberian Dawn - Infantry", "Red Alert / Tiberian Dawn - Effects",
  "C&C Remastered", "C&C Remastered - Infantry", "C&C Remastered - Effects",
  "Dune 2000", "Dune 2000 - Infantry", "Dune 2000 - Effects",
]

GAME_SUFFIXES = [
  "RA2", "RA2.INF", "RA2.FX",
  "TS", "TS.INF", "TS.FX",
  "RW", "RW.INF", "RW.FX",
  "RA1", "RA1.INF", "RA1.FX",
  "RM", "RM.INF", "RM.FX",
  "D2K", "D2K.INF", "D2K.FX",
]

INF_SUFFIXES = {"RA2.INF", "TS.INF", "RW.INF", "RA1.INF", "RM.INF", "D2K.INF"}
FX_SUFFIXES = {"RA2.FX", "TS.FX", "RW.FX", "RA1.FX", "RM.FX", "D2K.FX"}
RA1_SUFFIXES = {"RA1", "RA1.INF", "RA1.FX"}

RENDER_TYPES = ["Reset", "Buildup", "Object", "Preview", "Shadow"]

VISIBILITY = {
  "Reset": {
    "aa_on": True, "switch_on": True, "pass_index": 0,
    "blue_transparent": False, "blue_visible": True, "grey_visible": True,
    "ao_on": True,
  },
  "Buildup": {
    "aa_on": True, "switch_on": True, "pass_index": 0,
    "blue_transparent": True, "blue_visible": True, "grey_visible": False,
    "ao_on": True,
  },
  "Object": {
    "aa_on": True, "switch_on": True, "pass_index": 0,
    "blue_transparent": False, "blue_visible": False, "grey_visible": False,
    "ao_on": True,
  },
  "Preview": {
    "aa_on": True, "switch_on": True, "pass_index": 0,
    "blue_transparent": False, "blue_visible": False, "grey_visible": True,
    "ao_on": True,
  },
  "Shadow": {
    "aa_on": False, "switch_on": False, "pass_index": 1,
    "blue_transparent": False, "blue_visible": True, "grey_visible": False,
    "ao_on": False,
  },
}


def _generate_base():
  lines = [
    "import bpy",
    "",
    get_suffix_if_elif(),
    "",
  ]
  return "\n".join(lines)


def _generate_aa_block(aa_on):
  val = "True" if aa_on else "False"
  lines = []
  for name in SCENE_NAMES:
    lines.append('bpy.data.scenes["{}"].render.use_antialiasing = {}'.format(name, val))
  return "\n".join(lines)


def _generate_switch_block(switch_on):
  val = "True" if switch_on else "False"
  return 'bpy.context.scene.node_tree.nodes["Switch"].check = {}'.format(val)


def _generate_pass_index_block(pass_index):
  lines = [
    "bpy.ops.object.select_all(action='SELECT')",
    "",
    "for ob in bpy.context.selected_objects:",
    "    ob.pass_index = {}".format(pass_index),
  ]
  return "\n".join(lines)


def _generate_plane_block(suffix, vis):
  lines = []

  blue_mat_name = "Plane.blue.material." + suffix
  blue_obj_name = "Plane.blue." + suffix
  grey_obj_name = "Plane.grey." + suffix
  grass_obj_name = "Plane.grass." + suffix

  if vis["blue_transparent"]:
    lines.append('bpy.data.materials["{}"].use_transparency = True'.format(blue_mat_name))
  else:
    lines.append('bpy.data.materials["{}"].use_transparency = False'.format(blue_mat_name))

  if vis["blue_visible"]:
    lines.append('bpy.data.objects["{}"].hide_render = False'.format(blue_obj_name))
  else:
    lines.append('bpy.data.objects["{}"].hide_render = True'.format(blue_obj_name))

  if vis["grey_visible"]:
    lines.append('bpy.data.objects["{}"].hide_render = False'.format(grey_obj_name))
  else:
    lines.append('bpy.data.objects["{}"].hide_render = True'.format(grey_obj_name))

  if suffix in RA1_SUFFIXES:
    lines.append('bpy.data.objects["{}"].hide_render = True'.format(grass_obj_name))

  return "\n".join(lines)


def _generate_ao_block(ao_on):
  val = "True" if ao_on else "False"
  lines = []
  for suffix in GAME_SUFFIXES:
    lines.append('bpy.data.worlds["World.{}"].light_settings.use_ambient_occlusion = {}'.format(suffix, val))
  return "\n".join(lines)


def generate_render_script(render_type):
  vis = VISIBILITY[render_type]
  parts = [
    _generate_base(),
    "",
    _generate_aa_block(vis["aa_on"]),
    "",
    _generate_switch_block(vis["switch_on"]),
    "",
    _generate_pass_index_block(vis["pass_index"]),
    "",
  ]

  for suffix in GAME_SUFFIXES:
    parts.append(_generate_plane_block(suffix, vis))

  parts.append("")
  parts.append(_generate_ao_block(vis["ao_on"]))
  parts.append("")

  return "\n".join(parts)


def generate_alpha_disable():
  return "\n".join([
    "import bpy",
    "",
    'bpy.context.scene.render.image_settings.color_mode = \'RGB\'',
    "",
  ])


def generate_alpha_enable():
  return "\n".join([
    "import bpy",
    "",
    'bpy.context.scene.render.image_settings.file_format = \'PNG\'',
    'bpy.context.scene.render.image_settings.color_mode = \'RGBA\'',
    "",
  ])


def generate_all():
  os.makedirs(output_path, exist_ok=True)

  for render_type in RENDER_TYPES:
    script = generate_render_script(render_type)
    filename = "Legacy.Render.{}.txt".format(render_type)
    with open(os.path.join(output_path, filename), "w") as f:
      f.write(script)
    print("Generated:", filename)

  with open(os.path.join(output_path, "Alpha.Disable.txt"), "w") as f:
    f.write(generate_alpha_disable())
  print("Generated: Alpha.Disable.txt")

  with open(os.path.join(output_path, "Alpha.Enable.txt"), "w") as f:
    f.write(generate_alpha_enable())
  print("Generated: Alpha.Enable.txt")

  readme_path = os.path.join(current_path, "README.md")
  if os.path.exists(readme_path):
    with open(readme_path, "r") as rf:
      with open(os.path.join(output_path, "Readme.txt"), "w") as f:
        f.write(rf.read())
    print("Generated: Readme.txt")


if __name__ == "__main__":
  generate_all()
