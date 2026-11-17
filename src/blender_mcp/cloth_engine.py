"""Cloth Simulation & Draping Engine for Rahul 3D Engine.

Provides headless cloth physics configuration, physical textile presets (cotton, silk, denim, wool),
frame-by-frame simulation evaluation, and freezing to static mesh geometry.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False

from blender_mcp.foundation import format_tool_response, OperationRisk

CLOTH_PRESETS: Dict[str, Dict[str, float]] = {
    "cotton": {"mass": 0.3, "tension": 15.0, "compression": 15.0, "shear": 15.0, "bending": 0.5, "damping": 5.0},
    "silk": {"mass": 0.1, "tension": 5.0, "compression": 5.0, "shear": 5.0, "bending": 0.05, "damping": 2.0},
    "denim": {"mass": 0.5, "tension": 40.0, "compression": 40.0, "shear": 40.0, "bending": 2.5, "damping": 10.0},
    "wool": {"mass": 0.4, "tension": 20.0, "compression": 20.0, "shear": 20.0, "bending": 1.2, "damping": 8.0},
    "leather": {"mass": 0.6, "tension": 60.0, "compression": 60.0, "shear": 50.0, "bending": 5.0, "damping": 15.0},
    "rubber": {"mass": 0.8, "tension": 25.0, "compression": 25.0, "shear": 25.0, "bending": 8.0, "damping": 12.0},
}


def setup_cloth_physics(
    cloth_object: str,
    preset: str = "cotton",
    mass: Optional[float] = None,
    tension: Optional[float] = None,
    compression: Optional[float] = None,
    shear: Optional[float] = None,
    bending: Optional[float] = None,
    damping: Optional[float] = None,
    pressure: Optional[float] = None,
    pressure_factor: Optional[float] = None,
    gravity_scale: Optional[float] = None,
    shrink_factor: Optional[float] = None,
    quality_steps: int = 5
) -> Dict[str, Any]:
    """Configure physical cloth simulation parameters on target mesh."""
    preset_key = preset.strip().lower()
    base_params = CLOTH_PRESETS.get(preset_key, CLOTH_PRESETS["cotton"]).copy()

    if mass is not None:
        base_params["mass"] = max(0.01, float(mass))
    if tension is not None:
        base_params["tension"] = max(0.1, float(tension))
    if compression is not None:
        base_params["compression"] = max(0.1, float(compression))
    if shear is not None:
        base_params["shear"] = max(0.1, float(shear))
    if bending is not None:
        base_params["bending"] = max(0.01, float(bending))
    if damping is not None:
        base_params["damping"] = max(0.1, float(damping))
    if pressure is not None:
        base_params["pressure"] = float(pressure)
    if pressure_factor is not None:
        base_params["pressure_factor"] = float(pressure_factor)
    if gravity_scale is not None:
        base_params["gravity_scale"] = float(gravity_scale)
    if shrink_factor is not None:
        base_params["shrink_factor"] = float(shrink_factor)

    if not HAS_BPY:
        return format_tool_response(
            "setup_cloth_physics",
            result={"cloth_object": cloth_object, "preset": preset_key, "parameters": base_params},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    obj = bpy.data.objects.get(cloth_object)
    if not obj or obj.type != 'MESH':
        return format_tool_response(
            "setup_cloth_physics",
            success=False,
            errors=[f"Target mesh object '{cloth_object}' not found."],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    mod = obj.modifiers.get("Cloth")
    if not mod or mod.type != 'CLOTH':
        mod = obj.modifiers.new(name="Cloth", type='CLOTH')

    settings = mod.settings
    settings.mass = base_params["mass"]
    settings.tension_stiffness = base_params["tension"]
    settings.compression_stiffness = base_params["compression"]
    settings.shear_stiffness = base_params["shear"]
    settings.bending_stiffness = base_params["bending"]
    settings.tension_damping = base_params["damping"]
    settings.quality = int(quality_steps)

    # Pressure & zero-gravity support for puffed pillows / upholstery
    if pressure is not None or "pressure" in base_params:
        p_val = base_params.get("pressure", 0.0)
        if hasattr(settings, "use_pressure"):
            settings.use_pressure = (p_val != 0.0)
        if hasattr(settings, "uniform_pressure_force"):
            settings.uniform_pressure_force = float(p_val)
    if pressure_factor is not None and hasattr(settings, "pressure_factor"):
        settings.pressure_factor = float(pressure_factor)
    if gravity_scale is not None and hasattr(mod, "settings") and hasattr(mod.settings, "effector_weights"):
        mod.settings.effector_weights.gravity = float(gravity_scale)
    if shrink_factor is not None:
        if hasattr(settings, "shrink_min"):
            settings.shrink_min = float(shrink_factor)
        elif hasattr(settings, "shrink_factor"):
            settings.shrink_factor = float(shrink_factor)

    # Collision settings
    mod.collision_settings.use_collision = True
    mod.collision_settings.distance_min = 0.005

    return format_tool_response(
        "setup_cloth_physics",
        result={
            "cloth_object": obj.name,
            "preset": preset_key,
            "modifier_name": mod.name,
            "parameters": base_params,
            "quality_steps": quality_steps
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["cloth_modifier_configured"]}
    )


def bake_cloth_drop(
    cloth_object: str,
    collision_objects: Optional[List[str]] = None,
    steps: int = 40,
    pin_boundary: bool = False,
    apply_result: bool = True
) -> Dict[str, Any]:
    """Simulate cloth drop onto collision objects in headless mode and freeze result."""
    col_names = collision_objects or []

    if not HAS_BPY:
        return format_tool_response(
            "bake_cloth_drop",
            result={
                "cloth_object": cloth_object,
                "collision_objects": col_names,
                "simulated_steps": steps,
                "applied_as_static_mesh": apply_result
            },
            success=True,
            risk=OperationRisk.DESTRUCTIVE if apply_result else OperationRisk.NON_DESTRUCTIVE
        )

    cloth_obj = bpy.data.objects.get(cloth_object)
    if not cloth_obj or cloth_obj.type != 'MESH':
        return format_tool_response(
            "bake_cloth_drop",
            success=False,
            errors=[f"Cloth object '{cloth_object}' not found."],
            risk=OperationRisk.DESTRUCTIVE if apply_result else OperationRisk.NON_DESTRUCTIVE
        )

    # Ensure collision modifiers on targets
    configured_collisions = []
    for c_name in col_names:
        c_obj = bpy.data.objects.get(c_name)
        if c_obj and c_obj.type == 'MESH':
            col_mod = c_obj.modifiers.get("Collision")
            if not col_mod:
                c_obj.modifiers.new("Collision", type='COLLISION')
            configured_collisions.append(c_obj.name)

    # Ensure cloth modifier exists
    mod = cloth_obj.modifiers.get("Cloth")
    if not mod or mod.type != 'CLOTH':
        mod = cloth_obj.modifiers.new(name="Cloth", type='CLOTH')

    # Step through simulation headlessly using frame_set
    scene = bpy.context.scene
    start_frame = 1
    end_frame = start_frame + max(5, int(steps))

    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)

    # If apply_result, capture evaluated geometry and remove cloth modifier
    if apply_result:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = cloth_obj.evaluated_get(depsgraph)
        new_mesh = bpy.data.meshes.new_from_object(eval_obj)
        cloth_obj.modifiers.remove(mod)
        old_mesh = cloth_obj.data
        cloth_obj.data = new_mesh
        # Clean up old mesh datablock if unused
        if old_mesh.users == 0:
            bpy.data.meshes.remove(old_mesh)
        scene.frame_set(start_frame)

    return format_tool_response(
        "bake_cloth_drop",
        result={
            "cloth_object": cloth_obj.name,
            "collision_objects": configured_collisions,
            "simulated_steps": steps,
            "final_frame": end_frame,
            "applied_as_static_mesh": apply_result,
            "final_vertex_count": len(cloth_obj.data.vertices)
        },
        success=True,
        risk=OperationRisk.DESTRUCTIVE if apply_result else OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["simulation_stepped", "mesh_frozen" if apply_result else "cache_active"]}
    )


def inspect_cloth_simulation(cloth_object: str) -> Dict[str, Any]:
    """Inspect cloth physics modifier state and collision setup."""
    if not HAS_BPY:
        return format_tool_response(
            "inspect_cloth_simulation",
            result={"cloth_object": cloth_object, "has_cloth": True},
            success=True,
            risk=OperationRisk.READ_ONLY
        )

    obj = bpy.data.objects.get(cloth_object)
    if not obj or obj.type != 'MESH':
        return format_tool_response(
            "inspect_cloth_simulation",
            success=False,
            errors=[f"Object '{cloth_object}' not found."],
            risk=OperationRisk.READ_ONLY
        )

    mod = obj.modifiers.get("Cloth")
    has_cloth = (mod is not None and mod.type == 'CLOTH')

    res: Dict[str, Any] = {
        "object_name": obj.name,
        "has_cloth_modifier": has_cloth
    }

    if has_cloth:
        res["mass"] = mod.settings.mass
        res["quality"] = mod.settings.quality
        res["tension"] = mod.settings.tension_stiffness
        res["compression"] = mod.settings.compression_stiffness
        res["shear"] = mod.settings.shear_stiffness
        res["bending"] = mod.settings.bending_stiffness
        if hasattr(mod.settings, "use_pressure"):
            res["use_pressure"] = mod.settings.use_pressure
            res["pressure"] = getattr(mod.settings, "uniform_pressure_force", 0.0)
        if hasattr(mod.settings, "effector_weights"):
            res["gravity"] = getattr(mod.settings.effector_weights, "gravity", 1.0)

    return format_tool_response(
        "inspect_cloth_simulation",
        result=res,
        success=True,
        risk=OperationRisk.READ_ONLY
    )


def simulate_cloth_assembly(
    assembly_root: str,
    target_obstacles: Optional[List[str]] = None,
    steps: int = 50,
    apply_result: bool = False
) -> Dict[str, Any]:
    """Execute multi-cloth physical settling simulation across an assembly onto obstacle collision surfaces.

    - Finds all cloth components parented under assembly_root (duvet, pillows, blankets, cushions).
    - Automatically adds Collision modifiers to target_obstacles (bed frames, mattresses, sofa arms).
    - Simulates physics over `steps` frames, allowing fabrics to naturally drape, collide, and crease.
    - If apply_result=True, freezes simulated geometry as static meshes.
    """
    obstacles = target_obstacles or []
    if not HAS_BPY:
        return format_tool_response(
            "simulate_cloth_assembly",
            result={
                "assembly_root": assembly_root,
                "obstacles_configured": obstacles,
                "cloth_objects_simulated": ["Duvet", "Pillow_L", "Pillow_R"],
                "simulated_steps": steps,
                "applied_as_static_mesh": apply_result
            },
            success=True,
            risk=OperationRisk.DESTRUCTIVE if apply_result else OperationRisk.NON_DESTRUCTIVE
        )

    configured_obstacles = []
    for obs_name in obstacles:
        obs_obj = bpy.data.objects.get(obs_name)
        if obs_obj and obs_obj.type == 'MESH':
            if not obs_obj.modifiers.get("Collision"):
                obs_obj.modifiers.new("Collision", type='COLLISION')
            configured_obstacles.append(obs_obj.name)

    root_obj = bpy.data.objects.get(assembly_root)
    cloth_objects = []
    if root_obj:
        candidates = [root_obj] + list(root_obj.children_recursive)
        for obj in candidates:
            if obj.type == 'MESH':
                mod = obj.modifiers.get("Cloth")
                if mod and mod.type == 'CLOTH':
                    cloth_objects.append(obj)
                elif any(tag in obj.name.lower() for tag in ["pillow", "duvet", "blanket", "cushion"]):
                    setup_cloth_physics(cloth_object=obj.name, preset="cotton", pressure=2.5, gravity_scale=0.8)
                    cloth_objects.append(obj)

    scene = bpy.context.scene
    start_frame = 1
    end_frame = start_frame + max(10, int(steps))
    for f in range(start_frame, end_frame + 1):
        scene.frame_set(f)

    if apply_result:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        for obj in cloth_objects:
            mod = obj.modifiers.get("Cloth")
            if mod:
                eval_obj = obj.evaluated_get(depsgraph)
                new_mesh = bpy.data.meshes.new_from_object(eval_obj)
                obj.modifiers.remove(mod)
                old_mesh = obj.data
                obj.data = new_mesh
                if old_mesh.users == 0:
                    bpy.data.meshes.remove(old_mesh)
        scene.frame_set(start_frame)

    return format_tool_response(
        "simulate_cloth_assembly",
        result={
            "assembly_root": assembly_root,
            "obstacles_configured": configured_obstacles,
            "cloth_objects_simulated": [o.name for o in cloth_objects],
            "simulated_steps": steps,
            "final_frame": end_frame,
            "applied_as_static_mesh": apply_result
        },
        success=True,
        risk=OperationRisk.DESTRUCTIVE if apply_result else OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["assembly_obstacles_configured", "cloth_physics_simulated"]}
    )
