"""CLAS Cluster Templates & Zero-Copy C-Buffer Tensor Shaper.

Evaluates high-order parametric surfaces (Bicubic Bezier Tensor Patches,
Spline Lofting) using vectorized Bernstein polynomials and produces contiguous
C-RNA buffers ready for direct injection via mesh.vertices.foreach_set().
"""

from __future__ import annotations

from typing import Any
import numpy as np


def _bernstein_basis_and_derivs(
    t: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Evaluate degree-3 Bernstein basis polynomials and their first derivatives."""
    t = np.clip(t, 0.0, 1.0)
    om_t = 1.0 - t

    b0 = om_t**3
    b1 = 3.0 * t * (om_t**2)
    b2 = 3.0 * (t**2) * om_t
    b3 = t**3
    basis = np.stack([b0, b1, b2, b3], axis=1)

    db0 = -3.0 * (om_t**2)
    db1 = 3.0 * (om_t**2) - 6.0 * t * om_t
    db2 = 6.0 * t * om_t - 3.0 * (t**2)
    db3 = 3.0 * (t**2)
    derivs = np.stack([db0, db1, db2, db3], axis=1)

    return basis, derivs


def eval_bicubic_bezier_patch(
    control_grid_4x4: np.ndarray, res_u: int = 32, res_v: int = 32
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Evaluate a bicubic Bezier surface patch from a 4x4 control grid.

    Parameters:
    - control_grid_4x4: shape (4, 4, 3) float array
    - res_u, res_v: grid evaluation resolution

    Returns:
    - vertices: (res_u * res_v, 3) float32 array
    - quads: ((res_u - 1) * (res_v - 1), 4) int32 quad indices
    - normals: (res_u * res_v, 3) unit normal vectors
    """
    P = np.asarray(control_grid_4x4, dtype=np.float32)
    if P.shape != (4, 4, 3):
        raise ValueError(f"Control grid must have shape (4, 4, 3), got {P.shape}")

    u = np.linspace(0.0, 1.0, res_u, dtype=np.float32)
    v = np.linspace(0.0, 1.0, res_v, dtype=np.float32)

    Bu, dBu = _bernstein_basis_and_derivs(u)
    Bv, dBv = _bernstein_basis_and_derivs(v)

    # Tensor contraction S(u, v) = sum_i sum_j B_i(u) B_j(v) P_{i,j}
    # Bu: (Ru, 4), P: (4, 4, 3), Bv: (Rv, 4)
    # Result: (Ru, Rv, 3)
    S = np.einsum("ia,abk,jb->ijk", Bu, P, Bv)

    # Tangent vectors
    Tu = np.einsum("ia,abk,jb->ijk", dBu, P, Bv)
    Tv = np.einsum("ia,abk,jb->ijk", Bu, P, dBv)

    # Surface normal N = Tu x Tv
    N = np.cross(Tu, Tv)
    norm = np.linalg.norm(N, axis=2, keepdims=True)
    norm = np.where(norm < 1e-7, 1.0, norm)
    normals = N / norm

    # Topology: Quad face connectivity
    i_indices, j_indices = np.meshgrid(
        np.arange(res_u - 1), np.arange(res_v - 1), indexing="ij"
    )
    v00 = i_indices * res_v + j_indices
    v10 = (i_indices + 1) * res_v + j_indices
    v11 = (i_indices + 1) * res_v + (j_indices + 1)
    v01 = i_indices * res_v + (j_indices + 1)

    quads = np.stack([v00, v10, v11, v01], axis=-1).reshape(-1, 4)

    return (
        S.reshape(-1, 3).astype(np.float32),
        quads.astype(np.int32),
        normals.reshape(-1, 3).astype(np.float32),
    )


def loft_spline_sections(
    sections: list[np.ndarray], resolution: int = 32, closed: bool = True
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Loft a sequence of cross-section profile splines into a surface hull.

    Parameters:
    - sections: list of (M, 3) cross-section point arrays
    - resolution: number of samples along each perimeter profile
    - closed: whether each cross-section loop is closed

    Returns:
    - vertices, quads, normals
    """
    if len(sections) < 2:
        raise ValueError("Lofting requires at least 2 cross-section profiles")

    num_sections = len(sections)
    res = resolution
    resampled_sections = []

    for sec in sections:
        sec = np.asarray(sec, dtype=np.float32)
        m = len(sec)
        if closed:
            sec_extended = np.vstack([sec, sec[0:1]])
            t_orig = np.linspace(0.0, 1.0, m + 1)
            t_target = np.linspace(0.0, 1.0, res, endpoint=False)
        else:
            t_orig = np.linspace(0.0, 1.0, m)
            t_target = np.linspace(0.0, 1.0, res, endpoint=True)

        resampled = np.empty((len(t_target), 3), dtype=np.float32)
        for dim in range(3):
            resampled[:, dim] = np.interp(t_target, t_orig, sec_extended[:, dim] if closed else sec[:, dim])
        resampled_sections.append(resampled)

    verts = np.vstack(resampled_sections)  # Shape: (num_sections * res, 3)

    quads_list = []
    for s in range(num_sections - 1):
        for i in range(res):
            next_i = (i + 1) % res if closed else i + 1
            if not closed and next_i >= res:
                continue
            v0 = s * res + i
            v1 = (s + 1) * res + i
            v2 = (s + 1) * res + next_i
            v3 = s * res + next_i
            quads_list.append([v0, v1, v2, v3])

    quads = np.array(quads_list, dtype=np.int32)

    # Compute vertex normals via quad normal averaging
    normals = np.zeros_like(verts)
    if len(quads) > 0:
        v0 = verts[quads[:, 0]]
        v1 = verts[quads[:, 1]]
        v2 = verts[quads[:, 2]]
        face_normals = np.cross(v1 - v0, v2 - v0)
        for q_idx, face_norm in enumerate(face_normals):
            for v_idx in quads[q_idx]:
                normals[v_idx] += face_norm

    norm = np.linalg.norm(normals, axis=1, keepdims=True)
    norm = np.where(norm < 1e-7, 1.0, norm)
    normals = normals / norm

    return verts, quads, normals.astype(np.float32)


def apply_blender_version_compatibility(
    node_or_mesh: Any, version_tuple: tuple[int, int, int] | None = None
) -> bool:
    """Remap legacy Blender 3.x property and socket names for Blender 4.x/5.x compatibility."""
    if version_tuple is None:
        try:
            import bpy

            version_tuple = bpy.app.version
        except Exception:
            version_tuple = (4, 2, 0)

    major = version_tuple[0]

    # Handle Principled BSDF socket name updates in Blender 4.0+
    if major >= 4 and hasattr(node_or_mesh, "type") and getattr(node_or_mesh, "type") == "BSDF_PRINCIPLED":
        socket_mapping = {
            "Specular": "Specular IOR Level",
            "Subsurface": "Subsurface Weight",
            "Subsurface Color": "Base Color",
            "Transmission": "Transmission Weight",
            "Coat": "Coat Weight",
            "Sheen": "Sheen Weight",
        }
        for sock in getattr(node_or_mesh, "inputs", []):
            if sock.name in socket_mapping:
                sock.name = socket_mapping[sock.name]
        return True

    # Handle mesh auto-smooth deprecation in Blender 4.1+
    if major >= 4 and hasattr(node_or_mesh, "use_auto_smooth"):
        # Auto smooth replaced with modifier / node in 4.1
        try:
            setattr(node_or_mesh, "use_auto_smooth", True)
        except Exception:
            pass
        return True

    return False
