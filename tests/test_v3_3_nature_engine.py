"""Unit tests for Phase V3.3 Nature & Organic Environment Engine.

Verifies parametric grass blade cluster generation with translucent foliage materials,
procedural Geometry Nodes grass field scattering with Musgrave density masks,
rolling terrain mesh generation, and multi-asset foliage scattering.
"""

import pytest
from blender_mcp.nature_engine import (
    create_grass_blade_cluster,
    create_grass_field,
    create_terrain_ground,
    scatter_foliage
)


def test_create_grass_blade_cluster():
    """Verify create_grass_blade_cluster generates curved grass blades and dead stalks."""
    res = create_grass_blade_cluster(
        blade_count=16,
        height=0.4,
        curve_intensity=0.85,
        dead_blade_ratio=0.25,
        name="Wild_Grass_Cluster"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Wild_Grass_Cluster"
    assert result["blade_count"] == 16
    assert result["dead_stalk_count"] >= 3
    assert result["vertex_count"] > 40
    assert result["face_count"] > 20
    assert result["has_translucent_material"] is True


def test_create_grass_field_scattering():
    """Verify create_grass_field configures Geometry Nodes procedural scattering."""
    res = create_grass_field(
        target_ground="Ground_Plane",
        density=180.0,
        patchiness=0.65,
        scale_range=(0.6, 1.4),
        seed=101
    )
    assert res["success"] is True
    result = res["result"]
    assert result["target_ground"] == "Ground_Plane"
    assert result["density"] == 180.0
    assert result["patchiness"] == 0.65
    assert result["has_geometry_nodes"] is True


def test_create_terrain_ground():
    """Verify create_terrain_ground generates displaced quad terrain mesh."""
    res = create_terrain_ground(
        width=12.0,
        length=12.0,
        resolution=30,
        height_variation=0.8,
        noise_scale=2.0,
        name="Lush_Hillside"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Lush_Hillside"
    assert result["width"] == 12.0
    assert result["length"] == 12.0
    assert result["vertex_count"] == (30 + 1) * (30 + 1)
    assert result["face_count"] == 30 * 30


def test_scatter_foliage_system():
    """Verify scatter_foliage generates multi-asset scatter distribution with slope cutoff."""
    res = scatter_foliage(
        target_surface="Lush_Hillside",
        asset_types=["grass", "weeds", "fallen_leaves"],
        density_preset="lush",
        slope_limit_deg=40.0,
        name="Hillside_Foliage"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["target_surface"] == "Lush_Hillside"
    assert result["density_preset"] == "lush"
    assert result["slope_limit_deg"] == 40.0
    assert len(result["asset_types"]) == 3
