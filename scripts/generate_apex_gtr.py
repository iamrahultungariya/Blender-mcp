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
