import bpy


def _clear_nodes(mat):
    mat.use_nodes = True
    for node in list(mat.node_tree.nodes):
        mat.node_tree.nodes.remove(node)
    output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    output.location = (0, 0)
    return output


def Plane_Ambient(suffix):
    ambient_mat = bpy.data.materials.new(name="Plane.ambient." + suffix)
    output_node = _clear_nodes(ambient_mat)
    lightpath_node = ambient_mat.node_tree.nodes.new("ShaderNodeLightPath")
    diffuse_node01 = ambient_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node01.inputs[0].default_value = (0.0193824, 0.0193824, 0.0193824, 1)
    diffuse_node01.inputs[1].default_value = 1
    diffuse_node02 = ambient_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
    diffuse_node02.inputs[1].default_value = 1
    transparent_node = ambient_mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    mixshader_node01 = ambient_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node02 = ambient_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node03 = ambient_mat.node_tree.nodes.new("ShaderNodeMixShader")
    holdout_node = ambient_mat.node_tree.nodes.new("ShaderNodeHoldout")
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
    blue_mat = bpy.data.materials.new(name="Plane.blue." + suffix)
    output_node = _clear_nodes(blue_mat)
    lightpath_node = blue_mat.node_tree.nodes.new("ShaderNodeLightPath")
    diffuse_node01 = blue_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
    diffuse_node01.inputs[1].default_value = 1
    diffuse_node02 = blue_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
    diffuse_node02.inputs[1].default_value = 1
    diffuse_node03 = blue_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node03.inputs[0].default_value = (0, 0, 1, 1)
    diffuse_node03.inputs[1].default_value = 0
    transparent_node = blue_mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    mixshader_node01 = blue_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node02 = blue_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node03 = blue_mat.node_tree.nodes.new("ShaderNodeMixShader")
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
    grey_mat = bpy.data.materials.new(name="Plane.grey." + suffix)
    output_node = _clear_nodes(grey_mat)
    lightpath_node = grey_mat.node_tree.nodes.new("ShaderNodeLightPath")
    diffuse_node01 = grey_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
    diffuse_node01.inputs[1].default_value = 1
    diffuse_node02 = grey_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
    diffuse_node02.inputs[1].default_value = 1
    transparent_node = grey_mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    mixshader_node01 = grey_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node02 = grey_mat.node_tree.nodes.new("ShaderNodeMixShader")
    grey_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
    grey_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
    grey_mat.node_tree.links.new(transparent_node.outputs[0], mixshader_node01.inputs[1])
    grey_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
    grey_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
    grey_mat.node_tree.links.new(mixshader_node02.outputs[0], output_node.inputs[0])

    return grey_mat


def Plane_Holdout(suffix):
    holdout_mat = bpy.data.materials.new(name="Plane.holdout." + suffix)
    output_node = _clear_nodes(holdout_mat)
    lightpath_node = holdout_mat.node_tree.nodes.new("ShaderNodeLightPath")
    diffuse_node01 = holdout_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
    diffuse_node01.inputs[1].default_value = 1
    diffuse_node02 = holdout_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
    diffuse_node02.inputs[1].default_value = 1
    transparent_node = holdout_mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    mixshader_node01 = holdout_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node02 = holdout_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node03 = holdout_mat.node_tree.nodes.new("ShaderNodeMixShader")
    holdout_node = holdout_mat.node_tree.nodes.new("ShaderNodeHoldout")
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
    shadow_mat = bpy.data.materials.new(name="Plane.shadow." + suffix)
    output_node = _clear_nodes(shadow_mat)
    lightpath_node = shadow_mat.node_tree.nodes.new("ShaderNodeLightPath")
    diffuse_node01 = shadow_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node01.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
    diffuse_node01.inputs[1].default_value = 1
    diffuse_node02 = shadow_mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_node02.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
    diffuse_node02.inputs[1].default_value = 1
    transparent_node01 = shadow_mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    mixshader_node01 = shadow_mat.node_tree.nodes.new("ShaderNodeMixShader")
    mixshader_node02 = shadow_mat.node_tree.nodes.new("ShaderNodeMixShader")
    shadow_mat.node_tree.links.new(lightpath_node.outputs[3], mixshader_node02.inputs[0])
    shadow_mat.node_tree.links.new(diffuse_node01.outputs[0], mixshader_node02.inputs[1])
    shadow_mat.node_tree.links.new(transparent_node01.outputs[0], mixshader_node01.inputs[1])
    shadow_mat.node_tree.links.new(diffuse_node02.outputs[0], mixshader_node01.inputs[2])
    shadow_mat.node_tree.links.new(mixshader_node01.outputs[0], mixshader_node02.inputs[2])
    shadow_mat.node_tree.links.new(mixshader_node02.outputs[0], output_node.inputs[0])

    return shadow_mat
