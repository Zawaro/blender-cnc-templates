# future_five/scenes.py
"""
Scene helper module for Blender 5.0 (Future Five).

The module exposes two example scenes:
* ``default_scene`` – a simple world with camera, light and a cube.
* ``camera_only`` – a scene that only contains a camera and light.

Each function returns the name of the created objects so the build system can reference them,
and provides a lightweight cleanup helper that removes all objects belonging to the scene.
"""

import bpy
from typing import List


def _ensure_collection(name: str) -> None:
    """Return an existing collection or create it."""
    if name not in bpy.data.collections:
        bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(bpy.data.collections[name])


def default_scene() -> List[str]:
    """
    Create a basic scene with a camera, light and cube.

    Returns
    -------
    list of object names that were added.
    """
    _ensure_collection("Future5_Default")
    col = bpy.data.collections["Future5_Default"]

    # Clean any pre‑existing objects in the collection
    for obj in col.objects:
        col.objects.unlink(obj)

    objs: List[str] = []

    # Camera
    cam_data = bpy.data.cameras.new(name="Camera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    cam_obj.location = (0, -3, 1.5)
    cam_obj.rotation_euler = (1.10871, 0, 0)
    col.objects.link(cam_obj)
    objs.append(cam_obj.name)

    # Light
    light_data = bpy.data.lights.new(name="Light", type="POINT")
    light_obj = bpy.data.objects.new("Light", light_data)
    light_obj.location = (4, -3, 6)
    col.objects.link(light_obj)
    objs.append(light_obj.name)

    # Cube
    mesh = bpy.data.meshes.new(name="Cube")
    cube_obj = bpy.data.objects.new("Cube", mesh)
    bpy.context.scene.collection.objects.link(cube_obj)
    objs.append(cube_obj.name)

    return objs


def camera_only() -> List[str]:
    """
    Create a scene that contains only a camera and a point light.

    Returns
    -------
    list of object names that were added.
    """
    _ensure_collection("Future5_CameraOnly")
    col = bpy.data.collections["Future5_CameraOnly"]

    for obj in col.objects:
        col.objects.unlink(obj)

    objs: List[str] = []

    cam_data = bpy.data.cameras.new(name="Camera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    cam_obj.location = (0, -3, 1.5)
    col.objects.link(cam_obj)
    objs.append(cam_obj.name)

    light_data = bpy.data.lights.new(name="Light", type="POINT")
    light_obj = bpy.data.objects.new("Light", light_data)
    light_obj.location = (4, -3, 6)
    col.objects.link(light_obj)
    objs.append(light_obj.name)

    return objs


def cleanup_scene(collection_name: str) -> None:
    """
    Remove all objects that belong to the specified collection.

    Parameters
    ----------
    collection_name : str
        Name of the collection created by one of the scene helpers.
    """
    if collection_name not in bpy.data.collections:
        return

    col = bpy.data.collections[collection_name]
    for obj in list(col.objects):
        # Avoid deleting data blocks that are used elsewhere
        if obj.type == "CAMERA":
            continue
        if obj.type == "LIGHT":
            continue
        bpy.data.objects.remove(obj, do_unlink=True)
