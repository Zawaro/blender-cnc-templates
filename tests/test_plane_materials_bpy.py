import pytest

bpy = pytest.importorskip("bpy")


SUFFIX = "TEST"


def _mat_exists(name):
  return bpy.data.materials.get(name) is not None


def _node_count(mat):
  return len(mat.node_tree.nodes)


def _link_count(mat):
  return len(mat.node_tree.links)


def _output_connected(mat):
  """Check that the Material Output node has at least one input link."""
  for node in mat.node_tree.nodes:
    if node.type == "OUTPUT_MATERIAL":
      return any(link.to_node == node for link in mat.node_tree.links)
  return False


class TestPlaneAmbient:
  def test_creates_material(self):
    from shared.plane_materials import Plane_Ambient
    mat = Plane_Ambient(SUFFIX)
    assert _mat_exists("Plane.ambient." + SUFFIX)
    assert mat.use_nodes is True

  def test_has_nodes_and_links(self):
    from shared.plane_materials import Plane_Ambient
    mat = Plane_Ambient(SUFFIX)
    assert _node_count(mat) >= 8
    assert _link_count(mat) >= 7

  def test_output_connected(self):
    from shared.plane_materials import Plane_Ambient
    mat = Plane_Ambient(SUFFIX)
    assert _output_connected(mat)


class TestPlaneBlue:
  def test_creates_material(self):
    from shared.plane_materials import Plane_Blue
    mat = Plane_Blue(SUFFIX)
    assert _mat_exists("Plane.blue." + SUFFIX)
    assert mat.use_nodes is True

  def test_has_nodes_and_links(self):
    from shared.plane_materials import Plane_Blue
    mat = Plane_Blue(SUFFIX)
    assert _node_count(mat) >= 7
    assert _link_count(mat) >= 7

  def test_output_connected(self):
    from shared.plane_materials import Plane_Blue
    mat = Plane_Blue(SUFFIX)
    assert _output_connected(mat)


class TestPlaneGrey:
  def test_creates_material(self):
    from shared.plane_materials import Plane_Grey
    mat = Plane_Grey(SUFFIX)
    assert _mat_exists("Plane.grey." + SUFFIX)
    assert mat.use_nodes is True

  def test_has_nodes_and_links(self):
    from shared.plane_materials import Plane_Grey
    mat = Plane_Grey(SUFFIX)
    assert _node_count(mat) >= 5
    assert _link_count(mat) >= 5

  def test_output_connected(self):
    from shared.plane_materials import Plane_Grey
    mat = Plane_Grey(SUFFIX)
    assert _output_connected(mat)


class TestPlaneHoldout:
  def test_creates_material(self):
    from shared.plane_materials import Plane_Holdout
    mat = Plane_Holdout(SUFFIX)
    assert _mat_exists("Plane.holdout." + SUFFIX)
    assert mat.use_nodes is True

  def test_has_nodes_and_links(self):
    from shared.plane_materials import Plane_Holdout
    mat = Plane_Holdout(SUFFIX)
    assert _node_count(mat) >= 8
    assert _link_count(mat) >= 7

  def test_output_connected(self):
    from shared.plane_materials import Plane_Holdout
    mat = Plane_Holdout(SUFFIX)
    assert _output_connected(mat)


class TestPlaneShadow:
  def test_creates_material(self):
    from shared.plane_materials import Plane_Shadow
    mat = Plane_Shadow(SUFFIX)
    assert _mat_exists("Plane.shadow." + SUFFIX)
    assert mat.use_nodes is True

  def test_has_cycles_output(self):
    from shared.plane_materials import Plane_Shadow
    mat = Plane_Shadow(SUFFIX)
    outputs = [n for n in mat.node_tree.nodes if n.type == "OUTPUT_MATERIAL"]
    assert len(outputs) >= 1

  def test_has_eevee_output(self):
    from shared.plane_materials import Plane_Shadow
    mat = Plane_Shadow(SUFFIX)
    outputs = [n for n in mat.node_tree.nodes if n.type == "OUTPUT_MATERIAL"]
    # On 2.80+ there should be 2 outputs (Cycles + Eevee), on 2.79 just 1
    assert len(outputs) >= 1

  def test_output_connected(self):
    from shared.plane_materials import Plane_Shadow
    mat = Plane_Shadow(SUFFIX)
    assert _output_connected(mat)
