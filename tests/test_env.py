import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_env_example_exists():
  assert os.path.exists(".env.example")


def test_env_example_has_all_vars():
  expected = [
    "BLENDER_LEGACY", "BLENDER_LEGACY_CYCLES", "BLENDER_EEVEE",
    "BLENDER_CYCLESX", "BLENDER_EEVEE_NEXT", "BLENDER_HI_FIVE",
  ]
  with open(".env.example") as f:
    content = f.read()
  for var in expected:
    assert var in content, f"Missing {var} in .env.example"


def test_env_file_format():
  if not os.path.exists(".env"):
    return
  with open(".env") as f:
    for line in f:
      line = line.strip()
      if not line or line.startswith("#"):
        continue
      assert "=" in line, f"Invalid .env line (no '='): {line}"
      key, _, value = line.partition("=")
      assert key.startswith("BLENDER_"), f"Unexpected key in .env: {key}"
      if value:
        assert os.path.exists(value), f"Blender binary not found: {value} (for {key})"


def test_fill_env_script_exists():
  assert os.path.exists("fill_env.sh")


def test_build_script_loads_env():
  with open("build.sh") as f:
    content = f.read()
  assert 'BLENDER_' in content
  assert '.env' in content
