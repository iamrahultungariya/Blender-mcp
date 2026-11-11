import numpy as np
import pytest
from blender_mcp.kernel.curvature_pbr_compiler import (
    compute_laplacian_curvature,
    build_triplanar_pbr_spec,
    calculate_bottom_pivot_offset,
)

def test_compute_laplacian_curvature_cube():
    # 8 vertices of unit cube [-1, 1]^3
    from itertools import product
    verts = np.array(list(product([-1.0, 1.0], repeat=3)), dtype=np.float32)
    # 6 quad faces
    faces = [
        [0, 1, 3, 2], # -X
        [4, 6, 7, 5], # +X
        [0, 4, 5, 1], # -Y
        [2, 3, 7, 6], # +Y
        [0, 2, 6, 4], # -Z
        [1, 5, 7, 3], # +Z
    ]
    curv = compute_laplacian_curvature(verts, faces)
    assert len(curv) == len(verts)
    # Cube corners are all convex, so curvature should be positive
    assert np.all(curv > 0.0)

def test_calculate_bottom_pivot_offset():
    # Geometry spanning X: [-2, 2], Y: [-1, 1], Z: [3, 7]
    verts = np.array([
        [-2.0, -1.0, 3.0],
        [ 2.0,  1.0, 7.0],
    ], dtype=np.float32)

    offset = calculate_bottom_pivot_offset(verts)
    # Center X=0, Center Y=0, Min Z=3.0
    assert np.allclose(offset, [0.0, 0.0, 3.0], atol=1e-5)

def test_build_triplanar_pbr_spec():
    spec = build_triplanar_pbr_spec("CarPaint_Red", base_color=[0.8, 0.0, 0.0, 1.0], metallic=0.9, roughness=0.2)
    assert spec["material_name"] == "CarPaint_Red"
    assert spec["metallic"] == 0.9
    assert spec["roughness"] == 0.2
    assert "attribute_name" in spec
    assert spec["attribute_name"] == "McpCurvatureAO"
