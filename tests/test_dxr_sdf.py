import numpy as np
import pytest
from blender_mcp.kernel.sdf_visual_hull import (
    compute_visual_hull_tensor,
    extract_sdf_isosurface,
    generate_hull_mesh_data,
)

def test_visual_hull_tensor_cylinder_intersection():
    res = 32
    # Circle mask for front (x, z)
    x = np.linspace(-1, 1, res)
    z = np.linspace(-1, 1, res)
    xx, zz = np.meshgrid(x, z, indexing="ij")
    front_circle = (xx**2 + zz**2 <= 0.8**2).astype(np.float32)

    # Square mask for side (y, z)
    side_square = np.ones((res, res), dtype=np.float32)

    hull = compute_visual_hull_tensor(front_mask=front_circle, side_mask=side_square, top_mask=None, resolution=res)
    assert hull.shape == (res, res, res)
    # Center should be inside hull (value > 0 or 1.0)
    assert hull[res//2, res//2, res//2] > 0.5
    # Corner should be outside hull (0.0)
    assert hull[0, res//2, 0] < 0.5

def test_extract_sdf_isosurface():
    res = 16
    # Create simple solid sphere/cube in center
    vol = np.zeros((res, res, res), dtype=np.float32)
    vol[4:12, 4:12, 4:12] = 1.0
    
    verts, quads = extract_sdf_isosurface(vol, iso_value=0.5)
    assert len(verts) > 0
    assert len(quads) > 0
    assert verts.shape[1] == 3
    assert quads.shape[1] == 4  # Quad faces

def test_generate_hull_mesh_synthetic():
    res = 24
    front = np.ones((res, res), dtype=np.uint8) * 255
    side = np.ones((res, res), dtype=np.uint8) * 255
    
    result = generate_hull_mesh_data(front_array=front, side_array=side, resolution=res)
    assert "vertices" in result
    assert "faces" in result
    assert len(result["vertices"]) > 0
    assert len(result["faces"]) > 0
