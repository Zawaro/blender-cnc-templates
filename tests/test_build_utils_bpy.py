import pytest

bpy = pytest.importorskip("bpy")


class TestLoadScripts:
  def test_creates_text_datablocks(self, tmp_path):
    from shared.build_utils import load_scripts
    # Create temporary .txt files
    (tmp_path / "Alpha.Enable.txt").write_text("bpy.context.scene.render.film_transparent = True")
    (tmp_path / "Alpha.Disable.txt").write_text("bpy.context.scene.render.film_transparent = False")
    (tmp_path / "not_a_script.py").write_text("ignore me")
    load_scripts(str(tmp_path))
    assert bpy.data.texts.get("Alpha.Enable") is not None
    assert bpy.data.texts.get("Alpha.Disable") is not None
    assert bpy.data.texts.get("not_a_script") is None

  def test_script_content_matches_file(self, tmp_path):
    from shared.build_utils import load_scripts
    content = "bpy.context.scene.render.resolution_x = 1920"
    (tmp_path / "TestScript.txt").write_text(content)
    load_scripts(str(tmp_path))
    text = bpy.data.texts["TestScript"]
    assert text.as_string() == content

  def test_empty_directory_creates_nothing(self, tmp_path):
    from shared.build_utils import load_scripts
    before = len(bpy.data.texts)
    load_scripts(str(tmp_path))
    assert len(bpy.data.texts) == before

  def test_script_name_from_filename(self, tmp_path):
    from shared.build_utils import load_scripts
    (tmp_path / "Cycles.Render.Reset.txt").write_text("pass")
    load_scripts(str(tmp_path))
    assert bpy.data.texts.get("Cycles.Render.Reset") is not None
