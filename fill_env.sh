#!/usr/bin/env bash
set -e

ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

if [[ ! -f "$ENV_EXAMPLE" ]]; then
  echo "Error: $ENV_EXAMPLE not found"
  exit 1
fi

# Version ranges for each folder
declare -A VER_MIN VER_MAX
VER_MIN[legacy]=2.79;       VER_MAX[legacy]=2.79
VER_MIN[legacy_cycles]=2.79; VER_MAX[legacy_cycles]=2.79
VER_MIN[eevee]=2.80;        VER_MAX[eevee]=2.93
VER_MIN[cyclesx]=3.0;       VER_MAX[cyclesx]=3.6
VER_MIN[eevee_next]=4.1;    VER_MAX[eevee_next]=4.5
VER_MIN[hi_five]=5.0;       VER_MAX[hi_five]=6.0

ver_ge(){ [[ "$1" == "$2" || "$1" == "$(printf '%s\n%s' "$1" "$2" | sort -V | tail -n1)" ]]; }
ver_le(){ [[ "$1" == "$2" || "$1" == "$(printf '%s\n%s' "$1" "$2" | sort -V | head -n1)" ]]; }

check_blender(){
  local path="$1"
  [[ ! -x "$path" ]] && return 1
  local v
  v=$("$path" --version 2>/dev/null | grep -Eo "[0-9]+\.[0-9]+" | head -n1) || return 1
  echo "$v"
}

find_best(){
  local vmin="$1" vmax="$2"
  local best="" best_v=""
  local candidates=()

  # PATH
  if command -v blender &>/dev/null; then
    local v
    v=$(check_blender "$(command -v blender)") || true
    if [[ -n "$v" ]] && ver_ge "$v" "$vmin" && ver_le "$v" "$vmax"; then
      candidates+=("$(command -v blender)|$v")
    fi
  fi

  # Known platform paths
  for p in \
    "/Applications/Blender.app/Contents/MacOS/Blender" \
    "$HOME/software/blender-$vmin/blender" \
    "$HOME/blender-$vmin/blender" \
    "/usr/bin/blender"; do
    local v
    v=$(check_blender "$p") || true
    if [[ -n "$v" ]] && ver_ge "$v" "$vmin" && ver_le "$v" "$vmax"; then
      candidates+=("$p|$v")
    fi
  done

  # Blender Launcher library folders
  for t in stable daily experimental custom; do
    local lib_dir="$HOME/blender/$t"
    [[ -d "$lib_dir" ]] || continue
    for sub in "$lib_dir"/*; do
      for bin in "$sub/blender" "$sub/blender.exe"; do
        local v
        v=$(check_blender "$bin") || true
        if [[ -n "$v" ]] && ver_ge "$v" "$vmin" && ver_le "$v" "$vmax"; then
          candidates+=("$bin|$v")
        fi
      done
    done
  done

  # Pick best match (highest version)
  for cand in "${candidates[@]}"; do
    local path="${cand%%|*}"
    local v="${cand##*|}"
    if [[ -z "$best" ]] || [[ "$(printf '%s\n%s' "$v" "$best_v" | sort -V | tail -n1)" == "$v" ]]; then
      best="$path"
      best_v="$v"
    fi
  done

  echo "$best"
}

echo "=== Blender binary auto-detection ==="
echo

# Start from .env.example
cp "$ENV_EXAMPLE" "$ENV_FILE"

declare -A FOUND
for folder in legacy legacy_cycles eevee cyclesx eevee_next hi_five; do
  var_name="BLENDER_$(echo "$folder" | tr '[:lower:]' '[:upper:]' | tr '-' '_')"
  path=$(find_best "${VER_MIN[$folder]}" "${VER_MAX[$folder]}")
  if [[ -n "$path" ]]; then
    FOUND[$var_name]="$path"
    echo "  $var_name = $path"
  else
    echo "  $var_name = (not found)"
  fi
done

echo

# Write values into .env
for var_name in "${!FOUND[@]}"; do
  if [[ -n "${FOUND[$var_name]}" ]]; then
    sed -i "s|^${var_name}=.*|${var_name}=${FOUND[$var_name]}|" "$ENV_FILE"
  fi
done

echo "Written to $ENV_FILE"
echo
echo "Edit $ENV_FILE to adjust paths manually if needed."
