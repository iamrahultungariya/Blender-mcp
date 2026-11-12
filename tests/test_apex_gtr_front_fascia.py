"""Unit tests for Apex GT-R Front Bumper, Grille & Splitter (Task 6)."""
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    generate_front_bumper_mesh_data,
)


def test_front_bumper_geometry_bounds_and_splitter():
    """Verify front bumper and splitter reach the forward envelope limit with aggressive stance."""
    verts, faces = generate_front_bumper_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Reaches front bumper length limit (~2.305m)
    assert max(ys) >= 2.280
    # Connects back to front wheelhouse / cowl area
    assert min(ys) <= 1.800

    # Low ground-scraping splitter height
    assert min(zs) <= 0.060
    assert max(zs) >= 0.650

    # Width spans front fascia (~0.90m to 0.94m half-width)
    assert max(xs) >= 0.90
    assert min(xs) <= -0.90

    # Symmetry check
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4


def test_front_bumper_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for front bumper assembly."""
    verts, faces = generate_front_bumper_mesh_data()
    assert 1800 <= len(faces) <= 4500

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
