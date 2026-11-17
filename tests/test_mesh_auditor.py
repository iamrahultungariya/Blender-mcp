import pytest
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_audit_mesh_topology_contract():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "def audit_mesh_topology" in content
    assert '"audit_mesh_topology":' in content or "cmd_type == \"audit_mesh_topology\"" in content
    assert "non_manifold_edges" in content
    assert "is_watertight" in content

def test_pure_topology_auditor_watertight_cube():
    from blender_mcp.mesh_auditor import audit_geometry_topology

    # 8 vertices, 6 quad faces (cube)
    verts = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ]
    # Outward CCW faces
    faces = [
        [0, 3, 2, 1], [4, 5, 6, 7],
        [0, 1, 5, 4], [2, 3, 7, 6],
        [0, 4, 7, 3], [1, 2, 6, 5]
    ]

    report = audit_geometry_topology(verts, faces)
    assert report["is_watertight"] is True
    assert report["non_manifold_edges"] == 0
    assert report["open_boundary_edges"] == 0
    assert report["loose_verts"] == 0
    assert report["status"] == "PASS"

def test_pure_topology_auditor_open_boundary():
    from blender_mcp.mesh_auditor import audit_geometry_topology

    # Single quad face (open boundary)
    verts = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    faces = [[0, 1, 2, 3]]

    report = audit_geometry_topology(verts, faces)
    assert report["is_watertight"] is False
    assert report["open_boundary_edges"] == 4
    assert report["status"] == "FAIL"

def test_pure_topology_auditor_non_manifold_t_junction():
    from blender_mcp.mesh_auditor import audit_geometry_topology

    # 3 quads sharing the edge between v1 and v2 (non-manifold)
    verts = [
        [0, 0, 0], [0, 1, 0],  # Shared edge: (0, 1)
        [1, 0, 0], [1, 1, 0],  # Face 1: [0, 1, 3, 2]
        [-1, 0, 0], [-1, 1, 0], # Face 2: [0, 1, 5, 4]
        [0, 0, 1], [0, 1, 1]   # Face 3: [0, 1, 7, 6]
    ]
    faces = [
        [0, 1, 3, 2],
        [0, 1, 5, 4],
        [0, 1, 7, 6]
    ]

    report = audit_geometry_topology(verts, faces)
    assert report["non_manifold_edges"] >= 1
    assert report["is_watertight"] is False
    assert report["status"] == "FAIL"

def test_pure_topology_auditor_loose_verts():
    from blender_mcp.mesh_auditor import audit_geometry_topology

    verts = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [99, 99, 99]]
    faces = [[0, 1, 2, 3]]

    report = audit_geometry_topology(verts, faces)
    assert report["loose_verts"] == 1
