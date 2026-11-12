"""Apex GT-R Concept Procedural Vehicle Generator for Blender.

Procedurally generates the 12 modular component assemblies for the Apex GT-R Concept
supercar strictly following the reference blueprint dimensions, ~30,000 polygon budget,
and the in-memory 90/10 Hybrid Procedural Pipeline.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

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
