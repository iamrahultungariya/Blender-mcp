# Phases 4–7: Camera, Topology & LOD, Cloth & Placement, Modifiers & Rigging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Phases 4 through 7 of the Rahul 3D Engine Master Engineering Directive: Camera Framing & Composition (System 03), Automated Mesh Repair, Remeshing & Decimation (System 04), Cloth Simulation & Surface Placement (Systems 05 & 06), and Modifier Stack Automation & Mechanical Rigging (Systems 08 & 09).

**Architecture:**
- Modular engine pattern under `src/blender_mcp/`:
  - `camera_engine.py`: Bounding-box trigonometry, sensor aspect ratio, FOV math, DoF bokeh, turntable orbit keyframing.
  - `topology_engine.py`: QuadriFlow remeshing, decimation with UV preservation, non-manifold topology repair, LOD chain generation.
  - `cloth_engine.py`: Physical cloth parameter setup, headless frame-by-frame simulation evaluation, freeze to static mesh.
  - `placement_engine.py`: Raycast surface snapping, surface-normal alignment, memory-efficient instance scattering (`Alt+D` shared mesh datablocks).
  - `modifier_engine.py`: Declarative modifier stack builder, validation, ordering, non-destructive inspection, and safe freezing.
  - `rigging_engine.py`: Vehicle wheel/steering pivot empty hierarchy, architectural hinge constraints with rotation limits, mechanical pivot controllers.
- Blender execution: `addon.py` command dispatch table and delegation methods.
- Server orchestration: `server.py` FastMCP tool registrations with structured schemas and risk classifications.
- Pure-Python fallbacks: Math calculations and contracts execute cleanly in unit tests without `bpy`.

**Tech Stack:** Python 3.11+, Blender Python API (`bpy`, `bmesh`, `mathutils`), FastMCP / MCP SDK, Pytest.

**Spec:** `docs/production_capability_audit.md` and Master Engineering Directive.

## Global Constraints

- Do not alter or break TCP port `9876` or Protocol version `15`.
- Do not modify or break any existing tools.
- Keep `src/blender_mcp/bundled/addon.py` byte-identical to `addon.py`.
- Handle headless environments where `bpy` is absent cleanly in unit tests (`try: import bpy except ImportError: HAS_BPY = False`).
- Automatic safety: Any destructive operation (QuadriFlow remeshing, modifier freezing, mesh decimation) must automatically trigger or recommend `create_scene_checkpoint()`.

## Review Focus

1. *Camera FOV & aspect ratio calculation*: Correct distance computation ($D = \frac{R \cdot M}{\sin(\text{FOV}/2)}$) taking into account sensor width, lens focal length, and render aspect ratio.
2. *Non-destructive QuadriFlow remeshing*: Ensure target mesh is duplicated or backed up prior to invoking C-level remesher operators.
3. *Headless cloth baking*: Ensure frame evaluation uses `bpy.context.scene.frame_set()` iteratively instead of blocking modal UI operators.
4. *Instance scattering memory efficiency*: Ensure `scatter_instances` shares existing mesh datablocks (`obj.data = master_mesh`) rather than spawning heavy duplicate mesh geometries.
5. *Addon deployment parity*: Mirror `addon.py` to `bundled/addon.py` and deploy to Blender roaming directory.

---

### Task 1: Phase 4 — Camera Framing, Composition & Depth of Field Engine (System 03)

**Files:**
- Create: `src/blender_mcp/camera_engine.py`
- Modify: `addon.py` (Dispatch table + methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase4_camera_engine.py`

**Interfaces:**
- Consumes: `bpy.data.cameras`, `mathutils.Vector`, `mathutils.Euler`
- Produces: MCP tools:
  - `frame_camera_to_object(object_name, lens_mm, angle, margin, camera_name, composition)`
  - `setup_camera_dof(target_object, f_stop, focus_distance, enabled, camera_name)`
  - `create_turntable_camera(target_object, frames, height, radius, start_frame, end_frame, camera_name)`
  - `inspect_camera_setup(camera_name)`

- [x] **Step 1: Create `src/blender_mcp/camera_engine.py`**
- [x] **Step 2: Add Camera handlers to `addon.py`**
- [x] **Step 3: Register Camera tools in `server.py`**
- [x] **Step 4: Write and run Phase 4 unit tests (`tests/test_phase4_camera_engine.py`)**

---

### Task 2: Phase 5 — Automated Mesh Repair, Remeshing & Decimation (System 04)

**Files:**
- Create: `src/blender_mcp/topology_engine.py`
- Modify: `addon.py` (Dispatch table + methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase5_topology_engine.py`

**Interfaces:**
- Consumes: `bpy.ops.object.quadriflow_remesh`, `bmesh.ops.remove_doubles`, `bpy.data.meshes`
- Produces: MCP tools:
  - `quad_remesh(object_name, target_quads, preserve_symmetry, preserve_sharp, preserve_boundary, adaptive_size)`
  - `decimate_mesh(object_name, target_ratio, preserve_uvs, preserve_symmetry, triangulate, apply_modifier)`
  - `repair_mesh_topology(object_name, remove_doubles, remove_loose, fix_normals, dissolve_degenerate, merge_distance)`
  - `generate_lod_chain(object_name, lod_ratios, collection_name)`

- [x] **Step 1: Create `src/blender_mcp/topology_engine.py`**
- [x] **Step 2: Add Topology handlers to `addon.py`**
- [x] **Step 3: Register Topology tools in `server.py`**
- [x] **Step 4: Write and run Phase 5 unit tests (`tests/test_phase5_topology_engine.py`)**

---

### Task 3: Phase 6 — Cloth Simulation & Surface Placement (Systems 05 & 06)

**Files:**
- Create: `src/blender_mcp/cloth_engine.py`
- Create: `src/blender_mcp/placement_engine.py`
- Modify: `addon.py` (Dispatch table + methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase6_cloth_and_placement.py`

**Interfaces:**
- Consumes: `bpy.ops.object.modifier_add(type='CLOTH')`, `scene.ray_cast`, `mathutils.bvhtree.BVHTree`
- Produces: MCP tools:
  - `setup_cloth_physics(cloth_object, preset, mass, tension, compression, shear, bending, damping, quality_steps)`
  - `bake_cloth_drop(cloth_object, collision_objects, steps, pin_boundary, apply_result)`
  - `inspect_cloth_simulation(cloth_object)`
  - `snap_to_surface(object_name, target_surface_name, offset, alignment_mode, ray_direction)`
  - `align_object_to_surface(object_name, target_surface_name)`
  - `scatter_instances(collection_name, target_surface, count, random_rotation, random_scale, min_distance, distribution, seed)`
  - `inspect_scatter_result(target_surface)`

- [x] **Step 1: Create `src/blender_mcp/cloth_engine.py`**
- [x] **Step 2: Create `src/blender_mcp/placement_engine.py`**
- [x] **Step 3: Add Cloth & Placement handlers to `addon.py`**
- [x] **Step 4: Register Cloth & Placement tools in `server.py`**
- [x] **Step 5: Write and run Phase 6 unit tests (`tests/test_phase6_cloth_and_placement.py`)**

---

### Task 4: Phase 7 — Modifier Stack Automation & Mechanical Rigging (Systems 08 & 09)

**Files:**
- Create: `src/blender_mcp/modifier_engine.py`
- Create: `src/blender_mcp/rigging_engine.py`
- Modify: `addon.py` (Dispatch table + methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase7_modifiers_and_rigging.py`

**Interfaces:**
- Consumes: `obj.modifiers`, `bpy.data.objects.new('EMPTY')`, `obj.constraints`
- Produces: MCP tools:
  - `apply_modifier_stack(object_name, stack, apply_immediately)`
  - `inspect_modifier_stack(object_name)`
  - `freeze_modifiers(object_name, modifier_names, create_backup)`
  - `setup_vehicle_rig(chassis_obj, wheel_objs, steering_wheels, suspension_enabled, rig_name)`
  - `setup_hinge_constraint(door_obj, frame_obj, axis, limits, hinge_position, constraint_type)`
  - `setup_mechanical_pivot(object_name, pivot_location, parent_name)`
  - `inspect_rig_hierarchy(root_obj)`

- [x] **Step 1: Create `src/blender_mcp/modifier_engine.py`**
- [x] **Step 2: Create `src/blender_mcp/rigging_engine.py`**
- [x] **Step 3: Add Modifier & Rigging handlers to `addon.py`**
- [x] **Step 4: Register Modifier & Rigging tools in `server.py`**
- [x] **Step 5: Write and run Phase 7 unit tests (`tests/test_phase7_modifiers_and_rigging.py`)**

---

### Task 5: Addon Synchronization, Deployment & Documentation

**Files:**
- Modify: `src/blender_mcp/bundled/addon.py` (Ensure byte parity with `addon.py`)
- Deploy to: `C:/Users/Rahul/AppData/Roaming/Blender Foundation/Blender/5.2/scripts/addons/blender_mcp.py`
- Create docs:
  - `docs/camera_engine.md`
  - `docs/topology_repair.md`
  - `docs/cloth_simulation.md`
  - `docs/surface_placement.md`
  - `docs/modifier_engine.md`
  - `docs/mechanical_rigging.md`

- [x] **Step 1: Mirror `addon.py` to `src/blender_mcp/bundled/addon.py`**
- [x] **Step 2: Deploy addon to local Blender user addons folder**
- [x] **Step 3: Run comprehensive pytest regression suite across all phases**
- [x] **Step 4: Author documentation files**
