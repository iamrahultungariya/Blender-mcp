"""Unit tests for Apex GT-R Side Skirts & Ground Effects (Task 8)."""
import pytest
from scripts.generate_apex_gtr import (
    generate_side_skirts_mesh_data,
)


def test_side_skirts_geometry_bounds_and_symmetry():
    """Verify side skirts fit between front and rear wheel arches with low ground clearance."""
    verts, faces = generate_side_skirts_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Spans between front and rear arches (~0.95m span)
    assert max(ys) >= 0.90
    assert min(ys) <= -0.90

    # Low ground clearance shelf (Z ~0.06m)
    assert min(zs) <= 0.070
    assert max(zs) >= 0.140

    # Width reaches track width (~0.92m to 0.96m half-width)
    assert max(xs) >= 0.92
    assert min(xs) <= -0.92

    # Exact lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4, "Side skirts must be symmetric across X=0"


def test_side_skirts_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for side skirts."""
    verts, faces = generate_side_skirts_mesh_data()
    assert 800 <= len(faces) <= 2200

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
