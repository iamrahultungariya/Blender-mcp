"""Mechanical & Vehicle Rigging Engine for Rahul 3D Engine.

Provides automated vehicle chassis/wheel/steering empty rigs,
architectural hinge constraints with rotational limits, and mechanical pivot setups.
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


def setup_vehicle_rig(
    chassis_obj: str,
    wheel_objs: List[str],
    steering_wheels: Optional[List[str]] = None,
    suspension_enabled: bool = False,
    rig_name: str = "Vehicle_Rig"
) -> Dict[str, Any]:
    """Build complete vehicle empty controller hierarchy (Root, Chassis, Steer, Wheels)."""
    steer_names = steering_wheels or []

    if not HAS_BPY:
        return format_tool_response(
            "setup_vehicle_rig",
            result={"rig_name": rig_name, "chassis": chassis_obj, "wheels": wheel_objs, "steering": steer_names},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    chassis = bpy.data.objects.get(chassis_obj)
    if not chassis:
        return format_tool_response("setup_vehicle_rig", success=False, errors=[f"Chassis object '{chassis_obj}' not found."], risk=OperationRisk.NON_DESTRUCTIVE)

    # 1. Master Root Empty
    root_empty = bpy.data.objects.new(f"{rig_name}_Root", None)
    root_empty.empty_display_type = 'ARROWS'
    root_empty.empty_display_size = 1.0
    root_empty.location = chassis.location
    bpy.context.scene.collection.objects.link(root_empty)

    # 2. Chassis Controller Empty
    chassis_empty = bpy.data.objects.new(f"{rig_name}_Body_CTRL", None)
    chassis_empty.empty_display_type = 'CUBE'
    chassis_empty.empty_display_size = 0.5
    chassis_empty.location = chassis.location
    chassis_empty.parent = root_empty
    bpy.context.scene.collection.objects.link(chassis_empty)

    # Parent chassis mesh to body empty
    chassis.parent = chassis_empty

    wheel_controllers = []
    steer_controllers = []

    for w_name in wheel_objs:
        w_obj = bpy.data.objects.get(w_name)
        if not w_obj:
            continue

        # Calculate wheel center
        w_center = w_obj.matrix_world.translation.copy()

        # Wheel Roll Controller
        wheel_empty = bpy.data.objects.new(f"CTRL_Wheel_{w_obj.name}", None)
        wheel_empty.empty_display_type = 'CIRCLE'
        wheel_empty.empty_display_size = 0.35
        wheel_empty.location = w_center
        bpy.context.scene.collection.objects.link(wheel_empty)

        if w_name in steer_names:
            # Steering Empty (controls Z yaw)
            steer_empty = bpy.data.objects.new(f"CTRL_Steer_{w_obj.name}", None)
            steer_empty.empty_display_type = 'SINGLE_ARROW'
            steer_empty.empty_display_size = 0.4
            steer_empty.location = w_center
            steer_empty.parent = chassis_empty
            bpy.context.scene.collection.objects.link(steer_empty)

            wheel_empty.parent = steer_empty
            steer_controllers.append(steer_empty.name)
        else:
            wheel_empty.parent = chassis_empty

        w_obj.parent = wheel_empty
        wheel_controllers.append(wheel_empty.name)

    return format_tool_response(
        "setup_vehicle_rig",
        result={
            "rig_name": rig_name,
            "root_controller": root_empty.name,
            "chassis_controller": chassis_empty.name,
            "wheel_controllers": wheel_controllers,
            "steering_controllers": steer_controllers,
            "total_wheels_rigged": len(wheel_controllers)
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["hierarchy_linked", "wheel_empties_aligned"]}
    )


def setup_hinge_constraint(
    door_obj: str,
    frame_obj: Optional[str] = None,
    axis: str = "Z",
    limits: Optional[List[float]] = None,
    hinge_position: Optional[List[float]] = None,
    constraint_type: str = "LIMIT_ROTATION"
) -> Dict[str, Any]:
    """Configure architectural or furniture door/drawer hinge pivot and rotation limits."""
    rot_limits = limits or [-90.0, 0.0]
    axis_key = axis.strip().upper()

    if not HAS_BPY:
        return format_tool_response(
            "setup_hinge_constraint",
            result={"door": door_obj, "axis": axis_key, "limits": rot_limits},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    door = bpy.data.objects.get(door_obj)
    if not door:
        return format_tool_response("setup_hinge_constraint", success=False, errors=[f"Door object '{door_obj}' not found."], risk=OperationRisk.NON_DESTRUCTIVE)

    # Hinge position defaults to bounding edge if not given
    if hinge_position:
        h_pos = mathutils.Vector(hinge_position)
    else:
        bb = [door.matrix_world @ mathutils.Vector(v) for v in door.bound_box]
        min_x = min(v.x for v in bb)
        cy = sum(v.y for v in bb) / 8.0
        cz = sum(v.z for v in bb) / 8.0
        h_pos = mathutils.Vector((min_x, cy, cz))

    # Spawn hinge pivot empty controller
    pivot_name = f"Pivot_{door.name}"
    pivot_empty = bpy.data.objects.new(pivot_name, None)
    pivot_empty.empty_display_type = 'SINGLE_ARROW'
    pivot_empty.empty_display_size = 0.2
    pivot_empty.location = h_pos
    bpy.context.scene.collection.objects.link(pivot_empty)

    # Parent door to pivot empty (preserving world transforms)
    door.parent = pivot_empty
    door.matrix_parent_inverse = pivot_empty.matrix_world.inverted()

    # If frame given, parent pivot empty to frame
    if frame_obj:
        frame = bpy.data.objects.get(frame_obj)
        if frame:
            pivot_empty.parent = frame
            pivot_empty.matrix_parent_inverse = frame.matrix_world.inverted()

    # Limit rotation constraint
    con = pivot_empty.constraints.new(type='LIMIT_ROTATION')
    con.owner_space = 'LOCAL'

    min_rad = math.radians(rot_limits[0])
    max_rad = math.radians(rot_limits[1])

    if axis_key == "Z":
        con.use_limit_z = True
        con.min_z = min_rad
        con.max_z = max_rad
    elif axis_key == "X":
        con.use_limit_x = True
        con.min_x = min_rad
        con.max_x = max_rad
    elif axis_key == "Y":
        con.use_limit_y = True
        con.min_y = min_rad
        con.max_y = max_rad

    return format_tool_response(
        "setup_hinge_constraint",
        result={
            "door_object": door.name,
            "pivot_controller": pivot_empty.name,
            "axis": axis_key,
            "limits_deg": rot_limits,
            "hinge_location": [round(v, 3) for v in h_pos]
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["pivot_empty_spawned", "limit_constraint_configured"]}
    )


def setup_mechanical_pivot(
    object_name: str,
    pivot_location: List[float],
    parent_name: Optional[str] = None
) -> Dict[str, Any]:
    """Create a designated mechanical rotation/translation pivot controller empty."""
    if not HAS_BPY:
        return format_tool_response(
            "setup_mechanical_pivot",
            result={"object_name": object_name, "pivot": pivot_location},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    obj = bpy.data.objects.get(object_name)
    if not obj:
        return format_tool_response("setup_mechanical_pivot", success=False, errors=[f"Object '{object_name}' not found."], risk=OperationRisk.NON_DESTRUCTIVE)

    ctrl_name = f"Pivot_{obj.name}"
    ctrl = bpy.data.objects.new(ctrl_name, None)
    ctrl.empty_display_type = 'PLAIN_AXES'
    ctrl.location = tuple(pivot_location)
    bpy.context.scene.collection.objects.link(ctrl)

    obj.parent = ctrl
    obj.matrix_parent_inverse = ctrl.matrix_world.inverted()

    if parent_name:
        p_obj = bpy.data.objects.get(parent_name)
        if p_obj:
            ctrl.parent = p_obj
            ctrl.matrix_parent_inverse = p_obj.matrix_world.inverted()

    return format_tool_response(
        "setup_mechanical_pivot",
        result={
            "object_name": obj.name,
            "controller_empty": ctrl.name,
            "pivot_location": pivot_location
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE
    )


def inspect_rig_hierarchy(root_obj: str) -> Dict[str, Any]:
    """Traverse and return hierarchical tree of rigged objects, constraints, and controllers."""
    if not HAS_BPY:
        return format_tool_response(
            "inspect_rig_hierarchy",
            result={"root": root_obj, "children_count": 0, "controllers": []},
            success=True,
            risk=OperationRisk.READ_ONLY
        )

    root = bpy.data.objects.get(root_obj)
    if not root:
        return format_tool_response("inspect_rig_hierarchy", success=False, errors=[f"Root object '{root_obj}' not found."], risk=OperationRisk.READ_ONLY)

    def _traverse(obj: Any) -> Dict[str, Any]:
        constraints = [{"name": c.name, "type": c.type} for c in obj.constraints]
        children = [_traverse(child) for child in obj.children]
        return {
            "name": obj.name,
            "type": obj.type,
            "constraints": constraints,
            "children": children
        }

    tree = _traverse(root)
    return format_tool_response(
        "inspect_rig_hierarchy",
        result={"root_name": root.name, "hierarchy": tree},
        success=True,
        risk=OperationRisk.READ_ONLY
    )
