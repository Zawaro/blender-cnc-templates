import bpy
import os
import sys
from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, CURRENT_PATH)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plane_materials import (
  _make_blue, _make_grey, _make_grass, _make_ambient, _make_holdout, _make_shadow,
)
from world_materials import WORLD_FACTORIES


RESOLUTION_X = 640
RESOLUTION_Y = 480
RENDER_FPS = 24
FILTER_SIZE = 1.5
AA_SAMPLES = "11"

LAYER_SHARED = 0
LAYER_RA2 = 1
LAYER_TS = 2
LAYER_RA1 = 3
LAYER_RW = 4
LAYER_RM = 5
LAYER_D2K = 6

GAME_LAMP_LAYER = {
  "RA2": LAYER_RA2,
  "TS": LAYER_TS,
  "RA1": LAYER_RA1,
  "RW": LAYER_RW,
  "RM": LAYER_RM,
  "D2K": LAYER_D2K,
}

ALL_LAMP_LAYERS = [LAYER_RA2, LAYER_TS, LAYER_RA1, LAYER_RW, LAYER_RM, LAYER_D2K]


GAME_CONFIGS = {
  "RA2": {
    "camera_type": "ORTHO", "camera_scale": 29.92,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.4, "key_loc": (-4.139, -9.995, 12.269), "key_rot": (0.6329, 0.0727, 5.7945),
    "fill_energy": 0.1, "fill_loc": (9.995, -4.139, 12.269), "fill_rot": (0.6329, 0.0727, 7.3653),
    "rim_energy": 0.25, "rim_loc": (-9.995, 4.139, 12.269), "rim_rot": (0.6329, 0.0727, 4.2237),
  },
  "RA2_INF": {
    "camera_type": "ORTHO", "camera_scale": 29.92,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.0, "key_loc": (0, 0, 12.269), "key_rot": (0, 0, 0),
    "fill_energy": 0, "fill_loc": (0, 0, 0), "fill_rot": (0, 0, 0),
    "rim_energy": 0, "rim_loc": (0, 0, 0), "rim_rot": (0, 0, 0),
  },
  "TS": {
    "camera_type": "ORTHO", "camera_scale": 37.4,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.325, "key_loc": (-0.638, -9.995, 12.269), "key_rot": (0.6329, 0.0727, 6.1134),
    "fill_energy": 0.1, "fill_loc": (9.995, -0.638, 12.269), "fill_rot": (0.6329, 0.0727, 7.6842),
    "rim_energy": 0.25, "rim_loc": (-9.995, 0.638, 12.269), "rim_rot": (0.6329, 0.0727, 4.5426),
  },
  "TS_INF": {
    "camera_type": "ORTHO", "camera_scale": 37.4,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.0, "key_loc": (-0.638, -9.995, 12.269), "key_rot": (0.6329, 0.0727, 6.1134),
    "fill_energy": 0.3, "fill_loc": (11.267, 0.131, 3.838), "fill_rot": (1.324, 0.125, 7.817),
    "rim_energy": 0.3, "rim_loc": (-8.560, 8.062, 3.838), "rim_rot": (1.324, 0.125, 10.202),
  },
  "RA1": {
    "camera_type": "PERSP", "camera_scale": 29.92,
    "camera_loc": (0, -40.469, 28.337), "camera_rot": (0.9599, 0, 0),
    "key_energy": 1.0, "key_loc": (-4.0, 4.0, 16.043), "key_rot": (-0.105, -0.179, 0.008),
    "fill_energy": 0.6, "fill_loc": (-7.071, -5.657, 7.0), "fill_rot": (0.035, 1.222, -2.356),
    "rim_energy": 0.25, "rim_loc": (7.071, 5.657, 7.0), "rim_rot": (0.035, 1.222, -5.498),
  },
  "RW": {
    "camera_type": "ORTHO", "camera_scale": 37.4,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.4, "key_loc": (-4.139, -9.995, 12.269), "key_rot": (0.6329, 0.0727, 5.7945),
    "fill_energy": 0.1, "fill_loc": (9.995, -4.139, 12.269), "fill_rot": (0.6329, 0.0727, 7.3653),
    "rim_energy": 0.25, "rim_loc": (-9.995, 4.139, 12.269), "rim_rot": (0.6329, 0.0727, 4.2237),
  },
  "RM": {
    "camera_type": "ORTHO", "camera_scale": 20.014,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.0, "key_loc": (-4.0, 4.0, 16.0), "key_rot": (-0.105, -0.180, 0.008),
    "fill_energy": 0.6, "fill_loc": (-7.071, -5.657, 7.0), "fill_rot": (0.035, 1.222, -2.356),
    "rim_energy": 0.25, "rim_loc": (7.071, 5.657, 7.0), "rim_rot": (0.035, 1.222, -5.498),
  },
  "D2K": {
    "camera_type": "ORTHO", "camera_scale": 39.43,
    "camera_loc": (110.039, -110.039, 89.847), "camera_rot": (1.0472, 0, 0.7854),
    "key_energy": 1.0, "key_loc": (-4.0, 4.0, 16.0), "key_rot": (-0.698, 0, 2.356),
    "fill_energy": 0.6, "fill_loc": (-7.071, -5.657, 7.0), "fill_rot": (0.035, 1.222, -2.356),
    "rim_energy": 0.25, "rim_loc": (7.071, 5.657, 7.0), "rim_rot": (0.035, 1.222, -5.498),
  },
}


def _get_game_key(suffix):
  base = suffix.split(".")[0]
  return base


def _create_compositor(scene):
  scene.use_nodes = True
  tree = scene.node_tree
  nodes = tree.nodes
  links = tree.links

  for n in list(nodes):
    nodes.remove(n)

  rl = nodes.new("CompositorNodeRLayers")
  rl.name = "Render Layers"
  rl.location = (-600, 0)

  rl2 = nodes.new("CompositorNodeRLayers")
  rl2.name = "Render Layers.002"
  rl2.location = (-600, -200)

  idmask = nodes.new("CompositorNodeIDMask")
  idmask.name = "ID Mask"
  idmask.index = 0
  idmask.location = (-200, -200)

  switch = nodes.new("CompositorNodeSwitch")
  switch.name = "Switch"
  switch.check = True
  switch.location = (200, 0)

  alpha_convert = nodes.new("CompositorNodePremulKey")
  alpha_convert.name = "Alpha Convert"
  alpha_convert.location = (-200, 100)

  combine_bg = nodes.new("CompositorNodeCombRGBA")
  combine_bg.name = "Combine RGBA"
  combine_bg.inputs[0].default_value = 0.0
  combine_bg.inputs[1].default_value = 0.0
  combine_bg.inputs[2].default_value = 1.0
  combine_bg.inputs[3].default_value = 1.0
  combine_bg.location = (0, -300)

  mix_bg = nodes.new("CompositorNodeMixRGB")
  mix_bg.name = "Mix"
  mix_bg.blend_type = "MIX"
  mix_bg.inputs[0].default_value = 1.0
  mix_bg.location = (200, -200)

  ao = nodes.new("CompositorNodeAlphaOver")
  ao.name = "Alpha Over"
  ao.location = (500, 0)

  composite = nodes.new("CompositorNodeComposite")
  composite.name = "Composite"
  composite.location = (700, 0)

  viewer = nodes.new("CompositorNodeViewer")
  viewer.name = "Viewer"
  viewer.location = (700, -200)

  links.new(rl.outputs[0], alpha_convert.inputs[0])
  links.new(alpha_convert.outputs[0], switch.inputs[1])
  links.new(rl2.outputs[14], idmask.inputs[0])
  links.new(combine_bg.outputs[0], mix_bg.inputs[1])
  links.new(idmask.outputs[0], mix_bg.inputs[2])
  links.new(mix_bg.outputs[0], switch.inputs[0])
  links.new(rl.outputs[0], ao.inputs[2])
  links.new(switch.outputs[0], ao.inputs[1])
  links.new(ao.outputs[0], composite.inputs[0])
  links.new(ao.outputs[0], viewer.inputs[0])


def _create_camera(name, cam_type, ortho_scale, loc, rot, layer=LAYER_SHARED):
  bpy.ops.object.camera_add(location=loc, rotation=rot)
  cam_obj = bpy.context.active_object
  cam_obj.name = name
  cam = cam_obj.data
  cam.name = name
  cam.type = cam_type
  cam.ortho_scale = ortho_scale
  cam.clip_end = 1000.0
  cam_obj.hide_render = True
  layers = [False] * 20
  layers[layer] = True
  cam_obj.layers = layers
  return cam_obj


def _create_lamp(name, energy, loc, rot, shadow_method="RAY_SHADOW", layer=LAYER_SHARED):
  bpy.ops.object.lamp_add(type="SUN", location=loc, rotation=rot)
  lamp_obj = bpy.context.active_object
  lamp_obj.name = name
  lamp = lamp_obj.data
  lamp.name = name
  lamp.energy = energy
  lamp.shadow_method = shadow_method
  lamp.use_shadow = shadow_method == "RAY_SHADOW"
  layers = [False] * 20
  layers[layer] = True
  lamp_obj.layers = layers
  return lamp_obj


def _create_plane(name, loc, material, hide_render=True, layer=LAYER_SHARED):
  bpy.ops.mesh.primitive_plane_add(location=loc)
  obj = bpy.context.active_object
  obj.name = name
  obj.data.materials.append(material)
  obj.hide_render = hide_render
  layers = [False] * 20
  layers[layer] = True
  obj.layers = layers
  return obj


def build_scene(full_name, suffix, game_key, compat):
  cfg = GAME_CONFIGS[game_key]

  bpy.ops.scene.new(type="NEW")
  scene = bpy.context.scene
  scene.name = full_name
  scene.render.engine = "BLENDER_RENDER"
  scene.render.resolution_x = RESOLUTION_X
  scene.render.resolution_y = RESOLUTION_Y
  scene.render.resolution_percentage = 100
  scene.render.fps = RENDER_FPS
  scene.render.filter_size = FILTER_SIZE
  scene.render.use_antialiasing = True
  scene.render.antialiasing_samples = AA_SAMPLES
  scene.frame_start = 0
  scene.frame_end = 250

  rl = scene.render.layers["RenderLayer"]
  game_layer = GAME_LAMP_LAYER[game_key]
  exclude_layers = [l for l in ALL_LAMP_LAYERS if l != game_layer]
  layers_exclude = [False] * 20
  for l in exclude_layers:
    layers_exclude[l] = True
  rl.layers_exclude = layers_exclude

  world_factory = WORLD_FACTORIES.get(game_key, lambda s: WORLD_FACTORIES["RA2"](s))
  world = world_factory(suffix)
  scene.world = world

  cam_obj = _create_camera(
    "Camera." + suffix,
    cfg["camera_type"], cfg["camera_scale"],
    cfg["camera_loc"], cfg["camera_rot"],
    layer=LAYER_SHARED,
  )
  scene.camera = cam_obj

  _create_lamp(
    "Lamp." + suffix + ".key.shadow",
    cfg["key_energy"], cfg["key_loc"], cfg["key_rot"],
    shadow_method="RAY_SHADOW", layer=game_layer,
  )

  if cfg["fill_energy"] > 0:
    _create_lamp(
      "Lamp." + suffix + ".fill",
      cfg["fill_energy"], cfg["fill_loc"], cfg["fill_rot"],
      shadow_method="NOSHADOW", layer=game_layer,
    )

  if cfg["rim_energy"] > 0:
    _create_lamp(
      "Lamp." + suffix + ".rim",
      cfg["rim_energy"], cfg["rim_loc"], cfg["rim_rot"],
      shadow_method="NOSHADOW", layer=game_layer,
    )

  blue_mat = _make_blue(suffix)
  grey_mat = _make_grey(suffix)
  ambient_mat = _make_ambient(suffix)
  holdout_mat = _make_holdout(suffix)
  shadow_mat = _make_shadow(suffix)

  _create_plane("Plane.blue." + suffix, (0, 0, -0.0001), blue_mat, hide_render=True, layer=LAYER_SHARED)
  _create_plane("Plane.grey." + suffix, (0, 0, -0.0001), grey_mat, hide_render=False, layer=LAYER_SHARED)
  _create_plane("Plane.ambient." + suffix, (0, 0, -20), ambient_mat, hide_render=True, layer=LAYER_SHARED)
  _create_plane("Plane.holdout." + suffix, (0, 0, -0.015), holdout_mat, hide_render=True, layer=LAYER_SHARED)
  _create_plane("Plane.shadow." + suffix, (0, 0, -0.01), shadow_mat, hide_render=True, layer=LAYER_SHARED)

  _create_compositor(scene)

  return scene
