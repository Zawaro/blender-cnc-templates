#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load .env if present
if [ -f "$SCRIPT_DIR/.env" ]; then
  set -a
  source "$SCRIPT_DIR/.env"
  set +a
fi

# Map .env variables to Blender executables
declare -A BLENDER_MAP=(
  ["5.1"]="${BLENDER_HI_FIVE:-}"
  ["4.3"]="${BLENDER_EEVEE_NEXT:-}"
  ["3.6"]="${BLENDER_CYCLESX:-}"
  ["2.93"]="${BLENDER_EEVEE:-}"
)

run_version() {
  local ver="$1"
  local exe="${BLENDER_MAP[$ver]:-}"

  if [ -z "$exe" ] || [ ! -x "$exe" ]; then
    echo "SKIP  Blender $ver — executable not found"
    return 0
  fi

  # Clear pytest cache to prevent stale blender_version from poisoning next run
  rm -rf "$SCRIPT_DIR/.pytest_cache"

  echo "==== Blender $ver ===="
  uv run pytest -p pytest-blender --blender-executable "$exe" "$SCRIPT_DIR/tests/" -v
}

# Single-version mode: ./test.sh 5.1
if [ "${1:-}" != "--all" ] && [ -n "${1:-}" ]; then
  run_version "$1"
  exit $?
fi

# No args: usage
if [ "${1:-}" == "" ]; then
  echo "Usage: ./test.sh <version>    Run tests against one Blender version"
  echo "       ./test.sh --all        Run tests against all available versions"
  echo ""
  echo "Versions: 5.1, 4.3, 3.6, 2.93"
  exit 0
fi

# All-variant mode: ./test.sh --all
fail=0
for ver in 5.1 4.3 3.6 2.93; do
  run_version "$ver" || fail=1
done

if [ "$fail" -ne 0 ]; then
  echo "Some versions failed or were skipped"
  exit 1
fi

echo "All versions passed"
