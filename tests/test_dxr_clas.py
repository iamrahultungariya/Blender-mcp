import numpy as np
import pytest
from blender_mcp.kernel.clas_tensor_shaper import (
    eval_bicubic_bezier_patch,
    loft_spline_sections,
    apply_blender_version_compatibility,
)

def test_eval_bicubic_bezier_patch_flat_plane():
    # 4x4 flat grid on Z=0
    x = np.linspace(0, 3, 4)
    y = np.linspace(0, 3, 4)
    xx, yy = np.meshgrid(x, y, indexing="ij")
    control_grid = np.zeros((4, 4, 3), dtype=np.float32)
    control_grid[:, :, 0] = xx
    control_grid[:, :, 1] = yy
    control_grid[:, :, 2] = 0.0

    res_u, res_v = 16, 16
    verts, quads, normals = eval_bicubic_bezier_patch(control_grid, res_u=res_u, res_v=res_v)
    assert verts.shape == (res_u * res_v, 3)
    assert quads.shape == ((res_u - 1) * (res_v - 1), 4)
    # Z should be 0 everywhere on flat plane
    assert np.allclose(verts[:, 2], 0.0, atol=1e-5)
    # Normals should point up along +Z (0, 0, 1)
    assert np.allclose(normals[:, 2], 1.0, atol=1e-4)

def test_eval_bicubic_bezier_patch_curved_dome():
    # Raise the central control points to create an aerodynamic curvature
    control_grid = np.zeros((4, 4, 3), dtype=np.float32)
    for i in range(4):
        for j in range(4):
            control_grid[i, j] = [i, j, 0.0]
    # Raise center 2x2 points
    control_grid[1:3, 1:3, 2] = 2.0

    verts, quads, normals = eval_bicubic_bezier_patch(control_grid, res_u=8, res_v=8)
    assert verts[:, 2].max() > 1.0
    assert len(quads) == (8 - 1) * (8 - 1)

def test_loft_spline_sections_cylinder():
    # 3 circular cross-sections stacked along Z
    num_pts = 12
    theta = np.linspace(0, 2*np.pi, num_pts, endpoint=False)
    radius = 1.0
    
    sections = []
    for z in [0.0, 1.0, 2.0]:
        sec = np.column_stack([radius * np.cos(theta), radius * np.sin(theta), np.full(num_pts, z)])
        sections.append(sec)

    verts, quads, normals = loft_spline_sections(sections, resolution=16, closed=True)
    assert len(verts) == 3 * 16
    assert len(quads) == 2 * 16  # 2 bands of 16 quad faces

def test_apply_blender_version_compatibility_shim():
    # Mock node tree with old Blender 3.x socket names
    class MockSocket:
        def __init__(self, name):
            self.name = name
    class MockNode:
        def __init__(self):
            self.type = "BSDF_PRINCIPLED"
            self.inputs = [MockSocket("Specular"), MockSocket("Roughness"), MockSocket("Base Color")]

    node = MockNode()
    # On 4.0+, "Specular" maps to "Specular IOR Level"
    applied = apply_blender_version_compatibility(node, version_tuple=(4, 2, 0))
    assert applied is True
    socket_names = [s.name for s in node.inputs]
    assert "Specular IOR Level" in socket_names
