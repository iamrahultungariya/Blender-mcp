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
    sections: list[np.ndarray], resolution: int = 32, closed: bool = True, longitudinal_samples: int = 1
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Loft a sequence of cross-section profile splines into a surface hull.

    Parameters:
    - sections: list of (M, 3) cross-section point arrays
    - resolution: number of samples along each perimeter profile
    - closed: whether each cross-section loop is closed
    - longitudinal_samples: number of spline interpolation steps between stations (>1 enables smooth G1 Catmull-Rom lofting)

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

    # Apply Catmull-Rom longitudinal spline interpolation if requested
    if longitudinal_samples > 1 and num_sections >= 2:
        S = np.array(resampled_sections, dtype=np.float32)  # (K, res, 3)
        P_neg1 = (2 * S[0] - S[1])[None, ...]
        P_K = (2 * S[-1] - S[-2])[None, ...]
        P = np.vstack([P_neg1, S, P_K])

        interpolated_sections = []
        for s in range(num_sections - 1):
            p0 = P[s]
            p1 = P[s+1]
            p2 = P[s+2]
            p3 = P[s+3]
            is_last = (s == num_sections - 2)
            steps = longitudinal_samples + (1 if is_last else 0)
            t = np.linspace(0.0, 1.0, steps, endpoint=is_last, dtype=np.float32)[:, None, None]
            val = 0.5 * (2 * p1 + (-p0 + p2) * t + (2*p0 - 5*p1 + 4*p2 - p3) * (t**2) + (-p0 + 3*p1 - 3*p2 + p3) * (t**3))
            for step_idx in range(len(val)):
                interpolated_sections.append(val[step_idx])
        eval_sections = interpolated_sections
    else:
        eval_sections = resampled_sections

    total_sections = len(eval_sections)
    verts = np.vstack(eval_sections)  # Shape: (total_sections * res, 3)

    quads_list = []
    for s in range(total_sections - 1):
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


def extract_visual_hull_mesh(
    front_mask: np.ndarray | None = None,
    side_mask: np.ndarray | None = None,
    top_mask: np.ndarray | None = None,
    resolution: int = 32,
    bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]] = ((-1.0, 1.0), (-1.0, 1.0), (-1.0, 1.0))
) -> tuple[np.ndarray, np.ndarray]:
    """Compute 3-axis visual hull occupancy grid and extract watertight quad surface."""
    R = int(resolution)
    if R < 2:
        R = 2

    occ = np.ones((R, R, R), dtype=bool)

    def resample_mask(mask: np.ndarray | None) -> np.ndarray | None:
        if mask is None:
            return None
        arr = np.asarray(mask, dtype=float)
        if arr.ndim > 2:
            if arr.shape[-1] >= 4:
                arr = arr[..., 3]
            else:
                arr = arr.mean(axis=-1)
        if arr.max() > 1.0:
            arr = arr / 255.0
        bin_mask = arr > 0.3
        h, w = bin_mask.shape
        row_idx = (np.linspace(0, h - 1, R)).astype(int)
        col_idx = (np.linspace(0, w - 1, R)).astype(int)
        return bin_mask[np.ix_(row_idx, col_idx)]

    m_front = resample_mask(front_mask)
    m_side = resample_mask(side_mask)
    m_top = resample_mask(top_mask)

    if m_front is not None:
        occ &= m_front[:, None, :]
    if m_side is not None:
        occ &= m_side[:, :, None]
    if m_top is not None:
        occ &= m_top[None, :, :]

    if not np.any(occ):
        zz, yy, xx = np.mgrid[:R, :R, :R]
        c = (R - 1) / 2.0
        occ = ((xx - c)**2 + (yy - c)**2 + (zz - c)**2) <= (c * 0.9)**2

    (x_min, x_max), (y_min, y_max), (z_min, z_max) = bounds
    grid_x = np.linspace(x_min, x_max, R + 1, dtype=np.float32)
    grid_y = np.linspace(y_min, y_max, R + 1, dtype=np.float32)
    grid_z = np.linspace(z_min, z_max, R + 1, dtype=np.float32)

    def corner_idx(k, j, i):
        return k * (R + 1) * (R + 1) + j * (R + 1) + i

    quads = []
    for k in range(R):
        for j in range(R):
            for i in range(R):
                if not occ[k, j, i]:
                    continue

                if i == 0 or not occ[k, j, i - 1]:
                    quads.append([
                        corner_idx(k, j, i),
                        corner_idx(k + 1, j, i),
                        corner_idx(k + 1, j + 1, i),
                        corner_idx(k, j + 1, i)
                    ])
                if i == R - 1 or not occ[k, j, i + 1]:
                    quads.append([
                        corner_idx(k, j, i + 1),
                        corner_idx(k, j + 1, i + 1),
                        corner_idx(k + 1, j + 1, i + 1),
                        corner_idx(k + 1, j, i + 1)
                    ])
                if j == 0 or not occ[k, j - 1, i]:
                    quads.append([
                        corner_idx(k, j, i),
                        corner_idx(k, j, i + 1),
                        corner_idx(k + 1, j, i + 1),
                        corner_idx(k + 1, j, i)
                    ])
                if j == R - 1 or not occ[k, j + 1, i]:
                    quads.append([
                        corner_idx(k, j + 1, i),
                        corner_idx(k + 1, j + 1, i),
                        corner_idx(k + 1, j + 1, i + 1),
                        corner_idx(k, j + 1, i + 1)
                    ])
                if k == 0 or not occ[k - 1, j, i]:
                    quads.append([
                        corner_idx(k, j, i),
                        corner_idx(k, j + 1, i),
                        corner_idx(k, j + 1, i + 1),
                        corner_idx(k, j, i + 1)
                    ])
                if k == R - 1 or not occ[k + 1, j, i]:
                    quads.append([
                        corner_idx(k + 1, j, i),
                        corner_idx(k + 1, j, i + 1),
                        corner_idx(k + 1, j + 1, i + 1),
                        corner_idx(k + 1, j + 1, i)
                    ])

    if not quads:
        return np.zeros((0, 3), dtype=np.float32), np.zeros((0, 4), dtype=np.int32)

    quads_arr = np.array(quads, dtype=np.int32)
    used_indices, inverse = np.unique(quads_arr, return_inverse=True)
    new_quads = inverse.reshape(quads_arr.shape)

    kk = used_indices // ((R + 1) * (R + 1))
    rem = used_indices % ((R + 1) * (R + 1))
    jj = rem // (R + 1)
    ii = rem % (R + 1)

    verts = np.column_stack([grid_x[ii], grid_y[jj], grid_z[kk]]).astype(np.float32)
    return verts, new_quads.astype(np.int32)


def apply_blender_version_compatibility(
    node_or_mesh: Any,
    version_tuple: tuple[int, int, int] | None = None,
    smooth_angle_deg: float = 30.0,
) -> bool:
    """Remap legacy Blender 3.x property and socket names for Blender 4.x/5.x/5.3+ compatibility.
    
    Handles:
    1. Principled BSDF socket name updates in Blender 4.0+.
    2. Legacy Blender 3.x / 4.0 auto-smooth properties (use_auto_smooth, auto_smooth_angle).
    3. Modern Blender 4.1+ / 5.0 / 5.3+ auto-smooth via 'Smooth by Angle' modifier and polygon smooth shading.
    """
    if version_tuple is None:
        try:
            import bpy

            version_tuple = bpy.app.version
        except Exception:
            version_tuple = (5, 3, 0)

    major = version_tuple[0]
    minor = version_tuple[1] if len(version_tuple) > 1 else 0
    is_modern_smooth = (major > 4) or (major == 4 and minor >= 1)

    # 1. Handle Principled BSDF socket name updates in Blender 4.0+
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

    # 2. Modern Blender 4.1+ / 5.0 / 5.3+ Mesh & Mesh Object Handling
    if is_modern_smooth:
        applied = False

        # Check if node_or_mesh is a Mesh Object
        is_mesh_obj = hasattr(node_or_mesh, "type") and getattr(node_or_mesh, "type") == "MESH"
        mesh_data = getattr(node_or_mesh, "data", None) if is_mesh_obj else None

        # Enable smooth shading on polygons if accessible
        target_mesh = mesh_data if mesh_data is not None else (node_or_mesh if hasattr(node_or_mesh, "polygons") else None)
        if target_mesh and hasattr(target_mesh, "polygons"):
            try:
                for p in target_mesh.polygons:
                    p.use_smooth = True
                applied = True
            except Exception:
                pass

        # Attach 'Smooth by Angle' modifier if node_or_mesh has modifiers
        if hasattr(node_or_mesh, "modifiers"):
            mod_names = [getattr(m, "name", "") for m in node_or_mesh.modifiers]
            if "Smooth by Angle" not in mod_names:
                try:
                    mod = node_or_mesh.modifiers.new(name="Smooth by Angle", type='NODES')
                    # Try linking official geometry node group if available in Blender session
                    try:
                        import bpy
                        ng = bpy.data.node_groups.get("Smooth by Angle")
                        if ng and hasattr(mod, "node_group"):
                            mod.node_group = ng
                    except Exception:
                        pass
                    applied = True
                except Exception:
                    pass
            else:
                applied = True

        return applied

    # 3. Legacy Blender 3.x / 4.0 auto-smooth
    if hasattr(node_or_mesh, "use_auto_smooth"):
        try:
            node_or_mesh.use_auto_smooth = True
            if hasattr(node_or_mesh, "auto_smooth_angle"):
                import math
                node_or_mesh.auto_smooth_angle = math.radians(smooth_angle_deg)
            return True
        except Exception:
            pass

    # If an Object was passed in legacy Blender, check obj.data
    if hasattr(node_or_mesh, "data") and hasattr(node_or_mesh.data, "use_auto_smooth"):
        try:
            node_or_mesh.data.use_auto_smooth = True
            if hasattr(node_or_mesh.data, "auto_smooth_angle"):
                import math
                node_or_mesh.data.auto_smooth_angle = math.radians(smooth_angle_deg)
            return True
        except Exception:
            pass

    return False
