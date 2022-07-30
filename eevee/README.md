# blender-cnc-templates

CnC Cycles/Eevee Template version 1.00 alpha 1 for Blender 2.8/2.9
Created by: Ari Oravasaari / DonutArnold / Zawaro
Contact: Personal message 'donutarnold' in PPMSite.com or email: donutarnold@gmail.com

---------------------
- TABLE OF CONTENTS -
---------------------
    
1.  Introduction

2.  How to use
    2.1  Basics
    2.2  Animations
    2.3  Scale output canvas
    2.4  Cell heights
    2.5  Render Quality

3.  Version history

4.  Licence / Terms of usage

5.  Credits / Thanks


-------------------
- 1. INTRODUCTION -
-------------------

This is currently one and the only public Blender template to render assets for Classic Command & Conquer games.
I've created this template because of the sudden interest towards Blender which is a great open-source 3d modeling software.
Anyone having an interest to create assets for C&C games may not afford commercial software such as 3ds max or Maya.
That's why I created this template for the community needs.

After Blender 2.80 Beta release, I started to re-build the template. The plan is to support Eevee and Cycles simultaneously.
You can choose the correct rendering method (Cycles or Eevee / Object, Buildup, Shadow, Preview or Reset) from Text Editor and hit Run Script.

I am trying to update this template frequently and your feedback and suggestions are more than welcome.

Happy rendering!

Note: To make this readme not to appear like this when opening the template .blend file, just scale it down and save.


-----------------
- 2. HOW TO USE -
-----------------

2.1 BASICS

    1. Select correct template scene (Tiberian Sun or Red Alert 2 or Red Alert / Tiberian Dawn or Dune 2000) from top bar/Info editor.
    2. To import model press Shift+F1 and open a .blend file and then 'Object' sub-folder and select everything except camera and lights.
    3. Move the model so its (top)corner is at zero-point.
    4. Select Text Editor from current editor menu.
    5. Select wanted script form text data block and press 'Run Script'. (Note: If you switch between scenes you need to run the script again.)
    6. Press F10 to render.


2.2 ANIMATIONS

In Blender you cannot set custom file frame numbers so you need to render animations by following method:

    This method uses Blender Video Editor and at the beginning renders animations separately and finally combines them:
    1. Set Frame Range to render non-shadow frames.
    2. Set path an output path.
    3. Run 'Render.object' or 'Render.buildup' script
    4. Hit Render Animation
    5. Run 'Render.shadows' script.
    6. Set another output path.
    7. Hit Render Animation
    8. Select 'Video Editing' Screen Layout
    9. Add both image sequences in the sequencer, shadow frames after the non-shadow frames.
    10. Set final output path.
    11. Set Frame Range to match the whole animation.
    12. Hit Render Animation.

    OR

    This method duplicates frames and renders the animation as whole:
    1. Set Frame Range to render non-shadow frames.
    2. Set path an output path.
    3. Run 'Render.object' or 'Render.buildup' script
    4. Hit Render Animation
    5. Move or clone animated frames after the non-shadow frames.
    6. Run 'Render.shadows' script.
    7. Change Frame Range to match shadow frames.
    8. Hit Render Animation.
    
Note: To scale output canvas while rendering in Blender, check the next part "2.3 SCALE CANVAS".


2.3 SCALE CANVAS
    
This template has an ability to scale output canvas and render it that way to save (a lot of)
time (otherwise you'd have to use 3rd party software to batch scale canvas).

Normally when you set a mask node and mix it to compose and hit render it ignores the canvas scale.
Currently there's no script made to make it for you, so you need to do it by yourself.
It renders the filename as Image0000.png which is combatiable with SHP Builder and XCC Mixer.

    1. Go to Node Editor.
    2. Insert wanted canvas size to Mask node.
    3. Connect the last Mix node on the right to File Output.
    4. Set File Output path to where you want your frames to be rendered.
    5. Hit render
    
Note: It also creates duplicate renders into a folder which path is set in Render tab (default: /tmp\).
      To save HDD space, check Placeholder in Render tab.
      Use even number value, odd number value will produce blur render result.


2.4 CELL HEIGHTS

These are the cell heights / Z coords:
    0 = 0 BUs
    1 = 0.816625 BUs
    2 = 1.63325 BUs
    3 = 2.449875 BUs
    4 = 3.2665 BUs (Default cliff height)
    
*BUs = Blender units


2.5 RENDER QUALITY

Cycles requires more time to render than Blender Render engine because it's totally different render engine.
I've set default value to 25 so it won't take too long time to render, but still renders with ok quality.
To change the sampling value:
    
    1. Go to Render tab
    2. Expand Sampling
    3. Set "Samples: Render:" higher, eg. 100 samples starts to produce quite good render result


2.6 PERFORMANCE

Render time may vary depending on what kind of hardware your PC has. 
I've set default values to match my hardware and to give the fastest and best result.
If you are able to use GPU to render make sure you are enabled GPU settings in User Preferences...
If you can't use GPU to render set following settings:
    
    1. Go to Render tab
    2. Expand Render and set Device to CPU
    3. Expand Performance and set Tiles to 16x16


-----------------------
- 3. ADDITIONAL TOOLS -
-----------------------

3.1 REAL SNOW BY 3D-WOLF

A great tool to create snow frames. It's easy, fast and produces really nice result.
After creating the snow mesh, you can use Decimate Modifier to drop polycount.

Download: https://3d-wolf.com/products/snow


3.2 CELL FRACTURE BY ideasman42, phymec, Sergey Sharybin

This is an embedded Blender Add-On you can enable in Preferences.
It helps you to create nice damage frames for buildings.


----------------------
- 4. VERSION HISTORY -
----------------------

1.00 alpha 1
-Rewritten templates as python scripts


-------------------------------
- 5: LICENCE / TERMS OF USAGE -
-------------------------------

You are freely to make changes of this template to match your needs. 
You can use scene settings as a reference to create your own templates. 
You can distribute the template with your changes (please let me know what kind of changes you've done, I'm curious ;) .) 
Please credit when used (optional).


-----------------------
- 6. CREDITS / THANKS -
-----------------------

I'd like to thank following people / community for feedback, testing, inspirations etc.:
    
PPMSite (https://www.ppmsite.com/)
Banshee
tomsons26
LKO
Nolt
BySc
DaFool
Palkia323
Apollo
Darkstorm 
Blade 
Phrohdoh 
Zengar_Zombolt 
Chrono2 
HG_SCIPCION 
PillBox20 
Agent Z
cookie110 
deathreaperz 
PussyPus 
Kamuix 
ReFlex 
Mig Eater
Gangster
E1 Elite
Orac
Grantelbart 
FekLeyrTarg 
TAK02 
4StarGeneral 
Nooze
...and many more.
