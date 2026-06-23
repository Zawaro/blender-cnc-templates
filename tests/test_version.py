import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

VERSION_FOLDERS = [
  "legacy_cycles", "legacy_eevee", "eevee", "cyclesx", "eevee_next", "hi_five",
]


def test_template_version_exists_in_shared():
  from shared.constants import TEMPLATE_VERSION
  assert TEMPLATE_VERSION, "TEMPLATE_VERSION must not be empty"


def test_template_version_format():
  from shared.constants import TEMPLATE_VERSION
  assert re.match(r"^\d+\.\d+\.\d+$", TEMPLATE_VERSION), (
    "TEMPLATE_VERSION must be semver like '1.0.0', got '{}'".format(TEMPLATE_VERSION)
  )


def test_no_version_in_folder_constants():
  for folder in VERSION_FOLDERS:
    constants_path = os.path.join(folder, "constants.py")
    if not os.path.exists(constants_path):
      continue
    with open(constants_path) as f:
      content = f.read()
    assert "TEMPLATE_VERSION" not in content, (
      "{} must not define TEMPLATE_VERSION — use shared.constants".format(constants_path)
    )


def test_build_number_in_build_script():
  with open("build.sh") as f:
    content = f.read()
  assert "BUILD_NUMBER" in content
  assert "git rev-list --count" in content


def test_build_utils_reads_build_number():
  source = open(
    os.path.join(os.path.dirname(__file__), "..", "shared", "build_utils.py")
  ).read()
  assert 'os.environ.get("BUILD_NUMBER"' in source
