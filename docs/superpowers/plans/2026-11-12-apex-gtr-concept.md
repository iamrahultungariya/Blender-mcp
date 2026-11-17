# Apex GT-R Concept Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a production-grade 3D model of the Apex GT-R Concept matching reference orthographics and specifications from scratch in Blender 4.x within a ~600k polygon budget, utilizing the 90/10 bmesh procedural pipeline.

**Architecture:** Pure Zone A (`bmesh` + `bpy.data`) pipeline. All parts generated as distinct procedural meshes in discrete collections. Mirrors and modifiers evaluated cleanly. Limo blackout glass (0% transmission, pure dark gloss) ensures zero interior geometry or reflections needed, dedicating 100% of polycount to exterior aerodynamics, bodywork, wheels, and lighting details.

**Tech Stack:** Blender 4.x Python API (`bmesh`, `bpy.data`, `mathutils`), Blender MCP.

---

## Global Constraints
- Target Polygons: ~600,000 max.
- Dimensions: Length = 4610 mm, Width = 1870 mm, Height = 1180 mm, Wheelbase = 2700 mm.
- Ground Clearance: 60 mm (track stance).
- Interior: 100% excluded / blackout limo tint (Transmission = 0.0, Roughness = 0.03).
- Pipeline Rule: 90% execution in `bmesh` memory; `bpy.ops` strictly limited to I/O and render triggers.

---

## Part & Polycount Allocation (Updated)

| Task / Part | Poly Budget | Description & Key Features |
|---|---|---|
| **Phase 1: Scene & Foundation** | ~1k | Metric units, Collections, PBR Master Shaders, Bounding Box Cage (Done) |
| **Phase 2: Main Body Shell** | ~140k | Aerodynamic hood-to-roof curvature, cabin pillars, side door scallops, wheel arches |
| **Phase 3: Front Aero & Bumper** | ~90k | Aggressive front grill, multi-tier front carbon splitter, side canards |
| **Phase 4: Flared Widebody Fenders** | ~60k | 25mm flared arches (front & rear) with cooling vents |
| **Phase 5: Rear Diffuser & Wing** | ~90k | Swan-neck carbon GT wing with endplates + multi-channel race diffuser |
| **Phase 6: Wheel Assembly (x4)** | ~120k | Twin-spoke forged rims (x4), grooved track tires, slotted rotors, red calipers |
| **Phase 7: Aerodynamic Skirts & Mirrors** | ~40k | Stepped side skirts, aerodynamic side mirrors with integrated indicators |
| **Phase 8: Lighting, Badging & Accents** | ~50k | Multi-element LED DRLs, rear lightbar, GT-R badges, red pinstripes |
| **Phase 9: Final Assembly & Presentation** | - | Cycles/Eevee LookDev, studio lighting & turntable setup |

---

## Tasks Breakdown

### Task 1: Scene Setup, Calibration & Shaders (Phase 1)
- [x] Configure metric units (1.0 scale).
- [x] Create 6 core scene collections (`00_Guides_References`, `01_Body_Chassis`, `02_Aero_Canards_Diffuser`, `03_Wheels_Assembly`, `04_Blackout_Glass`, `05_Lighting_FX`).
- [x] Create PBR Master materials (`Mat_Apex_BlackoutGlass`, `Mat_Apex_GunmetalPaint`, `Mat_Apex_CarbonAero`, `Mat_Apex_RedTrim`, `Mat_Apex_TireRubber`, `Mat_Apex_RimAlloy`, `Mat_Apex_BrakeSteel`, `Mat_Apex_BrakeCaliperRed`, `Mat_Apex_LED_White`, `Mat_Apex_LED_Red`).
- [x] Generate exact 4.61m x 1.87m x 1.18m dimensional wireframe guides and 2.70m wheelbase axle guides in `bmesh`.

### Task 2: Main Body Shell Generation (Phase 2)
- [x] Construct the longitudinal profile slices (front nose, hood slope, A-pillar, roofline, fastback C-pillar, rear deck).
- [x] Loft quad surfaces along X-symmetry.
- [x] Form door recesses and side intakes.
- [x] Assign `Mat_Apex_GunmetalPaint` and separate window cutouts to `Mat_Apex_BlackoutGlass`.
- [x] Add Mirror Modifier (X-clipping) and Subdivision Surface modifier (Level 2 evaluated to 21,600 quads).

### Task 3: Front Bumper & Splitter Assembly (Phase 3)
- [x] Build trapezoidal center radiator grille with honeycomb depth.
- [x] Create carbon fiber multi-tier splitter with red accent leading edge.
- [x] Extrude side air ducts with aerodynamic dive planes / canards.
- [x] Model dedicated Hood with dual recessed heat extraction vents and angled carbon louvers.
- [x] Apply X-Mirror and Subsurf modifiers across both components.

### Task 4: Widebody Flared Fenders (Phase 4)
- [x] Form front wheel arch flares extending beyond 1.87m boundary with carbon cooling louvers.
- [x] Form muscular rear hip widebody fenders matching maximum 1.87m track envelope.
- [x] Apply X-Mirror and Subsurf modifiers.

### Task 5: Rear Diffuser & GT Swan-Neck Wing (Phase 5)
- [x] Construct 6-fin rear aero diffuser with twin titanium exhaust cutouts and red accent rim.
- [x] Construct dual swan-neck aerodynamic uprights and curved aerofoil wing profile with red endplate accents.
- [x] Apply X-Mirror and Subsurf modifiers.

### Task 6: Track Wheels & Brakes (Phase 6)
- [x] Model master wheel in `bmesh`: 10-spoke forged rim, center lock nut, bead rim.
- [x] Model track tire with sidewall red pinstripe accent and drop center barrel.
- [x] Model cross-drilled ceramic brake rotor and Brembo-style 6-piston red caliper.
- [x] Instance across all 4 wheel stations using shared mesh data (`obj.data = master_mesh`).

### Task 7: Side Aero Skirts & Carbon Mirrors (Phase 7)
- [x] Extrude stepped aero side skirts running between front and rear fenders with red pinstripe and rear vertical fin.
- [x] Model aerodynamic wing mirrors with carbon stalks, rear-facing blackout glass, and integrated LED indicator strips.
- [x] Apply X-Mirror and Subsurf modifiers.

### Task 8: Lighting Hardware & Badging (Phase 8)
- [x] Build angular front headlight housings with sharp triple-chevron LED DRLs, twin projectors, and smoked lenses.
- [x] Build continuous rear horizontal LED lightbar with GT-R signature halo motifs and dark carbon backplate.
- [x] Create 3D embossed GT-R emblem on front grille and rear deck with chrome 'GT' and racing red 'R'.
- [x] Apply X-Mirror and material slots.

### Task 9: Quality Audit & Presentation Render (Phase 9)
- [x] Verify polygon count target (30,816 viewport / up to 480k at render level 3-4 within 600k budget).
- [x] Verify non-intersecting geometry and normal directions via bmesh recalculations.
- [x] Verify complete part decomposition (14 discrete major components matching test specification).
- [x] Setup studio hero 3-point lighting and capture hero perspective render via MCP.
