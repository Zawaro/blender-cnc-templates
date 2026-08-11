import bpy
import os
import sys
from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, CURRENT_PATH)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plane_materials import _make_blue, _make_grey, _make_grass, _make_hiding_blue
from world_materials import WORLD_FACTORIES
from compositor import create_compositor, uses_shadow_pass


RESOLUTION_X = 640
RESOLUTION_Y = 480
RENDER_FPS = 24
FILTER_SIZE = 1.5
AA_SAMPLES = "11"

# Values recovered from CnC_template2_11.blend (Blender 2.79, BLENDER_RENDER).
# RA1/RA2/RA2_INF/TS/TS_INF are exact; RW/RM/D2K mirror the template.
GAME_CONFIGS = {
  "RA1": {
    "camera": {"type": "PERSP", "ortho_scale": 29.92, "lens": 27.7128, "obj_scale": 0.2749,
               "loc": (0, -40.4692, 28.3369), "rot": (0.9599, 0, 0)},
    "isometric_camera": {"type": "ORTHO", "ortho_scale": 55.72, "lens": 27.7128, "obj_scale": 0.2749,
                         "loc": (0, -40.4692, 28.3369), "rot": (0.9599, 0, 0)},
    "lamps": {
      "key": {"energy": 1.0, "loc": (-4.0, 4.0, 16.0431), "rot": (-0.105, -0.179, 0.008), "distance": 30.0},
      "fill": {"energy": 0.6, "loc": (-7.0711, -5.6569, 7.0), "rot": (0.035, 1.222, -2.356), "distance": 25.0},
      "rim": {"energy": 0.25, "loc": (7.0711, 5.6569, 7.0), "rot": (0.035, 1.222, -5.498), "distance": 25.0},
    },
    "planes": {"scale": (82.8483, 78.9994, 2.2571), "loc": (0, 45.3373, -0.0001), "rot_z": -1.5708, "grass": True},
    "material_index": True,
  },
  "RA2": {
    "camera": {"type": "ORTHO", "ortho_scale": 29.92, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.0389, -110.0389, 89.8467), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.4, "loc": (-4.1386, -9.9945, 12.2692), "rot": (0.6329, 0.0727, 5.7945), "distance": 30.0},
      "fill": {"energy": 0.1, "loc": (9.9945, -4.1386, 12.2692), "rot": (0.6329, 0.0727, 7.3653), "distance": 30.0},
      "rim": {"energy": 0.25, "loc": (-9.9945, 4.1386, 12.2692), "rot": (0.6329, 0.0727, 4.2237), "distance": 30.0},
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": False,
  },
  "RA2_INF": {
    "camera": {"type": "ORTHO", "ortho_scale": 29.92, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.0389, -110.0389, 89.8467), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.0, "loc": (0.0, 0.0, 12.2692), "rot": (0.0, 0.0, 0.0), "distance": 30.0},
      "fill": None,
      "rim": None,
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": False,
  },
  "TS": {
    "camera": {"type": "ORTHO", "ortho_scale": 37.4, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.0389, -110.0389, 89.8467), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.325, "loc": (-0.6378, -9.9945, 12.2692), "rot": (0.6329, 0.0727, 6.1134), "distance": 30.0},
      "fill": {"energy": 0.1, "loc": (9.9945, -0.6378, 12.2692), "rot": (0.6329, 0.0727, 7.6842), "distance": 30.0},
      "rim": {"energy": 0.25, "loc": (-9.9945, 0.6378, 12.2692), "rot": (0.6329, 0.0727, 4.5426), "distance": 30.0},
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": True,
  },
  "TS_INF": {
    "camera": {"type": "ORTHO", "ortho_scale": 37.4, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.0389, -110.0389, 89.8467), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.0, "loc": (-0.6378, -9.9945, 12.2692), "rot": (0.6329, 0.0727, 6.1134), "distance": 30.0},
      "fill": {"energy": 0.3, "loc": (11.2671, 0.131, 3.8384), "rot": (1.324, 0.125, 7.817), "distance": 30.0},
      "rim": {"energy": 0.3, "loc": (-8.5603, 8.0619, 3.8384), "rot": (1.324, 0.125, 10.202), "distance": 30.0},
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": True,
  },
  "RW": {
    "camera": {"type": "ORTHO", "ortho_scale": 37.4, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.039, -110.039, 89.847), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.4, "loc": (-4.139, -9.995, 12.269), "rot": (0.6329, 0.0727, 5.7945), "distance": 30.0},
      "fill": {"energy": 0.1, "loc": (9.995, -4.139, 12.269), "rot": (0.6329, 0.0727, 7.3653), "distance": 30.0},
      "rim": {"energy": 0.25, "loc": (-9.995, 4.139, 12.269), "rot": (0.6329, 0.0727, 4.2237), "distance": 30.0},
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": True,
  },
  "RM": {
    "camera": {"type": "ORTHO", "ortho_scale": 20.014, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.039, -110.039, 89.847), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.0, "loc": (-4.0, 4.0, 16.0), "rot": (-0.105, -0.180, 0.008), "distance": 30.0},
      "fill": {"energy": 0.6, "loc": (-7.071, -5.657, 7.0), "rot": (0.035, 1.222, -2.356), "distance": 25.0},
      "rim": {"energy": 0.25, "loc": (7.071, 5.657, 7.0), "rot": (0.035, 1.222, -5.498), "distance": 25.0},
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": True,
  },
  "D2K": {
    "camera": {"type": "ORTHO", "ortho_scale": 39.43, "lens": 35.0, "obj_scale": 1.0,
               "loc": (110.039, -110.039, 89.847), "rot": (1.0472, 0, 0.7854)},
    "lamps": {
      "key": {"energy": 1.0, "loc": (-4.0, 4.0, 16.0), "rot": (-0.698, 0, 2.356), "distance": 30.0},
      "fill": {"energy": 0.6, "loc": (-7.071, -5.657, 7.0), "rot": (0.035, 1.222, -2.356), "distance": 25.0},
      "rim": {"energy": 0.25, "loc": (7.071, 5.657, 7.0), "rot": (0.035, 1.222, -5.498), "distance": 25.0},
    },
    "planes": {"scale": (35.0, 35.0, 1.0), "loc": (0, 0, -0.0001), "rot_z": 0.0, "grass": False},
    "material_index": True,
  },
}


def _get_game_key(suffix):
  base = suffix.split(".")[0]
  if ".INF" in suffix:
    return base + "_INF"
  return base


def _setup_render(scene):
  scene.render.engine = "BLENDER_RENDER"
  scene.render.resolution_x = RESOLUTION_X
  scene.render.resolution_y = RESOLUTION_Y
  scene.render.resolution_percentage = 100
  scene.render.fps = RENDER_FPS
  scene.render.use_antialiasing = True
  scene.render.antialiasing_samples = AA_SAMPLES
  scene.render.pixel_filter_type = "MITCHELL"
  scene.render.filter_size = FILTER_SIZE
  scene.render.alpha_mode = "TRANSPARENT"
  scene.render.image_settings.file_format = "PNG"
  scene.render.image_settings.color_mode = "RGB"
  scene.render.image_settings.color_depth = "8"
  scene.render.image_settings.compression = 90
  scene.render.use_compositing = True
  scene.frame_start = 0
  scene.frame_end = 250


def _setup_render_layer(scene, cfg, use_shadow_pass):
  rl = scene.render.layers["RenderLayer"]
  rl.use_pass_z = True
  rl.use_pass_object_index = True
  rl.use_pass_ambient_occlusion = True
  rl.use_ao = True
  rl.use_pass_material_index = cfg["material_index"]
  if use_shadow_pass:
    rl.use_pass_shadow = True


def _create_camera(name, cfg):
  bpy.ops.object.camera_add(location=cfg["loc"], rotation=cfg["rot"])
  cam_obj = bpy.context.active_object
  cam_obj.name = name
  cam_obj.scale = (cfg["obj_scale"], cfg["obj_scale"], cfg["obj_scale"])
  cam = cam_obj.data
  cam.name = name
  cam.type = cfg["type"]
  cam.lens = cfg["lens"]
  if cfg["type"] == "ORTHO":
    cam.ortho_scale = cfg["ortho_scale"]
  cam.clip_start = 0.1
  cam.clip_end = 1000.0
  return cam_obj


def _create_lamp(name, energy, loc, rot, distance, shadow_method="RAY_SHADOW"):
  bpy.ops.object.lamp_add(type="SUN", location=loc, rotation=rot)
  lamp_obj = bpy.context.active_object
  lamp_obj.name = name
  lamp = lamp_obj.data
  lamp.name = name
  lamp.energy = energy
  lamp.distance = distance
  lamp.shadow_method = shadow_method
  lamp.use_shadow = shadow_method == "RAY_SHADOW"
  lamp.shadow_soft_size = 0.1
  return lamp_obj


def _create_plane(name, loc, material, scale, rot_z, hide_render=True):
  bpy.ops.mesh.primitive_plane_add(location=loc)
  obj = bpy.context.active_object
  obj.name = name
  obj.data.materials.append(material)
  obj.hide_render = hide_render
  if rot_z:
    obj.rotation_euler = (0, 0, rot_z)
  obj.scale = scale
  return obj


def build_scene(full_name, suffix, game_key, compat):
  cfg = GAME_CONFIGS.get(game_key, GAME_CONFIGS[game_key.split("_")[0]])

  bpy.ops.scene.new(type="NEW")
  scene = bpy.context.scene
  scene.name = full_name

  _setup_render(scene)
  _setup_render_layer(scene, cfg, uses_shadow_pass(game_key))

  world_factory = WORLD_FACTORIES.get(game_key, lambda s: WORLD_FACTORIES["RA2"](s))
  scene.world = world_factory(suffix)

  cam_obj = _create_camera("Camera." + suffix, cfg["camera"])
  scene.camera = cam_obj
  if cfg.get("isometric_camera"):
    _create_camera("Camera." + suffix + ".isometric", cfg["isometric_camera"])

  for lamp_name, lamp_cfg in (("key.shadow", cfg["lamps"]["key"]), ("fill", cfg["lamps"]["fill"]), ("rim", cfg["lamps"]["rim"])):
    if not lamp_cfg or lamp_cfg["energy"] <= 0:
      continue
    _create_lamp(
      "Lamp." + suffix + "." + lamp_name,
      lamp_cfg["energy"], lamp_cfg["loc"], lamp_cfg["rot"], lamp_cfg["distance"],
      shadow_method="RAY_SHADOW" if lamp_name == "key.shadow" else "NOSHADOW",
    )

  blue_mat = _make_blue(suffix, game_key)
  grey_mat = _make_grey(suffix)

  _create_plane("Plane.blue." + suffix, cfg["planes"]["loc"], blue_mat, cfg["planes"]["scale"], cfg["planes"]["rot_z"], hide_render=True)
  _create_plane("Plane.grey." + suffix, cfg["planes"]["loc"], grey_mat, cfg["planes"]["scale"], cfg["planes"]["rot_z"], hide_render=False)
  if cfg["planes"]["grass"]:
    grass_mat = _make_grass(suffix)
    _create_plane("Plane.grass." + suffix, cfg["planes"]["loc"], grass_mat, cfg["planes"]["scale"], cfg["planes"]["rot_z"], hide_render=True)

  # Hiding Blue: recovered from the source .blend as a user-facing material for
  # hiding objects against the blue screen (README v2.10). Not assigned to any
  # plane in the source; kept as a datablock with fake_user so it survives save.
  _make_hiding_blue()

  create_compositor(scene, game_key)

  return scene
