"""Unit tests for Apex GT-R Sculpted Vented Hood (Task 7)."""
import pytest
from scripts.generate_apex_gtr import (
    generate_hood_mesh_data,
)


def test_hood_geometry_bounds_and_symmetry():
    """Verify hood fits precisely between front cowl and bumper nose with character creases."""
    verts, faces = generate_hood_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Spans from cowl (+0.88m) to front nose (+2.15m)
    assert max(ys) >= 2.12
    assert min(ys) <= 0.90

    # Width conforms to hood shutlines (~0.68m to 0.75m half-width)
    assert max(xs) >= 0.65
    assert min(xs) <= -0.65

    # Height slope: lower at nose (~0.65m), higher at cowl (~0.78m)
    assert max(zs) <= 0.80
    assert min(zs) >= 0.60

    # Symmetry check
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4, "Hood must be symmetric across X=0"


def test_hood_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for vented hood."""
    verts, faces = generate_hood_mesh_data()
    assert 1200 <= len(faces) <= 3000

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
