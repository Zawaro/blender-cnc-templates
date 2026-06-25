# AGENTS.md

## Project summary

Generates `.blend` scene templates for multiple Blender versions (2.79–5.1). Each variant is isolated in its own folder. Output goes to `release/{variant}/`.

## Directory structure

```
{variant}/               # One per Blender target
  constants.py           # TEMPLATE_PREFIX, TEMPLATE_VARIANT
  main.py                # ~20 lines: compat setup + scene creation + save .blend
  generate_scripts.py    # ~5 lines: delegates to shared/script_gen.py
  world_materials.py     # (eevee, legacy_eevee, legacy_cycles only) variant-specific world materials
  scripts/               # Generated .txt scripts (gitignored)
  requirements.txt
  README.md

  legacy/ is unique: has its own scene_builder.py, plane_materials.py,
  compat.py, world_materials.py — does NOT use shared/scenes.py.
  legacy_cycles/ has a local plane_materials.py.
shared/
  compat.py              # BaseCompat interface + get_compat() factory
  compat_279.py          # Blender 2.79 adapters
  compat_280.py          # Blender 2.80–2.92 adapters
  compat_293.py          # Blender 2.93 adapters (CryptomatteV2 + Shader to RGB)
  compat_300.py          # Blender 3.0 adapters
  compat_420.py          # Blender 4.2 adapters
  compat_500.py          # Blender 5.0 adapters
  scenes.py              # BaseScene + all game classes (single copy)
  plane_materials.py     # Material factories (single copy)
  world_materials.py     # World material factories (single copy, compat-aware)
  scene_names.py         # SCENE_SUFFIX_MAP (single source of truth)
  script_gen.py          # Data-driven .txt script generator
  build_utils.py         # Load scripts into Blender + save .blend
  constants.py           # TEMPLATE_VERSION + filter width/size values
  node_arrange.py        # Auto-layout for Blender nodes
  node_arrange_legacy.py
tests/
  test_compat.py         # Compat layer interface compliance
  test_scene_names.py    # Scene name mapping completeness
  test_script_gen.py     # Script generation (no bpy needed)
  test_version.py        # Version single source of truth + env tests
  test_env.py            # .env format and build script tests
release/                 # Output .blend/.zip/.7z files (gitignored)
```

## Build commands

```sh
uv run ./build.sh       # Interactive: pick variant, auto-finds Blender, generates + renders
uv run python {variant}/generate_scripts.py   # Generate scripts only (no Blender needed)
uv run pytest tests/ -v                        # Run tests (no Blender needed)
```

`build.sh` flow: compute `BUILD_NUMBER` from `git rev-list --count HEAD` → select variant → find Blender executable → create per-variant `.venv` via `bootstrap.sh` if missing → `pip install` from `requirements.txt` → run `generate_scripts.py` → run Blender headless with `main.py` → archive to `.zip` + `.7z`.

`bootstrap.sh` creates `.venv` in each variant folder and installs `fake-bpy-module` for IDE autocomplete.

## Variants

| Variant | Blender | Compositing method | Notes |
|---------|---------|-------------------|-------|
| legacy | 2.79 | None (internal render) | Unique: own scene_builder.py, no shared/scenes.py |
| legacy_cycles | 2.79 | IDMask (Object Index) | Cycles only, Python 3.5 compat |
| legacy_eevee | 2.80–2.92 | ShadowLayer (2 view layers) | Eevee, no CryptomatteV2 |
| eevee | 2.93 | CryptomatteV2 | Eevee, needs 2.93+ |
| cyclesx | 3.0–3.6 | CryptomatteV2 | Cycles |
| eevee_next | 4.2–4.3 | CryptomatteV2 | Eevee Next |
| hi_five | 5.0–5.1 | CryptomatteV2 | Eevee Next |

## Version management

- `shared/constants.py` — single source of truth for `TEMPLATE_VERSION = "1.0.0"`
- Each variant's `constants.py` has `TEMPLATE_VARIANT` (matches folder name) and `TEMPLATE_PREFIX`
- `build.sh` computes `BUILD_NUMBER` from git commit count and exports it
- `shared/build_utils.py` reads `BUILD_NUMBER` from env: `{prefix}_{version}_build{number}_{date}.blend`
- Output goes to `release/{variant}/` subdirectories

## Architecture

### Compat layer

All Blender API differences across versions (2.79–5.1) are abstracted through `shared/compat.py`. Each variant has a compat class implementing the same interface:

- **Compositor access**: `scene.node_tree` (2.79–4.x) vs `scene.compositing_node_group` (5.0)
- **Node types**: `CompositorNodeSepHSVA` vs `CompositorNodeSeparateColor`, `CompositorNodeMixRGB` vs `ShaderNodeMix`
- **Node group I/O**: `inputs.new()` vs `interface.new_socket()`
- **Switch node toggle**: `.check` vs `.inputs[0].default_value`
- **Material transparency**: `blend_method`/`shadow_method` vs `surface_render_method`
- **Light creation**: `lamp_add` (2.79) vs `light_add` (2.80+)
- **Eevee settings**: GTAO/TAA/SSR (2.80–4.x) vs `use_shadows` only (5.0)
- **Cryptomatte**: `has_cryptomatte()` returns False for 2.79/2.80–2.92, True for 2.93+
- **Shader to RGB**: `has_shader_to_rgb()` returns False for 2.79/2.80–2.92, True for 2.93+

### Compositing (three methods)

`create_composite_nodes()` in `shared/scenes.py` uses a three-way branch:

1. **CryptomatteV2** (3.0+): `CompositorNodeCryptomatteV2` with `matte_id` matching shadow plane names
2. **ShadowLayer** (2.80–2.92): Two view layers — default excludes shadows, ShadowLayer renders only shadows. Uses `CompositorNodeRLayers` with `.layer = "ShadowLayer"`
3. **IDMask** (2.79): `CompositorNodeIDMask` with `pass_index` on shadow planes, reads `IndexOB` output at index 14

### Scene creation flow

Each variant's `main.py` is ~20 lines:
1. `get_compat(major, minor)` — detect version
2. `register_world(suffix, world_cls)` — register world material classes
3. `cls(compat)` for each scene class — creates full Blender scene
4. `load_scripts()` + `setup_text_editor()` + `save_blend()` — finalize

Exception: `legacy/` uses its own `scene_builder.py` with hardcoded camera/light configs per game. It does not import from `shared/scenes.py`.

### World materials

- `shared/world_materials.py` — cyclesx/eevee_next/hi_five via `Base_World(props, compat)`
- `eevee/world_materials.py` — Eevee 2.93+ (different API pattern, has `_set_mapping()` helper for cross-version Mapping node)
- `legacy_eevee/world_materials.py` — Eevee 2.80–2.92 (same as eevee, copied)
- `legacy_cycles/` — uses adapter wrappers to convert world class signatures

### Script generation

`shared/script_gen.py` uses data-driven generation with named `PlaneVisibility` dataclasses. Each variant's `generate_scripts.py` is ~5 lines delegating to `generate_all_scripts()`.

## Linting

```sh
uv run ruff check .
```

Config in `pyproject.toml`: 2-space indent, 200-char line length.

## Testing

```sh
uv run pytest tests/ -v
```

23 tests covering: compat layer interface, scene name mapping, script generation, version management, env format. All run outside Blender (no bpy dependency).

## Key conventions

- **2-space indentation** throughout (enforced by ruff).
- Scripts inside version folders run in Blender's Python interpreter, not standalone. `bpy` is the core API. Do not write Blender add-ons — these are headless automation scripts.
- Each game scene (RA2, TS, RW, RA1, RM, D2K) has 3 variants: base, INF (infantry, lower res), FX (effects). The `_FX` classes typically inherit from the base and override a few attributes.
- `shared/node_arrange.py` must be called after creating node trees to auto-layout nodes.
- `scripts/` directories and `release/` are gitignored. Never commit generated artifacts.
- `TEMPLATE_VERSION` lives only in `shared/constants.py`. Never put it in variant folders.
- Output files: `{prefix}_{version}_build{number}_{date}.blend` in `release/{variant}/`

## Gotchas

- `build.sh` is interactive (uses `select` for variant choice). Cannot be run non-interactively.
- Version folder names do not match Blender versions exactly (e.g. `hi_five` = Blender 5.1, `eevee_next` = Blender 4.3).
- `shared/constants.py` has different filter sizes per render engine (Cycles vs Eevee vs Eevee Next). Check this before changing filter-related values.
- `fake-bpy-module` in `requirements.txt` is for IDE support only, not runtime. The real `bpy` comes from the Blender installation.
- Eevee never had Object Index, Material Index, or Cryptomatte in any version. The ShadowLayer approach (2 view layers) works around this for 2.80–2.92.
- `CompositorNodeCryptomatteV2` was introduced in Blender 3.0. Before that, only `CompositorNodeCryptomatte` (4 inputs) exists.
- `eevee/world_materials.py` has `_set_mapping()` helper because Mapping node inputs differ: 1 input (Vector) in 2.80, 3 inputs (Location/Rotation/Scale) in 2.90+.
- `compat_280.py` overrides `has_cryptomatte() → False` and `has_shader_to_rgb() → False` because Eevee 2.80–2.92 lacks these features. 2.93 has its own `compat_293.py` that returns True for both.
- `legacy/` does not use the shared scene classes at all — it has its own `scene_builder.py` with hardcoded camera/light configs per game. Do not add shared scene logic there.
- All shared modules must be Python 3.5 compatible for legacy_cycles (no f-strings, no variable annotations, no dataclass).
