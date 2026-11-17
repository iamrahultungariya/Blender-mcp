# Surface Snapping, Scattering & Kitbash Placement Engine (System 06)
**Rahul 3D Engine — Phase 6 Documentation**

---

## 1. Overview
The Placement Engine enables AI agents to distribute props naturally and accurately across surfaces without penetration or floating.

It features:
- **Raycast Surface Snapping**: Drops objects along arbitrary ray vectors until their lowest bounding vertex sits flush on the target surface.
- **Normal Alignment**: Matches object orientation with target surface normals.
- **Memory-Efficient Instancing**: Employs `Alt+D` shared mesh datablocks (`new_obj.data = proto.data`) so that scattering hundreds of rocks, books, or foliage props adds zero polygon memory overhead.

---

## 2. FastMCP Tool Interface

### `snap_to_surface`
Snaps an object so its lowest bound rests on a target surface.
- **Parameters**:
  - `object_name` (str): Target prop object to place.
  - `target_surface_name` (str): Ground, table, shelf, or floor object.
  - `offset` (float): Clearance offset in meters (default: 0.0).
  - `alignment_mode` (str): `BOTTOM_TO_SURFACE`.
  - `ray_direction` (list[float]): Raycast vector (default: `[0.0, 0.0, -1.0]`).
- **Risk**: `NON_DESTRUCTIVE`.

### `align_object_to_surface`
Aligns local +Z axis of an object with the surface normal at its contact point.
- **Risk**: `NON_DESTRUCTIVE`.

### `scatter_instances`
Scatters linked instances of prototype models across a surface with distance rejection.
- **Parameters**:
  - `collection_name` (str): Collection containing prototype models.
  - `target_surface` (str): Surface to scatter across.
  - `count` (int): Number of instances to scatter (default: 20).
  - `random_rotation` (bool): Randomize Z-axis yaw [0° to 360°] (default: True).
  - `random_scale` (list[float]): Min and max scale bounds (default: `[0.8, 1.2]`).
  - `min_distance` (float): Minimum distance between instances (default: 0.1m).
  - `distribution` (str): `random`, `uniform`.
  - `seed` (int): Reproducible random seed.
- **Risk**: `NON_DESTRUCTIVE`.

### `inspect_scatter_result`
Returns instance count and scatter collection details.
- **Risk**: `READ_ONLY`.
