import os
import sys
from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_PATH)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared.compat import get_compat
from shared.build_utils import load_scripts, setup_text_editor, save_blend
from shared.constants import TEMPLATE_VERSION
from constants import TEMPLATE_PREFIX, TEMPLATE_VARIANT
from scene_builder import build_scene, GAME_CONFIGS, _get_game_key

compat = get_compat(2, 79)

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

for full_name, suffix in SCENES:
  game_key = _get_game_key(suffix)
  build_scene(full_name, suffix, game_key, compat)

load_scripts(os.path.join(CURRENT_PATH, "scripts"))
setup_text_editor()

save_blend(TEMPLATE_PREFIX, TEMPLATE_VERSION, str(Path(__file__).resolve().parents[1]), TEMPLATE_VARIANT)
