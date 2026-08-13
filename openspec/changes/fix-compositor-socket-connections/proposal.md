## Why

`create_composite_nodes()` in `shared/scenes.py` hardcodes compositor socket indices that assume the 2.79–4.x node layout. Blender 5.0 reordered `CompositorNodeSwitch` and `CompositorNodeAlphaOver` sockets, so the `hi_five` (5.0–5.1) template wires images into boolean controls, leaves background sockets empty, and connects the Alpha switch to the Factor input — breaking alpha compositing and channel switching (issue #21). The 4.x templates have the same latent Alpha Over bug: two links to the same foreground socket leave the sprite background empty.

## What Changes

- `shared/scenes.py` wires `CompositorNodeSwitch` and `CompositorNodeAlphaOver` through new compat index helpers instead of hardcoded indices.
- `shared/compat.py` (BaseCompat) gains concrete default index helpers for the ≤4.x layout; only `shared/compat_500.py` overrides them for the 5.0 layout.
- Alpha Over wiring fixed: background socket receives the Alpha switch selection (blue/transparent), foreground socket receives the sprite (`alpha_convert`) / shadow (`colorramp`) output — for both 4.x and 5.0.
- Switch wiring fixed: pass-through chain → "off/false" branch, composited result → "on/true" branch; Alpha switch branches keep `BackgroundRGB` → off/false and `BackgroundAlpha` → on/true.
- `set_alpha_over_premultiply` unchanged (verified identical to the reference toolkit: `use_premultiply=True` ≤4.x, `inputs[4]=True` 5.0).
- `legacy/compositor.py` (2.79 BLENDER_RENDER) is untouched — it has its own wiring and doesn't use the shared scene classes.

## Capabilities

### New Capabilities
- `compositor-node-wiring`: Correct, version-correct compositor node connections for channel switching and alpha background compositing across all shared variants (2.79–5.1).

### Modified Capabilities
<!-- None — legacy-render-scenes is variant-specific and unaffected. -->

## Non-goals

- Not changing premultiply semantics (`set_alpha_over_premultiply`) — behavior is consistent with the reference toolkit.
- Not re-verifying Cryptomatte/Invert/SeparateColor socket layouts for 5.0 — the reporter did not flag them and `compat_500.py` already abstracts invert/mix indices; a render check is a follow-up, not part of this change.
- Not rebuilding the toolkit's per-render-type node graphs — the switch chain stays as-is.
- Not touching the `legacy/` variant.

## Impact

- `shared/scenes.py` — `create_composite_nodes()` wiring.
- `shared/compat.py` — two new default index helpers on `BaseCompat`.
- `shared/compat_500.py` — two overrides for the 5.0 socket layout.
- `tests/test_compat_runtime.py` — index-helper assertions (mirrors existing 2.79/5.0 index tests).
- `tests/test_compat.py` — `EXPECTED_METHODS` gains the two new helpers.
- 6 variants affected via shared code: `legacy_cycles`, `legacy_eevee`, `eevee`, `cyclesx`, `eevee_next`, `hi_five`.
