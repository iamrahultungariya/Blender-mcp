# Apex GT-R Concept Supercar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Procedurally generate a high-fidelity, game-ready Apex GT-R Concept Supercar in Blender matching the user's reference blueprint, decomposed into 12 separate component assemblies with PBR materials and strictly adhering to a ~30,000 polygon budget.

**Architecture:** Built using the in-memory 90/10 Hybrid Procedural Pipeline (`bmesh` + `bpy.data`), leveraging `blender_mcp.bmesh_toolkit` for parametric geometry, `blender_mcp.vehicle_thinking` for supercar rake angles and proportions, and `blender_mcp.materials_preset` for 8 PBR shaders. Wheels use shared mesh instancing to maximize geometric detail while staying strictly within the 30k poly budget.

**Tech Stack:** Blender 5.2.2 LTS C-API (`bpy`, `bmesh`, `mathutils`), Python 3.10+, numpy, FastMCP via live Blender MCP server.

**Spec:** [docs/superpowers/specs/2026-11-12-apex-gtr-design.md](file:///c:/Users/Rahul/OneDrive/Desktop/Blender%20MCP/docs/superpowers/specs/2026-11-12-apex-gtr-design.md)

## Global Constraints

- **Exact Envelope:** Length $4610\text{ mm}$ ($Y: -2.305\text{ to } +2.305\text{ m}$), Width $1870\text{ mm}$ ($X: \pm 0.935\text{ m}$), Height $1180\text{ mm}$ ($Z: 0\text{ to } 1.18\text{ m}$), Wheelbase $2700\text{ mm}$ (Axles at $Y = \pm 1.350\text{ m}$).
- **Polygon Target:** Total scene polygon budget must be between $27,000$ and $31,000$ quads/tris (nominally ~29,500).
- **Separated Components:** 12 distinct modular assemblies organized cleanly in the `Apex_GTR_Concept` collection.
- **Normal Standards:** No deprecated `use_auto_smooth`; all panels use `Bevel` (2 segments, profile 0.5, harden normals) + `WeightedNormal` (keep sharp) for razor-sharp automotive reflections.
- **Zero UI Freeze:** 100% geometry operations in C RAM via `bmesh` and `bpy.data`.

## Review Focus

1. **Wheel Arch Clearance & Flared Stance:** Front and rear wheels must sit flush inside the flared widebody arches without clipping through fenders during turning or compression.
2. **Hood Vents & Grille Depth:** Vents and grilles must have 3D recessed depth with dark backing geometry, never flat painted surfaces.
3. **Splitter & Wing Aerodynamics:** Front splitter canards, side skirts, and rear diffuser fins must exhibit razor-sharp beveled edges with the distinctive crimson red pinstripe accent.
4. **Shared Wheel Instancing:** 4 wheels (FL, FR, RL, RR) must share master mesh data (`obj.data = master_wheel.data`) to conserve polygon memory.
5. **Headlight & Taillight Internal Detail:** Dual projector lens housings and angular LED DRL ribbons must be visible through the front clear lenses.

---

### Phase 1: Foundation, Coordinate Grid & PBR Material Vault

#### Task 1: Scene Hierarchy & Dimension Envelope Calibration

**Files:**
- Create: `scripts/generate_apex_gtr.py`
- Test: `tests/test_apex_gtr_envelope.py`

**Interfaces:**
- Produces: `setup_scene_hierarchy() -> dict[str, bpy.types.Collection]`
- Produces: `verify_bounding_box(obj, expected_min, expected_max, tolerance=0.02)`

- [x] **Step 1: Write test verifying dimension envelope and collection structure**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement scene setup and collection hierarchy creation in `scripts/generate_apex_gtr.py`**
- [x] **Step 4: Execute in live Blender and verify collection hierarchy**
- [x] **Step 5: Commit changes**

---

#### Task 2: PBR Automotive Shader Vault Setup

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Test: `tests/test_apex_gtr_materials.py`

**Interfaces:**
- Produces: `setup_gtr_materials() -> dict[str, bpy.types.Material]`
  - `MAT_GTR_Paint_Gunmetal`: Dark Metallic Grey (Base Color `(0.04, 0.04, 0.05, 1.0)`, Metallic `0.92`, Roughness `0.22`, Clearcoat `1.0`, Clearcoat Roughness `0.03`)
  - `MAT_GTR_Carbon_Satin`: Satin Carbon Fiber (Base Color `(0.02, 0.02, 0.02, 1.0)`, Roughness `0.35`, Specular `0.6`)
  - `MAT_GTR_Crimson_Accent`: Vibrant Aero Red (Base Color `(0.85, 0.02, 0.03, 1.0)`, Roughness `0.25`, Clearcoat `0.8`)
  - `MAT_GTR_Automotive_Glass`: Tinted Glass (Transmission `1.0`, IOR `1.52`, Roughness `0.02`, Base Color `(0.1, 0.12, 0.14, 1.0)`)
  - `MAT_GTR_Tire_Rubber`: Radial Rubber (Base Color `(0.03, 0.03, 0.03, 1.0)`, Roughness `0.78`)
  - `MAT_GTR_Brake_Steel`: Cross-drilled steel (Metallic `0.95`, Roughness `0.3`)
  - `MAT_GTR_Caliper_Red`: Glossy Red Enamel (Base Color `(0.9, 0.01, 0.01, 1.0)`, Roughness `0.15`, Clearcoat `1.0`)
  - `MAT_GTR_LED_Emissive`: High-intensity LED (Emission Color `(1.0, 1.0, 1.0)`, Strength `15.0`)
  - `MAT_GTR_Tail_Emissive`: Crimson Ribbon LED (Emission Color `(1.0, 0.02, 0.02)`, Strength `12.0`)

- [x] **Step 1: Write test verifying all 9 materials exist and have valid shader nodes**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `setup_gtr_materials()` in `scripts/generate_apex_gtr.py`**
- [x] **Step 4: Execute in live Blender and verify material nodes**
- [x] **Step 5: Commit changes**

---

### Phase 2: Primary Unibody Structure & Aerodynamic Cabin

#### Task 3: Unibody Cabin & Roof Shell (`GTR_Body_Shell`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Body_Shell` (~6,000 polygons)

**Interfaces:**
- Produces: `build_body_shell(materials: dict) -> bpy.types.Object`
- Coordinates:
  - Roof Peak: $Z = 1.180\text{ m}$, spanning $Y = -0.30\text{ m}$ to $+0.35\text{ m}$
  - A-Pillar: $65^\circ$ slope down to cowl at $Y = +0.88\text{ m}, Z = 0.78\text{ m}$
  - B/C-Pillars & Fastback Decklid: sloping down to rear ducktail at $Y = -1.95\text{ m}, Z = 0.82\text{ m}$
  - Side Scoops: Sculpted intake recesses ahead of rear wheels ($Y = -0.4\text{ to } -0.9\text{ m}$)

- [ ] **Step 1: Write verification test for `GTR_Body_Shell` geometry and vertex bounds**
- [ ] **Step 2: Implement BMesh cross-sectional parametric generation for body unibody**
- [ ] **Step 3: Execute in live Blender and verify quad topology and smooth curves**
- [ ] **Step 4: Commit changes**

---

#### Task 4: Flared Widebody Fenders (`GTR_Fenders_Widebody`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Fenders_Widebody` (~3,000 polygons)

**Interfaces:**
- Produces: `build_widebody_fenders(materials: dict) -> bpy.types.Object`
- Dimensions:
  - Front arch center: $Y = +1.350\text{ m}, Z = 0.340\text{ m}$, Radius $0.380\text{ m}$, Width flare extending to $X = \pm 0.985\text{ m}$
  - Rear arch center: $Y = -1.350\text{ m}, Z = 0.340\text{ m}$, Radius $0.390\text{ m}$, Width flare extending to $X = \pm 0.995\text{ m}$
  - Aero cutouts: Vertical air pressure relief louvers/extractors behind front wheel wells

- [ ] **Step 1: Write test verifying wheel arch radii and clearance**
- [ ] **Step 2: Implement flared fender BMesh generator with wheel arch cutouts**
- [ ] **Step 3: Execute in live Blender and inspect fender curvature**
- [ ] **Step 4: Commit changes**

---

#### Task 5: Flush Automotive Glass Canopy (`GTR_Glass_Canopy`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Glass_Canopy` (~1,500 polygons)

**Interfaces:**
- Produces: `build_glass_canopy(materials: dict) -> bpy.types.Object`
- Components:
  - Curved Front Windshield: Sagitta curvature $0.06\text{ m}$, rake $65^\circ$, black ceramic border frit
  - Frameless Side Quarter Glass: Sleek low aerodynamic profile
  - Fastback Rear Hatch: Sloped rear window with integrated defroster lines

- [ ] **Step 1: Write test verifying glass canopy alignment to body pillars**
- [ ] **Step 2: Implement glass canopy BMesh generator with glass and black frit materials**
- [ ] **Step 3: Execute in live Blender and verify optical transparency and fit**
- [ ] **Step 4: Commit changes**

---

### Phase 3: Front & Rear Aerodynamic Fascia Assemblies

#### Task 6: Front Bumper, Grille & Low Splitter (`GTR_Front_Bumper_Splitter`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Front_Bumper_Splitter` (~3,500 polygons)

**Interfaces:**
- Produces: `build_front_bumper_splitter(materials: dict) -> bpy.types.Object`
- Components:
  - Central hexagonal GT-R intake mouth ($Y = +2.15\text{ to } +2.25\text{ m}$)
  - Dual outer brake cooling ducts with aerodynamic vanes
  - Ground-scraping front splitter blade ($Z = 0.05\text{ m}$) extending to $Y = +2.305\text{ m}$
  - Dual aerodynamic canards / dive planes on outer bumper corners
  - Continuous lower crimson red pinstripe accent

- [ ] **Step 1: Write test verifying front splitter extension and ground clearance**
- [ ] **Step 2: Implement BMesh front bumper and splitter with carbon and red accent materials**
- [ ] **Step 3: Execute in live Blender and verify aggressive front fascia**
- [ ] **Step 4: Commit changes**

---

#### Task 7: Sculpted Vented Hood (`GTR_Hood`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Hood` (~2,000 polygons)

**Interfaces:**
- Produces: `build_hood(materials: dict) -> bpy.types.Object`
- Features:
  - Low-rake hood slope ($14^\circ$ rake, $Y = +0.88\text{ to } +2.15\text{ m}$)
  - Dual central power bulge crease lines
  - Recessed twin aero heat extraction vents with dark mesh backing
  - Front Apex emblem recess

- [ ] **Step 1: Write test verifying hood shutline alignment with fenders and bumper**
- [ ] **Step 2: Implement sculpted hood BMesh generator with recessed extraction ducts**
- [ ] **Step 3: Execute in live Blender and verify hood creases**
- [ ] **Step 4: Commit changes**

---

#### Task 8: Side Skirts & Ground Effects (`GTR_Side_Skirts`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Side_Skirts` (~1,500 polygons)

**Interfaces:**
- Produces: `build_side_skirts(materials: dict) -> bpy.types.Object`
- Features:
  - Low ground-effect aero extensions ($Z = 0.06\text{ m}$) spanning $Y = -0.95\text{ to } +0.95\text{ m}$
  - Rear brake duct inlet scoop
  - Aerodynamic vertical end flick ahead of rear wheel arch
  - Crimson red pinstripe along lower edge

- [ ] **Step 1: Write test verifying skirt alignment between front and rear wheel arches**
- [ ] **Step 2: Implement side skirts BMesh generator with carbon fiber and red accent**
- [ ] **Step 3: Execute in live Blender and inspect stance**
- [ ] **Step 4: Commit changes**

---

#### Task 9: Rear Diffuser & Quad Titanium Exhaust (`GTR_Rear_Diffuser_Exhaust`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Rear_Diffuser_Exhaust` (~3,000 polygons)

**Interfaces:**
- Produces: `build_rear_diffuser_exhaust(materials: dict) -> bpy.types.Object`
- Features:
  - Rear bumper valence spanning $Y = -2.10\text{ to } -2.305\text{ m}$
  - Massive underbody aerodynamic diffuser with 6 vertical flow strakes
  - Central F1-style rectangular LED rain / fog safety light
  - Quad round titanium exhaust tips ($2\times$ left, $2\times$ right) with heat-treated blue/gold rim
  - Lower diffuser crimson red accent outline

- [ ] **Step 1: Write test verifying diffuser fin count (6) and exhaust tip positions**
- [ ] **Step 2: Implement BMesh diffuser, exhaust tubes, and rain light**
- [ ] **Step 3: Execute in live Blender and inspect rear aerodynamic tunnel**
- [ ] **Step 4: Commit changes**

---

#### Task 10: GT High-Downforce Rear Wing (`GTR_Rear_Wing`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Rear_Wing` (~1,500 polygons)

**Interfaces:**
- Produces: `build_rear_wing(materials: dict) -> bpy.types.Object`
- Features:
  - Dual swan-neck upright stanchions mounted to rear decklid ($Y = -1.85\text{ m}, X = \pm 0.45\text{ m}, Z = 0.85\text{ to } 1.05\text{ m}$)
  - Cambered high-downforce airfoil blade spanning width $1.650\text{ m}$ at $Z = 1.05\text{ m}$
  - Large vertical aerodynamic endplates finished in vibrant Crimson Red

- [ ] **Step 1: Write test verifying rear wing height and width limits**
- [ ] **Step 2: Implement BMesh rear wing generator with swan-neck pylons and red endplates**
- [ ] **Step 3: Execute in live Blender and verify wing stance**
- [ ] **Step 4: Commit changes**

---

### Phase 4: High-Detail Subsystems (Wheels, Lights, Mirrors)

#### Task 11: Master Wheel Assembly (`GTR_Wheel_Assembly`) & 4-Corner Instancing

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Wheel_Master` (~4,000 polygons in memory, instanced 4x)

**Interfaces:**
- Produces: `build_master_wheel(materials: dict) -> bpy.types.Object`
- Produces: `instance_wheels(master_wheel_obj, positions: list[tuple[str, mathutils.Vector, float]]) -> list[bpy.types.Object]`
- Components:
  - Forged Lightweight Rim: 10-spoke GT racing design ($R = 0.260\text{ m}$, satin gunmetal/black)
  - Performance Radial Tire: Outer $R = 0.340\text{ m}$, width $0.280\text{ m}$ (front) / $0.320\text{ m}$ (rear), directional tread grooves
  - Carbon-Ceramic Brake Rotor: Cross-drilled ventilation holes, center hub
  - 6-Piston High-Performance Brake Caliper: Vibrant Brembo-style red enamel with white lettering
- Positions:
  - Front Left: $(-0.880, +1.350, 0.340)$
  - Front Right: $(+0.880, +1.350, 0.340)$
  - Rear Left: $(-0.890, -1.350, 0.340)$
  - Rear Right: $(+0.890, -1.350, 0.340)$

- [ ] **Step 1: Write test verifying wheel instancing (`obj.data` shared across all 4 wheel objects)**
- [ ] **Step 2: Implement detailed master wheel assembly BMesh generator**
- [ ] **Step 3: Instance master wheel to FL, FR, RL, RR with proper symmetry and brake orientation**
- [ ] **Step 4: Execute in live Blender and verify wheel fitment and stance**
- [ ] **Step 5: Commit changes**

---

#### Task 12: Precision Lighting Assemblies (`GTR_Headlights` & `GTR_Tail_Lights`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Headlights` (~1,500 polys) & `GTR_Tail_Lights` (~1,200 polys)

**Interfaces:**
- Produces: `build_headlights(materials: dict) -> bpy.types.Object`
- Produces: `build_tail_lights(materials: dict) -> bpy.types.Object`
- Features:
  - Headlights: Smoked housing, dual projector LED glass lenses, sharp angled Z-pattern LED daytime running light ribbons (Emissive White $15.0$)
  - Tail Lights: Sculpted angular ribbon LED bar spanning rear deck with deep red luminescence (Emissive Red $12.0$) and smoked lens cover

- [ ] **Step 1: Write test verifying lighting positions and emission materials**
- [ ] **Step 2: Implement BMesh headlights and taillights with lenses and reflectors**
- [ ] **Step 3: Execute in live Blender and verify light guides**
- [ ] **Step 4: Commit changes**

---

#### Task 13: Aerodynamic Wing Mirrors (`GTR_Aero_Mirrors`)

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Target: `GTR_Aero_Mirrors` (~800 polygons)

**Interfaces:**
- Produces: `build_aero_mirrors(materials: dict) -> bpy.types.Object`
- Features:
  - Slender aerodynamic support stalks mounting to door beltline ($Y = +0.72\text{ m}, X = \pm 0.88\text{ m}, Z = 0.74\text{ m}$)
  - Sculpted aero mirror caps with subtle indicator strip
  - Reflective chrome mirror glass facing rearward

- [ ] **Step 1: Write test verifying mirror positions and symmetry**
- [ ] **Step 2: Implement aerodynamic mirror BMesh generator**
- [ ] **Step 3: Execute in live Blender and verify placement**
- [ ] **Step 4: Commit changes**

---

### Phase 5: Topology Audit, Normal Polish & Asset Inspection

#### Task 14: Automated Automotive Modifier Stack & Normal Hardening

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Test: `tests/test_apex_gtr_modifiers.py`

**Interfaces:**
- Produces: `apply_automotive_finishing(objects: list[bpy.types.Object])`
- Modifiers applied per panel:
  - `Auto_Bevel`: Width `0.006\text{ m}` ($6\text{ mm}$), Segments `2`, Profile `0.50`, Harden Normals `True`
  - `Auto_WeightedNormal`: Keep Sharp `True`, Weight `50`
  - Smooth Shading applied to all polygon faces

- [ ] **Step 1: Write test verifying all 12 component objects have Bevel + WeightedNormal modifiers**
- [ ] **Step 2: Implement modifier assignment loop in `scripts/generate_apex_gtr.py`**
- [ ] **Step 3: Execute in live Blender and verify reflection highlights across panels**
- [ ] **Step 4: Commit changes**

---

#### Task 15: Polygon Budget Audit & Multi-Angle Contact Sheet Inspection

**Files:**
- Modify: `scripts/generate_apex_gtr.py`
- Output: `assets/renders/Apex_GTR_Contact_Sheet.png`

**Interfaces:**
- Produces: `audit_polygon_budget() -> dict[str, int]` (verifies total scene faces $\le 30,000$)
- Produces: `render_4_angle_contact_sheet() -> str` (calls `inspect_asset` / 4-angle viewport capture: Front, Right Side, Top, Three-Quarter Hero)

- [ ] **Step 1: Execute scripted polygon audit in live Blender and print per-component counts**
- [ ] **Step 2: Verify total count is between $27,000$ and $31,000$ quads/tris**
- [ ] **Step 3: Capture multi-angle contact sheet and inspect visual fidelity against blueprint**
- [ ] **Step 4: Commit changes**

---

#### Task 16: Blend & Production GLB Export

**Files:**
- Output: `Apex_GTR_Concept.blend`
- Output: `Apex_GTR_Concept.glb`

**Interfaces:**
- Produces: Native `.blend` saved with packed textures and organized collection hierarchy
- Produces: Production `.glb` export with materials, vertex normals, and instanced wheels

- [ ] **Step 1: Save `Apex_GTR_Concept.blend` via `bpy.ops.wm.save_as_mainfile`**
- [ ] **Step 2: Export `Apex_GTR_Concept.glb` via `bpy.ops.export_scene.gltf` with format `GLB`**
- [ ] **Step 3: Verify exported files exist and are non-empty on disk**
- [ ] **Step 4: Commit final deliverables**
