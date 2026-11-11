# DXR-Inspired Blender MCP Graphics Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-architect `mcp-for-blender` (v2.0.0) from a naive script-runner into a Zero-Copy, Partitioned Neural-CAD and SDF Geometry Kernel inspired by Microsoft DirectX Raytracing (PTLAS, CLAS, OpenVDB Visual Hull, G-Buffer Vision, and Laplacian Curvature/AO).

**Architecture:** Layered systems architecture featuring:
1. `src/blender_mcp/protocol.py`: Length-prefixed framing (4-byte big-endian uint32) with automatic fallback for legacy unframed JSON.
2. `src/blender_mcp/kernel/ptlas_partition_manager.py`: Spatial DAG partition isolation, C-pointer Merkle hashes, AST validation, and Copy-on-Write rollback.
3. `src/blender_mcp/kernel/sdf_visual_hull.py`: 3-axis broadcast distance transform space-carving and OpenVDB volume meshing.
4. `src/blender_mcp/kernel/clas_tensor_shaper.py`: 16-point Bicubic Bezier tensor patches, spline profile lofting, and direct C-RNA `foreach_set` injection.
5. `src/blender_mcp/kernel/gbuffer_vision.py`: 4-quad offscreen G-buffer composite (Top, Front, Side+Diff, AgX Studio) and 2D-to-3D BVH raycast unprojector.
6. `src/blender_mcp/kernel/curvature_pbr_compiler.py`: Vectorized Laplacian mean curvature, BVH AO vertex attribute generation, and Triplanar PBR shader compiler.
7. `src/blender_mcp/server.py` & `addon.py`: FastMCP tools and Blender add-on event integration (synced with `src/blender_mcp/bundled/addon.py`).
8. `skills/blender-dxr-kernel-architect/SKILL.md`: Companion skill enforcing CAD workflows.

**Tech Stack:** Python 3.10+, numpy, Blender RNA/C-API (`bpy.data`, `bmesh`, `mathutils`, `gpu`), FastMCP, socket protocol framing.

**Spec:** DXR-Inspired Blender MCP Systems Architecture Specification.

## Global Constraints

1. 100% Backward Compatibility: All legacy tools (`execute_blender_code`, `get_scene_info`, `search_assets`, `import_asset`, `viewport_capture`, etc.) must remain functional without breaking signatures or behavior.
2. Dual-Mode Transport: Socket communication must support 4-byte length-header framing (`>I`) while auto-detecting and decoding legacy unframed JSON.
3. Cross-Version Blender Support: Shims must dynamically support Blender 3.0 to 4.x+ (`Principled BSDF` socket renaming and 4.1+ `use_auto_smooth` deprecation).
4. Headless & Background Mode: Background execution (`blender -b`) must not block on missing UI timers.
5. Addon Synchronization: Any modification to `addon.py` must be mirrored in `src/blender_mcp/bundled/addon.py`.

## Review Focus

1. Framed socket receiver handling TCP window fragmentation and arbitrary payload sizes without memory leakage or desynchronization.
2. AST audit rejecting destructive scene operations (`select_all`, `delete`, `read_factory_settings`) during partition mutation.
3. SDF space carving handling edge cases (single image, missing silhouettes, zero-area masks).
4. UV-to-surface raycast gracefully handling rays that miss the mesh geometry.
5. Laplacian matrix generation handling non-manifold or disconnected vertex graphs without divide-by-zero errors.

---

### Task 1: Length-Prefixed Binary Socket Framing Protocol

**Files:**
- Create: `src/blender_mcp/protocol.py`
- Test: `tests/test_dxr_protocol.py`

**Interfaces:**
- Produces: `encode_frame(data: bytes | str | dict) -> bytes`
- Produces: `class FrameReceiver`: `feed(data: bytes) -> list[dict]`, `reset()`
- Produces: `send_framed_message(sock: socket.socket, message: dict)`
- Produces: `receive_framed_message(sock: socket.socket, timeout: float = 180.0) -> dict`

- [ ] **Step 1: Write the failing test for framing protocol**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `src/blender_mcp/protocol.py` with 4-byte uint32 header and dual-mode JSON fallback**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 2: PTLAS Scene Partitioning & Copy-on-Write Isolation Kernel

**Files:**
- Create: `src/blender_mcp/kernel/ptlas_partition_manager.py`
- Test: `tests/test_dxr_ptlas.py`

**Interfaces:**
- Produces: `audit_script_ast(code: str, allowed_partition: str) -> tuple[bool, str]`
- Produces: `compute_mesh_hash(mesh_data) -> str`
- Produces: `class PTLASManager`:
  - `create_partition(name: str, parent: str = "") -> dict`
  - `begin_transaction(partition_name: str) -> dict`
  - `verify_integrity() -> tuple[bool, list[str]]`
  - `rollback_transaction(partition_name: str) -> bool`
  - `commit_transaction(partition_name: str) -> bool`

- [ ] **Step 1: Write the failing test for PTLAS AST validation and Merkle hashing**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `src/blender_mcp/kernel/ptlas_partition_manager.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 3: Visual Hull Space-Carving & OpenVDB SDF Engine

**Files:**
- Create: `src/blender_mcp/kernel/sdf_visual_hull.py`
- Test: `tests/test_dxr_sdf.py`

**Interfaces:**
- Produces: `compute_visual_hull_tensor(front_mask: np.ndarray, side_mask: np.ndarray, top_mask: np.ndarray, resolution: int = 128) -> np.ndarray`
- Produces: `extract_sdf_isosurface(voxel_tensor: np.ndarray, iso_value: float = 0.0) -> tuple[np.ndarray, np.ndarray]`
- Produces: `generate_hull_mesh_data(front_path: str, side_path: str, top_path: str, resolution: int = 128) -> dict`

- [ ] **Step 1: Write the failing test for 3D tensor intersection and distance transforms**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `src/blender_mcp/kernel/sdf_visual_hull.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 4: CLAS Cluster Templates & Zero-Copy Tensor Shaper

**Files:**
- Create: `src/blender_mcp/kernel/clas_tensor_shaper.py`
- Test: `tests/test_dxr_clas.py`

**Interfaces:**
- Produces: `eval_bicubic_bezier_patch(control_grid_4x4: np.ndarray, res_u: int = 32, res_v: int = 32) -> tuple[np.ndarray, np.ndarray, np.ndarray]`
- Produces: `loft_spline_sections(sections: list[np.ndarray], resolution: int = 32, closed: bool = True) -> tuple[np.ndarray, np.ndarray, np.ndarray]`
- Produces: `apply_blender_version_compatibility(node_tree_or_mesh, version_tuple=None)`

- [ ] **Step 1: Write the failing test for vectorized Bezier patch evaluation and lofting**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `src/blender_mcp/kernel/clas_tensor_shaper.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 5: G-Buffer Vision Sensor & 2D-to-3D Raycast Unprojector

**Files:**
- Create: `src/blender_mcp/kernel/gbuffer_vision.py`
- Test: `tests/test_dxr_gbuffer.py`

**Interfaces:**
- Produces: `unproject_pixel_ray(quadrant: str, u: float, v: float, view_matrix: list, proj_matrix: list) -> tuple[list[float], list[float]]`
- Produces: `raycast_bvh_surface(bvh_tree, ray_origin, ray_direction) -> dict`
- Produces: `normal_to_track_quaternion(normal: list[float], track_axis: str = 'Z', up_axis: str = 'Y') -> list[float]`

- [ ] **Step 1: Write the failing test for unprojection mathematics and quaternion alignment**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `src/blender_mcp/kernel/gbuffer_vision.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 6: Vectorized Laplacian Curvature & AO Compiler

**Files:**
- Create: `src/blender_mcp/kernel/curvature_pbr_compiler.py`
- Test: `tests/test_dxr_curvature.py`

**Interfaces:**
- Produces: `compute_laplacian_curvature(vertices: np.ndarray, loop_indices: np.ndarray, normals: np.ndarray) -> np.ndarray`
- Produces: `build_triplanar_pbr_nodes(material_name: str, base_color: tuple, metallic: float, roughness: float)`
- Produces: `prepare_asset_export_transforms(obj) -> dict`

- [ ] **Step 1: Write the failing test for Laplacian curvature vectorization**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `src/blender_mcp/kernel/curvature_pbr_compiler.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 7: FastMCP Server Integration

**Files:**
- Modify: `src/blender_mcp/server.py`
- Test: `tests/test_dxr_server_tools.py`

**Interfaces:**
- Registers 11 new FastMCP tools:
  - `ptlas_create_partition`
  - `ptlas_mutate_partition`
  - `ptlas_verify_integrity`
  - `sdf_space_carve`
  - `clas_eval_bezier_patch`
  - `clas_loft_splines`
  - `clas_boolean_carve`
  - `gbuffer_quad_capture`
  - `gbuffer_project_uv`
  - `pbr_compile_curvature_ao`
  - `export_game_asset`

- [ ] **Step 1: Write the failing test for server tool registration and framed client calls**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Update `src/blender_mcp/server.py` with framed transport and new tools**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 8: Blender Addon Core Integration

**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_dxr_addon_commands.py`

- [ ] **Step 1: Write the failing test for addon command dispatch**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Update `addon.py` and sync `src/blender_mcp/bundled/addon.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Task 9: Companion Skill Creation

**Files:**
- Create: `skills/blender-dxr-kernel-architect/SKILL.md`

- [ ] **Step 1: Draft `skills/blender-dxr-kernel-architect/SKILL.md` with trigger conditions, workflows, anti-patterns, and CAD rules**
- [ ] **Step 2: Validate YAML frontmatter, keywords, and instructions**
- [ ] **Step 3: Commit changes**

---

### Task 10: Full Regression & Integration Verification

**Files:**
- Run all existing tests and new DXR kernel tests.

- [ ] **Step 1: Run complete test suite: `pytest tests/ -v`**
- [ ] **Step 2: Verify zero regression in existing test suite**
- [ ] **Step 3: Final git commit and summary**
