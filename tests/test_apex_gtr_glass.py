"""Unit tests for Apex GT-R Flush Automotive Glass Canopy (Task 5)."""
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    generate_glass_mesh_data,
)


def test_glass_geometry_bounds():
    """Verify glass canopy components fit within supercar greenhouse envelope."""
    verts, faces = generate_glass_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Stays within greenhouse width (~0.75m half-width)
    assert max(xs) <= 0.78
    assert min(xs) >= -0.78

    # Spans from front windshield cowl (+0.88m) to fastback rear (-1.55m)
    assert max(ys) >= 0.85
    assert min(ys) <= -1.45

    # Height reaches roofline peak (~1.18m) and drops to beltline (~0.70m)
    assert pytest.approx(max(zs), 0.02) == APEX_GTR_ENVELOPE["height"]
    assert min(zs) >= 0.68


def test_glass_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for glass canopy."""
    verts, faces = generate_glass_mesh_data()
    assert 800 <= len(faces) <= 2000

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
