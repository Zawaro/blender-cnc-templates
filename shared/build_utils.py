import datetime as _dt
import os
from pathlib import Path

import bpy


def load_scripts(script_dir: str) -> None:
  """Load all .txt files from *script_dir* into Blender text datablocks."""
  for filename in os.listdir(script_dir):
    if not filename.endswith(".txt"):
      continue
    script_name = filename.replace(".txt", "")
    with open(os.path.join(script_dir, filename), "r") as f:
      bpy.ops.text.new()
      text = bpy.data.texts["Text"]
      text.name = script_name
      text.write(f.read())


def setup_text_editor(readme_name: str = "Readme") -> None:
  """Split the 3D viewport and show a Text Editor with the readme."""
  view3d_area = next((a for a in bpy.context.screen.areas if a.type == "VIEW_3D"), None)
  if view3d_area is None:
    return

  # temp_override requires Blender 3.2+
  if not hasattr(bpy.context, "temp_override"):
    return

  old_areas = list(bpy.context.screen.areas)
  with bpy.context.temp_override(area=view3d_area):
    bpy.ops.screen.area_split(direction="HORIZONTAL", factor=0.001)

  new_area = None
  for area in bpy.context.screen.areas:
    if area not in old_areas:
      new_area = area
      break
  if new_area is None:
    return

  new_area.type = "TEXT_EDITOR"
  text_block = bpy.data.texts.get(readme_name)
  if text_block:
    for space in new_area.spaces:
      if space.type == "TEXT_EDITOR":
        space.text = text_block
        break


def save_blend(template_prefix, template_version, project_root, variant=""):
  now = _dt.datetime.utcnow()
  build_number = os.environ.get("BUILD_NUMBER", "0")
  version_tag = "{}_build{}".format(template_version, build_number)
  file_name = "{}_{}_{:%Y%m%d}.blend".format(template_prefix, version_tag, now)
  output_dir = Path(project_root) / "release" / variant if variant else Path(project_root) / "release"
  output_dir.mkdir(parents=True, exist_ok=True)
  save_path = output_dir / file_name

  if save_path.exists():
    os.remove(str(save_path))

  bpy.ops.file.pack_all()
  bpy.ops.wm.save_as_mainfile(filepath=str(save_path), check_existing=False)
  return save_path
