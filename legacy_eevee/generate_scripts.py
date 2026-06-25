import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(current_path)
sys.path.append(parent_path)

from shared.compat import get_compat
from shared.script_gen import generate_all_scripts

compat = get_compat(2, 80)
generate_all_scripts(compat, os.path.join(current_path, "scripts"), os.path.join(current_path, "README.md"))
