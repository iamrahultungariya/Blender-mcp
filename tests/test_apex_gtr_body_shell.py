"""Unit tests for Apex GT-R Unibody Cabin & Roof Shell (Task 3)."""
import pytest
from scripts.generate_apex_gtr import (
    APEX_GTR_ENVELOPE,
    generate_body_shell_mesh_data,
)


def test_body_shell_geometry_bounds():
    """Verify body shell bounding envelope satisfies supercar proportions."""
    verts, faces = generate_body_shell_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Max width within body envelope (1.87m width -> ~0.935 half-width)
    assert max(xs) <= APEX_GTR_ENVELOPE["width"] / 2.0 + 0.05
    assert min(xs) >= -APEX_GTR_ENVELOPE["width"] / 2.0 - 0.05

    # Height peak matches roofline (1.18m)
    assert pytest.approx(max(zs), 0.02) == APEX_GTR_ENVELOPE["height"]
    # Bottom clearance matches 0.10m
    assert min(zs) >= APEX_GTR_ENVELOPE["ground_clearance"] - 0.02

    # Length spans from front cowl to rear decklid
    assert max(ys) >= 0.85
    assert min(ys) <= -2.00


def test_body_shell_topology_budget():
    """Verify body shell polygon count meets the ~3k-6k quad target."""
    verts, faces = generate_body_shell_mesh_data()
    assert len(verts) > 1000
    assert 2500 <= len(faces) <= 6500

    # Quad dominance check
    quads = [f for f in faces if len(f) == 4]
    quad_ratio = len(quads) / len(faces)
    assert quad_ratio >= 0.85, f"Expected quad dominance >= 85%, got {quad_ratio:.2%}"
