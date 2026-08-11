## Why

Releases are currently manual and inconsistent: `build.sh` is interactive, version bumps require editing `shared/constants.py`, and there is no CHANGELOG. The sibling `blender-cnc-toolkit` repo already has a proven automated release pipeline (release-please + commitlint) that we should adopt so versioning, changelogs, and release assets are generated automatically on merge to `main`.

## What Changes

- Add `release-please` automation: config, manifest, and a GitHub Actions workflow that opens a Release PR on version-worthy commits to `main` and, once merged, builds all 7 variants and attaches assets to the GitHub release.
- Single-source the version: `pyproject.toml` derives its version from `shared/constants.py` (`TEMPLATE_VERSION`) instead of duplicating it.
- Add commitlint enforcement (commit message + PR title) so conventional commits — which release-please depends on for versioning — stay valid.
- Update `AGENTS.md`: release-please-managed versioning, conventional commits/commitlint, git conventions, GitHub CLI, issues & labels, docstring guidance.
- First release lands on `v1.0.0` (existing `v1.00-alpha*` tags are pre-release).

## Capabilities

### New Capabilities
- `release-pipeline`: automated version bumps, CHANGELOG generation, and GitHub releases with per-variant `.blend`/`.zip`/`.7z` assets for all 7 Blender variants.

### Modified Capabilities

## Impact

- `pyproject.toml`, `shared/constants.py` (version single-sourcing; bumping responsibility moves to release-please)
- New files: `release-please-config.json`, `.release-please-manifest.json`, `.github/workflows/release-please.yml`, `.github/workflows/commitlint.yml`, `commitlint.config.cjs`, `CHANGELOG.md` (generated)
- CI: `test.yml` unchanged; release pipeline builds reuse its proven build-test steps and Blender cache.
- Process: all future commits/PRs must follow conventional commits (enforced); version bumps are never done manually.

## Non-goals

- Changing `shared/constants.py` filter sizes or scene-building code.
- Migrating away from `build.sh` for local builds — it stays interactive; the release pipeline uses a non-interactive equivalent.
- Publishing Blender add-ons/extensions (templates are `.blend` scene files, not addons).
- Cleaning up stale `release/` artifacts or old `v1.00-alpha*` tags.
