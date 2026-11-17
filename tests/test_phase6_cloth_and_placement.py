import pytest
from blender_mcp.cloth_engine import (
    setup_cloth_physics,
    bake_cloth_drop,
    inspect_cloth_simulation,
    CLOTH_PRESETS
)
from blender_mcp.placement_engine import (
    snap_to_surface,
    align_object_to_surface,
    scatter_instances,
    inspect_scatter_result
)


def test_cloth_presets():
    assert "cotton" in CLOTH_PRESETS
    assert "silk" in CLOTH_PRESETS
    assert "denim" in CLOTH_PRESETS
    assert "wool" in CLOTH_PRESETS


def test_setup_cloth_physics_contract():
    res = setup_cloth_physics("Plane", preset="silk", mass=0.15)
    assert res["success"] is True
    assert res["tool"] == "setup_cloth_physics"
    assert res["result"]["preset"] == "silk"


def test_bake_cloth_drop_contract():
    res = bake_cloth_drop("Plane", collision_objects=["Cube"], steps=30, apply_result=True)
    assert res["success"] is True
    assert res["tool"] == "bake_cloth_drop"
    assert res["result"]["applied_as_static_mesh"] is True


def test_snap_to_surface_contract():
    res = snap_to_surface("Pillow", "Bed_Mattress", offset=0.01)
    assert res["success"] is True
    assert res["tool"] == "snap_to_surface"


def test_scatter_instances_contract():
    res = scatter_instances("Props_Collection", "Terrain_Surface", count=15, seed=123)
    assert res["success"] is True
    assert res["tool"] == "scatter_instances"
    assert res["result"]["instances_placed"] == 15
