#!/bin/bash

source ./env/Scripts/activate

python ./generate_scripts.py

export "PATH=$PATH:/c/Program Files/Blender Foundation/Blender 2.93"

blender -b -P main.py