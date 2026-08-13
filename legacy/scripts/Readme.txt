# CnC Template version 2.11 rel. 05/04/2019 for Blender v2.77
# Created by: Ari Oravasaari / DonutArnold / Zawaro
# Contact: Personal message 'donutarnold' at PPMSite.com or email: donutarnold@gmail.com

# ---------------------
# - TABLE OF CONTENTS -
# ---------------------
    
# 1.  Introduction

# 2.  How to use
#     2.1  Basics
#     2.2  Animations
#     2.3  Scale output canvas
#     2.4  Cell heights
#     2.5  Shaper textures

# 3.  Version history

# 4.  Licence / Terms of usage


# -------------------
# - 1. INTRODUCTION -
# -------------------

# This is currently one and the only public Blender template to render assets for Classic Command & Conquer games.
# I've created this template because of the sudden interest towards Blender which is a great open-source 3d modeling software.
# Anyone having an interest to create assets for C&C games may not afford commercial software such as 3ds max or Maya.
# That's why I created this template for community needs.

# I am trying to update this template frequently and your feedback and suggestions are more than welcome.

# Note: To make this readme not to appear when opening the template .blend file, select 3d view from current editor menu and save.


# -----------------
# - 2. HOW TO USE -
# -----------------

# 2.1 BASICS

#     1. Select correct template scene (Tiberian Sun or Red Alert 2 or Red Alert / Tiberian Dawn) from top bar/Info editor.
#     2. To import model press Shift+F1 and open a .blend file and then 'Object' sub-folder and select everything except camera and lights.
#     3. Move the model so its (top)corner is at zero-point.
#     4. Select Text Editor from current editor menu.
#     5. Select wanted script form text data block and press 'Run Script'. (Note: If you switch between scenes you need to run the script again.)
#     6. Press F10 to render.


# 2.2 ANIMATIONS

# In Blender you cannot set custom file frame numbers so you need to render animations by following method:

#     This method uses Blender Video Editor and at the beginning renders animations separately and finally combines them:
#     1. Set Frame Range to render non-shadow frames.
#     2. Set path an output path.
#     3. Run 'Render.object' or 'Render.buildup' script
#     4. Hit Render Animation
#     5. Run 'Render.shadows' script.
#     6. Set another output path.
#     7. Hit Render Animation
#     8. Select 'Video Editing' Screen Layout
#     9. Add both image sequences in the sequencer, shadow frames after the non-shadow frames.
#     10. Set final output path.
#     11. Set Frame Range to match the whole animation.
#     12. Hit Render Animation.

#     OR

#     This method duplicates frames and renders the animation as whole:
#     1. Set Frame Range to render non-shadow frames.
#     2. Set path an output path.
#     3. Run 'Render.object' or 'Render.buildup' script
#     4. Hit Render Animation
#     5. Move or clone animated frames after the non-shadow frames.
#     6. Run 'Render.shadows' script.
#     7. Change Frame Range to match shadow frames.
#     8. Hit Render Animation.
    
# Note: To scale output canvas while rendering in Blender, check the next part "2.3 SCALE CANVAS".


# 2.3 SCALE CANVAS
    
# This template has an ability to scale output canvas and render it that way to save (a lot of)
# time (otherwise you'd have to use 3rd party software to batch scale canvas).

# Normally when you set a mask node and mix it to compose and hit render it ignores the canvas scale.
# Currently there's no script made to make it for you, so you need to do it by yourself.
# It renders the filename as Image0000.png which is combatiable with SHP Builder and XCC Mixer.

#     1. Go to Node Editor.
#     2. Insert wanted canvas size to Mask node.
#     3. Connect the last Mix node on the right to File Output.
#     4. Set File Output path to where you want your frames to be rendered.
#     5. Hit render
    
# Note: It also creates duplicate renders into a folder which path is set in Render tab (default: /tmp\).
#       To save HDD space, check Placeholder in Render tab.


# 2.4 CELL HEIGHTS

# These are the cell heights / Z coords:
#     0 = 0 BUs
#     1 = 0.816625 BUs
#     2 = 1.63325 BUs
#     3 = 2.449875 BUs
#     4 = 3.2665 BUs (Default cliff height)
    
# *BUs = Blender units


# 2.5 SHARPER TEXTURES

# By default Blender has a bit blurry texture filter which makes some texture details hard to see.
# This can be fixed by setting all your texture 'Filter Size:' to 0.6 in Texture > Image Sampling.


# 2.6 INFANTRY MATERIALS

# Infantry in RA2 has been rendered with falloff effect. Blender normally doesn't allow falloff to be added from Materials tab.
# You need to add it manually via nodes. Example: http://www.ppmforums.com/files/falloff_nodes_109.png


# ----------------------
# - 3. VERSION HISTORY -
# ----------------------

# 2.11
# -Fixed run script error caused by wrongly named Switch node

# 2.10
# -Added nodes what can be used to mix & crop terrain tiles with a custom image (works with Mask and Output nodes)
# -Fixed edge crop against background which previously resulted bad bad anti-aliasing with Alpha Convert
# -Fixed Hiding Blue material which was broken and provided really bad blue anti-aliasing on edges
# -Reorganized the nodes a bit

# 2.09
# -Improved lighting settings in RA, RA2 and TS scenes (experimental 3-point lighting) which provides more contrast and smoother shadow transition (especially with sphere objects)

# 2.08
# -Cleaned Outliner list from unused lights
# -Cleaned Material list from junk materials
# -Added Text Editor to Default screen layout, so you can run render scripts faster
# -Added Tiberian Sun - Infantry scene that allows to render infantry with correct TS lighting (shadows)

# 2.07
# -Added Red Alert 2 - Infantry scene that allows to render infantry with RA2 lighting (shadows)

# 2.06
# -Fixed lighting/shadow density in all scenes
# -Improved Render.buildup edge (doesn't cut too much detail anymore)
# -Removed AO on grey and blue planes

# 2.05
# -Dramatically improved and optimized lighting, AO and shadows in all scenes

# 2.04
# -Optimized lighting in all scenes, also turned off AO in shadow rendering
# -Dramatically improved lighting in RA2 scene

# 2.03
# -Fixed lighting settings in all scenes, caused bland contrast (needs more testing!)

# 2.02
# -Added mask node to scale canvas
# -Cleaned readme file
# -Fixed shadow rendering nodes

# 2.01
# -Added RA1/TD template
# -Added grass plane for RA1/TD template
# -Added an additional orthographic camera for RA1/TD terrain rendering (can be switched in Scene tab)
# -Fixed lighting overlapping other scenes

# 2.00
# -Combined TS & RA2 templates

# 1.07
# -Last individual template release.
# -Fixed lighting
# -Added new lightspot which creates negative light from top to create similar result than original TS assets.
# -Changed current Render.object script to Render.buildup because it cuts out too much edge detail, but is still useful for buildups.
# -Added new render option Render.object which has disabled AA against background which is similar to 3ds max template rendering.

# 1.06
# -Fixed ColorRamp node's value to make shadows single coloured
# -Reduced Raytrace Samples to 5 to increase render speed (previous version had 15, but I don't see any significant difference)
# -Added cell height to text editor 

# 1.05
# -Fixed contrast node's place (was affecting background blue color)
# -Added Python scripts to skip few steps
# -Added grey plane to render preview images 

# 1.04
# -Added contrast node
# -Added switch which allows you to render between model and shadow (Switch on + Plane's Pass index: 1 = render model; switch off + Model's Pass index: 1 = render shadow)
# -Fixed lighting (now more similar to 3ds template)
# -Fixed camera position (dunno how I kind of screwed that, lol) 

# 1.02
# -Second release
# -Added plane that hides everything below z=0.

# 1.00
# -First release
# -Rendering between objects and shadows had be made manually (hide plane, turn off AA, etc.)


# -------------------------------
# - 4: LICENCE / TERMS OF USAGE -
# -------------------------------

# You are freely to make changes of this template to match your needs. 
# You can use scene settings as a reference to create your own templates. 
# You can distribute the template with your changes (please let me know what kind of changes you've done, I'm curious ;) .) 
# Please credit when used. 