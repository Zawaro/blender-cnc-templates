#!/usr/bin/env bash
set -e

echo "=== Initialize per-version virtual environments with uv ==="
echo

# List all version folders (adjust if you add more)
versions=(
  "legacy"
  "legacy_cycles"
  "legacy_eevee"
  "eevee"
  "cyclesx"
  "eevee_next"
  "hi_five"
)

# Make sure uv is installed
if ! command -v uv &>/dev/null; then
    echo "uv not found — installing globally..."
    python3 -m pip install uv
fi

for ver in "${versions[@]}"; do
    if [[ -d "./$ver" ]]; then
        echo "--- Setting up .venv for '$ver' ---"
        pushd "./$ver" >/dev/null

        # Create .venv using uv (will use default Python)
        if [[ ! -d ".venv" ]]; then
            echo "Creating .venv in $ver..."
            uv venv .venv
        else
            echo "Found existing .venv in $ver — skipping creation."
        fi

        # Activate and install fake-bpy-module by default for IDE support
        source .venv/bin/activate
        echo "Installing default dev dependencies (fake-bpy-module) into $ver/.venv"
        uv pip install fake-bpy-module

        deactivate

        popd >/dev/null
        echo
    else
        echo "Folder '$ver' not found — skipping"
    fi
done

echo "✅ bootstrap.sh completed, .venv created."
