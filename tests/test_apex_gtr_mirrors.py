"""Unit tests for Apex GT-R Aerodynamic Wing Mirrors (Task 13)."""
import pytest
from scripts.generate_apex_gtr import (
    generate_mirrors_mesh_data,
)


def test_mirrors_geometry_bounds_and_symmetry():
    """Verify aerodynamic mirrors fit on door beltline and reach outer width envelope."""
    verts, faces = generate_mirrors_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Stalk and mirror width extends past body beltline (~0.98m to 1.05m)
    assert max(xs) >= 0.98
    assert min(xs) <= -0.98

    # Mounted around A-pillar/door beltline (~0.65m to 0.78m)
    assert 0.60 <= min(ys) <= 0.72
    assert 0.72 <= max(ys) <= 0.85

    # Height around beltline/cowl (~0.72m to 0.86m)
    assert 0.70 <= min(zs) <= 0.75
    assert 0.80 <= max(zs) <= 0.88

    # Lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4, "Mirrors must be symmetric across X=0"


def test_mirrors_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for mirrors."""
    verts, faces = generate_mirrors_mesh_data()
    assert 500 <= len(faces) <= 1500

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
