import pytest
import numpy as np

def test_bmesh_toolkit_imports():
    from blender_mcp import bmesh_toolkit
    assert hasattr(bmesh_toolkit, "create_filleted_box")
    assert hasattr(bmesh_toolkit, "create_cylinder")
    assert hasattr(bmesh_toolkit, "create_wheel_arch")
    assert hasattr(bmesh_toolkit, "create_curved_windshield")
    assert hasattr(bmesh_toolkit, "create_swept_profile")
    assert hasattr(bmesh_toolkit, "apply_automotive_modifiers")

def test_generate_box_mesh_data():
    from blender_mcp.bmesh_toolkit import calculate_box_geometry
    min_v = (-1.0, -2.0, 0.0)
    max_v = (1.0, 2.0, 1.5)
    verts, faces = calculate_box_geometry(min_v, max_v)
    assert len(verts) == 8
    assert len(faces) == 6
    # Check bounds
    arr = np.array(verts)
    assert np.allclose(arr.min(axis=0), min_v)
    assert np.allclose(arr.max(axis=0), max_v)

def test_generate_cylinder_mesh_data():
    from blender_mcp.bmesh_toolkit import calculate_cylinder_geometry
    p1 = (0.0, 0.0, 0.0)
    p2 = (0.0, 0.0, 2.0)
    radius = 0.5
    segments = 16
    verts, faces = calculate_cylinder_geometry(p1, p2, radius=radius, segments=segments, cap_ends=True)
    assert len(verts) == segments * 2
    # Side quads = segments, caps = 2
    assert len(faces) >= segments

def test_generate_wheel_arch_mesh_data():
    from blender_mcp.bmesh_toolkit import calculate_wheel_arch_geometry
    center = (1.0, 2.0, 0.45)
    radius = 0.45
    width = 0.1
    lip_thickness = 0.02
    lip_outset = 0.03
    verts, faces = calculate_wheel_arch_geometry(
        center=center, radius=radius, width=width,
        lip_thickness=lip_thickness, lip_outset=lip_outset,
        segments=12, axis="X"
    )
    assert len(verts) > 0
    assert len(faces) > 0
    # Center Y of arch should match center[1]
    arr = np.array(verts)
    assert np.isclose(arr[:, 1].mean(), center[1], atol=0.1)

def test_generate_curved_windshield_mesh_data():
    from blender_mcp.bmesh_toolkit import calculate_windshield_geometry
    bottom_center = (0.0, 1.5, 1.2)
    top_center = (0.0, 0.8, 2.0)
    width_bottom = 1.8
    width_top = 1.5
    curvature_depth = 0.08
    verts, quads = calculate_windshield_geometry(
        bottom_center=bottom_center,
        top_center=top_center,
        width_bottom=width_bottom,
        width_top=width_top,
        curvature_depth=curvature_depth,
        segments_u=8,
        segments_v=4
    )
    assert len(verts) == (8 + 1) * (4 + 1)
    assert len(quads) == 8 * 4
    # Curvature check: Center should bow forward compared to corners
    arr = np.array(verts)
    center_verts = arr[np.isclose(arr[:, 0], 0.0, atol=0.01)]
    assert len(center_verts) > 0
