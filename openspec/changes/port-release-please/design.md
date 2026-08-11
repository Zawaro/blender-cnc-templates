## Context

This repo generates `.blend` scene templates for Blender 2.79–5.1 across 7 isolated variants (`legacy`, `legacy_cycles`, `legacy_eevee`, `eevee`, `cyclesx`, `eevee_next`, `hi_five`). Version lives only in `shared/constants.py` (`TEMPLATE_VERSION = "1.0.0"`); `pyproject.toml` duplicates it. Local builds go through interactive `build.sh`; CI (`test.yml`) already has a proven non-interactive per-variant build ("build-test" job: blender-downloader + `generate_scripts.py` + `blender -b --python main.py`, Blender cached under `build-blender-$version`).

The sibling `blender-cnc-toolkit` repo has a working release-please setup (`release-please.yml`, `release-please-config.json`, `commitlint.yml`, `commitlint.config.cjs`) to port from. Existing tags `v1.00-alpha1..4` are pre-releases; the next release is `v1.0.0`.

## Goals / Non-Goals

**Goals:**
- Automatic version bumps + CHANGELOG on conventional commits to `main`.
- On release: build all 7 variants and publish `.blend`, `.zip`, `.7z` to the GitHub release, with a per-variant download table and `{tag}_build{N}` tag.
- Single source of truth for the version (`shared/constants.py`).
- Commitlint enforcement of commit messages and PR titles.

**Non-Goals:**
- Changing `build.sh` (stays interactive, for local use).
- Changing how `.blend` files are named by `shared/build_utils.py`.
- Migrating the toolkit's exact job structure (its `dist.py --all` single-job model does not fit 7 Blender versions).

## Decisions

### D1. Build orchestration: matrix build, not single job
The toolkit builds all variants sequentially in one job (`python dist.py --all`). Here, downloading 7 Blender versions (~1.4GB) into one job is wasteful. Instead reuse the `test.yml` build-test pattern: a 7-way matrix, each job downloading/caching its own Blender (same cache key `build-blender-$version`, so the cache is already warm from CI) and uploading its assets directly to the release via `softprops/action-gh-release`.
- Alternative considered: single sequential job (mirrors toolkit) — rejected for cache sharing and parallelism.

### D2. Version single-sourcing via dynamic pyproject version
`pyproject.toml` uses `dynamic = ["version"]` + `[tool.setuptools.dynamic] version = { attr = "shared.constants.TEMPLATE_VERSION" }` + explicit `[build-system]` (setuptools). Setuptools statically parses `TEMPLATE_VERSION = "1.0.0"` (no import of `bpy`; `shared/__init__.py` is a bare comment). release-please bumps only `shared/constants.py`.
- Alternative: keep literal version and have release-please bump both files — fallback if `uv sync` misbehaves in CI.

### D3. Release notes table via deterministic filename reconstruction
Each variant emits exactly one `.blend` named `{prefix}_{version}_build{N}_{UTC date}.blend` (per `shared/build_utils.py`). The notes job reconstructs the table from a static variant→prefix map (`CnC_Legacy`, `CnC_LegacyCycles`, `CnC_LegacyEevee`, `CnC_Eevee`, `CnC_CyclesX`, `CnC_EeveeNext`, `CnC_HiFive`), `VERSION` from the tag, `BUILD_NUM` from `git rev-list --count HEAD`, and `date -u +%Y%m%d`.
- Alternative: build jobs emit a per-variant `manifest.json` artifact for the notes job — more robust but more wiring; deferred until the date edge case actually bites.

### D4. Commitlint keeps the standard type enum
Copy `commitlint.config.cjs` + `commitlint.yml` from the toolkit verbatim (both skip the `release-please--branches--main` branch). The enum stays standard (`feat/fix/docs/style/refactor/perf/test/build/ci/chore/revert`) — no `bug` type, because release-please only maps `fix`/`perf`/`revert` → patch and `feat` → minor; a `bug:` commit would not trigger a release.

### D5. First release baseline = 1.0.0
`.release-please-manifest.json` starts at `1.0.0`, matching `shared/constants.py`. The `v1.00-alpha*` tags parse as pre-releases below 1.0.0, so the first Release PR should land on `v1.0.0`. If release-please mis-seeds the baseline from the non-standard tag format, the first release may land on `1.0.1` — low harm, observe and adjust.

## Risks / Trade-offs

- [Dynamic version breaks `uv sync` in CI] → Verify locally (`uv sync --group test` + `uv run pytest tests/`) before pushing; fallback is bumping both files (D2 alternative).
- [Build crosses UTC midnight; notes table links point at wrong date] → Rare; accepted. Switch to manifest-file handoff (D3 alternative) if it recurs.
- [release-please mis-parses `v1.00-alpha4` baseline] → First release might be `1.0.1` not `1.0.0`. Low harm; adjust manifest after observing.
- [Concurrent `softprops/action-gh-release` calls on the same tag] → Known-working pattern; each job uploads distinct files.
- [commitlint fails existing-style PR titles] → Intended enforcement; existing open branches must comply before merge.
