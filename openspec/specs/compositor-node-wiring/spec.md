# compositor-node-wiring Specification

## Requirements

### Requirement: Alpha Over compositing uses correct sockets per version
Each shared scene's compositor SHALL composite the sprite (foreground) over the Alpha switch selection (background) using the version-correct Alpha Over sockets: for ≤4.x the background SHALL be the first Image input and the foreground the second Image input; for 5.0 the background SHALL be the Background input and the foreground the Foreground input. The Factor/Fac input SHALL keep its default value (not receive the Alpha switch).

#### Scenario: Alpha Over background receives the Alpha switch selection
- **WHEN** a scene's compositor is built on any shared variant (≤4.x or 5.0)
- **THEN** the Alpha switch output is linked to the Alpha Over background socket (input index 1 for ≤4.x, input index 0 for 5.0) on both Alpha Over nodes

#### Scenario: Alpha Over foreground receives the sprite and shadow
- **WHEN** a scene's compositor is built on any shared variant (≤4.x or 5.0)
- **THEN** the Alpha Convert group output is linked to the foreground socket of the first Alpha Over node, and the Color Ramp output is linked to the foreground socket of the second Alpha Over node (input index 2 for ≤4.x, input index 1 for 5.0)

#### Scenario: no socket receives two conflicting links
- **WHEN** a scene's compositor is built
- **THEN** no Alpha Over input socket has more than one incoming link, and no Alpha Over Image/Background input is left unconnected

### Requirement: Channel switches select between pass-through and composited result
Each channel switch (Object, Buildup.Cycles, Buildup.Eevee, Shadow.Cycles, Shadow.Eevee, Preview.Cycles, Preview.Eevee) SHALL route the raw pass-through chain into the version's "off/false" branch and the Alpha Over composited result into the "on/true" branch: for ≤4.x these are the Off (index 0) and On (index 1) inputs; for 5.0 these are the False (index 1) and True (index 2) inputs. The switch control input SHALL remain the boolean selector, never connected to an image output.

#### Scenario: pass-through chain links to the off/false branch
- **WHEN** a scene's compositor is built on any shared variant (≤4.x or 5.0)
- **THEN** the Render Layers image and each upstream switch output link to the pass-through branch (input index 0 for ≤4.x, input index 1 for 5.0) of the downstream switch

#### Scenario: composited result links to the on/true branch
- **WHEN** a scene's compositor is built on any shared variant (≤4.x or 5.0)
- **THEN** the Alpha Over outputs link to the composited branch (input index 1 for ≤4.x, input index 2 for 5.0) of the Object, Buildup, Shadow, and Preview switches

#### Scenario: switch control input is not connected to an image
- **WHEN** a scene's compositor is built on Blender 5.0
- **THEN** the Switch (control) input of every channel switch has no incoming link and defaults to selecting the pass-through branch

### Requirement: Alpha switch branches stay consistent across versions
The Alpha switch SHALL present `BackgroundRGB` (solid blue) on the off/false branch and `BackgroundAlpha` (transparent) on the on/true branch for every version: ≤4.x Off (index 0) and On (index 1); 5.0 False (index 1) and True (index 2). The control input SHALL not receive the background colors.

#### Scenario: Alpha switch branches are version-correct
- **WHEN** a scene's compositor is built on Blender 5.0
- **THEN** BackgroundRGB links to the False input, BackgroundAlpha links to the True input, and the Switch control input has no incoming link

### Requirement: Compat layer exposes version-correct socket indices
The compat interface SHALL expose the switch pass-through/composite input indices and the Alpha Over background/foreground input indices per version. Versions ≤4.x SHALL return the Off/On (0, 1) and background/foreground (1, 2) layouts; 5.0 SHALL return False/True (1, 2) and Background/Foreground (0, 1). `legacy/compat.py` SHALL inherit the ≤4.x defaults.

#### Scenario: index helpers return per-version values
- **WHEN** `get_switch_input_indices()` and `get_alpha_over_image_indices()` are called for each compat version
- **THEN** 2.79–4.2 return `(0, 1)` and `(1, 2)`, and 5.0 returns `(1, 2)` and `(0, 1)`
