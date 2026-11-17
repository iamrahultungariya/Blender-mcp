# Indian Vastu 2BHK Modular Residence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a modular, game-engine-ready, AAA-quality 400k triangle procedural 3D model of an Indian Vastu Shastra compliant 2BHK residence in Blender 4.x/5.x.

**Architecture:** Deconstruct the single monolithic script into a clean, reusable Python package (`vastu_modular/`) containing core materials, high-poly BMesh modeling primitives (lathe profiles, fluted channels, beveled chamfers, curve sweeps), dedicated room prefab modules, and a master scene assembler that instantiates components at precise Vastu coordinates.

**Tech Stack:** Python 3.11+, Blender 5.2 Python API (`bpy`, `bmesh`, `mathutils`), Principled BSDF PBR Shading, EEVEE Next Real-Time Engine.

**Spec:** `docs/superpowers/specs/2026-11-13-vastu-2bhk-modular-design.md`

## Global Constraints
- Target Triangle Budget: 400,000 Triangles (±15%).
- 90/10 Hybrid Pipeline: 90% of geometric computation runs in RAM via BMesh (`bmesh.new()`, `bmesh.ops.*`, `bm.to_mesh()`). Zero UI context operator dependencies inside loops.
- Vastu Cardinal Rules:
  - SW: Master Bedroom (Bed head South).
  - SE: Kitchen (Cook faces East).
  - NE: Living Lounge & Sacred Mandir (Divine Corner).
  - NW: 2nd Bed & Study Workstation.
  - West: Bathroom & WC (Facing North-South).
  - Center (Brahmasthan): Open, zero heavy columns or obstructions, circular inlaid mandala medallion.
- Door Openings: Real doorway casings with thin hinged door leaves pivoted at the hinge line (no giant blocking boxes!).

## Review Focus
1. **Doorway Obstruction Check**: Door leaves must be thin (35-40mm) and rotated on the hinge pivot without intersecting or barricading the door openings.
2. **Curvature Quality**: Sofas, cushions, lathe spindles, and sanitary bowls must have smooth subdivided contours (`face.smooth = True` with adequate radial segments).
3. **Triangle Budget Verification**: Total scene polygon count must reach ~400k triangles for rich real-time visual detail without viewport lag.
4. **Vastu Zone Integrity**: Every single room must correspond strictly to its prescribed cardinal quadrant and element.
5. **Material Fidelity**: Glass must be clean and transparent; polished granite must have bullnose edge highlights; brass must have specular sheen; velvet must have soft roughness.

---

### Task 1: Core Framework & PBR Material Palette
**Files:**
- Create: `vastu_modular/__init__.py`
- Create: `vastu_modular/core/__init__.py`
- Create: `vastu_modular/core/materials.py`

- [ ] Step 1: Create package folder structure under `c:\Users\Rahul\OneDrive\Desktop\Blender MCP\vastu_modular`.
- [ ] Step 2: Implement `materials.py` with Blender 4/5 Principled BSDF node setup (Base Color, Roughness, Metallic, Alpha, Transmission, Emission).
- [ ] Step 3: Define 22 distinct materials: Italian Botticino marble, rich walnut parquet, oak parquet, jet black granite, off-white lacquer, royal navy velvet, sage fabric, saffron mustard linen, peacock teal linen, polished temple brass, mirror chrome, clear architectural glass, sanitary white ceramic, and lawn grass.
- [ ] Step 4: Verify material creation via test script in Blender.

---

### Task 2: High-Poly Procedural BMesh Modeling Utilities
**Files:**
- Create: `vastu_modular/core/mesh_utils.py`

- [ ] Step 1: Implement `add_beveled_box(bm, x, y, z, sx, sy, sz, bevel_r, segs, mat_idx)` with edge beveling to eliminate 90° razor edges.
- [ ] Step 2: Implement `add_lathe_mesh(bm, cx, cy, cz, profile, segs, mat_idx)` for lathe-turned spindles, pillars, bells, diyas, and table legs.
- [ ] Step 3: Implement `add_fluted_panel(bm, x, y, z, length, depth, height, num_flutes, axis, mat_idx)` for vertical fluted headboards and tambours.
- [ ] Step 4: Implement `add_curved_cushion(bm, x, y, z, sx, sy, sz, puff, mat_idx)` with rounded organic volumetric curvature.
- [ ] Step 5: Implement `add_curved_pipe(bm, points, radius, segs, mat_idx)` for swept faucets, shower arms, and railings.
- [ ] Step 6: Test geometry utilities in Blender to verify manifold topology.

---

### Task 3: Architectural Prefab Kit & Door Assemblies
**Files:**
- Create: `vastu_modular/prefabs/__init__.py`
- Create: `vastu_modular/prefabs/arch_kit.py`

- [ ] Step 1: Implement `create_plinth_and_floors()` with stepped travertine foundation, individual room flooring materials, and central Brahmasthan medallion.
- [ ] Step 2: Implement `create_modular_walls()` with 1.45m cutaway height, 75mm baseboard skirting, and 40mm beveled mahogany coping caps.
- [ ] Step 3: Implement `create_modular_door_assembly(x, y, z, width, height, angle_deg)` with molded door jambs, stop bead, and a realistic thin 4-panel door leaf rotated around its hinge line ($Z$-axis).
- [ ] Step 4: Implement `create_casement_windows()` with beveled sills, center mullions, and clear glass glazing.
- [ ] Step 5: Implement `create_indian_archway()` with fluted pilasters and semicircular molded voussoirs connecting Living and Brahmasthan.
- [ ] Step 6: Test and verify door leaves swing open freely with zero doorway blockage.

---

### Task 4: Living Lounge & Sacred Mandir Prefab Kit
**Files:**
- Create: `vastu_modular/prefabs/living_kit.py`

- [ ] Step 1: Implement `create_curved_c_sofa_prefab()`: Organic C-curved boucle sofa with rolled armrests, channel-tufted backrest, bullnose seat cushions, and turned legs with brass caps.
- [ ] Step 2: Implement `create_tub_armchair_prefab()`: Semi-circular barrel armchairs with lumbar cushions.
- [ ] Step 3: Implement `create_coffee_table_prefab()`: Beveled walnut frame, tempered glass inset, and turned tapered legs.
- [ ] Step 4: Implement `create_fluted_tv_credenza_prefab()`: Low-profile credenza with fluted sliding doors and 65" frameless 4K OLED TV display.
- [ ] Step 5: Implement `create_sacred_mandir_prefab()`: Detailed traditional Indian temple in NE corner with 4 lathe-turned brass pillars, cusped torana arch, tiered shikhara roof, golden kalash spire, hanging bell, and stepped pooja diya with glowing flame.
- [ ] Step 6: Implement `create_biophilic_planter_prefab()`: Fluted ceramic planter with lush tiered foliage.

---

### Task 5: Modular Kitchen & Dining Suite Prefab Kit
**Files:**
- Create: `vastu_modular/prefabs/kitchen_kit.py`

- [ ] Step 1: Implement `create_granite_counter_prefab()`: L-shaped lower cabinets with continuous 40mm polished black granite countertop and smooth bullnose front fillet.
- [ ] Step 2: Implement `create_gas_hob_prefab()`: 4-burner tempered glass cooktop with stepped rings, cast-iron trivets, and control dials in the SE corner (cook facing East).
- [ ] Step 3: Implement `create_chimney_hood_prefab()`: Sloped stainless steel chimney hood and duct stack.
- [ ] Step 4: Implement `create_undermount_sink_prefab()`: Stainless sink in NE of kitchen with radiused corners and swept chrome gooseneck faucet.
- [ ] Step 5: Implement `create_refrigerator_prefab()`: Double-door brushed stainless refrigerator in SW of kitchen.
- [ ] Step 6: Implement `create_dining_suite_prefab()`: Beveled teak dining table with turned tapered legs and 4 curved upholstered dining chairs with placemats and fruit bowl.

---

### Task 6: Master & Guest Bedroom Suite Prefab Kit
**Files:**
- Create: `vastu_modular/prefabs/bedroom_kit.py`

- [ ] Step 1: Implement `create_master_bed_prefab()`: King-size bed in SW corner with 9-channel fluted royal navy velvet headboard, beveled frame, mattress with curved corners, draped folded duvet, 4 plush pillows with piping, and bed runner.
- [ ] Step 2: Implement `create_nightstand_lamp_prefab()`: Turned-leg nightstand with drawer and lathe-turned ceramic/brass bulbous table lamp with flared shade.
- [ ] Step 3: Implement `create_master_wardrobe_prefab()`: 4-door wardrobe with fluted panels and full-length brass handles.
- [ ] Step 4: Implement `create_vanity_console_prefab()`: Tambour fluted vanity desk with oval backlit mirror and cylindrical velvet pouf.
- [ ] Step 5: Implement `create_guest_bed_prefab()`: Queen-size bed in NW with curved sage green headboard, comforter, and pillows.
- [ ] Step 6: Implement `create_study_station_prefab()`: Wooden desk with open laptop, organizer, and 5-star caster ergonomic swivel office chair.

---

### Task 7: Luxury Restroom & Sanitary Prefab Kit
**Files:**
- Create: `vastu_modular/prefabs/bath_kit.py`

- [ ] Step 1: Implement `create_wall_hung_wc_prefab()`: D-shaped smooth curved ceramic toilet bowl aligned North-South with dual-flush chrome actuator plate.
- [ ] Step 2: Implement `create_vanity_basin_prefab()`: Floating teak vanity with fluted drawer, oval ceramic vessel washbasin, and curved chrome mixer faucet.
- [ ] Step 3: Implement `create_walk_in_shower_prefab()`: Frameless tempered glass enclosure with chrome pivot clamps and wall-mounted swept rain shower head.
- [ ] Step 4: Implement `create_towel_rail_prefab()`: Tubular chrome rail with draped folded towels.

---

### Task 8: Master Scene Assembler & Vastu Layout Orchestration
**Files:**
- Create: `vastu_modular/main.py`

- [ ] Step 1: Implement scene orchestration pipeline: cleanup scene, initialize material palette, create organized collections (`01_Architecture`, `02_Furnishings`, `03_Vastu_Labels`, `04_Lighting_Cameras`).
- [ ] Step 2: Instantiate all prefabs at exact Vastu coordinates.
- [ ] Step 3: Add floating 3D brass Vastu room title badges.
- [ ] Step 4: Set up cinematic warm morning sun light (East/NE angle), room ambient fill lights, and 3 cameras (`Cam_Isometric_Southeast`, `Cam_Isometric_Southwest`, `Cam_TopDown_Floorplan`).
- [ ] Step 5: Execute pipeline in live Blender session.

---

### Task 9: Quality Assurance & Triangle Budget Verification
**Files:**
- Test / Verify in Blender

- [ ] Step 1: Check total triangle count using Blender API (`sum(len(o.data.polygons)*2 for o in bpy.data.objects if o.type == 'MESH')`) to verify ~400k tris.
- [ ] Step 2: Verify all door openings are clear and door leaves swing smoothly without blocking.
- [ ] Step 3: Verify all curves (curved sofa, turned mandir pillars, fluted headboards, oval sanitaryware, bullnose granite) match the visual concept.
- [ ] Step 4: Capture multi-angle screenshots via `look` tool.
