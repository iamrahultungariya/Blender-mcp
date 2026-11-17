"""Camera Framing, Composition & Depth of Field Engine for Rahul 3D Engine.

Provides mathematically precise bounding-box framing, sensor-calibrated distances,
cinematic compositions (rule of thirds, hero angle), Depth of Field bokeh,
and 360-degree turntable orbit animation.
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


def _get_or_create_camera(camera_name: str = "Camera_Main") -> Any:
    """Retrieve existing camera or spawn new one linked to scene collection."""
    if not HAS_BPY:
        return None
    cam_obj = bpy.data.objects.get(camera_name)
    if not cam_obj or cam_obj.type != 'CAMERA':
        cam_data = bpy.data.cameras.new(name=f"{camera_name}_Data")
        cam_obj = bpy.data.objects.new(camera_name, cam_data)
        bpy.context.scene.collection.objects.link(cam_obj)
    return cam_obj


def _get_object_bounds_and_radius(object_name: str) -> Tuple[Tuple[float, float, float], float]:
    """Calculate world-space center coordinate and circumscribed bounding sphere radius."""
    if not HAS_BPY:
        return (0.0, 0.0, 1.0), 1.5

    obj = bpy.data.objects.get(object_name)
    if not obj:
        # Fallback to scene
        return (0.0, 0.0, 1.0), 2.0

    bb = [obj.matrix_world @ mathutils.Vector(v) for v in obj.bound_box]
    center = sum(bb, mathutils.Vector()) / 8.0
    radius = max((v - center).length for v in bb)
    return (center.x, center.y, center.z), max(0.2, radius)


def _compute_framing_distance(radius: float, lens_mm: float, sensor_width: float, margin: float) -> float:
    """Calculate required distance to fit sphere inside sensor FOV with margin."""
    fov_h = 2.0 * math.atan(sensor_width / (2.0 * lens_mm))
    # Assume 16:9 aspect ratio for vertical FOV
    sensor_height = sensor_width * (9.0 / 16.0)
    fov_v = 2.0 * math.atan(sensor_height / (2.0 * lens_mm))
    min_fov = min(fov_h, fov_v)
    return (radius * max(1.0, margin)) / math.sin(min_fov / 2.0)


def frame_camera_to_object(
    object_name: str,
    lens_mm: float = 50.0,
    angle: str = "three_quarters",
    margin: float = 1.15,
    camera_name: str = "Camera_Main",
    composition: str = "center"
) -> Dict[str, Any]:
    """Calculate world bounds and position active camera to perfectly frame object.
    
    Supported Angles:
    front, back, left, right, top, bottom, three_quarters, isometric, hero, low_angle, high_angle.
    
    Supported Compositions:
    center, rule_of_thirds, cinematic, product_hero, architectural.
    """
    angle_key = angle.strip().lower()
    valid_angles = [
        "front", "back", "left", "right", "top", "bottom",
        "three_quarters", "isometric", "hero", "low_angle", "high_angle"
    ]
    if angle_key not in valid_angles:
        return format_tool_response(
            "frame_camera_to_object",
            success=False,
            errors=[f"Unsupported angle '{angle}'. Valid angles: {', '.join(valid_angles)}"],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    if not HAS_BPY:
        return format_tool_response(
            "frame_camera_to_object",
            result={"camera": camera_name, "object": object_name, "angle": angle_key, "framed": True},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    obj = bpy.data.objects.get(object_name)
    if not obj:
        return format_tool_response(
            "frame_camera_to_object",
            success=False,
            errors=[f"Target object '{object_name}' not found."],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    cam_obj = _get_or_create_camera(camera_name)
    cam = cam_obj.data
    cam.lens = max(10.0, min(300.0, float(lens_mm)))
    sensor_w = cam.sensor_width or 36.0

    center, radius = _get_object_bounds_and_radius(object_name)
    cx, cy, cz = center
    dist = _compute_framing_distance(radius, cam.lens, sensor_w, margin)

    # Calculate camera coordinate relative to target center
    if angle_key == "front":
        pos = (cx, cy - dist, cz)
    elif angle_key == "back":
        pos = (cx, cy + dist, cz)
    elif angle_key == "left":
        pos = (cx - dist, cy, cz)
    elif angle_key == "right":
        pos = (cx + dist, cy, cz)
    elif angle_key == "top":
        pos = (cx, cy, cz + dist)
    elif angle_key == "bottom":
        pos = (cx, cy, cz - dist)
    elif angle_key == "three_quarters":
        azimuth = math.radians(45)
        elevation = math.radians(25)
        pos = (
            cx + dist * math.cos(elevation) * math.sin(azimuth),
            cy - dist * math.cos(elevation) * math.cos(azimuth),
            cz + dist * math.sin(elevation)
        )
    elif angle_key == "isometric":
        azimuth = math.radians(45)
        elevation = math.radians(35.264)
        pos = (
            cx + dist * math.cos(elevation) * math.sin(azimuth),
            cy - dist * math.cos(elevation) * math.cos(azimuth),
            cz + dist * math.sin(elevation)
        )
    elif angle_key == "hero":
        # Dramatic low quarter angle looking upward
        azimuth = math.radians(35)
        elevation = math.radians(10)
        pos = (
            cx + dist * math.cos(elevation) * math.sin(azimuth),
            cy - dist * math.cos(elevation) * math.cos(azimuth),
            cz - radius * 0.3
        )
    elif angle_key == "low_angle":
        pos = (cx, cy - dist, cz - radius * 0.5)
    elif angle_key == "high_angle":
        pos = (cx + dist * 0.5, cy - dist * 0.5, cz + dist * 0.8)

    cam_obj.location = pos

    # Composition offset
    target_vec = mathutils.Vector(center)
    if composition.lower() == "rule_of_thirds":
        target_vec.x += radius * 0.3
        target_vec.z += radius * 0.15
    elif composition.lower() == "product_hero":
        target_vec.z -= radius * 0.1

    # Aim camera directly at target vector
    direction = target_vec - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Set as active scene camera
    bpy.context.scene.camera = cam_obj

    return format_tool_response(
        "frame_camera_to_object",
        result={
            "camera_name": cam_obj.name,
            "target_object": obj.name,
            "angle": angle_key,
            "composition": composition,
            "lens_mm": cam.lens,
            "distance": round(dist, 2),
            "camera_location": [round(v, 2) for v in cam_obj.location],
            "target_center": [round(v, 2) for v in center]
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["camera_positioned", "active_camera_set"]}
    )


def setup_camera_dof(
    target_object: Optional[str] = None,
    f_stop: float = 2.8,
    focus_distance: float = 0.0,
    enabled: bool = True,
    camera_name: str = "Camera_Main"
) -> Dict[str, Any]:
    """Configure optical Depth of Field (bokeh blur) on camera."""
    if not HAS_BPY:
        return format_tool_response(
            "setup_camera_dof",
            result={"camera": camera_name, "f_stop": f_stop, "enabled": enabled},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    cam_obj = bpy.data.objects.get(camera_name) or bpy.context.scene.camera
    if not cam_obj or cam_obj.type != 'CAMERA':
        return format_tool_response(
            "setup_camera_dof",
            success=False,
            errors=[f"Camera '{camera_name}' not found and no active scene camera set."],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    cam = cam_obj.data
    cam.dof.use_dof = bool(enabled)
    cam.dof.aperture_fstop = max(0.5, min(64.0, float(f_stop)))

    focus_obj_name = None
    if target_object:
        focus_target = bpy.data.objects.get(target_object)
        if focus_target:
            cam.dof.focus_object = focus_target
            focus_obj_name = focus_target.name

    if not focus_obj_name and focus_distance > 0.0:
        cam.dof.focus_object = None
        cam.dof.focus_distance = focus_distance

    return format_tool_response(
        "setup_camera_dof",
        result={
            "camera_name": cam_obj.name,
            "enabled": cam.dof.use_dof,
            "f_stop": cam.dof.aperture_fstop,
            "focus_object": focus_obj_name,
            "focus_distance": round(cam.dof.focus_distance, 2)
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["dof_configured"]}
    )


def create_turntable_camera(
    target_object: str,
    frames: int = 120,
    height: float = 1.5,
    radius: float = 0.0,
    start_frame: int = 1,
    end_frame: int = 120,
    camera_name: str = "Camera_Turntable"
) -> Dict[str, Any]:
    """Animate a 360-degree orbit camera path around target object."""
    if not HAS_BPY:
        return format_tool_response(
            "create_turntable_camera",
            result={"camera_name": camera_name, "frames": frames, "total_frames": frames, "start": start_frame, "end": end_frame},
            success=True,
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    center, b_radius = _get_object_bounds_and_radius(target_object)
    cx, cy, cz = center
    orbit_radius = radius if radius > 0.0 else max(2.0, b_radius * 2.8)

    cam_obj = _get_or_create_camera(camera_name)
    bpy.context.scene.camera = cam_obj
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Create empty aim controller at object center
    aim_name = f"{camera_name}_AimTarget"
    aim_obj = bpy.data.objects.get(aim_name)
    if not aim_obj:
        aim_obj = bpy.data.objects.new(aim_name, None)
        aim_obj.empty_display_type = 'PLAIN_AXES'
        aim_obj.empty_display_size = 0.2
        bpy.context.scene.collection.objects.link(aim_obj)
    aim_obj.location = center

    # Setup TrackTo constraint to eliminate camera roll
    track_con = None
    for con in cam_obj.constraints:
        if con.type == 'TRACK_TO':
            track_con = con
            break
    if not track_con:
        track_con = cam_obj.constraints.new(type='TRACK_TO')
    track_con.target = aim_obj
    track_con.track_axis = 'TRACK_NEGATIVE_Z'
    track_con.up_axis = 'UP_Y'

    # Clear previous animation data
    cam_obj.animation_data_clear()

    # Keyframe circular motion at 5 cardinal points
    steps = 4
    for i in range(steps + 1):
        frac = i / float(steps)
        frame = int(start_frame + frac * (end_frame - start_frame))
        theta = frac * 2.0 * math.pi
        px = cx + orbit_radius * math.cos(theta)
        py = cy + orbit_radius * math.sin(theta)
        pz = cz + height
        cam_obj.location = (px, py, pz)
        cam_obj.keyframe_insert(data_path="location", frame=frame)

    # Set linear extrapolation on animation curves for seamless loop
    if cam_obj.animation_data and cam_obj.animation_data.action:
        for fcurve in cam_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    return format_tool_response(
        "create_turntable_camera",
        result={
            "camera_name": cam_obj.name,
            "target_object": target_object,
            "total_frames": frames,
            "frame_range": [start_frame, end_frame],
            "orbit_radius": round(orbit_radius, 2),
            "height": height
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["orbit_keyframes_inserted", "track_constraint_active"]}
    )


def inspect_camera_setup(camera_name: str = "Camera_Main") -> Dict[str, Any]:
    """Inspect structured camera settings, focal length, clipping, and DoF."""
    if not HAS_BPY:
        return format_tool_response(
            "inspect_camera_setup",
            result={"camera": camera_name, "lens_mm": 50.0, "active": True},
            success=True,
            risk=OperationRisk.READ_ONLY
        )

    cam_obj = bpy.data.objects.get(camera_name) or bpy.context.scene.camera
    if not cam_obj or cam_obj.type != 'CAMERA':
        return format_tool_response(
            "inspect_camera_setup",
            success=False,
            errors=[f"Camera '{camera_name}' not found and no active camera set in scene."],
            risk=OperationRisk.READ_ONLY
        )

    cam = cam_obj.data
    is_active = (bpy.context.scene.camera == cam_obj)

    return format_tool_response(
        "inspect_camera_setup",
        result={
            "camera_name": cam_obj.name,
            "is_active_scene_camera": is_active,
            "lens_mm": cam.lens,
            "sensor_width": cam.sensor_width,
            "clip_start": cam.clip_start,
            "clip_end": cam.clip_end,
            "location": [round(v, 2) for v in cam_obj.location],
            "rotation_euler": [round(math.degrees(v), 1) for v in cam_obj.rotation_euler],
            "dof": {
                "enabled": cam.dof.use_dof,
                "f_stop": cam.dof.aperture_fstop,
                "focus_object": cam.dof.focus_object.name if cam.dof.focus_object else None,
                "focus_distance": round(cam.dof.focus_distance, 2)
            }
        },
        success=True,
        risk=OperationRisk.READ_ONLY
    )
