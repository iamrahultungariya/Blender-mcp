# Design Document: Type II Mercedes-Benz Sprinter Van Ambulance (AAA Game-Ready)

**Date:** 2026-11-11  
**Target:** Blender 5.2.2 LTS via Local Blender MCP Server (Port 9876)  
**Standard:** 90/10 Hybrid Procedural Pipeline (`RULE[user_global]`)  
**Reference:** User-supplied 6-view blueprint sheet (`media_1794403034040_0d58cb01.jpg`)

---

## 1. Intent & Scope

### 1.1 Intent
Build a high-fidelity, AAA game-ready **Type II Modern Mercedes-Benz Sprinter (VS30 High-Roof) Van Ambulance** matching the exact specifications and 6 orthographic views (Front, Rear, Left, Right, Top, Bottom) of the reference blueprint.

### 1.2 Target Specifications
- **Vehicle Type:** Modern Type II European/Commercial Van Ambulance (High-Roof Unibody).
- **Target Polycount:** ~150k triangles (clean quad-dominant, game-ready topology).
- **Materials:** Full PBR shading (Glossy Automotive Paint, Matte Textured Cladding, Tinted Glass, Emissive Strobe LEDs, Diamond/Road Rubber, Polished Steel).
- **Format:** Native Blender `.blend` collection hierarchy, ready for GLTF/GLB/FBX export.

---

## 2. Goals, Non-Goals & Anti-Goals

### 2.1 Goals
1. **Accurate Dimensional Proportions:** Adhere to real-world Sprinter 3500 High-Roof dimensions verified in `vehicle_thinking.py`:
   - Overall Length: 5.92 m
   - Overall Width: 2.05 m (body) / 2.42 m (with mirrors)
   - Overall Height: 2.75 m (with rooftop lightbars and AC pod)
   - Wheelbase: 3.66 m (Front axle at $Y = 1.73$ m, Rear axle at $Y = -1.93$ m)
   - Ground Clearance: 0.20 m
   - Wheel Radius: 0.375 m (Tire diameter 0.75 m), Rim Radius: 0.215 m (17-inch rim)
2. **Modular Architecture:** Partition into 6 logical assemblies with dedicated collections for animation/rigging flexibility and clean modifier pipelines:
   - `VAN_Body_Shell`
   - `VAN_Cladding_Bumpers`
   - `VAN_Glass_and_Doors`
   - `VAN_Emergency_System`
   - `VAN_Wheels_and_Suspension`
   - `VAN_Livery_Decals`
3. **Exact Visual Livery Alignment:**
   - Pure high-gloss white base paint.
   - Red waistline stripe spanning from front fender across doors with the distinctive **digital stepped pattern** at the rear corner.
   - Bold red sans-serif `"AMBULANCE"` text on hood (angled), body sides, and rear doors.
   - Blue 6-pointed Star of Life emblems on side panels, rear door windows, and front roof brow.
   - Lower rear doors alternating 45° diagonal Red and White hazard safety chevrons.
4. **Emergency Lighting Stack:**
   - Front rooftop low-profile aerodynamic lightbar (Driver Red / Passenger Blue).
   - Rear rooftop matching lightbar (Left Red / Right Blue).
   - 4 corner roof warning pods (Red).
   - Xenon projector headlights with LED daytime running lights, plus high-mounted rear taillights.
5. **90/10 Hybrid Pipeline Standard:**
   - 100% of procedural mesh generation executed in memory via `bmesh` and `bpy.data`.
   - Sub-second rebuild execution, zero UI context freeze.
   - Automatic `Auto_Bevel` (Angle limit 35°) and `Auto_WeightedNormal` modifiers for sharp panel edges and smooth automotive curves.

### 2.2 Non-Goals
- Full interior ICU/stretcher equipment (the reference blueprint specifies tinted flush glass with opaque cabin silhouette; interior medical cabinetry is out of scope).
- Physics driving rig (asset is static game-ready model with separated rotatable wheel objects).
- Articulated opening doors / door hinge rigging (doors are static closed exterior assemblies with crisp shutline gaps).

### 2.3 Anti-Goals
- No solid block wheel wells that obscure rims.
- No flat unshaded geometry without bevel highlights.
- No single monolithic unseparated mesh that prevents modular material assignment.

---

## 2.4 Finalized Design Clarifications (Builder Check Decisions)
1. **Livery & Decals Pipeline:** All graphics (Red `"AMBULANCE"` typography, Blue 6-pointed Star of Life emblems with staff and serpent, red waistline digital stepped chevrons, and rear diagonal hazard chevrons) are modeled as **high-precision procedural 3D geometric decals** offset by 1.0 mm along panel normals. This ensures 100% vector sharpness in any engine and renders without requiring external image files.
2. **Undercarriage & Running Gear:** To faithfully match the blueprint's **Bottom View**, a lightweight procedural 3D chassis assembly (`VAN_Chassis_Undercarriage`) is included with dual frame rails, transmission crossmember, exhaust pipe with center expansion muffler and tailpipe, rear drive axle tube, differential pumpkin, and fuel tank (~6k–8k tris).
3. **Cab Interior & Door Visibility:** Front cab doors, side sliding door, and rear barn doors are static closed with clean exterior panel shutline seams. A low-poly dark front cab interior blockout (dual bucket seats, dashboard cowl, steering wheel) is positioned inside the cab so the front 3/4 hero view through the curved windshield has realistic depth, while the rear patient compartment glass remains dark opaque.

---

## 3. Approaches Considered

### Approach 1: Modular Multi-Partition Assembly (SELECTED)
- **Concept:** Construct the vehicle as 6 distinct coordinated modular objects sharing a unified coordinate origin `(0, 0, 0)`.
- **Pros:** Clean quad topology; isolated modifier stacks; easy material assignment; doors and wheels can be articulated or exported individually; sub-second BMesh execution.
- **Cons:** Requires precise coordinate alignment between mating parts (handled via parametric dimensional rules in `bmesh_toolkit.py` and `vehicle_thinking.py`).

### Approach 2: Monolithic Single-Mesh Van Body (REJECTED)
- **Concept:** Combine body, cladding, windows, and bumpers into a single connected mesh.
- **Why Rejected:** Extremely difficult to texture cleanly with multi-materials, impossible to animate or open doors, high risk of non-manifold boolean errors.

### Approach 3: SDF Visual Hull Voxel Carving (REJECTED)
- **Concept:** Use `sdf_space_carve` on the orthographic blueprint silhouettes.
- **Why Rejected:** Voxelized/triangulated mesh results require heavy manual retopology to achieve automotive-grade surface flow.

---

## 4. Technical Specification by Assembly

### 4.1 `VAN_Body_Shell`
- **Cab & Cargo Greenhouse:** Single unibody van shell ($X = [-1.02, 1.02]$, $Y = [-2.96, 2.96]$, $Z = [0.38, 2.65]$).
- **Aerodynamic Hood & Cowl:** Sloped hood extending from cowl ($Y = 1.25, Z = 1.20$) to front grille ($Y = 2.85, Z = 0.92$) with subtle central convex crown.
- **High-Roof Blister:** Smooth aerodynamic front slope above windshield transitioning to a level high-roof ($Z = 2.65$).
- **Roof Stiffener Corrugations:** 4 longitudinal indented stamping channels along the roof ($Y = -2.60$ to $0.80$) for structural realism as seen in the Top View.
- **Window Cutouts:** Recessed window frames for windshield, front cab doors, right sliding door, left fixed window, and rear barn doors.

### 4.2 `VAN_Cladding_Bumpers`
- **Lower Perimeter Cladding:** Dark matte grey impact-resistant polymer cladding ($Z = 0.22$ to $0.56$) running around the entire vehicle.
- **Wheel Arches:** Molded semi-circular fender flares ($R = 0.44$ m, clearance $0.065$ m above tire) integrated into the cladding at $Y = 1.73$ (front) and $Y = -1.93$ (rear).
- **Front Bumper:** Integrated 3-bar grille with Mercedes-style trapezoid taper, lower center intake, side fog lamp bezels, and front license plate recess.
- **Rear Step Bumper:** Integrated non-slip rear step bumper with license plate mount and corner step reliefs.

### 4.3 `VAN_Glass_and_Doors`
- **Windshield:** Compound curved automotive safety glass ($bx=1.85, tx=1.65, sagitta=0.075$) with dark ceramic frit border.
- **Cab Door Windows:** Left and right driver/passenger door glass with black rubber weatherstripping.
- **Side Body Windows:** Right sliding door flush tinted window and left side large paramedic view window.
- **Rear Barn Doors:** Dual vertical doors ($50/50$ split) with dark tinted rectangular windows.
- **Hardware:** Modern flush door handles and dual commercial vertical towing mirrors with integrated amber LED turn signals.

### 4.4 `VAN_Emergency_System`
- **Front Lightbar:** Aerodynamic rooftop lightbar mounted on windshield brow ($Y = 1.22, Z = 2.66$): Driver-side Red LED cluster, Passenger-side Blue LED cluster, clear polycarbonate aerodynamic dome.
- **Rear Lightbar:** Matching aerodynamic rooftop lightbar mounted on rear roof edge ($Y = -2.90, Z = 2.66$): Left Red / Right Blue.
- **Roof Strobe Pods:** 4 compact red perimeter strobe pods mounted on upper roof corners.
- **Rooftop AC / Vent Pod:** Low-profile center climate control unit with fan vents situated on the roof ($Y = -0.50$ to $0.30$).
- **Headlights & Taillights:** Dual front projector assemblies with LED halos; vertical rear taillight stacks mounted high on the D-pillars.

### 4.5 `VAN_Wheels_and_Suspension`
- **Master Van Wheel (`VAN_Master_Wheel`):**
  - Modern 17-inch commercial van steel wheel with 12 circular perimeter cooling vents.
  - Deep center hub with 6 heavy-duty lug bolts.
  - Heavy-duty road radial tire ($R = 0.375$ m, width $0.235$ m) with realistic tread shoulder and sidewall bulge.
  - Internal steel brake disc rotor and front brake caliper.
- **Instanced Wheel Objects:**
  - `VAN_Wheel_FL` at $(+0.86, +1.73, 0.375)$
  - `VAN_Wheel_FR` at $(-0.86, +1.73, 0.375)$
  - `VAN_Wheel_RL` at $(+0.865, -1.93, 0.375)$
  - `VAN_Wheel_RR` at $(-0.865, -1.93, 0.375)$

### 4.6 `VAN_Livery_Decals`
- **Stepped Red Beltline Stripe:** Precision 3D decal band running horizontally along the waistline, transitioning into the iconic 3-step digital chevron at the rear corner.
- **"AMBULANCE" Typography:**
  - Hood: Angled red bold decal across front slope.
  - Sides: Bold red lettering positioned centrally below the side windows.
  - Rear: Prominent red lettering across the upper barn doors.
- **Star of Life Emblems:**
  - Blue 6-pointed star with white Rod of Asclepius on left and right rear quarter panels.
  - Dual blue stars on rear door windows.
  - Front brow star above windshield.
- **Rear Safety Chevrons:** Alternating 45° diagonal Red and White reflective chevrons on lower rear doors ($Z = 0.42$ to $0.92$).

---

## 5. Verification & Acceptance Criteria

1. **Dimensional Accuracy:** Vehicle bounds fit within $L: 5.92 \pm 0.05$ m, $W: 2.05 \pm 0.04$ m, $H: 2.75 \pm 0.05$ m.
2. **Visual Fidelity:** Viewport rendering matches the reference image in all 6 aspects:
   - Front 3/4 perspective matching hero shot.
   - Front & rear orthographic alignment.
   - Side profile and roof corrugation alignment.
3. **Execution Safety:** Pure BMesh execution completes in $< 3$ seconds with zero unhandled exceptions.
4. **Persistence:** Scene saved to `Type_II_Sprinter_Ambulance.blend`.