"""Apex GT-R Concept Procedural Vehicle Generator for Blender.

Procedurally generates the 12 modular component assemblies for the Apex GT-R Concept
supercar strictly following the reference blueprint dimensions, ~30,000 polygon budget,
and the in-memory 90/10 Hybrid Procedural Pipeline.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
import numpy as np

try:
    import bpy
    import bmesh
    import mathutils
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


# ==============================================================================
# 1. Blueprint Dimensions & Architectural Constants
# ==============================================================================

APEX_GTR_ENVELOPE: Dict[str, float] = {
    "length": 4.610,         # Total length (meters)
    "width": 1.870,          # Body width without flares
    "width_flared": 1.980,   # Widebody flared fender width
    "height": 1.180,         # Roofline peak
    "wheelbase": 2.700,      # Distance between front & rear axles
    "front_axle_y": 1.350,   # Front axle Y coordinate
    "rear_axle_y": -1.350,   # Rear axle Y coordinate
    "front_overhang": 0.955, # Distance from front axle to front bumper
    "rear_overhang": 0.955,  # Distance from rear axle to rear diffuser
    "ground_clearance": 0.100, # Track stance ground clearance
    "wheel_radius": 0.340,   # Tire outer radius
    "rim_radius": 0.260,     # 20-inch rim radius
    "wheel_center_z": 0.340, # Wheel axle height
    "tire_width_front": 0.280,
    "tire_width_rear": 0.320,
    "track_width_front": 1.660,
    "track_width_rear": 1.680,
}

COLLECTION_HIERARCHY: Dict[str, List[str]] = {
    "01_Body_Structure": [
        "GTR_Body_Shell",
        "GTR_Fenders_Widebody",
        "GTR_Hood",
    ],
    "02_Aero_Fascia": [
        "GTR_Front_Bumper_Splitter",
        "GTR_Side_Skirts",
        "GTR_Rear_Diffuser_Exhaust",
        "GTR_Rear_Wing",
    ],
    "03_Glass_and_Mirrors": [
        "GTR_Glass_Canopy",
        "GTR_Aero_Mirrors",
    ],
    "04_Lighting": [
        "GTR_Headlights",
        "GTR_Tail_Lights",
    ],
    "05_Wheels": [
        "GTR_Wheel_FL",
        "GTR_Wheel_FR",
        "GTR_Wheel_RL",
        "GTR_Wheel_RR",
    ],
}


# ==============================================================================
# 2. PBR Automotive Material Vault Specifications
# ==============================================================================

GTR_MATERIAL_SPECS: Dict[str, Dict[str, Any]] = {
    "MAT_GTR_Paint_Gunmetal": {
        "base_color": (0.04, 0.04, 0.05, 1.0),
        "metallic": 0.92,
        "roughness": 0.22,
        "clearcoat": 1.0,
        "clearcoat_roughness": 0.03,
    },
    "MAT_GTR_Carbon_Satin": {
        "base_color": (0.02, 0.02, 0.02, 1.0),
        "metallic": 0.10,
        "roughness": 0.35,
        "clearcoat": 0.4,
        "clearcoat_roughness": 0.1,
    },
    "MAT_GTR_Crimson_Accent": {
        "base_color": (0.85, 0.02, 0.03, 1.0),
        "metallic": 0.20,
        "roughness": 0.25,
        "clearcoat": 0.8,
        "clearcoat_roughness": 0.05,
    },
    "MAT_GTR_Automotive_Glass": {
        "base_color": (0.08, 0.10, 0.12, 1.0),
        "metallic": 0.0,
        "roughness": 0.02,
        "transmission": 1.0,
        "ior": 1.52,
    },
    "MAT_GTR_Tire_Rubber": {
        "base_color": (0.03, 0.03, 0.03, 1.0),
        "metallic": 0.0,
        "roughness": 0.78,
        "clearcoat": 0.0,
    },
    "MAT_GTR_Brake_Steel": {
        "base_color": (0.75, 0.75, 0.75, 1.0),
        "metallic": 0.95,
        "roughness": 0.30,
        "clearcoat": 0.0,
    },
    "MAT_GTR_Caliper_Red": {
        "base_color": (0.90, 0.01, 0.01, 1.0),
        "metallic": 0.10,
        "roughness": 0.15,
        "clearcoat": 1.0,
        "clearcoat_roughness": 0.03,
    },
    "MAT_GTR_LED_Emissive": {
        "base_color": (1.0, 1.0, 1.0, 1.0),
        "emission_color": (1.0, 1.0, 1.0, 1.0),
        "emission_strength": 15.0,
        "metallic": 0.0,
        "roughness": 0.1,
    },
    "MAT_GTR_Tail_Emissive": {
        "base_color": (0.9, 0.02, 0.02, 1.0),
        "emission_color": (1.0, 0.02, 0.02, 1.0),
        "emission_strength": 12.0,
        "metallic": 0.0,
        "roughness": 0.1,
    },
}


def calculate_bounding_dimensions(
    min_v: Tuple[float, float, float],
    max_v: Tuple[float, float, float]
) -> Dict[str, float]:
    """Calculate width (X), length (Y), and height (Z) from bounding box vectors."""
    return {
        "width": abs(max_v[0] - min_v[0]),
        "length": abs(max_v[1] - min_v[1]),
        "height": abs(max_v[2] - min_v[2]),
    }


def setup_scene_hierarchy() -> Dict[str, Any]:
    """Initialize clean Blender scene collections for the Apex GT-R Concept."""
    if not HAS_BPY:
        return {}

    # Purge default scene items if present
    for obj in list(bpy.data.objects):
        if obj.name in {"Cube", "Light"}:
            bpy.data.objects.remove(obj, do_unlink=True)

    # Master collection
    master_col_name = "Apex_GTR_Concept"
    if master_col_name in bpy.data.collections:
        master_col = bpy.data.collections[master_col_name]
    else:
        master_col = bpy.data.collections.new(master_col_name)
        bpy.context.scene.collection.children.link(master_col)

    created_collections: Dict[str, bpy.types.Collection] = {"root": master_col}

    for sub_name in COLLECTION_HIERARCHY.keys():
        if sub_name in bpy.data.collections:
            sub_col = bpy.data.collections[sub_name]
        else:
            sub_col = bpy.data.collections.new(sub_name)
            master_col.children.link(sub_col)
        created_collections[sub_name] = sub_col

    return created_collections


def _set_bsdf_socket(node: Any, socket_names: List[str], value: Any) -> bool:
    """Set socket value dynamically checking for Blender 3.x/4.x/5.x socket names."""
    if node is None or not hasattr(node, "inputs"):
        return False
    for name in socket_names:
        sock = node.inputs.get(name)
        if sock is not None:
            try:
                sock.default_value = value
                return True
            except Exception:
                pass
    return False


def setup_gtr_materials() -> Dict[str, Any]:
    """Build and return all 9 PBR materials for the Apex GT-R Concept."""
    if not HAS_BPY:
        return {}

    built_materials: Dict[str, bpy.types.Material] = {}

    for mat_name, spec in GTR_MATERIAL_SPECS.items():
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # Find Principled BSDF
        bsdf = None
        for n in nodes:
            if n.type == 'BSDF_PRINCIPLED':
                bsdf = n
                break
        if bsdf is None:
            bsdf = nodes.new('ShaderNodeBsdfPrincipled')

        # Base Color
        if "base_color" in spec:
            _set_bsdf_socket(bsdf, ["Base Color"], spec["base_color"])

        # Metallic
        if "metallic" in spec:
            _set_bsdf_socket(bsdf, ["Metallic"], spec["metallic"])

        # Roughness
        if "roughness" in spec:
            _set_bsdf_socket(bsdf, ["Roughness"], spec["roughness"])

        # Clearcoat / Coat Weight
        if "clearcoat" in spec:
            _set_bsdf_socket(bsdf, ["Coat Weight", "Coat", "Clearcoat"], spec["clearcoat"])
        if "clearcoat_roughness" in spec:
            _set_bsdf_socket(bsdf, ["Coat Roughness", "Clearcoat Roughness"], spec["clearcoat_roughness"])

        # Transmission
        if "transmission" in spec:
            _set_bsdf_socket(bsdf, ["Transmission Weight", "Transmission"], spec["transmission"])
        if "ior" in spec:
            _set_bsdf_socket(bsdf, ["IOR"], spec["ior"])

        # Emission
        if "emission_color" in spec:
            _set_bsdf_socket(bsdf, ["Emission Color", "Emission"], spec["emission_color"])
        if "emission_strength" in spec:
            _set_bsdf_socket(bsdf, ["Emission Strength"], spec["emission_strength"])

        built_materials[mat_name] = mat

    return built_materials


# ==============================================================================
# 3. Component Assembly Generators: Body Structure (Phase 2)
# ==============================================================================

def generate_body_shell_mesh_data(
    ny: int = 49,
    nu: int = 49
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Body_Shell."""
    y_stations = np.linspace(0.88, -2.15, ny)
    verts: List[List[float]] = []
    faces: List[List[int]] = []

    # 1. Outer Aerodynamic Shell
    for i, y in enumerate(y_stations):
        t = i / (ny - 1)
        if y >= 0.25:
            # Cowl to A-pillar top
            tt = (y - 0.25) / (0.88 - 0.25)
            z_top = 1.15 * (1 - tt) + 0.78 * tt
            w_top = 0.62 * (1 - tt) + 0.74 * tt
        elif y >= -0.40:
            # Roof peak
            z_top = 1.180
            w_top = 0.60
        elif y >= -1.50:
            # Fastback canopy slope
            tt = (y - (-1.50)) / (-0.40 - (-1.50))
            z_top = 0.85 * (1 - tt) + 1.180 * tt
            w_top = 0.72 * (1 - tt) + 0.60 * tt
        else:
            # Rear decklid to ducktail
            tt = (y - (-2.15)) / (-1.50 - (-2.15))
            z_top = 0.86 * (1 - tt) + 0.85 * tt
            w_top = 0.76 * (1 - tt) + 0.72 * tt

        z_sill = 0.12
        w_sill = 0.84

        # Side scoop pinch ahead of rear wheels
        if -1.10 <= y <= -0.45:
            scoop_factor = math.sin((y - (-1.10)) / 0.65 * math.pi)
            w_belt = 0.91 - 0.10 * scoop_factor
        else:
            w_belt = 0.91
        z_belt = 0.70 + 0.04 * math.sin(t * math.pi)

        ring = []
        for j in range(nu):
            s = j / (nu - 1)  # 0: left sill to 1: right sill
            if s <= 0.25:
                # Left rocker sill to left beltline
                u = s / 0.25
                x = -w_sill * (1 - u) + (-w_belt) * u
                z = z_sill * (1 - u) + z_belt * u
            elif s <= 0.5:
                # Left beltline to roof center
                u = (s - 0.25) / 0.25
                x = -w_belt * (1 - u) + 0.0 * u
                bub = 0.015 * math.sin(u * math.pi) if z_top > 0.95 else 0.0
                z = z_belt * (1 - u) + z_top * u + bub
            elif s <= 0.75:
                # Roof center to right beltline
                u = (s - 0.5) / 0.25
                x = 0.0 * (1 - u) + w_belt * u
                bub = 0.015 * math.sin((1 - u) * math.pi) if z_top > 0.95 else 0.0
                z = z_top * (1 - u) + z_belt * u + bub
            else:
                # Right beltline to right rocker sill
                u = (s - 0.75) / 0.25
                x = w_belt * (1 - u) + w_sill * u
                z = z_belt * (1 - u) + z_sill * u

            ring.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])
        verts.extend(ring)

    # Shell Quad Faces
    for i in range(ny - 1):
        for j in range(nu - 1):
            i0 = i * nu + j
            i1 = i0 + 1
            i2 = (i + 1) * nu + (j + 1)
            i3 = (i + 1) * nu + j
            faces.append([i0, i1, i2, i3])

    # 2. Underbody Floor Pan (connecting left sill to right sill at Z=0.10)
    floor_start_idx = len(verts)
    n_floor = 17
    for i, y in enumerate(y_stations):
        w_sill = 0.84
        for k in range(n_floor):
            sf = k / (n_floor - 1)
            xf = -w_sill * (1 - sf) + w_sill * sf
            zf = 0.100
            verts.append([round(float(xf), 4), round(float(y), 4), round(float(zf), 4)])

    for i in range(ny - 1):
        for k in range(n_floor - 1):
            f0 = floor_start_idx + i * n_floor + k
            f1 = f0 + 1
            f2 = floor_start_idx + (i + 1) * n_floor + (k + 1)
            f3 = floor_start_idx + (i + 1) * n_floor + k
            faces.append([f0, f3, f2, f1])  # outward downward normal

    return verts, faces


def build_body_shell(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Body_Shell inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_body_shell_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Body_Shell_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    # Smooth shading
    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Body_Shell", mesh)

    # Materials
    if "MAT_GTR_Paint_Gunmetal" in materials:
        obj.data.materials.append(materials["MAT_GTR_Paint_Gunmetal"])
    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])

    # Modifiers
    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.006
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    # Link to collection
    col = collections.get("01_Body_Structure", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


def generate_fenders_mesh_data(
    n_theta: int = 32,
    n_radial: int = 10
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for flared widebody fenders."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    configs = [
        # (yc, r_in, r_out, x_body, x_flare, side, is_front)
        (1.350, 0.380, 0.470, 0.900, 0.985, -1, True),   # Front Left
        (1.350, 0.380, 0.470, 0.900, 0.985, 1, True),    # Front Right
        (-1.350, 0.390, 0.480, 0.910, 0.995, -1, False), # Rear Left
        (-1.350, 0.390, 0.480, 0.910, 0.995, 1, False),  # Rear Right
    ]

    for yc, r_in, r_out, x_body, x_flare, side, is_front in configs:
        base_idx = len(all_verts)
        # Angular span extending down to rocker sill (Z=0.14)
        extra_th = math.asin(min(0.99, (0.340 - 0.140) / r_in))
        th_min = -extra_th
        th_max = math.pi + extra_th

        # 1. Blister arch surface
        for i in range(n_theta + 1):
            t_angle = i / n_theta
            th = th_min * (1 - t_angle) + th_max * t_angle
            sin_th = math.sin(th)
            cos_th = math.cos(th)

            for j in range(n_radial + 1):
                rf = j / n_radial
                r = r_in * (1 - rf) + r_out * rf
                y_r = yc - cos_th * r
                z_r = max(0.100, 0.340 + sin_th * r)
                # Parabolic blister flare profile
                flare_shape = 1.0 - (rf ** 1.7)
                x = side * (x_body + (x_flare - x_body) * flare_shape)
                all_verts.append([round(float(x), 4), round(float(y_r), 4), round(float(z_r), 4)])

        for i in range(n_theta):
            for j in range(n_radial):
                v0 = base_idx + i * (n_radial + 1) + j
                v1 = v0 + 1
                v2 = base_idx + (i + 1) * (n_radial + 1) + (j + 1)
                v3 = base_idx + (i + 1) * (n_radial + 1) + j
                if side < 0:
                    all_faces.append([v0, v1, v2, v3])
                else:
                    all_faces.append([v0, v3, v2, v1])

        # 2. Inward wheel arch return lip flange (15mm return inside wheel well)
        lip_base = len(all_verts)
        n_lip = 3
        for i in range(n_theta + 1):
            t_angle = i / n_theta
            th = th_min * (1 - t_angle) + th_max * t_angle
            sin_th = math.sin(th)
            cos_th = math.cos(th)
            y_r = yc - cos_th * r_in
            z_r = 0.340 + sin_th * r_in
            for k in range(n_lip + 1):
                kf = k / n_lip
                x = side * (x_flare - 0.035 * kf)
                all_verts.append([round(float(x), 4), round(float(y_r), 4), round(float(z_r), 4)])

        for i in range(n_theta):
            for k in range(n_lip):
                v0 = lip_base + i * (n_lip + 1) + k
                v1 = v0 + 1
                v2 = lip_base + (i + 1) * (n_lip + 1) + (k + 1)
                v3 = lip_base + (i + 1) * (n_lip + 1) + k
                if side < 0:
                    all_faces.append([v0, v3, v2, v1])
                else:
                    all_faces.append([v0, v1, v2, v3])

        # 3. Aero air relief louvers (only on front fenders, behind wheel arch)
        if is_front:
            louver_base = len(all_verts)
            n_louver_v = 4
            for lv in range(n_louver_v):
                y_lv = 0.980 + lv * 0.060
                z_lv = 0.380 + lv * 0.080
                # 4 vertices per louver slat
                x0 = side * 0.920
                x1 = side * 0.965
                all_verts.append([round(float(x0), 4), round(float(y_lv), 4), round(float(z_lv), 4)])
                all_verts.append([round(float(x1), 4), round(float(y_lv), 4), round(float(z_lv + 0.025), 4)])
                all_verts.append([round(float(x1), 4), round(float(y_lv + 0.040), 4), round(float(z_lv + 0.025), 4)])
                all_verts.append([round(float(x0), 4), round(float(y_lv + 0.040), 4), round(float(z_lv), 4)])
                lv_idx = louver_base + lv * 4
                if side < 0:
                    all_faces.append([lv_idx, lv_idx + 1, lv_idx + 2, lv_idx + 3])
                else:
                    all_faces.append([lv_idx, lv_idx + 3, lv_idx + 2, lv_idx + 1])

    return all_verts, all_faces


def build_widebody_fenders(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Fenders_Widebody inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_fenders_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Fenders_Widebody_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Fenders_Widebody", mesh)

    if "MAT_GTR_Paint_Gunmetal" in materials:
        obj.data.materials.append(materials["MAT_GTR_Paint_Gunmetal"])
    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])

    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.005
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("01_Body_Structure", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 4. Component Assembly Generators: Glass Canopy (Phase 2)
# ==============================================================================

def generate_glass_mesh_data(
    ny_ws: int = 20,
    nx_ws: int = 18,
    ny_side: int = 16,
    nz_side: int = 12,
    ny_rear: int = 20,
    nx_rear: int = 18
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Glass_Canopy."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    # 1. Front Windshield (cowl y=0.88 to header y=0.25)
    ws_base = len(all_verts)
    for i in range(ny_ws + 1):
        yf = i / ny_ws
        y = 0.880 * (1 - yf) + 0.250 * yf
        z_base = 0.780 * (1 - yf) + 1.140 * yf
        w = 0.720 * (1 - yf) + 0.600 * yf

        for j in range(nx_ws + 1):
            xf = j / nx_ws
            x = -w * (1 - xf) + w * xf
            arc = math.cos((xf - 0.5) * math.pi) * 0.040
            all_verts.append([round(float(x), 4), round(float(y + arc * 0.3), 4), round(float(z_base + arc * 0.5), 4)])

    for i in range(ny_ws):
        for j in range(nx_ws):
            v0 = ws_base + i * (nx_ws + 1) + j
            v1 = v0 + 1
            v2 = ws_base + (i + 1) * (nx_ws + 1) + (j + 1)
            v3 = ws_base + (i + 1) * (nx_ws + 1) + j
            all_faces.append([v0, v1, v2, v3])

    # 2. Frameless Door Windows (Left & Right)
    for side in (-1, 1):
        side_base = len(all_verts)
        for i in range(ny_side + 1):
            yf = i / ny_side
            y = 0.250 * (1 - yf) + (-0.650) * yf
            z_top = 1.140 * (1 - yf) + 1.170 * yf
            z_bot = 0.700

            for j in range(nz_side + 1):
                zf = j / nz_side
                z = z_bot * (1 - zf) + z_top * zf
                w = 0.750 * (1 - zf) + 0.600 * zf
                x = side * w
                all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

        for i in range(ny_side):
            for j in range(nz_side):
                v0 = side_base + i * (nz_side + 1) + j
                v1 = v0 + 1
                v2 = side_base + (i + 1) * (nz_side + 1) + (j + 1)
                v3 = side_base + (i + 1) * (nz_side + 1) + j
                if side < 0:
                    all_faces.append([v0, v1, v2, v3])
                else:
                    all_faces.append([v0, v3, v2, v1])

    # 3. Fastback Rear Hatch Glass (y=-0.65 to y=-1.50)
    rear_base = len(all_verts)
    for i in range(ny_rear + 1):
        yf = i / ny_rear
        y = -0.650 * (1 - yf) + (-1.500) * yf
        z_base = 1.160 * (1 - yf) + 0.850 * yf
        w = 0.580 * (1 - yf) + 0.680 * yf

        for j in range(nx_rear + 1):
            xf = j / nx_rear
            x = -w * (1 - xf) + w * xf
            arc = math.cos((xf - 0.5) * math.pi) * 0.018
            all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z_base + arc), 4)])

    for i in range(ny_rear):
        for j in range(nx_rear):
            v0 = rear_base + i * (nx_rear + 1) + j
            v1 = v0 + 1
            v2 = rear_base + (i + 1) * (nx_rear + 1) + (j + 1)
            v3 = rear_base + (i + 1) * (nx_rear + 1) + j
            all_faces.append([v0, v1, v2, v3])

    return all_verts, all_faces


def build_glass_canopy(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Glass_Canopy inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_glass_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Glass_Canopy_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Glass_Canopy", mesh)

    if "MAT_GTR_Automotive_Glass" in materials:
        obj.data.materials.append(materials["MAT_GTR_Automotive_Glass"])
    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])

    # Solidify modifier for glass refraction depth
    sol = obj.modifiers.new("Auto_Solidify", 'SOLIDIFY')
    sol.thickness = 0.004

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("03_Glass_and_Mirrors", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 5. Component Assembly Generators: Front Bumper & Splitter (Phase 3)
# ==============================================================================

def generate_front_bumper_mesh_data(
    ny_b: int = 24,
    nx_b: int = 32,
    n_spl_y: int = 16,
    n_spl_x: int = 28
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Front_Bumper_Splitter."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    # 1. Front Bumper Main Fascia
    b_base = len(all_verts)
    for i in range(ny_b + 1):
        yf = i / ny_b
        y_center = 1.800 + 0.450 * yf
        z_bot = 0.120 + 0.040 * yf
        z_top = 0.650 + 0.030 * yf

        for j in range(nx_b + 1):
            xf = j / nx_b
            x = -0.920 * (1 - xf) + 0.920 * xf
            sweep = 0.350 * (1.0 - (x / 0.920) ** 2)
            y = 1.800 + (y_center - 1.800) * (sweep / 0.350)
            z = z_bot * (1 - yf) + z_top * yf
            all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

    for i in range(ny_b):
        for j in range(nx_b):
            v0 = b_base + i * (nx_b + 1) + j
            v1 = v0 + 1
            v2 = b_base + (i + 1) * (nx_b + 1) + (j + 1)
            v3 = b_base + (i + 1) * (nx_b + 1) + j
            all_faces.append([v0, v1, v2, v3])

    # 2. Ground-Scraping Front Splitter Blade (Z=0.050 to 0.070, Y reaching 2.305)
    spl_base = len(all_verts)
    for k in (0, 1):
        z_spl = 0.050 if k == 0 else 0.070
        for i in range(n_spl_y + 1):
            yf = i / n_spl_y
            y_curr = 1.850 * (1 - yf) + 2.305 * yf

            for j in range(n_spl_x + 1):
                xf = j / n_spl_x
                x = -0.940 * (1 - xf) + 0.940 * xf
                spl_sweep = 0.380 * (1.0 - (x / 0.940) ** 2)
                y = 1.850 + (y_curr - 1.850) * max(0.2, spl_sweep / 0.380)
                all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z_spl), 4)])

    n_pts_layer = (n_spl_y + 1) * (n_spl_x + 1)
    for layer in (0, 1):
        l_base = spl_base + layer * n_pts_layer
        for i in range(n_spl_y):
            for j in range(n_spl_x):
                v0 = l_base + i * (n_spl_x + 1) + j
                v1 = v0 + 1
                v2 = l_base + (i + 1) * (n_spl_x + 1) + (j + 1)
                v3 = l_base + (i + 1) * (n_spl_x + 1) + j
                if layer == 0:
                    all_faces.append([v0, v3, v2, v1])
                else:
                    all_faces.append([v0, v1, v2, v3])

    # Splitter leading edge perimeter rim
    for j in range(n_spl_x):
        b_lead0 = spl_base + n_spl_y * (n_spl_x + 1) + j
        b_lead1 = b_lead0 + 1
        t_lead0 = b_lead0 + n_pts_layer
        t_lead1 = b_lead1 + n_pts_layer
        all_faces.append([b_lead0, b_lead1, t_lead1, t_lead0])

    # 3. Aerodynamic Dive Planes / Canards (2 pairs on left and right)
    canard_base = len(all_verts)
    n_can_u = 8
    n_can_v = 6
    for side in (-1, 1):
        for tier in (0, 1):
            c_layer_base = len(all_verts)
            z_c_base = 0.260 + tier * 0.160
            y_c_base = 2.080 + tier * 0.050

            for cu in range(n_can_u + 1):
                uf = cu / n_can_u
                # Span outward
                x_c = side * (0.840 * (1 - uf) + 0.940 * uf)
                for cv in range(n_can_v + 1):
                    vf = cv / n_can_v
                    y_c = y_c_base + 0.120 * vf
                    z_c = z_c_base + 0.040 * uf + 0.020 * (vf ** 2)
                    all_verts.append([round(float(x_c), 4), round(float(y_c), 4), round(float(z_c), 4)])

            for cu in range(n_can_u):
                for cv in range(n_can_v):
                    v0 = c_layer_base + cu * (n_can_v + 1) + cv
                    v1 = v0 + 1
                    v2 = c_layer_base + (cu + 1) * (n_can_v + 1) + (cv + 1)
                    v3 = c_layer_base + (cu + 1) * (n_can_v + 1) + cv
                    if side < 0:
                        all_faces.append([v0, v1, v2, v3])
                    else:
                        all_faces.append([v0, v3, v2, v1])

    # 4. Central Grille Recess Pocket
    grille_base = len(all_verts)
    n_g_y = 6
    n_g_x = 16
    for gi in range(n_g_y + 1):
        gf = gi / n_g_y
        zg = 0.200 * (1 - gf) + 0.480 * gf
        for gj in range(n_g_x + 1):
            gxf = gj / n_g_x
            xg = -0.460 * (1 - gxf) + 0.460 * gxf
            # Recessed inward
            yg = 2.140 - 0.080 * math.cos(gxf * math.pi - math.pi / 2.0)
            all_verts.append([round(float(xg), 4), round(float(yg), 4), round(float(zg), 4)])

    for gi in range(n_g_y):
        for gj in range(n_g_x):
            v0 = grille_base + gi * (n_g_x + 1) + gj
            v1 = v0 + 1
            v2 = grille_base + (gi + 1) * (n_g_x + 1) + (gj + 1)
            v3 = grille_base + (gi + 1) * (n_g_x + 1) + gj
            all_faces.append([v0, v1, v2, v3])

    return all_verts, all_faces


def build_front_bumper_splitter(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Front_Bumper_Splitter inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_front_bumper_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Front_Bumper_Splitter_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Front_Bumper_Splitter", mesh)

    if "MAT_GTR_Paint_Gunmetal" in materials:
        obj.data.materials.append(materials["MAT_GTR_Paint_Gunmetal"])
    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])
    if "MAT_GTR_Crimson_Accent" in materials:
        obj.data.materials.append(materials["MAT_GTR_Crimson_Accent"])

    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.005
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("02_Aero_Fascia", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 6. Component Assembly Generators: Hood (Phase 3)
# ==============================================================================

def generate_hood_mesh_data(
    ny_h: int = 36,
    nx_h: int = 36
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Hood."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    h_base = len(all_verts)
    for i in range(ny_h + 1):
        yf = i / ny_h
        y = 0.880 * (1 - yf) + 2.150 * yf
        z_base = 0.750 * (1 - yf) + 0.630 * yf
        w = 0.700 * (1 - yf) + 0.580 * yf

        for j in range(nx_h + 1):
            xf = j / nx_h
            x = -w * (1 - xf) + w * xf

            # Crown camber across hood
            camber = 0.020 * (1.0 - (x / w) ** 2)

            # Dual power bulges at |x| around 0.28m
            dist_bulge = abs(abs(x) - 0.280)
            bulge = 0.012 * max(0.0, 1.0 - (dist_bulge / 0.120) ** 2) if y <= 1.80 else 0.0

            # Recessed heat extractor vents between y=1.20 and y=1.65
            if 1.20 <= y <= 1.65 and 0.16 <= abs(x) <= 0.40:
                y_vent_f = math.sin((y - 1.20) / 0.45 * math.pi)
                x_vent_f = math.sin((abs(x) - 0.16) / 0.24 * math.pi)
                recess = -0.035 * y_vent_f * x_vent_f
            else:
                recess = 0.0

            z = z_base + camber + bulge + recess
            all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

    for i in range(ny_h):
        for j in range(nx_h):
            v0 = h_base + i * (nx_h + 1) + j
            v1 = v0 + 1
            v2 = h_base + (i + 1) * (nx_h + 1) + (j + 1)
            v3 = h_base + (i + 1) * (nx_h + 1) + j
            all_faces.append([v0, v1, v2, v3])

    # Downward shutline perimeter return flange
    flange_base = len(all_verts)
    for i in range(ny_h + 1):
        for side in (0, nx_h):
            v_idx = h_base + i * (nx_h + 1) + side
            orig_v = all_verts[v_idx]
            all_verts.append([orig_v[0], orig_v[1], round(orig_v[2] - 0.025, 4)])

    for i in range(ny_h):
        # Left edge flange
        v_top0 = h_base + i * (nx_h + 1)
        v_top1 = h_base + (i + 1) * (nx_h + 1)
        v_bot0 = flange_base + i * 2
        v_bot1 = flange_base + (i + 1) * 2
        all_faces.append([v_top0, v_bot0, v_bot1, v_top1])

        # Right edge flange
        v_top0_r = h_base + i * (nx_h + 1) + nx_h
        v_top1_r = h_base + (i + 1) * (nx_h + 1) + nx_h
        v_bot0_r = flange_base + i * 2 + 1
        v_bot1_r = flange_base + (i + 1) * 2 + 1
        all_faces.append([v_top0_r, v_top1_r, v_bot1_r, v_bot0_r])

    # Louver extraction slats
    for side in (-1, 1):
        for lv in range(3):
            lv_base = len(all_verts)
            y_lv = 1.300 + lv * 0.100
            for ku in (0, 1):
                x_lv = side * (0.200 if ku == 0 else 0.360)
                for kv in (0, 1):
                    z_lv = 0.680 + (0.012 if kv == 1 else 0.0)
                    all_verts.append([round(float(x_lv), 4), round(float(y_lv + kv * 0.035), 4), round(float(z_lv), 4)])
            if side < 0:
                all_faces.append([lv_base, lv_base + 1, lv_base + 3, lv_base + 2])
            else:
                all_faces.append([lv_base, lv_base + 2, lv_base + 3, lv_base + 1])

    return all_verts, all_faces


def build_hood(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Hood inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_hood_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Hood_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Hood", mesh)

    if "MAT_GTR_Paint_Gunmetal" in materials:
        obj.data.materials.append(materials["MAT_GTR_Paint_Gunmetal"])
    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])

    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.005
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("01_Body_Structure", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 7. Component Assembly Generators: Side Skirts (Phase 3)
# ==============================================================================

def generate_side_skirts_mesh_data(
    ny_sk: int = 32,
    n_prof: int = 16
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Side_Skirts."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    for side in (-1, 1):
        sk_base = len(all_verts)
        for i in range(ny_sk + 1):
            yf = i / ny_sk
            y = 0.950 * (1 - yf) + (-0.950) * yf

            # Winglet flick ahead of rear wheel arch
            if y <= -0.700:
                flick_factor = math.sin((y - (-0.700)) / (-0.250) * (math.pi / 2.0))
                z_flick = 0.100 * (flick_factor ** 2)
            else:
                z_flick = 0.0

            x_inner = side * 0.840
            x_outer = side * (0.940 + (0.015 if z_flick > 0 else 0.0))
            z_inner = 0.120
            z_outer_bot = 0.060
            z_outer_top = 0.080 + z_flick

            for j in range(n_prof + 1):
                pf = j / n_prof
                if pf <= 0.333:
                    u = pf / 0.333
                    x = x_inner * (1 - u) + x_outer * u
                    z = z_inner * (1 - u) + z_outer_top * u
                elif pf <= 0.666:
                    u = (pf - 0.333) / 0.333
                    x = x_outer
                    z = z_outer_top * (1 - u) + z_outer_bot * u
                else:
                    u = (pf - 0.666) / 0.334
                    x = x_outer * (1 - u) + x_inner * u
                    z = z_outer_bot * (1 - u) + 0.100 * u
                all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

        for i in range(ny_sk):
            for j in range(n_prof):
                v0 = sk_base + i * (n_prof + 1) + j
                v1 = v0 + 1
                v2 = sk_base + (i + 1) * (n_prof + 1) + (j + 1)
                v3 = sk_base + (i + 1) * (n_prof + 1) + j
                if side < 0:
                    all_faces.append([v0, v1, v2, v3])
                else:
                    all_faces.append([v0, v3, v2, v1])

    return all_verts, all_faces


def build_side_skirts(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Side_Skirts inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_side_skirts_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Side_Skirts_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Side_Skirts", mesh)

    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])
    if "MAT_GTR_Crimson_Accent" in materials:
        obj.data.materials.append(materials["MAT_GTR_Crimson_Accent"])

    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.005
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("02_Aero_Fascia", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 8. Component Assembly Generators: Rear Diffuser & Exhaust (Phase 3)
# ==============================================================================

def generate_rear_diffuser_mesh_data(
    ny_d: int = 30,
    nx_d: int = 32,
    n_tun_y: int = 22,
    n_tun_x: int = 28
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Rear_Diffuser_Exhaust."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    # 1. Rear Bumper Valence (y from -2.00 to -2.28)
    v_base = len(all_verts)
    for i in range(ny_d + 1):
        yf = i / ny_d
        y_val = -2.000 * (1 - yf) + (-2.270) * yf
        z_bot = 0.260 * (1 - yf) + 0.300 * yf
        z_top = 0.650

        for j in range(nx_d + 1):
            xf = j / nx_d
            x = -0.900 * (1 - xf) + 0.900 * xf
            y_curve = 0.040 * (1.0 - (x / 0.900) ** 2)
            y = y_val - y_curve
            z = z_bot * (1 - yf) + z_top * yf
            all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

    for i in range(ny_d):
        for j in range(nx_d):
            v0 = v_base + i * (nx_d + 1) + j
            v1 = v0 + 1
            v2 = v_base + (i + 1) * (nx_d + 1) + (j + 1)
            v3 = v_base + (i + 1) * (nx_d + 1) + j
            all_faces.append([v0, v3, v2, v1])

    # 2. Diffuser Venturi Floor (upswept from z=0.08 to z=0.26, y from -1.80 to -2.28)
    tun_base = len(all_verts)
    for i in range(n_tun_y + 1):
        yf = i / n_tun_y
        y = -1.800 * (1 - yf) + (-2.280) * yf
        z = 0.080 + 0.180 * (yf ** 1.6)

        for j in range(n_tun_x + 1):
            xf = j / n_tun_x
            x = -0.740 * (1 - xf) + 0.740 * xf
            all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

    for i in range(n_tun_y):
        for j in range(n_tun_x):
            v0 = tun_base + i * (n_tun_x + 1) + j
            v1 = v0 + 1
            v2 = tun_base + (i + 1) * (n_tun_x + 1) + (j + 1)
            v3 = tun_base + (i + 1) * (n_tun_x + 1) + j
            all_faces.append([v0, v1, v2, v3])

    # 3. 6 Vertical Aerodynamic Strakes
    strake_xs = [-0.600, -0.360, -0.120, 0.120, 0.360, 0.600]
    n_st_y = 12
    for sx in strake_xs:
        st_base = len(all_verts)
        for i in range(n_st_y + 1):
            yf = i / n_st_y
            y = -1.850 * (1 - yf) + (-2.285) * yf
            z_top = 0.080 + 0.180 * (yf ** 1.6)
            z_bot = 0.080
            for layer in (0, 1):
                x = sx + (-0.004 if layer == 0 else 0.004)
                for kv in (0, 1):
                    z = z_bot if kv == 0 else z_top
                    all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

        for i in range(n_st_y):
            # Left face
            v0 = st_base + i * 4
            v1 = v0 + 1
            v2 = st_base + (i + 1) * 4 + 1
            v3 = st_base + (i + 1) * 4
            all_faces.append([v0, v1, v2, v3])
            # Right face
            v0_r = st_base + i * 4 + 2
            v1_r = v0_r + 1
            v2_r = st_base + (i + 1) * 4 + 3
            v3_r = st_base + (i + 1) * 4 + 2
            all_faces.append([v0_r, v3_r, v2_r, v1_r])

    # 4. Quad Titanium Exhaust Tips (cylinders)
    tip_configs = [-0.550, -0.420, 0.420, 0.550]
    n_seg = 24
    for tx in tip_configs:
        ex_base = len(all_verts)
        tz = 0.320
        r_tip = 0.048
        for yi, y_ex in enumerate([-2.140, -2.210, -2.280]):
            for s in range(n_seg):
                ang = s * 2.0 * math.pi / n_seg
                x = tx + math.cos(ang) * r_tip
                z = tz + math.sin(ang) * r_tip
                all_verts.append([round(float(x), 4), round(float(y_ex), 4), round(float(z), 4)])

        for ring in (0, 1):
            r_offset = ex_base + ring * n_seg
            for s in range(n_seg):
                s_next = (s + 1) % n_seg
                v0 = r_offset + s
                v1 = r_offset + s_next
                v2 = r_offset + n_seg + s_next
                v3 = r_offset + n_seg + s
                all_faces.append([v0, v1, v2, v3])

    # 5. Central F1 Rain Light & Red Perimeter Trim
    f1_base = len(all_verts)
    n_f1 = 8
    for fi in range(n_f1 + 1):
        for fj in range(n_f1 + 1):
            xf = -0.060 + (fi / n_f1) * 0.120
            zf = 0.220 + (fj / n_f1) * 0.080
            all_verts.append([round(float(xf), 4), -2.275, round(float(zf), 4)])

    for fi in range(n_f1):
        for fj in range(n_f1):
            v0 = f1_base + fi * (n_f1 + 1) + fj
            v1 = v0 + 1
            v2 = f1_base + (fi + 1) * (n_f1 + 1) + (fj + 1)
            v3 = f1_base + (fi + 1) * (n_f1 + 1) + fj
            all_faces.append([v0, v3, v2, v1])

    # Red trim edge strip along lower diffuser edge
    trim_base = len(all_verts)
    n_tr = 32
    for ti in range(n_tr + 1):
        xt = -0.800 + (ti / n_tr) * 1.600
        all_verts.append([round(float(xt), 4), -2.285, 0.080])
        all_verts.append([round(float(xt), 4), -2.285, 0.095])

    for ti in range(n_tr):
        v0 = trim_base + ti * 2
        v1 = v0 + 1
        v2 = trim_base + (ti + 1) * 2 + 1
        v3 = trim_base + (ti + 1) * 2
        all_faces.append([v0, v1, v2, v3])

    return all_verts, all_faces


def build_rear_diffuser_exhaust(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Rear_Diffuser_Exhaust inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_rear_diffuser_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Rear_Diffuser_Exhaust_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Rear_Diffuser_Exhaust", mesh)

    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])
    if "MAT_GTR_Crimson_Accent" in materials:
        obj.data.materials.append(materials["MAT_GTR_Crimson_Accent"])
    if "MAT_GTR_Brake_Steel" in materials:
        obj.data.materials.append(materials["MAT_GTR_Brake_Steel"])
    if "MAT_GTR_Tail_Emissive" in materials:
        obj.data.materials.append(materials["MAT_GTR_Tail_Emissive"])

    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.005
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("02_Aero_Fascia", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 9. Component Assembly Generators: Rear Wing (Phase 3)
# ==============================================================================

def generate_rear_wing_mesh_data(
    nx_w: int = 36,
    nc_w: int = 16
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Rear_Wing."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    # 1. Cambered Airfoil Blade
    blade_base = len(all_verts)
    n_pts_chord = nc_w + 1
    for layer in (0, 1):  # 0: bottom, 1: top
        for i in range(nx_w + 1):
            xf = i / nx_w
            x = -0.825 * (1 - xf) + 0.825 * xf
            droop = 0.015 * ((x / 0.825) ** 2)

            for j in range(nc_w + 1):
                cf = j / nc_w
                y = -1.940 * (1 - cf) + (-2.260) * cf
                camber = 0.025 * math.sin(cf * math.pi)
                thickness = 0.020 * math.sin(cf * math.pi)
                if layer == 1:
                    z = 1.035 + camber + thickness * 0.5 - droop
                else:
                    z = 1.035 + camber - thickness * 0.5 - droop
                all_verts.append([round(float(x), 4), round(float(y), 4), round(float(z), 4)])

    n_blade_layer = (nx_w + 1) * (nc_w + 1)
    for layer in (0, 1):
        l_base = blade_base + layer * n_blade_layer
        for i in range(nx_w):
            for j in range(nc_w):
                v0 = l_base + i * n_pts_chord + j
                v1 = v0 + 1
                v2 = l_base + (i + 1) * n_pts_chord + (j + 1)
                v3 = l_base + (i + 1) * n_pts_chord + j
                if layer == 0:
                    all_faces.append([v0, v3, v2, v1])
                else:
                    all_faces.append([v0, v1, v2, v3])

    # Leading and trailing edge perimeter
    for i in range(nx_w):
        bl_0 = blade_base + i * n_pts_chord
        bl_1 = blade_base + (i + 1) * n_pts_chord
        tl_0 = bl_0 + n_blade_layer
        tl_1 = bl_1 + n_blade_layer
        all_faces.append([bl_0, bl_1, tl_1, tl_0])

        bt_0 = blade_base + i * n_pts_chord + nc_w
        bt_1 = blade_base + (i + 1) * n_pts_chord + nc_w
        tt_0 = bt_0 + n_blade_layer
        tt_1 = bt_1 + n_blade_layer
        all_faces.append([bt_0, tt_0, tt_1, bt_1])

    # 2. Dual Swan-Neck Pylons
    n_py_s = 12
    for sx in (-0.450, 0.450):
        py_base = len(all_verts)
        for i in range(n_py_s + 1):
            pf = i / n_py_s
            y_py = -1.860 * (1 - pf) + (-2.020) * pf
            z_py = 0.850 * (1 - pf) + 1.090 * pf
            for side_w in (-0.010, 0.010):
                x_p = sx + side_w
                for chord_p in (-0.025, 0.025):
                    all_verts.append([round(float(x_p), 4), round(float(y_py + chord_p), 4), round(float(z_py), 4)])

        for i in range(n_py_s):
            v0 = py_base + i * 4
            v1 = v0 + 1
            v2 = py_base + (i + 1) * 4 + 1
            v3 = py_base + (i + 1) * 4
            all_faces.append([v0, v1, v2, v3])

            v0_r = py_base + i * 4 + 2
            v1_r = v0_r + 1
            v2_r = py_base + (i + 1) * 4 + 3
            v3_r = py_base + (i + 1) * 4 + 2
            all_faces.append([v0_r, v3_r, v2_r, v1_r])

    # 3. Vertical Endplates (Crimson Red)
    n_ep_y = 10
    n_ep_z = 8
    for ep_x in (-0.835, 0.835):
        ep_base = len(all_verts)
        for i in range(n_ep_y + 1):
            yf = i / n_ep_y
            y = -1.900 * (1 - yf) + (-2.280) * yf
            for j in range(n_ep_z + 1):
                zf = j / n_ep_z
                z = 0.960 * (1 - zf) + 1.140 * zf
                all_verts.append([round(float(ep_x), 4), round(float(y), 4), round(float(z), 4)])

        for i in range(n_ep_y):
            for j in range(n_ep_z):
                v0 = ep_base + i * (n_ep_z + 1) + j
                v1 = v0 + 1
                v2 = ep_base + (i + 1) * (n_ep_z + 1) + (j + 1)
                v3 = ep_base + (i + 1) * (n_ep_z + 1) + j
                if ep_x < 0:
                    all_faces.append([v0, v1, v2, v3])
                else:
                    all_faces.append([v0, v3, v2, v1])

    return all_verts, all_faces


def build_rear_wing(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Rear_Wing inside Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_rear_wing_mesh_data()
    mesh = bpy.data.meshes.new("GTR_Rear_Wing_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("GTR_Rear_Wing", mesh)

    if "MAT_GTR_Carbon_Satin" in materials:
        obj.data.materials.append(materials["MAT_GTR_Carbon_Satin"])
    if "MAT_GTR_Crimson_Accent" in materials:
        obj.data.materials.append(materials["MAT_GTR_Crimson_Accent"])

    bev = obj.modifiers.new("Auto_Bevel", 'BEVEL')
    bev.width = 0.004
    bev.segments = 2
    bev.profile = 0.5
    bev.harden_normals = True

    wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True

    col = collections.get("02_Aero_Fascia", bpy.context.scene.collection)
    col.objects.link(obj)

    return obj


# ==============================================================================
# 10. Component Assembly Generators: Wheels & Instancing (Phase 4)
# ==============================================================================

def generate_master_wheel_mesh_data(
    n_th: int = 48,
    n_prof: int = 20,
    n_barrel: int = 8
) -> Tuple[List[List[float]], List[List[int]]]:
    """Generate vertex coordinates and quad faces for GTR_Wheel_Master."""
    all_verts: List[List[float]] = []
    all_faces: List[List[int]] = []

    # 1. Performance Radial Tire (R_bead=0.260 to R_tread=0.340, width=0.280)
    tire_base = len(all_verts)
    prof_x: List[float] = []
    prof_r: List[float] = []
    for k in range(n_prof + 1):
        kf = k / n_prof
        if kf <= 0.25:
            u = kf / 0.25
            x = -0.110 * (1 - u) + (-0.140) * u
            r = 0.260 * (1 - u) + 0.320 * u
        elif kf <= 0.75:
            u = (kf - 0.25) / 0.50
            x = -0.140 * (1 - u) + 0.140 * u
            r = 0.340 - 0.004 * ((2.0 * u - 1.0) ** 2)
        else:
            u = (kf - 0.75) / 0.25
            x = 0.140 * (1 - u) + 0.110 * u
            r = 0.320 * (1 - u) + 0.260 * u
        prof_x.append(x)
        prof_r.append(r)

    for i in range(n_th):
        ang = i * 2.0 * math.pi / n_th
        sin_a = math.sin(ang)
        cos_a = math.cos(ang)
        for k in range(n_prof + 1):
            all_verts.append([
                round(float(prof_x[k]), 4),
                round(float(cos_a * prof_r[k]), 4),
                round(float(sin_a * prof_r[k]), 4)
            ])

    for i in range(n_th):
        i_next = (i + 1) % n_th
        for k in range(n_prof):
            v0 = tire_base + i * (n_prof + 1) + k
            v1 = v0 + 1
            v2 = tire_base + i_next * (n_prof + 1) + (k + 1)
            v3 = tire_base + i_next * (n_prof + 1) + k
            all_faces.append([v0, v1, v2, v3])

    # 2. Forged Alloy Rim Barrel (R=0.260)
    rim_base = len(all_verts)
    for i in range(n_th):
        ang = i * 2.0 * math.pi / n_th
        sin_a = math.sin(ang)
        cos_a = math.cos(ang)
        for b in range(n_barrel + 1):
            bf = b / n_barrel
            x = -0.110 * (1 - bf) + 0.110 * bf
            r = 0.260 - 0.015 * math.sin(bf * math.pi)
            all_verts.append([round(float(x), 4), round(float(cos_a * r), 4), round(float(sin_a * r), 4)])

    for i in range(n_th):
        i_next = (i + 1) % n_th
        for b in range(n_barrel):
            v0 = rim_base + i * (n_barrel + 1) + b
            v1 = v0 + 1
            v2 = rim_base + i_next * (n_barrel + 1) + (b + 1)
            v3 = rim_base + i_next * (n_barrel + 1) + b
            all_faces.append([v0, v1, v2, v3])

    # 3. 10 Spoke Assembly (Split-Spoke GT Racing Design)
    spoke_base = len(all_verts)
    n_spokes = 10
    n_sub_sp = 2
    n_sp_len = 8
    for sp in range(n_spokes):
        base_ang = sp * 2.0 * math.pi / n_spokes
        for sub in range(n_sub_sp):
            sub_ang = base_ang + (-0.035 if sub == 0 else 0.035)
            s_offset = len(all_verts)
            for step in range(n_sp_len + 1):
                sf = step / n_sp_len
                r = 0.060 * (1 - sf) + 0.245 * sf
                x = 0.040 * (1 - sf) + 0.095 * sf
                for w in (-0.009, 0.009):
                    tang = sub_ang + w / max(0.05, r)
                    for layer in (-0.006, 0.006):
                        all_verts.append([
                            round(float(x + layer), 4),
                            round(float(math.cos(tang) * r), 4),
                            round(float(math.sin(tang) * r), 4)
                        ])

            for step in range(n_sp_len):
                v0 = s_offset + step * 4
                v1 = v0 + 1
                v2 = v0 + 3
                v3 = v0 + 2
                vn0 = s_offset + (step + 1) * 4
                vn1 = vn0 + 1
                vn2 = vn0 + 3
                vn3 = vn0 + 2
                all_faces.append([v0, v1, vn1, vn0])
                all_faces.append([v3, vn2, vn3, v2])
                all_faces.append([v0, vn0, vn2, v3])
                all_faces.append([v1, v2, vn3, vn1])

    # 4. Ventilated Carbon-Ceramic Brake Rotor
    rotor_base = len(all_verts)
    n_rot_th = 48
    for i in range(n_rot_th):
        ang = i * 2.0 * math.pi / n_rot_th
        sin_a = math.sin(ang)
        cos_a = math.cos(ang)
        for r_val in (0.070, 0.195):
            for x_val in (0.010, 0.026):
                all_verts.append([round(float(x_val), 4), round(float(cos_a * r_val), 4), round(float(sin_a * r_val), 4)])

    for i in range(n_rot_th):
        i_next = (i + 1) % n_rot_th
        v0 = rotor_base + i * 4 + 1
        v1 = rotor_base + i_next * 4 + 1
        v2 = rotor_base + i_next * 4 + 3
        v3 = rotor_base + i * 4 + 3
        all_faces.append([v0, v1, v2, v3])

        v0_b = rotor_base + i * 4
        v1_b = rotor_base + i * 4 + 2
        v2_b = rotor_base + i_next * 4 + 2
        v3_b = rotor_base + i_next * 4
        all_faces.append([v0_b, v1_b, v2_b, v3_b])
        all_faces.append([v3, v2, v2_b, v1_b])

    # 5. 6-Piston Caliper (Brembo Red)
    cal_base = len(all_verts)
    n_cal_u = 10
    n_cal_v = 10
    for cu in range(n_cal_u + 1):
        cuf = cu / n_cal_u
        ang = 0.18 * math.pi + cuf * 0.28 * math.pi
        sin_a = math.sin(ang)
        cos_a = math.cos(ang)
        for cv in range(n_cal_v + 1):
            cvf = cv / n_cal_v
            r = 0.155 * (1 - cvf) + 0.215 * cvf
            x = 0.035 + 0.038 * (cvf ** 0.5)
            all_verts.append([round(float(x), 4), round(float(cos_a * r), 4), round(float(sin_a * r), 4)])

    for cu in range(n_cal_u):
        for cv in range(n_cal_v):
            v0 = cal_base + cu * (n_cal_v + 1) + cv
            v1 = v0 + 1
            v2 = cal_base + (cu + 1) * (n_cal_v + 1) + (cv + 1)
            v3 = cal_base + (cu + 1) * (n_cal_v + 1) + cv
            all_faces.append([v0, v1, v2, v3])

    return all_verts, all_faces


def build_master_wheel(materials: Dict[str, Any], collections: Dict[str, Any]) -> Any:
    """Construct GTR_Wheel_Master and instance 4 wheels (FL, FR, RL, RR) in Blender C RAM."""
    if not HAS_BPY:
        return None

    verts, faces = generate_master_wheel_mesh_data()
    master_mesh = bpy.data.meshes.new("GTR_Wheel_Master_Mesh")
    bm = bmesh.new()

    bm_verts = [bm.verts.new(v) for v in verts]
    bm.verts.ensure_lookup_table()

    for f_indices in faces:
        try:
            bm.faces.new([bm_verts[idx] for idx in f_indices])
        except ValueError:
            pass

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(master_mesh)
    bm.free()

    # Materials for wheel mesh
    if "MAT_GTR_Tire_Rubber" in materials:
        master_mesh.materials.append(materials["MAT_GTR_Tire_Rubber"])
    if "MAT_GTR_Carbon_Satin" in materials:
        master_mesh.materials.append(materials["MAT_GTR_Carbon_Satin"])
    if "MAT_GTR_Brake_Steel" in materials:
        master_mesh.materials.append(materials["MAT_GTR_Brake_Steel"])
    if "MAT_GTR_Caliper_Red" in materials:
        master_mesh.materials.append(materials["MAT_GTR_Caliper_Red"])

    col = collections.get("05_Wheels", bpy.context.scene.collection)

    wheel_configs = [
        ("GTR_Wheel_FL", (-0.880, 1.350, 0.340), 0.0),
        ("GTR_Wheel_FR", (0.880, 1.350, 0.340), math.pi),
        ("GTR_Wheel_RL", (-0.890, -1.350, 0.340), 0.0),
        ("GTR_Wheel_RR", (0.890, -1.350, 0.340), math.pi),
    ]

    instanced_objects = []
    for name, pos, rot_z in wheel_configs:
        obj = bpy.data.objects.get(name)
        if obj is None:
            obj = bpy.data.objects.new(name, master_mesh)
            col.objects.link(obj)
        else:
            obj.data = master_mesh

        obj.location = pos
        obj.rotation_euler = (0.0, 0.0, rot_z)

        # Modifiers per instanced object
        if "Auto_WeightedNormal" not in obj.modifiers:
            wn = obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
            wn.keep_sharp = True

        instanced_objects.append(obj)

    return instanced_objects
