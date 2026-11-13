import pytest
from blender_mcp.bmesh_toolkit import (
    create_cushioned_profile,
    create_architectural_wall_with_openings,
    create_profile_sweep_molding,
)

def test_create_cushioned_profile_geometry():
    res = create_cushioned_profile(width=0.8, depth=0.8, thickness=0.15, crown_height=0.04, segments=8)
    assert res["status"] == "success"
    assert res["vert_count"] > 30
    assert res["is_crowned"] is True
    assert res["max_z"] > (0.15 / 2.0)  # Has vertical crown dome

def test_create_architectural_wall_with_window_opening():
    openings = [{"type": "window", "x": 1.5, "z": 0.9, "width": 1.2, "height": 1.4}]
    res = create_architectural_wall_with_openings(length=4.0, height=3.0, thickness=0.25, openings=openings)
    assert res["status"] == "success"
    assert res["thickness"] == 0.25
    assert len(res["openings"]) == 1
    assert res["vert_count"] >= 16

def test_create_profile_sweep_molding():
    path = [(0.0, 0.0, 0.0), (4.0, 0.0, 0.0), (4.0, 3.0, 0.0)]
    res = create_profile_sweep_molding(path_points=path, profile_type="BASEBOARD", height=0.12, depth=0.02)
    assert res["status"] == "success"
    assert res["segments"] >= 2
