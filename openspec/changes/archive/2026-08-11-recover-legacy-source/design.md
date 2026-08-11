## Context

The `legacy/` variant targets Blender 2.79 with the `BLENDER_RENDER` engine and has its own builder (`scene_builder.py`, `plane_materials.py`, `world_materials.py`, `compat.py`) — it does not use `shared/scenes.py`. The authoritative source is `CnC_template2_11.blend` (2019-04-05, Blender 2.79), extracted read-only with the local Blender 2.79 binary (`/home/ari/blender/stable/blender-2.79.0-b+stable.f4dc9f9d68b/blender`). The `.blend` contains 5 scenes (TD/RA1, RA2, RA2-INF, TS, TS-INF), all on layer 0, with exact render/world/camera/lamp/plane/material/compositor values recovered (full recovery report in the extraction). Existing `legacy_cycles/` demonstrates the data-driven pattern to mirror.

## Goals / Non-Goals

**Goals:**
- `legacy/` produces 6 games × base/INF/FX `BLENDER_RENDER` scenes reproducing the recovered `.blend` values for the 5 games it contains.
- Render output of the recovered scenes matches the original (functional compositor equivalence).
- Materials, textures, lamps, cameras, planes, worlds match the recovered data.
- The 5 embedded text scripts are regenerated as `.txt`.

**Non-Goals:**
- Pixel-faithful compositor (no REROUTEs/Frames/empty Mask).
- Porting other variants or touching `shared/`.
- Reproducing orphaned/unbound data.

## Decisions

### D1. Data-driven GAME_CONFIGS covering 6 games × base/INF/FX
Extend the existing `GAME_CONFIGS` shape: each game defines cameras, lamps, planes, materials, render/render-layer settings. The 5 recovered games use exact `.blend` values. RM/D2K mirror the RA2/TS template (ORTHO camera, 3 lamps, blue/grey planes). FX variants reuse the base config with an FX suffix and the lower-resolution convention used by the other variants.

### D2. Render + render-layer settings per scene
Set per scene: engine `BLENDER_RENDER`, 640×480@100%, AA on / `antialiasing_samples='11'`, `pixel_filter_type='MITCHELL'` / `filter_size=1.5`, `alpha_mode='TRANSPARENT'`, PNG/RGB/8bit/compression 90/quality 90, `use_compositing=True`, and render-layer flags (`use_pass_object_index`, `use_pass_z`, `use_pass_ambient_occlusion`, `use_ao`; `use_pass_material_index` only for TD/TS/TS-INF). All objects on layer 0 (no `layers_exclude`).

### D3. Functional-equivalent compositor as a data-driven module
New `legacy/compositor.py`: per-scene node graph described as data (nodes + links + params), created through `shared/node_arrange.py`. Includes: RLayers → PremulKey → Switch, IDMask → ColorRamp → Mix, Gamma (1.2–1.4), Hue/Sat (1.05–1.1), Math GREATER_THAN, Combine RGBA, MULTIPLY shadow mixes (fac 0.2–0.5), Image node (unbound when `RA2_LAT01.png` missing), File Output. Skips REROUTEs/Frames/empty Mask.
- Alternative considered: byte-faithful reproduction incl. REROUTEs — rejected for maintenance cost with identical output.

### D4. Materials reproduced from recovery data
`plane_materials.py` builds the 12 materials with exact values: blue (emit 0.28, spec 0.5 except RA1/TS.INF = 0.0), grey (0.4/0.4/0.4, emit 0.28, no texture slots), grass (green 0.074/0.095/0.058, ambient 0.5, CLOUDS texture WINDOW/FLAT GRAYSCALE CELL_NOISE depth 2 scale 0.005), `Hiding Blue` (MASK transparency, `use_raytrace=False`, ambient 1.0). All `use_nodes=False`. Unbound grey IMAGE slots dropped (render blank).

### D5. Scripts recovered as generated `.txt`
`generate_scripts.py` emits the 5 recovered texts: `Readme` (template docs) + `Render.buildup` / `Render.object` / `Render.reset` / `Render.shadows` — each toggles per-scene transparency / `hide_render` / `pass_index` (0↔1) / world AO / compositor `Switch.check`.

### D6. Missing image handled gracefully
`RA2_LAT01.png` does not exist. The compositor Image node stays unbound (like the RA2 scene in the original) and loading never fails. No asset shipped.

### D7. Verification against the source
Build with Blender 2.79; dump `bpy.data` of the rebuilt scene and diff against the original `.blend` dump (same read-only technique used for recovery). Render parity spot-check on the recovered games.

## Risks / Trade-offs

- [Extrapolated RM/D2K/FX configs may not match an unpublished original] → Flagged as invented values; user review before finalize; separate future fix if a source file appears.
- [Functional compositor output differs subtly from the original] → Diff bpy dumps + render spot-check during verification.
- [AA/filter or pass-flag differences are easy to miss in code] → Centralize in one render-setup function; verification diff catches it.
- [Blender 2.79 API quirks (e.g. `filter_size`, `pixel_filter_type` names) ] → Confirmed against 2.79 at extraction time; reference `compat_279.py`.
- [The 12 materials are shared globals; per-scene naming must stay consistent] → Follow the recovered `Plane.<color>.material.<game>` naming pattern.

## Migration Plan

Single commit-able change in `legacy/`; no schema/data migration. Rollback = revert the PR. Release pipeline unaffected (legacy builds via its own `main.py`).

## Open Questions

- Exact RM/D2K lamp rotations/camera placements (invented; propose before coding).
- FX variant resolution convention (match other variants' lower-res override).
- Scene naming: use `.blend` names (`Red Alert 2`) or the codebase's `SCENE_SUFFIX_MAP` convention — recommend the codebase convention for consistency.
