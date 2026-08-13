## Context

All shared variants (`legacy_cycles`, `legacy_eevee`, `eevee`, `cyclesx`, `eevee_next`, `hi_five`) build their compositor via `BaseScene.create_composite_nodes()` in `shared/scenes.py`. It hardcodes socket indices for `CompositorNodeSwitch` (`inputs[0]`/`inputs[1]`) and `CompositorNodeAlphaOver` (`inputs[1]`/`inputs[2]`). Those indices match the 2.79–4.x node layout but Blender 5.0 reordered both nodes:

- Switch: ≤4.x `Off(0)/On(1)/Check(2)` → 5.0 `Switch(0, bool)/False(1)/True(2)`
- Alpha Over: ≤4.x `Fac(0)/Image bg(1)/Image fg(2)` → 5.0 `Background(0)/Foreground(1)/Factor(2)/Type(3)/Straight Alpha(4)`

The sibling `../blender-cnc-toolkit` confirmed both layouts: its `cyclesx`/`eevee_next` use bg=`inputs[1]`, fg=`inputs[2]`; its `hi_five` uses bg=`inputs[0]`, fg=`inputs[1]`, premultiply=`inputs[4]`. The toolkit has no switch nodes, so the switch layout rests on the 5.0 API, the issue report, and the existing `Compat500.compositor_switch_toggle` (already uses `inputs[0]` as the boolean control).

A second, version-independent bug: the Alpha switch output and `alpha_convert` output both link to `ao01.inputs[2]` — the second link replaces the first, leaving the background socket empty.

## Goals / Non-Goals

**Goals:**
- Wire switch and Alpha Over nodes by socket *role* via the compat interface, never hardcoded indices.
- Correct Alpha Over wiring: background = Alpha switch selection, foreground = sprite/shadow.
- Correct switch wiring: pass-through chain → off/false branch, composited result → on/true branch.
- Keep ≤4.x behavior byte-identical; fix only the 5.0 socket mapping and the 4.x duplicate-link bug.

**Non-Goals:**
- No premultiply semantic change (`set_alpha_over_premultiply` is confirmed correct vs the toolkit).
- No changes to Cryptomatte/Invert/SeparateColor wiring (not flagged; abstracted already).
- No change to `legacy/compositor.py` or the `legacy/` variant.

## Decisions

**D1 — Compat index helpers with concrete defaults in BaseCompat.**
Add two methods to `BaseCompat`, each returning a `Tuple[int, int]`:

- `get_switch_input_indices()` → `(0, 1)` (≤4.x `Off/On`)
- `get_alpha_over_image_indices()` → `(1, 2)` (≤4.x `Image bg/Image fg`)

Override only in `Compat500`: `(1, 2)` and `(0, 1)`. *Alternative rejected:* making them `@abstractmethod` and copy-pasting into all 6 shared files + `legacy/compat.py` — matches the existing `get_invert_color_input` style but adds ~20 lines of identical code for zero benefit. Concrete defaults keep the diff to two files + two overrides, and mirror the existing non-abstract defaults (`has_cryptomatte`, `get_shadow_pass_index`).

**D2 — Wire by role in `create_composite_nodes()`.**
Read `switch_pass, switch_comp = compat.get_switch_input_indices()` and `ao_bg, ao_fg = compat.get_alpha_over_image_indices()` once, then:

- chain links + `rgb01/rgb02` Alpha branches → `inputs[switch_pass]` / `inputs[switch_comp]`
- `alpha_convert.outputs[0]` and `colorramp.outputs[0]` → `inputs[ao_fg]` (foreground)
- `switches["Alpha"].outputs[0]` → `inputs[ao_bg]` on both `ao01` and `ao02` (background)

This yields the same topology as the current ≤4.x output except the two re-pointed Alpha Over links that fix the duplicate-link/background-empty bug.

**D3 — Scripts and toggles untouched.**
`compositor_switch_toggle`/`alpha_toggle` already target the correct control socket per version (`node.check` ≤4.x, `inputs[0].default_value` 5.0). `set_switch_value` is dead code — left as-is.

**D4 — Verify 5.0 build via tests, not blind render.**
Add non-bpy assertions for the new helpers (mirroring `test_279_uses_old_node_indices` / `test_500_uses_new_node_indices`) and extend `EXPECTED_METHODS`. bpy integration (pytest-blender) confirms the graph builds, if a 4.2/5.x Blender is available.

## Risks / Trade-offs

- [≤4.x regression from touching shared wiring] → The role-based remap is identical to current topology for ≤4.x except two corrected links; verified by re-running the existing non-bpy + bpy test tiers before and after.
- [5.0 switch layout assumption unverified against a live Blender] → Triangulated from Blender 5.0 API, the issue report, and the toolkit's 5.0 alpha-over indices; the reporter's socket names (`Switch/False/True`, `Background/Foreground/Factor`) match exactly.
- [Future Blender socket reorder hidden by BaseCompat defaults] → The defaults are documented as the ≤4.x layout; a 5.x+ reorder would follow the same override pattern.
