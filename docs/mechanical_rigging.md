# Mechanical & Vehicle Rigging Engine (System 09)
**Rahul 3D Engine — Phase 7 Documentation**

---

## 1. Overview
The Mechanical & Vehicle Rigging Engine automates empty controller hierarchies, constraints, and pivot points for interactive environmental assets, architectural doors/drawers, and vehicle chassis.

---

## 2. FastMCP Tool Interface

### `setup_vehicle_rig`
Constructs an empty-controller hierarchy for vehicle bodies, roll wheels, and steering yaw.
- **Hierarchy Structure**:
  - `Vehicle_Root` (Master scene transform)
    - `Vehicle_Body_CTRL` (Chassis roll/pitch controller)
      - `CTRL_Steer_Wheel_FL` (Steering yaw controller)
        - `CTRL_Wheel_Wheel_FL` (Roll spin controller)
          - `Wheel_FL` (Mesh geometry)
- **Parameters**:
  - `chassis_obj` (str): Vehicle body mesh.
  - `wheel_objs` (list[str]): List of 4 wheel mesh objects.
  - `steering_wheels` (list[str]): Wheels that steer (e.g. front pair).
  - `suspension_enabled` (bool): Enable suspension empties.
  - `rig_name` (str): Prefix for rig controllers (default: `Vehicle_Rig`).
- **Risk**: `NON_DESTRUCTIVE`.

### `setup_hinge_constraint`
Creates an architectural door or cabinet drawer hinge controller with limit constraints.
- **Parameters**:
  - `door_obj` (str): Moving door/drawer panel object.
  - `frame_obj` (str, optional): Stationary wall or cabinet frame object.
  - `axis` (str): Rotation axis (`X`, `Y`, `Z` - default: `Z`).
  - `limits` (list[float]): Min and max rotation angles in degrees (default: `[-90.0, 0.0]`).
  - `hinge_position` (list[float], optional): Explicit hinge pivot coordinates (defaults to door bounding edge).
  - `constraint_type` (str): `LIMIT_ROTATION`.
- **Risk**: `NON_DESTRUCTIVE`.

### `setup_mechanical_pivot`
Creates an Empty controller at a specified 3D pivot coordinate and parents the target object to it.
- **Risk**: `NON_DESTRUCTIVE`.

### `inspect_rig_hierarchy`
Traverses and returns the controller parent/children tree, constraints, and limits starting from a root object.
- **Risk**: `READ_ONLY`.
