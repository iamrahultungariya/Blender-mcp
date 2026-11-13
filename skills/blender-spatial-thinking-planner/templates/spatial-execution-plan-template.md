# 3D Spatial Execution & Tooling Plan: [Asset / Scene Name]

> **Execution Directive**: This plan must be approved before generating or executing any procedural 3D modeling scripts. Monolithic scripts (>250 lines) are strictly prohibited.

---

## 1. Request Deconstruction & Reference Matrix

* **Request Type**: [Image-led | Text-led | Hybrid]
* **Target Domain**: [Class A: Architectural Envelope | Class B: Hard CAD | Class C: Soft Goods | Class D: Curves]
* **Real-World Metric Bounds**:
  * Width ($X$): `[e.g., 2.20 m]`
  * Depth ($Y$): `[e.g., 2.40 m]`
  * Height ($Z$): `[e.g., 1.10 m]`

### Reference & Datum Alignment Matrix
| Datum / Feature | Front View (X/Z) | Side View (Y/Z) | Top View (X/Y) | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Ground Line** | $Z = 0.0$ | $Z = 0.0$ | - | HIGH |
| **Primary Footprint** | $X \in [-1.1, 1.1]$ | $Y \in [0.0, 2.4]$ | $2.2 \times 2.4\text{ m}$ | HIGH |
| **Secondary Transition** | [e.g., Mattress top $Z=0.55$] | [e.g., Headboard back $Y=0.0$] | - | HIGH |
| **Tertiary Details** | [e.g., Seam welt radius $12\text{mm}$] | - | [e.g., Pillow spacing] | MEDIUM (Inferred) |

---

## 2. Component Decomposition & Tool Selection Matrix

| Component ID | Component Name | Domain Class | Est. Triangles | FastMCP / Native Tool | Technical Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C-01** | North Wall | Class A | 12 tris | `create_architectural_wall` | Planar envelope; 1 quad span with door reveal. Zero subdiv waste. |
| **C-02** | Room Baseboard | Class A | 96 tris | `create_profile_sweep_molding` | Clean 2D profile sweep along wall path. |
| **C-03** | Bed Frame Chassis | Class B | 240 tris | BMesh Box + Bevel | Rigid structural base; 2-segment bevel on corners. |
| **C-04** | Sleeping Pillows (x2) | Class C | 1,536 tris ea | `create_cushioned_profile` + Sub-D | Parabolic crown dome ($h_{crown}=0.05\text{m}$), perimeter seam, pinched corners. |
| **C-05** | Duvet Blanket | Class C | 2,048 tris | BMesh Draped Quads + Sub-D | Pliable folded textile; natural gravity sag and overhang. |
| **C-06** | Lamp Cords | Class D | 256 tris | `create_bezier_tube` | Spline curve with bevel depth and tapered ends (`Alt+S`). |

---

## 3. Socratic Clarifications & Design Choices

* **Clarification 1**: [e.g., "The reference shows decorative wall paneling. Do you prefer modern vertical acoustic slats or classical picture-frame molding?"]
  * **Option A (Recommended)**: Vertical acoustic oak slats via single-buffer BMesh merging.
  * **Option B**: Classical wainscoting via `create_profile_sweep_molding`.
* **Clarification 2**: [e.g., "Pillow arrangement: 2 sleeping pillows flat, or 2 propped upright with 2 decorative accent pillows?"]
  * **Selected Default**: 2 sleeping pillows propped at 15° against headboard + 2 square accent cushions.

---

## 4. Modular Code Architecture Mapping

```
<scene_package>/
├── core/
│   ├── materials.py       # PBR shaders: VelvetFabric, NaturalOakWood, MattePlaster, BrushedBrass
│   └── mesh_utils.py      # Matrix transforms, BMesh tagging, normal recalculation
├── prefabs/
│   ├── arch_kit.py        # create_walls(), create_baseboards()
│   ├── bed_kit.py         # create_bed_frame(), create_mattress()
│   └── soft_goods_kit.py  # create_pillow_master(), create_folded_duvet()
└── main.py                # assemble_scene(): Alt+D pillow instances, 3-point lighting, Nishita sky, camera
```

---

## 5. Phase-by-Phase Execution Checklist

- [ ] **Phase 1**: Verify scene metric units (Meters) and initialize `core/materials.py`.
- [ ] **Phase 2**: Generate Class A structural envelope (`prefabs/arch_kit.py`).
- [ ] **Phase 3**: Generate Class B rigid furniture frame (`prefabs/bed_kit.py`).
- [ ] **Phase 4**: Generate Class C soft goods with parabolic crown loft (`prefabs/soft_goods_kit.py`).
- [ ] **Phase 5**: Assemble scene in `main.py` using `Alt+D` shared instancing.
- [ ] **Phase 6**: QA mesh topology using `audit_mesh_topology` (0 non-manifold edges, verified budget).
