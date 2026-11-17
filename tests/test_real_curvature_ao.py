import pytest
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_pbr_curvature_not_empty_stub():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate pbr_compile_curvature_ao function body
    start = content.find("def pbr_compile_curvature_ao")
    assert start != -1
    func_body = content[start:start+2500]

    # Old fake stub only had:
    # color_layer = mesh.attributes.new(name="McpCurvatureAO", type='BYTE_COLOR', domain='CORNER')
    # return {"object": object_name, "attribute": "McpCurvatureAO", "computed": True}
    assert "foreach_set" in func_body
    assert "laplacian" in func_body.lower() or "neighbors" in func_body.lower()


def test_discrete_laplacian_curvature_math():
    from blender_mcp.bmesh_toolkit import compute_laplacian_curvature

    # Create a pyramid: base at z=0, apex at z=1
    verts = np.array([
        [-1.0, -1.0, 0.0],
        [ 1.0, -1.0, 0.0],
        [ 1.0,  1.0, 0.0],
        [-1.0,  1.0, 0.0],
        [ 0.0,  0.0, 1.0],  # Apex (vertex 4)
    ], dtype=np.float32)

    # Edges connecting base to apex
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (0, 4), (1, 4), (2, 4), (3, 4)
    ]
    # Apex normal points straight up +Z
    normals = np.array([
        [-0.5, -0.5, 0.7],
        [ 0.5, -0.5, 0.7],
        [ 0.5,  0.5, 0.7],
        [-0.5,  0.5, 0.7],
        [ 0.0,  0.0, 1.0],
    ], dtype=np.float32)

    curvature = compute_laplacian_curvature(verts, edges, normals)
    assert len(curvature) == 5
    # The apex (idx 4) has neighbors with z=0, so (neighbor - apex).z < 0.
    # Dot product with normal (0,0,1) must be strictly negative (convex peak/sharp edge)!
    assert curvature[4] < 0.0
