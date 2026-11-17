import sys
import os

workspace_dir = r"c:\Users\Rahul\OneDrive\Desktop\Blender MCP"
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

# Force reload all vastu_modular modules
for mod in list(sys.modules.keys()):
    if mod.startswith("vastu_modular"):
        del sys.modules[mod]

from vastu_modular.main import assemble_scene

assemble_scene()
