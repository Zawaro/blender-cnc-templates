from __future__ import annotations

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
    raise RuntimeError("No 3D View found in the current screen.")

  old_areas = list(bpy.context.screen.areas)
  with bpy.context.temp_override(area=view3d_area):
    bpy.ops.screen.area_split(direction="HORIZONTAL", factor=0.001)

  new_area = None
  for area in bpy.context.screen.areas:
    if area not in old_areas:
      new_area = area
      break
  if new_area is None:
    raise RuntimeError("Could not find the newly created area after splitting.")

  new_area.type = "TEXT_EDITOR"
  text_block = bpy.data.texts.get(readme_name)
  if text_block:
    for space in new_area.spaces:
      if space.type == "TEXT_EDITOR":
        space.text = text_block
        break


def save_blend(template_prefix: str, template_version: str, project_root: str) -> Path:
  """Pack assets and save a dated .blend file to release/."""
  now = _dt.datetime.utcnow()
  file_name = f"{template_prefix}_{template_version}_{now:%Y%m%d}.blend"
  output_dir = Path(project_root) / "release"
  output_dir.mkdir(parents=True, exist_ok=True)
  save_path = output_dir / file_name

  if save_path.exists():
    os.remove(save_path)

  bpy.ops.file.pack_all()
  bpy.ops.wm.save_as_mainfile(filepath=str(save_path), check_existing=False)
  return save_path
