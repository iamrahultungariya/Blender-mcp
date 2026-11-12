"""Unit tests for Apex GT-R High-Downforce Rear Wing (Task 10)."""
import pytest
from scripts.generate_apex_gtr import (
    generate_rear_wing_mesh_data,
)


def test_rear_wing_geometry_bounds_and_symmetry():
    """Verify rear wing matches swan-neck mount positions, airfoil span, and endplates."""
    verts, faces = generate_rear_wing_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Airfoil spans full rear width (~1.60m to 1.70m)
    assert max(xs) >= 0.80
    assert min(xs) <= -0.80

    # Overhangs rear decklid (~-1.80m to -2.30m)
    assert max(ys) >= -1.90
    assert min(ys) <= -2.20

    # Height: mounts to decklid (~0.85m) and reaches wing peak (~1.12m)
    assert min(zs) <= 0.88
    assert max(zs) >= 1.08

    # Lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4, "Rear wing must be symmetric across X=0"


def test_rear_wing_polycount_and_quad_ratio():
    """Verify polygon budget and quad dominance for rear wing."""
    verts, faces = generate_rear_wing_mesh_data()
    assert 800 <= len(faces) <= 2200

    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
