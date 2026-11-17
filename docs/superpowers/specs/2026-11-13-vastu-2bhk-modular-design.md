# Indian Vastu 2BHK Luxury Residence: Modular Architecture & Game-Dev Asset Kit Design

**Date:** 2026-11-13  
**Status:** Approved Design Document  
**Triangle Budget:** 400,000 Triangles (400k tris / ~200k quads)  
**Visual Reference:** `vastu_luxury_2bhk_cutaway_1794547442188.jpg`  

---

## 1. Intent & The "Why"
Previous iterations generated the entire house inside a single monolithic procedural script using crude geometric cuboids (`add_box`), causing unnatural sharpness, lack of organic curves, and critical geometric defects (such as door leaves forming giant diagonal bounding boxes that barricaded doorways).

This design establishes a professional **Game-Engine Modular Prefab Architecture**:
- Each asset is treated as a high-fidelity reusable component (Prefab) built once in BMesh and instanced via shared mesh data / matrix transforms.
- Geometry uses real architectural curves: curved organic boucle sofas, fluted velvet headboards, lathe-profiled turned pillars, bullnose countertop bevels, and D-shaped sanitary porcelain.
- Door assemblies are decoupled into **Modular Door Frames** and **Hinged Thin Door Leaves** pivoted realistically on hinge points ($Z$-axis rotation), ensuring zero doorway obstruction.

---

## 2. Goals, Non-Goals & Anti-Goals

### Goals
- **400k Triangle Budget Utilization**: Allocate generous geometric resolution (subdivisions, rounded fillets, lathe rings, cushion creases) to achieve AAA architectural visualization quality matching the reference concept.
- **Strict Vastu Shastra Compliance**:
  - **South-West (Nairutya)**: Master Bedroom with king bed (head to South per Vastu) & heavy wooden wardrobe along West wall.
  - **South-East (Agni)**: Modular Kitchen & Dining. Cooktop in SE (cook faces East). Undermount sink in NE of kitchen.
  - **North-East (Ishanya)**: Open living lounge & authentic carved wooden Pooja Mandir with brass bells and diya in the NE corner.
  - **North-West (Vayu)**: 2nd Bedroom & Ergonomic Study Workstation.
  - **West (Varuna)**: Restroom & Bathroom with wall-hung WC facing North-South.
  - **Center (Brahmasthan)**: 100% open, unobstructed cosmic foyer with an inlaid marble mandala medallion.
- **Modular Game-Dev Decomposition**: Break monolithic code into clean, modular Python modules:
  - `src/core/materials.py`
  - `src/core/mesh_utils.py`
  - `src/prefabs/arch_kit.py`
  - `src/prefabs/furniture_living.py`
  - `src/prefabs/furniture_bedroom.py`
  - `src/prefabs/furniture_kitchen.py`
  - `src/prefabs/sanitary_bath.py`
  - `src/assembler.py`

### Non-Goals
- Full exterior roof / ceiling slabs (the asset is specifically an architectural dollhouse cutaway model to display interior furnishings and layout).
- Exterior multi-floor building structure.

### Anti-Goals
- **No Razor-Sharp 90° CG Edges**: Every hard surface must carry realistic bevels for specular highlights.
- **No Monolithic Blobs**: Never generate disparate room assets in one unseparated BMesh object.
- **No Blocking Door Leaves**: Never use axis-aligned bounding boxes for rotated doors; rotate the thin slab about its hinge origin.

---

## 3. Visual Reference Analysis (From Concept Render)
Based on `vastu_luxury_2bhk_cutaway_1794547442188.jpg`:
1. **Walls**: Finished white plaster with warm LED cove lighting recessed along the top cutaway perimeter. Clean openings without bulky frames blocking walkways.
2. **Flooring Transition**: Warm dark walnut parquet in bedrooms, matte slate in bathroom, polished Botticino marble across Living, Foyer, and Kitchen.
3. **Brahmasthan Medallion**: Concentric circular mandala inlay with golden bronze and cream marble tessellation.
4. **Living Room Sofas**: Organic curved C-shaped / kidney-shaped boucle sofas with cylindrical throw pillows and rounded backrest contours.
5. **Pooja Mandir**: Ornate carved teakwood structure with lathe-turned pillars, hanging brass bells, tiered shikhara roof, and glowing oil diya.
6. **Master Bed**: Floor-to-ceiling royal navy fluted vertical velvet headboard, deep padded mattress, folded runner, and globe bedside lamps.
7. **Kitchen**: Minimalist dark granite counter with seamless bullnose front edge, sleek cabinets, stainless chimney, and 4-chair dining table.

---

## 4. Triangle Budget Breakdown (400,000 Tris Total)

| Component Subsystem | Target Triangles | Key Geometry Features |
| :--- | :--- | :--- |
| **Architecture & Openings** | 50,000 tris | Plinth, multi-layered flooring, beveled walls, door frames, thin hinged doors, window mullions. |
| **Living Room & Mandir** | 100,000 tris | Curved C-sofas, barrel armchairs, marble coffee table, lathe mandir pillars, tiered shikhara, bells. |
| **Master Bedroom Suite** | 90,000 tris | Fluted 11-channel velvet headboard, bed base, curved mattress, draped duvet, pillows, wardrobe, vanity. |
| **Kitchen & Dining Suite** | 70,000 tris | Bullnose granite counter, 4-burner hob, chimney, sink/faucet, dining table, 4 curved dining chairs. |
| **2nd Bedroom / Study** | 55,000 tris | Queen bed, study desk, 5-star caster ergonomic swivel office chair, open laptop, wardrobe. |
| **Sanitary & Bathroom** | 35,000 tris | D-shaped ceramic WC, oval vessel washbasin, curved chrome faucets, rain shower arm, glass screen. |
| **Total** | **400,000 tris** | Complete AAA Real-Time Architectural Dollhouse Model |

---

## 5. Architectural Component Decomposition & Module Interfaces

```
c:\Users\Rahul\OneDrive\Desktop\Blender MCP\
├── docs/superpowers/
│   ├── specs/2026-11-13-vastu-2bhk-modular-design.md
│   └── plans/2026-11-13-vastu-2bhk-modular-implementation.md
└── vastu_modular/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── materials.py      # PBR Material palette & node setup
    │   └── mesh_utils.py     # High-poly bmesh helpers (beveled box, lathe, fluting, curves)
    ├── prefabs/
    │   ├── __init__.py
    │   ├── arch_kit.py       # Plinth, walls, door frames, hinged doors, windows, medallion
    │   ├── living_kit.py     # Curved C-sofa, tub chairs, coffee table, mandir, planter
    │   ├── bedroom_kit.py    # Master fluted bed, guest bed, nightstands, lamps, desks, wardrobes
    │   ├── kitchen_kit.py    # Counter, hob, chimney, sink, dining table & chairs
    │   └── bath_kit.py       # D-shaped WC, vanity, vessel sink, shower glass & rainshower
    └── main.py               # Master scene assembler & camera/lighting orchestrator
```

---

## 6. Approached Considered & Trade-Offs

### Approach A: Single Procedural Monolithic Script (Previous Method)
- *Pros:* Quick to execute in one pass.
- *Cons:* Unmaintainable, rigid, prone to geometric bounding-box bugs (doors blocking gates), zero reuse. **Rejected.**

### Approach B: Modular Python Package with Instanced Prefabs (Recommended)
- *Pros:* Decoupled components, high-poly geometry precision, instanced asset reuse (chairs, lamps, door leaves), exact 400k triangle budget allocation, easily testable per room.
- *Cons:* Requires structured file layout and clean orchestrator. **Selected.**

---
