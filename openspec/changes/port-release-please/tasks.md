## 1. Version single-sourcing

- [x] 1.1 Add `[build-system]` (setuptools) to `pyproject.toml`
- [x] 1.2 Change `[project]` to `dynamic = ["version"]` and drop the literal `version = "1.0.0"` line
- [x] 1.3 Add `[tool.setuptools.dynamic] version = { attr = "shared.constants.TEMPLATE_VERSION" }`
- [x] 1.4 Verify locally: `uv sync --group test` works and `uv run pytest tests/` passes (version tests green). If `uv sync` breaks, fall back to bumping both `shared/constants.py` and `pyproject.toml` (see design D2)

## 2. Release-please config

- [x] 2.1 Add `release-please-config.json` (release-type `simple`, conventional commits, `extra-files: ["shared/constants.py"]`, changelog-sections mirroring the toolkit)
- [x] 2.2 Add `.release-please-manifest.json` with `{".": "1.0.0"}`

## 3. Release workflow

- [x] 3.1 Add `.github/workflows/release-please.yml` (on push to `main`, `permissions: contents + pull-requests: write`) with a `release-please` job using `googleapis/release-please-action@v4` (token + config + manifest)
- [x] 3.2 Add a `build` matrix job (7 variants, same `include` table and Blender cache key `build-blender-*` as `test.yml`) that: checks out, setup-uv, downloads/caches Blender via blender-downloader, installs `libglu1-mesa` for 2.79, exports `BUILD_NUMBER=$(git rev-list --count HEAD)`, runs `generate_scripts.py` + `blender -b --python main.py`, then creates `.zip` + `.7z` (p7zip) per `.blend`
- [x] 3.3 Have the `build` job upload `.blend`/`.zip`/`.7z` to the release via `softprops/action-gh-release` using the tag from the release-please job outputs
- [x] 3.4 Add a `notes` job (needs all build jobs) that formats the release body: extracts the CHANGELOG via `gh release view`, builds the download table from the variant→prefix map + tag version + build number + `date -u +%Y%m%d`, appends install steps, and runs `gh release edit --notes-file`
- [x] 3.5 Have the `notes` job create and push the `{tag}_build{N}` git tag

## 4. Commitlint

- [x] 4.1 Copy `commitlint.config.cjs` from the toolkit (standard type enum, no `bug`)
- [x] 4.2 Copy `.github/workflows/commitlint.yml` from the toolkit (both jobs skip `release-please--branches--main`)

## 5. AGENTS.md updates

- [x] 5.1 Rewrite the Version management section for release-please (Release PR flow; version is never bumped manually)
- [x] 5.2 Add Conventional Commits / commitlint guidance to the linting/testing section
- [x] 5.3 Add GitHub CLI section (`gh issue create/list`, `gh pr view`)
- [x] 5.4 Add Issues & labels section (bug / enhancement / documentation / good first issue / help wanted)
- [x] 5.5 Add docstring guidance: keep short docstrings, match existing style (`shared/*.py`) — no no-docstring rule

## 6. Verify

- [x] 6.1 Run `uv run ruff check .` — no lint regressions
- [x] 6.2 Run `uv run pytest tests/ -v` (non-bpy tier) — all pass with the dynamic version
- [x] 6.3 Confirm `openspec validate --all` passes for the change
