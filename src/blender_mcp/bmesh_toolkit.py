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


def boolean_difference(target_obj: Any, cutter_obj: Any, apply: bool = True) -> dict:
    """Carve cutter_obj from target_obj using boolean difference."""
    if not HAS_BPY or target_obj is None or cutter_obj is None:
        return {"status": "skipped_or_no_bpy"}

    init_verts = len(target_obj.data.vertices) if hasattr(target_obj, "data") and hasattr(target_obj.data, "vertices") else 0
    bool_mod = target_obj.modifiers.new("CLAS_Boolean_Diff", "BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.solver = "EXACT"
    bool_mod.object = cutter_obj

    if apply:
        applied = False
        try:
            with bpy.context.temp_override(object=target_obj, active_object=target_obj):
                bpy.ops.object.modifier_apply(modifier=bool_mod.name)
                applied = True
        except Exception:
            pass

        if not applied:
            depsgraph = bpy.context.evaluated_depsgraph_get()
            eval_obj = target_obj.evaluated_get(depsgraph)
            new_mesh = bpy.data.meshes.new_from_object(eval_obj)
            old_mesh = target_obj.data
            target_obj.modifiers.remove(bool_mod)
            target_obj.data = new_mesh
            bpy.data.meshes.remove(old_mesh)

    final_verts = len(target_obj.data.vertices) if hasattr(target_obj, "data") and hasattr(target_obj.data, "vertices") else 0
    return {"status": "success", "initial_verts": init_verts, "final_verts": final_verts}


def carve_cavity(
    target_obj: Any,
    cutter_spec: Any,
    bevel_segments: int = 2,
    harden_normals: bool = True
) -> dict:
    """Carve cavity in target_obj from parametric specification or cutter object."""
    if not HAS_BPY or target_obj is None:
        return {"status": "skipped_or_no_bpy"}

    is_temporary_cutter = False
    cutter_obj = None

    if isinstance(cutter_spec, str):
        cutter_obj = bpy.data.objects.get(cutter_spec)
        if not cutter_obj:
            return {"error": f"Cutter object '{cutter_spec}' not found"}
    elif isinstance(cutter_spec, dict):
        if "object" in cutter_spec or "name" in cutter_spec:
            name = cutter_spec.get("name") or cutter_spec.get("object")
            cutter_obj = bpy.data.objects.get(name)
            if not cutter_obj:
                return {"error": f"Cutter object '{name}' not found"}
        else:
            # Parametric cutter creation
            c_type = cutter_spec.get("type", "box").lower()
            loc = cutter_spec.get("location", (0.0, 0.0, 0.0))
            rot = cutter_spec.get("rotation", (0.0, 0.0, 0.0))
            cutter_mesh = bpy.data.meshes.new("_tmp_cutter_mesh")
            cutter_obj = bpy.data.objects.new("_tmp_cutter_obj", cutter_mesh)
            bpy.context.scene.collection.objects.link(cutter_obj)
            is_temporary_cutter = True

            bm = bmesh.new()
            if c_type == "cylinder":
                radius = float(cutter_spec.get("radius", 0.5))
                depth = float(cutter_spec.get("depth", 0.5))
                segs = int(cutter_spec.get("segments", 32))
                bmesh.ops.create_cone(
                    bm,
                    cap_ends=True,
                    segments=segs,
                    radius1=radius,
                    radius2=radius,
                    depth=depth
                )
            else:  # default box
                size = cutter_spec.get("size", (1.0, 1.0, 1.0))
                if isinstance(size, (int, float)):
                    sx, sy, sz = float(size), float(size), float(size)
                else:
                    sx, sy, sz = float(size[0]), float(size[1]), float(size[2])
                bmesh.ops.create_cube(bm, size=1.0)
                bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)

            bm.to_mesh(cutter_mesh)
            bm.free()

            cutter_obj.location = loc
            cutter_obj.rotation_euler = rot

    if not cutter_obj:
        return {"error": "Invalid cutter_spec provided"}

    # Execute boolean difference
    res = boolean_difference(target_obj, cutter_obj, apply=True)

    # Clean up temporary cutter
    if is_temporary_cutter:
        mesh_to_del = cutter_obj.data
        bpy.data.objects.remove(cutter_obj, do_unlink=True)
        if mesh_to_del:
            bpy.data.meshes.remove(mesh_to_del, do_unlink=True)

    # Optional bevel & normal hardening
    if bevel_segments > 0:
        bev = target_obj.modifiers.new("CLAS_Bevel", "BEVEL")
        bev.segments = int(bevel_segments)
        bev.harden_normals = bool(harden_normals)
        bev.limit_method = "ANGLE"
        bev.angle_limit = math.radians(35.0)

    return {"target": target_obj.name, "carved": True, "details": res}


def tile_quadrant_buffers(
    top_left: np.ndarray,
    top_right: np.ndarray,
    bottom_left: np.ndarray,
    bottom_right: np.ndarray
) -> np.ndarray:
    """Tile 4 quadrant pixel buffers (H, W, C) into a 2x2 grid (2H, 2W, C)."""
    top_row = np.concatenate([top_left, top_right], axis=1)
    bottom_row = np.concatenate([bottom_left, bottom_right], axis=1)
    return np.concatenate([top_row, bottom_row], axis=0)


def compute_laplacian_curvature(
    verts: np.ndarray,
    edges: Any,
    normals: np.ndarray
) -> np.ndarray:
    """Compute discrete graph Laplacian curvature per vertex.

    Returns:
    - curvature: (N,) float32 array, where:
        negative = convex peak / sharp ridge
        positive = concave crevice / cavity
    """
    num_verts = len(verts)
    neighbors = [[] for _ in range(num_verts)]
    for e in edges:
        u, v = int(e[0]), int(e[1])
        if 0 <= u < num_verts and 0 <= v < num_verts:
            neighbors[u].append(v)
            neighbors[v].append(u)

    curv = np.zeros(num_verts, dtype=np.float32)
    for i in range(num_verts):
        nbrs = neighbors[i]
        if not nbrs:
            continue
        laplacian = np.mean(verts[nbrs], axis=0) - verts[i]
        curv[i] = float(np.dot(laplacian, normals[i]))

    return curv


def eval_cubic_bezier_curve(
    p0: Any,
    p1: Any,
    p2: Any,
    p3: Any,
    num_samples: int = 16
) -> np.ndarray:
    """Evaluate cubic Bezier curve points using Bernstein polynomials."""
    p0_arr = np.asarray(p0, dtype=np.float32)
    p1_arr = np.asarray(p1, dtype=np.float32)
    p2_arr = np.asarray(p2, dtype=np.float32)
    p3_arr = np.asarray(p3, dtype=np.float32)

    t = np.linspace(0.0, 1.0, int(num_samples), dtype=np.float32)[:, None]
    om_t = 1.0 - t

    b0 = om_t**3
    b1 = 3.0 * (om_t**2) * t
    b2 = 3.0 * om_t * (t**2)
    b3 = t**3

    return (b0 * p0_arr + b1 * p1_arr + b2 * p2_arr + b3 * p3_arr).astype(np.float32)


def apply_smart_uv_unwrapping(
    obj: Any,
    angle_limit_deg: float = 66.0,
    island_margin: float = 0.02
) -> dict:
    """Ensure obj has valid UVMap and apply Smart UV Project for game-ready export."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return {"status": "skipped_or_no_bpy"}

    mesh = obj.data
    if not mesh.uv_layers:
        mesh.uv_layers.new(name="UVMap")
    mesh.uv_layers.active = mesh.uv_layers[0]

    try:
        with bpy.context.temp_override(object=obj, active_object=obj, selected_editable_objects=[obj]):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project(
                angle_limit=math.radians(angle_limit_deg),
                island_margin=island_margin
            )
            bpy.ops.object.mode_set(mode='OBJECT')
        return {
            "status": "unwrapped",
            "uv_layer": mesh.uv_layers.active.name,
            "polygons": len(mesh.polygons)
        }
    except Exception as e:
        return {"status": "fallback", "error": str(e)}


def carve_wheel_well_cavities(
    body_obj: Any,
    wheel_specs: dict,
    arch_clearance: float = 0.08,
    well_depth: float = 0.35
) -> dict:
    """Carve 4 recessed wheel well cavities into the body_obj using boolean difference."""
    if not HAS_BPY or body_obj is None or body_obj.type != 'MESH':
        return {"status": "skipped_or_no_bpy"}

    arch_radius = float(wheel_specs.get("arch_radius", 0.455))
    results = []

    arch_keys = ["front_left", "front_right", "rear_left", "rear_right"]
    for key in arch_keys:
        pos = wheel_specs.get(key)
        if not pos:
            continue
        cx, cy, cz = float(pos[0]), float(pos[1]), float(pos[2])
        sign_x = 1.0 if cx >= 0 else -1.0
        cutter_loc = (cx - sign_x * (well_depth * 0.3), cy, cz)

        cutter_spec = {
            "type": "cylinder",
            "radius": arch_radius,
            "depth": well_depth,
            "location": cutter_loc,
            "rotation": (0.0, math.radians(90.0), 0.0),
            "segments": 32
        }
        res = carve_cavity(body_obj, cutter_spec, bevel_segments=0, harden_normals=False)
        results.append({"arch": key, "result": res})

    return {"status": "carved", "wheel_wells": results}


def get_component_tree(archetype: str = "VEHICLE") -> dict:
    """Return formal 4-level component tree decomposition (Asset -> System -> Component -> Detail)."""
    arch = archetype.upper()

    # Domain 1: VEHICLE / AUTOMOTIVE
    if arch == "VEHICLE" or any(v in arch for v in ["CAR", "VAN", "TRUCK", "SEDAN", "COUPE", "AUTOMOBILE", "SUPERCAR", "SUV"]):
        return {
            "archetype": "VEHICLE",
            "domain": "VEHICLE",
            "systems": {
                "body_shell": {
                    "strategy": "subdivision_cage",
                    "components": ["hood_bonnet", "fenders_left_right", "cab_roof", "cargo_box", "rear_doors"],
                    "datums": ["centerline", "axle_planes", "beltline_z"]
                },
                "aerodynamics": {
                    "strategy": "subdivision_cage",
                    "components": ["front_bumper_cover", "lower_splitter", "radiator_grille_opening", "brake_cooling_ducts"],
                    "datums": ["ground_plane", "approach_angle"]
                },
                "lighting": {
                    "strategy": "boolean_bevel",
                    "components": ["headlamp_housings", "projector_lenses", "drl_strips", "rear_vertical_taillights"],
                    "datums": ["fascia_recesses"]
                },
                "wheel_assembly": {
                    "strategy": "subdivision_cage",
                    "components": ["treaded_tires", "rim_barrel", "10_hole_alloy_face", "center_hub_cap", "brake_disc_caliper"],
                    "datums": ["wheel_centers", "tire_envelopes"]
                },
                "secondary_trim": {
                    "strategy": "bezier_curve",
                    "components": ["roof_rails", "window_weather_seals", "side_rubbing_strips", "emergency_cable_harnesses"],
                    "datums": ["surface_contours"]
                }
            }
        }

    # Domain 2: ARCHITECTURE (Houses, Villas, Buildings, Facades, Cabins)
    if any(a in arch for a in ["ARCH", "HOUSE", "VILLA", "BUILDING", "FACADE", "CABIN", "COTTAGE", "MANSION"]):
        return {
            "archetype": arch,
            "domain": "ARCHITECTURE",
            "systems": {
                "foundation_slab": {
                    "strategy": "subdivision_cage",
                    "components": ["ground_slab", "perimeter_grade_beams", "entry_porch_slab", "foundation_footings"],
                    "datums": ["ground_plane_z0", "exterior_grade_offset"]
                },
                "structural_walls": {
                    "strategy": "boolean_bevel",
                    "components": ["exterior_cavity_walls", "load_bearing_piers", "interior_partitions", "lintel_bands"],
                    "datums": ["finished_floor_z", "exterior_wall_thickness_280mm", "window_sill_height", "lintel_height"]
                },
                "roof_structure": {
                    "strategy": "subdivision_cage",
                    "components": ["primary_roof_planes", "fascia_trim_boards", "soffit_panels", "overhang_eaves", "parapet_caps"],
                    "datums": ["ridge_line", "eaves_line", "overhang_projection_600mm"]
                },
                "fenestration": {
                    "strategy": "boolean_bevel",
                    "components": ["window_frames_and_mullions", "double_glazed_units", "exterior_sloped_sills", "entry_door_assembly"],
                    "datums": ["rough_opening_reveals_150mm", "jamb_alignment"]
                },
                "architectural_trim": {
                    "strategy": "bezier_curve",
                    "components": ["corner_quoins", "exterior_molding_bands", "gutter_and_downspouts", "canopy_supports"],
                    "datums": ["envelope_boundary_alignment"]
                }
            }
        }

    # Domain 3: INTERIOR SPACES (Living Rooms, Bedrooms, Kitchens)
    if any(i in arch for i in ["ROOM", "INTERIOR", "BEDROOM", "KITCHEN", "BATHROOM", "LIVING"]):
        return {
            "archetype": arch,
            "domain": "INTERIOR_SPACES",
            "systems": {
                "room_envelope": {
                    "strategy": "boolean_bevel",
                    "components": ["finished_flooring_layer", "perimeter_drywall_planes", "ceiling_plane", "recessed_ceiling_tray"],
                    "datums": ["finished_floor_level", "clear_ceiling_height", "tray_drop_150mm"]
                },
                "trim_carpentry": {
                    "strategy": "bezier_curve",
                    "components": ["profiled_baseboards", "cove_crown_moldings", "door_architraves", "window_casing_surrounds"],
                    "datums": ["floor_wall_junction", "wall_ceiling_junction", "casing_perimeter"]
                },
                "built_in_millwork": {
                    "strategy": "boolean_bevel",
                    "components": ["cabinet_carcasses", "countertops_with_waterfall_edge", "shaker_cabinet_doors", "recessed_kickplates"],
                    "datums": ["countertop_datum_900mm", "backsplash_height_600mm"]
                },
                "ambient_lighting": {
                    "strategy": "subdivision_cage",
                    "components": ["recessed_pot_light_fixtures", "led_cove_troughs", "pendant_drop_fixtures", "flush_mount_diffusers"],
                    "datums": ["ceiling_grid_centers", "cove_lip_datum"]
                }
            }
        }

    # Domain 4: FURNITURE & PRODUCT DESIGN (Sofas, Chairs, Tables, Beds, Desks)
    if any(f in arch for f in ["SOFA", "COUCH", "CHAIR", "ARMCHAIR", "TABLE", "DESK", "BED", "BENCH", "FURNITURE"]):
        return {
            "archetype": arch,
            "domain": "FURNITURE_PRODUCT",
            "systems": {
                "cushion_assemblies": {
                    "strategy": "procedural_loft",
                    "components": ["crowned_seat_cushions", "ergonomic_back_cushions", "perimeter_welt_piping", "side_bolsters"],
                    "datums": ["seat_plane_z440mm", "cushion_crown_apex", "comfort_compression_depth"]
                },
                "frame_and_chassis": {
                    "strategy": "subdivision_cage",
                    "components": ["internal_hardwood_frame", "contoured_armrest_profiles", "inclined_backrest_shell", "seat_apron"],
                    "datums": ["seat_incline_angle_104deg", "armrest_height_datum", "perimeter_clearance"]
                },
                "support_legs": {
                    "strategy": "boolean_bevel",
                    "components": ["tapered_turned_legs", "metal_sled_runners", "protective_foot_glides", "structural_corner_brackets"],
                    "datums": ["ground_contact_plane", "mounting_socket_centers"]
                },
                "tactile_hardware": {
                    "strategy": "bezier_curve",
                    "components": ["drawer_pull_handles", "edge_beveled_surrounds", "fabric_tufting_buttons", "seam_stitches"],
                    "datums": ["fillet_edge_radius", "ergonomic_touch_points"]
                }
            }
        }

    # Default Universal Fallback (Clean Spatial Decomposition, NOT Car Chassis)
    return {
        "archetype": arch,
        "domain": "GENERAL_SPATIAL",
        "systems": {
            "primary_structure": {"strategy": "subdivision_cage", "components": ["core_body", "outer_hull"]},
            "secondary_housings": {"strategy": "boolean_bevel", "components": ["apertures", "beveled_mounts"]},
            "connective_trim": {"strategy": "bezier_curve", "components": ["perimeter_trims", "conduits"]},
            "wear_and_finish": {"strategy": "sculpt_and_bake", "components": ["surface_breakup", "tactile_bevels"]}
        }
    }


def crop_image_array(img: np.ndarray, box: list[float] | tuple[float, float, float, float]) -> np.ndarray:
    """Crop image numpy array using normalized coordinates [ymin, xmin, ymax, xmax]."""
    h, w = img.shape[:2]
    ymin, xmin, ymax, xmax = box
    r0 = max(0, min(h - 1, int(round(ymin * h))))
    r1 = max(r0 + 1, min(h, int(round(ymax * h))))
    c0 = max(0, min(w - 1, int(round(xmin * w))))
    c1 = max(c0 + 1, min(w, int(round(xmax * w))))
    return img[r0:r1, c0:c1].copy()


def calculate_spline_normals_and_lengths(points: Any) -> tuple[np.ndarray, np.ndarray]:
    """Calculate cumulative arc lengths and tangent vectors along 3D spline keypoints."""
    pts = np.asarray(points, dtype=np.float32)
    n = len(pts)
    if n < 2:
        return np.zeros(n, dtype=np.float32), np.zeros((n, 3), dtype=np.float32)

    diffs = pts[1:] - pts[:-1]
    seg_lens = np.linalg.norm(diffs, axis=1)
    cum_lens = np.zeros(n, dtype=np.float32)
    cum_lens[1:] = np.cumsum(seg_lens)

    tangents = np.zeros((n, 3), dtype=np.float32)
    tangents[0] = diffs[0] / max(1e-7, seg_lens[0])
    tangents[-1] = diffs[-1] / max(1e-7, seg_lens[-1])
    for i in range(1, n - 1):
        v = pts[i + 1] - pts[i - 1]
        norm_v = np.linalg.norm(v)
        tangents[i] = v / max(1e-7, norm_v)

    return cum_lens, tangents


def create_bezier_tube(
    name: str,
    points: list,
    radius: float = 0.02,
    resolution: int = 12,
    fill_caps: bool = True,
    collection_name: str | None = None
) -> dict:
    """Create a non-destructive 3D curve tube (cables, pipes, trims)."""
    if not HAS_BPY:
        return {"status": "skipped_or_no_bpy", "name": name, "points": len(points)}

    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = float(radius)
    curve_data.bevel_resolution = int(resolution)
    curve_data.use_fill_caps = bool(fill_caps)

    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(len(points) - 1)

    for i, pt in enumerate(points):
        bp = spline.bezier_points[i]
        bp.co = mathutils.Vector(pt)
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'

    obj = bpy.data.objects.new(name, curve_data)
    col = bpy.data.collections.get(collection_name) if collection_name else bpy.context.scene.collection
    col.objects.link(obj)
    return {"status": "created", "name": obj.name, "points": len(points), "bevel_depth": radius}


def setup_subdivision_cage(
    obj: Any,
    levels: int = 2,
    render_levels: int = 2,
    bevel_width: float = 0.008,
    weighted_normal: bool = True
) -> dict:
    """Configure modern Aryan 3D / Isto Inc low-poly subdivision cage workflow."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return {"status": "skipped_or_no_bpy"}

    for poly in obj.data.polygons:
        poly.use_smooth = True

    sub_mod = obj.modifiers.get("Cage_Subsurf")
    if not sub_mod:
        sub_mod = obj.modifiers.new("Cage_Subsurf", "SUBSURF")
    sub_mod.levels = int(levels)
    sub_mod.render_levels = int(render_levels)

    if bevel_width > 0:
        bev_mod = obj.modifiers.get("Cage_Bevel")
        if not bev_mod:
            bev_mod = obj.modifiers.new("Cage_Bevel", "BEVEL")
        bev_mod.width = float(bevel_width)
        bev_mod.segments = 2
        bev_mod.limit_method = 'ANGLE'
        bev_mod.angle_limit = math.radians(35.0)
        bev_mod.harden_normals = True

    if weighted_normal:
        wn_mod = obj.modifiers.get("Cage_WeightedNormal")
        if not wn_mod:
            wn_mod = obj.modifiers.new("Cage_WeightedNormal", "WEIGHTED_NORMAL")
        wn_mod.keep_sharp = True
        wn_mod.weight = 50

    return {"status": "configured", "object": obj.name, "modifiers": [m.name for m in obj.modifiers]}


def crop_reference_region(
    image_path: str,
    crop_box: list[float] | None = None,
    output_path: str | None = None,
    region_name: str = "region"
) -> dict:
    """Extract named visual region crop from reference image to eliminate hallucination."""
    import os
    if not os.path.exists(image_path):
        return {"error": f"Image file not found: {image_path}"}

    REGION_PRESETS = {
        "nose_grille": [0.35, 0.05, 0.70, 0.45],
        "hood_windshield": [0.15, 0.15, 0.55, 0.60],
        "front_wheel_arch": [0.45, 0.10, 0.85, 0.40],
        "side_flank": [0.25, 0.20, 0.75, 0.85],
        "rear_fascia": [0.20, 0.60, 0.80, 0.98]
    }

    box = crop_box or REGION_PRESETS.get(region_name.lower(), [0.0, 0.0, 1.0, 1.0])

    if output_path is None:
        import tempfile
        output_path = os.path.join(tempfile.gettempdir(), f"crop_{region_name}.png")

    try:
        from PIL import Image
        with Image.open(image_path) as im:
            w, h = im.size
            ymin, xmin, ymax, xmax = box
            px_box = (int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h))
            cropped = im.crop(px_box)
            cropped.save(output_path)
        return {
            "status": "success",
            "region": region_name,
            "crop_path": output_path,
            "box": box,
            "source": image_path
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}






