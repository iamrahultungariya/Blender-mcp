"""BMesh Automotive & Procedural Modeling Toolkit.

High-performance parametric builders and normal/modifier management for Blender MCP.
Runs inside Blender (using bmesh, bpy, mathutils) and exposes mathematical geometry
generators for standalone verification and unit tests.
"""
from __future__ import annotations

import math
from typing import Any, List, Tuple
import numpy as np

try:
    import bpy
    import bmesh
    import mathutils
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


# ==============================================================================
# 1. Pure Geometric Data Generators (Callable inside or outside Blender)
# ==============================================================================

def calculate_box_geometry(
    min_v: Tuple[float, float, float],
    max_v: Tuple[float, float, float]
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate 8 vertices and 6 quad face indices for an axis-aligned box."""
    x0, y0, z0 = min_v
    x1, y1, z1 = max_v

    verts = [
        [x0, y0, z0],  # 0
        [x1, y0, z0],  # 1
        [x1, y1, z0],  # 2
        [x0, y1, z0],  # 3
        [x0, y0, z1],  # 4
        [x1, y0, z1],  # 5
        [x1, y1, z1],  # 6
        [x0, y1, z1],  # 7
    ]

    # CCW outward faces: bottom, top, front(-Y), back(+Y), left(-X), right(+X)
    faces = [
        [0, 3, 2, 1],  # bottom (-Z)
        [4, 5, 6, 7],  # top (+Z)
        [0, 1, 5, 4],  # front (-Y)
        [2, 3, 7, 6],  # back (+Y)
        [0, 4, 7, 3],  # left (-X)
        [1, 2, 6, 5],  # right (+X)
    ]
    return verts, faces


def calculate_cylinder_geometry(
    p1: Tuple[float, float, float],
    p2: Tuple[float, float, float],
    radius: float = 0.1,
    segments: int = 24,
    cap_ends: bool = True
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and polygon face indices for a 3D cylinder from p1 to p2."""
    v1 = np.array(p1, dtype=np.float64)
    v2 = np.array(p2, dtype=np.float64)
    axis = v2 - v1
    length = float(np.linalg.norm(axis))

    if length < 1e-6:
        axis_norm = np.array([0.0, 0.0, 1.0])
    else:
        axis_norm = axis / length

    # Construct orthonormal basis (u, v, axis_norm)
    if abs(axis_norm[2]) < 0.9:
        ref = np.array([0.0, 0.0, 1.0])
    else:
        ref = np.array([1.0, 0.0, 0.0])

    u = np.cross(axis_norm, ref)
    u /= np.linalg.norm(u)
    v = np.cross(axis_norm, u)
    v /= np.linalg.norm(v)

    angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
    cos_a = np.cos(angles)
    sin_a = np.sin(angles)

    verts: List[List[float]] = []
    # Bottom circle (at p1)
    for c, s in zip(cos_a, sin_a):
        pt = v1 + radius * (c * u + s * v)
        verts.append(pt.tolist())

    # Top circle (at p2)
    for c, s in zip(cos_a, sin_a):
        pt = v2 + radius * (c * u + s * v)
        verts.append(pt.tolist())

    faces: List[List[int]] = []
    # Side quads
    for i in range(segments):
        next_i = (i + 1) % segments
        b0 = i
        b1 = next_i
        t0 = i + segments
        t1 = next_i + segments
        faces.append([b0, b1, t1, t0])

    # End caps
    if cap_ends:
        bottom_cap = list(reversed(range(segments)))
        top_cap = list(range(segments, 2 * segments))
        faces.append(bottom_cap)
        faces.append(top_cap)

    return verts, faces


def calculate_wheel_arch_geometry(
    center: Tuple[float, float, float],
    radius: float = 0.45,
    width: float = 0.15,
    lip_thickness: float = 0.02,
    lip_outset: float = 0.03,
    segments: int = 16,
    axis: str = "X"
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate geometry for an automotive semicircular wheel flare arch (upper 180 deg)."""
    cx, cy, cz = center
    # Semicircle angles from 0 to pi (front to back)
    theta = np.linspace(0.0, np.pi, segments + 1)

    verts: List[List[float]] = []
    faces: List[List[int]] = []

    # 3 concentric rings:
    # 0: Inner cutout edge (inside fender)
    # 1: Outer lip edge (flared outward)
    # 2: Outer body blend (flush with body panel)
    sign = 1.0 if (axis == "X" and cx >= 0) else -1.0

    r_inner = radius
    r_lip = radius + lip_thickness
    r_outer = radius + lip_thickness + 0.04

    # Ring 0: Inner
    for t in theta:
        y = cy + r_inner * np.cos(t)
        z = cz + r_inner * np.sin(t)
        x = cx
        verts.append([float(x), float(y), float(z)])

    # Ring 1: Lip (outset along X)
    for t in theta:
        y = cy + r_lip * np.cos(t)
        z = cz + r_lip * np.sin(t)
        x = cx + sign * lip_outset
        verts.append([float(x), float(y), float(z)])

    # Ring 2: Body Blend
    for t in theta:
        y = cy + r_outer * np.cos(t)
        z = cz + r_outer * np.sin(t)
        x = cx + sign * (lip_outset * 0.2)
        verts.append([float(x), float(y), float(z)])

    n_pts = segments + 1
    # Quads between Ring 0 and Ring 1 (lip underside)
    for i in range(segments):
        v0 = i
        v1 = i + 1
        v2 = i + 1 + n_pts
        v3 = i + n_pts
        faces.append([v0, v1, v2, v3])

    # Quads between Ring 1 and Ring 2 (outer flare)
    for i in range(segments):
        v0 = i + n_pts
        v1 = i + 1 + n_pts
        v2 = i + 1 + 2 * n_pts
        v3 = i + 2 * n_pts
        faces.append([v0, v1, v2, v3])

    return verts, faces


def calculate_windshield_geometry(
    bottom_center: Tuple[float, float, float],
    top_center: Tuple[float, float, float],
    width_bottom: float = 1.8,
    width_top: float = 1.6,
    curvature_depth: float = 0.08,
    segments_u: int = 8,
    segments_v: int = 4
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate compound curved, aerodynamic automotive windshield geometry."""
    bx, by, bz = bottom_center
    tx, ty, tz = top_center

    u_vals = np.linspace(-0.5, 0.5, segments_u + 1)
    v_vals = np.linspace(0.0, 1.0, segments_v + 1)

    verts: List[List[float]] = []

    for v in v_vals:
        # Interpolate center and width from bottom to top
        cx = (1.0 - v) * bx + v * tx
        cy = (1.0 - v) * by + v * ty
        cz = (1.0 - v) * bz + v * tz
        w = (1.0 - v) * width_bottom + v * width_top

        for u in u_vals:
            x = cx + u * w
            # Parabolic forward curvature bow (sagitta) along +Y
            bow = (1.0 - 4.0 * (u ** 2)) * curvature_depth
            y = cy + bow
            z = cz
            verts.append([float(x), float(y), float(z)])

    faces: List[List[int]] = []
    stride = segments_u + 1
    for j in range(segments_v):
        for i in range(segments_u):
            v0 = j * stride + i
            v1 = j * stride + (i + 1)
            v2 = (j + 1) * stride + (i + 1)
            v3 = (j + 1) * stride + i
            faces.append([v0, v1, v2, v3])

    return verts, faces


# ==============================================================================
# 2. Blender BMesh Integration Functions
# ==============================================================================

def create_filleted_box(
    bm: Any,
    min_v: Tuple[float, float, float],
    max_v: Tuple[float, float, float],
    bevel_radius: float = 0.02,
    bevel_segments: int = 2,
    material_index: int = 0
) -> dict:
    """Create a box in BMesh bounded by min_v and max_v, with optional edge filleting."""
    if not HAS_BPY or bm is None:
        verts, faces = calculate_box_geometry(min_v, max_v)
        return {"verts": verts, "faces": faces}

    size_x = max_v[0] - min_v[0]
    size_y = max_v[1] - min_v[1]
    size_z = max_v[2] - min_v[2]
    cx = (min_v[0] + max_v[0]) * 0.5
    cy = (min_v[1] + max_v[1]) * 0.5
    cz = (min_v[2] + max_v[2]) * 0.5

    matrix = mathutils.Matrix.Translation((cx, cy, cz)) @ mathutils.Matrix.Diagonal((size_x, size_y, size_z, 1.0))
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=matrix)
    verts = res["verts"]

    # Gather created faces
    faces = list({f for v in verts for f in v.link_faces})
    for f in faces:
        f.material_index = material_index
        f.smooth = True

    if bevel_radius > 0.001:
        edges = list({e for v in verts for e in v.link_edges})
        try:
            bmesh.ops.bevel(
                bm,
                geom=edges,
                offset=bevel_radius,
                offset_type='OFFSET',
                segments=bevel_segments,
                profile=0.5,
                affect='EDGES'
            )
        except Exception:
            pass

    return {"verts": [v.co[:] for v in bm.verts], "face_count": len(bm.faces)}


def create_cylinder(
    bm: Any,
    p1: Tuple[float, float, float],
    p2: Tuple[float, float, float],
    radius: float = 0.1,
    segments: int = 24,
    material_index: int = 0,
    cap_ends: bool = True
) -> dict:
    """Create an aligned cylinder between p1 and p2 in BMesh."""
    if not HAS_BPY or bm is None:
        verts, faces = calculate_cylinder_geometry(p1, p2, radius=radius, segments=segments, cap_ends=cap_ends)
        return {"verts": verts, "faces": faces}

    v1 = mathutils.Vector(p1)
    v2 = mathutils.Vector(p2)
    axis = v2 - v1
    depth = axis.length
    if depth < 1e-6:
        depth = 0.001
        axis = mathutils.Vector((0, 0, 1))

    mid = (v1 + v2) * 0.5
    rot = mathutils.Vector((0, 0, 1)).rotation_difference(axis)
    mat = mathutils.Matrix.Translation(mid) @ rot.to_matrix().to_4x4()

    res = bmesh.ops.create_cone(
        bm,
        cap_ends=cap_ends,
        cap_tris=False,
        segments=segments,
        radius1=radius,
        radius2=radius,
        depth=depth,
        matrix=mat
    )
    verts = res["verts"]
    faces = list({f for v in verts for f in v.link_faces})
    for f in faces:
        f.material_index = material_index
        f.smooth = True

    return {"verts": verts, "faces": faces}


def create_wheel_arch(
    bm: Any,
    center: Tuple[float, float, float],
    radius: float = 0.45,
    width: float = 0.15,
    lip_thickness: float = 0.02,
    lip_outset: float = 0.03,
    segments: int = 16,
    axis: str = "X",
    material_index: int = 0
) -> dict:
    """Create an automotive wheel flare arch inside BMesh."""
    verts_data, faces_data = calculate_wheel_arch_geometry(
        center=center, radius=radius, width=width,
        lip_thickness=lip_thickness, lip_outset=lip_outset,
        segments=segments, axis=axis
    )

    if not HAS_BPY or bm is None:
        return {"verts": verts_data, "faces": faces_data}

    bm_verts = [bm.verts.new(v) for v in verts_data]
    bm.verts.ensure_lookup_table()
    new_faces = []
    for f_idx in faces_data:
        try:
            f = bm.faces.new([bm_verts[i] for i in f_idx])
            f.material_index = material_index
            f.smooth = True
            new_faces.append(f)
        except ValueError:
            pass

    return {"verts": bm_verts, "faces": new_faces}


def create_curved_windshield(
    bm: Any,
    bottom_center: Tuple[float, float, float],
    top_center: Tuple[float, float, float],
    width_bottom: float = 1.8,
    width_top: float = 1.6,
    curvature_depth: float = 0.08,
    segments_u: int = 8,
    segments_v: int = 4,
    thickness: float = 0.01,
    material_index: int = 0
) -> dict:
    """Create a curved windshield mesh in BMesh."""
    verts_data, faces_data = calculate_windshield_geometry(
        bottom_center=bottom_center,
        top_center=top_center,
        width_bottom=width_bottom,
        width_top=width_top,
        curvature_depth=curvature_depth,
        segments_u=segments_u,
        segments_v=segments_v
    )

    if not HAS_BPY or bm is None:
        return {"verts": verts_data, "faces": faces_data}

    bm_verts = [bm.verts.new(v) for v in verts_data]
    bm.verts.ensure_lookup_table()
    new_faces = []
    for f_idx in faces_data:
        try:
            f = bm.faces.new([bm_verts[i] for i in f_idx])
            f.material_index = material_index
            f.smooth = True
            new_faces.append(f)
        except ValueError:
            pass

    return {"verts": bm_verts, "faces": new_faces}


def create_swept_profile(
    bm: Any,
    profile_points_2d: List[Tuple[float, float]],
    rail_points_3d: List[Tuple[float, float, float]],
    closed: bool = False,
    material_index: int = 0
) -> dict:
    """Sweep a 2D cross-section profile along a 3D rail."""
    if not HAS_BPY or bm is None:
        return {"profile_points": profile_points_2d, "rail_points": rail_points_3d}

    # Build rail vectors
    pts = [mathutils.Vector(p) for p in rail_points_3d]
    n_rail = len(pts)
    n_prof = len(profile_points_2d)

    ring_verts: List[List[Any]] = []

    for i in range(n_rail):
        curr = pts[i]
        if i == 0:
            tangent = (pts[1] - curr).normalized() if n_rail > 1 else mathutils.Vector((0, 1, 0))
        elif i == n_rail - 1:
            tangent = (curr - pts[i - 1]).normalized()
        else:
            tangent = (pts[i + 1] - pts[i - 1]).normalized()

        rot = mathutils.Vector((0, 0, 1)).rotation_difference(tangent)
        u_axis = rot @ mathutils.Vector((1, 0, 0))
        v_axis = rot @ mathutils.Vector((0, 1, 0))

        ring = []
        for pu, pv in profile_points_2d:
            pos = curr + pu * u_axis + pv * v_axis
            ring.append(bm.verts.new(pos))
        ring_verts.append(ring)

    new_faces = []
    for i in range(n_rail - 1):
        r0 = ring_verts[i]
        r1 = ring_verts[i + 1]
        lim = n_prof if closed else n_prof - 1
        for j in range(lim):
            j_next = (j + 1) % n_prof
            f = bm.faces.new([r0[j], r0[j_next], r1[j_next], r1[j]])
            f.material_index = material_index
            f.smooth = True
            new_faces.append(f)

    return {"faces": new_faces}


def apply_automotive_modifiers(
    obj: Any,
    bevel_width: float = 0.008,
    bevel_segments: int = 2,
    weighted_normal: bool = True,
    smooth_angle_deg: float = 35.0
) -> dict:
    """Apply standard automotive modifier stack (Smooth, Bevel, WeightedNormal)."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return {"status": "skipped_or_no_bpy"}

    # 1. Smooth all polygons
    mesh = obj.data
    for poly in mesh.polygons:
        poly.use_smooth = True

    # 2. Bevel modifier
    bevel_mod = obj.modifiers.get("Auto_Bevel")
    if not bevel_mod:
        bevel_mod = obj.modifiers.new("Auto_Bevel", "BEVEL")
    bevel_mod.width = float(bevel_width)
    bevel_mod.segments = int(bevel_segments)
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = math.radians(smooth_angle_deg)
    bevel_mod.profile = 0.5
    bevel_mod.harden_normals = True

    # 3. Weighted normal modifier
    if weighted_normal:
        wn_mod = obj.modifiers.get("Auto_WeightedNormal")
        if not wn_mod:
            wn_mod = obj.modifiers.new("Auto_WeightedNormal", "WEIGHTED_NORMAL")
        wn_mod.keep_sharp = True
        wn_mod.weight = 50

    return {"status": "applied", "modifiers": [m.name for m in obj.modifiers]}
