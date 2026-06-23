import os
import sys

from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_PATH)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared.compat import get_compat
from shared.scenes import ALL_SCENE_CLASSES, register_world
from shared.build_utils import load_scripts, setup_text_editor, save_blend
from constants import TEMPLATE_PREFIX, TEMPLATE_VERSION

compat = get_compat(2, 80)

from world_materials import (
  RA2_World, RA2_INF_World, RA1_World, RW_World, TS_World, D2K_World, RM_World
)
register_world("RA2", RA2_World)
register_world("RA2_INF", RA2_INF_World)
register_world("RA1", RA1_World)
register_world("RW", RW_World)
register_world("TS", TS_World)
register_world("D2K", D2K_World)
register_world("RM", RM_World)

for cls in ALL_SCENE_CLASSES:
  cls(compat)

load_scripts(os.path.join(CURRENT_PATH, "scripts"))
setup_text_editor()

save_blend(TEMPLATE_PREFIX, TEMPLATE_VERSION, str(Path(__file__).resolve().parents[1]))
