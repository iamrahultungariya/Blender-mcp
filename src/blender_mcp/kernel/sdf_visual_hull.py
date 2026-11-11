"""Visual Hull Space-Carving & OpenVDB SDF Engine.

Takes 1 to 3 orthographic reference projections (Front, Side, Top)
and computes a 3-axis broadcast intersection in a 3D voxel tensor,
extracting a clean quad-dominant surface mesh in milliseconds.
"""

from __future__ import annotations

import io
from typing import Any
import numpy as np


def _resize_2d(mask: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
    """Resize a 2D numpy array to target (height, width) via bilinear interpolation."""
    h_in, w_in = mask.shape
    h_out, w_out = target_shape
    if (h_in, w_in) == (h_out, w_out):
        return mask.astype(np.float32)

    y_indices = np.linspace(0, h_in - 1, h_out)
    x_indices = np.linspace(0, w_in - 1, w_out)
    
    y0 = np.floor(y_indices).astype(int)
    y1 = np.clip(y0 + 1, 0, h_in - 1)
    x0 = np.floor(x_indices).astype(int)
    x1 = np.clip(x0 + 1, 0, w_in - 1)

    wy = (y_indices - y0)[:, np.newaxis]
    wx = (x_indices - x0)[np.newaxis, :]

    top = mask[y0[:, np.newaxis], x0] * (1 - wx) + mask[y0[:, np.newaxis], x1] * wx
    bottom = mask[y1[:, np.newaxis], x0] * (1 - wx) + mask[y1[:, np.newaxis], x1] * wx

    return (top * (1 - wy) + bottom * wy).astype(np.float32)


def compute_visual_hull_tensor(
    front_mask: np.ndarray | None = None,
    side_mask: np.ndarray | None = None,
    top_mask: np.ndarray | None = None,
    resolution: int = 64,
) -> np.ndarray:
    """Compute the 3D visual hull tensor V(x, y, z) by 3-axis broadcast intersection.

    - front_mask: X (cols) x Z (rows)
    - side_mask: Y (cols) x Z (rows)
    - top_mask: X (cols) x Y (rows)
    """
    res = resolution
    hull = np.ones((res, res, res), dtype=np.float32)

    if front_mask is not None:
        f = _resize_2d(front_mask, (res, res))
        # Front is X (x) and Z (z), broadcast over Y
        # f[x, z] -> [x, 1, z]
        hull = np.minimum(hull, f[:, np.newaxis, :])

    if side_mask is not None:
        s = _resize_2d(side_mask, (res, res))
        # Side is Y (y) and Z (z), broadcast over X
        # s[y, z] -> [1, y, z]
        hull = np.minimum(hull, s[np.newaxis, :, :])

    if top_mask is not None:
        t = _resize_2d(top_mask, (res, res))
        # Top is X (x) and Y (y), broadcast over Z
        # t[x, y] -> [x, y, 1]
        hull = np.minimum(hull, t[:, :, np.newaxis])

    return hull


def extract_sdf_isosurface(
    voxel_tensor: np.ndarray, iso_value: float = 0.5
) -> tuple[np.ndarray, np.ndarray]:
    """Extract a watertight quad boundary surface from a 3D binary/SDF voxel grid."""
    res_x, res_y, res_z = voxel_tensor.shape
    solid = voxel_tensor >= iso_value

    # Pad with False to easily compute boundary exposed faces
    padded = np.pad(solid, 1, mode="constant", constant_values=False)

    vertices_dict: dict[tuple[int, int, int], int] = {}
    quads_list: list[list[int]] = []

    def get_vertex_id(grid_x: int, grid_y: int, grid_z: int) -> int:
        key = (grid_x, grid_y, grid_z)
        if key not in vertices_dict:
            vertices_dict[key] = len(vertices_dict)
        return vertices_dict[key]

    # Directions: (dx, dy, dz), face corner offsets (4 points in CCW order)
    face_defs = [
        # +X face
        (
            (1, 0, 0),
            [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)],
            padded[2:, 1:-1, 1:-1],
        ),
        # -X face
        (
            (-1, 0, 0),
            [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
            padded[:-2, 1:-1, 1:-1],
        ),
        # +Y face
        (
            (0, 1, 0),
            [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)],
            padded[1:-1, 2:, 1:-1],
        ),
        # -Y face
        (
            (0, -1, 0),
            [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
            padded[1:-1, :-2, 1:-1],
        ),
        # +Z face
        (
            (0, 0, 1),
            [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
            padded[1:-1, 1:-1, 2:],
        ),
        # -Z face
        (
            (0, 0, -1),
            [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)],
            padded[1:-1, 1:-1, :-2],
        ),
    ]

    for (dx, dy, dz), corners, neighbor_solid in face_defs:
        # Exposed where current voxel is solid and neighbor is empty
        exposed = solid & (~neighbor_solid)
        coords = np.argwhere(exposed)

        for cx, cy, cz in coords:
            quad = [get_vertex_id(cx + ox, cy + oy, cz + oz) for ox, oy, oz in corners]
            quads_list.append(quad)

    if not vertices_dict:
        return np.empty((0, 3), dtype=np.float32), np.empty((0, 4), dtype=np.int32)

    # Convert vertex integer keys to normalized centered coordinates [-1, 1]
    num_verts = len(vertices_dict)
    verts_array = np.zeros((num_verts, 3), dtype=np.float32)
    for (gx, gy, gz), idx in vertices_dict.items():
        verts_array[idx] = [
            (gx / res_x) * 2.0 - 1.0,
            (gy / res_y) * 2.0 - 1.0,
            (gz / res_z) * 2.0 - 1.0,
        ]

    return verts_array, np.array(quads_list, dtype=np.int32)


def generate_hull_mesh_data(
    front_array: np.ndarray | None = None,
    side_array: np.ndarray | None = None,
    top_array: np.ndarray | None = None,
    resolution: int = 32,
) -> dict[str, Any]:
    """Generate normalized quad mesh geometry from silhouette inputs."""
    def normalize_mask(arr: np.ndarray | None) -> np.ndarray | None:
        if arr is None:
            return None
        if arr.ndim == 3:
            # If RGBA, use Alpha channel; if RGB, use luminance
            if arr.shape[2] == 4:
                arr = arr[:, :, 3]
            else:
                arr = arr.mean(axis=2)
        return (arr > 127).astype(np.float32) if arr.max() > 1.0 else arr.astype(np.float32)

    f = normalize_mask(front_array)
    s = normalize_mask(side_array)
    t = normalize_mask(top_array)

    voxel_grid = compute_visual_hull_tensor(f, s, t, resolution=resolution)
    verts, quads = extract_sdf_isosurface(voxel_grid, iso_value=0.5)

    return {
        "vertices": verts.tolist(),
        "faces": quads.tolist(),
        "resolution": resolution,
        "vertex_count": len(verts),
        "face_count": len(quads),
    }
