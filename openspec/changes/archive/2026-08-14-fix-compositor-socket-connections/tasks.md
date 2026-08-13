## 1. Compat layer socket helpers

- [x] 1.1 Add `get_switch_input_indices()` to `BaseCompat` (`shared/compat.py`) returning `(0, 1)` with a docstring noting it is the ≤4.x `Off/On` layout
- [x] 1.2 Add `get_alpha_over_image_indices()` to `BaseCompat` returning `(1, 2)` with a docstring noting it is the ≤4.x `Image bg/Image fg` layout
- [x] 1.3 Override both in `Compat500` (`shared/compat_500.py`): `(1, 2)` for switch `False/True` and `(0, 1)` for Alpha Over `Background/Foreground`
- [x] 1.4 Add both methods to `EXPECTED_METHODS` in `tests/test_compat.py`

## 2. Rewire `create_composite_nodes`

- [x] 2.1 In `shared/scenes.py`, read `switch_pass, switch_comp = self.compat.get_switch_input_indices()` and `ao_bg, ao_fg = self.compat.get_alpha_over_image_indices()` at the top of `create_composite_nodes()`
- [x] 2.2 Update the 7 chain links + Render Layers start link to use `inputs[switch_pass]`
- [x] 2.3 Update the Alpha switch branch links: `rgb01` → `inputs[switch_pass]`, `rgb02` → `inputs[switch_comp]`
- [x] 2.4 Update the 7 composited-result links (ao01/ao02 outputs into Object/Buildup/Shadow/Preview switches) to use `inputs[switch_comp]`
- [x] 2.5 Update Alpha Over links: `alpha_convert.outputs[0]` → `ao01.inputs[ao_fg]`, `colorramp.outputs[0]` → `ao02.inputs[ao_fg]` (3 branch copies), and `switches["Alpha"].outputs[0]` → `ao01.inputs[ao_bg]` + `ao02.inputs[ao_bg]`
- [x] 2.6 Confirm `legacy/compositor.py` and `legacy/` are untouched (own wiring, no shared scenes)

## 3. Tests

- [x] 3.1 Add `test_279_uses_old_node_indices`-style assertions in `tests/test_compat_runtime.py`: ≤4.x versions return `(0, 1)` and `(1, 2)`
- [x] 3.2 Add 5.0 assertions: `get_switch_input_indices() == (1, 2)` and `get_alpha_over_image_indices() == (0, 1)`
- [x] 3.3 Run `uv run ruff check .`
- [x] 3.4 Run `uv run pytest tests/ -v` (non-bpy tier) and confirm green

## 4. Build verification

- [x] 4.1 Build `hi_five` and `eevee_next` (or run the bpy tier with pytest-blender if a 4.2/5.x Blender is available) and confirm the compositor graph builds without errors
- [x] 4.2 Spot-check the built graph: Alpha Over background receives the Alpha switch, foreground receives sprite/shadow, switch control inputs unconnected on 5.0
