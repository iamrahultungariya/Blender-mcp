---
name: blender-computational-geometry
description: Use when authoring, modifying, or auditing 3D models, vehicles, CAD assets, or game props in Blender requiring Class-A surfacing, watertight boolean carving, visual hull space carving, or UV/PBR texture pipeline without fake stubs.
---

# Blender Computational Geometry & Class-A Surfacing

## Overview

Governs procedural and automated 3D geometry creation in Blender via MCP. Replaces naive box-stacking and placeholder mock stubs with **real computational geometry**: vectorized spline lofting, watertight boolean carving, 3-axis visual hull space carving, and mandatory UV unwrapping for game-ready PBR pipelines.

**Core Principle:** Every geometric tool must perform genuine computational math. No fake stubs, no floating ribbons posing as cavities, and no untextured meshes exported as game assets.

---

## The 4 Iron Laws of Computational Geometry

```
1. ZERO FAKE STUBS LAW
   Every MCP tool and add-on function (sdf_space_carve, clas_loft_splines, clas_boolean_carve,
   pbr_compile_curvature_ao, gbuffer_quad_capture) must execute genuine computational geometry algorithms.
   Banned: Returning hardcoded 8-vertex cubes, 0-vertex empty meshes, or ignoring input parameters.

2. WATERTIGHT BOOLEAN CAVITY LAW
   Cavities, wheelhouses, window recesses, and vents must be carved into the parent geometry
   using real boolean difference operations (Exact/Manifold solver).
   Banned: Gluing floating ribbons or planes on top of uncarved surfaces where geometry clips through.

3. CONTINUOUS CLASS-A SURFACING LAW
   Vehicle hoods, windshields, fuselages, and roof blisters must use Cubic Bezier tensor patches,
   Bernstein polynomials, or C-RNA spline lofting with smooth curvature continuity.
   Banned: Calling linear (1 - t) * A + t * B interpolation "splines" or assembling vehicles from cubes.

4. MANDATORY UV & PBR TEXTURE LAW
   Every production game asset must have a valid UV map (TEXCOORD_0 in glTF) and PBR material
   definition (Base Color, Normal/Bump, Roughness, Metallic).
   Banned: Exporting raw geometry with unmapped solid-color BSDF shaders and zero texture coordinates.
```

---

## Tool & Subsystem Reference

| Subsystem | Method / Tool | Genuine Algorithm Requirement |
| :--- | :--- | :--- |
| **Spline Lofting** | `clas_loft_splines` | Resamples $N$ cross-section splines to resolution $R$, stitches quad rings, computes vertex normals, and injects via C-RNA `foreach_set`. |
| **Boolean Carving** | `clas_boolean_carve` | Spawns parametric cutter volume, executes `BOOLEAN` (operation=`DIFFERENCE`, solver=`EXACT`), applies modifiers, and cleans up cutter. |
| **Visual Hull** | `sdf_space_carve` | Computes 3D voxel intersection $V(x,y,z) = F(x,z) \land S(y,z) \land T(x,y)$ across 1–3 orthographic silhouette masks and extracts quad isosurface. |
| **G-Buffer Multi-Angle** | `gbuffer_quad_capture` | Renders 4 distinct camera views (Top, Front, Right, Perspective) into offscreen buffers and stitches a genuine 2x2 contact sheet. |
| **Curvature & AO** | `pbr_compile_curvature_ao` | Computes graph Laplacian mean curvature $H_i = (V_i - \bar{V}_{\text{adj}}) \cdot N_i$ and stores in `mesh.attributes["McpCurvatureAO"]`. |

---

## Standard Workflows

### 1. Watertight Cavity Carving (e.g. Wheelhouse, Cabin Door, Window Frame)
```python
# 1. Target body exists: 'AMB_Chassis'
# 2. Carve wheel well cavity using genuine boolean difference
toolkit.carve_cavity(
    target_object="AMB_Chassis",
    cutter_type="CYLINDER",
    center=(1.02, 1.55, 0.38),
    radius=0.46,
    depth=0.28,
    axis="X"
)
# 3. Target now has an inward recessed cavity; wheel sits inside without clipping.
```

### 2. Class-A Aerodynamic Lofting (e.g. Van Fuselage, Boat Hull, Wing)
```python
# Pass M cross-section profiles (each containing P 3D points)
sections = [cowl_profile, header_profile, blister_profile, cargo_profile, rear_profile]
mesh_data = toolkit.loft_splines(
    name="Fuselage_Shell",
    sections=sections,
    resolution=32,
    closed=True
)
# Automatically creates watertight quad mesh with smooth normal transitions.
```

### 3. Automated UV Unwrapping & PBR Baking
```python
# Before export, ensure TEXCOORD_0 exists on all meshes
toolkit.apply_smart_uv_unwrapping(obj, angle_limit=66.0, island_margin=0.02)
# Assign PBR shader with normal map and procedural roughness
materials.setup_car_paint(name="M_Car_Paint", base_color=(0.95, 0.95, 0.95, 1.0))
```

---

## Anti-Patterns & Rationalizations

| Excuse / Rationalization | Reality | Required Action |
| :--- | :--- | :--- |
| *"I'll just return a cube for now and implement space carving later"* | Fake stubs corrupt the pipeline and force subsequent agents into boxy fallback loops. | Implement the real numpy voxel intersection or visual hull algorithm immediately. |
| *"Floating ribbons look good enough from one camera angle"* | From any other angle, the solid wall clips through the wheel, breaking 360-degree inspection. | Use boolean carving to create real inward cavities. |
| *"Linear interpolation between 6 points is a spline"* | Straight lines between 6 points produce angular facets, not smooth automotive stamping curves. | Use Bernstein basis polynomials or Bezier patches. |
| *"Material colors are enough; UV unwrapping isn't necessary for .glb"* | A glTF without `TEXCOORD_0` cannot receive normal maps, dirt overlays, or decals in game engines. | Always call automated UV unwrapping before export. |
