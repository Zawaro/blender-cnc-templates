import os
import sys

from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_PATH)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared.compat import get_compat
from shared.scenes import ALL_SCENE_CLASSES, register_world
from shared.build_utils import load_scripts, setup_text_editor, save_blend
from shared.constants import TEMPLATE_VERSION
from constants import TEMPLATE_PREFIX

compat = get_compat(2, 80)

from world_materials import WORLD_CLASS_MAP

for name, cls in WORLD_CLASS_MAP.items():
  register_world(name, cls)

for cls in ALL_SCENE_CLASSES:
  cls(compat)

load_scripts(os.path.join(CURRENT_PATH, "scripts"))
setup_text_editor()

save_blend(TEMPLATE_PREFIX, TEMPLATE_VERSION, str(Path(__file__).resolve().parents[1]))
