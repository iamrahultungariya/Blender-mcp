# Cloth Simulation & Draping Engine (System 05)
**Rahul 3D Engine — Phase 6 Documentation**

---

## 1. Overview
The Cloth Simulation Engine introduces physical textile behavior for props where geometric math alone is insufficient (e.g. bedding duvets, dropped blankets, hanging curtains, tablecloths, and sofa slipcovers).

It operates **fully headlessly in background mode** using iterative scene frame evaluation, eliminating modal UI hangs. Once settled, the simulation can be frozen into a clean, zero-overhead static mesh.

---

## 2. FastMCP Tool Interface

### `setup_cloth_physics`
Configures a Cloth modifier with calibrated physical textile parameters.
- **Parameters**:
  - `cloth_object` (str): Target mesh object.
  - `preset` (str): `cotton`, `silk`, `denim`, `wool`, `leather`, `rubber`.
  - `mass` (float, optional): Vertex mass in kilograms.
  - `tension` (float, optional): Structural tension stiffness.
  - `compression` (float, optional): Compression stiffness.
  - `shear` (float, optional): Diagonal shear resistance.
  - `bending` (float, optional): Fabric fold stiffness.
  - `damping` (float, optional): Velocity damping.
  - `quality_steps` (int): Solver iterations per frame (default: 5).
- **Risk**: `NON_DESTRUCTIVE`.

### `bake_cloth_drop`
Simulates dropping cloth onto collision obstacles headlessly and freezes the final resting pose into static geometry.
- **Parameters**:
  - `cloth_object` (str): Target cloth object.
  - `collision_objects` (list[str]): Obstacle objects (automatically assigns Collision modifiers).
  - `steps` (int): Number of settling frames to step through (default: 40).
  - `pin_boundary` (bool): Pin boundary edge vertices.
  - `apply_result` (bool): Freeze final shape to static mesh (default: True).
- **Risk**: `DESTRUCTIVE` if `apply_result=True`, else `NON_DESTRUCTIVE`.

### `inspect_cloth_simulation`
Inspects cloth settings, mass, tension, and modifier presence.
- **Risk**: `READ_ONLY`.
