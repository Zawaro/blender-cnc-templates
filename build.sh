#!/usr/bin/env bash
set -e

echo "=== Blender Addon Build Script (Launcher-aware with per-version venv) ==="
echo

# --- 1) Prompt for engine group / version folder ---
engines=("legacy" "legacy_cycles" "eevee" "cyclesx" "eevee_next" "hi_five")
echo "Select Blender engine group:"
select engine in "${engines[@]}"; do
    [[ -n "$engine" ]] && break
    echo "Invalid choice."
done

# Map engine groups to version ranges
case "$engine" in
    "legacy")         ver_min=2.79; ver_max=2.79 ;;
    "legacy_cycles")  ver_min=2.79; ver_max=2.79 ;;
    "eevee")          ver_min=2.80; ver_max=2.93 ;;
    "cyclesx")        ver_min=3.0;  ver_max=3.6 ;;
    "eevee_next")     ver_min=4.1;  ver_max=4.5 ;;
    "hi_five")    ver_min=5.0;  ver_max=6.0 ;;
esac

echo "Searching for Blender versions matching $ver_min → $ver_max …"
echo

# --- Version compare helpers ---
ver_ge(){ [[ "$1" == "$2" || "$1" == "$(printf '%s\n%s' "$1" "$2" | sort -V | head -n1)" ]]; }
ver_le(){ [[ "$1" == "$2" || "$1" == "$(printf '%s\n%s' "$2" "$1" | sort -V | head -n1)" ]]; }

candidates=()

search_exec(){
    local path="$1"
    [[ ! -x "$path" ]] && return

    local v
    v=$("$path" --version 2>/dev/null | grep -Eo "[0-9]+\.[0-9]+" | head -n1) || return
    if ver_ge "$v" "$ver_min" && ver_le "$v" "$ver_max"; then
        candidates+=("$path|$v")
    fi
}

# --- 2) Search for Blender executables ---
# PATH
if command -v blender &>/dev/null; then
    search_exec "$(command -v blender)"
fi

# Known platform paths
search_exec "/Applications/Blender.app/Contents/MacOS/Blender"
search_exec "/c/Program Files/Blender Foundation/Blender $ver_min/blender.exe"
search_exec "/c/Program Files (x86)/Blender Foundation/Blender $ver_min/blender.exe"
search_exec "$HOME/software/blender-$ver_min/blender"
search_exec "$HOME/blender-$ver_min/blender"
search_exec "/usr/bin/blender"

# --- Blender Launcher library folders (all types) ---
launcher_types=("stable" "daily" "experimental" "custom")
for t in "${launcher_types[@]}"; do
    lib_dir="$HOME/blender/$t"
    [[ -d "$lib_dir" ]] || continue
    for sub in "$lib_dir"/*; do
        search_exec "$sub/blender"
        search_exec "$sub/blender.exe"
    done
done

# --- Pick best match ---
if [[ ${#candidates[@]} -eq 0 ]]; then
    echo "❌ No suitable Blender found!"
    exit 1
fi

best=""
for cand in "${candidates[@]}"; do
    path="${cand%%|*}"
    ver="${cand##*|}"
    if [[ -z "$best" ]] || [[ "$(printf '%s\n%s' "$ver" "${best##*|}" | sort -V | tail -n1)" == "$ver" ]]; then
        best="$path|$ver"
    fi
done

blender_exec="${best%%|*}"
blender_ver="${best##*|}"
echo "Using Blender $blender_ver at: $blender_exec"
echo

# --- 3) Ensure version folder exists ---
if [[ ! -d "./$engine" ]]; then
    echo "❌ Version folder './$engine' not found!"
    exit 1
fi

ver_dir="./$engine"
echo "Using version folder: $ver_dir"
echo

# --- 4) Ensure .venv exists for this version ---
if [[ ! -d "$ver_dir/.venv" ]]; then
    echo "No .venv found for $engine — running bootstrap.sh"
    ./bootstrap.sh
fi

# Activate the version’s .venv
echo "Activating $ver_dir/.venv"
source "$ver_dir/.venv/bin/activate"

# --- 5) Install dependencies from version folder ---
if [[ -f "$ver_dir/requirements.txt" ]]; then
    echo "Installing dependencies from $ver_dir/requirements.txt …"
    uv pip install -r "$ver_dir/requirements.txt"
else
    echo "No requirements.txt found in $ver_dir — skipping."
fi

echo

# --- 6) Run generate_scripts.py ---
if [[ -f "$ver_dir/generate_scripts.py" ]]; then
    echo "Running $ver_dir/generate_scripts.py …"
    uv run python "$ver_dir/generate_scripts.py"
else
    echo "No generate_scripts.py in $ver_dir — skipping."
fi

echo

# --- 7) Run Blender with main.py ---
if [[ -f "$ver_dir/main.py" ]]; then
    echo "Running Blender headlessly for $engine …"
    "$blender_exec" -b --python "$ver_dir/main.py"
else
    echo "No main.py in $ver_dir — nothing to run."
fi

# --- 8) Archive generated .blend files using zip if available, otherwise install py7zr Python lib ---
if hash zip > /dev/null 2>/dev/null; then
    for f in release/*.blend; do
        base=${f%%.*}
        zip_file="${base}.7z"
        if [ ! -e "$zip_file" ]; then
            echo "Creating archive $zip_file …"
            zip -j "$zip_file" "$f"
        else
            echo "Archive $zip_file already exists – skipping."
        fi
    done
else
    echo "No zip utility found – install via your package manager (e.g., apt‑get install zip)."
fi

echo
echo "✅ Build complete for $engine!"
