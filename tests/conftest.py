import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="function")
def clean_scene():
  """Reset Blender to factory state before each test.

  Uses the nuclear option for correctness — read_factory_settings()
  guarantees a clean state. Can be optimized to surgical cleanup later
  if test speed matters.
  """
  import bpy
  bpy.ops.wm.read_factory_settings(use_empty=True)
  yield
  bpy.ops.wm.read_factory_settings(use_empty=True)


@pytest.fixture
def compat(blender_version):
  """Return the compat instance for the running Blender version.

  blender_version is provided by pytest-blender as a string like '5.1.2'.
  get_compat needs (major, minor) as ints.
  """
  from shared.compat import get_compat
  parts = str(blender_version).split(".")
  return get_compat(int(parts[0]), int(parts[1]))
