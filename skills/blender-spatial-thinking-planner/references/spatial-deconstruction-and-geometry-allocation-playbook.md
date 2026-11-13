# Spatial Deconstruction & Geometry Allocation Playbook

## 1. Intent & Purpose

This playbook provides the definitive engineering framework for deconstructing 2D/3D reference imagery, establishing spatial datum lines, classifying physical materials, and deliberately allocating polygon budgets.

---

## 2. Multi-Angle Reference Fusion

When modeling from multiple reference angles (e.g., Front, Side, Top, Perspective), never treat each view as an isolated 2D sketch. You must build a unified **Spatial Datum Matrix**:

```
                 Z (Height)
                 ▲
                 │     [Front View: Width X vs Height Z]
                 │     [Side View:  Depth Y vs Height Z]
                 │
                 └──────────────► X (Width)
                /
               /
              ▼ Y (Depth) [Top View: Width X vs Depth Y]
```

### Steps for Reference Fusion:
1. **Identify Common Datums**:
   - **Ground Line ($Z=0.0$)**: The contact surface (floor, tires, chassis base).
   - **Centerline Symmetry Plane ($X=0.0$)**: Mirror plane for bilateral symmetric objects.
   - **Primary Datum Bounds**: Max height ($Z_{max}$), max width ($X_{max}$), max depth ($Y_{max}$).
2. **Reconcile Perspective Distortion**:
   - Perspective photos suffer from lens foreshortening (focal length typically 24mm–50mm).
   - Cross-verify proportions using feature ratios: $\frac{\text{Headboard Height}}{\text{Mattress Length}}$, $\frac{\text{Wheel Diameter}}{\text{Wheelbase}}$.
   - If Front and Side views contradict, favor orthographic technical drawings over artistic perspective renders.

---

## 3. The 3 Modeling Passes (Primary -> Secondary -> Tertiary)

As taught in core modeling principles, attempting to model final details in pass 1 always leads to lumpy, unmanageable geometry.

```mermaid
flowchart LR
    A["Pass 1: Primary Forms<br/>(Macro Proportions, Bounding Volumes)"] --> B["Pass 2: Secondary Features<br/>(Bevels, Apertures, Lofts, Cutouts)"]
    B --> C["Pass 3: Tertiary Micro-Details<br/>(Piping Seams, Wrinkles, Hardware)"]
```

### Pass 1: Primary Forms (Macro Proportions)
- Create low-resolution blockout volumes matching outer bounding boxes.
- Zero bevels, zero subdivision, zero seams.
- Immediately execute `Ctrl + A > Scale` to freeze transforms to $(1.0, 1.0, 1.0)$.
- Verify metric dimensions: A standard king mattress is $1.8\text{m} \times 2.0\text{m} \times 0.25\text{m}$; an interior wall is $2.8\text{m} - 3.2\text{m}$ high with $0.15\text{m} - 0.25\text{m}$ thickness.

### Pass 2: Secondary Features (Form & Curvature)
- Introduce major functional transitions:
  - Hard surface: Chamfers, fillet bevels, boolean openings.
  - Soft goods: Parabolic crown curvature, edge pinch loops.
  - Architecture: Door/window reveals, recessed niches, step profiles.
- Keep polygon density strictly quad-dominant.

### Pass 3: Tertiary Details (Micro & Surface Storytelling)
- Edge welts, stitching, tufting depression buttons, tension fold creases.
- Fasteners, screws, cable connectors.
- Subtle organic variations (random rotation of pillows, drape sag).

---

## 4. Physical Surface Classification & Geometry Budgeting

Every component in a 3D scene belongs to one of four physical regimes. Allocating geometry inversely to these rules is the #1 cause of AI modeling failure.

### Class A: Architectural Envelope (Planar Surfaces)
* **Components**: Walls, ceilings, floors, flat partitions, cabinet carcasses.
* **Physical Nature**: Perfectly planar, rigid, static. Light reflects uniformly across the face.
* **Geometry Rule**: **MINIMAL TOPOLOGY (1 quad per wall face)**.
  - Adding subdivision to a flat wall creates zero visual improvement while multiplying polygon count by $16\times$ and bloating BVH build times.
  - Detail belongs strictly on the perimeter: baseboards, crown molding, door jambs. Use `create_architectural_wall` and `create_profile_sweep_molding`.

### Class B: Precision Hard CAD & Mechanical
* **Components**: Table frames, metal legs, door handles, electronics, chassis.
* **Physical Nature**: Rigid, machined, dimensional. Sharp corners catch specular highlights.
* **Geometry Rule**: **CONTROLLED QUAD BEVELS & UNIFORM PRE-BOOLEAN GRIDS**.
  - All sharp edges must have at least a 2-segment bevel or edge crease (pure 90-degree mathematical edges do not exist in reality).
  - Pre-Boolean rule: Dense uniform grid loops before boolean cutting; resolve N-gons into quads; apply **Shrinkwrap Modifier** on vertex group to eliminate shading pinching.

### Class C: Organic Soft Goods (Pillows, Cushions, Draped Fabric)
* **Components**: Pillows, sofa cushions, mattresses, duvets, blankets, curtains.
* **Physical Nature**: Pliable, flexible, filled with foam or down feathers under internal pressure.
* **Geometry Rule**: **CROWNED PARABOLIC LOFT + PERIMETER SEAM + SUB-D CAGE**.
  - Never model a pillow as a cube with beveled edges!
  - **The 3D Anatomy of a Pillow**:
    1. **Perimeter Seam (Welt Line)**: The outer boundary stays pinned at baseline $Z_0$.
    2. **Parabolic Crown Dome**: The center rises to maximum crown height $h_{crown}$. For normalized coordinates $u \in [-1, 1], v \in [-1, 1]$:
       $$Z(u, v) = Z_0 + h_{crown} \cdot (1 - u^2)(1 - v^2)$$
       For a standard $0.6\text{m} \times 0.4\text{m}$ sleeping pillow with thickness $0.16\text{m}$, the crown height $h_{crown} \approx 0.05\text{m}$ above the seam.
    3. **Pinched Corners**: At $(\pm 1, \pm 1)$, fabric tension pulls the seam inwards and flattens the dome.
    4. **Subdivision Cage**: Minimum 8×8 quad topology with `setup_subdivision_cage(levels=2)`.

### Class D: Slender Curved Extrusions
* **Components**: Cables, power cords, pipes, decorative piping cords, stylized hair strands.
* **Physical Nature**: Continuous 3D curves with circular or oval cross-sections.
* **Geometry Rule**: **BEZIER 3D CURVES WITH BEVEL OBJECT & TAPER**.
  - Add `Curve > Bezier`, set 3D mode.
  - Set `bevel_depth` or use a `Curve > Circle` as `bevel_object`.
  - Use `Alt + S` on end control vertices to taper tips smoothly (as demonstrated in stylized character modeling).

---

## 5. Geometry Allocation Matrix Comparison

| Scene Asset | Component | Domain Class | Allocation Strategy | Target Tris | FastMCP / Native Tool |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Luxury Bedroom** | North Wall | Class A | 1 quad face + door cutout | 12 tris | `create_architectural_wall` |
| **Luxury Bedroom** | Baseboard | Class A | Swept 2D profile along path | 96 tris | `create_profile_sweep_molding` |
| **Luxury Bedroom** | Mattress Core | Class B/C | Rounded box + edge loops | 180 tris | BMesh Box + Bevel |
| **Luxury Bedroom** | Sleeping Pillow | Class C | Parabolic dome + perimeter seam | 1,536 tris | `create_cushioned_profile` + Sub-D |
| **Luxury Bedroom** | Accent Pillow | Class C | Parabolic dome + pinched corners | 1,024 tris | `create_cushioned_profile` + Sub-D |
| **Luxury Bedroom** | Reading Lamp Cord | Class D | 3D Bezier curve with bevel | 256 tris | `create_bezier_tube` |
| **Luxury Bedroom** | Nightstand Drawer | Class B | Inset front + chamfered handle | 120 tris | BMesh Inset + Bevel |
