---
name: blender-dxr-kernel-architect
description: Use when authoring, modifying, or refactoring 3D scenes, CAD assets, vehicles, architecture, or game-ready props in Blender using DXR-grade scene partitioning, parametric tensor surfaces, visual hull space carving, and G-buffer vision.
---

# Blender DXR Kernel Architect

## Overview

Replaces naive text-token Python script running with DirectX Raytracing-inspired (DXR 1.722) graphics paradigms: **Partitioned TLAS (PTLAS)** for zero scene corruption, **Bicubic Bezier Tensor Patches (CLAS)** for smooth aerodynamic CAD surfaces, **3-Axis Visual Hull Space-Carving** for instant reference-to-3D silhouettes, and **G-Buffer 2D-to-3D Unprojection** for millimeter-accurate prop placement.

---

## The 4 Core Architectural Laws

```
1. MANDATORY PTLAS PARTITIONING
   Never execute unscoped global scripts. Every subsystem (room, chassis, interior, wheel)
   must be isolated in a named partition with Copy-on-Write rollback guarantees.

2. ZERO RAW PRIMITIVE RULE
   Banned: Stacking raw cubes/cylinders (primitive_cube_add) for curved or aerodynamic bodies.
   Required: Use sdf_space_carve (from reference PNGs) or clas_eval_bezier_patch / clas_loft_splines.

3. UV-RAY SURFACE PLACEMENT
   Banned: Guessing (X, Y, Z) world coordinates to attach props (lights, handles, beds, doors).
   Required: Query gbuffer_project_uv(quadrant, u, v) to resolve exact hit point and surface normal quaternion.

4. CLOSED-LOOP G-BUFFER VERIFICATION
   Before finalizing any multi-part build, render gbuffer_quad_capture to verify alignment
   across Top, Front, Side (with wireframe overlay) and Perspective views.
```

---

## FastMCP Tool Reference

| Tool Name | Subsystem | Purpose |
| --- | --- | --- |
| `ptlas_create_partition` | PTLAS | Creates isolated Collection with Merkle hash tracking |
| `ptlas_mutate_partition` | PTLAS | Executes Python strictly inside partition with CoW rollback |
| `ptlas_verify_integrity` | PTLAS | Audits SHA-256 hashes of all partitions to guarantee zero corruption |
| `sdf_space_carve` | SDF Engine | 3-axis visual hull voxel space carving from 1-3 reference PNGs in <350ms |
| `clas_eval_bezier_patch` | CLAS Tensor | Evaluates 16-point Bicubic Bezier patch into quad mesh via direct C-RNA |
| `clas_loft_splines` | CLAS Tensor | Lofts cross-section splines into aerodynamic fuselage/hull via C-RNA |
| `clas_boolean_carve` | CLAS Tensor | Watertight boolean carving with automatic bevel & weighted normals |
| `gbuffer_quad_capture` | G-Buffer | Renders 1024x1024 4-quad composite (Top, Front, Side+Wireframe, Studio) |
| `gbuffer_project_uv` | G-Buffer | Unprojects (u, v) pixel coordinate into 3D hit point & normal quaternion |
| `pbr_compile_curvature_ao` | PBR Compiler | Vectorized Laplacian edge-wear & cavity AO attribute bake in <20ms |
| `export_game_asset` | Exporter | Normalizes bottom pivot to (0,0,0), applies transforms, and exports GLB/FBX |

---

## Standard Workflows

### Workflow 1: Aerodynamic Vehicle (e.g. Ambulance, Sports Car)

1. **Step 1: Base Hull Generation**
   * If reference images exist: Call `sdf_space_carve(name="Ambulance_Hull", front_png_path=..., side_png_path=..., resolution=128)`.
   * If generating procedurally: Call `clas_eval_bezier_patch` with 16 control points defining hood and roof curvature, followed by `clas_loft_splines` for the main body.
2. **Step 2: Partition Isolation**
   * Call `ptlas_create_partition(name="Chassis")` and `ptlas_create_partition(name="Accessories")`.
3. **Step 3: Flush Accessory Attachment**
   * Render `gbuffer_quad_capture(filepath="render.png")`.
   * Find siren location on roof at normalized `(u=0.50, v=0.65)` in quadrant `"top"`.
   * Call `gbuffer_project_uv(quadrant="top", u=0.50, v=0.65)`.
   * Position Siren Lightbar at `hit_point` rotated by `quaternion`. Zero millimeter gap!
4. **Step 4: Weathering & Export**
   * Call `pbr_compile_curvature_ao(object_name="Ambulance_Hull")`.
   * Call `export_game_asset(target="Ambulance_Hull", filepath="ambulance.glb")`.

### Workflow 2: Large Architecture / Multi-Room Scene (e.g. 50-Room Hospital)

1. Create parent partition: `ptlas_create_partition("Hospital_Floor_1")`.
2. For each room, create an isolated child partition: `ptlas_create_partition(name="Room_ICU_101", parent_partition="Hospital_Floor_1")`.
3. Edit only the target room:
   ```python
   ptlas_mutate_partition(partition_id="Room_ICU_101", script="...")
   ```
4. Verify non-target partitions:
   ```python
   ptlas_verify_integrity()
   ```

---

## Anti-Patterns & Rationalizations

| Excuse / Bad Practice | Why It Fails | Correct Engineering Solution |
| --- | --- | --- |
| *"I'll just write a quick script that calls `select_all` and `delete`"* | Destroys the user's existing work and corrupts unrelated scene collections. | Use `ptlas_mutate_partition`. Only touch objects within your assigned partition. |
| *"I'll construct the vehicle hood out of cubes scaled and rotated"* | Creates ugly Lego-like boxy models with non-aerodynamic sharp seams. | Pass 16 Bezier control points to `clas_eval_bezier_patch`. |
| *"I'll calculate the 3D position of the door handle in my head"* | 95% chance of clipping into the door or floating in empty space. | Use `gbuffer_project_uv` to raycast to the actual evaluated surface. |
| *"Cycles baking will make it look realistic"* | Freezes the user's GPU for 30-60 seconds. | Use `pbr_compile_curvature_ao` for instant 18ms Laplacian edge weathering. |
