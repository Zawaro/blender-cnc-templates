## ADDED Requirements

### Requirement: BLENDER_RENDER scenes for all games
The `legacy/` variant SHALL build `BLENDER_RENDER` scenes for 6 games (RA2, TS, RW, RA1, RM, D2K) × base/INF/FX. The 5 games present in the source `.blend` (TD/RA1, RA2, RA2-INF, TS, TS-INF) MUST reproduce the recovered scene content exactly; RM/D2K and FX variants follow the recovered pattern.

#### Scenario: recovered game scenes match the source
- **WHEN** the rebuilt RA1/RA2/RA2-INF/TS/TS-INF scenes are compared against `CnC_template2_11.blend`
- **THEN** cameras, lamps, planes, materials, worlds, and render settings match the recovered values

#### Scenario: all 18 scenes build
- **WHEN** `legacy/main.py` runs headless in Blender 2.79
- **THEN** 6 games × base/INF/FX scenes are created and a `.blend` is saved

### Requirement: Recovered render settings
Every scene MUST set engine `BLENDER_RENDER`, resolution 640×480@100%, anti-aliasing on with 11 samples, `pixel_filter_type='MITCHELL'` with `filter_size=1.5`, `alpha_mode='TRANSPARENT'`, and PNG/RGB/8-bit output. Render layers MUST enable `use_pass_object_index`, `use_pass_z`, `use_pass_ambient_occlusion`, and `use_ao`; `use_pass_material_index` SHALL be enabled only for TD/TS/TS-INF scenes.

#### Scenario: render configuration is applied
- **WHEN** a scene is created by the builder
- **THEN** `scene.render.engine`, sampling, filter, alpha mode, output format, and render-layer pass flags equal the recovered values

### Requirement: Worlds with ambient occlusion
Each scene SHALL have a world with blue horizon color and ambient occlusion enabled (`RAYTRACE`, 5 samples, distance 10). AO factor SHALL be 0.25 for base scenes and 0.75 for INF/FX scenes.

#### Scenario: world and AO are set
- **WHEN** a scene's world is inspected
- **THEN** horizon is blue, AO is on, and the factor matches the base/INF/FX rule

### Requirement: Cameras and lamps match recovered layout
Each scene SHALL create its recovered camera(s) — including RA1's PERSP + ORTHO pair (lens 27.7128, object scale 0.2749, ortho_scale 55.72) and the ORTHO RA2/TS cameras (ortho_scale 29.92 / 37.4) — and 3 lamps per game (`key.shadow` with `RAY_SHADOW`, `fill`, `rim`) with the recovered energies and rotations.

#### Scenario: camera and lamp transforms are applied
- **WHEN** a scene's camera and lamps are inspected
- **THEN** their types, transforms, lens/ortho settings, energies, and shadow methods equal the recovered values

### Requirement: Planes and materials match recovered layout
Each scene SHALL create the recovered plane set — blue (hidden from render) + grey (visible) for RA2/TS, plus a hidden grass plane in the TD scene — with the recovered scale/rotation/location (RA2/TS scale 35, TD scale 82.85×79×2.26, rotation −90°). Materials MUST reproduce the recovered 12 materials: blue (emit 0.28, spec 0.5 except RA1/TS.INF 0.0), grey (0.4/0.4/0.4, emit 0.28), grass (dark green, ambient 0.5, CLOUDS texture), and `Hiding Blue` (MASK transparency, `use_raytrace=False`).

#### Scenario: planes are placed with materials
- **WHEN** a scene's mesh objects are inspected
- **THEN** plane names, transforms, and material assignments match the recovered values

### Requirement: Functional-equivalent compositor
Each scene SHALL have the IDMask blue-screen compositor node graph with the recovered per-scene parameters (Gamma 1.2–1.4, Hue/Saturation 1.05–1.1, ColorRamp positions, MULTIPLY shadow-mix factors 0.2–0.5). Inert REROUTE/Frame nodes and the empty Mask node SHALL NOT be created. The Image node SHALL stay unbound when `RA2_LAT01.png` is missing without failing the build.

#### Scenario: compositor nodes match functionally
- **WHEN** a scene's node tree is inspected
- **THEN** all functional nodes and links exist with the recovered parameters, and no REROUTE/Frame nodes exist

### Requirement: Recovered scripts are generated
`generate_scripts.py` SHALL emit the 5 recovered text blocks as `.txt`: `Readme`, `Render.buildup`, `Render.object`, `Render.reset`, and `Render.shadows` (toggling transparency, `hide_render`, `pass_index` 0↔1, world AO, and the compositor `Switch.check`).

#### Scenario: scripts are produced and loaded
- **WHEN** scripts are generated and loaded into the saved `.blend`
- **THEN** the 5 text blocks exist with the recovered names and content
