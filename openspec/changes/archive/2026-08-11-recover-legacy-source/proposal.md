## Why

The `legacy/` variant (Blender Render engine, 2.79) is WIP and does not match the original template. The authoritative scene — `CnC_template2_11.blend` (2019, Blender 2.79) — exists only as a `.blend` file built by hand in the Blender GUI; its source was never ported to Python. The recovered data (render settings, worlds, cameras, lamps, planes, 12 materials, per-scene compositor, 5 embedded scripts) must become fully-fledged Python code so the variant is buildable like the other 6 variants.

## What Changes

- Rebuild `legacy/`'s `scene_builder.py` as a data-driven builder reproducing the recovered `BLENDER_RENDER` scene content for **6 games × base/INF/FX**.
- Recover exact render settings (640×480, AA 11, MITCHELL filter 1.5, alpha TRANSPARENT, PNG/RGB/8bit, render-layer passes), world AO (factor 0.25/0.75), cameras (incl. RA1's PERSP+ORTHO pair), 3 lamps/game, plane sets (blue/grey/grass), and the 12 materials (emit 0.28, spec variants, `Hiding Blue`, grass CLOUDS texture).
- Recreate the per-scene IDMask blue-screen compositor as a **functional equivalent** (skip inert REROUTEs/Frames/empty Mask).
- Emit the 5 recovered text scripts (`Readme`, `Render.buildup/object/reset/shadows`) via `generate_scripts.py`.
- RM/D2K scenes and FX variants are **extrapolated** from the recovered pattern (no source data exists).

## Capabilities

### New Capabilities
- `legacy-render-scenes`: the `legacy/` variant builds Blender-Render-Engine scenes (6 games × base/INF/FX) that reproduce the recovered `CnC_template2_11.blend` content — render settings, worlds, cameras, lamps, planes, materials, compositor, and scripts — as Python.

### Modified Capabilities

## Impact

- `legacy/scene_builder.py`, `legacy/plane_materials.py`, `legacy/world_materials.py`, `legacy/generate_scripts.py`, `legacy/main.py` (all rebuilt within `legacy/`)
- Possibly a new `legacy/compositor.py` (data-driven node graph)
- `shared/` and the other 6 variants untouched
- Reference data source (read-only): `/mnt/work2/Blender/Scenes/CnC_template2_11.blend`, verified with local Blender 2.79

## Non-goals

- Porting `legacy_cycles` (Cycles) or any other variant.
- Recovering the ~55 inert REROUTE nodes / Frame nodes / empty Mask per compositor (functional equivalent only).
- Reproducing orphaned data (`blood01`/`blood02`, unbound grey IMAGE texture slots, unused `NONE` world textures).
- Shipping the missing `RA2_LAT01.png` asset (handle missing images gracefully instead).
- Changing shared compat layer or render engines.
