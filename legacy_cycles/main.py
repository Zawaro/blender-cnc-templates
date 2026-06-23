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
from constants import TEMPLATE_PREFIX, TEMPLATE_VARIANT

compat = get_compat(2, 79)

from world_materials import (
  RA2_World, RA1_World, RW_World, TS_World, D2K_World, RM_World
)


def _adapt(world_fn):
  def wrapper(suffix, props, compat=None):
    return world_fn(props["world_texture_path"], props["world_texture_name"], suffix)
  return wrapper


register_world("RA2", _adapt(RA2_World))
register_world("RA2_INF", _adapt(RA2_World))
register_world("RA1", _adapt(RA1_World))
register_world("RW", _adapt(RW_World))
register_world("TS", _adapt(TS_World))
register_world("D2K", _adapt(D2K_World))
register_world("RM", _adapt(RM_World))

for cls in ALL_SCENE_CLASSES:
  cls(compat)

load_scripts(os.path.join(CURRENT_PATH, "scripts"))
setup_text_editor()

save_blend(TEMPLATE_PREFIX, TEMPLATE_VERSION, str(Path(__file__).resolve().parents[1]), TEMPLATE_VARIANT)
