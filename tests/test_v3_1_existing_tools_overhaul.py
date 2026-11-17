"""Unit tests for Phase V3.1 Existing Tools Overhaul.

Tests cloth simulation zero-g pressure inflation, translucent foliage & velvet shaders,
and organic puffed cushion profiling with welt seam piping and corner pinching.
"""

import pytest
from blender_mcp.cloth_engine import setup_cloth_physics, inspect_cloth_simulation
from blender_mcp.material_engine import create_procedural_shader
from blender_mcp.bmesh_toolkit import create_cushioned_profile


def test_cloth_physics_pressure_and_zero_gravity():
    """Verify cloth physics accepts pressure, gravity_scale, and shrink_factor for pillow/sofa inflation."""
    res = setup_cloth_physics(
        cloth_object="Pillow_Mesh",
        preset="cotton",
        pressure=3.5,
        pressure_factor=1.2,
        gravity_scale=0.0,
        shrink_factor=0.15,
        quality_steps=6
    )
    assert res["success"] is True
    result = res["result"]
    assert result["cloth_object"] == "Pillow_Mesh"
    assert result["preset"] == "cotton"
    assert "pressure" in result["parameters"]
    assert result["parameters"]["pressure"] == 3.5
    assert result["parameters"]["gravity_scale"] == 0.0
    assert result["parameters"]["shrink_factor"] == 0.15


def test_material_engine_translucent_foliage_preset():
    """Verify procedural shader supports translucent_foliage preset for natural grass/leaves."""
    res = create_procedural_shader(
        material_name="Grass_Blade_Translucent",
        preset="translucent_foliage",
        scale=2.0,
        color_tint=(0.15, 0.45, 0.08, 1.0)
    )
    assert res["success"] is True
    assert res["result"]["preset"] == "translucent_foliage"
    assert res["result"]["material_name"] == "Grass_Blade_Translucent"


def test_material_engine_velvet_fabric_preset():
    """Verify procedural shader supports velvet_fabric preset with sheen."""
    res = create_procedural_shader(
        material_name="Luxury_Sofa_Velvet",
        preset="velvet_fabric",
        scale=1.5,
        color_tint=(0.2, 0.05, 0.15, 1.0),
        roughness_multiplier=0.9
    )
    assert res["success"] is True
    assert res["result"]["preset"] == "velvet_fabric"


def test_cushioned_profile_pinch_and_welt():
    """Verify cushioned profile generator supports corner pinching, welt piping, and tufting grid."""
    res = create_cushioned_profile(
        width=0.8,
        depth=0.8,
        thickness=0.2,
        crown_height=0.05,
        segments=8,
        pinch_corners=True,
        welt_depth=0.015,
        tufting_grid=(3, 3)
    )
    assert "vertices" in res
    assert "faces" in res
    assert len(res["vertices"]) > 0
    assert len(res["faces"]) > 0
    assert res.get("pinch_corners") is True
    assert res.get("has_welt") is True
    assert res.get("tufting_points") == 9
