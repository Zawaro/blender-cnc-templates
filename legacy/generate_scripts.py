import os

current_path = os.path.dirname(os.path.realpath(__file__))

output_path = os.path.join(current_path, "scripts")

# All 18 scenes. The recovered v2.11 scripts covered the 5 source games
# (TS/TS.INF/RA2/RA2.INF/RA1) with identical per-game values; the extrapolated
# games follow the same pattern.
SCENES = [
  ("Red Alert 2", "RA2"),
  ("Red Alert 2 - Infantry", "RA2.INF"),
  ("Red Alert 2 - Effects", "RA2.FX"),
  ("Tiberian Sun", "TS"),
  ("Tiberian Sun - Infantry", "TS.INF"),
  ("Tiberian Sun - Effects", "TS.FX"),
  ("ReWire", "RW"),
  ("ReWire - Infantry", "RW.INF"),
  ("ReWire - Effects", "RW.FX"),
  ("Red Alert / Tiberian Dawn", "RA1"),
  ("Red Alert / Tiberian Dawn - Infantry", "RA1.INF"),
  ("Red Alert / Tiberian Dawn - Effects", "RA1.FX"),
  ("C&C Remastered", "RM"),
  ("C&C Remastered - Infantry", "RM.INF"),
  ("C&C Remastered - Effects", "RM.FX"),
  ("Dune 2000", "D2K"),
  ("Dune 2000 - Infantry", "D2K.INF"),
  ("Dune 2000 - Effects", "D2K.FX"),
]
GRASS_GAMES = {"RA1", "RA1.INF", "RA1.FX"}

RENDER_TYPES = ["Reset", "Buildup", "Object", "Shadow"]

# Toggles recovered from the CnC_template2_11.blend render scripts.
VISIBILITY = {
  "Reset": {
    "aa_on": True, "switch_on": True, "pass_index": 0,
    "blue_transparent": False, "blue_visible": False, "grey_visible": True,
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
  "Shadow": {
    "aa_on": False, "switch_on": False, "pass_index": 1,
    "blue_transparent": False, "blue_visible": True, "grey_visible": False,
    "ao_on": False,
  },
}


def _render_script(render_type):
  vis = VISIBILITY[render_type]
  parts = ["import bpy"]

  for full_name, _ in SCENES:
    parts.append('bpy.data.scenes["{}"].render.use_antialiasing = {}'.format(full_name, vis["aa_on"]))

  parts.append("bpy.context.scene.node_tree.nodes[\"Switch\"].check = {}".format(vis["switch_on"]))

  parts.append("bpy.ops.object.select_all(action='SELECT')")
  parts.append("for ob in bpy.context.selected_objects:\n    ob.pass_index = {}".format(vis["pass_index"]))

  for _, suffix in SCENES:
    parts.append('bpy.data.materials["{}"].use_transparency = {}'.format("Plane.blue.material." + suffix, vis["blue_transparent"]))
    parts.append('bpy.data.objects["{}"].hide_render = {}'.format("Plane.blue." + suffix, not vis["blue_visible"]))
    parts.append('bpy.data.objects["{}"].hide_render = {}'.format("Plane.grey." + suffix, not vis["grey_visible"]))
    if suffix in GRASS_GAMES:
      parts.append('bpy.data.objects["{}"].hide_render = True'.format("Plane.grass." + suffix))

  for _, suffix in SCENES:
    parts.append('bpy.data.worlds["{}"].light_settings.use_ambient_occlusion = {}'.format("World." + suffix, vis["ao_on"]))

  return "\n\n".join(parts)


def generate_all():
  os.makedirs(output_path, exist_ok=True)

  filename_map = {"Reset": "reset", "Buildup": "buildup", "Object": "object", "Shadow": "shadows"}

  for render_type in RENDER_TYPES:
    script = _render_script(render_type)
    filename = "Render.{}.txt".format(filename_map[render_type])
    with open(os.path.join(output_path, filename), "w") as f:
      f.write(script)
    print("Generated:", filename)

  readme_path = os.path.join(current_path, "README.md")
  if os.path.exists(readme_path):
    with open(readme_path, "r") as rf:
      with open(os.path.join(output_path, "Readme.txt"), "w") as f:
        f.write("\n".join("# " + line if line.strip() else line for line in rf.read().split("\n")))
    print("Generated: Readme.txt")


if __name__ == "__main__":
  generate_all()
