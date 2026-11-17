import pytest
from blender_mcp.topology_engine import (
    repair_mesh_topology,
    decimate_mesh,
    quad_remesh,
    generate_lod_chain
)


def test_repair_mesh_topology_contract():
    res = repair_mesh_topology("Cube", remove_doubles=True, remove_loose=True, fix_normals=True)
    assert res["success"] is True
    assert res["tool"] == "repair_mesh_topology"
    assert res["risk"] == "DESTRUCTIVE"


def test_decimate_mesh_contract():
    res = decimate_mesh("Cube", target_ratio=0.5, apply_modifier=False)
    assert res["success"] is True
    assert res["tool"] == "decimate_mesh"
    assert res["result"]["target_ratio"] == 0.5


def test_decimate_mesh_invalid_ratio():
    res = decimate_mesh("Cube", target_ratio=1.5)
    assert res["success"] is False
    assert len(res["errors"]) > 0


def test_quad_remesh_contract():
    res = quad_remesh("Cube", target_quads=2000)
    assert res["success"] is True
    assert res["tool"] == "quad_remesh"
    assert res["risk"] == "DESTRUCTIVE"


def test_generate_lod_chain_contract():
    res = generate_lod_chain("Cube", lod_ratios=[1.0, 0.5, 0.25])
    assert res["success"] is True
    assert res["tool"] == "generate_lod_chain"
    assert res["result"]["total_lods"] == 3
