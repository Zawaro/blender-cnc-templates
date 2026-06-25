from collections import OrderedDict
from itertools import repeat
import bpy

CYCLES = False
VRAY = not CYCLES

class values():
  average_y = 0
  x_last = 0
  margin_x = 200
  margin_y = 200

def arrange_nodes(materials):
  for mat in materials:
    nodes_iterate(mat)
    nodes_center(mat)

def outputnode_search(ntree):	 # return node/None
  
  outputnodes = []
  for node in ntree.nodes:
    if not node.outputs:
      for _input in node.inputs:
        if _input.is_linked:
          outputnodes.append(node)
          break

  #print ("outputnodes:",outputnodes)			  

  if not outputnodes:
    print("No output node found")
    return None
  return outputnodes

###############################################################
def nodes_iterate(ntree, arrange=True):

  nodeoutput = outputnode_search(ntree)
  if nodeoutput is None:
    #print ("nodeoutput is None")
    return None
  a = []
  a.append([])
  for i in nodeoutput:
    a[0].append(i)
  
  
  level = 0
    
  while a[level]:
    a.append([])
    #pprint.pprint (a)
    #print ("level:",level)
    
    for node in a[level]:
      #pdb.set_trace()
      #print ("while: level:", level)
      inputlist = [i for i in node.inputs if i.is_linked]
      #print ("inputlist:", inputlist)
      if inputlist:
                
        for _input in inputlist:
          for nlinks in _input.links:
            #dont add parented nodes (inside frame) to list
            #if not nlinks.from_node.parent:
            node1 = nlinks.from_node
            #print ("appending node:",node1)
            a[level + 1].append(node1)
      
      else:
        pass
        #print ("no inputlist at level:", level)

    level += 1
    
  #pprint.pprint(a)
  
  #delete last empty list
  del a[level]
  level -= 1
  
  #remove duplicate nodes at the same level, first wins
  for x, nodes in enumerate(a):
    a[x] = list(OrderedDict(zip(a[x], repeat(None))))
  #print ("Duplicate nodes removed")
  #pprint.pprint(a)
  
  #remove duplicate nodes in all levels, last wins
  top = level 
  for row1 in range(top, 1, -1):
    #print ("row1:",row1, a[row1])
    for col1 in a[row1]:
      #print ("col1:",col1)
      for row2 in range(row1-1, 0, -1):
        for col2 in a[row2]:
          if col1 == col2:
            #print ("Duplicate node found:", col1)
            #print ("Delete node:", col2)
            a[row2].remove(col2)
            break

  if not arrange:
    nodelist = [j for i in a for j in i]
    nodes_odd(ntree, nodelist=nodelist)
    return None

  ########################################
  
  levelmax = level + 1
  level = 0
  values.x_last = 0

  while level < levelmax:

    values.average_y = 0
    nodes = [x for x in a[level]]
    #print ("level, nodes:", level, nodes)
    nodes_arrange(nodes, level)
    
    level = level + 1

  return None


###############################################################
def nodes_odd(mat, nodelist):

  ntree = nodetree_get(mat)
  for i in ntree:
    i.select = False

  a = [x for x in ntree if x not in nodelist]
  # print ("odd nodes:",a)
  for i in a:
    i.select = True


def nodes_arrange(nodelist, level):

  parents = []
  for node in nodelist:
    parents.append(node.parent)
    node.parent = None
    bpy.context.space_data.node_tree.nodes.update()
    
    
  #print ("nodes arrange def")
  # node x positions

  widthmax = max([x.dimensions.x for x in nodelist])
  xpos = values.x_last - (widthmax + values.margin_x) if level != 0 else 0
  #print ("nodelist, xpos", nodelist,xpos)
  values.x_last = xpos

  # node y positions
  x = 0
  y = 0

  for node in nodelist:

    if node.hide:
      hidey = (node.dimensions.y / 2) - 8
      y = y - hidey
    else:
      hidey = 0

    node.location.y = y
    y = y - values.margin_y - node.dimensions.y + hidey

    node.location.x = xpos #if node.type != "FRAME" else xpos + 1200
    
  y = y + values.margin_y

  center = (0 + y) / 2
  values.average_y = center - values.average_y

  for node in nodelist:

    node.location.y -= values.average_y

  for i, node in enumerate(nodelist):
    node.parent =  parents[i]
    
def nodetree_get(mat):

  if VRAY:
    return mat.vray.ntree.nodes
  else:
    return mat.node_tree.nodes


def nodes_center(ntree):

  bboxminx = []
  bboxmaxx = []
  bboxmaxy = []
  bboxminy = []

  for node in ntree.nodes:
    if not node.parent:
      bboxminx.append(node.location.x)
      bboxmaxx.append(node.location.x + node.dimensions.x)
      bboxmaxy.append(node.location.y)
      bboxminy.append(node.location.y - node.dimensions.y)

  # print ("bboxminy:",bboxminy)
  bboxminx = min(bboxminx)
  bboxmaxx = max(bboxmaxx)
  bboxminy = min(bboxminy)
  bboxmaxy = max(bboxmaxy)
  center_x = (bboxminx + bboxmaxx) / 2
  center_y = (bboxminy + bboxmaxy) / 2

  for node in ntree.nodes:

    if not node.parent:
      node.location.x -= center_x
      node.location.y += -center_y
