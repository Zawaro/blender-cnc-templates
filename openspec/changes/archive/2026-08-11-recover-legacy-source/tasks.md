## 1. Propose extrapolated configs

- [x] 1.1 Propose RM/D2K camera + lamp configs (mirror RA2/TS template) and FX variant convention (lower-res) for user review
- [x] 1.2 Confirm scene naming (codebase `SCENE_SUFFIX_MAP` convention vs `.blend` names)

## 2. Data model (GAME_CONFIGS)

- [x] 2.1 Read current `legacy/scene_builder.py` and map existing `GAME_CONFIGS` against the recovery report
- [x] 2.2 Add recovered camera/plane/lamp data for TD/RA1, RA2, RA2-INF, TS, TS-INF (exact values: transforms, lens/ortho, energies, shadow methods, plane scales/rotations)
- [x] 2.3 Add extrapolated RM, D2K, and FX configs
- [x] 2.4 Add per-scene render + render-layer settings (engine, 640×480, AA 11, MITCHELL 1.5, alpha TRANSPARENT, PNG/RGB/8, pass flags incl. per-scene `use_pass_material_index`)

## 3. Render setup

- [x] 3.1 Implement scene render configuration (engine, sampling, filter, alpha mode, image settings) in `scene_builder.py`
- [x] 3.2 Implement render-layer pass flag setup (index/z/ao + per-scene material_index), all objects on layer 0
- [x] 3.3 Implement world creation (blue horizon + AO RAYTRACE/5/distance 10, factor 0.25 base / 0.75 INF/FX) in `world_materials.py`

## 4. Materials & planes

- [x] 4.1 Rebuild `plane_materials.py` for the 12 recovered materials (blue emit 0.28 + spec variants, grey 0.4/0.4/0.4 emit 0.28, grass + CLOUDS texture, `Hiding Blue` MASK/use_raytrace False); drop unbound grey IMAGE slots
- [x] 4.2 Implement plane creation with recovered transforms (blue hidden / grey visible / grass hidden in TD), no ambient/holdout/shadow planes
- [x] 4.3 Verify material/texture slots against recovery report (CLOUDS WINDOW/FLAT, CELL_NOISE, depth 2, scale 0.005)

## 5. Compositor

- [x] 5.1 Add `legacy/compositor.py` (data-driven node graph: RLayers→PremulKey→Switch, IDMask→ColorRamp→Mix, Gamma, Hue/Sat, Math GREATER_THAN, Combine RGBA, MULTIPLY shadow mixes, Image node, File Output)
- [x] 5.2 Wire per-scene compositor parameters (Gamma 1.2–1.4, sat 1.05–1.1, ColorRamp positions, shadow-mix factors 0.2–0.5); Image node unbound when `RA2_LAT01.png` missing
- [x] 5.3 Apply `shared/node_arrange.py` to layout each node tree; skip REROUTEs/Frames/empty Mask

## 6. Scripts

- [x] 6.1 Port the 5 recovered text blocks (Readme + Render.buildup/object/reset/shadows) into `generate_scripts.py` as `.txt` outputs
- [x] 6.2 Verify script content/toggles (transparency, hide_render, pass_index 0↔1, AO, Switch.check) match the recovered blocks

## 7. main.py wiring

- [x] 7.1 Update `legacy/main.py` to create all 6 games × base/INF/FX scenes, load scripts, setup text editor, save

## 8. Verify against source

- [x] 8.1 Build with Blender 2.79; dump `bpy.data` of rebuilt scenes and diff against the original `.blend` dump for the 5 recovered games
- [x] 8.2 Render spot-check recovered scenes for parity
- [x] 8.3 Run `uv run ruff check .` and existing test suite (non-bpy tier)
- [x] 8.4 Run `openspec validate --all`
