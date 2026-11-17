---
name: blender-spatial-thinking-planner
description: >
  Universal 3D spatial thinking, reference deconstruction, tool mapping, and modular
  planning skill for Blender MCP agents. Enforces multi-angle reference analysis,
  physical surface classification, anti-boxy geometry allocation (walls vs soft goods),
  live FastMCP tool mapping, socratic clarification, and strict modular code architecture.
  Load before creating, planning, or editing any 3D asset or scene.
---

# Blender Universal Spatial Thinking & Modular Planning Contract

## 0. Executive Mandate & Non-Negotiables

Every 3D modeling request processed through Blender MCP must pass through the **6 Cognitive Phases** before writing or executing any code. 

### The 4 Non-Negotiable Iron Laws:
1. **The Anti-Boxy Law**: Never use a primitive box, cylinder, or naive extrusion to represent an organic, pliable, or sculpted shape. Soft goods (pillows, cushions, mattresses, cloth) must exhibit physical curvature, perimeter seams, pinched corners, and parabolic crown lofting.
2. **The Geometry Allocation Law**: Geometry is expensive and deliberate. Never waste subdivision or dense geometry nodes on flat architectural envelopes (walls, floors, slabs). Conversely, never starve soft goods or silhouette-critical curves of geometry.
3. **The Tool Mapping Law**: Every component in an asset must be explicitly mapped to an existing FastMCP tool or verified BMesh technique with a documented technical justification. Never guess or hallucinate non-existent tool names.
4. **The Modular Architecture Law**: Monolithic scripts (>250 lines) are strictly banned. Every asset must be decomposed into modular prefabs, shared materials, and an assembly coordinator (`core/materials.py`, `prefabs/<feature>_kit.py`, and `main.py`).

---

## 1. The 6 Cognitive Phases

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Multi-Angle Reference & Domain Deconstruction                 │
│ └─ Break down request into hierarchical components & datum planes      │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 2: Physical & Material Classification                            │
│ └─ Classify into Architecture, Hard CAD, Soft Goods, or Slender Curves │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 3: Geometry & Budget Allocation Matrix                           │
│ └─ Zero-waste flats vs. high-density parabolic lofts & seam loops      │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 4: Live MCP & Native Tool Selection Matrix                       │
│ └─ Map components to create_cushioned_profile, sweep_molding, etc.     │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 5: Socratic Clarification & Inquiry Gate                         │
│ └─ Resolve ambiguities with 1-2 focused questions before coding        │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 6: Modular Code Architecture Mandate                             │
│ └─ Generate modular kits & prefabs; enforce 90/10 Hybrid Pipeline      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Multi-Angle Reference & Domain Deconstruction

When the user provides reference images (front, side, top, isometric) or descriptions:
1. **Datum Plane Alignment**: Lock the coordinate axes.
   - Front View ($X/Z$): Establishes overall height, profile contour, and horizontal symmetry.
   - Side View ($Y/Z$): Establishes depth, lean/camber, and longitudinal cross-sections.
   - Top View ($X/Y$): Establishes perimeter footprint and clearance.
2. **Component Tree Decomposition**: Decompose the object into primary structural systems, secondary sub-assemblies, and tertiary details.
   - Example (Bed): Frame chassis, slatted base, mattress core, topper, pillows (sleeping + accent), duvet blanket, headboard upholstery, nightstands.
3. **Passes Hierarchy (Primary -> Secondary -> Tertiary)**:
   - *Primary*: Macro-proportions and silhouette bounds (verified in real-world metric units).
   - *Secondary*: Form cuts, bevels, apertures, cushion crowning, and recess panels.
   - *Tertiary*: Seam welts, stitching, tufting buttons, surface wrinkles, fasteners, and hardware.

---

### Phase 2: Physical & Material Classification

Classify every single component into one of four physical surface domains:

| Domain Class | Physical Characteristics | Common Examples | Primary Construction Rule |
| :--- | :--- | :--- | :--- |
| **Class A: Architectural Envelope** | Rigid, planar, rectilinear, structural | Walls, ceilings, floors, window reveals | Minimal polygon quads (1 quad per wall face). Bevel or molding at perimeter. Zero subdiv. |
| **Class B: Precision Hard CAD** | Rigid, machined, dimensional, precise | Furniture frames, legs, handles, electronic dials, chassis | Millimeter coordinates, `Shift+D X [dist]`, uniform grid cuts before booleans, quad repair. |
| **Class C: Organic Soft Goods** | Pliable, non-rigid, pressurized, inflated, draped | Pillows, cushions, mattresses, folded duvets, curtains | Parabolic crown dome $Z(u,v) = Z_0 + h_{crown}(1-u^2)(1-v^2)$, perimeter welts, pinched corners, Sub-D level 2. |
| **Class D: Slender Curved Extrusions** | Continuous centerline curvature, radial thickness | Hair locks, cables, pipes, ropes, welt piping | Bezier 3D curve with Bevel Depth/Object + `Alt+S` radius tapering. |

---

### Phase 3: Geometry & Budget Allocation Matrix

#### Architectural Envelope Discipline (Anti-Waste):
- Walls and flat floors do not bend; they reflect light uniformly.
- **Rule**: Never apply Subdivision Surface or dense procedural Geometry Nodes to planar walls. Use `create_architectural_wall` to generate exact openings and `create_profile_sweep_molding` for trim.

#### Soft Goods & Cloth Discipline (Anti-Boxy):
- A pillow or cushion is NOT a beveled cube. It is an inflated textile membrane under tension.
- **Mandatory Anatomy of a Pillow/Cushion**:
  1. **Perimeter Seam (Piping / Welt)**: The boundary edge where fabric pieces are stitched.
  2. **Parabolic Crown Loft**: The center swells convexly. Given normalized coordinates $u, v \in [-1, 1]$:
     $$Z(u,v) = Z_0 + h_{crown} \cdot (1 - u^2)(1 - v^2)$$
  3. **Pinched Corners**: At $(u=\pm 1, v=\pm 1)$, fabric tension pulls the corners tight and flat.
  4. **Subdivision Cage**: Minimum 8×8 quad topology with `setup_subdivision_cage(levels=2)` and Smooth Shading.

---

### Phase 4: Live MCP & Native Tool Selection Matrix

Always select tools from the verified FastMCP and BMesh toolkit across the 9 Major Production Systems:

| Component Role / Production Stage | Verified FastMCP Tool | Native Blender Technique | Technical Justification |
| :--- | :--- | :--- | :--- |
| **Pillow / Cushion / Mattress** | `create_cushioned_profile` | BMesh parabolic vertex displacement + edge creases | Produces authentic lofted crown dome and perimeter welting in <10ms. |
| **Subdivision Smoothing** | `setup_subdivision_cage` | `modifiers.new(type='SUBSURF')` | Applies Catmull-Clark subdivision while preserving boundary edge creases. |
| **Walls with Openings** | `create_architectural_wall` | BMesh boolean knife / grid bridges | Creates watertight wall geometry with exact millimeter window/door cutouts. |
| **Baseboards & Cornices** | `create_profile_sweep_molding` | Curve extrusion with custom profile | Sweeps classical architectural profiles along room boundaries cleanly. |
| **Cables, Pipes, Hair** | `create_bezier_tube` | Bezier Spline + Bevel Object + `Alt+S` | Spline-based control with smooth tangent interpolation and tapered tips. |
| **Curved Hard-Surface Cuts** | `clas_boolean_carve` | Pre-boolean grid cuts + `LoopTools Circle` | Cuts round apertures into quad grids without ruining edge flow. |
| **Curvature Shading Artifact Fix** | *N/A (Modifier Stack)* | **Shrinkwrap Modifier** on target Vertex Group | Completely eliminates shading pinching on complex curved fillet transitions. |
| **PBR Material Assignment** | `assign_pbr_material`, `modify_material_property` | Principled BSDF socket configuration | Version-aware socket lookup (Blender 3.x–5.x LTS) with multi-slot support. |
| **Procedural Surface Shaders** | `create_procedural_shader` | Procedural node networks (15 presets: wood, marble, metal, concrete, etc.) | Physically believable materials with micro-roughness and bump without external image dependencies. |
| **Shader Tree Validation** | `inspect_material_nodes`, `validate_material_setup` | Node tree graph connectivity audit | Detects disconnected nodes, missing outputs, or zero-roughness mirrors before rendering. |
| **Studio & Cinematic Lighting** | `setup_studio_lighting`, `setup_environment_hdri` | 10 calibrated rigs (`three_point`, `cinematic`, `dramatic_rim`, etc.) + World HDRI | Dynamic energy/distance scaling to object bounds, Kelvin-to-RGB color balance, dedicated collection. |
| **Camera Framing & DoF Bokeh** | `frame_camera_to_object`, `setup_camera_dof`, `create_turntable_camera` | Sensor-aware FOV trigonometry, TrackTo constraints, orbit keyframes | Precise optical framing with rule-of-thirds offsets, hero angles, and aperture blade bokeh. |
| **Automated Mesh Repair** | `repair_mesh_topology` | BMesh non-manifold repair, weld doubles, recalculate normals | Cleans degenerates and loose geometry in memory (<10ms) before sub-d or booleans. |
| **Quad Remeshing & Decimation** | `quad_remesh`, `decimate_mesh`, `generate_lod_chain` | QuadriFlow remeshing & ratio decimation | Generates clean uniform quad flow or multi-tier game LOD chains (LOD0–LOD3) preserving UVs. |
| **Cloth Physics & Draping** | `setup_cloth_physics`, `bake_cloth_drop` | Headless iterative frame stepping + evaluated mesh freeze | Natural fabric folds and draping for bedsheets, tablecloths, curtains, and throws. |
| **Surface Snapping & Alignment** | `snap_to_surface`, `align_object_to_surface` | Bounding-box raycast snapping + surface normal reorientation | Seats props flush on floors, desks, or walls with zero manual coordinate guesswork. |
| **Memory-Efficient Instancing** | `scatter_instances`, `inspect_scatter_result` | Shared mesh datablocks (`Alt+D` instancing) | Batches thousands of debris, books, or foliage props with Poisson disk spacing and near-zero memory footprint. |
| **Modifier Stack Pipeline** | `apply_modifier_stack`, `inspect_modifier_stack`, `freeze_modifiers` | Declarative modifier order enforcement & selective evaluation | Builds reliable bevel -> mirror -> subsurf chains and freezes them safely to static meshes. |
| **Mechanical & Vehicle Rigging** | `setup_vehicle_rig`, `setup_hinge_constraint`, `setup_mechanical_pivot` | Empty hierarchy, Limit Rotation constraints, child-of parenting | Rig vehicles with steering/suspension, cabinets/doors with swing limits, and mechanical hinges. |
| **Scene Checkpoints & Safe Mode** | `create_scene_checkpoint`, `restore_scene_checkpoint` | Non-destructive `.blend` snapshots & rollback indexing | Mandatory pre-flight safeguard before running destructive remeshing, boolean, or freezing operations. |
| **Topology & Manifold QA** | `audit_mesh_topology` | `bmesh.ops.find_doubles`, check `is_manifold` | Verifies zero non-manifold edges, zero boundary holes, and quad integrity. |
| **Game Asset Export & UVs** | `apply_uv_unwrap`, `export_game_asset` | Smart UV Project with margin isolation | Enforces clean UV islands and evaluated triangle budget decimation. |

---

### Phase 5: Socratic Clarification & Inquiry Gate

Before jumping into code, evaluate if the user's prompt or references leave major design choices open:
- **When to Ask**:
  - Missing functional specs (e.g., "Is the headboard tufted chesterfield style or smooth vertical fluting?").
  - Budget/Platform trade-offs (e.g., "Real-time game asset (<15k tris) or hero architectural render (subdivision enabled)?").
  - Occluded views in reference images (e.g., "The backside of the nightstand is not visible; should it include rear cable management cutouts?").
- **Questioning Rules**:
  - Ask at most 1-2 sharp questions.
  - Provide concrete, labeled options with a recommended default.
  - Never ask about trivial implementation details (file paths, tool syntax).

---

### Phase 6: Modular Code Architecture Mandate

**Strict Rule: Never output a single monolithic script (>250 lines).**

Every asset or scene must follow the modular 4-tier structure:
```
<project_name>/
├── core/
│   ├── __init__.py
│   ├── materials.py       # PBR shaders (Principled BSDF, roughness, normal maps)
│   └── mesh_utils.py      # BMesh helpers (transforms, matrix multiplications)
├── prefabs/
│   ├── __init__.py
│   ├── arch_kit.py        # Walls, floor slabs, ceiling, baseboards
│   ├── <asset>_kit.py     # Main prop geometry (e.g., bed_kit.py, car_chassis_kit.py)
│   └── soft_goods_kit.py  # Pillows, cushions, duvets, drapery
└── main.py                # Scene assembler, Alt+D linked instances, lighting & camera
```

#### The 90/10 Hybrid Pipeline Standard:
- **Zone A (`bmesh` + `bpy.data`) (90%)**: All geometry creation, vertex positioning, and face tagging run in memory. Sub-second execution.
- **Zone B (`bpy.ops`) (10%)**: Strictly reserved for scene I/O, file loading, and final render.
- **Single-Buffer Merging**: Batch scatter items into a single `bmesh` before writing to mesh data.
- **Shared Mesh Instancing (`Alt+D`)**: Create the master mesh once; instance across objects with transforms.

---

## 2. Mandatory Pre-Planning Gate

Before writing any implementation script, the agent MUST output a plan matching `templates/spatial-execution-plan-template.md` containing:
1. Reference Evidence & Datum Matrix.
2. Component Breakdown Table with Domain Class, Geometry Budget, Tool Selection, and "Why".
3. Modular File Structure Mapping.
4. Resolved/Proposed Clarifications.

Only after presenting this plan may the agent proceed to generate modular code.

---

## 3. Mandatory Safety & Scene Checkpoint Policy

Before executing any high-risk or destructive operation:
1. **Always Create a Checkpoint**: Invoke `create_scene_checkpoint(label="pre_destructive_op")` before running `quad_remesh`, `decimate_mesh`, `freeze_modifiers`, heavy boolean cuts, or large-scale cloth bakes.
2. **Verify After Operation**: Inspect geometry via `audit_mesh_topology`, `inspect_modifier_stack`, or `inspect_cloth_simulation`.
3. **Instant Rollback on Failure**: If self-intersections, non-manifold tears, or mesh corruption occur, call `restore_scene_checkpoint()` immediately to return the scene to its verified clean state without data loss.
