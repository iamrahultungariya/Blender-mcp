# AAA Automotive & Vehicle Procedural Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform `mcp-for-blender` from naive blocky cube-stacking into a professional AAA Automotive & Procedural Vehicle Pipeline featuring a BMesh Builder SDK, an Autonomous Vehicle Thinking/Heuristics Engine (reasoning about curves, tumblehome, rakes, blisters without requiring an image), a Procedural PBR Material Vault, and a 4-View Contact Sheet Asset Inspector.

**Architecture:**
1. `src/blender_mcp/bmesh_toolkit.py`: High-level parametric BMesh operations (`create_filleted_box`, `create_cylinder`, `create_wheel_arch`, `create_curved_windshield`, `create_swept_profile`, `apply_automotive_modifiers`).
2. `src/blender_mcp/vehicle_thinking.py`: Autonomous Vehicle Thinking & Topology Heuristics Engine specifying dimensional proportions, hood/windshield rake angles, aerodynamic roof blister transitions, tumblehome inward tilt, wheel arch clearances, and decal placement guidelines for various vehicle classes (Ambulance Van, Supercar, Sedan, Truck, SUV).
3. `src/blender_mcp/materials_preset.py`: Factory PBR shader vault (Car Paint with Clearcoat, Textured Bumper Plastic, Automotive Glass with Ceramic Frit, High-Lumen Emergency Emissives, Radial Tire Rubber, Chrome).
4. `src/blender_mcp/server.py` & `addon.py`: Automatic namespace injection of `toolkit`, `thinking`, and `materials` into `execute_blender_code`, plus the `inspect_asset` 2x2 multi-angle contact sheet tool.
5. Synchronization with `src/blender_mcp/bundled/addon.py`.

**Tech Stack:** Python 3.10+, Blender 4.x / 5.2+ LTS C-API (`bpy`, `bmesh`, `mathutils`), numpy, Pillow / offscreen OpenGL/GPU viewport capture, FastMCP.

**Spec:** Automotive Procedural Engineering Specification for Blender MCP.

## Global Constraints

1. Zero Breaking Changes: All existing tools (`execute_blender_code`, `get_scene_info`, `look`, DXR kernel tools) must remain fully backwards compatible.
2. Blender 4.1+ / 5.2+ Normal Standard: Deprecation of `use_auto_smooth` handled cleanly; geometry must use `Bevel` (2 segments, profile 0.5, harden normals) + `WeightedNormal` (keep sharp) + smooth shading or `geometry_node_smooth_by_angle`.
3. Addon Dual-Maintenance: Any change to `addon.py` must be mirrored synchronously in `src/blender_mcp/bundled/addon.py`.
4. Token Efficiency: Procedural builder helpers must reduce context payload by at least 60% compared to raw per-vertex scripts.
5. In-Memory Execution: All geometric computations remain in BMesh C RAM; object linking occurs only once per component.

## Review Focus

1. `bmesh_toolkit` primitive generators handling degenerate parameters (e.g., zero radius, coplanar points) without crashing Blender.
2. `VehicleThinkingEngine` correctly producing non-zero aerodynamic curves and rake angles when zero user reference images are supplied.
3. Automated modifier stack properly handling non-manifold or open sheet geometry without visual artifacts.
4. `inspect_asset` generating a clean, labeled 2x2 contact sheet image across different screen DPIs and headless setups.
5. `addon.py` client handler preserving zero-copy framing and namespace persistence across sequential commands.

---

### Phase 1: BMesh Automotive SDK & Vehicle Thinking Engine

#### Task 1: BMesh Parametric Builder SDK (`bmesh_toolkit.py`)

**Files:**
- Create: `src/blender_mcp/bmesh_toolkit.py`
- Test: `tests/test_bmesh_toolkit.py`

**Interfaces:**
- Produces: `create_filleted_box(bm, min_v, max_v, bevel_radius=0.02, bevel_segments=2, material_index=0)`
- Produces: `create_cylinder(bm, p1, p2, radius=0.1, segments=24, material_index=0, cap_ends=True)`
- Produces: `create_wheel_arch(bm, center, radius=0.45, width=0.15, lip_thickness=0.02, lip_outset=0.03, segments=16, material_index=0)`
- Produces: `create_curved_windshield(bm, bottom_center, top_center, width_bottom=1.8, width_top=1.6, curvature_depth=0.08, segments_u=8, segments_v=4, thickness=0.01, material_index=0)`
- Produces: `create_swept_profile(bm, profile_points_2d, rail_points_3d, closed=False, material_index=0)`
- Produces: `apply_automotive_modifiers(obj, bevel_width=0.008, bevel_segments=2, weighted_normal=True, smooth_angle_deg=35.0)`

- [x] **Step 1: Write the failing test for `bmesh_toolkit`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `src/blender_mcp/bmesh_toolkit.py`**
- [x] **Step 4: Run test to verify it passes**
- [x] **Step 5: Commit changes**

---

#### Task 2: Autonomous Vehicle Thinking & Topology Heuristics Engine (`vehicle_thinking.py`)

**Files:**
- Create: `src/blender_mcp/vehicle_thinking.py`
- Test: `tests/test_vehicle_thinking.py`

**Interfaces:**
- Produces: `class VehicleThinkingEngine`:
  - `get_archetype_proportions(vehicle_type: str) -> dict` (length, width, height, wheelbase, track, overhangs)
  - `get_aerodynamic_curvatures(vehicle_type: str) -> dict` (hood_rake_deg, windshield_rake_deg, windshield_curvature_sagitta, roof_blister_arc, tumblehome_deg)
  - `generate_van_chassis_profile(length=5.9, width=2.0, height=2.7) -> dict` (parametric guide splines for hood, windshield, roof, bumper, rear doors, wheel arches)
  - `get_decal_and_lighting_spec(vehicle_type: str) -> dict` (coordinates for front lightbar, rear pods, grille strobes, beltline stripes, emblem)

- [x] **Step 1: Write the failing test for `VehicleThinkingEngine`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `src/blender_mcp/vehicle_thinking.py`**
- [x] **Step 4: Run test to verify it passes**
- [x] **Step 5: Commit changes**

---

#### Task 3: Addon Namespace Injection & Toolkit Integration

**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_addon_namespace_injection.py`

**Interfaces:**
- Consumes: `bmesh_toolkit`, `vehicle_thinking`
- Produces: `execute_code` namespace containing `bpy`, `bmesh`, `mathutils`, `math`, `toolkit`, `thinking`

- [x] **Step 1: Write failing test verifying `execute_code` namespace contains `toolkit` and `thinking`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Update `addon.py` and `src/blender_mcp/bundled/addon.py` with embedded toolkit/thinking injection**
- [x] **Step 4: Run test to verify it passes**
- [x] **Step 5: Commit changes**

---

### Phase 2: Procedural PBR Material Vault & 4-View Contact Sheet Inspector

#### Task 4: Procedural PBR Material Vault (`materials_preset.py`)

**Files:**
- Create: `src/blender_mcp/materials_preset.py`
- Modify: `addon.py` & `src/blender_mcp/bundled/addon.py` (to inject `materials` into execution namespace)
- Test: `tests/test_materials_preset.py`

**Interfaces:**
- Produces: `setup_car_paint_material(name, base_color=(0.95, 0.95, 0.95, 1.0), clearcoat=1.0, metallic=0.0, roughness=0.12)`
- Produces: `setup_textured_plastic_material(name, base_color=(0.04, 0.04, 0.04, 1.0), roughness=0.75, bump_strength=0.15)`
- Produces: `setup_automotive_glass_material(name, tint_color=(0.08, 0.1, 0.12, 1.0), transmission=0.85, roughness=0.02, ior=1.52)`
- Produces: `setup_emergency_emissive_material(name, color=(1.0, 0.05, 0.05, 1.0), emission_strength=40.0)`
- Produces: `setup_radial_tire_material(name, base_color=(0.025, 0.025, 0.025, 1.0), roughness=0.6)`
- Produces: `setup_chrome_trim_material(name)`

- [x] **Step 1: Write the failing test for `materials_preset`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `src/blender_mcp/materials_preset.py` with Blender 4.x/5.2+ Principled BSDF socket mappings**
- [x] **Step 4: Run test to verify it passes**
- [x] **Step 5: Commit changes**

---

#### Task 5: 4-View Contact Sheet Asset Inspector (`inspect_asset`)

**Files:**
- Modify: `src/blender_mcp/server.py`
- Modify: `addon.py` & `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_inspect_asset.py`

**Interfaces:**
- Produces: `inspect_asset(target: list[str] | None = None, resolution: int = 1024, shading: str = "rendered") -> dict`
  - Captures 4 camera viewpoints:
    1. Top-Left: Front 3/4 perspective
    2. Top-Right: Rear 3/4 perspective
    3. Bottom-Left: Left Side orthographic
    4. Bottom-Right: Top orthographic
  - Assembles them into a single 2x2 grid image with labeled overlay text
  - Encodes directly as Base64 PNG for instant visual inspection

- [x] **Step 1: Write the failing test for `inspect_asset`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `inspect_asset` in `addon.py`, `bundled/addon.py`, and `server.py`**
- [x] **Step 4: Run test to verify it passes**
- [x] **Step 5: Commit changes**

---

### Phase 3: AAA Mercedes-Benz Sprinter Ambulance Generation (Subsequent Phase)

- Build continuous aerodynamic van monocoque body using `toolkit` & `thinking` rules.
- Add contoured bumper, air intake, flush curved headlights, and curved raked windshield.
- Build high-roof blister and rear 50/50 barn doors.
- Create steel van wheels with 6 cooling holes, center hub, and radial rubber tires.
- Apply PBR materials and high-visibility decals.
- Inspect 4-view contact sheet to verify zero boxiness.

---

### Phase 4: Beauty Rendering, Verification & Export Pipeline (Subsequent Phase)

- Run final quality verification checklist.
- Set up AgX camera framing and high-dynamic range studio lights.
- Export to GLB / FBX with bottom-centered pivot and applied transforms.
