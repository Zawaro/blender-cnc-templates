import bpy


def _remove_default_shader(mat):
  """Remove the default shader node (Principled BSDF in 2.80+, Diffuse BSDF in 2.79)."""
  nodes = mat.node_tree.nodes
  for name in ["Principled BSDF", "Diffuse BSDF"]:
    if name in nodes:
      nodes.remove(nodes[name])
      return


def _get_output_node(mat):
  """Get the Material Output node (name varies by Blender version)."""
  nodes = mat.node_tree.nodes
  for name in ["Material Output", "Output"]:
    if name in nodes:
      return nodes[name]
  return None


def Plane_Ambient(suffix):
  mat = bpy.data.materials.new(name="Plane.ambient." + suffix)
  mat.use_nodes = True
  _remove_default_shader(mat)
  output_node = _get_output_node(mat)
  lightpath_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
  diffuse01 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse01.inputs[0].default_value = (0.0193824, 0.0193824, 0.0193824, 1)
  diffuse01.inputs[1].default_value = 1
  diffuse02 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse02.inputs[1].default_value = 1
  transparent = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mix01 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix02 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix03 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  holdout = mat.node_tree.nodes.new("ShaderNodeHoldout")
  mat.node_tree.links.new(mix03.outputs[0], output_node.inputs[0])
  mat.node_tree.links.new(holdout.outputs[0], mix03.inputs[2])
  mat.node_tree.links.new(mix02.outputs[0], mix03.inputs[1])
  mat.node_tree.links.new(lightpath_node.outputs[0], mix03.inputs[0])
  mat.node_tree.links.new(lightpath_node.outputs[3], mix02.inputs[0])
  mat.node_tree.links.new(diffuse01.outputs[0], mix02.inputs[1])
  mat.node_tree.links.new(mix01.outputs[0], mix02.inputs[2])
  mat.node_tree.links.new(diffuse02.outputs[0], mix01.inputs[2])
  mat.node_tree.links.new(transparent.outputs[0], mix01.inputs[1])
  return mat


def Plane_Blue(suffix):
  mat = bpy.data.materials.new(name="Plane.blue." + suffix)
  mat.use_nodes = True
  _remove_default_shader(mat)
  output_node = _get_output_node(mat)
  lightpath_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
  diffuse01 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse01.inputs[1].default_value = 1
  diffuse02 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse02.inputs[1].default_value = 1
  diffuse03 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse03.inputs[0].default_value = (0, 0, 1, 1)
  diffuse03.inputs[1].default_value = 0
  transparent = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mix01 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix02 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix03 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mat.node_tree.links.new(mix03.outputs[0], output_node.inputs[0])
  mat.node_tree.links.new(diffuse03.outputs[0], mix03.inputs[2])
  mat.node_tree.links.new(mix02.outputs[0], mix03.inputs[1])
  mat.node_tree.links.new(lightpath_node.outputs[0], mix03.inputs[0])
  mat.node_tree.links.new(lightpath_node.outputs[3], mix02.inputs[0])
  mat.node_tree.links.new(diffuse01.outputs[0], mix02.inputs[1])
  mat.node_tree.links.new(mix01.outputs[0], mix02.inputs[2])
  mat.node_tree.links.new(diffuse02.outputs[0], mix01.inputs[2])
  mat.node_tree.links.new(transparent.outputs[0], mix01.inputs[1])
  return mat


def Plane_Grey(suffix):
  mat = bpy.data.materials.new(name="Plane.grey." + suffix)
  mat.use_nodes = True
  _remove_default_shader(mat)
  output_node = _get_output_node(mat)
  lightpath_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
  diffuse01 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse01.inputs[1].default_value = 1
  diffuse02 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse02.inputs[1].default_value = 1
  transparent = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mix01 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix02 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mat.node_tree.links.new(lightpath_node.outputs[3], mix02.inputs[0])
  mat.node_tree.links.new(diffuse01.outputs[0], mix02.inputs[1])
  mat.node_tree.links.new(transparent.outputs[0], mix01.inputs[1])
  mat.node_tree.links.new(diffuse02.outputs[0], mix01.inputs[2])
  mat.node_tree.links.new(mix01.outputs[0], mix02.inputs[2])
  mat.node_tree.links.new(mix02.outputs[0], output_node.inputs[0])
  return mat


def Plane_Holdout(suffix):
  mat = bpy.data.materials.new(name="Plane.holdout." + suffix)
  mat.use_nodes = True
  _remove_default_shader(mat)
  output_node = _get_output_node(mat)
  lightpath_node = mat.node_tree.nodes.new("ShaderNodeLightPath")
  diffuse01 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse01.inputs[1].default_value = 1
  diffuse02 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse02.inputs[1].default_value = 1
  transparent = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mix01 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix02 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix03 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  holdout = mat.node_tree.nodes.new("ShaderNodeHoldout")
  mat.node_tree.links.new(transparent.outputs[0], mix01.inputs[1])
  mat.node_tree.links.new(diffuse02.outputs[0], mix01.inputs[2])
  mat.node_tree.links.new(mix01.outputs[0], mix02.inputs[2])
  mat.node_tree.links.new(lightpath_node.outputs[3], mix02.inputs[0])
  mat.node_tree.links.new(diffuse01.outputs[0], mix02.inputs[1])
  mat.node_tree.links.new(lightpath_node.outputs[0], mix03.inputs[0])
  mat.node_tree.links.new(mix02.outputs[0], mix03.inputs[1])
  mat.node_tree.links.new(holdout.outputs[0], mix03.inputs[2])
  mat.node_tree.links.new(mix03.outputs[0], output_node.inputs[0])
  return mat


def Plane_Shadow(suffix):
  mat = bpy.data.materials.new(name="Plane.shadow." + suffix)
  mat.use_nodes = True
  _remove_default_shader(mat)

  # Cycles output
  output01 = _get_output_node(mat)
  if hasattr(output01, "target"):
    output01.target = "CYCLES"
  mix01 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  mix02 = mat.node_tree.nodes.new("ShaderNodeMixShader")
  lightpath = mat.node_tree.nodes.new("ShaderNodeLightPath")
  diffuse01 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse01.inputs[1].default_value = 1
  diffuse02 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse02.inputs[1].default_value = 1
  transparent01 = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")

  mat.node_tree.links.new(lightpath.outputs[3], mix02.inputs[0])
  mat.node_tree.links.new(diffuse01.outputs[0], mix02.inputs[1])
  mat.node_tree.links.new(transparent01.outputs[0], mix01.inputs[1])
  mat.node_tree.links.new(diffuse02.outputs[0], mix01.inputs[2])
  mat.node_tree.links.new(mix01.outputs[0], mix02.inputs[2])
  mat.node_tree.links.new(mix02.outputs[0], output01.inputs[0])

  # Eevee output (2.80+ only)
  try:
    output02 = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    if hasattr(output02, "target"):
      output02.target = "EEVEE"
    mix03 = mat.node_tree.nodes.new("ShaderNodeMixShader")
    principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    principled.inputs[0].default_value = (0.371235, 0.371238, 0.371238, 0)
    try:
      principled.inputs[2].default_value = 0.0
    except (TypeError, ValueError):
      principled.inputs[2].default_value = (0, 0, 0)
    transparent02 = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    shader_to_rgb = mat.node_tree.nodes.new("ShaderNodeShaderToRGB")
    diffuse03 = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse03.inputs[0].default_value = (0, 0, 0, 1)
    diffuse03.inputs[1].default_value = 0

    mat.node_tree.links.new(principled.outputs[0], shader_to_rgb.inputs[0])
    mat.node_tree.links.new(shader_to_rgb.outputs[0], mix03.inputs[0])
    mat.node_tree.links.new(diffuse03.outputs[0], mix03.inputs[1])
    mat.node_tree.links.new(transparent02.outputs[0], mix03.inputs[2])
    mat.node_tree.links.new(mix03.outputs[0], output02.inputs[0])
  except (RuntimeError, KeyError):
    pass

  return mat
