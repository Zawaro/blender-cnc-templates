## ADDED Requirements

### Requirement: Version is single-sourced
The project SHALL maintain exactly one source of truth for the version, `TEMPLATE_VERSION` in `shared/constants.py`. `pyproject.toml` MUST derive its `version` from that constant rather than duplicating it. Variant folders MUST NOT define their own `TEMPLATE_VERSION`.

#### Scenario: pyproject version derives from shared constant
- **WHEN** `pyproject.toml` is built or inspected
- **THEN** its version resolves from `shared.constants.TEMPLATE_VERSION`

#### Scenario: no version duplication in variant folders
- **WHEN** a variant folder's `constants.py` is read
- **THEN** it does not define `TEMPLATE_VERSION`

### Requirement: Automated version bumps via release-please
On every push to `main`, the `release-please-action` MUST evaluate conventional commits and open a `chore: release` PR that bumps the version and generates the CHANGELOG. The version MUST be bumped only by release-please, never manually.

#### Scenario: version-worthy commits open a Release PR
- **WHEN** a `feat:` or `fix:` commit lands on `main`
- **THEN** release-please opens a Release PR with an incremented version and updated CHANGELOG

#### Scenario: no user-facing commits do not open a Release PR
- **WHEN** only `ci:`/`chore:`/`docs:` commits land on `main`
- **THEN** no Release PR is opened

### Requirement: Release builds all variants
When a release is created, the pipeline MUST build all 7 variants (`legacy`, `legacy_cycles`, `legacy_eevee`, `eevee`, `cyclesx`, `eevee_next`, `hi_five`) using the non-interactive build pattern from `test.yml` (generate scripts, then run Blender headless) and MUST export the build number from the git commit count so `.blend` files are named `{prefix}_{version}_build{N}_{date}.blend`.

#### Scenario: release triggers a full variant build
- **WHEN** release-please creates a release
- **THEN** each of the 7 variants is built and produces a `.blend` in `release/{variant}/`

#### Scenario: build number is embedded in filenames
- **WHEN** a variant build runs with `BUILD_NUMBER` exported
- **THEN** the output `.blend` name includes `_build{N}`

### Requirement: Release assets are published
For each built variant, the pipeline MUST publish the `.blend` file plus `.zip` and `.7z` archives to the GitHub release.

#### Scenario: assets attach to the release
- **WHEN** all variant builds finish
- **THEN** the GitHub release contains each variant's `.blend`, `.zip`, and `.7z`

### Requirement: Release notes include a download table
The release body MUST be rewritten with the CHANGELOG content plus a table listing each variant, its Blender version range, and download links to the `.blend`/`.zip`/`.7z` assets, plus installation steps.

#### Scenario: notes table links resolve to the release
- **WHEN** a user opens the release
- **THEN** each table row links to an asset file named `{prefix}_{version}_build{N}_{date}.{blend|zip|7z}` that exists on the release

### Requirement: Build-number tag created
The pipeline MUST create and push an additional git tag `{tag}_build{N}` (e.g. `v1.0.0_build42`) on release.

#### Scenario: build tag pushed after release
- **WHEN** a release is created
- **THEN** a `{tag}_build{N}` tag exists on the released commit

### Requirement: Commits and PR titles follow conventional commits
Commit messages and PR titles MUST follow the Conventional Commits format as enforced by commitlint, using only the standard types (`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`). The commitlint checks MUST be skipped for the release-please branch (`release-please--branches--main`).

#### Scenario: non-conventional commit message is rejected
- **WHEN** a PR contains a commit whose subject lacks a valid type prefix
- **THEN** commitlint marks the check as failed

#### Scenario: release-please branch is exempt
- **WHEN** commitlint runs on a PR from `release-please--branches--main`
- **THEN** the commitlint checks are skipped
