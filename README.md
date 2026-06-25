# blender‑cnc‑templates

A lightweight toolkit that generates ready‑to‑use Blender scene templates for several Blender releases (2.79 – 5.1).
Each version has its own folder with scripts, materials and a small build script that produces a `.blend` file.

---

## Supported Blender versions

| Version         | Folder          | Notes                       |
|-----------------|-----------------|-----------------------------|
| 2.79b           | `legacy`        | Legacy Blender renderer     |
| 2.79b (Cycles)  | `legacy_cycles` | Classic Cycles renderer     |
| 2.80–2.92       | `legacy_eevee`  | Eevee (pre-2.93)            |
| 2.93            | `eevee`         | Eevee (CryptomatteV2)       |
| 3.0–3.6         | `cyclesx`       | Cycles X                    |
| 4.2–4.3         | `eevee_next`    | Eevee Next                  |
| 5.0–5.1         | `hi_five`       | Latest stable release       |

---

## Project layout

- **`{variant}/`** — One folder per Blender target (e.g. `legacy/`, `hi_five/`)
  - `constants.py` — TEMPLATE_PREFIX, TEMPLATE_VARIANT
  - `main.py` — Compat setup, scene creation, save .blend
  - `generate_scripts.py` — Delegates to shared/script_gen.py
  - `world_materials.py` — (some variants) variant-specific world materials
  - `scripts/` — Generated .txt scripts (gitignored)
- **`shared/`** — Compat layer, scene classes, material factories, build utils
- **`tests/`** — Tests (no bpy needed)

---

## Testing

```sh
# Run all tests (no Blender needed)
uv run pytest tests/ -v

# Run all tests against a specific Blender version
./test.sh 5.1

# Run all tests against all available Blender versions
./test.sh --all
```


## Build with `uv`

```sh
# 1. Set up Blender paths (auto-detect or edit manually)
./fill_env.sh          # Auto-detects installed Blender versions
# — or —
cp .env.example .env   # Then edit .env with your Blender paths

# 2. Run the build (interactive: pick a variant)
uv run ./build.sh

# Or generate scripts only (no Blender needed):
uv run python {variant}/generate_scripts.py
```

The `uv` commands replace the old `pip`‑based workflow, provide deterministic installs and keep a reproducible lock file (`uv.lock`).  

## Support

Got questions? Join our Discord community: **[https://discord.gg/YWZM9s7](https://discord.gg/YWZM9s7)**

