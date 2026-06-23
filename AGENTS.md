# AGENTS.md

## Project summary

Generates `.blend` scene templates for multiple Blender versions (2.79b–5.0). Each version is isolated in its own folder with independent venv. Output goes to `release/`.

## Directory structure

```
{version}/              # One per Blender target: legacy, legacy_cycles, eevee, cyclesx, eevee_next, hi_five
  constants.py          # TEMPLATE_PREFIX, TEMPLATE_VERSION
  main.py               # ~20 lines: compat setup + scene creation + save .blend
  generate_scripts.py   # ~5 lines: delegates to shared/script_gen.py
  __init__.py
  requirements.txt
  README.md
  scripts/              # Generated .txt scripts (gitignored)
shared/
  compat.py             # BaseCompat interface + get_compat() factory
  compat_279.py         # Blender 2.79 adapters
  compat_280.py         # Blender 2.80 adapters
  compat_300.py         # Blender 3.0 adapters
  compat_420.py         # Blender 4.2 adapters
  compat_500.py         # Blender 5.0 adapters
  scenes.py             # BaseScene + all game classes (single copy)
  plane_materials.py    # Material factories (single copy)
  world_materials.py    # World material factories (single copy, compat-aware)
  scene_names.py        # SCENE_SUFFIX_MAP (single source of truth)
  script_gen.py         # Data-driven .txt script generator
  build_utils.py        # Load scripts into Blender + save .blend
  constants.py          # Shared filter width/size values
  node_arrange.py       # Auto-layout for Blender nodes
  node_arrange_legacy.py
  *.exr                 # HDRI textures used by scenes
tests/
  test_compat.py        # Compat layer interface compliance
  test_scene_names.py   # Scene name mapping completeness
  test_script_gen.py    # Script generation (no bpy needed)
release/                # Output .blend and .7z files (gitignored)
```

## Build commands

```sh
uv run ./build.sh       # Interactive: pick version, auto-finds Blender, generates + renders
uv run python {version}/generate_scripts.py   # Generate scripts only (no Blender needed)
uv run pytest tests/ -v                        # Run tests (no Blender needed)
```

`build.sh` flow: select engine → find Blender executable → create per-version `.venv` via `bootstrap.sh` if missing → `pip install` from `requirements.txt` → run `generate_scripts.py` → run Blender headless with `main.py` → archive to `.7z`.

`bootstrap.sh` creates `.venv` in each version folder and installs `fake-bpy-module` for IDE autocomplete.

## Architecture

### Compat layer

All Blender API differences across versions (2.79–5.0) are abstracted through `shared/compat.py`. Each version has a compat class implementing the same interface:

- **Compositor access**: `scene.node_tree` (2.79–4.x) vs `scene.compositing_node_group` (5.0)
- **Node types**: `CompositorNodeSepHSVA` vs `CompositorNodeSeparateColor`, `CompositorNodeMixRGB` vs `ShaderNodeMix`
- **Node group I/O**: `inputs.new()` vs `interface.new_socket()`
- **Switch node toggle**: `.check` vs `.inputs[0].default_value`
- **Material transparency**: `blend_method`/`shadow_method` vs `surface_render_method`
- **Light creation**: `lamp_add` (2.79) vs `light_add` (2.80+)
- **Eevee settings**: GTAO/TAA/SSR (2.80–4.x) vs `use_shadows` only (5.0)

### Scene creation flow

Each version's `main.py` is ~20 lines:
1. `get_compat(major, minor)` — detect version
2. `register_world(suffix, world_cls)` — register world material classes
3. `cls(compat)` for each scene class — creates full Blender scene
4. `load_scripts()` + `setup_text_editor()` + `save_blend()` — finalize

### World materials

`shared/world_materials.py` handles cyclesx/eevee_next/hi_five via `Base_World(props, compat)`. The eevee version keeps its own `world_materials.py` (different API pattern). Legacy_cycles uses adapter wrappers.

### Script generation

`shared/script_gen.py` replaces string concatenation with data-driven generation. Uses named `PlaneVisibility` dataclasses instead of magic arrays. Each version's `generate_scripts.py` is ~5 lines delegating to `generate_all_scripts()`.

## Linting

```sh
uv run ruff check .
```

Config in `pyproject.toml`: 2-space indent, 200-char line length.

## Testing

```sh
uv run pytest tests/ -v
```

13 tests covering: compat layer interface, scene name mapping, script generation. All run outside Blender (no bpy dependency).

## Key conventions

- **2-space indentation** throughout (enforced by ruff).
- Scripts inside version folders run in Blender's Python interpreter, not standalone. `bpy` is the core API. Do not write Blender add-ons — these are headless automation scripts.
- Each game scene (RA2, TS, RW, RA1, RM, D2K) has 3 variants: base, INF (infantry, lower res), FX (effects). The `_FX` classes typically inherit from the base and override a few attributes.
- `shared/node_arrange.py` must be called after creating node trees to auto-layout nodes.
- `scripts/` directories and `release/` are gitignored. Never commit generated artifacts.

## Gotchas

- `build.sh` is interactive (uses `select` for engine choice). Cannot be run non-interactively.
- Version folder names do not match Blender versions exactly (e.g. `hi_five` = Blender 5.0, `eevee_next` = Blender 4.2).
- `shared/constants.py` has different filter sizes per render engine (Cycles vs Eevee vs Eevee Next). Check this before changing filter-related values.
- `fake-bpy-module` in `requirements.txt` is for IDE support only, not runtime. The real `bpy` comes from the Blender installation.
- The `eevee/` folder keeps its own `world_materials.py` because it uses a different API pattern (per-function copy-paste without Base_World).
- The `legacy_cycles/` folder uses adapter wrappers to convert its world class signatures to the shared format.
