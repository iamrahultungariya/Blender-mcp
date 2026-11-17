import math
import pytest

try:
    import bmesh
except ImportError:
    from luxury_bedroom.core.bmesh_utils import MockBMesh as bmesh

from luxury_bedroom.core.bmesh_utils import (
    create_beveled_box,
    create_cushion_loft,
    create_draped_cloth_surface,
    create_fluted_panel,
)


def test_create_beveled_box():
    bm = bmesh.new()
    create_beveled_box(bm, width=1.0, length=1.0, height=0.5, bevel_radius=0.05, segments=3, mat_index=1)
    assert len(bm.verts) >= 8
    assert len(bm.faces) >= 6
    # Check material assignment
    for f in bm.faces:
        assert f.material_index == 1
    bm.free()


def test_create_cushion_loft():
    bm = bmesh.new()
    # Base height 0.10, crown 0.05 -> apex should reach ~0.15
    create_cushion_loft(
        bm,
        width=0.8,
        length=0.5,
        height=0.10,
        crown=0.05,
        subdivisions_u=8,
        subdivisions_v=8,
        offset=(0, 0, 0),
        mat_index=2,
    )
    assert len(bm.verts) >= 64
    assert len(bm.faces) >= 40
    max_z = max(v.co.z for v in bm.verts)
    assert max_z > 0.12  # Verifies crown elevation
    for f in bm.faces:
        assert f.material_index == 2
    bm.free()


def test_create_cushion_loft_with_tilt():
    bm = bmesh.new()
    create_cushion_loft(
        bm,
        width=0.75,
        length=0.48,
        height=0.15,
        crown=0.06,
        subdivisions_u=6,
        subdivisions_v=6,
        offset=(0, 0, 0),
        mat_index=0,
        tilt_deg_x=15.0,
    )
    assert len(bm.verts) >= 36
    # Y-coordinates should exhibit tilt slope
    min_z = min(v.co.z for v in bm.verts)
    max_z = max(v.co.z for v in bm.verts)
    assert (max_z - min_z) > 0.15
    bm.free()


def test_create_draped_cloth_surface():
    bm = bmesh.new()
    create_draped_cloth_surface(
        bm,
        width=2.0,
        length=1.8,
        drape_drop=0.20,
        folds_freq=4.0,
        folds_amp=0.02,
        subdivisions_x=12,
        subdivisions_y=12,
        offset=(0, 0, 0.4),
        mat_index=3,
        cuff_length=0.25,
        cuff_mat_index=4,
    )
    assert len(bm.faces) > 50
    # Both base and cuff materials should be assigned
    mat_indices = {f.material_index for f in bm.faces}
    assert 3 in mat_indices
    assert 4 in mat_indices
    bm.free()


def test_create_fluted_panel():
    bm = bmesh.new()
    create_fluted_panel(
        bm,
        width=2.4,
        height=1.3,
        depth=0.08,
        num_flutes=8,
        flute_radius=0.015,
        offset=(0, 0, 0),
        mat_index=1,
    )
    assert len(bm.faces) >= 16
    assert all(f.material_index == 1 for f in bm.faces)
    bm.free()
