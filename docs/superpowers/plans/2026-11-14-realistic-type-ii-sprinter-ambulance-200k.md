# Realistic Type II Mercedes-Benz Sprinter Ambulance (200k Poly/Tri Budget, Exterior Only) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Procedurally generate an ultra-realistic, AAA game-ready Type II Mercedes-Benz Sprinter (VS30 High-Roof) Van Ambulance exterior in Blender 5.2.2 LTS hitting a target budget of ~200,000 polygons/triangles with natural geometric curvature, zero interior overhead, strict non-metallic finishes, and fully modular architecture (< 200 LOC per file).

**Architecture:** 100% in-memory procedural generation using the 90/10 Hybrid Pipeline (`bmesh` + `bpy.data` in memory, sub-second execution). The model is partitioned into 9 cleanly separated modular components in `ambulance_builder/`. Interior geometry is dropped so 100% of the 200k polygon budget is dedicated to natural parametric automotive surface lofting ($G^1/G^2$ tangency, compound curved hood with power crown, aerodynamic high-roof forehead blister, radiused wheel arch flares, continuous body-side tumblehome, flush tinted privacy glazing, 3D treaded tires, alloy wheels, and Whelen Freedom IV emergency lighting).

**Tech Stack:** Blender 5.2.2 LTS, Python 3.11+, `bmesh`, `mathutils`, Blender MCP Server (Port 9876).

**Spec:** `docs/superpowers/specs/2026-11-11-type-ii-van-ambulance-design.md`

---

## Global Constraints

- **Polygon & Triangle Budget:** Target $\approx 200,000$ evaluated polygons / triangles.
- **Scope:** 100% exterior only. No interior seats, dashboard, or medical cabinets. Cab windows use high-gloss dark tinted privacy safety glass (`roughness: 0.04`, `transmission: 0.10`, base color `(0.02, 0.025, 0.03)` with IOR 1.52).
- **Finish:** Strictly non-metallic shaders (`metallic = 0.0` across all materials).
- **Dimensions:** Length $5.92 \pm 0.05$ m, Width $2.05 \pm 0.04$ m (body) / $2.42$ m (with mirrors), Height $2.75 \pm 0.05$ m. Wheelbase $3.66$ m (Front axle $Y = +1.73$ m, Rear axle $Y = -1.93$ m).
- **Modularity:** Strictly no monolithic files; every Python file in `ambulance_builder/` must remain $< 200$ LOC.
- **Placement:** Placed beside the master bedroom in collection `07_AMBULANCE_BAY` at base coordinate offset `(6.0, 0.0, 0.0)`.

---

## Review Focus

1. **Curvature Tangency & No Hollow Cutouts:** Ensure the unibody shell has continuous solid side panels, seamless windshield header transition into the high-roof brow, and realistic B-pillars so the vehicle looks solid and structural from any angle.
2. **True Geometric Shutlines:** Verify door and hood perimeters have recessed 4mm dark weatherseal reveal channels rather than flat texture lines.
3. **Budget Precision (~200k Triangles):** Ensure total evaluated triangle count lands between $190,000$ and $210,000$ triangles, with proper weight distribution (wheels ~112k, cladding ~32k, body shell ~28k, emergency ~18k, glass ~6k, chassis ~3k, decals ~1.5k).
4. **Wheel Arch Flush Fit:** Ensure the 17-inch multi-spoke wheels with 3D tread lugs sit flush with the outer flared wheel arch trim ($X = \pm 0.90$ m hub offset).
5. **Non-Metallic Compliance:** Assert that all 16 materials in `bpy.data.materials` have `Metallic == 0.0`.

---

## Polycount & Triangle Allocation (200k Target)

| Subsystem / Assembly | Target Tris | Geometric Technique |
| :--- | :---: | :--- |
| **`VAN_Master_Wheel` (4x instanced)** | **~112,000** ($4 \times 28\text{k}$) | 128-seg tire carcass, 480 3D tread lugs, 192 radial sidewall sipes, twin-spoke alloy rim, dual vented rotor plates with 64 curved cooling vanes, dual calipers |
| **`VAN_Cladding_Bumpers`** | **~32,000** | Front bumper with rounded corner fillets, 3-bar grille with 36 honeycomb cells, tubular push bar, 32-seg wheel arches with return flange, diamond tread rear step |
| **`VAN_Body_Shell`** | **~28,000** | 36x24 lofted aerodynamic hood with central parabolic crown, seamless brow, solid side panels, cab partition bulkhead, 6 roof corrugations with Subsurf Level 1 |
| **`VAN_Emergency_System`** | **~18,000** | Front & rear Whelen Freedom IV lightbars with 64 parabolic LED reflector cups, siren speaker horn, xenon projector headlights with DRL eyebrows, taillights |
| **`VAN_Glass_and_Doors`** | **~6,000** | 24x16 compound curved windshield with black ceramic frit, flush dark privacy side/rear glass, towing mirrors with LED signals, flush door handles |
| **`VAN_Chassis_Undercarriage`** | **~3,000** | Ladder frame rails, tubular crossmembers, ribbed shock absorber dust boots, exhaust muffler with tailpipe, rear drive axle with differential |
| **`VAN_Livery_Decals`** | **~1,500** | 1mm offset 3D geometric decals: Battenburg yellow/red chevrons, 6-pointed Star of Life emblems, extruded "AMBULANCE" typography |
| **TOTAL EVALUATED BUDGET** | **~200,500 tris** | **Full exterior realism, natural curvature, zero interior waste** |

---

## Detailed Task Breakdown

### Task 1: Shaders & Material Tuning (`ambulance_builder/materials.py`)
- Remove interior seat materials.
- Set `VAN_Glass_Tinted` to ultra-dark high-gloss exterior privacy glass (`Base Color: (0.02, 0.025, 0.03)`, `Roughness: 0.04`, `Transmission: 0.05`, `Metallic: 0.0`, `IOR: 1.52`).
- Verify all 16 shaders have `Metallic = 0.0`.
- Target: $< 130$ lines.

### Task 2: High-Density Exterior Running Gear & Wheels (`ambulance_builder/wheels.py`)
- Model 128-segment tire carcass with 5 longitudinal tread channels.
- 480 transverse biting lugs around the tire circumference.
- 192 radial sidewall markings (96 outer, 96 inner).
- 17-inch twin-spoke alloy rim with drop center and center hub well with 6 hex lug bolts.
- Dual ventilated brake rotor plates with 64 curved internal cooling vanes and 48 drilled rotor holes.
- Primary multi-piston caliper and parking caliper.
- Enforce $X = \pm 0.90$ m axle track for flush alignment with wheel arch flares.
- Target: $\approx 28\text{k}$ tris per wheel $\times 4 = 112\text{k}$ tris. Target lines: $< 180$.

### Task 3: Natural Curved Unibody Shell & Solid Exterior (`ambulance_builder/body.py`)
- 36x24 lofted quad hood with natural parabolic power dome crown and smooth cowl transition.
- Seamless aerodynamic high-roof forehead brow connecting A-pillars to roof cap ($Z = 2.08 \to 2.65$).
- Solid sheet metal exterior side panels along passenger and cargo compartment with precise recessed window reveal cutouts.
- Solid rear barn doors with dual window reveals and center vertical shutline seam.
- Solid interior partition bulkhead at $Y = 0.65$ sealing off the front cab.
- 6 stamped longitudinal roof stiffening ribs with radiused fillet edges.
- Subsurf Level 1 + Auto Bevel + Weighted Normal for smooth automotive reflection highlights.
- Target: $\approx 28\text{k}$ tris. Target lines: $< 180$.

### Task 4: Sculpted Front Bumper, Grille, Push Bar & Step Bumper (`ambulance_builder/cladding.py`)
- Sculpted front bumper with 32-segment rounded corner fillets and lower air dam.
- Mercedes-Benz VS30 Sprinter 3-bar grille with 36 hexagonal honeycomb intake cells.
- Front tubular push bar / bull bar with beveled tube elbows.
- 4 molded semicircular wheel arch trims with 32 segments and inner return flanges.
- Heavy-duty rear step bumper with 48 non-slip diamond-plate tread studs.
- Subsurf Level 1 + Auto Bevel.
- Target: $\approx 32\text{k}$ tris. Target lines: $< 160$.

### Task 5: Emergency Lighting, Whelen Lightbars & Headlights (`ambulance_builder/emergency.py`)
- Front Whelen Freedom IV low-profile aerodynamic lightbar: 32 red LED parabolic reflector cups (driver side), 32 blue LED parabolic reflector cups (passenger side), center siren speaker horn.
- Rear matching aerodynamic rooftop lightbar with 32 parabolic reflector cups.
- 4 perimeter roof corner strobe warning pods with 24-segment faceted lenses.
- Xenon projector headlights: dual 32-seg projector barrels, upper eyebrow LED DRL light guides, and amber turn markers.
- High-mount vertical D-pillar taillight stacks with 32 LED blades and turn/reverse indicators.
- Rooftop AC climate control pod with dual 32-seg circular ventilation fans.
- Target: $\approx 18\text{k}$ tris. Target lines: $< 160$.

### Task 6: Flush Exterior Glazing, Towing Mirrors & Hardware (`ambulance_builder/glass.py`)
- Compound curved aerodynamic windshield (24x16 quad loft, $sagitta = 0.075$ m) with black ceramic frit border.
- Flush tinted privacy side windows and rear barn door windows with molded rubber gaskets.
- Sculpted commercial vertical towing mirrors with twin aerodynamic mounting stalks and integrated amber LED turn signals.
- Flush-fit recessed exterior door handles (cab doors, sliding door, rear barn door).
- Target: $\approx 6\text{k}$ tris. Target lines: $< 140$.

### Task 7: Undercarriage Silhouette & Running Gear (`ambulance_builder/chassis.py`)
- Focus exclusively on exterior undercarriage visibility: dual ladder frame rails, crossmembers, fuel tank with metal straps, full exhaust system with cylindrical muffler and side exit tailpipe, rear live axle tube with differential pumpkin, dual 5-leaf spring packs, and 4 ribbed shock absorber bellows.
- Remove interior seats/steering wheel code (saving lines and polycount).
- Target: $\approx 3\text{k}$ tris. Target lines: $< 130$.

### Task 8: High-Visibility 3D Livery Decals (`ambulance_builder/decals.py`)
- 1mm offset 3D geometric decals: fluorescent yellow Battenburg waistline band with 45° forward red chevrons.
- 6-Pointed Blue Star of Life emblems with white Rod of Asclepius on quarter panels, rear door windows, and roof brow.
- 3D extruded "AMBULANCE" block lettering across hood and upper rear doors.
- Alternating 45° diagonal safety hazard chevrons on lower rear doors.
- Target: $\approx 1.5\text{k}$ tris. Target lines: $< 130$.

### Task 9: Assembly, Polycount Evaluation & Multi-Angle Verification (`ambulance_builder/staging.py` & `assemble.py`)
- Update `staging.py` with multi-camera rig:
  - `Camera_Ambulance_Hero`: 50mm 3/4 front beauty angle.
  - `Camera_Ambulance_Rear`: 45mm rear 3/4 angle.
  - `Camera_Ambulance_Side`: Orthographic side profile.
  - `Camera_Scene_Overview`: Wide view showing both bedroom & ambulance.
- Run `evaluate_ambulance_budget()` in Blender to verify exact evaluated polygon and triangle counts meet the **~200k target**.
- Capture high-resolution viewport renders via `look` to verify exterior realism, natural curvature, and clean panel seams.
