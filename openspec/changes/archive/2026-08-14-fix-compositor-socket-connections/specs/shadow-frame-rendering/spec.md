# shadow-frame-rendering Specification

## ADDED Requirements

### Requirement: Sun stays visible during shadow renders
Shadow render scripts SHALL keep the sun object visible (`Sun.<suffix>.hide_render = False`) so Eevee / Eevee Next shadow frames are not empty. This applies to the generated shadow scripts for every shared variant and to the `legacy_eevee` Eevee shadow script.

#### Scenario: generated shadow script does not hide the sun
- **WHEN** a shadow render script is generated for any non-Cycles variant
- **THEN** its `Sun.<suffix>.hide_render` line is `False`

#### Scenario: legacy_eevee shadow script keeps the sun
- **WHEN** the `Eevee.Render.Shadow` script is inspected in the `legacy_eevee` variant
- **THEN** `Sun.<suffix>.hide_render` is set to `False`

### Requirement: Shadow plane renders transparent on 4.2+
`set_material_transparency` for the Blender 4.2+ surface render method SHALL set `surface_render_method = "BLENDED"` when transparency is `BLEND`, so shadow planes render with transparent shadows instead of an opaque fallback.

#### Scenario: 4.2+ shadow material uses BLENDED surface render method
- **WHEN** `set_material_transparency` is called with `"BLEND"` on a 4.2+ material exposing only `surface_render_method`
- **THEN** `surface_render_method` is set to `"BLENDED"`

### Requirement: Blender 5 uses a valid engine identifier
`Compat500.get_engine_string()` SHALL return `"BLENDER_EEVEE"` for the Eevee engine key so Blender 5.0+ scenes select a valid engine instead of the nonexistent `"BLENDER_EEVEE_NEXT"`.

#### Scenario: engine string resolves for Blender 5
- **WHEN** `get_engine_string("EEVEE")` is called on the 5.0 compat
- **THEN** it returns `"BLENDER_EEVEE"`
