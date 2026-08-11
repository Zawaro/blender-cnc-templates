# Per-game compositor parameters recovered from CnC_template2_11.blend.
# `id_ramp` is the ID-mask -> blue ColorRamp stop positions, `shadow` is the
# MULTIPLY factor applied to the gamma'd render vs AO, `shadow2` is the extra
# MULTIPLY factor for the shadow pass (INF scenes only).
COMPOSITOR_CONFIG = {
  "RA1": {"gamma": 1.2, "sat": 1.05, "id_ramp": (0.2330, 0.2381), "shadow": 0.5, "shadow2": None},
  "RA2": {"gamma": 1.3, "sat": 1.1, "id_ramp": (0.3045, 0.3136), "shadow": 0.5, "shadow2": None},
  "RA2_INF": {"gamma": 1.3, "sat": 1.1, "id_ramp": (0.3050, 0.3060), "shadow": 0.5, "shadow2": 0.2},
  "TS": {"gamma": 1.3, "sat": 1.1, "id_ramp": (0.3270, 0.3280), "shadow": 0.25, "shadow2": None},
  "TS_INF": {"gamma": 1.4, "sat": 1.1, "id_ramp": (0.3270, 0.3280), "shadow": 0.5, "shadow2": 0.4},
  # Extrapolated (no source data): mirror the RA2/RA1 template
  "RW": {"gamma": 1.3, "sat": 1.1, "id_ramp": (0.3045, 0.3136), "shadow": 0.5, "shadow2": None},
  "RM": {"gamma": 1.2, "sat": 1.05, "id_ramp": (0.2330, 0.2381), "shadow": 0.5, "shadow2": None},
  "D2K": {"gamma": 1.3, "sat": 1.1, "id_ramp": (0.3045, 0.3136), "shadow": 0.5, "shadow2": None},
}

DEFAULT_COMPOSITOR = COMPOSITOR_CONFIG["RA2"]


def _config(game_key):
  return COMPOSITOR_CONFIG.get(game_key) or COMPOSITOR_CONFIG.get(game_key.split("_")[0], DEFAULT_COMPOSITOR)


def uses_shadow_pass(game_key):
  return _config(game_key)["shadow2"] is not None


def _ramp_two_stops(ramp, pos0, col0, pos1, col1):
  elements = ramp.color_ramp.elements
  elements[0].position = pos0
  elements[0].color = col0
  elements[1].position = pos1
  elements[1].color = col1


def create_compositor(scene, game_key):
  scene.use_nodes = True
  tree = scene.node_tree
  nodes = tree.nodes
  links = tree.links

  for n in list(nodes):
    nodes.remove(n)

  cfg = _config(game_key)

  rl_main = nodes.new("CompositorNodeRLayers")
  rl_main.name = "Render Layers"
  rl_index = nodes.new("CompositorNodeRLayers")
  rl_index.name = "Render Layers.Index"

  premul_main = nodes.new("CompositorNodePremulKey")
  premul_main.name = "Alpha Convert"
  premul_main.mapping = "PREMUL_TO_STRAIGHT"
  premul_index = nodes.new("CompositorNodePremulKey")
  premul_index.name = "Alpha Convert.Index"
  premul_index.mapping = "PREMUL_TO_STRAIGHT"

  gamma = nodes.new("CompositorNodeGamma")
  gamma.name = "Gamma"
  gamma.inputs[1].default_value = cfg["gamma"]

  hue = nodes.new("CompositorNodeHueSat")
  hue.name = "Hue Saturation Value"
  hue.inputs[2].default_value = cfg["sat"]

  idmask = nodes.new("CompositorNodeIDMask")
  idmask.name = "ID Mask"
  idmask.index = 0
  idmask.use_antialiasing = False

  ramp_bluekey = nodes.new("CompositorNodeValToRGB")
  ramp_bluekey.name = "ColorRamp.BlueKey"
  _ramp_two_stops(ramp_bluekey, 0.0, (1.0, 1.0, 1.0, 1.0), 0.001, (0.0, 0.0, 1.0, 1.0))

  combine_black = nodes.new("CompositorNodeCombRGBA")
  combine_black.name = "Combine Black"
  combine_black.inputs[0].default_value = 0.0
  combine_black.inputs[1].default_value = 0.0
  combine_black.inputs[2].default_value = 0.0
  combine_black.inputs[3].default_value = 1.0

  mix_idcut = nodes.new("CompositorNodeMixRGB")
  mix_idcut.name = "Mix.IDCut"
  mix_idcut.blend_type = "MIX"

  ramp_idblue = nodes.new("CompositorNodeValToRGB")
  ramp_idblue.name = "ColorRamp.IDToBlue"
  _ramp_two_stops(ramp_idblue, cfg["id_ramp"][0], (0.0, 0.0, 0.0, 1.0), cfg["id_ramp"][1], (0.0, 0.0, 1.0, 1.0))

  combine_blue = nodes.new("CompositorNodeCombRGBA")
  combine_blue.name = "Combine Blue"
  combine_blue.inputs[0].default_value = 0.0
  combine_blue.inputs[1].default_value = 0.0
  combine_blue.inputs[2].default_value = 1.0
  combine_blue.inputs[3].default_value = 1.0

  math_alpha = nodes.new("CompositorNodeMath")
  math_alpha.name = "Math.Alpha"
  math_alpha.operation = "GREATER_THAN"
  math_alpha.inputs[0].default_value = 0.5
  math_alpha.inputs[1].default_value = 0.1

  mix_shadow = nodes.new("CompositorNodeMixRGB")
  mix_shadow.name = "Mix.Shadow"
  mix_shadow.blend_type = "MULTIPLY"
  mix_shadow.use_clamp = True
  mix_shadow.inputs[0].default_value = cfg["shadow"]

  mix_blueover = nodes.new("CompositorNodeMixRGB")
  mix_blueover.name = "Mix.BlueOver"
  mix_blueover.blend_type = "MIX"

  switch = nodes.new("CompositorNodeSwitch")
  switch.name = "Switch"
  switch.check = True

  image = nodes.new("CompositorNodeImage")
  image.name = "Image"

  alpha_over = nodes.new("CompositorNodeAlphaOver")
  alpha_over.name = "Alpha Over"
  alpha_over.use_premultiply = False

  composite = nodes.new("CompositorNodeComposite")
  composite.name = "Composite"
  viewer = nodes.new("CompositorNodeViewer")
  viewer.name = "Viewer"

  links.new(rl_main.outputs["Image"], premul_main.inputs[0])
  links.new(premul_main.outputs[0], gamma.inputs[0])
  links.new(gamma.outputs[0], hue.inputs[0])

  if cfg["shadow2"] is not None:
    mix_shadow2 = nodes.new("CompositorNodeMixRGB")
    mix_shadow2.name = "Mix.Shadow2"
    mix_shadow2.blend_type = "MULTIPLY"
    mix_shadow2.use_clamp = True
    mix_shadow2.inputs[0].default_value = cfg["shadow2"]
    links.new(hue.outputs[0], mix_shadow2.inputs[1])
    links.new(rl_main.outputs["Shadow"], mix_shadow2.inputs[2])
    links.new(mix_shadow2.outputs[0], mix_shadow.inputs[1])
  else:
    links.new(hue.outputs[0], mix_shadow.inputs[1])
  links.new(rl_main.outputs["AO"], mix_shadow.inputs[2])
  links.new(mix_shadow.outputs[0], mix_blueover.inputs[2])

  links.new(rl_main.outputs["Alpha"], math_alpha.inputs[0])
  links.new(combine_blue.outputs[0], mix_blueover.inputs[1])
  links.new(math_alpha.outputs[0], mix_blueover.inputs[0])
  links.new(mix_blueover.outputs[0], switch.inputs[1])

  links.new(rl_index.outputs["IndexOB"], idmask.inputs[0])
  links.new(idmask.outputs[0], ramp_bluekey.inputs[0])
  links.new(ramp_bluekey.outputs[0], combine_black.inputs[2])
  links.new(combine_black.outputs[0], mix_idcut.inputs[1])
  links.new(idmask.outputs[0], mix_idcut.inputs[0])
  links.new(rl_index.outputs["Image"], premul_index.inputs[0])
  links.new(premul_index.outputs[0], mix_idcut.inputs[2])
  links.new(mix_idcut.outputs[0], ramp_idblue.inputs[0])
  links.new(ramp_idblue.outputs[0], switch.inputs[0])

  links.new(switch.outputs[0], alpha_over.inputs[1])
  links.new(image.outputs[0], alpha_over.inputs[2])
  links.new(image.outputs[1], alpha_over.inputs[0])

  links.new(alpha_over.outputs[0], composite.inputs[0])
  links.new(alpha_over.outputs[0], viewer.inputs[0])
