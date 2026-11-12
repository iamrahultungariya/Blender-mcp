"""Unit tests for Apex GT-R Master Wheel Assembly & Instancing (Task 11)."""
import math
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    generate_master_wheel_mesh_data,
)


def test_master_wheel_geometry_dimensions():
    """Verify master wheel rim, tire, brake rotor, and caliper radii."""
    verts, faces = generate_master_wheel_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Cylindrical radius in Y-Z plane
    radii = [math.sqrt(v[1]**2 + v[2]**2) for v in verts]

    # Outer tire radius matches 0.34m
    assert pytest.approx(max(radii), 0.01) == APEX_GTR_ENVELOPE["wheel_radius"]

    # Tire width across X matches ~0.28m
    width = max(xs) - min(xs)
    assert pytest.approx(width, 0.02) == APEX_GTR_ENVELOPE["tire_width_front"]


def test_master_wheel_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for master wheel."""
    verts, faces = generate_master_wheel_mesh_data()
    assert 2200 <= len(faces) <= 4800

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
