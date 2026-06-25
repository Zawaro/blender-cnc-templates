import pytest

bpy = pytest.importorskip("bpy")


class MockWorld:
  """Minimal world class for testing — creates a world with no external deps."""

  def __init__(self, suffix, props, compat):
    world = bpy.data.worlds.new("World." + suffix)
    world.use_nodes = True
    bpy.context.scene.world = world
    self.node_tree = world.node_tree
    self.name = world.name


@pytest.fixture(autouse=True)
def _setup_world():
  """Register a mock world class and clean up after."""
  from shared.scenes import register_world, _WORLD_REGISTRY
  register_world("TEST", MockWorld)
  register_world("TEST.INF", MockWorld)
  register_world("TEST.FX", MockWorld)
  yield
  _WORLD_REGISTRY.clear()


def _make_scene(compat):
  from shared.scenes import BaseScene

  class TestScene(BaseScene):
    name = "Test"
    suffix = "TEST"
    full_name = "Test"
    world_class_suffix = "TEST"

  return TestScene(compat)


class TestBaseScene:
  def test_creates_scene(self, clean_scene, compat):
    _make_scene(compat)
    created = bpy.data.scenes.get("Test")
    assert created is not None

  def test_creates_camera(self, clean_scene, compat):
    _make_scene(compat)
    cameras = [o for o in bpy.data.objects if o.type == "CAMERA"]
    assert len(cameras) >= 1

  def test_creates_sun_light(self, clean_scene, compat):
    _make_scene(compat)
    lights = [o for o in bpy.data.objects if o.type == "LIGHT"]
    assert len(lights) >= 1

  def test_creates_plane_objects(self, clean_scene, compat):
    _make_scene(compat)
    planes = [o for o in bpy.data.objects if o.type == "MESH"]
    assert len(planes) >= 6

  def test_creates_materials(self, clean_scene, compat):
    _make_scene(compat)
    mat_names = [m.name for m in bpy.data.materials]
    assert any("ambient" in n for n in mat_names)
    assert any("shadow" in n for n in mat_names)

  def test_scene_has_world(self, clean_scene, compat):
    _make_scene(compat)
    scene = bpy.data.scenes.get("Test")
    assert scene is not None
    assert scene.world is not None

  def test_creates_collections_on_280plus(self, clean_scene, compat):
    if not compat.has_collections():
      pytest.skip("Collections not supported on this version")
    _make_scene(compat)
    col_names = [c.name for c in bpy.data.collections]
    assert "Test" in col_names or "Test Template" in col_names
