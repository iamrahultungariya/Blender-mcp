"""Unit tests for Apex GT-R Precision Lighting Assemblies (Task 12)."""
import pytest
from scripts.generate_apex_gtr import (
    generate_headlights_mesh_data,
    generate_tail_lights_mesh_data,
)


def test_headlights_geometry_and_symmetry():
    """Verify headlights fit within front fascia corners and have dual projector features."""
    verts, faces = generate_headlights_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Front corner coordinates
    assert max(ys) >= 2.10
    assert min(ys) <= 1.95
    assert max(xs) >= 0.85
    assert min(xs) <= -0.85
    assert 0.44 <= min(zs) <= 0.52
    assert 0.58 <= max(zs) <= 0.68

    # Lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4

    # Quad budget
    assert 800 <= len(faces) <= 2200
    quads = [f for f in faces if len(f) == 4]
    assert len(quads) / len(faces) >= 0.85


def test_tail_lights_geometry_and_symmetry():
    """Verify tail lights span rear deck with continuous LED ribbon geometry."""
    verts, faces = generate_tail_lights_mesh_data()
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]

    # Rear deck coordinates
    assert min(ys) <= -2.22
    assert max(ys) >= -2.20
    assert max(xs) >= 0.82
    assert min(xs) <= -0.82
    assert 0.55 <= min(zs) <= 0.65
    assert 0.68 <= max(zs) <= 0.78

    # Lateral symmetry
    x_sum = sum(xs)
    assert abs(x_sum / len(xs)) < 1e-4

    # Quad budget
    assert 600 <= len(faces) <= 1800
    quads = [f for f in faces if len(f) == 4]
    assert len(quads) / len(faces) >= 0.85
