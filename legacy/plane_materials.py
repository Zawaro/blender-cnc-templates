import bpy


BLUE_COLOR = (0.0, 0.0, 1.0)
GREY_COLOR = (0.4, 0.4, 0.4)
GRASS_COLOR = (0.0742812529206276, 0.09483204782009125, 0.058180421590805054)


def _make_blue(suffix):
  mat = bpy.data.materials.new(name="Plane.blue.material." + suffix)
  mat.diffuse_color = BLUE_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.5
  mat.alpha = 0.0
  mat.use_transparency = False
  mat.transparency_method = "MASK"
  return mat


def _make_grey(suffix):
  mat = bpy.data.materials.new(name="Plane.grey.material." + suffix)
  mat.diffuse_color = GREY_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"
  return mat


def _make_grass(suffix):
  mat = bpy.data.materials.new(name="Plane.grass.material." + suffix)
  mat.diffuse_color = GRASS_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"
  return mat


def _make_hiding_blue(suffix):
  mat = bpy.data.materials.new(name="Hiding Blue." + suffix)
  mat.diffuse_color = BLUE_COLOR
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.alpha = 0.0
  mat.use_transparency = True
  mat.transparency_method = "MASK"
  return mat


def _make_ambient(suffix):
  mat = bpy.data.materials.new(name="Plane.ambient.material." + suffix)
  mat.diffuse_color = (0.0193824, 0.0193824, 0.0193824)
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"
  return mat


def _make_holdout(suffix):
  mat = bpy.data.materials.new(name="Plane.holdout.material." + suffix)
  mat.diffuse_color = (0.090655, 0.090655, 0.090655)
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"
  return mat


def _make_shadow(suffix):
  mat = bpy.data.materials.new(name="Plane.shadow.material." + suffix)
  mat.diffuse_color = (0.090655, 0.090655, 0.090655)
  mat.diffuse_intensity = 1.0
  mat.specular_intensity = 0.0
  mat.alpha = 1.0
  mat.use_transparency = False
  mat.transparency_method = "Z_TRANSPARENCY"
  return mat
