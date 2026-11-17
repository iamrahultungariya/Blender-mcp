# Modern Minimalist 5-Star Luxury Bedroom: Modular 3D Asset System Design

**Date:** 2026-11-13  
**Status:** Approved Design Document  
**Archetype:** `BEDROOM` / `BED` (Interior Spaces & High-End Furniture)  
**Pipeline Standard:** 90/10 Hybrid Pipeline (`bmesh` in C-RAM, zero UI freezes, multi-material face indexing)  
**Architecture:** Reusable 3D Modular Prefab Types (Zero monolithic `.py` files)

---

## 1. Intent & The "Why"
Previous single-script procedural generators suffered from:
1. **Monolithic sprawl**: A single giant script containing geometry, math, materials, and placement logic, making maintenance and reusability impossible.
2. **Boxy & Uncanny Furniture**: Cuboidal beds and stiff, flat blankets/pillows with sharp 90-degree edges that look like video-game blockouts rather than high-end physical fabric.
3. **UI Freezes**: Using `bpy.ops` inside construction loops freezing Blender for 10-30 seconds.

This system establishes a **Reusable Modular 3D Architecture**:
- Each asset component (Bed frame, fluted headboard, organic pillows, draped chadar/duvet, floating nightstands, acoustic wood slats, ambient lights, room envelope) is an independent, reusable Python class/module.
- Bedding features true physical textile aesthetics: organic cushion lofting via $Z(u,v) = z_0 + crown \cdot (1 - u^2)(1 - v^2)$, sinusoidal ripple waves for blanket folds, and turned-down cuff folds.
- 100% compliant with the 4-phase spatial pipeline:
  `[Prompt] ──> Step 1: generate_spatial_blueprint ──> Step 2: get_component_tree ──> Step 3: bmesh Procedural Construction ──> Step 4: validate_phase_gate(phase_id=2)`.

---

## 2. Goals, Non-Goals & Anti-Goals

### Goals
- **True-to-Life Bedding Realism**:
  - King-size bed (2.0m wide $\times$ 2.1m long) with recessed plinth creating a floating aesthetic.
  - Multi-tier pillow cluster: 2 structural back pillows (tilted at 15° with welted piping) + 2 crowned soft pillows + 1 lumbar accent cushion.
  - Chadar / Duvet: Sinusoidal cloth fold deformation, realistic drape over mattress flanks, and folded turned-down top border revealing contrasting inner sheet.
- **5-Star Luxury Bedroom Essentials**:
  - Dual floating cantilevered nightstands with concealed drawer bevels and metallic accent pulls.
  - Feature accent wall: Vertical acoustic wood slat paneling with warm backlighting.
  - Designer lighting: Suspended brushed brass minimalist cylindrical pendant lights and recessed ceiling cove LED tray.
  - Plush woven area rug beneath the bed with beveled edges.
- **Strict 90/10 BMesh Execution**:
  - All procedural geometry built in memory using `bmesh.new()`, `bmesh.ops.*`, and `bm.to_mesh()`.
  - Sub-second construction without UI freeze.
  - Multi-material face tagging via `face.material_index` within single-buffer meshes.
- **Modular Codebase**:
  - Clean separation into `core/materials.py`, `core/bmesh_utils.py`, `modules/bed_assembly.py`, `modules/bedding_cloth.py`, `modules/nightstand_lighting.py`, `modules/room_envelope.py`, and `assembler.py`.

### Non-Goals
- Real-time physics simulation running for minutes (instead, mathematical procedural lofting and cloth wave equations are used for instant, deterministic, sub-second execution).
- Whole-mansion exterior modeling (focus is strictly on the self-contained luxury master bedroom suite).

### Anti-Goals
- **No Monolithic Scripts**: Never put all logic into a single file.
- **No Unfilleted Sharp Edges**: Zero unfilleted primitives per the Anti-Boxy mandate.
- **No Flat Stickers**: Pillows and blankets must have genuine 3D volume, loft, and draping.

---

## 3. 4-Phase Pipeline Integration

```
[Prompt: "luxury bedroom with king bed, pillows, chadar, nightstands"]
       │
       ▼
Step 1: generate_spatial_blueprint(domain="INTERIOR_SPACES", query)
       │  • Dimensions: Length 4.5m, Width 4.0m, Height 2.8m
       │  • Ergonomic Clearances: Walkway 0.9m, Bedside gap 0.75m
       │  • Anti-Boxy Mandates: Required bevels, cushion loft formula
       ▼
Step 2: get_component_tree(archetype="BEDROOM") & archetype="BED"
       │  • Systems: room_envelope, trim_carpentry, built_in_millwork,
       │             ambient_lighting, cushion_assemblies, frame_and_chassis
       ▼
Step 3: bmesh Procedural Construction (C-RAM, Zero UI Freeze)
       │  • Materials creation & shader node wiring
       │  • Modular component instancing via BMesh
       ▼
Step 4: validate_phase_gate(phase_id=2) [Gate G2 Anti-Boxy Check]
       │  • Verified component_strategies:
       │    - bed_frame: "boolean_bevel"
       │    - fluted_headboard: "subdivision_cage"
       │    - mattress_cushion: "subdivision_cage"
       │    - pillows_layered: "subdivision_cage"
       │    - chadar_duvet: "subdivision_cage"
       │    - nightstands: "boolean_bevel"
       │    - pendant_lighting: "bezier_curve"
       │    - room_envelope: "boolean_bevel"
```

---

## 4. Architectural Component Decomposition & Module Structure

```
luxury_bedroom/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── materials.py         # Multi-material PBR palettes (Walnut, Linen, Velvet, Brass, Parquet)
│   └── bmesh_utils.py       # Math & procedural geometric operators (cushion loft, bevel box, cloth ripple)
├── modules/
│   ├── __init__.py
│   ├── bed_assembly.py      # Floating platform frame, fluted headboard, mattress
│   ├── bedding_cloth.py     # Organic pillows with piping, draped chadar/duvet with folds
│   ├── nightstand_lighting.py # Floating nightstands & suspended brass pendant lights
│   └── room_envelope.py     # Walls, parquet flooring, acoustic wood slat wall, cove ceiling, rug
└── assembler.py             # Orchestrates 4 phases, runs BMesh construction, validates Gate 2
```

---

## 5. Technical Specifications

### Bed & Bedding Dimensions
- **Bed Frame**: 2.04m (W) $\times$ 2.14m (L) $\times$ 0.32m (H), recessed plinth 0.12m from edges.
- **Headboard**: 2.40m (W) $\times$ 0.10m (D) $\times$ 1.30m (H), 12 vertical fluted padded velvet channels with 0.02m bevel radii.
- **Mattress**: 1.96m (W) $\times$ 2.06m (L) $\times$ 0.28m (H), beveled crown contour.
- **Sleeping Pillows (2x)**: 0.75m $\times$ 0.48m $\times$ 0.16m, tilted at 15°, crowned loft equation $Z(u,v) = z_0 + 0.08 \cdot (1-u^2)(1-v^2)$.
- **Decorative Pillows (2x)**: 0.60m $\times$ 0.40m $\times$ 0.14m, resting in front of sleeping pillows.
- **Accent Cushion (1x)**: 0.45m $\times$ 0.28m $\times$ 0.10m, center lumbar placement.
- **Chadar / Duvet**: 2.00m (W) $\times$ 1.70m (L) covering 75% of the bed length, with turned-down top cuff (0.25m fold), side drape overhang (0.15m drop over left, right, and foot edges), and sinusoidal ripple displacement ($A = 0.015m, \lambda = 0.25m$).

### Room Dimensions & Lighting
- **Room Envelope**: 4.8m (X) $\times$ 4.2m (Y) $\times$ 2.85m (Z).
- **Acoustic Slat Accent Wall**: 3.2m (W) centered behind bed, composed of 32 vertical walnut slats (0.05m wide $\times$ 0.02m deep with 0.03m acoustic felt gaps).
- **Nightstands**: Floating cantilevered box 0.55m (W) $\times$ 0.42m (D) $\times$ 0.22m (H), placed at $Z = 0.45m$.
- **Pendant Lights**: Cylindrical brass fixtures ($\varnothing 0.08m \times 0.35m$) suspended from ceiling with glowing warm light diffuser.
- **Area Rug**: 3.4m $\times$ 2.8m placed under lower 70% of the bed extending past the nightstands.
