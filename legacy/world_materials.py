import bpy


HORIZON_COLOR = (0.0, 0.0, 1.0)


def _make_world(suffix, ao_factor=0.25):
  world = bpy.data.worlds.new("World." + suffix)
  world.horizon_color = HORIZON_COLOR
  world.light_settings.use_ambient_occlusion = True
  world.light_settings.ao_factor = ao_factor
  world.light_settings.gather_method = "RAYTRACE"
  world.light_settings.samples = 5
  world.light_settings.distance = 10.0
  return world


WORLD_FACTORIES = {
  "RA2": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RA2_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RA2_FX": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "TS": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "TS_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "TS_FX": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RW": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RW_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RW_FX": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RA1": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RA1_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RA1_FX": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RM": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "RM_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "RM_FX": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "D2K": lambda suffix: _make_world(suffix, ao_factor=0.25),
  "D2K_INF": lambda suffix: _make_world(suffix, ao_factor=0.75),
  "D2K_FX": lambda suffix: _make_world(suffix, ao_factor=0.25),
}
