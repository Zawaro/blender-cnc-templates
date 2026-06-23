from shared.scene_names import SCENE_SUFFIX_MAP, get_suffix_if_elif


def test_scene_suffix_map_has_all_games():
  expected_games = {"RA2", "TS", "RW", "RA1", "RM", "D2K"}
  found_games = set()
  for suffix in SCENE_SUFFIX_MAP.values():
    base = suffix.split(".")[0]
    found_games.add(base)
  assert found_games == expected_games


def test_scene_suffix_map_has_variants():
  for game in ["RA2", "TS", "RW", "RA1", "RM", "D2K"]:
    assert game in SCENE_SUFFIX_MAP.values(), f"{game} base variant missing"
    assert f"{game}.INF" in SCENE_SUFFIX_MAP.values(), f"{game}.INF variant missing"
    assert f"{game}.FX" in SCENE_SUFFIX_MAP.values(), f"{game}.FX variant missing"


def test_scene_suffix_map_count():
  assert len(SCENE_SUFFIX_MAP) == 18


def test_get_suffix_if_elif_generates_valid_python():
  code = get_suffix_if_elif()
  assert "suffix = " in code
  assert "scenename = bpy.context.scene.name" in code
  compile(code, "<test>", "exec")
