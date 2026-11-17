# Real Computational Geometry Kernel & Automotive CAD Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate all fake stubs from `addon.py` by implementing genuine computational geometry algorithms (`clas_loft_splines`, `clas_boolean_carve`, `sdf_space_carve`, `gbuffer_quad_capture`, `pbr_compile_curvature_ao`), upgrading the automotive toolkit with Cubic Bezier curves, watertight boolean wheelhouse cavity carving, automated UV unwrapping (`TEXCOORD_0`), and PBR textures.

**Architecture:**
1. `addon.py` & `src/blender_mcp/bundled/addon.py`: Embed real algorithms for spline lofting, exact boolean carving, visual hull space carving, true 4-quadrant offscreen capture, and Laplacian curvature attribute compilation.
2. `src/blender_mcp/bmesh_toolkit.py`: Add `loft_splines`, `carve_cavity` (boolean difference), `apply_smart_uv_unwrapping`, and `eval_cubic_bezier_spline`.
3. `src/blender_mcp/vehicle_thinking.py`: Replace linear interpolation with Cubic Bezier math for hood rake, windshield compound curvature, and roof blister S-curve.
4. `src/blender_mcp/materials_preset.py`: Add procedural PBR node trees (normal map generation, clearcoat orange-peel, micro-scratches).
5. Synchronize with active Blender 5.2 add-on directory.

**Tech Stack:** Python 3.10+, Blender 5.2 C-API (`bpy`, `bmesh`, `mathutils`), numpy, Pillow/offscreen GPU, FastMCP.

**Spec:** Blender Computational Geometry & Class-A Automotive Surfacing Specification.

## Global Constraints

1. Zero Fake Stubs: Every method must execute genuine computational math; no hardcoded 8-vertex cubes, 0-vertex meshes, or unapplied modifiers.
2. Complete In-Addon Self-Containment: `addon.py` must run standalone inside Blender without requiring external pip dependencies outside Blender's standard distribution (`numpy`, `bpy`, `bmesh`, `mathutils`).
3. Addon Dual-Maintenance: `addon.py` and `src/blender_mcp/bundled/addon.py` must remain 100% byte-for-byte identical.
4. Mandatory Game-Ready Assets: Exported GLB models must include `TEXCOORD_0` UV maps and multi-material PBR setups.

## Review Focus

1. `clas_loft_splines` generating valid quad topology without twist or non-manifold edge collapse.
2. `clas_boolean_carve` executing clean boolean difference without leaving behind ghost cutter objects.
3. `sdf_space_carve` correctly extracting 3D visual hulls from real binary masks.
4. `gbuffer_quad_capture` rendering 4 distinct camera views rather than duplicating a single viewport.
5. `apply_smart_uv_unwrapping` producing non-overlapping UV islands with valid `TEXCOORD_0` in exported GLTF/GLB files.

---

### Phase 1: Real Computational Geometry Kernel Implementation in `addon.py`

#### Task 1: Real Spline Lofting Implementation (`clas_loft_splines`)
**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_real_clas_loft.py`

**Interfaces:**
- Produces: `clas_loft_splines(name, sections, resolution=32, closed=True, partition_id="") -> dict`
- Verifies: Mesh contains `len(sections) * resolution` vertices and `(len(sections)-1) * resolution` quads.

- [ ] **Step 1: Write failing test verifying `clas_loft_splines` generates real geometry**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement real vectorized spline lofting in `addon.py` and `bundled/addon.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

#### Task 2: Real Watertight Boolean Carving (`clas_boolean_carve`)
**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_real_boolean_carve.py`

**Interfaces:**
- Produces: `clas_boolean_carve(target_object, cutter_spec, bevel_segments=2, harden_normals=True) -> dict`
- Verifies: Spawns parametric cutter, applies `BOOLEAN` (operation=`DIFFERENCE`, solver=`EXACT`), verifies target vertex count changes, and cleans up cutter object.

- [ ] **Step 1: Write failing test for real boolean carving**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement real boolean difference in `addon.py` and `bundled/addon.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

#### Task 3: Real Visual Hull Space-Carving (`sdf_space_carve`)
**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_real_sdf_space_carve.py`

**Interfaces:**
- Produces: `sdf_space_carve(name, front_png=None, side_png=None, top_png=None, resolution=64, partition_id="") -> dict`
- Verifies: Processes real image masks, computes 3-axis broadcast intersection, and extracts watertight boundary quads.

- [ ] **Step 1: Write failing test for real visual hull space carving**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement real 3-axis visual hull engine in `addon.py` and `bundled/addon.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

#### Task 4: Real 4-Quadrant Viewport Capture (`gbuffer_quad_capture`)
**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_real_gbuffer_quad.py`

**Interfaces:**
- Produces: `gbuffer_quad_capture(filepath=None, max_size=1024) -> dict`
- Verifies: Renders 4 separate camera view matrices (Top, Front, Right, Perspective) into offscreen buffers and tiles them into a 2x2 grid image.

- [ ] **Step 1: Write failing test for 4-quadrant capture**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement genuine 4-view offscreen tiling in `addon.py` and `bundled/addon.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

#### Task 5: Real Laplacian Curvature & AO Compilation (`pbr_compile_curvature_ao`)
**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_real_curvature_ao.py`

**Interfaces:**
- Produces: `pbr_compile_curvature_ao(object_name, curvature_weight=1.0) -> dict`
- Verifies: Computes graph Laplacian curvature and stores actual non-zero floating-point values in `mesh.attributes["McpCurvatureAO"]`.

- [ ] **Step 1: Write failing test for Laplacian curvature compilation**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement real Laplacian graph math in `addon.py` and `bundled/addon.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Phase 2: Automotive Surfacing & UV/PBR Texture Engine

#### Task 6: Cubic Bezier & Hermite Splines in `bmesh_toolkit.py` & `vehicle_thinking.py`
**Files:**
- Modify: `src/blender_mcp/bmesh_toolkit.py`
- Modify: `src/blender_mcp/vehicle_thinking.py`
- Test: `tests/test_cubic_bezier_surfacing.py`

- [ ] **Step 1: Write failing test for Cubic Bezier curvature**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement Bernstein basis cubic evaluation in `bmesh_toolkit.py` and `vehicle_thinking.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

#### Task 7: Automated UV Unwrapping (`TEXCOORD_0`) & Wheelhouse Cavity Carving
**Files:**
- Modify: `src/blender_mcp/bmesh_toolkit.py`
- Modify: `src/blender_mcp/materials_preset.py`
- Test: `tests/test_uv_and_wheelhouse_carve.py`

- [ ] **Step 1: Write failing test verifying UV generation and wheelhouse carving**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `apply_smart_uv_unwrapping` and `carve_wheel_well_cavity`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit changes**

---

### Phase 3: Production Validation & Live Asset Rebuild

#### Task 8: Live Blender Verification & Model Rebuild
- [ ] Sync updated `addon.py` to active Blender 5.2 addon directory.
- [ ] Run full automated test suite (`uv run pytest`).
- [ ] Rebuild `AAA_Ambulance.blend` with genuine carved wheel wells, Cubic Bezier compound curvature, and valid `TEXCOORD_0` UV maps.
- [ ] Verify `AAA_Ambulance.glb` binary buffers contain `TEXCOORD_0` and clean quad topology.
