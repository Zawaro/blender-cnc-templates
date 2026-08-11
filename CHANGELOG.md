# Changelog

## [1.1.0](https://github.com/Zawaro/blender-cnc-templates/compare/v1.0.0...v1.1.0) (2026-08-11)


### Features

* add compat_293.py for Blender 2.93 with CryptomatteV2 and Shader to RGB support ([bf59b43](https://github.com/Zawaro/blender-cnc-templates/commit/bf59b43776c011b6ae5c8ee736e6c384c90ce361))
* add generate script to eevee ([c1b4ef6](https://github.com/Zawaro/blender-cnc-templates/commit/c1b4ef6819a1cfe8bdd8eb572e687d0e16c6d151))
* add legacy cycles ([c3595d6](https://github.com/Zawaro/blender-cnc-templates/commit/c3595d67fe5f6829dd6552002fa129247606eaa0))
* add node arranger to legacy ([29d9ebe](https://github.com/Zawaro/blender-cnc-templates/commit/29d9ebe27d2751e3503d3db423a19741662dd0ac))
* add variant subdirs to release output ([aa6f532](https://github.com/Zawaro/blender-cnc-templates/commit/aa6f532a84e250b0abc0e61c2dc9da346870ac1f))
* add version management and archive improvements ([c08b292](https://github.com/Zawaro/blender-cnc-templates/commit/c08b292c143375b55aeffcf1cb8b0f32475fb817))
* **eevee_next:** add Blender 4.2+ template support ([4dff140](https://github.com/Zawaro/blender-cnc-templates/commit/4dff140b9c0f9050b993ed28dea623feb58c602b))
* **future_five:** add Blender 5.0 template support ([66cb282](https://github.com/Zawaro/blender-cnc-templates/commit/66cb28228c9fc4b3e20b0ef50812ab913563927e))
* gitignore .blend file ([ceb440e](https://github.com/Zawaro/blender-cnc-templates/commit/ceb440e6307883af3f30b9a1ec929ca79f397ef1))
* implement legacy variant (BLENDER_RENDER on 2.79) ([487b8bc](https://github.com/Zawaro/blender-cnc-templates/commit/487b8bc5ca75061933663b57bc9d90d58fc8e3fd))
* init legacy scripting ([c334a31](https://github.com/Zawaro/blender-cnc-templates/commit/c334a31773732a6f65ee9f108447c3274962f4ea))
* port release-please setup from blender-cnc-toolkit ([#14](https://github.com/Zawaro/blender-cnc-templates/issues/14)) ([3f1a2ac](https://github.com/Zawaro/blender-cnc-templates/commit/3f1a2ac559b5053eaea3be493f34e809eae2cea1))
* recover legacy variant source from .blend files ([#17](https://github.com/Zawaro/blender-cnc-templates/issues/17)) ([2ffd991](https://github.com/Zawaro/blender-cnc-templates/commit/2ffd9915fc34d342d4fe7591ebdfead6f8d67dc7))
* restore Cryptomatte path, add legacy_eevee variant ([9a192ad](https://github.com/Zawaro/blender-cnc-templates/commit/9a192ad71912fc6f0097b2b093cce8eb1a1b8170))
* ShadowLayer compositing for Eevee, bump min to 2.81 ([d0f6f1e](https://github.com/Zawaro/blender-cnc-templates/commit/d0f6f1e6783e448132d0d1e65a6faf9c5b8ae420))
* use sky material instead of hdri texture ([1a3047d](https://github.com/Zawaro/blender-cnc-templates/commit/1a3047d417a6efd6d5c214cb0dd462476a57da4e))


### Bug Fixes

* annotate TEMPLATE_VERSION for release-please version sync ([690a25f](https://github.com/Zawaro/blender-cnc-templates/commit/690a25f3a68e3f05c852b8d86b62b60804b474bf))
* archive filenames now match .blend basename (was stripping version info) ([794ef1a](https://github.com/Zawaro/blender-cnc-templates/commit/794ef1af53a152d9a00823d54f4d39f7366755ea))
* bugs from code review — compat routing, legacy_cycles crashes, misc ([54ebdd4](https://github.com/Zawaro/blender-cnc-templates/commit/54ebdd4b1cdff126369ad343347302a28eaef534))
* CI — install test deps for non-bpy job, re-enable pytest-blender for bpy job ([deeb91e](https://github.com/Zawaro/blender-cnc-templates/commit/deeb91e71d1ade1e294565bcf784d3c1dd8555ad))
* CI — lint errors, blender-downloader flags, ruff dependency ([d826c49](https://github.com/Zawaro/blender-cnc-templates/commit/d826c49d35a2aa2f918e5cd76514af2f5a3f6fae))
* eevee compat for Blender 2.80 ([c727872](https://github.com/Zawaro/blender-cnc-templates/commit/c7278725ba27df2feeb240379712b038eb6a55d6))
* pin ruff to lockfile version in CI ([#14](https://github.com/Zawaro/blender-cnc-templates/issues/14)) ([0054e88](https://github.com/Zawaro/blender-cnc-templates/commit/0054e8823bdf5f53aaed01fb92faec5b4ad8438f))
* release assets .zip only, drop .7z from CI ([054b23c](https://github.com/Zawaro/blender-cnc-templates/commit/054b23cd557dbe896c9c42cd49c374ac82f02a6c))
* remove EEVEE nodes from legacy_cycles (EEVEE didn't exist in 2.79) ([af9eebd](https://github.com/Zawaro/blender-cnc-templates/commit/af9eebd87f4824cba8b2575e6ec1caa88d0a4c8d))
* rewrite CI workflow to match working blender-cnc-toolkit pattern ([a69b966](https://github.com/Zawaro/blender-cnc-templates/commit/a69b966a171e52e8a31483fce09a1a0ad4a3ca07))
* use sharper pixel filter "blackman-harris" ([c35ae2b](https://github.com/Zawaro/blender-cnc-templates/commit/c35ae2b28e0c2ddefacc0544099365bbff567918))
