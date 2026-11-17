# Apex GT-R Approach 2: Hypercar Concept Interior & Body Rework Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the Apex GT-R Concept by completely redesigning the front bonnet to eliminate sunken indentations and panel gaps, reconstructing the rear deck/fascia with recessed 3D taillights and exhaust bezels, converting the glass to high-fidelity transparent automotive tint, and building a full driver-focused hypercar concept interior (dual-cowl digital dashboard, carbon bucket seats, GT-R steering wheel, center console, and rear strut brace) within the remaining 600k poly budget.

**Architecture:** Pure Zone A (`bmesh` + `bpy.data`) procedural execution. All modifications happen in memory without UI freezing. The interior is organized in a dedicated collection (`04_Interior_Cockpit`) with shared instancing for twin bucket seats and multi-material slots for Alcantara, carbon fiber, leather, red accents, and digital screens.

**Tech Stack:** Blender 4.x/5.x Python API (`bmesh`, `bpy.data`, `mathutils`), Blender MCP.

**Spec:** Approach 2 (Hypercar / Nismo Concept) approved by user during brainstorming on 2026-11-12.

---

## Global Constraints
- Target Polygons: Well within 600,000 polygon ceiling (~80k interior, ~35k exterior refinements, total scene ~150k evaluated quads).
- Glass: Must be transparent with realistic IOR (1.45), subtle smoke tint, and Fresnel reflections so interior is clearly visible from outside.
- Shutlines: Zero floating gaps between hood, bumper, and fenders.
- Rear Deck: Solid integrated rear valence with recessed housing cups for taillight halos and exhaust surrounds.
- Pipeline Standard: 90% execution in `bmesh` memory; `bpy.ops` strictly limited to I/O and render boundaries.

---

## Review Focus
1. **Hood-to-Bumper Gap:** Front hood leading edge must seamlessly align with front bumper top fascia without hovering or intersecting.
2. **Surface Smoothness (No Sunken Dents):** Elimination of pinched normals or disconnected dark patches on hood vents.
3. **Rear Fascia Enclosure:** Rear deck and bumper must not appear as hollow disconnected sheets; solid fascia backplate with recessed light housings.
4. **Cockpit Visibility:** Interior elements must be scaled to human ergonomics and visible from exterior camera angles through front, side, and rear fastback glass.
5. **Seat Symmetry & Instancing:** Driver and passenger seats must share master mesh data (`obj.data = master_seat_mesh`) with appropriate mirror/offset transforms.

---

## Tasks Breakdown

### Task 1: Glass Shader Update & Front Bonnet Complete Redesign
**Files:**
- Modify: In-memory scene shaders & `Apex_GTR_Hood_Vented` object in `01_Body_Chassis`.

**Interfaces:**
- Consumes: Existing scene collections and material `Mat_Apex_BlackoutGlass`.
- Produces: Updated `Mat_Apex_CockpitGlass` (Transmission=0.82, Roughness=0.04, IOR=1.45) and reconstructed `Apex_GTR_Hood_Vented` mesh.

- [x] **Step 1: Update Glass Shader to Realistic Automotive Tint**
  - Switch `Mat_Apex_BlackoutGlass` to use Transmission = 0.82, Roughness = 0.04, Metallic = 0.05, Base Color = (0.08, 0.09, 0.10, 1.0), IOR = 1.45.
- [x] **Step 2: Reconstruct Front Hood with Sleek Aero Contours**
  - Delete old patched hood mesh.
  - Build new quad hood with center power dome and flush-mounted aerodynamic carbon extractor strakes (no sunken holes).
  - Align leading edge ($Y = 2.14$) flush with bumper apron ($Z \approx 0.53$) to eliminate the hovering gap.
- [x] **Step 3: Verify Front End via MCP `look`**
  - Verified seamless fit, clean quad curvature, and elimination of the dented patch look.

---

### Task 2: Rear Deck, Fascia & Taillight Housing Overhaul
**Files:**
- Modify: `Apex_GTR_Rear_Diffuser`, `Apex_GTR_Tail_Lights`, and rear trunk deck of `Apex_GTR_Body_Shell`.

**Interfaces:**
- Consumes: Rear haunch coordinates and exhaust positions.
- Produces: `Apex_GTR_Rear_Fascia_Enclosure` with recessed taillight cups, ducktail trunk lid integration, and quad titanium exhaust surrounds.

- [x] **Step 1: Construct Solid Rear Fascia Enclosure**
  - Build closed rear valence bridging body haunches down to diffuser floor, eliminating the hollow gaping sheet.
  - Add integrated exhaust surrounds with carbon heat shields around exhaust pipes.
- [x] **Step 2: Recess Taillights into Molded Fascia Cups**
  - Reposition halo rings and horizontal lightbar into dedicated recessed bezel pockets molded into the rear fascia.
  - Integrate smooth ducktail kickup on the upper trunk lid edge.
- [x] **Step 3: Verify Rear Assembly via MCP `look`**
  - Confirmed solid rear panel, recessed 3D taillight pockets, and seamless diffuser integration.

---

### Task 3: Interior Tub, Floorpan & Door Cards
**Files:**
- Create: `Apex_GTR_Interior_Tub` in collection `04_Interior_Cockpit`.

**Interfaces:**
- Consumes: Body shell inner boundaries ($X \in [-0.78, 0.78], Y \in [-0.95, 0.68], Z \in [0.12, 0.72]$).
- Produces: Cockpit tub geometry with floor carpet, aluminum racing pedal box, carbon door sills, and sculpted leather door cards with red fabric pull loops.

- [x] **Step 1: Create Master Interior Materials**
  - Configured `Mat_Interior_Alcantara`, `Mat_Interior_Leather`, `Mat_Apex_CarbonAero`, `Mat_Apex_RedTrim`, `Mat_Apex_BrakeSteel`.
- [x] **Step 2: Model Cockpit Tub in bmesh**
  - Sloping firewall, flat floorpan, central transmission tunnel, and sculpted door cards with armrests.
  - Multi-pedal aluminum racing pedal box (dead pedal, clutch, brake, throttle).
  - Motorsport red fabric door pull loops.
- [x] **Step 3: Assign Multi-Material Slots & Smooth Shading**
  - Assigned multi-material slots across tub, door cards, and pedal plates. Subsurf applied.

---

### Task 4: Dual-Cowl Dashboard & Digital Telemetry Cockpit
**Files:**
- Create: `Apex_GTR_Dashboard` in `04_Interior_Cockpit`.

**Interfaces:**
- Consumes: Cowl line at base of windshield ($Y \in [0.45, 0.70], Z \in [0.65, 0.85]$).
- Produces: Driver-oriented sculpted dashboard, digital gauge screen, center console screen, and circular AC turbine vents.

- [x] **Step 1: Build Sculpted Dual-Cowl Dashboard Structure**
  - Driver binnacle cowl and passenger swept wing dash in `bmesh`.
- [x] **Step 2: Add Digital Screens & Vents**
  - Driver curved digital gauge cluster screen with simulated telemetry display (`Mat_Interior_Screen`).
  - Center floating infotainment screen.
  - 4 circular turbine AC vents with satin red bezels.

---

### Task 5: Center Console, Transmission Tunnel & Controls
**Files:**
- Create: `Apex_GTR_Center_Console` in `04_Interior_Cockpit`.

**Interfaces:**
- Consumes: Center tunnel floor space ($X \in [-0.14, 0.14], Y \in [-0.60, 0.45]$).
- Produces: Carbon bridge console, sequential drive selector, start/stop button, and rotary drive mode selector.

- [x] **Step 1: Model Carbon Fiber Floating Center Bridge**
  - Extrude angled center bridge connecting lower tunnel to dash stack.
- [x] **Step 2: Detail Controls**
  - Sequential gear shift knob with steel boot.
  - Anodized red Engine Start/Stop pushbutton.

---

### Task 6: High-Bolster Carbon Racing Bucket Seats (Driver & Passenger)
**Files:**
- Create: `Apex_GTR_Seat_Master_Mesh`, `Apex_GTR_Seat_Driver`, `Apex_GTR_Seat_Passenger` in `04_Interior_Cockpit`.

**Interfaces:**
- Consumes: Floor tub seat mounts ($Y \in [-0.45, 0.15], Z \in [0.15, 0.88]$).
- Produces: Shared master bucket seat mesh with ergonomic high bolsters, headrest, harness cutouts, and red racing seatbelts.

- [x] **Step 1: Model Master Carbon Bucket Seat in bmesh**
  - High-support lateral side bolsters and thigh bolsters.
  - Ergonomic headrest, rear carbon shell backing (`Mat_Apex_CarbonAero`), Alcantara cushions, and red racing harness straps.
- [x] **Step 2: Instance Across Left & Right Stations**
  - Created Driver seat at $X = -0.36$ and Passenger seat at $X = +0.36$ using shared mesh data.

---

### Task 7: Flat-Bottom GT-R Steering Wheel & Rear Strut Half-Cage
**Files:**
- Create: `Apex_GTR_Steering_Wheel` and `Apex_GTR_Rear_Brace` in `04_Interior_Cockpit`.

**Interfaces:**
- Consumes: Steering column position in front of driver ($X = -0.36, Y = 0.28, Z = 0.68$) and rear cabin bulkhead ($Y \in [-0.95, -0.65]$).
- Produces: Detailed 3-spoke flat-bottom steering wheel, carbon paddle shifters, and tubular rear chassis strut brace.

- [x] **Step 1: Model GT-R Flat-Bottom Racing Wheel**
  - Alcantara rim with red 12 o'clock center alignment stripe, 3-spoke carbon hub with thumb buttons, column shroud, and dual carbon paddle shifters (+/-).
- [x] **Step 2: Model Rear Chassis Cross-Brace (Half-Cage)**
  - 44mm tubular titanium X-brace connecting rear suspension strut towers and roof hoops with red anodized corner mounting flanges, clearly visible through the rear fastback glass.

---

### Task 8: Verification, Lighting Integration & Hero Turntable Audit
**Files:**
- Modify: `Apex_GTR_Project` scene & studio cameras.

**Interfaces:**
- Consumes: All exterior and interior components.
- Produces: Final verified asset with polycount audit, exterior + interior hero renders.

- [x] **Step 1: Scene Geometry & Polycount Audit**
  - 40,740 evaluated quads across 23 discrete components safely within 600,000 budget (6.8% utilized).
- [x] **Step 2: Exterior & Interior Camera LookDev Passes**
  - Front 3/4 hero view, rear afterburner view, cockpit steering wheel close-up, and rear fastback half-cage view captured and verified via MCP `look`.
