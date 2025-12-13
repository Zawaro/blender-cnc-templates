# blender‑cnc‑templates

A lightweight toolkit that generates ready‑to‑use Blender scene templates for several Blender releases (2.79 – 5.0).
Each version has its own folder with scripts, materials and a small build script that produces a `.blend` file.

---

## Supported Blender versions

| Version         | Folder          | Notes                       |
|-----------------|-----------------|-----------------------------|
| 2.79b           | `legacy`        | Legacy Blender renderer     |
| 2.79b (Cycles)  | `legacy_cycles` | Classic Cycles renderer     |
| 2.80            | `eevee`         | Eevee engine                |
| 3.00            | `cyclesx`       | Cycles X                    |
| 4.2             | `eevee_next`    | Eevee Next                  |
| 5.0             | `future_five`   | Latest stable release       |

---

## Project layout (inside each `{version}` folder)

- **scripts/** – Blender‑specific Python helpers
- **constants.py** – shared constants across all templates
- **generate_scripts.py** – creates template scripts at build time
- **scenes.py** – scene definitions and selectors/cleanup logic
- **plane_materials.py** – plane‑object node materials
- **world_materials.py** – world‑node materials

---


## Build with `uv`

```sh
# 1. Create a uv virtual environment (if it doesn’t exist)
uv venv .

# 2. Activate the environment (Linux/macOS)
source .venv/bin/activate   # Windows: .\\.venv\\Scripts\\activate

# 3. Install dependencies – uv reads pyproject.toml and lock files
uv sync

# 4. Run the build script for this Blender version
uv run ./build.sh
```

The `uv` commands replace the old `pip`‑based workflow, provide deterministic installs and keep a reproducible lock file (`uv.lock`).  

## Dependencies

Only a small set of third‑party libraries is required – they’re listed in *pyproject.toml* and installed with `uv sync`.


## Support

Got questions? Join our Discord community: **[https://discord.gg/YWZM9s7](https://discord.gg/YWZM9s7)**

