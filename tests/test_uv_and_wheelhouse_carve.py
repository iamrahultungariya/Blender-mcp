import pytest
from pathlib import Path

def test_uv_unwrapping_toolkit_interface():
    from blender_mcp.bmesh_toolkit import apply_smart_uv_unwrapping
    # Calling with None should return skipped
    res = apply_smart_uv_unwrapping(None)
    assert res.get("status") == "skipped_or_no_bpy"

def test_carve_wheel_well_cavity_interface():
    from blender_mcp.bmesh_toolkit import carve_wheel_well_cavities
    # Calling with None should return skipped
    res = carve_wheel_well_cavities(None, {})
    assert res.get("status") == "skipped_or_no_bpy"
