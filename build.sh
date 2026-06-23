#!/usr/bin/env bash
set -e

echo "=== Blender Addon Build Script (Launcher-aware with per-version venv) ==="
echo

# --- 0) Load .env if present ---
ENV_FILE=".env"
if [[ -f "$ENV_FILE" ]]; then
    echo "Loading Blender paths from $ENV_FILE"
    # Only export BLENDER_* variables from .env
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        [[ "$key" =~ ^BLENDER_ ]] && export "$key=$value"
    done < "$ENV_FILE"
    echo
fi

# --- 1) Compute build number from git commit count ---
BUILD_NUMBER=$(git rev-list --count HEAD 2>/dev/null || echo "0")
export BUILD_NUMBER
echo "Build number: $BUILD_NUMBER"
echo

# --- 2) Prompt for engine group / version folder ---
engines=("legacy" "legacy_cycles" "eevee" "cyclesx" "eevee_next" "hi_five")
echo "Select Blender engine group:"
select engine in "${engines[@]}"; do
    [[ -n "$engine" ]] && break
    echo "Invalid choice."
done

# Map engine groups to .env variable names and version ranges
case "$engine" in
    "legacy")         env_var="BLENDER_LEGACY";         ver_min=2.79; ver_max=2.79 ;;
    "legacy_cycles")  env_var="BLENDER_LEGACY_CYCLES";  ver_min=2.79; ver_max=2.79 ;;
    "eevee")          env_var="BLENDER_EEVEE";          ver_min=2.80; ver_max=2.93 ;;
    "cyclesx")        env_var="BLENDER_CYCLESX";        ver_min=3.0;  ver_max=3.6 ;;
    "eevee_next")     env_var="BLENDER_EEVEE_NEXT";     ver_min=4.1;  ver_max=4.5 ;;
    "hi_five")        env_var="BLENDER_HI_FIVE";        ver_min=5.0;  ver_max=6.0 ;;
esac

# --- 3) Resolve Blender executable ---
blender_exec=""

# Try .env path first
env_path="${!env_var:-}"
if [[ -n "$env_path" && -x "$env_path" ]]; then
    blender_exec="$env_path"
    blender_ver=$("$blender_exec" --version 2>/dev/null | grep -Eo "[0-9]+\.[0-9]+" | head -n1)
    echo "Using Blender $blender_ver from $ENV_FILE: $blender_exec"
else
    # Fall back to filesystem search
    echo "No valid path in $ENV_FILE for $env_var — searching system…"
    echo "Searching for Blender versions matching $ver_min → $ver_max …"
    echo

    # --- Version compare helpers ---
    ver_ge(){ [[ "$1" == "$2" || "$1" == "$(printf '%s\n%s' "$1" "$2" | sort -V | tail -n1)" ]]; }
    ver_le(){ [[ "$1" == "$2" || "$1" == "$(printf '%s\n%s' "$1" "$2" | sort -V | head -n1)" ]]; }

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

    # Blender Launcher library folders
    launcher_types=("stable" "daily" "experimental" "custom")
    for t in "${launcher_types[@]}"; do
        lib_dir="$HOME/blender/$t"
        [[ -d "$lib_dir" ]] || continue
        for sub in "$lib_dir"/*; do
            search_exec "$sub/blender"
            search_exec "$sub/blender.exe"
        done
    done

    # Pick best match
    if [[ ${#candidates[@]} -eq 0 ]]; then
        echo "❌ No suitable Blender found! Set $env_var in $ENV_FILE or install Blender."
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

    # Prompt to save to .env
    echo
    read -rp "Save this path to $ENV_FILE for next time? [Y/n] " save_choice
    save_choice="${save_choice:-Y}"
    if [[ "$save_choice" =~ ^[Yy] ]]; then
        if [[ -f "$ENV_FILE" ]]; then
            sed -i "s|^${env_var}=.*|${env_var}=${blender_exec}|" "$ENV_FILE"
        else
            echo "${env_var}=${blender_exec}" > "$ENV_FILE"
        fi
        echo "Saved to $ENV_FILE"
    fi
fi

echo

# --- 4) Ensure version folder exists ---
if [[ ! -d "./$engine" ]]; then
    echo "❌ Version folder './$engine' not found!"
    exit 1
fi

ver_dir="./$engine"
echo "Using version folder: $ver_dir"
echo

# --- 5) Ensure .venv exists for this version ---
if [[ ! -d "$ver_dir/.venv" ]]; then
    echo "No .venv found for $engine — running bootstrap.sh"
    ./bootstrap.sh
fi

# Activate the version's .venv
echo "Activating $ver_dir/.venv"
source "$ver_dir/.venv/bin/activate"

# --- 6) Install dependencies from version folder ---
if [[ -f "$ver_dir/requirements.txt" ]]; then
    echo "Installing dependencies from $ver_dir/requirements.txt …"
    uv pip install -r "$ver_dir/requirements.txt"
else
    echo "No requirements.txt found in $ver_dir — skipping."
fi

echo

# --- 7) Run generate_scripts.py ---
if [[ -f "$ver_dir/generate_scripts.py" ]]; then
    echo "Running $ver_dir/generate_scripts.py …"
    uv run python "$ver_dir/generate_scripts.py"
else
    echo "No generate_scripts.py in $ver_dir — skipping."
fi

echo

# --- 8) Run Blender with main.py ---
if [[ -f "$ver_dir/main.py" ]]; then
    echo "Running Blender headlessly for $engine …"
    "$blender_exec" -b --python "$ver_dir/main.py"
else
    echo "No main.py in $ver_dir — nothing to run."
fi

# --- 9) Verify archive tools are available ---
if ! hash zip > /dev/null 2>/dev/null; then
    echo "❌ 'zip' not found — install via your package manager (e.g. apt-get install zip)."
    exit 1
fi
if ! hash 7z > /dev/null 2>/dev/null; then
    echo "❌ '7z' not found — install via your package manager (e.g. apt-get install p7zip-full)."
    exit 1
fi

# --- 10) Archive generated .blend files ---
for f in "release/$engine"/*.blend; do
    base=${f%%.*}
    zip_file="${base}.zip"
    sevenz_file="${base}.7z"

    if [ ! -e "$zip_file" ]; then
        echo "Creating $zip_file …"
        zip -j "$zip_file" "$f"
    fi

    if [ ! -e "$sevenz_file" ]; then
        echo "Creating $sevenz_file …"
        7z a -t7z -mx=9 "$sevenz_file" "$f"
    fi
done

echo
echo "✅ Build complete for $engine!"
