# Automated Mesh Repair, Remeshing & Decimation Engine (System 04)
**Rahul 3D Engine — Phase 5 Documentation**

---

## 1. Overview
The Topology & Remeshing Engine moves beyond diagnosing mesh defects to providing non-destructive, automated mesh repair and polygon optimization.

It features:
- **QuadriFlow Remeshing**: Reconstructs chaotic triangulated or boolean-sliced geometry into clean quad-dominant flow, automatically backing up target mesh datablocks prior to execution.
- **Controlled Decimation**: Downsamples polygon count while preserving existing UV coordinates and vertex groups.
- **Watertight Topology Repair**: BMesh-level cleanup that removes duplicate vertices, purges loose edges/vertices, dissolves degenerate zero-area faces, and recalculates outward normals.
- **Multi-LOD Chain Generation**: Produces LOD0 (100%), LOD1 (50%), LOD2 (25%), and LOD3 (10%) assets organized in a dedicated collection.

---

## 2. FastMCP Tool Interface

### `repair_mesh_topology`
Cleans up non-manifold geometry, loose vertices, zero-area faces, and inconsistent normals.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `remove_doubles` (bool): Merge coincident vertices within threshold (default: True).
  - `remove_loose` (bool): Delete unconnected vertices and edges (default: True).
  - `fix_normals` (bool): Recalculate outward normals (default: True).
  - `dissolve_degenerate` (bool): Delete zero-area faces (default: True).
  - `merge_distance` (float): Distance threshold in meters (default: 0.0001m).
- **Risk**: `DESTRUCTIVE`.

### `decimate_mesh`
Reduces polygon and triangle count with controlled ratios.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `target_ratio` (float): Ratio [0.01 to 1.0] (default: 0.5).
  - `preserve_uvs` (bool): Preserve UV seam borders (default: True).
  - `preserve_symmetry` (bool): Preserve bilateral symmetry.
  - `triangulate` (bool): Triangulate collapsed faces.
  - `apply_modifier` (bool): Destructively collapse modifier into mesh.
- **Risk**: `DESTRUCTIVE` if `apply_modifier=True`, else `REVERSIBLE`.

### `quad_remesh`
Executes QuadriFlow remeshing with quad dominance validation.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `target_quads` (int): Target quad polygon count (default: 5000).
  - `preserve_symmetry` (bool): Maintain symmetry.
  - `preserve_sharp` (bool): Respect sharp creases.
  - `preserve_boundary` (bool): Retain open boundary edge loops.
  - `adaptive_size` (int): Curvature adaptive resolution [0 to 100].
- **Risk**: `DESTRUCTIVE`.

### `generate_lod_chain`
Builds a sequential LOD asset chain in a designated collection.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `lod_ratios` (list[float]): Ratios for each level (default: `[1.0, 0.5, 0.25, 0.10]`).
  - `collection_name` (str): Output collection (default: `LODs`).
- **Risk**: `NON_DESTRUCTIVE`.
