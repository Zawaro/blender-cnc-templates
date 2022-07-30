#!/bin/bash

source ./env/Scripts/activate

export "PATH=$PATH:/c/Program Files/Blender Foundation/Blender 3.2"

blender -b -P main.py