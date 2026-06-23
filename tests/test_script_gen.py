import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.compat import get_compat
from shared.script_gen import (
  generate_render_script, generate_alpha_scripts, generate_all_scripts,
  RENDER_TYPES, ENGINE_KEYS, VISIBILITY,
)


def test_all_engine_render_type_combinations():
  for compat_ver in [(2, 79), (2, 80), (3, 0), (4, 2), (5, 0)]:
    compat = get_compat(*compat_ver)
    for engine in ENGINE_KEYS:
      for rtype in RENDER_TYPES:
        script = generate_render_script(compat, engine, rtype)
        assert "import bpy" in script
        assert "suffix" in script
        assert "bpy.context.scene.render.engine" in script


def test_visibility_covers_all_combinations():
  for engine_key in ["CYCLES", "EEVEE"]:
    assert engine_key in VISIBILITY
    for rtype in RENDER_TYPES:
      assert rtype in VISIBILITY[engine_key]
      vis = VISIBILITY[engine_key][rtype]
      assert hasattr(vis, "holdout")
      assert hasattr(vis, "holdout2")
      assert hasattr(vis, "shadow")
      assert hasattr(vis, "shadow2")
      assert hasattr(vis, "blue")
      assert hasattr(vis, "grey")
      assert hasattr(vis, "ambient")


def test_alpha_scripts_generated():
  for compat_ver in [(2, 79), (4, 2), (5, 0)]:
    compat = get_compat(*compat_ver)
    disable, enable = generate_alpha_scripts(compat)
    assert "import bpy" in disable
    assert "import bpy" in enable
    assert "color_mode = 'RGB'" in disable
    assert "color_mode = 'RGBA'" in enable


def test_engine_string_mapping():
  for compat_ver in [(2, 79), (2, 80), (3, 0), (4, 2), (5, 0)]:
    compat = get_compat(*compat_ver)
    assert compat.get_engine_string("CYCLES") == "CYCLES"
    eevee_str = compat.get_engine_string("EEVEE")
    assert eevee_str in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT")


def test_generate_all_scripts_creates_files():
  import tempfile
  import shutil
  tmpdir = tempfile.mkdtemp()
  try:
    compat = get_compat(5, 0)
    generate_all_scripts(compat, tmpdir)
    expected_files = []
    for engine in ["Cycles", "Eevee"]:
      for rtype in RENDER_TYPES:
        expected_files.append(f"{engine}.Render.{rtype}.txt")
    expected_files.append("Alpha.Disable.txt")
    expected_files.append("Alpha.Enable.txt")
    for f in expected_files:
      assert os.path.exists(os.path.join(tmpdir, f)), f"Missing: {f}"
  finally:
    shutil.rmtree(tmpdir)
