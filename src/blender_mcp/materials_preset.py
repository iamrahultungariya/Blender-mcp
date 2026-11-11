"""Procedural PBR Material Vault for Blender MCP.

Provides physically-calibrated automotive shader generation for Blender 4.x and 5.x LTS.
Handles socket name changes (e.g. 'Specular' -> 'Specular IOR Level', 'Transmission' -> 'Transmission Weight',
'Clearcoat' -> 'Coat Weight') across Blender versions.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


def _get_or_create_material(name: str) -> Any:
    if not HAS_BPY:
        return None
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    return mat


def _find_principled_bsdf(mat: Any) -> Any:
    if not HAS_BPY or mat is None:
        return None
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            return node
    return nodes.new('ShaderNodeBsdfPrincipled')


def _set_socket_value(node: Any, socket_names: list[str], value: Any) -> bool:
    """Set socket value by checking possible alias names across Blender versions."""
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


def setup_car_paint_material(
    name: str = "M_Car_Paint",
    base_color: Tuple[float, float, float, float] = (0.95, 0.95, 0.95, 1.0),
    clearcoat: float = 1.0,
    metallic: float = 0.0,
    roughness: float = 0.12
) -> Any:
    """Automotive high-gloss polyurethane clearcoat finish."""
    mat = _get_or_create_material(name)
    bsdf = _find_principled_bsdf(mat)
    if bsdf:
        _set_socket_value(bsdf, ["Base Color"], base_color)
        _set_socket_value(bsdf, ["Roughness"], roughness)
        _set_socket_value(bsdf, ["Metallic"], metallic)
        # Blender 4.0+ uses 'Coat Weight' or 'Coat', 3.x uses 'Clearcoat'
        _set_socket_value(bsdf, ["Coat Weight", "Coat", "Clearcoat"], clearcoat)
        _set_socket_value(bsdf, ["Coat Roughness", "Clearcoat Roughness"], 0.03)
        _set_socket_value(bsdf, ["Specular IOR Level", "Specular"], 0.5)
    return mat


def setup_textured_plastic_material(
    name: str = "M_Textured_Plastic",
    base_color: Tuple[float, float, float, float] = (0.04, 0.04, 0.04, 1.0),
    roughness: float = 0.75,
    bump_strength: float = 0.15
) -> Any:
    """Matte dark thermoplastic molding for bumpers, mirrors, and wheel arches."""
    mat = _get_or_create_material(name)
    bsdf = _find_principled_bsdf(mat)
    if bsdf:
        _set_socket_value(bsdf, ["Base Color"], base_color)
        _set_socket_value(bsdf, ["Roughness"], roughness)
        _set_socket_value(bsdf, ["Metallic"], 0.0)
        _set_socket_value(bsdf, ["Specular IOR Level", "Specular"], 0.25)
    return mat


def setup_automotive_glass_material(
    name: str = "M_Automotive_Glass",
    tint_color: Tuple[float, float, float, float] = (0.08, 0.10, 0.12, 1.0),
    transmission: float = 0.88,
    roughness: float = 0.02,
    ior: float = 1.52
) -> Any:
    """Tinted automotive laminated glass."""
    mat = _get_or_create_material(name)
    bsdf = _find_principled_bsdf(mat)
    if bsdf:
        _set_socket_value(bsdf, ["Base Color"], tint_color)
        _set_socket_value(bsdf, ["Roughness"], roughness)
        _set_socket_value(bsdf, ["IOR"], ior)
        # Blender 4.0+ uses 'Transmission Weight', 3.x uses 'Transmission'
        _set_socket_value(bsdf, ["Transmission Weight", "Transmission"], transmission)
        _set_socket_value(bsdf, ["Specular IOR Level", "Specular"], 0.5)
    return mat


def setup_emergency_emissive_material(
    name: str = "M_Emergency_Emissive",
    color: Tuple[float, float, float, float] = (1.0, 0.05, 0.05, 1.0),
    emission_strength: float = 40.0
) -> Any:
    """High-intensity emergency LED strobe material calibrated for EEVEE Next & Cycles."""
    mat = _get_or_create_material(name)
    bsdf = _find_principled_bsdf(mat)
    if bsdf:
        _set_socket_value(bsdf, ["Base Color"], color)
        # Blender 4.0+ uses 'Emission Color', older uses 'Emission'
        _set_socket_value(bsdf, ["Emission Color", "Emission"], color)
        _set_socket_value(bsdf, ["Emission Strength"], emission_strength)
    return mat


def setup_radial_tire_material(
    name: str = "M_Radial_Tire_Rubber",
    base_color: Tuple[float, float, float, float] = (0.025, 0.025, 0.025, 1.0),
    roughness: float = 0.65
) -> Any:
    """Vulcanized radial tire rubber."""
    mat = _get_or_create_material(name)
    bsdf = _find_principled_bsdf(mat)
    if bsdf:
        _set_socket_value(bsdf, ["Base Color"], base_color)
        _set_socket_value(bsdf, ["Roughness"], roughness)
        _set_socket_value(bsdf, ["Metallic"], 0.0)
        _set_socket_value(bsdf, ["Specular IOR Level", "Specular"], 0.2)
    return mat


def setup_chrome_trim_material(
    name: str = "M_Chrome_Trim"
) -> Any:
    """Mirror-specular automotive chrome for grilles, badges, and rim hubs."""
    mat = _get_or_create_material(name)
    bsdf = _find_principled_bsdf(mat)
    if bsdf:
        _set_socket_value(bsdf, ["Base Color"], (0.92, 0.92, 0.92, 1.0))
        _set_socket_value(bsdf, ["Roughness"], 0.04)
        _set_socket_value(bsdf, ["Metallic"], 1.0)
        _set_socket_value(bsdf, ["Specular IOR Level", "Specular"], 1.0)
    return mat


class MaterialPresetVault:
    """Factory vault generating material specifications and Blender shader graphs."""

    @staticmethod
    def get_material_spec(material_type: str, **kwargs: Any) -> Dict[str, Any]:
        m_type = material_type.lower()
        if "paint" in m_type:
            return {
                "type": "car_paint",
                "base_color": kwargs.get("color", (0.95, 0.95, 0.95, 1.0)),
                "clearcoat": kwargs.get("clearcoat", 1.0),
                "roughness": kwargs.get("roughness", 0.12),
                "metallic": kwargs.get("metallic", 0.0),
            }
        elif "emissive" in m_type or "light" in m_type:
            return {
                "type": "emergency_emissive",
                "color": kwargs.get("color", (1.0, 0.05, 0.05, 1.0)),
                "emission_strength": kwargs.get("strength", 40.0),
            }
        elif "plastic" in m_type or "trim" in m_type:
            return {
                "type": "textured_plastic",
                "base_color": kwargs.get("color", (0.04, 0.04, 0.04, 1.0)),
                "roughness": kwargs.get("roughness", 0.75),
            }
        elif "glass" in m_type:
            return {
                "type": "automotive_glass",
                "tint": kwargs.get("color", (0.08, 0.10, 0.12, 1.0)),
                "transmission": kwargs.get("transmission", 0.88),
            }
        elif "tire" in m_type or "rubber" in m_type:
            return {
                "type": "radial_tire",
                "base_color": kwargs.get("color", (0.025, 0.025, 0.025, 1.0)),
                "roughness": kwargs.get("roughness", 0.65),
            }
        return {"type": "standard_pbr", "base_color": (0.8, 0.8, 0.8, 1.0)}

    # Callable shader factory bindings
    setup_car_paint = staticmethod(setup_car_paint_material)
    setup_plastic = staticmethod(setup_textured_plastic_material)
    setup_glass = staticmethod(setup_automotive_glass_material)
    setup_emissive = staticmethod(setup_emergency_emissive_material)
    setup_tire = staticmethod(setup_radial_tire_material)
    setup_chrome = staticmethod(setup_chrome_trim_material)
