"""G-Buffer Vision Sensor & 2D-to-3D Raycast Unprojector.

Provides 4-quad offscreen viewport capture and unprojects 2D normalized
image coordinates (u, v) into 3D world space (X, Y, Z) with surface-normal
aligned quaternions using scene BVHTree raycasting.
"""

from __future__ import annotations

from typing import Any
import numpy as np


def unproject_pixel_ray(
    quadrant: str,
    u: float,
    v: float,
    view_matrix: list[list[float]] | np.ndarray,
    proj_matrix: list[list[float]] | np.ndarray,
) -> tuple[list[float], list[float]]:
    """Unproject a 2D normalized coordinate (u, v) into a 3D ray (origin, direction).

    Parameters:
    - quadrant: 'top', 'front', 'side', 'perspective'
    - u, v: normalized coordinates in [0, 1], with (0,0) top-left
    - view_matrix: 4x4 camera view matrix
    - proj_matrix: 4x4 camera projection matrix
    """
    V = np.asarray(view_matrix, dtype=np.float64)
    P = np.asarray(proj_matrix, dtype=np.float64)

    VP = P @ V
    inv_VP = np.linalg.inv(VP)

    # NDC coordinates: x in [-1, 1], y in [1, -1]
    ndc_x = 2.0 * float(u) - 1.0
    ndc_y = 1.0 - 2.0 * float(v)

    # Unproject near plane point (z = -1) and far plane point (z = 1)
    p_near_clip = np.array([ndc_x, ndc_y, -1.0, 1.0], dtype=np.float64)
    p_far_clip = np.array([ndc_x, ndc_y, 1.0, 1.0], dtype=np.float64)

    p_near_world = inv_VP @ p_near_clip
    p_far_world = inv_VP @ p_far_clip

    w_near = p_near_world[3] if abs(p_near_world[3]) > 1e-9 else 1.0
    w_far = p_far_world[3] if abs(p_far_world[3]) > 1e-9 else 1.0

    p_near = p_near_world[:3] / w_near
    p_far = p_far_world[:3] / w_far

    direction = p_far - p_near
    norm = np.linalg.norm(direction)
    if norm > 1e-9:
        direction /= norm
    else:
        direction = np.array([0.0, 0.0, -1.0], dtype=np.float64)

    return p_near.tolist(), direction.tolist()


def normal_to_track_quaternion(
    normal: list[float] | np.ndarray,
    track_axis: str = "Z",
    up_axis: str = "Y",
) -> list[float]:
    """Calculate the unit quaternion [w, x, y, z] aligning the track axis (+Z) to the surface normal."""
    n = np.asarray(normal, dtype=np.float64)
    norm = np.linalg.norm(n)
    if norm < 1e-9:
        return [1.0, 0.0, 0.0, 0.0]
    n = n / norm

    # Default axis is +Z: [0, 0, 1]
    v_from = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    dot = np.dot(v_from, n)

    if dot >= 1.0 - 1e-7:
        return [1.0, 0.0, 0.0, 0.0]
    elif dot <= -1.0 + 1e-7:
        # 180 degree rotation around X axis
        return [0.0, 1.0, 0.0, 0.0]

    axis = np.cross(v_from, n)
    w = 1.0 + dot
    q = np.array([w, axis[0], axis[1], axis[2]], dtype=np.float64)
    q /= np.linalg.norm(q)
    return q.tolist()


def raycast_surface_point(
    ray_origin: list[float],
    ray_direction: list[float],
    bvh_tree: Any = None,
    plane_point: list[float] | None = None,
    plane_normal: list[float] | None = None,
) -> dict[str, Any]:
    """Cast ray into scene BVH or reference plane, returning 3D hit point and alignment quaternion."""
    ro = np.asarray(ray_origin, dtype=np.float64)
    rd = np.asarray(ray_direction, dtype=np.float64)

    # 1. Blender native BVHTree raycast
    if bvh_tree is not None:
        try:
            from mathutils import Vector

            hit, loc, norm, idx = bvh_tree.ray_cast(Vector(ro), Vector(rd))
            if hit:
                h_point = list(loc)
                h_norm = list(norm)
                quat = normal_to_track_quaternion(h_norm)
                return {
                    "hit": True,
                    "hit_point": h_point,
                    "normal": h_norm,
                    "quaternion": quat,
                    "polygon_index": idx,
                }
        except Exception:
            pass

    # 2. Infinite plane fallback
    if plane_point is not None and plane_normal is not None:
        p0 = np.asarray(plane_point, dtype=np.float64)
        pn = np.asarray(plane_normal, dtype=np.float64)
        denom = np.dot(rd, pn)
        if abs(denom) > 1e-7:
            t = np.dot(p0 - ro, pn) / denom
            if t >= 0:
                hit_pt = ro + t * rd
                quat = normal_to_track_quaternion(pn)
                return {
                    "hit": True,
                    "hit_point": hit_pt.tolist(),
                    "normal": pn.tolist(),
                    "quaternion": quat,
                    "distance": float(t),
                }

    return {"hit": False, "hit_point": None, "normal": None, "quaternion": None}
