## Why

`create_composite_nodes()` in `shared/scenes.py` hardcodes compositor socket indices that assume the 2.79–4.x node layout. Blender 5.0 reordered `CompositorNodeSwitch` and `CompositorNodeAlphaOver` sockets, so the `hi_five` (5.0–5.1) template wires images into boolean controls, leaves background sockets empty, and connects the Alpha switch to the Factor input — breaking alpha compositing and channel switching (issue #21). The 4.x templates have the same latent Alpha Over bug: two links to the same foreground socket leave the sprite background empty.

The same release surfaced three adjacent render-correctness defects: Eevee shadow frames hid the sun (empty shadows), the 4.2+ shadow-plane material fell back to a non-transparent render method, and Blender 5 requested a nonexistent engine string. The template also opened on a random scene and shipped an uncommented `Readme.txt` text block that errors when run.

## What Changes

- `shared/scenes.py` wires `CompositorNodeSwitch` and `CompositorNodeAlphaOver` through new compat index helpers instead of hardcoded indices; Alpha Over background receives the Alpha switch selection, foreground receives the sprite (`alpha_convert`) / shadow (`colorramp`) output; switch chain routes pass-through → off/false branch, composited result → on/true branch.
- `shared/compat.py` (BaseCompat) gains concrete default index helpers for the ≤4.x layout; only `shared/compat_500.py` overrides them for the 5.0 layout.
- `shared/compat_420.py` sets `surface_render_method = "BLENDED"` for shadow planes instead of a fragile shadow-mode→render-method mapping, fixing transparent shadow rendering on 4.2+ (Eevee Next).
- `shared/compat_500.py` `get_engine_string()` returns `"BLENDER_EEVEE"` (the 5.0 engine identifier) instead of `"BLENDER_EEVEE_NEXT"`.
- Shadow render scripts keep the sun visible (`Sun.*.hide_render = False`) so Eevee shadow frames are not empty — `shared/script_gen.py` and `legacy_eevee/scripts/Eevee.Render.Shadow.txt`.
- Every variant except `legacy/` opens on the `Red Alert 2` scene via `compat.select_scene("Red Alert 2")` in `main.py`.
- Generated `Readme.txt` lines are prefixed with `#` so running the readme text block is a no-op — `shared/script_gen.py`, `legacy/generate_scripts.py`, `legacy_cycles/generate_scripts.py`.
- `legacy/compositor.py` (2.79 BLENDER_RENDER) is untouched — it has its own wiring and doesn't use the shared scene classes.

## Capabilities

### New Capabilities
- `compositor-node-wiring`: Correct, version-correct compositor node connections for channel switching and alpha background compositing across all shared variants (2.79–5.1).
- `shadow-frame-rendering`: Eevee / Eevee Next shadow frames render with the sun visible and a properly transparent shadow-plane material across 4.2–5.1.

### Modified Capabilities
<!-- None — legacy-render-scenes is variant-specific and unaffected. -->

## Non-goals

- Not changing premultiply semantics (`set_alpha_over_premultiply`) — behavior is consistent with the reference toolkit.
- Not re-verifying Cryptomatte/Invert/SeparateColor socket layouts for 5.0 — the reporter did not flag them and `compat_500.py` already abstracts invert/mix indices; a render check is a follow-up.
- Not rebuilding the toolkit's per-render-type node graphs — the switch chain stays as-is.
- Not touching the `legacy/` variant.
- Not changing readme *content* — only prefixing lines so the text block is a safe no-op.

## Impact

- `shared/scenes.py` — `create_composite_nodes()` wiring.
- `shared/compat.py` — two new default index helpers on `BaseCompat`.
- `shared/compat_500.py` — index overrides for the 5.0 socket layout + `get_engine_string()` fix.
- `shared/compat_420.py` — `surface_render_method = "BLENDED"`.
- `shared/script_gen.py` — sun visibility in shadow scripts + readme comment prefixing.
- `legacy/generate_scripts.py`, `legacy_cycles/generate_scripts.py` — readme comment prefixing.
- `legacy_eevee/scripts/Eevee.Render.Shadow.txt` — sun visible in the Eevee shadow script.
- `main.py` of `cyclesx`, `eevee`, `eevee_next`, `hi_five`, `legacy_cycles`, `legacy_eevee` — default scene selection.
- `tests/test_compat_runtime.py` — index-helper assertions (mirrors existing 2.79/5.0 index tests) + updated `surface_render_method` expectation.
- `tests/test_compat.py` — `EXPECTED_METHODS` gains the two new helpers.
- 6 variants affected via shared code: `legacy_cycles`, `legacy_eevee`, `eevee`, `cyclesx`, `eevee_next`, `hi_five`.
