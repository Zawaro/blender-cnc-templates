#!/bin/bash

# Function to create Python virtual environment if it doesn't exist
create_python_venv() {
    if [ ! -d "./env" ]; then
        echo "Python virtual environment not found. Creating venv..."

        # Check if Python 3 is available
        if command -v python3 &>/dev/null; then
            python3 -m venv ./env
        elif command -v python &>/dev/null; then
            python -m venv ./env
        else
            echo "Python is not installed. Please install Python 3 to continue."
            exit 1
        fi

        echo "Virtual environment created."
    else
        echo "Virtual environment already exists."
    fi
}

# Function to activate Python virtual environment
activate_venv() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if [ -f "./env/bin/activate" ]; then
            source ./env/bin/activate
        else
            echo "Virtual environment activation script not found for Linux."
            exit 1
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows (Git Bash, Cygwin, or WSL)
        if [ -f "./env/Scripts/activate" ]; then
            source ./env/Scripts/activate
        else
            echo "Virtual environment activation script not found for Windows."
            exit 1
        fi
    else
        echo "Unsupported OS: $OSTYPE"
        exit 1
    fi
}

# Function to locate Blender 2.79 on Linux
find_blender_linux() {
    echo "Searching for Blender 2.79 on Linux..."

    # Typical locations with version-specific checks
    paths=(
        "/usr/bin/blender"
        "/usr/local/bin/blender"
        "$HOME/blender_versions/blender-2.79*/blender"
        "$HOME/blender/stable/blender-2.79*/blender"
        "/opt/blender/blender-2.79*/blender"
    )

    for path in "${paths[@]}"; do
        if [ -x "$path" ]; then
            # Check if the version is 2.79
            version=$("$path" --version | grep -o "Blender 2.79")
            if [ "$version" == "Blender 2.79" ]; then
                echo "Blender 2.79 found at: $path"
                export BLENDER_PATH="$path"
                return
            fi
        fi
    done

    echo "Blender 2.79 not found in default locations."
    exit 1
}

# Function to locate Blender 2.79 on Windows
find_blender_windows() {
    echo "Searching for Blender 2.79 on Windows..."

    # Converting Windows paths to Linux format using /mnt/c for Git Bash, Cygwin, or WSL
    paths=(
        "/mnt/c/Program Files/Blender Foundation/Blender 2.79*/blender.exe"
        "/mnt/c/Program Files/Blender Foundation/Blender 2.79*/blender.exe"
        "/mnt/c/Program Files (x86)/Blender Foundation/Blender 2.79*/blender.exe"
        "/mnt/c/Users/$USER/AppData/Local/Blender Foundation/Blender 2.79*/blender.exe"
    )

    for path in "${paths[@]}"; do
        if [ -f "$path" ]; then
            # Check if the version is 2.79
            version=$("$path" --version | grep -o "Blender 2.79")
            if [ "$version" == "Blender 2.79" ]; then
                echo "Blender 2.79 found at: $path"
                export BLENDER_PATH="$path"
                return
            fi
        fi
    done

    echo "Blender 2.79 not found in default locations."
    exit 1
}

# Detect the OS and locate Blender
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    find_blender_linux
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    find_blender_windows
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# If Blender was found, append it to the PATH and run the script
if [ -n "$BLENDER_PATH" ]; then
    echo "Using Blender located at: $BLENDER_PATH"
    export PATH="$PATH:$(dirname "$BLENDER_PATH")"
else
    echo "Blender path not found. Exiting."
    exit 1
fi

# Activate the Python virtual environment
create_python_venv
activate_venv
pip install -r requirements.txt

# Run the Python script to generate any necessary Blender scripts
python ./generate_scripts.py

# Run Blender with the script
"$BLENDER_PATH" -b -P main.py
