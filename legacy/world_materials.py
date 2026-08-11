import bpy


HORIZON_COLOR = (0.0, 0.0, 1.0)


def _make_world(suffix, ao_factor=0.25):
  world = bpy.data.worlds.new("World." + suffix)
  world.horizon_color = HORIZON_COLOR
  ls = world.light_settings
  ls.use_ambient_occlusion = True
  ls.ao_factor = ao_factor
  ls.gather_method = "RAYTRACE"
  ls.samples = 5
  ls.distance = 10.0
  ls.bias = 0.05
  ls.use_falloff = True
  ls.falloff_strength = 0.1
  ls.sample_method = "CONSTANT_QMC"
  ls.threshold = 0.005
  ls.error_threshold = 0.25
  ls.ao_blend_type = "ADD"
  return world


WORLD_FACTORIES = {
  "RA2": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RA2_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "TS": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "TS_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RW": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RW_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RA1": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RA1_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RM": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RM_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "D2K": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "D2K_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
}
