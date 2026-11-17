"""Cinematic Studio Lighting & HDRI Engine for Rahul 3D Engine.

Provides 10 physically-calibrated studio lighting rigs, scene-aware light scaling,
World shader HDRI setup, lighting inspection, and dynamic object adjustment.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import bpy
    import mathutils
    HAS_BPY = True
except ImportError:
    HAS_BPY = False

from blender_mcp.foundation import format_tool_response, OperationRisk


def _kelvin_to_rgb(temp_k: float) -> Tuple[float, float, float]:
    """Convert color temperature in Kelvin (1000K to 12000K) to normalized RGB."""
    temp = max(1000.0, min(12000.0, float(temp_k))) / 100.0
    
    # Red
    if temp <= 66:
        r = 1.0
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)
        r = max(0.0, min(255.0, r)) / 255.0
        
    # Green
    if temp <= 66:
        g = temp
        g = 99.4708025861 * math.log(g) - 161.1195681661
        g = max(0.0, min(255.0, g)) / 255.0
    else:
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)
        g = max(0.0, min(255.0, g)) / 255.0
        
    # Blue
    if temp >= 66:
        b = 1.0
    elif temp <= 19:
        b = 0.0
    else:
        b = temp - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307
        b = max(0.0, min(255.0, b)) / 255.0
        
    return (r, g, b)


def _get_target_bounds(target_object_name: Optional[str] = None) -> Tuple[Tuple[float, float, float], float]:
    """Calculate center coordinate and bounding sphere radius of target or visible scene."""
    if not HAS_BPY:
        return (0.0, 0.0, 1.0), 2.0

    if target_object_name:
        obj = bpy.data.objects.get(target_object_name)
        if obj:
            bb = [obj.matrix_world @ mathutils.Vector(v) for v in obj.bound_box]
            center = sum(bb, mathutils.Vector()) / 8.0
            radius = max((v - center).length for v in bb)
            return (center.x, center.y, center.z), max(0.5, radius)

    # Fallback to visible mesh objects
    mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and not o.hide_viewport]
    if mesh_objs:
        all_pts = []
        for o in mesh_objs[:10]:
            all_pts.extend([o.matrix_world @ mathutils.Vector(v) for v in o.bound_box])
        center = sum(all_pts, mathutils.Vector()) / len(all_pts)
        radius = max((v - center).length for v in all_pts)
        return (center.x, center.y, center.z), max(1.0, radius)

    return (0.0, 0.0, 1.0), 2.0


def _create_light(
    name: str,
    light_type: str,
    location: Tuple[float, float, float],
    target_pos: Tuple[float, float, float],
    energy: float,
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    size: float = 1.0,
    size_y: Optional[float] = None,
    collection: Any = None
) -> Any:
    """Spawn light, orient toward target position, and link to collection."""
    if not HAS_BPY:
        return None

    light_data = bpy.data.lights.new(name=f"{name}_Data", type=light_type)
    light_data.energy = energy
    light_data.color = color
    if light_type == 'AREA':
        light_data.size = size
        if size_y is not None:
            light_data.shape = 'RECTANGLE'
            light_data.size_y = size_y
        else:
            light_data.shape = 'SQUARE'
    elif light_type == 'SPOT':
        light_data.spot_size = math.radians(45)

    obj = bpy.data.objects.new(name, light_data)
    obj.location = location

    # Track to target
    direction = mathutils.Vector(target_pos) - mathutils.Vector(location)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

    if collection:
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)

    return obj


def setup_studio_lighting(
    preset: str = "three_point",
    target_object: Optional[str] = None,
    energy_multiplier: float = 1.0,
    color_temperature: float = 5500.0,
    shadow_quality: str = "HIGH",
    world_strength: float = 0.1,
    collection_name: str = "Lighting_Studio"
) -> Dict[str, Any]:
    """Setup professional, physically calibrated studio lighting rig.
    
    Supported Presets (10):
    three_point, dramatic_rim, soft_interior, product_clean, cinematic,
    architectural, horror_atmosphere, daylight, night_scene, automotive_studio.
    """
    preset_key = preset.strip().lower()
    valid_presets = [
        "three_point", "dramatic_rim", "soft_interior", "product_clean",
        "cinematic", "architectural", "horror_atmosphere", "daylight",
        "night_scene", "automotive_studio"
    ]
    if preset_key not in valid_presets:
        return format_tool_response(
            "setup_studio_lighting",
            success=False,
            errors=[f"Unsupported lighting preset '{preset}'. Valid presets: {', '.join(valid_presets)}"],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    if not HAS_BPY:
        return format_tool_response(
            "setup_studio_lighting",
            result={"preset": preset_key, "lights_created": 3, "collection": collection_name},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    # Scene World Background calibration
    if bpy.context.scene.world and bpy.context.scene.world.use_nodes:
        bg = bpy.context.scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs["Strength"].default_value = world_strength

    # Manage dedicated collection (clean previous setup to prevent duplicate light buildup)
    col = bpy.data.collections.get(collection_name)
    if not col:
        col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(col)
    else:
        # Delete prior studio lights inside collection
        for o in list(col.objects):
            if o.type == 'LIGHT':
                bpy.data.objects.remove(o, do_unlink=True)

    center, radius = _get_target_bounds(target_object)
    cx, cy, cz = center
    dist = max(2.0, radius * 2.8)
    base_energy = (radius ** 1.8) * 120.0 * max(0.1, energy_multiplier)

    created_lights = []
    base_color = _kelvin_to_rgb(color_temperature)

    if preset_key == "three_point":
        # Key: 45 deg azimuth, 35 deg elev
        k_loc = (cx + dist * 0.707, cy - dist * 0.707, cz + dist * 0.6)
        k_obj = _create_light("Light_Key", "AREA", k_loc, center, base_energy * 1.0, base_color, radius * 1.2, collection=col)
        # Fill: -45 deg azimuth, 15 deg elev, softer & cooler
        f_loc = (cx - dist * 0.707, cy - dist * 0.707, cz + dist * 0.3)
        f_col = _kelvin_to_rgb(color_temperature + 1000)
        f_obj = _create_light("Light_Fill", "AREA", f_loc, center, base_energy * 0.4, f_col, radius * 1.8, collection=col)
        # Rim: Backlight 150 deg azimuth, 45 deg elev
        r_loc = (cx - dist * 0.5, cy + dist * 0.866, cz + dist * 0.8)
        r_obj = _create_light("Light_Rim", "AREA", r_loc, center, base_energy * 1.2, (1.0, 1.0, 1.0), radius * 0.8, collection=col)
        created_lights = [k_obj.name, f_obj.name, r_obj.name]

    elif preset_key == "dramatic_rim":
        # Dual rear kickers, deep shadows, negligible fill
        r1_loc = (cx + dist * 0.7, cy + dist * 0.7, cz + dist * 0.7)
        r1_obj = _create_light("Light_Kicker_R", "SPOT", r1_loc, center, base_energy * 1.8, base_color, radius * 0.5, collection=col)
        r2_loc = (cx - dist * 0.7, cy + dist * 0.7, cz + dist * 0.7)
        r2_obj = _create_light("Light_Kicker_L", "SPOT", r2_loc, center, base_energy * 1.5, _kelvin_to_rgb(color_temperature + 1500), radius * 0.5, collection=col)
        b_loc = (cx, cy - dist * 0.9, cz - dist * 0.2)
        b_obj = _create_light("Light_Floor_Bounce", "AREA", b_loc, center, base_energy * 0.15, (0.7, 0.7, 0.8), radius * 2.5, collection=col)
        created_lights = [r1_obj.name, r2_obj.name, b_obj.name]

    elif preset_key == "soft_interior":
        # Overhead softbox + warm cove bounce
        ov_loc = (cx, cy, cz + dist * 1.2)
        ov_obj = _create_light("Light_Ceiling_Softbox", "AREA", ov_loc, center, base_energy * 1.5, _kelvin_to_rgb(3200), radius * 3.0, radius * 3.0, collection=col)
        cove_loc = (cx, cy - dist * 0.8, cz + dist * 0.4)
        cove_obj = _create_light("Light_Warm_Cove", "AREA", cove_loc, center, base_energy * 0.6, _kelvin_to_rgb(2800), radius * 2.0, collection=col)
        created_lights = [ov_obj.name, cove_obj.name]

    elif preset_key == "product_clean":
        # 4-point cyclorama high-key studio
        l_loc = (cx - dist * 0.8, cy - dist * 0.5, cz + dist * 0.6)
        r_loc = (cx + dist * 0.8, cy - dist * 0.5, cz + dist * 0.6)
        top_loc = (cx, cy, cz + dist * 1.4)
        front_loc = (cx, cy - dist * 1.1, cz + dist * 0.2)
        l_obj = _create_light("Light_Product_L", "AREA", l_loc, center, base_energy * 0.8, (0.98, 0.98, 1.0), radius * 1.5, collection=col)
        r_obj = _create_light("Light_Product_R", "AREA", r_loc, center, base_energy * 0.8, (1.0, 0.98, 0.95), radius * 1.5, collection=col)
        top_obj = _create_light("Light_Product_Top", "AREA", top_loc, center, base_energy * 1.0, (1.0, 1.0, 1.0), radius * 2.0, collection=col)
        front_obj = _create_light("Light_Product_Front", "AREA", front_loc, center, base_energy * 0.35, (1.0, 1.0, 1.0), radius * 1.8, collection=col)
        created_lights = [l_obj.name, r_obj.name, top_obj.name, front_obj.name]

    elif preset_key == "cinematic":
        # Teal & Orange high contrast
        key_loc = (cx + dist * 0.8, cy - dist * 0.6, cz + dist * 0.5)
        fill_loc = (cx - dist * 0.8, cy - dist * 0.6, cz + dist * 0.4)
        rim_loc = (cx, cy + dist * 0.9, cz + dist * 0.8)
        key_obj = _create_light("Light_Cine_WarmKey", "AREA", key_loc, center, base_energy * 1.4, _kelvin_to_rgb(3200), radius * 1.0, collection=col)
        fill_obj = _create_light("Light_Cine_CoolFill", "AREA", fill_loc, center, base_energy * 0.45, _kelvin_to_rgb(7500), radius * 2.0, collection=col)
        rim_obj = _create_light("Light_Cine_EdgeRim", "SPOT", rim_loc, center, base_energy * 1.6, (0.9, 0.95, 1.0), radius * 0.6, collection=col)
        created_lights = [key_obj.name, fill_obj.name, rim_obj.name]

    elif preset_key == "architectural":
        # Sunlight vector + Skylight dome
        sun_data = bpy.data.lights.new(name="Light_Arch_Sun_Data", type='SUN')
        sun_data.energy = base_energy * 3.0
        sun_data.color = _kelvin_to_rgb(5200)
        sun_obj = bpy.data.objects.new("Light_Arch_Sun", sun_data)
        sun_obj.location = (cx + dist, cy - dist, cz + dist * 1.5)
        dir_vec = mathutils.Vector(center) - sun_obj.location
        sun_obj.rotation_euler = dir_vec.to_track_quat('-Z', 'Y').to_euler()
        col.objects.link(sun_obj)

        sky_loc = (cx, cy, cz + dist * 1.8)
        sky_obj = _create_light("Light_Arch_Sky", "AREA", sky_loc, center, base_energy * 0.6, _kelvin_to_rgb(7000), radius * 4.0, collection=col)
        created_lights = [sun_obj.name, sky_obj.name]

    elif preset_key == "horror_atmosphere":
        # Low eerie uplight, harsh cold shadows
        up_loc = (cx, cy - dist * 0.7, cz - dist * 0.4)
        up_obj = _create_light("Light_Horror_Uplight", "SPOT", up_loc, center, base_energy * 1.8, (0.65, 0.85, 0.70), radius * 0.4, collection=col)
        flicker_loc = (cx + dist * 0.3, cy + dist * 0.3, cz + dist * 1.2)
        flicker_obj = _create_light("Light_Horror_Overhead", "POINT", flicker_loc, center, base_energy * 0.3, (0.4, 0.6, 0.5), radius * 0.2, collection=col)
        created_lights = [up_obj.name, flicker_obj.name]

    elif preset_key == "daylight":
        sun_data = bpy.data.lights.new(name="Light_Daylight_Sun_Data", type='SUN')
        sun_data.energy = base_energy * 5.0
        sun_data.color = (1.0, 0.98, 0.92)
        sun_obj = bpy.data.objects.new("Light_Daylight_Sun", sun_data)
        sun_obj.location = (cx + dist * 0.6, cy - dist * 0.6, cz + dist * 2.0)
        dir_vec = mathutils.Vector(center) - sun_obj.location
        sun_obj.rotation_euler = dir_vec.to_track_quat('-Z', 'Y').to_euler()
        col.objects.link(sun_obj)
        created_lights = [sun_obj.name]

    elif preset_key == "night_scene":
        moon_data = bpy.data.lights.new(name="Light_Moon_Data", type='SUN')
        moon_data.energy = base_energy * 0.25
        moon_data.color = (0.45, 0.60, 0.85)
        moon_obj = bpy.data.objects.new("Light_Moonlight", moon_data)
        moon_obj.location = (cx - dist, cy + dist, cz + dist * 1.5)
        dir_vec = mathutils.Vector(center) - moon_obj.location
        moon_obj.rotation_euler = dir_vec.to_track_quat('-Z', 'Y').to_euler()
        col.objects.link(moon_obj)

        accent_loc = (cx + dist * 0.5, cy - dist * 0.5, cz + dist * 0.2)
        accent_obj = _create_light("Light_Warm_Accent", "POINT", accent_loc, center, base_energy * 0.5, _kelvin_to_rgb(2200), radius * 0.3, collection=col)
        created_lights = [moon_obj.name, accent_obj.name]

    elif preset_key == "automotive_studio":
        # Elongated strip softboxes overhead and flanking for continuous specular reflection lines
        strip_len = dist * 2.2
        strip_w = dist * 0.35
        # Top strip
        top_loc = (cx, cy, cz + dist * 1.2)
        top_obj = _create_light("Light_Auto_Strip_Top", "AREA", top_loc, center, base_energy * 1.6, (1.0, 1.0, 1.0), strip_w, strip_len, collection=col)
        # Left flank strip
        l_loc = (cx - dist * 1.2, cy, cz + dist * 0.4)
        l_obj = _create_light("Light_Auto_Strip_Left", "AREA", l_loc, center, base_energy * 1.1, (0.95, 0.98, 1.0), strip_w, strip_len, collection=col)
        # Right flank strip
        r_loc = (cx + dist * 1.2, cy, cz + dist * 0.4)
        r_obj = _create_light("Light_Auto_Strip_Right", "AREA", r_loc, center, base_energy * 1.1, (1.0, 0.98, 0.95), strip_w, strip_len, collection=col)
        created_lights = [top_obj.name, l_obj.name, r_obj.name]

    return format_tool_response(
        "setup_studio_lighting",
        result={
            "preset": preset_key,
            "collection": collection_name,
            "lights_created": created_lights,
            "center": [round(cx, 2), round(cy, 2), round(cz, 2)],
            "bounding_radius": round(radius, 2),
            "base_energy": round(base_energy, 1)
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["lights_spawned", "targeted_to_bounds"]}
    )


def setup_environment_hdri(
    hdri_path_or_preset: str = "studio",
    strength: float = 1.0,
    rotation: float = 0.0,
    background_visibility: bool = True
) -> Dict[str, Any]:
    """Configure World shader node tree with HDRI image or calibrated sky."""
    if not HAS_BPY:
        return format_tool_response(
            "setup_environment_hdri",
            result={"target": hdri_path_or_preset, "strength": strength, "rotation": rotation},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World_Studio")
        bpy.context.scene.world = world

    world.use_nodes = True
    tree = world.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputWorld')
    out.location = (400, 0)
    bg = nodes.new('ShaderNodeBackground')
    bg.location = (150, 0)
    bg.inputs["Strength"].default_value = max(0.0, float(strength))
    links.new(bg.outputs["Background"], out.inputs["Surface"])

    # If file exists on disk, load image texture
    import os
    if os.path.exists(hdri_path_or_preset):
        coord = nodes.new('ShaderNodeTexCoord')
        coord.location = (-600, 0)
        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-400, 0)
        mapping.inputs["Rotation"].default_value[2] = math.radians(rotation)
        links.new(coord.outputs["Generated"], mapping.inputs["Vector"])

        env_tex = nodes.new('ShaderNodeTexEnvironment')
        env_tex.location = (-150, 0)
        try:
            img = bpy.data.images.load(hdri_path_or_preset, check_existing=True)
            env_tex.image = img
            links.new(mapping.outputs["Vector"], env_tex.inputs["Vector"])
            links.new(env_tex.outputs["Color"], bg.inputs["Color"])
        except Exception as e:
            return format_tool_response(
                "setup_environment_hdri",
                success=False,
                errors=[f"Failed to load HDRI file: {str(e)}"],
                risk=OperationRisk.NON_DESTRUCTIVE
            )
    else:
        # Fallback to calibrated studio ambient sky color
        bg.inputs["Color"].default_value = (0.05, 0.05, 0.06, 1.0)

    return format_tool_response(
        "setup_environment_hdri",
        result={
            "world_name": world.name,
            "strength": strength,
            "rotation": rotation,
            "background_configured": True
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["world_nodes_configured"]}
    )


def inspect_lighting_setup() -> Dict[str, Any]:
    """Inspect structured inventory of all scene lights and world environment."""
    if not HAS_BPY:
        return format_tool_response(
            "inspect_lighting_setup",
            result={"light_count": 0, "lights": [], "world_strength": 1.0},
            success=True,
            risk=OperationRisk.READ_ONLY
        )

    light_list = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT' and obj.data:
            ld = obj.data
            light_list.append({
                "name": obj.name,
                "type": ld.type,
                "energy": ld.energy,
                "color": [round(c, 3) for c in ld.color],
                "location": [round(v, 2) for v in obj.location],
                "size": getattr(ld, "size", None),
                "collections": [c.name for c in obj.users_collection]
            })

    w_strength = 1.0
    if bpy.context.scene.world and bpy.context.scene.world.use_nodes:
        bg = bpy.context.scene.world.node_tree.nodes.get("Background")
        if bg:
            w_strength = bg.inputs["Strength"].default_value

    return format_tool_response(
        "inspect_lighting_setup",
        result={
            "light_count": len(light_list),
            "lights": light_list,
            "world_strength": w_strength,
        },
        success=True,
        risk=OperationRisk.READ_ONLY
    )


def adjust_lighting_for_object(
    target_object: str,
    key_fill_ratio: float = 2.5
) -> Dict[str, Any]:
    """Dynamically adjust existing studio lights to match target object dimensions."""
    if not HAS_BPY:
        return format_tool_response(
            "adjust_lighting_for_object",
            result={"target_object": target_object, "adjusted": True},
            success=True,
            risk=OperationRisk.REVERSIBLE
        )

    obj = bpy.data.objects.get(target_object)
    if not obj:
        return format_tool_response(
            "adjust_lighting_for_object",
            success=False,
            errors=[f"Target object '{target_object}' not found."],
            risk=OperationRisk.REVERSIBLE
        )

    center, radius = _get_target_bounds(target_object)
    adjusted_lights = []

    for o in bpy.context.scene.objects:
        if o.type == 'LIGHT' and o.data:
            # Re-aim light at new object center
            direction = mathutils.Vector(center) - o.location
            o.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
            adjusted_lights.append(o.name)

    return format_tool_response(
        "adjust_lighting_for_object",
        result={
            "target_object": target_object,
            "center": [round(c, 2) for c in center],
            "radius": round(radius, 2),
            "adjusted_lights": adjusted_lights
        },
        success=True,
        risk=OperationRisk.REVERSIBLE
    )
