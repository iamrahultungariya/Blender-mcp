# Design Document: Apex GT-R Concept Supercar (AAA Game-Ready)

**Date:** 2026-11-12  
**Target:** Blender 5.2.2 LTS via Local Blender MCP Server (Port 9876)  
**Standard:** 90/10 Hybrid Procedural Pipeline (`RULE[user_global]`)  
**Reference Blueprint:** User-supplied orthographic sheet (`media_1794463703583_908f42b0.jpg`)  
**Polygon Target:** ~30,000 Polygons (Clean Quad-Dominant Topology)  

---

## 1. Intent & Scope

### 1.1 Intent
Build a high-fidelity, AAA game-ready **Apex GT-R Concept Supercar** matching the exact dimensions, 12 separate component assemblies, aggressive aerodynamic widebody styling, and PBR materials shown in the reference orthographic blueprint.

### 1.2 Target Specifications
- **Vehicle Type:** High-Performance Track-Focused Concept Supercar.
- **Dimensional Envelope:**
  - Length: **4610 mm** ($4.610\text{ m}$)
  - Width: **1870 mm** ($1.870\text{ m}$) (Body shell) / $\approx 1980\text{ mm}$ (Flared fenders)
  - Height: **1180 mm** ($1.180\text{ m}$) (Roofline peak)
  - Wheelbase: **2700 mm** ($2.700\text{ m}$)
  - Ground Clearance: **100 mm** ($0.100\text{ m}$) track stance
- **Target Polycount:** ~30,000 polygons (clean quad-dominant, smooth aerodynamic curvatures, hard-surface creases).
- **Format:** Modular Blender Collection hierarchy (`Apex_GTR_Concept`), ready for GLTF/GLB/FBX export.

---

## 2. Goals, Non-Goals & Anti-Goals

### 2.1 Goals
1. **Blueprint Proportions & Envelope Fidelity:**
   - Front axle at $Y = +1.350\text{ m}$, Rear axle at $Y = -1.350\text{ m}$.
   - Front overhang: $0.955\text{ m}$, Rear overhang: $0.955\text{ m}$.
   - Aggressive supercar tumblehome ($12^\circ$ inward greenhouse slope) and low rake angles (Windshield $65^\circ$, Hood $14^\circ$).
2. **Modular 12-Component Assembly Decomposition:**
   Model each major assembly as a separate object for rigging, animation, and export flexibility:
   - `GTR_Body_Shell`
   - `GTR_Front_Bumper_Splitter`
   - `GTR_Hood`
   - `GTR_Fenders_Widebody`
   - `GTR_Headlights`
   - `GTR_Tail_Lights`
   - `GTR_Glass_Canopy`
   - `GTR_Aero_Mirrors`
   - `GTR_Side_Skirts`
   - `GTR_Rear_Diffuser_Exhaust`
   - `GTR_Rear_Wing`
   - `GTR_Wheel_Assembly` (Instanced 4x: FL, FR, RL, RR)
3. **Dedicated PBR Materials Vault:**
   - *Body Paint:* Dark Metallic Gunmetal Grey with clearcoat gloss.
   - *Aero Components:* High-gloss Satin Carbon Fiber (Splitter, Diffuser, Skirts, Wing).
   - *Accent Pinstripes:* Vibrant Crimson Red Anodized Accent.
   - *Glass:* Dark tinted automotive glass with black ceramic frit borders.
   - *Tires:* Radial rubber with directional tread grooves and matte sidewall.
   - *Brakes:* Ventilated steel/carbon ceramic disc rotor with bright red 6-piston Brembo-style caliper.
   - *Lighting:* Emissive White LED projectors + angular DRLs, Emissive Crimson Red rear ribbon bar.
4. **90/10 Hybrid Pipeline Standard:**
   - 100% procedural BMesh generation in C RAM via `bmesh` and `bpy.data`.
   - Modifiers (`Bevel` 2 segments + `WeightedNormal` keep sharp) applied on individual panels for razor-sharp automotive reflections without high-poly cage subsurf bloat.
   - Sub-second execution with zero UI freeze.

### 2.2 Non-Goals
- Full engine bay internal pistons/valves (hood vents have dark mesh backing).
- Articulated interior suspension physics rig (springs and dampers are static visual elements).
- Interactive door latch mechanisms (exterior shutlines are modeled cleanly with 3mm depth seams).

### 2.3 Anti-Goals
- No monolithic single-mesh blob (violates modular component requirement).
- No uncontrolled Sub-D modifier explosion exceeding the 30k poly budget.
- No blurry flat shading or unweighted normals on curved automotive panels.

---

## 3. Polygon Budget Allocation (~30,000 Polys)

| Component Assembly | Object Name | Target Quads/Tris | Description |
| :--- | :--- | :--- | :--- |
| **Main Body Shell** | `GTR_Body_Shell` | ~6,000 | Cabin, roof, A/B/C pillars, rear quarter panels, side intake ducts |
| **Front Bumper & Splitter** | `GTR_Front_Bumper_Splitter` | ~3,500 | Central hexagonal grille, dual cooling vents, splitter blade, canards, red trim |
| **Sculpted Hood** | `GTR_Hood` | ~2,000 | Low rake bonnet, power bulges, dual recessed aero heat extraction vents |
| **Widebody Fenders** | `GTR_Fenders_Widebody` | ~3,000 | Flared front & rear arches with aero cutouts and wheel clearance |
| **Headlight Assemblies** | `GTR_Headlights` | ~1,500 | Smoked housing, dual projector lenses, angular Z-pattern LED DRLs |
| **Tail Light Assemblies** | `GTR_Tail_Lights` | ~1,200 | Angular continuous LED ribbon lightbar, housing and reflector |
| **Glass Canopy** | `GTR_Glass_Canopy` | ~1,500 | Curved windshield, frameless door glass, fastback rear canopy |
| **Aero Wing Mirrors** | `GTR_Aero_Mirrors` | ~800 | Left & Right aero stalks, sculpted housings, reflective glass |
| **Side Skirts** | `GTR_Side_Skirts` | ~1,500 | Ground-effect lower aero blades, rear brake cooling entry, red stripe |
| **Rear Diffuser & Exhaust** | `GTR_Rear_Diffuser_Exhaust` | ~3,000 | 6 vertical aero strakes, F1 rain light, quad titanium exhaust tips |
| **GT Rear Wing** | `GTR_Rear_Wing` | ~1,500 | Dual stanchion uprights, curved airfoil blade, crimson red endplates |
| **Wheel Assemblies (Master)** | `GTR_Wheel_Master` (4x instanced) | ~4,000 | 10-spoke rim, radial tire, drilled brake rotor, red caliper |
| **Total Target** | | **~29,500** | **Strictly within 30k budget** |

---

## 4. Approaches Considered

### Approach 1: Modular BMesh Parametric Assembly + Shared Instancing (SELECTED)
- **Concept:** Construct each of the 12 components using mathematical parametric cross-sections in `bmesh`. Use shared mesh instancing (`obj.data = master_wheel.data`) for the 4 wheels. Apply hard-surface modifiers (`Bevel` + `WeightedNormal`).
- **Pros:** Exact polygon budget control (~29.5k); razor-sharp edge highlights; wheels independently rotatable; execution sub-second in C RAM.
- **Cons:** Requires rigorous coordinate alignment between mating panels.

### Approach 2: Low-Poly Sub-D Cage Modeling
- **Concept:** Model a ~3k low-poly cage and apply `Subdivision Surface` Level 2.
- **Cons:** Level 2 subsurf turns 3k into 48k+ faces (violating 30k budget); softens designed sharp creases on splitters and vents.

### Approach 3: Monolithic Single Mesh
- **Concept:** Single mesh car body and parts.
- **Cons:** Violates component separation; impossible to animate or assign independent glass/rubber/metal shaders efficiently.

---

## 5. Architectural & Coordinate System Standards

- **Coordinate System:**
  - Origin `(0, 0, 0)`: Ground center directly midway between front and rear axles.
  - $+Y$: Forward (Front Bumper at $Y \approx +2.305\text{ m}$).
  - $-Y$: Backward (Rear Diffuser / Wing at $Y \approx -2.305\text{ m}$).
  - $+X$: Right side ($+0.935\text{ m}$ body / $+0.990\text{ m}$ flared arch).
  - $-X$: Left side ($-0.935\text{ m}$ body / $-0.990\text{ m}$ flared arch).
  - $+Z$: Up ($Z = 0.0$ ground, $Z = 0.10\text{ m}$ underbody floor, $Z = 1.18\text{ m}$ roof peak).
  - Front Axle: $Y = +1.350\text{ m}$, Wheel center $Z = 0.340\text{ m}$.
  - Rear Axle: $Y = -1.350\text{ m}$, Wheel center $Z = 0.340\text{ m}$.
- **Collection Hierarchy:**
  - `Apex_GTR_Concept`
    - `01_Body_Structure` (`GTR_Body_Shell`, `GTR_Fenders_Widebody`, `GTR_Hood`)
    - `02_Aero_Fascia` (`GTR_Front_Bumper_Splitter`, `GTR_Side_Skirts`, `GTR_Rear_Diffuser_Exhaust`, `GTR_Rear_Wing`)
    - `03_Glass_and_Mirrors` (`GTR_Glass_Canopy`, `GTR_Aero_Mirrors`)
    - `04_Lighting` (`GTR_Headlights`, `GTR_Tail_Lights`)
    - `05_Wheels` (`GTR_Wheel_FL`, `GTR_Wheel_FR`, `GTR_Wheel_RL`, `GTR_Wheel_RR`)
