import bpy

def Plane_Ambient(suffix):
  ambient_mat = bpy.data.materials.new(name="Plane.ambient."+suffix)
  ambient_mat.use_nodes = True
  ambient_mat.node_tree.nodes.remove(ambient_mat.node_tree.nodes['Principled BSDF'])
  output_node = ambient_mat.node_tree.nodes["Material Output"]
  lightpath_node = ambient_mat.node_tree.nodes.new('ShaderNodeLightPath')
  diffuse_node01 = ambient_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node01.inputs[0].default_value = (0.0193824, 0.0193824, 0.0193824, 1)
  diffuse_node01.inputs[1].default_value = 1
  diffuse_node02 = ambient_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse_node02.inputs[1].default_value = 1
  transparent_node = ambient_mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
  mixshader_node01 = ambient_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node02 = ambient_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node03 = ambient_mat.node_tree.nodes.new('ShaderNodeMixShader')
  holdout_node = ambient_mat.node_tree.nodes.new('ShaderNodeHoldout')
  ambient_mat.node_tree.links.new(mixshader_node03.outputs[0], output_node.inputs[0])
  ambient_mat.node_tree.links.new(holdout_node.outputs[0], mixshader_node03.inputs[2])
  ambient_mat.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node03.inputs[1])
  ambient_mat.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  ambient_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  ambient_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
  ambient_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
  ambient_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
  ambient_mat.node_tree.links.new(transparent_node.outputs[0], mixshader_node01.inputs[1])

  return ambient_mat

def Plane_Blue(suffix):
  blue_mat = bpy.data.materials.new(name="Plane.blue."+suffix)
  blue_mat.use_nodes = True
  blue_mat.node_tree.nodes.remove(blue_mat.node_tree.nodes['Principled BSDF'])
  output_node = blue_mat.node_tree.nodes["Material Output"]
  lightpath_node = blue_mat.node_tree.nodes.new('ShaderNodeLightPath')
  diffuse_node01 = blue_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse_node01.inputs[1].default_value = 1
  diffuse_node02 = blue_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse_node02.inputs[1].default_value = 1
  diffuse_node03 = blue_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node03.inputs[0].default_value = (0, 0, 1, 1)
  diffuse_node03.inputs[1].default_value = 0
  transparent_node = blue_mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
  mixshader_node01 = blue_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node02 = blue_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node03 = blue_mat.node_tree.nodes.new('ShaderNodeMixShader')
  blue_mat.node_tree.links.new(mixshader_node03.outputs[0], output_node.inputs[0])
  blue_mat.node_tree.links.new(diffuse_node03.outputs[0], mixshader_node03.inputs[2])
  blue_mat.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node03.inputs[1])
  blue_mat.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  blue_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  blue_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
  blue_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
  blue_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
  blue_mat.node_tree.links.new(transparent_node.outputs[0], mixshader_node01.inputs[1])

  return blue_mat

def Plane_Grey(suffix):
  grey_mat = bpy.data.materials.new(name="Plane.grey."+suffix)
  grey_mat.use_nodes = True
  grey_mat.node_tree.nodes.remove(grey_mat.node_tree.nodes['Principled BSDF'])
  output_node = grey_mat.node_tree.nodes["Material Output"]
  lightpath_node = grey_mat.node_tree.nodes.new('ShaderNodeLightPath')
  diffuse_node01 = grey_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse_node01.inputs[1].default_value = 1
  diffuse_node02 = grey_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse_node02.inputs[1].default_value = 1
  transparent_node = grey_mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
  mixshader_node01 = grey_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node02 = grey_mat.node_tree.nodes.new('ShaderNodeMixShader')
  grey_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  grey_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
  grey_mat.node_tree.links.new(transparent_node.outputs[0], mixshader_node01.inputs[1])
  grey_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
  grey_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
  grey_mat.node_tree.links.new(mixshader_node02.outputs[0], output_node.inputs[0])

  return grey_mat

def Plane_Holdout(suffix):
  holdout_mat = bpy.data.materials.new(name="Plane.holdout."+suffix)
  holdout_mat.use_nodes = True
  holdout_mat.node_tree.nodes.remove(holdout_mat.node_tree.nodes['Principled BSDF'])
  output_node = holdout_mat.node_tree.nodes["Material Output"]
  lightpath_node = holdout_mat.node_tree.nodes.new('ShaderNodeLightPath')
  diffuse_node01 = holdout_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse_node01.inputs[1].default_value = 1
  diffuse_node02 = holdout_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse_node02.inputs[1].default_value = 1
  transparent_node = holdout_mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
  mixshader_node01 = holdout_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node02 = holdout_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node03 = holdout_mat.node_tree.nodes.new('ShaderNodeMixShader')
  holdout_node = holdout_mat.node_tree.nodes.new('ShaderNodeHoldout')
  holdout_mat.node_tree.links.new(transparent_node.outputs[0], mixshader_node01.inputs[1])
  holdout_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
  holdout_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
  holdout_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  holdout_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
  holdout_mat.node_tree.links.new(lightpath_node.outputs[0], mixshader_node03.inputs[0])
  holdout_mat.node_tree.links.new(mixshader_node02.outputs[0], mixshader_node03.inputs[1])
  holdout_mat.node_tree.links.new(holdout_node.outputs[0], mixshader_node03.inputs[2])
  holdout_mat.node_tree.links.new(mixshader_node03.outputs[0], output_node.inputs[0])

  return holdout_mat

def Plane_Shadow(suffix):
  shadow_mat = bpy.data.materials.new(name="Plane.shadow."+suffix)
  shadow_mat.use_nodes = True
  shadow_mat.node_tree.nodes.remove(shadow_mat.node_tree.nodes['Principled BSDF'])
  output_node01 = shadow_mat.node_tree.nodes["Material Output"]
  output_node01.target = 'CYCLES'
  lightpath_node = shadow_mat.node_tree.nodes.new('ShaderNodeLightPath')
  diffuse_node01 = shadow_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  diffuse_node01.inputs[1].default_value = 1
  diffuse_node02 = shadow_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  diffuse_node02.inputs[1].default_value = 1
  transparent_node01 = shadow_mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
  mixshader_node01 = shadow_mat.node_tree.nodes.new('ShaderNodeMixShader')
  mixshader_node02 = shadow_mat.node_tree.nodes.new('ShaderNodeMixShader')
  shadow_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
  shadow_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
  shadow_mat.node_tree.links.new(transparent_node01.outputs[0], mixshader_node01.inputs[1])
  shadow_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
  shadow_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
  shadow_mat.node_tree.links.new(mixshader_node02.outputs[0], output_node01.inputs[0])
  output_node02 = shadow_mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
  output_node02.target = 'EEVEE'
  tex_coord_node = shadow_mat.node_tree.nodes.new('ShaderNodeTexCoord')
  value_node = shadow_mat.node_tree.nodes.new('ShaderNodeValue')
  value_node.outputs[0].default_value = 0.01
  multiply_node = shadow_mat.node_tree.nodes.new('ShaderNodeMixRGB')
  multiply_node.blend_type = 'MULTIPLY'
  multiply_node.inputs[0].default_value = 1
  gradient_node = shadow_mat.node_tree.nodes.new('ShaderNodeTexGradient')
  gradient_node.gradient_type = 'QUADRATIC_SPHERE'
  gamma01_node = shadow_mat.node_tree.nodes.new('ShaderNodeGamma')
  gamma01_node.inputs[1].default_value = 0.001
  diffuse_node03 = shadow_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node03.inputs[0].default_value = (1, 1, 1, 1)
  diffuse_node03.inputs[1].default_value = 0
  to_rgb_node = shadow_mat.node_tree.nodes.new('ShaderNodeShaderToRGB')
  rgb_to_bw_node = shadow_mat.node_tree.nodes.new('ShaderNodeRGBToBW')
  gamma02_node = shadow_mat.node_tree.nodes.new('ShaderNodeGamma')
  gamma02_node.inputs[1].default_value = 3.9
  colorramp_node = shadow_mat.node_tree.nodes.new('ShaderNodeValToRGB')
  colorramp_node.color_ramp.elements[1].position = 0.132
  mix_node = shadow_mat.node_tree.nodes.new('ShaderNodeMixRGB')
  mix_node.inputs[1].default_value = (0.431555, 0.431555, 0.431555, 1)
  greater_node = shadow_mat.node_tree.nodes.new('ShaderNodeMath')
  greater_node.operation = 'GREATER_THAN'
  greater_node.inputs[1].default_value = 0.1
  diffuse_node04 = shadow_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
  diffuse_node04.inputs[0].default_value = (0, 0, 0, 1)
  diffuse_node04.inputs[1].default_value = 0
  transparent_node02 = shadow_mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
  mixshader_node03 = shadow_mat.node_tree.nodes.new('ShaderNodeMixShader')
  shadow_mat.node_tree.links.new(tex_coord_node.outputs[3], multiply_node.inputs[1])
  shadow_mat.node_tree.links.new(value_node.outputs[0], multiply_node.inputs[2])
  shadow_mat.node_tree.links.new(multiply_node.outputs[0], gradient_node.inputs[0])
  shadow_mat.node_tree.links.new(gradient_node.outputs[0], gamma01_node.inputs[0])
  shadow_mat.node_tree.links.new(gamma01_node.outputs[0], mix_node.inputs[0])
  shadow_mat.node_tree.links.new(diffuse_node03.outputs[0], to_rgb_node.inputs[0])
  shadow_mat.node_tree.links.new(to_rgb_node.outputs[0], rgb_to_bw_node.inputs[0])
  shadow_mat.node_tree.links.new(rgb_to_bw_node.outputs[0], gamma02_node.inputs[0])
  shadow_mat.node_tree.links.new(gamma02_node.outputs[0], colorramp_node.inputs[0])
  shadow_mat.node_tree.links.new(colorramp_node.outputs[0], mix_node.inputs[2])
  shadow_mat.node_tree.links.new(mix_node.outputs[0], greater_node.inputs[0])
  shadow_mat.node_tree.links.new(greater_node.outputs[0], mixshader_node03.inputs[0])
  shadow_mat.node_tree.links.new(diffuse_node04.outputs[0], mixshader_node03.inputs[1])
  shadow_mat.node_tree.links.new(transparent_node02.outputs[0], mixshader_node03.inputs[2])
  shadow_mat.node_tree.links.new(mixshader_node03.outputs[0], output_node02.inputs[0])

  return shadow_mat
