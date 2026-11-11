import ast
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"
BUNDLED_PATH = REPO_ROOT / "src" / "blender_mcp" / "bundled" / "addon.py"

def test_addon_contains_toolkit_and_thinking_in_namespace():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Must inject bmesh, mathutils, math, toolkit, thinking into execute_code namespace
    assert '"toolkit":' in content or "'toolkit':" in content
    assert '"thinking":' in content or "'thinking':" in content
    assert '"bmesh":' in content or "'bmesh':" in content
    assert '"mathutils":' in content or "'mathutils':" in content

def test_addon_contains_bmesh_toolkit_definitions():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "class BMeshToolkit" in content or "def create_filleted_box" in content
    assert "class VehicleThinkingEngine" in content

def test_bundled_addon_identical_to_root():
    with open(ADDON_PATH, "rb") as f1, open(BUNDLED_PATH, "rb") as f2:
        assert f1.read() == f2.read(), "addon.py and src/blender_mcp/bundled/addon.py must be in sync"
