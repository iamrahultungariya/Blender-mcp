"""Unit tests for Apex GT-R Flared Widebody Fenders (Task 4)."""
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    generate_fenders_mesh_data,
)


def test_fenders_geometry_bounds_and_symmetry():
    """Verify widebody fender arches reach flared width and exhibit exact symmetry."""
    verts, faces = generate_fenders_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Reaches flared widebody width (~0.98m to 1.00m half-width)
    assert max(xs) >= 0.96
    assert min(xs) <= -0.96

    # Centers around front (+1.35m) and rear (-1.35m) wheelbases
    assert max(ys) >= 1.70
    assert min(ys) <= -1.80

    # Stance height from sill (Z=0.14) up over arches (Z=0.72)
    assert min(zs) >= APEX_GTR_ENVELOPE["ground_clearance"]
    assert max(zs) >= 0.70

    # Perfect lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4, "Fenders should be symmetric across X=0"


def test_fenders_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for widebody fenders."""
    verts, faces = generate_fenders_mesh_data()
    assert 1200 <= len(faces) <= 3500

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
