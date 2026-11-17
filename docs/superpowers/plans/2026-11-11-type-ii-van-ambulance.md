# Type II Sprinter Van Ambulance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Procedurally build a complete, AAA game-ready Type II Mercedes-Benz Sprinter Van Ambulance inside Blender 5.2.2 LTS matching the 6-view reference blueprint (`media_1794403034040_0d58cb01.jpg`), fully utilizing the upgraded `bmesh_toolkit` and `vehicle_thinking` modules.

**Architecture:** The vehicle is generated using the 90/10 Hybrid Pipeline (`bmesh` + `bpy.data` in memory, sub-second execution) partitioned into 6 coordinate-aligned modular assemblies plus undercarriage running gear and studio staging. Rims are instanced from a single master mesh, modifiers (`Auto_Bevel` + `Auto_WeightedNormal`) handle automotive highlights, and graphics are modeled as 1mm offset procedural 3D geometric decals.

**Tech Stack:** Blender 5.2.2 LTS, Python 3.11+, `bmesh`, `mathutils`, `numpy`, Blender MCP Server (Port 9876).

**Spec:** `docs/superpowers/specs/2026-11-11-type-ii-van-ambulance-design.md`

## Global Constraints
- Overall Length: $5.92 \pm 0.05$ m, Overall Width: $2.05 \pm 0.04$ m (body) / $2.42$ m (with mirrors), Height: $2.75 \pm 0.05$ m.
- Wheelbase: $3.66$ m (Front axle at $Y = +1.73$ m, Rear axle at $Y = -1.93$ m).
- Ground Clearance: $0.20$ m; Tire Radius: $0.375$ m (17-inch rim $R = 0.215$ m).
- 100% in-memory procedural generation via `bmesh` (`bmesh.new()`, `bm.to_mesh()`) without blocking UI operators.
- Shading: Principled BSDF with AgX color management; automotive modifier stack with angle-based bevel and weighted normals.

## Review Focus
1. Wheel Arch Clearance: Ensure wheel well cutouts maintain $\ge 0.06$ m radial clearance around tires so tires never intersect bodywork.
2. Decal Coplanar Z-Fighting: Ensure all 3D livery decals are offset by exactly $+1.0$ mm along panel normals.
3. Bottom View Mechanical Realism: Ensure exhaust pipe routes into center cylindrical muffler and exits curbside, and rear axle tube connects to differential.
4. Glass Transparency vs. Interior Masking: Ensure front windshield has realistic low-poly cab interior depth while rear patient compartment glass is opaque.
5. Coordinate Alignment: All modular assemblies must share the same world origin `(0, 0, 0)` so they snap together seamlessly without floating gaps.

---

### Task 1: Environment & Shader Library Setup

**Files:**
- Create: `scripts/pipeline/setup_van_materials.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: None (initial setup).
- Produces: 13 PBR Materials registered in `bpy.data.materials`:
  `VAN_Paint_White`, `VAN_Cladding_Grey`, `VAN_Glass_Tinted`, `VAN_Strobe_Red`, `VAN_Strobe_Blue`, `VAN_Strobe_Amber`, `VAN_Headlight_LED`, `VAN_Taillight_Red`, `VAN_Wheel_Steel`, `VAN_Tire_Rubber`, `VAN_Decal_Red`, `VAN_Decal_Blue`, `VAN_Decal_White`.

- [ ] **Step 1: Write the verification test script for materials**
Verify that script queries `bpy.data.materials` for all 13 required names and asserts their Principled BSDF inputs (Base Color, Metallic, Roughness, Coat Weight, Emission Strength).

- [ ] **Step 2: Run verification test to confirm materials do not yet exist**
Run via `execute_blender_code`. Expected: Returns missing material count.

- [ ] **Step 3: Implement `setup_van_materials()` in Blender memory**
Create all 13 PBR materials using nodes:
- `VAN_Paint_White`: Base Color (0.95, 0.95, 0.95), Roughness 0.15, Coat Weight 1.0, Coat Roughness 0.03.
- `VAN_Cladding_Grey`: Base Color (0.08, 0.08, 0.09), Roughness 0.85, Metallic 0.0.
- `VAN_Glass_Tinted`: Base Color (0.02, 0.03, 0.04), Roughness 0.05, Transmission 0.85 (or IOR 1.52).
- `VAN_Strobe_Red`: Emission Color (1.0, 0.02, 0.02), Strength 30.0.
- `VAN_Strobe_Blue`: Emission Color (0.02, 0.25, 1.0), Strength 30.0.
- `VAN_Strobe_Amber`: Emission Color (1.0, 0.45, 0.02), Strength 25.0.
- `VAN_Headlight_LED`: Emission Color (0.95, 0.98, 1.0), Strength 40.0.
- `VAN_Wheel_Steel`: Base Color (0.75, 0.77, 0.80), Metallic 0.85, Roughness 0.25.
- `VAN_Tire_Rubber`: Base Color (0.03, 0.03, 0.035), Roughness 0.88, Metallic 0.0.
- `VAN_Decal_Red`: Base Color (0.85, 0.04, 0.04), Roughness 0.30.
- `VAN_Decal_Blue`: Base Color (0.02, 0.18, 0.75), Roughness 0.30.
- `VAN_Decal_White`: Base Color (0.95, 0.95, 0.95), Roughness 0.30.

- [ ] **Step 4: Run verification test to verify all 13 materials pass**
Run via `execute_blender_code`. Expected: `PASS - All 13 materials valid`.

---

### Task 2: `VAN_Chassis_Undercarriage` & Front Cab Interior Blockout

**Files:**
- Create: `scripts/pipeline/build_chassis_and_cab_interior.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `VAN_Cladding_Grey`, `VAN_Wheel_Steel`, `VAN_Tire_Rubber`.
- Produces: `VAN_Chassis_Undercarriage` mesh object and `VAN_Cab_Interior` mesh object.

- [ ] **Step 1: Write test for chassis and interior objects**
Asserts `VAN_Chassis_Undercarriage` exists, bounding box spans $Y = [-2.80, 2.70]$, $Z = [0.18, 0.50]$, contains exhaust system, muffler, and rear axle; and `VAN_Cab_Interior` contains front seats and dashboard.

- [ ] **Step 2: Run test to verify failure**
Expected: Objects not found.

- [ ] **Step 3: Implement procedural chassis & interior generation**
In pure BMesh:
- Dual C-channel chassis rails ($X = \pm 0.48$, $Y = [-2.80, 2.70]$, $Z = 0.32$).
- Crossmembers at front axle, transmission, mid-body, and rear axle.
- Exhaust pipe routing from engine ($Y = 2.20$) into center cylindrical expansion muffler ($Y = -0.40$ to $0.20$, radius $0.12$ m), exiting curbside at $Y = -1.20$.
- Rear drive axle tube ($X = [-0.75, 0.75]$, $Y = -1.93$, $Z = 0.375$) with spherical differential pumpkin.
- Front cab interior: driver and passenger bucket seats with headrests at $Y = 1.05$, sloped dashboard cowl at $Y = 1.60$, steering column and 3-spoke steering wheel.

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - Chassis undercarriage and cab interior built`.

---

### Task 3: `VAN_Body_Shell` (Unibody High-Roof Van Envelope & Roof Ribs)

**Files:**
- Create: `scripts/pipeline/build_body_shell.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `bmesh_toolkit.py` parametric functions, `VAN_Paint_White`.
- Produces: `VAN_Body_Shell` mesh object with modifiers `Auto_Bevel` and `Auto_WeightedNormal`.

- [ ] **Step 1: Write test for body shell geometry**
Asserts `VAN_Body_Shell` exists, dimensions span Length $\approx 5.92$ m, Width $\approx 2.05$ m, Height $\approx 2.65$ m, contains 4 roof corrugation channels, and has `Auto_Bevel` + `Auto_WeightedNormal`.

- [ ] **Step 2: Run test to verify failure**
Expected: `VAN_Body_Shell` not found.

- [ ] **Step 3: Implement procedural unibody high-roof shell**
In pure BMesh:
- Base unibody van envelope ($X = [-1.02, 1.02]$, $Y = [-2.96, 2.96]$, $Z = [0.38, 2.65]$).
- Tumblehome inward tilt ($6.5^\circ$) from waistline ($Z = 1.25$) to roof shoulder ($Z = 2.45$).
- Sloped aerodynamic hood from cowl ($Y = 1.25, Z = 1.20$) to nosecone ($Y = 2.85, Z = 0.92$) with convex curvature sagitta $0.035$ m.
- Aerodynamic high-roof blister over windshield brow ($Y = 1.00$ to $1.40$, $Z = 2.05$ to $2.65$).
- 4 longitudinal roof corrugation channels (stamped sheet metal channels, $0.06$ m wide, $0.02$ m deep) along roof length ($Y = -2.60$ to $0.80$).
- Window frame openings for windshield, cab doors, right sliding door, left window, and rear barn doors.
- Apply `apply_automotive_modifiers(obj, bevel_width=0.008, smooth_angle_deg=35.0)`.

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - VAN_Body_Shell built with clean geometry and modifiers`.

---

### Task 4: `VAN_Cladding_Bumpers` & Wheel Arch Cutouts

**Files:**
- Create: `scripts/pipeline/build_cladding_and_bumpers.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `bmesh_toolkit.py` (`create_wheel_arch`), `VAN_Cladding_Grey`, `VAN_Paint_White`.
- Produces: `VAN_Cladding_Bumpers` mesh object.

- [ ] **Step 1: Write test for cladding and bumpers**
Asserts `VAN_Cladding_Bumpers` exists, spans full vehicle perimeter at $Z = [0.20, 0.58]$, has front bumper with 3-bar grille and fog light bezels, rear step bumper, and 4 wheel arch openings centered at $Y = +1.73$ and $Y = -1.93$ with $R \ge 0.44$ m.

- [ ] **Step 2: Run test to verify failure**
Expected: `VAN_Cladding_Bumpers` not found.

- [ ] **Step 3: Implement procedural cladding and bumpers**
In pure BMesh:
- Dark grey perimeter protective cladding band ($Z = 0.20$ to $0.58$).
- Front bumper ($Y = 2.70$ to $2.96$): integrated 3-bar Mercedes Sprinter grille, lower intake mesh, fog lamp pockets, and license plate holder.
- Rear bumper ($Y = -2.96$ to -3.12, $Z = 0.28$ to $0.52$): non-slip step bumper with corner reliefs.
- 4 molded circular wheel arches with flared lips using `calculate_wheel_arch_geometry` at $(X = \pm 1.025, Y = 1.73, Z = 0.375)$ and $(X = \pm 1.025, Y = -1.93, Z = 0.375)$ with $R = 0.44$ m.
- Apply `apply_automotive_modifiers`.

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - VAN_Cladding_Bumpers built`.

---

### Task 5: `VAN_Glass_and_Doors`

**Files:**
- Create: `scripts/pipeline/build_glass_and_doors.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `bmesh_toolkit.py` (`create_curved_windshield`), `VAN_Glass_Tinted`, `VAN_Cladding_Grey`, `VAN_Strobe_Amber`.
- Produces: `VAN_Glass_and_Doors` mesh object.

- [ ] **Step 1: Write test for glass and hardware**
Asserts `VAN_Glass_and_Doors` exists, contains compound curved windshield, cab door windows, sliding door window, rear barn door windows, dual towing mirrors with amber indicators, and wiper blades.

- [ ] **Step 2: Run test to verify failure**
Expected: `VAN_Glass_and_Doors` not found.

- [ ] **Step 3: Implement procedural glass, mirrors & door hardware**
In pure BMesh:
- Front compound curved windshield ($bx=1.85, tx=1.65, sagitta=0.075$) with black frit perimeter.
- Left and right front cab door windows with rubber weatherstripping.
- Right sliding side door flush window and left side large paramedic view window.
- Dual 50/50 rear cargo barn door windows.
- Dual vertical commercial towing mirrors at $(X = \pm 1.18, Y = 1.35, Z = 1.35)$ with upper flat glass, lower blind-spot glass, and forward amber LED indicator strip.
- Horizontal resting wiper blades and articulated black arms on cowl.
- Flush black door handles on cab doors, sliding door, and rear door.

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - VAN_Glass_and_Doors built`.

---

### Task 6: `VAN_Wheels_and_Suspension` (Shared Mesh Instancing)

**Files:**
- Create: `scripts/pipeline/build_van_wheels.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `VAN_Wheel_Steel`, `VAN_Tire_Rubber`, `VAN_Cladding_Grey`.
- Produces: `VAN_Master_Wheel` mesh data; instanced to 4 objects: `VAN_Wheel_FL`, `VAN_Wheel_FR`, `VAN_Wheel_RL`, `VAN_Wheel_RR`.

- [ ] **Step 1: Write test for wheels and instancing**
Asserts `VAN_Master_Wheel` mesh has 12 circular cooling vents, tire radius $= 0.375$ m, rim radius $= 0.215$ m, and 4 objects share `obj.data == master_mesh`.

- [ ] **Step 2: Run test to verify failure**
Expected: Objects not found.

- [ ] **Step 3: Implement procedural commercial van wheel and instances**
In pure BMesh:
- Radial road tire: outer radius $0.375$ m, inner bead $0.215$ m, width $0.235$ m, smooth shoulder and sidewall curvature.
- 17-inch commercial steel rim: 12 circular perimeter cooling vents, center axle hub with 6 lug nuts.
- Ventilated steel brake disc rotor and front brake caliper.
- Instance `VAN_Master_Wheel` into 4 objects:
  - `VAN_Wheel_FL` at $(+0.86, +1.73, 0.375)$
  - `VAN_Wheel_FR` at $(-0.86, +1.73, 0.375)$, rot $Z = 180^\circ$
  - `VAN_Wheel_RL` at $(+0.865, -1.93, 0.375)$
  - `VAN_Wheel_RR` at $(-0.865, -1.93, 0.375)$, rot $Z = 180^\circ$

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - Master wheel and 4 instances verified`.

---

### Task 7: `VAN_Emergency_System`

**Files:**
- Create: `scripts/pipeline/build_emergency_system.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `VAN_Strobe_Red`, `VAN_Strobe_Blue`, `VAN_Headlight_LED`, `VAN_Taillight_Red`, `VAN_Paint_White`, `VAN_Cladding_Grey`.
- Produces: `VAN_Emergency_System` mesh object.

- [ ] **Step 1: Write test for emergency lighting**
Asserts `VAN_Emergency_System` exists, contains front rooftop lightbar (Red left, Blue right), rear rooftop lightbar (Red left, Blue right), 4 roof corner strobe pods, rooftop AC unit, dual projector headlights, and rear taillight stacks.

- [ ] **Step 2: Run test to verify failure**
Expected: `VAN_Emergency_System` not found.

- [ ] **Step 3: Implement procedural emergency lighting & roof equipment**
In pure BMesh:
- Front rooftop low-profile aerodynamic lightbar ($Y = 1.18$ to $1.32$, $Z = 2.66$ to $2.75$): clear aero polycarbonate dome, Driver Red LED cluster, Passenger Blue LED cluster.
- Rear rooftop matching lightbar ($Y = -2.94$ to $-2.82$, $Z = 2.66$ to $2.75$): Left Red / Right Blue.
- 4 red perimeter strobe pods mounted on upper roof corners ($Y = 0.95$ and $Y = -2.85$, $X = \pm 1.01$, $Z = 2.58$).
- Low-profile rooftop AC/ventilation unit ($Y = -0.45$ to $0.25$, $Z = 2.65$ to $2.78$) with dual circular fan grilles.
- Front dual Xenon projector headlight capsules with chrome bowls and LED daytime running halos.
- High-mounted vertical rear taillight stacks on D-pillars ($Z = 0.95$ to $1.75$) with red brake, amber turn, and white reverse segments.

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - VAN_Emergency_System verified`.

---

### Task 8: `VAN_Livery_Decals` (3D Vector Geometry)

**Files:**
- Create: `scripts/pipeline/build_livery_decals.py`
- Test: Blender MCP `execute_blender_code`

**Interfaces:**
- Consumes: `VAN_Decal_Red`, `VAN_Decal_Blue`, `VAN_Decal_White`.
- Produces: `VAN_Livery_Decals` mesh object.

- [ ] **Step 1: Write test for livery geometry**
Asserts `VAN_Livery_Decals` exists, contains red stepped waistline stripe, 3D "AMBULANCE" decals on hood/sides/rear, Star of Life emblems, and rear diagonal chevrons; all offset by $1.0$ mm from body panels.

- [ ] **Step 2: Run test to verify failure**
Expected: `VAN_Livery_Decals` not found.

- [ ] **Step 3: Implement procedural 3D geometric decals**
In pure BMesh:
- Red waistline stripe ($Z = 1.05$ to $1.15$): continuous band along cab doors and sides, transitioning at the rear quarter panel into the 3-step digital chevron pattern seen in the blueprint.
- Bold red sans-serif `"AMBULANCE"` 3D lettering:
  - Hood: Angled text along hood slope ($Y = 2.25, Z = 1.08$).
  - Left & Right sides: Centered below windows ($Y = -0.10, Z = 0.95$).
  - Rear: Across upper barn doors ($Y = -2.965, Z = 1.55$).
- 6-pointed Blue Star of Life with white Rod of Asclepius:
  - Large on left and right rear quarter panels ($Y = -1.25, Z = 1.45$).
  - Medium on left and right rear barn door windows ($Y = -2.965, Z = 1.95$).
  - Front roof brow centered above windshield ($Y = 1.40, Z = 2.45$).
- Lower rear door alternating 45° Red and White reflective safety hazard chevrons ($Z = 0.42$ to $0.88$).

- [ ] **Step 4: Run test to verify pass**
Expected: `PASS - VAN_Livery_Decals verified`.

---

### Task 9: Studio Staging, 6-View Orthographic Verification & Save

**Files:**
- Create: `scripts/pipeline/stage_and_verify_views.py`
- Output: `Type_II_Sprinter_Ambulance.blend`
- Test: `look` and `gbuffer_quad_capture` tools

**Interfaces:**
- Consumes: All 6 vehicle modular objects + chassis + wheels.
- Produces: Studio floor, lighting, camera rigs for 6 orthographic views and beauty shot; saved `.blend` file.

- [ ] **Step 1: Write test for complete scene assembly**
Asserts all vehicle objects are present, total triangle budget is within $100\text{k} - 160\text{k}$ tris, no overlapping vertices, bottom pivot sits at $Z = 0.0$.

- [ ] **Step 2: Setup studio turntable, lighting & cameras**
- 36m circular dark reflective asphalt turntable floor (`M_Showroom_Floor`).
- 3-point studio lighting (`LGT_Key_Main` 2600W, `LGT_Fill_Soft` 1100W, `LGT_Rim_Back` 3200W).
- Front 3/4 beauty camera positioned matching the blueprint hero view.
- 6 orthographic camera markers (Top, Bottom, Front, Rear, Left, Right).

- [ ] **Step 3: Capture viewport renders and verify against reference blueprint**
Execute `look` and compare against `media_1794403034040_0d58cb01.jpg`.

- [ ] **Step 4: Save final scene to disk**
Save as `c:\Users\Rahul\OneDrive\Desktop\Blender MCP\Type_II_Sprinter_Ambulance.blend`.

- [ ] **Step 5: Verify save success and report completion**
Confirm file exists on disk and is non-empty.