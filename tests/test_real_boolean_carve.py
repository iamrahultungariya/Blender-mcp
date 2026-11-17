import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_clas_boolean_not_fake_stub():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Must use actual BOOLEAN modifier with DIFFERENCE
    assert '"BOOLEAN"' in content or "'BOOLEAN'" in content
    assert 'operation = "DIFFERENCE"' in content or "operation='DIFFERENCE'" in content
    assert "cutter_obj" in content

def test_boolean_carve_toolkit_helper():
    from blender_mcp import bmesh_toolkit
    assert hasattr(bmesh_toolkit, "carve_cavity")
    assert hasattr(bmesh_toolkit, "boolean_difference")
