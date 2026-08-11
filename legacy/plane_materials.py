import bpy


BLUE_COLOR = (0.0, 0.0, 1.0)
GREY_COLOR = (0.4, 0.4, 0.4)
GRASS_COLOR = (0.0742812529206276, 0.09483204782009125, 0.058180421590805054)

# Recovered per-game specular intensity (default 0.5); falls back to the base game.
BLUE_SPEC = {
  "RA1": 0.0,
  "TS_INF": 0.0,
}


def _base_game(game_key):
  return game_key.split("_")[0]


def _make_blue(suffix, game_key):
  mat = bpy.data.materials.new(name="Plane.blue.material." + suffix)
  mat.diffuse_color = BLUE_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = BLUE_SPEC.get(game_key, BLUE_SPEC.get(_base_game(game_key), 0.5))
  mat.emit = 0.28
  mat.ambient = 0.0
  mat.alpha = 0.0
  mat.use_transparency = False
  mat.transparency_method = "MASK"
  return mat


def _make_grey(suffix):
  mat = bpy.data.materials.new(name="Plane.grey.material." + suffix)
  mat.diffuse_color = GREY_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.emit = 0.28
  mat.ambient = 0.0
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"
  return mat


def _make_grass(suffix):
  mat = bpy.data.materials.new(name="Plane.grass.material." + suffix)
  mat.diffuse_color = GRASS_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.emit = 0.28
  mat.ambient = 0.5
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"

  tex = bpy.data.textures.new(name="plane.grass.texture." + suffix, type="CLOUDS")
  tex.cloud_type = "GRAYSCALE"
  tex.noise_type = "SOFT_NOISE"
  tex.noise_basis = "CELL_NOISE"
  tex.noise_depth = 2
  tex.noise_scale = 0.005
  tex.nabla = 0.025

  slot = mat.texture_slots.add()
  slot.texture = tex
  slot.texture_coords = "WINDOW"
  slot.mapping = "FLAT"
  slot.use_map_color_diffuse = True
  slot.use_map_to_bounds = True
  slot.blend_type = "MULTIPLY"
  slot.bump_method = "BUMP_LOW_QUALITY"
  slot.normal_map_space = "TANGENT"
  return mat


def _make_hiding_blue():
  mat = bpy.data.materials.get("Hiding Blue")
  if mat is not None:
    return mat
  mat = bpy.data.materials.new(name="Hiding Blue")
  mat.diffuse_color = BLUE_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.emit = 0.0
  mat.ambient = 1.0
  mat.alpha = 0.0
  mat.use_transparency = True
  mat.transparency_method = "MASK"
  mat.use_raytrace = False
  mat.use_fake_user = True
  return mat
