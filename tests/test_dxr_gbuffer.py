import numpy as np
import pytest
from blender_mcp.kernel.gbuffer_vision import (
    unproject_pixel_ray,
    normal_to_track_quaternion,
    raycast_surface_point,
)

def test_unproject_pixel_ray_ortho_front():
    # Identity view & ortho projection looking along +Y (from -Y towards +Y)
    # Camera at (0, -10, 0), looking down +Y
    view_mat = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, -1.0, 0.0, 10.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    proj_mat = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, -0.1, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    
    origin, direction = unproject_pixel_ray("front", 0.5, 0.5, view_mat, proj_mat)
    assert len(origin) == 3
    assert len(direction) == 3
    # Direction should be normalized
    d_norm = np.linalg.norm(direction)
    assert np.isclose(d_norm, 1.0, atol=1e-5)

def test_normal_to_track_quaternion():
    # Aligning +Z with +Z should give identity quaternion [1, 0, 0, 0]
    q_ident = normal_to_track_quaternion([0.0, 0.0, 1.0])
    assert np.allclose(q_ident, [1.0, 0.0, 0.0, 0.0], atol=1e-5)

    # Aligning with +X normal
    q_x = normal_to_track_quaternion([1.0, 0.0, 0.0])
    assert len(q_x) == 4
    assert np.isclose(np.linalg.norm(q_x), 1.0, atol=1e-5)

def test_raycast_surface_point_plane():
    # Ray from (0, 0, 5) pointing straight down (0, 0, -1) onto horizontal plane at Z=0
    origin = [0.0, 0.0, 5.0]
    direction = [0.0, 0.0, -1.0]
    
    # Plane at z=0 with normal (0, 0, 1)
    res = raycast_surface_point(
        origin, direction,
        plane_point=[0.0, 0.0, 0.0],
        plane_normal=[0.0, 0.0, 1.0]
    )
    assert res["hit"] is True
    assert np.allclose(res["hit_point"], [0.0, 0.0, 0.0], atol=1e-5)
    assert np.allclose(res["normal"], [0.0, 0.0, 1.0], atol=1e-5)
    assert np.allclose(res["quaternion"], [1.0, 0.0, 0.0, 0.0], atol=1e-5)
