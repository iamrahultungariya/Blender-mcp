# Contemporary Warm Luxury Master Bedroom Suite: Reference 3D Design Spec

**Date:** 2026-11-13  
**Status:** Approved Reference Design Document  
**Visual Reference:** Uploaded Concept Turnaround Sheet (`media_1794550685111_b4341c92.jpg`)  
**Triangle Budget:** 300,000 Triangles (~150,000 Quads / ~175,000 Vertices)  
**Architecture:** Pure Modular Prefab System (Zero monolithic `.py` files)  
**Pipeline:** 90/10 Hybrid Pipeline (`bmesh` in C-RAM, zero UI freezes, multi-material tagging)

---

## 1. Intent & Visual Reference Analysis
From the reference turnaround image (`media_1794550685111_b4341c92.jpg`):
1. **Bed & Headboard**:
   - Floating low-profile upholstered bed platform with recessed plinth creating a shadow-gap hover effect.
   - Winged segmented headboard: 3 horizontal cushioned channel pads flanked by angled side wing panels in taupe/beige textured bouclé fabric.
   - Ergonomic contoured mattress with crowned surface and beveled perimeter welt seams.
   - **6-Pillow Arrangement**:
     - 2 large white sleeping pillows leaning backwards at 15°.
     - 2 square decorative accent pillows in taupe/charcoal weave.
     - 2 front rectangular lumbar cushions.
   - **Layered Bedding**:
     - Crisp white draped duvet with folded-over top cuff revealing inner sheet.
     - Charcoal/dark taupe pleated bed runner folded neatly across the lower third of the bed.
2. **Nightstands & Tabletop Decor**:
   - Dual long floating cantilevered 2-drawer nightstands in warm walnut with horizontal brass channel reveals.
   - Dual black mushroom / dome designer table lamps emitting warm 2700K ambient illumination.
   - Ceramic potted indoor plant with layered organic leaves on the left nightstand.
3. **Foot-of-Bed Ottoman Bench**:
   - Long upholstered bench with rounded double cushion and dark recessed plinth.
4. **Lounge Corner**:
   - Ergonomic curved barrel/tub armchair with flared backrest in beige textured fabric and angled wooden legs.
   - Minimalist round pedestal martini side table with lathe-turned base.
   - Slim vertical black floor lamp with cylindrical linen shade behind the armchair.
5. **Media Wall**:
   - Floating low-profile media credenza running along the wall facing the bed.
   - Wall-mounted slim 65" TV display centered above the credenza.
   - Small tabletop decor and cascading potted greenery on the credenza edge.
6. **Wardrobe**:
   - Full-height 4-door wardrobe with tinted bronze glass panels, vertical recessed handles, and interior warm-lit shelving.
7. **Window & Drapery System**:
   - Large window aperture covered by double curtain tracks:
     - Pleated sheer white inner curtains.
     - Heavy draped floor-to-ceiling blackout side drapes.
8. **Accent Wall & Millwork**:
   - Vertical acoustic walnut slat panels on both the left and right sides.
   - Central warm-grey upholstered / architectural plaster recessed wall panel.
   - Framed horizontal mountain landscape artwork centered over the headboard.
   - Recessed vertical LED light channels illuminating the slat transitions.
9. **Ceiling & Chandelier**:
   - Dropped false ceiling tray with continuous warm indirect LED cove lighting.
   - Suspended circular halo ring LED chandelier with 3 thin suspension cables.
10. **Flooring & Area Rug**:
    - Large-format warm grey travertine / marble floor tiles with subtle grout lines.
    - Large textured plush area rug beneath the bed extending outward.

---

## 2. 300,000 Triangle Budget Breakdown

| Module | Target Triangles | Key Topology & Geometry Features |
| :--- | :--- | :--- |
| **`prefabs/bed_hero.py`** | 85,000 tris | Winged segmented headboard, 6 layered pillows, organic draped duvet with folded cuff, pleated runner |
| **`prefabs/room_envelope.py`** | 60,000 tris | 56 vertical walnut slats, travertine tile grid, ceiling cove tray, framed landscape art, plush rug |
| **`prefabs/lounge_corner.py`** | 35,000 tris | Curved tub armchair with ergonomic contours, lathe pedestal table, vertical floor lamp |
| **`prefabs/window_curtains.py`** | 25,000 tris | Sinusoidal high-density pleated double drapery folds (sheer + blackout) |
| **`prefabs/nightstands.py`** | 25,000 tris | Dual floating consoles, black dome mushroom lamps, potted tabletop plant |
| **`prefabs/media_wall.py`** | 25,000 tris | Floating credenza with beveled drawer fronts, wall-mounted slim TV, tabletop decor |
| **`prefabs/wardrobe.py`** | 20,000 tris | 4-door bronze glass wardrobe with vertical recessed pulls and lit shelving |
| **`prefabs/bench_ottoman.py`** | 15,000 tris | Double-crowned cushion with perimeter welt seams and recessed base |
| **`prefabs/chandelier.py`** | 10,000 tris | Extruded circular torus halo ring with inner emissive LED strip & suspension wires |
| **Total Scene Budget** | **~300,000 tris** | **Complete AAA Real-World Photorealistic Luxury Bedroom Suite** |

---

## 3. Modular Prefab File Architecture

```
luxury_bedroom/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── materials.py         # Complete PBR palette: Travertine, Walnut, Taupe Boucle, White Linen, Charcoal Fabric, Brass, Glass, LED
│   └── bmesh_utils.py       # High-density procedural math: Parabolic lofts, pleated cloth waves, lathe turning, beveled boxes
├── prefabs/
│   ├── __init__.py
│   ├── bed_hero.py          # Winged bed frame, headboard, mattress, 6 pillows, duvet, runner
│   ├── nightstands.py       # Dual floating consoles, black dome mushroom lamps, tabletop plant
│   ├── bench_ottoman.py     # End-of-bed upholstered bench with double cushion
│   ├── lounge_corner.py     # Curved barrel tub chair, pedestal table, floor lamp
│   ├── media_wall.py        # TV credenza, wall TV, decorative accessories
│   ├── wardrobe.py          # Full-height 4-door bronze glass wardrobe
│   ├── window_curtains.py   # Pleated double curtains (sheer + blackout)
│   ├── chandelier.py        # Circular halo ring LED chandelier
│   └── room_envelope.py     # Travertine floor, fluted slats wall, cove ceiling, rug, mountain art
└── assembler.py             # Master orchestrator executing 300k budget in live Blender scene
```
