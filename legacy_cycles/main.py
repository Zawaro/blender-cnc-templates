# legacy_cycles/main.py
"""
Build script for the **Legacy Cycles** (Blender 2.79b) template.

The script:

1. Instantiates all scene classes from :pymod:`scenes`.
2. Removes Blender's default scene and activates a representative template.
3. Loads every ``*.txt`` file in the local `scripts/` directory into Blender's text datablocks.
4. Packs assets and writes the generated `.blend` file using the pattern

  ``{TEMPLATE_PREFIX}_{TEMPLATE_VERSION}_YYYYMMDD.blend``

The date stamp helps track when a template was built.
"""

import os
from pathlib import Path
import datetime as _dt
import bpy
import sys

# Resolve the project root (parent of this folder)
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_PATH)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

from constants import TEMPLATE_PREFIX, TEMPLATE_VERSION  # noqa: E402
from scenes import (
    BaseScene,
    RA2,
    RA2_INF,
    RA2_FX,
    TS,
    TS_FX,
    TS_INF,
    RW,
    RW_INF,
    RW_FX,
    RA1,
    RA1_INF,
    RA1_FX,
    RM,
    RM_INF,
    RM_FX,
    D2K,
    D2K_INF,
    D2K_FX,
)  # noqa: E402

# --------------------------------------------------------------------------- #
# Scene instantiation helpers
# --------------------------------------------------------------------------- #
SCENES = (
    BaseScene(),
    RA2_FX(),
    RA2_INF(),
    TS(),
    TS_FX(),
    TS_INF(),
    RW(),
    RW_INF(),
    RW_FX(),
    RA1(),
    RA1_INF(),
    RA1_FX(),
    RM(),
    RM_INF(),
    RM_FX(),
    D2K(),
    D2K_INF(),
    D2K_FX(),
)

# --------------------------------------------------------------------------- #
# Initialise and activate a scene for the build
# --------------------------------------------------------------------------- #
BASE_SCENE = BaseScene()
BASE_SCENE.cleanup()  # clean default objects
RA2().select_scene()  # keep a visible template scene

# --------------------------------------------------------------------------- #
# Load local *.txt scripts into Blender text datablocks
# --------------------------------------------------------------------------- #
scripts = os.listdir(os.path.join(CURRENT_PATH, "scripts"))
for file in range(len(scripts)):
    filename = scripts[file]
    script_name = filename.replace(".txt", "")
    print(script_name)
    with open(os.path.join(CURRENT_PATH, "scripts", scripts[file]), "r") as script:
        bpy.ops.text.new()
        text = bpy.data.texts["Text"]
        text.name = script_name
        text.write(script.read())

# --------------------------------------------------------------------------- #
# Delete existing blend file if present (to avoid stale data)
# --------------------------------------------------------------------------- #
now = _dt.datetime.utcnow()
file_name = "{}_{}_{}.blend".format(TEMPLATE_PREFIX, TEMPLATE_VERSION, now.strftime("%Y%m%d"))
output_dir = PROJECT_ROOT / "release"
output_dir.mkdir(parents=True, exist_ok=True)
save_path = output_dir / file_name

if save_path.exists():
    print("Removing old bundle {}".format(save_path))
    os.remove(save_path)

# --------------------------------------------------------------------------- #
# Pack assets and write a dated blend file
# --------------------------------------------------------------------------- #
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(save_path), check_existing=False)
