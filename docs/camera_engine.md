# Camera Framing, Composition & Depth of Field Engine (System 03)
**Rahul 3D Engine — Phase 4 Documentation**

---

## 1. Overview
The Camera Engine eliminates blind, hardcoded camera positioning by computing mathematically accurate framing distances based on the 3D bounding volume of target assets, camera sensor width, and lens focal length.

It features:
- **Trigonometric Distance Calculation**:
  $$\text{Distance} = \frac{\text{bounding\_radius} \times \text{margin}}{\sin(\text{FOV} / 2)}$$
- **11 Canonical Viewing Angles**: Front, back, left, right, top, bottom, three_quarters, isometric, hero, low_angle, high_angle.
- **Cinematic Composition Shifts**: Rule of thirds, product hero, and architectural headroom adjustments.
- **Optical Depth of Field (Bokeh)**: Focal object tracking or manual focal distance with physical f-stops.
- **360° Turntable Animation**: Circular orbit path keyframing with TrackTo constraints guaranteeing zero roll.

---

## 2. FastMCP Tool Interface

### `frame_camera_to_object`
Frames the active scene camera onto target object.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `lens_mm` (float): Focal length in millimeters (default: 50.0mm).
  - `angle` (str): `front`, `back`, `left`, `right`, `top`, `bottom`, `three_quarters`, `isometric`, `hero`, `low_angle`, `high_angle`.
  - `margin` (float): Framing safety margin (default: 1.15).
  - `camera_name` (str): Camera object name (default: `Camera_Main`).
  - `composition` (str): `center`, `rule_of_thirds`, `cinematic`, `product_hero`, `architectural`.
- **Risk**: `NON_DESTRUCTIVE`.

### `setup_camera_dof`
Configures camera Depth of Field bokeh.
- **Parameters**:
  - `target_object` (str, optional): Object to lock focus onto.
  - `f_stop` (float): Aperture f-stop (default: 2.8).
  - `focus_distance` (float): Manual focal distance in meters if no target object.
  - `enabled` (bool): Toggle DoF on/off.
- **Risk**: `NON_DESTRUCTIVE`.

### `create_turntable_camera`
Creates a seamless 360-degree orbit camera animation loop around target.
- **Parameters**:
  - `target_object` (str): Object to orbit around.
  - `frames` (int): Total animation duration in frames (default: 120).
  - `height` (float): Height offset in meters (default: 1.5m).
  - `radius` (float): Orbit radius in meters (0.0 = auto-calculate).
  - `start_frame` (int): Starting frame (default: 1).
  - `end_frame` (int): Ending frame (default: 120).
- **Risk**: `NON_DESTRUCTIVE`.

### `inspect_camera_setup`
Returns structured camera settings (lens, sensor, clipping, location, rotation, DoF).
- **Risk**: `READ_ONLY`.
