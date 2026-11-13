"""Multi-material PBR Palette Library for Contemporary Warm Luxury Bedroom Suite.

Enforces 90/10 Hybrid Pipeline: materials are defined once and mapped by integer slot index,
allowing single-buffer BMesh geometry to tag `face.material_index` without UI context.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    import bpy
    HAS_BPY = True
except ImportError:
    bpy = None
    HAS_BPY = False


class MaterialLibrary:
    """Manages 10 reference PBR materials and maps them deterministically to integer indices."""

    DEFINITIONS: Dict[str, Dict[str, Any]] = {
        "TRAVERTINE_TILES": {
            "base_color": (0.78, 0.74, 0.68, 1.0),
            "roughness": 0.28,
            "metallic": 0.0,
            "specular_ior_level": 0.55,
        },
        "WALNUT_WOOD": {
            "base_color": (0.18, 0.11, 0.07, 1.0),
            "roughness": 0.35,
            "metallic": 0.0,
            "specular_ior_level": 0.5,
        },
        "TAUPE_BOUCLE": {
            "base_color": (0.58, 0.54, 0.48, 1.0),
            "roughness": 0.85,
            "metallic": 0.0,
            "sheen_weight": 0.9,
            "sheen_tint": (0.9, 0.86, 0.82, 1.0),
        },
        "LINEN_WHITE": {
            "base_color": (0.94, 0.93, 0.91, 1.0),
            "roughness": 0.82,
            "metallic": 0.0,
            "subsurface_weight": 0.04,
        },
        "CHARCOAL_PLEAT": {
            "base_color": (0.24, 0.23, 0.22, 1.0),
            "roughness": 0.75,
            "metallic": 0.0,
            "sheen_weight": 0.5,
        },
        "BRUSHED_BRASS": {
            "base_color": (0.92, 0.78, 0.45, 1.0),
            "roughness": 0.25,
            "metallic": 1.0,
            "specular_ior_level": 0.7,
        },
        "MATTE_BLACK_METAL": {
            "base_color": (0.05, 0.05, 0.05, 1.0),
            "roughness": 0.40,
            "metallic": 0.85,
            "specular_ior_level": 0.5,
        },
        "TINTED_BRONZE_GLASS": {
            "base_color": (0.42, 0.34, 0.26, 1.0),
            "roughness": 0.05,
            "metallic": 0.0,
            "transmission_weight": 0.85,
            "ior": 1.52,
        },
        "SHEER_WHITE": {
            "base_color": (0.95, 0.95, 0.95, 0.6),
            "roughness": 0.70,
            "metallic": 0.0,
            "transmission_weight": 0.50,
        },
        "LED_WARM_2700K": {
            "base_color": (1.0, 0.92, 0.75, 1.0),
            "emission_color": (1.0, 0.86, 0.65, 1.0),
            "emission_strength": 16.0,
            "roughness": 0.1,
            "metallic": 0.0,
        },
    }

    def __init__(self) -> None:
        self._name_to_index: Dict[str, int] = {
            name: idx for idx, name in enumerate(self.DEFINITIONS.keys())
        }
        self._index_to_name: Dict[int, str] = {
            idx: name for idx, name in enumerate(self.DEFINITIONS.keys())
        }

    def get_material_names(self) -> List[str]:
        """Return ordered list of material keys."""
        return list(self.DEFINITIONS.keys())

    def get_index(self, name: str) -> int:
        """Get integer slot index for a material name."""
        if name not in self._name_to_index:
            raise KeyError(
                f"Material '{name}' not found in MaterialLibrary. Valid names: {list(self._name_to_index.keys())}"
            )
        return self._name_to_index[name]

    def get_definition(self, name: str) -> Dict[str, Any]:
        """Return raw physical shader parameters for material name."""
        return self.DEFINITIONS[name]

    def create_or_get_material(self, name: str) -> Any:
        """Create or reuse bpy.types.Material in Blender scene."""
        if not HAS_BPY or bpy is None or not hasattr(bpy, "data"):
            return {"name": name, **self.DEFINITIONS.get(name, {})}

        mat_name = f"M_RefSuite_{name}"
        if mat_name in bpy.data.materials:
            return bpy.data.materials[mat_name]

        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            props = self.DEFINITIONS.get(name, {})
            if "base_color" in props and "Base Color" in bsdf.inputs:
                bsdf.inputs["Base Color"].default_value = props["base_color"]
            if "roughness" in props and "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = props["roughness"]
            if "metallic" in props and "Metallic" in bsdf.inputs:
                bsdf.inputs["Metallic"].default_value = props["metallic"]
            if "emission_color" in props:
                if "Emission Color" in bsdf.inputs:
                    bsdf.inputs["Emission Color"].default_value = props["emission_color"]
                if "Emission Strength" in bsdf.inputs and "emission_strength" in props:
                    bsdf.inputs["Emission Strength"].default_value = props["emission_strength"]
            if "sheen_weight" in props:
                if "Sheen Weight" in bsdf.inputs:
                    bsdf.inputs["Sheen Weight"].default_value = props["sheen_weight"]
                elif "Sheen" in bsdf.inputs:
                    bsdf.inputs["Sheen"].default_value = props["sheen_weight"]
            if "transmission_weight" in props:
                if "Transmission Weight" in bsdf.inputs:
                    bsdf.inputs["Transmission Weight"].default_value = props["transmission_weight"]
                elif "Transmission" in bsdf.inputs:
                    bsdf.inputs["Transmission"].default_value = props["transmission_weight"]
            if "ior" in props and "IOR" in bsdf.inputs:
                bsdf.inputs["IOR"].default_value = props["ior"]

        return mat

    def assign_to_object(self, obj: Any) -> None:
        """Assign all materials in library order to an object so face.material_index matches get_index."""
        if not HAS_BPY or bpy is None or obj is None or not hasattr(obj, "data"):
            return

        obj.data.materials.clear()
        for name in self.get_material_names():
            mat = self.create_or_get_material(name)
            obj.data.materials.append(mat)
