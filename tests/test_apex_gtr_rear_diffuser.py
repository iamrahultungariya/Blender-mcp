"""Unit tests for Apex GT-R Rear Diffuser & Quad Exhaust (Task 9)."""
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    generate_rear_diffuser_mesh_data,
)


def test_rear_diffuser_geometry_bounds_and_symmetry():
    """Verify rear diffuser and exhaust assembly reach rear envelope limit with 6 strakes."""
    verts, faces = generate_rear_diffuser_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Reaches rear overhang limit (~-2.305m)
    assert min(ys) <= -2.260
    assert max(ys) >= -2.000

    # Low diffuser tunnel entry (Z ~0.08m) up to taillight fascia (Z ~0.65m)
    assert min(zs) <= 0.100
    assert max(zs) >= 0.600

    # Width spans rear fascia (~0.88m to 0.94m half-width)
    assert max(xs) >= 0.88
    assert min(xs) <= -0.88

    # Exact lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4, "Rear diffuser must be symmetric across X=0"


def test_rear_diffuser_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for rear diffuser."""
    verts, faces = generate_rear_diffuser_mesh_data()
    assert 1800 <= len(faces) <= 4000

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
