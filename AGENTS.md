# AGENTS.md

## Project summary

Generates `.blend` scene templates for multiple Blender versions (2.79b–5.0). Each version is isolated in its own folder with independent venv. Output goes to `release/`.

## Directory structure

```
{version}/              # One per Blender target: legacy, legacy_cycles, eevee, cyclesx, eevee_next, hi_five
  constants.py          # TEMPLATE_PREFIX, TEMPLATE_VERSION
  scenes.py             # Scene classes (BaseScene + game-specific subclasses)
  plane_materials.py    # Plane material node graphs
  world_materials.py    # World material node graphs
  generate_scripts.py   # Produces scripts/*.txt files
  main.py               # Headless Blender entrypoint - builds .blend
  scripts/              # Generated .txt scripts (gitignored)
shared/
  constants.py          # Shared filter width/size values
  node_arrange.py       # Auto-layout for Blender nodes
  node_arrange_legacy.py
  *.exr                 # HDRI textures used by scenes
release/                # Output .blend and .7z files (gitignored)
```

## Build commands

```sh
uv run ./build.sh       # Interactive: pick version, auto-finds Blender, generates + renders
uv run python {version}/generate_scripts.py   # Generate scripts only (no Blender needed)
```

`build.sh` flow: select engine → find Blender executable → create per-version `.venv` via `bootstrap.sh` if missing → `pip install` from `requirements.txt` → run `generate_scripts.py` → run Blender headless with `main.py` → archive to `.7z`.

`bootstrap.sh` creates `.venv` in each version folder and installs `fake-bpy-module` for IDE autocomplete.

## Linting

```sh
uv run ruff check .
```

Config in `pyproject.toml`: 2-space indent, 200-char line length. Also uses `pylintrc` with 2-space indent and several disabled checks (`missing-docstring`, `line-too-long`, `trailing-whitespace`, etc.).

## Key conventions

- **2-space indentation** throughout (enforced by ruff + pylintrc).
- Scripts inside version folders run in Blender's Python interpreter, not standalone. `bpy` is the core API. Do not write Blender add-ons — these are headless automation scripts.
- `generate_scripts.py` uses string concatenation to build `.txt` script files. `main.py` loads them into Blender text datablocks at build time.
- Each game scene (RA2, TS, RW, RA1, RM, D2K) has 3 variants: base, INF (infantry, lower res), FX (effects). The `_FX` classes typically inherit from the base and override a few attributes.
- `scenes.py` is the most complex file per version. Scene classes inherit from `BaseScene` and chain setup: `create_scene()` → `set_*_settings()` → `create_collections()` → `create_camera()` → `create_light()` → material setup → `create_composite_nodes()`.
- Import paths are manually hacked via `sys.path.append` — each version folder adds its own path and `parent_path` to import from `shared/`.
- `shared/node_arrange.py` must be called after creating node trees to auto-layout nodes.
- `scripts/` directories and `release/` are gitignored. Never commit generated artifacts.

## Gotchas

- There is no automated test suite. Validation is: run `generate_scripts.py`, run Blender headless, check that `.blend` file is produced in `release/`.
- `build.sh` is interactive (uses `select` for engine choice). Cannot be run non-interactively.
- Version folder names do not match Blender versions exactly (e.g. `hi_five` = Blender 5.0, `eevee_next` = Blender 4.2).
- `shared/constants.py` has different filter sizes per render engine (Cycles vs Eevee vs Eevee Next). Check this before changing filter-related values.
- `fake-bpy-module` in `requirements.txt` is for IDE support only, not runtime. The real `bpy` comes from the Blender installation.
