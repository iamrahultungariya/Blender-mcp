---
name: blender-geometry-engineering
description: >
  Geometry-first engineering skill for Blender MCP agents. Use when creating,
  refining, repairing, or validating meshes and continuous surfaces where
  geometric accuracy, topology integrity, curvature, cross-sections, surface
  continuity, or reference deviation matter. Complements blender-artist-workflow:
  the artist skill defines the asset and workflow; this skill engineers and
  verifies the geometry. Does not own materials, UVs, lighting, presentation,
  or final asset delivery.
---

# Blender Geometry Engineering

## 0. Mission and authority

Build geometry that is structurally valid, mathematically controlled, dimensionally
consistent, and faithful to the intended shape. A smooth render is not proof of
good geometry. A high polygon count is not proof of accuracy.

**Core principle:**
> Define datums → construct profiles and sections → generate surfaces → validate
> topology and continuity → measure deviation → repair locally → verify again.

### 0.1 Scope

This skill owns:
- Mesh and surface construction strategy.
- Cross-section/profile design and alignment.
- Mesh topology, edge flow, poles, boundary loops and patch layout.
- G0/G1/G2 continuity reasoning and verification.
- Curvature, normals, silhouette and geometric deviation checks.
- Manifoldness, degenerates, duplicate geometry and self-intersections.
- Boolean cleanup, bevel integrity, subdivision behavior and local repair.
- Geometry-specific evidence and acceptance gates.

This skill does **not** own:
- Deciding what asset the user requested or interpreting the full reference brief.
- Overall project phases, scene presentation, materials, UVs, lighting or rendering.
- LOD/export policy, file delivery, rigging or animation unless geometry validation
  directly depends on them.

Use the skill-system sequence:
- `blender-preproduction-intelligence` defines the approved asset brief, scope, constraints, and build intent.
- `blender-visual-reference-intelligence` produces evidence-backed views, landmarks, component relationships, and uncertainty labels.
- `blender-geometry-engineering` (this skill) constructs and verifies geometry.
- `blender-artist-workflow` coordinates the wider scene workflow, task sequencing, materials, presentation, and delivery.
Invoke this skill for geometry tasks within that workflow. Do not duplicate the other skills' full pipelines. If a named skill is unavailable, do not pretend it was invoked; request or reconstruct only the missing handoff information.

### 0.2 Non-negotiable rules

1. Never claim a geometric property was verified unless the relevant check ran.
2. Never equate smooth shading, subdivision, weighted normals or a beauty render
   with correct underlying geometry.
3. Never add subdivisions merely to increase polygon count.
4. Never use a Boolean result as final geometry without checking its topology.
5. Never repair an entire asset when the defect is local and isolated.
6. Preserve the original object and source construction whenever practical.
7. Report unavailable checks as `UNVERIFIED`, not `PASS`.
8. Do not invent MCP tool names, parameters, kernel capabilities or API support.
9. Do not assume a module mentioned in an architecture report is exposed as an
   MCP tool. Discover the connected server's actual tool list first.
10. Geometry fidelity takes priority over arbitrary polygon targets unless the
    user explicitly imposes a hard budget. If the budget conflicts with the shape,
    report the trade-off before destructive simplification.

---

## 1. Capability discovery and safe execution

Before geometry work:

1. Inspect the connected MCP tool list and tool descriptions.
2. Identify actual capabilities for:
   - Scene/object inspection.
   - Mesh creation and editing.
   - BMesh or Blender Python execution.
   - Curve/surface creation.
   - Modifier inspection and evaluation.
   - Mesh statistics.
   - Normals and manifold checks.
   - Screenshots or viewport inspection.
3. Inspect Blender version and available API features before using version-specific
   properties or operators.
4. Read the current scene, active object, selection, object transforms, modifiers,
   mesh data and dependencies.
5. Identify the exact object/component allowed to change.
6. Preserve user work. Prefer a duplicate, working copy, or reversible modifier
   until the repair is verified.

### 1.1 Tool-use policy

- Prefer typed MCP tools for operations they explicitly support:
  - `apply_uv_unwrap`: Fast context-isolated Smart UV Project ensuring game-ready UV layouts.
  - `clas_loft_splines`: Spline lofting with `longitudinal_samples > 1` enabling smooth G1 Catmull-Rom interpolation.
  - `audit_mesh_topology`: Topology and manifold auditor with `try/finally: bm.free()` safety.
  - `pbr_compile_curvature_ao`: Vectorized NumPy `np.add.at` discrete Laplacian curvature (<20ms).
  - `export_game_asset`: Production export with selection isolation, evaluated triangle budget decimation, and Iron Law 4 UV enforcement (`auto_uv=True`, `enforce_uv=True`).
  - `validate_phase_gate`: State machine validator accepting numeric phases (1-6) or string gate aliases (`"G0"` through `"G6"`), persisted to `.pipeline_state.json`.
- Use BMesh for topology-heavy mesh construction and editing (Zone A 90/10 hybrid pipeline standard).
- For Blender 5.3 & 5.3+ compatibility, never rely on deprecated `use_auto_smooth`; always attach the official "Smooth by Angle" `NODES` modifier (`apply_blender_version_compatibility`).
- Use NumPy/vectorized operations for bulk numerical work.

### 1.2 Hardened engine architecture status

The Blender MCP architecture is fully hardened for production:
- **BMesh toolkit (Zone A)**: Pure `bmesh.new()` → `bm.to_mesh()` construction path executing in C-RAM in <0.1s.
- **CLAS tensor shaper**: Catmull-Rom longitudinal spline lofting (`longitudinal_samples`) replacing piecewise linear lofting.
- **Mesh auditor**: Watertight manifold verification with robust `try/finally: bm.free()` memory leak protection.
- **Curvature compiler**: Fully vectorized discrete Laplacian evaluation via `np.add.at` (sub-millisecond execution).
- **UV layout & texturing**: First-class `@mcp.tool() apply_uv_unwrap` tool and Iron Law 4 export enforcement.
- **Budget enforcement**: `export_game_asset` evaluates real evaluated geometry via `depsgraph`, flags `OVER_BUDGET`, and applies dynamic `DECIMATE` modifiers when `auto_decimate=True`.
- **Selection isolation**: `export_game_asset` isolates selection before `transform_apply` so neighboring objects are untouched.
- **Pipeline persistence**: `validate_phase_gate` accepts `"G0"` through `"G6"` aliases and auto-saves progress to `.pipeline_state.json`.
- **Blender 5.3+ normal handling**: Modifier-based "Smooth by Angle" standard for sharp edge preservation.

---

## 2. Geometry specification before construction

For each geometry task, write a compact Geometry Specification:

```text
Asset / component:
Target object(s):
Geometry role: silhouette / surface / solid / cutter / joint / detail
Reference or design source:
Coordinate system and units:
Primary datums:
Critical dimensions:
Cross-section stations:
Required surface boundaries:
Intended continuity:
Thickness / clearance requirements:
Topology requirements:
Base and evaluated triangle target:
Available construction methods:
Acceptance checks:
Known unknowns:
```

### 2.1 Coordinate system and datums

- Establish origin, axes, symmetry plane and units before construction.
- Use stable datums: center planes, wheel centers, floor levels, mounting faces,
  axes, section stations, bounding planes or other meaningful references.
- Dimension dependent parts from shared datums, not from repeatedly eyeballed
  positions.
- Keep local and world coordinates distinct.
- Apply or preserve transforms intentionally. Non-uniform scale can distort
  bevels, normals, offsets and measured dimensions.
- Record assumptions when dimensions are inferred from images.
- Do not silently average conflicting reference views.

### 2.2 Geometry classes

Classify each component before choosing a method:

| Geometry class | Preferred construction candidates |
|---|---|
| Smooth designed shell | Section curves, lofts, patch surfaces, subdivision cage |
| Mechanical planar part | Profile extrusion, controlled bevel, Boolean + cleanup |
| Round port / tube | Circular profile, curve sweep, bridge loops |
| Repeated ribs / fins | Parameterized profile and controlled array/instances |
| Organic irregular form | Sculpt/remesh followed by required cleanup or retopology |
| Thick panel / shell | Clean surface plus controlled solidification or explicit inner/outer surfaces |
| Precision joint | Shared datums, mating profiles, measured clearances |

These are candidates, not mandatory tools. Choose the method that preserves the
required shape and editability.

---

## 3. Profile and cross-section engineering

Cross-sections are the primary control mechanism for many designed surfaces.

### 3.1 Section planning

1. Define section stations at meaningful shape changes, not arbitrary equal
   intervals alone.
2. Include endpoints, extrema, transitions, openings and attachment boundaries.
3. Use consistent section orientation and point correspondence.
4. Maintain a stable parameter direction around each section.
5. Record section origin, tangent direction, normal direction and scale.
6. Avoid twisting by aligning section frames before lofting.
7. Add stations where the shape changes; do not add dense stations to conceal a
   poor profile.

### 3.2 Correspondence and resampling

Before lofting:
- Ensure section loops have compatible point counts or a deliberate correspondence
  map.
- Match start points and winding direction.
- Keep landmarks aligned across sections.
- Resample by arc length where appropriate, not by raw vertex index alone.
- Avoid abrupt changes in point spacing.
- Inspect section-to-section twist and local scale drift.
- Preserve sharp creases as explicit boundaries or crease constraints rather than
  smoothing them away.

If the available loft implementation uses linear interpolation, classify its
continuity honestly. Use a verified cubic/spline or patch method only if it is
actually available. Do not describe a linear interpolated loft as G2.

### 3.3 Surface construction

- Use a controlled cage or patch layout that follows the intended flow.
- Prefer fewer, well-placed control points over dense irregular grids.
- Keep patch boundaries on meaningful creases, seams or natural transitions.
- Plan how adjacent patches meet before generating them.
- Avoid long, skinny quads and sudden topology density changes in reflective zones.
- Use consistent edge spacing where curvature changes smoothly.
- Preserve designed discontinuities: a sharp panel gap is not a defect.
- Evaluate the generated surface, not just its control cage.

### 3.4 Thickness and offsets

- Determine whether thickness is constant, variable, tapered or locally reinforced.
- Check offset direction and local normal orientation.
- Inspect tight concavities where offsets may self-intersect.
- Verify open boundaries, caps and inner surfaces.
- Do not use a Solidify result as proof of a valid shell; inspect the evaluated mesh.
- For thin panels, ensure the chosen thickness is scale-appropriate and does not
  invert or collapse local features.

---

## 4. Surface continuity: G0, G1 and G2

Continuity requirements must match the design. Not every boundary should be smooth.

### 4.1 Definitions

- **G0 / positional continuity:** adjacent surfaces meet at the same boundary
  position. No gap or overlap at the join.
- **G1 / tangent continuity:** tangent directions agree across the boundary.
  The surface appears directionally smooth, though curvature may change.
- **G2 / curvature continuity:** curvature behavior agrees across the boundary.
  This is required for high-quality reflective Class-A-like transitions where
  the design calls for a smooth curvature flow.

Do not confuse geometric continuity (G) with parametric continuity (C). State
which condition is being evaluated.

### 4.2 Boundary checks

For each intended smooth join:
1. Verify boundary positions and measure maximum positional gap.
2. Compare boundary tangent directions.
3. Compare normal directions across the join.
4. Where required and supported, compare normal curvature in corresponding
   directions across the boundary.
5. Inspect a broad specular highlight or curvature visualization.
6. Record numeric tolerances and units. If no tolerance was specified, report the
   measured value without inventing a pass threshold.

For intentionally sharp joins:
- Mark the boundary as a designed crease or hard edge.
- Require positional fit where parts physically meet.
- Do not fail it for lacking G1/G2.

### 4.3 G2 honesty rule

A smooth-looking render does not prove G2. A subdivision cage does not automatically
prove G2. A linear loft does not become G2 because it has many sections.

If exact curvature continuity cannot be computed with available tools:
- Run a visual highlight-flow inspection.
- Report `VISUAL ONLY` or `UNVERIFIED NUMERICALLY`.
- Do not claim a mathematical G2 pass.

---

## 5. Topology engineering

### 5.1 Topology design

- Place edge loops to support silhouette, curvature, deformation and openings.
- Keep quad flow coherent on subdivision-controlled surfaces.
- Use poles deliberately; avoid placing high-valence poles in sensitive reflective
  regions where they cause pinching.
- Keep edge density proportional to curvature and silhouette importance.
- Avoid long thin faces, near-zero-area faces and chaotic triangle fans.
- Match boundary-loop counts and landmarks before bridging.
- Use Grid Fill only when the boundary shape and spacing support it.
- Use triangles and n-gons deliberately on planar or non-deforming regions; do not
  assume every n-gon is invalid.
- Avoid n-gons across strongly curved or subdivision-sensitive regions.
- Keep separate physical parts separate when their assembly boundary is real.
- Do not weld unrelated components merely to achieve one connected mesh.

### 5.2 Manifold and mesh integrity

Check, where supported:
- Boundary edges and unintended open boundaries.
- Non-manifold edges and vertices.
- Duplicate vertices/faces.
- Zero-area or near-zero-area faces.
- Zero-length or near-zero-length edges.
- Inconsistent or flipped normals.
- Loose vertices/edges.
- Self-intersections and internal faces.
- Duplicate overlapping shells.
- Degenerate triangles after triangulation.
- Disconnected islands and unexpected components.
- Unexpected holes, non-planar n-gons and invalid boundary loops.

A mesh can be intentionally open (for example, a single surface sheet). Classify
expected open boundaries separately from defects.

### 5.3 Normals and shading

- Recalculate normals only after understanding intended inside/outside orientation.
- Inspect face orientation and normal consistency.
- Use weighted normals or smoothing settings only to improve shading on valid
  geometry; never to conceal broken topology.
- Distinguish geometric creases from shading splits.
- Check normals after Boolean, bevel, mirror, remesh and conversion operations.
- Validate the evaluated result after modifiers.

---

## 6. Curvature and silhouette validation

### 6.1 Multi-view silhouette

For geometry-sensitive components, inspect the required orthographic views:
front, rear, left, right, top and bottom as applicable, plus a three-quarter view.

Compare:
- Overall envelope and bounding dimensions.
- Major landmarks and their relative positions.
- Curvature extrema and transition locations.
- Negative spaces, openings and wheel/port/arch profiles.
- Symmetry where intended.
- Section profile at critical stations.

Use matched camera scale and alignment for reference comparison. Do not compare
different perspective angles as though they were equivalent orthographic views.

### 6.2 Highlight-flow inspection

For reflective surfaces:
- Use neutral clay or a neutral glossy diagnostic material.
- Use broad, controlled light cards or equivalent reflections.
- Look for waviness, flat spots, sudden highlight kinks, pinching and curvature
  reversals.
- Inspect the surface from more than one angle.
- Do not let paint, dark materials, reflections or shadows conceal geometry defects.

### 6.3 Curvature analysis

When numerical curvature tools are available:
- State the method used (for example, principal curvature, mean curvature,
  Gaussian curvature or a discrete mesh approximation).
- State whether values are computed on control geometry or evaluated geometry.
- Record scale and units.
- Identify boundary and high-valence regions where discrete estimates may be
  unreliable.
- Avoid interpreting noisy per-vertex values as exact surface curvature.
- Use smoothing only for analysis visualization, never to alter the source mesh
  without an explicit repair task.

If a numeric method is unavailable, use highlight flow and section inspection,
and label the result visual-only.

---

## 7. Boolean, bevel and subdivision quality

### 7.1 Boolean operations

Before Boolean:
- Confirm cutter dimensions, orientation and clearance.
- Ensure the cutter fully crosses the target where a through-cut is intended.
- Avoid tangential or coplanar contacts where numerical ambiguity is likely.
- Keep source cutters in a clearly named collection until acceptance.

After Boolean:
- Inspect the entire cut boundary.
- Check sliver faces, thin triangles, duplicate/internal faces and normals.
- Confirm intended openings and wall thickness.
- Bevel only after the Boolean boundary is understood.
- Apply the Boolean only when the result is accepted or the workflow requires it.

### 7.2 Bevels

- Apply or account for object scale.
- Set bevel width from actual object scale and design intent.
- Inspect clamp overlap and corner intersections.
- Use segments appropriate to the intended edge radius.
- Avoid bevels collapsing narrow gaps or merging separate design features.
- Inspect the evaluated mesh and highlight response.
- Do not apply one generic bevel width to every object.

### 7.3 Subdivision

- Establish a clean base cage before adding subdivision.
- Place support loops or creases intentionally.
- Keep poles away from sensitive curvature zones where possible.
- Inspect pinching at corners, openings and narrow transitions.
- Compare control cage and evaluated surface.
- Do not use excessive subdivision to hide a poor cage.
- Preserve the editable cage and modifier stack until verified.

---

## 8. Geometric fit, clearances and assembly

For components that mate:
1. Identify the mating datum and local coordinate frame.
2. Define intended contact, clearance, overlap or interference.
3. Measure dimensions and relative transforms.
4. Check intersections and gaps at the interface.
5. Inspect the assembly from relevant views.
6. Record tolerances supplied by the user or source. Do not invent engineering
   tolerances.
7. If no tolerance exists, report actual measured gaps/intersections without
   declaring engineering compliance.

For vehicle-like assets, geometry checks may include:
- Wheel centers versus arch centers.
- Tire-to-fender clearance.
- Brake and rim concentricity.
- Hood/fender/bumper boundary fit.
- Door gaps and panel alignment.
- Glass-to-frame fit.
- Wing supports and mounting contacts.
- Undertray and wheel-well continuity.

These are geometric checks only; the artist workflow owns the complete component
brief and asset checklist.

---

## 9. Polygon and evaluated geometry accounting

Always distinguish:
- Vertices.
- Edges.
- Faces/polygons.
- Triangles.
- Base mesh counts.
- Evaluated mesh counts after modifiers.
- Asset-only counts versus whole-scene counts.
- Unique mesh data versus instances.

Use evaluated triangle count as the default when a user asks for a triangle
budget, unless they specify another convention.

Before a budget-sensitive operation:
1. Measure the current base and evaluated counts.
2. Estimate the operation's impact.
3. Preserve headroom for bevels, subdivision, curves, instances and conversion.
4. Re-measure after the operation.
5. Verify the exported asset independently when export is part of the task.

**Engine Budget & UV Enforcement Safeguard:** The updated `export_game_asset` implementation
actively enforces `triangle_budget` via `depsgraph.evaluated_get()`. When `auto_decimate=True`,
it dynamically adds an `MCP_Budget_Decimate` modifier. Furthermore, it strictly enforces
Iron Law 4 (Mandatory UV): if an asset lacks UV coordinates, `auto_uv=True` triggers
`apply_uv_unwrap` automatically before export, or `enforce_uv=True` rejects the export.

Never decimate blindly. If a mesh exceeds budget:
- Identify which components consume the geometry.
- Protect silhouette-critical and curvature-critical regions.
- Consider component-specific reduction, retopology or LOD only if supported.
- Re-run silhouette, curvature, manifold and fit checks after reduction.
- Report any lost detail.

---

## 10. Repair protocol

Repair the smallest possible region while preserving approved geometry.

### 10.1 Defect workflow

1. Identify the exact defect and affected component.
2. Capture the pre-repair state and relevant measurements.
3. Determine the likely cause: bad profile, section twist, topology flow, Boolean,
   modifier order, transform scale, normals, duplicate geometry or intersection.
4. Choose a repair that addresses the cause, not just the visible symptom.
5. Change only the affected geometry or modifier.
6. Re-run the original failing check.
7. Run neighboring checks to catch regressions.
8. Compare before/after evidence.
9. Save a checkpoint after verification.

### 10.2 Repair priority

1. Wrong coordinate system, dimensions or datums.
2. Incorrect silhouette or section profile.
3. Gaps, overlaps and failed component interfaces.
4. Self-intersections and invalid shell structure.
5. Topology flow and curvature defects.
6. Normals and shading artifacts.
7. Local detail defects.

Do not polish normals while the underlying silhouette is wrong.

---

## 11. Geometry task cards and hard gates

Every geometry task must have:

```text
Task ID:
Component:
Objective:
Allowed edit scope:
Datums / dimensions:
Construction method:
Expected geometry:
Checks:
Evidence:
Pass criteria:
Failure / rollback:
Status: NOT STARTED
```

Use this status vocabulary:
- `PASS` — directly checked and evidence captured.
- `FAIL` — a check shows the requirement is not met.
- `UNVERIFIED` — required evidence or capability is unavailable.
- `BLOCKED` — a dependency or required operation prevents progress.
- `NOT APPLICABLE` — the check genuinely does not apply, with reason.

A task is not complete because Blender returned without an exception.

### 11.1 Geometry gate sequence

**Gate G0 — Scene and target safety**
- Correct object and scope identified.
- Scene state inspected.
- Working copy/checkpoint available where appropriate.

**Gate G1 — Datums and profiles**
- Coordinate system and units defined.
- Critical dimensions and section stations recorded.
- Profile direction and correspondence checked.

**Gate G2 — Primary construction**
- Main surface/solid exists.
- Required silhouette and dimensions checked.
- No unapproved placeholder geometry remains.

**Gate G3 — Topology and interfaces**
- Boundary loops and patch joins inspected.
- Manifold/open-boundary expectations classified.
- Mating components and clearances checked.

**Gate G4 — Curvature and shading**
- G0/G1/G2 requirements stated per boundary.
- Required continuity checks run or marked unverified.
- Highlight flow and section profiles inspected.

**Gate G5 — Integrity and budget**
- Degenerates, duplicates, normals and intersections checked.
- Base and evaluated counts recorded.
- Budget compliance independently verified.

**Gate G6 — Regression**
- Required orthographic and close-up evidence captured.
- Neighboring components rechecked after repair.
- Final geometry state and unresolved defects reported.

> [!TIP]
> **Direct Gate Validation in Code:** The runtime validator `validate_phase_gate(phase_id=...)`
> directly accepts strings `"G0"` through `"G6"` (e.g. `validate_phase_gate("G3", evidence={...})`)
> and automatically persists pipeline progress to `.pipeline_state.json`.

Do not force a geometry gate to replace the broader artist workflow phases. These
gates apply to geometry tasks inside the larger asset plan.

---

## 12. Evidence and reporting format

For each geometry task, report:

| Check | Result | Evidence / measurement |
|---|---|---|
| Dimensions and datums | PASS/FAIL/UNVERIFIED | Values and units |
| Silhouette / sections | PASS/FAIL/UNVERIFIED | Views or deviation |
| Surface continuity | PASS/FAIL/UNVERIFIED | G0/G1/G2 and method |
| Topology integrity | PASS/FAIL/UNVERIFIED | Defect counts |
| Intersections / fit | PASS/FAIL/UNVERIFIED | Gap or overlap measurements |
| Normals / shading | PASS/FAIL/UNVERIFIED | Inspection method |
| Base/evaluated triangles | PASS/FAIL/UNVERIFIED | Counts and scope |

The final geometry report must include:
- Components created or modified.
- Construction methods actually used.
- Datums and dimensions.
- Base and evaluated vertex/edge/face/triangle counts.
- Topology defects found and repaired.
- Continuity requirements and which were numerically or visually verified.
- Intersection and clearance results.
- Reference deviation results where measurable.
- Unverified checks and unavailable MCP capabilities.
- Remaining defects and recommended next geometry task.

Never report an overall geometry score without showing the dimensions that
contributed to it. Never hide a failed check inside an average.

---

## 13. Common geometry failures

| Symptom | Likely cause | Correct response |
|---|---|---|
| Smooth shading but lumpy reflection | Poor surface shape or topology | Inspect sections and highlight flow; repair cage/profile |
| Loft twists between sections | Inconsistent start point, winding or frame | Align section correspondence and orientation |
| Flat spots in a reflective shell | Linear interpolation or poor section spacing | Add controlled curvature-aware sections or use a verified spline/patch method |
| Gaps between patches | Boundary mismatch or bad alignment | Match boundary points and tangents; verify G0 first |
| Pinching near a pole | Pole placement or uneven edge flow | Redirect loops or move pole away from sensitive region |
| Boolean shading artifacts | Sliver faces, coplanar contact or poor cleanup | Adjust cutter and inspect topology/normals |
| Bevel collapses corners | Excessive width, scale or overlap | Correct scale/width and inspect evaluated result |
| Solidify self-intersects | Tight concavity or excessive thickness | Reduce/localize thickness or build inner surface explicitly |
| Mesh passes manifold check but looks wrong | Shape/reference error | Compare silhouettes, sections and landmarks |
| Mesh looks correct in one view only | Inadequate multi-view constraints | Reconcile all required orthographic views |
| Triangle count unexpectedly explodes | Modifier, instance or conversion expansion | Inspect evaluated components and modifier stack |
| Geometry repair breaks adjacent parts | Repair scope too broad | Roll back and repair the smallest affected region |

---

## 14. Definition of geometry done

Geometry is complete only when:
- The specified shape and dimensions are verified to the required confidence.
- Required sections and silhouettes match the design/reference.
- Intended joins meet their stated continuity requirements.
- Topology is valid for the intended use.
- Expected open boundaries are distinguished from defects.
- Intersections, gaps and clearances are checked where relevant.
- Normals and evaluated modifier results are inspected.
- Base and evaluated geometry counts are recorded.
- All required checks are PASS or explicitly documented as UNVERIFIED/NOT
  APPLICABLE.
- No unsupported claim of mathematical accuracy is made.



## 15. Construction strategy selection and mathematical discipline

Choose the construction method from the required form, not from whichever MCP command is easiest to call.

| Form / requirement | Candidate method | Main risks to verify |
|---|---|---|
| Automotive freeform shell | Section-driven loft, tensor/Bernstein patch, controlled Sub-D cage | Section correspondence, twist, tangent/curvature breaks, patch boundaries |
| Wheel arch / fender | Datum-driven arch profile plus surrounding surface patches | Concentricity, clearance, silhouette, local pinching |
| Mechanical housing | Profile extrusion, bevels, Boolean openings, explicit wall thickness | Sliver faces, coplanar cuts, bevel collapse, manifoldness |
| Repeated fins / louvers | Parameterized master profile and controlled instances/arrays | Spacing, alignment, overlap, evaluated instance count |
| Tubes / pipes | Curve sweep or circular section loft | Radius consistency, frame twist, end caps, intersections |
| Thin body panels | Surface patch with controlled thickness or explicit inner/outer shell | Offset self-intersection, boundary thickness, open edges |
| Organic sculpted part | Sculpt/remesh followed by retopology where needed | Lost landmarks, uneven density, non-manifold remnants |

A candidate method is not a verified capability. Confirm that the installed MCP server exposes the necessary operation and inspect its schema before use.

### 15.1 Datums, parameterization and reproducibility
- Define a stable local coordinate frame for each component.
- Express critical features relative to shared datums.
- Store construction parameters and section station definitions where supported.
- Avoid unrelated hard-coded world-space coordinates for mating features.
- Use deterministic naming for source profiles, cages, final objects and cutters.
- Record Blender version, skill version, source object names and modifier state.
- Preserve source profiles/cages until the generated surface passes validation.

### 15.2 Section-driven surface construction
1. Define stations at extrema, inflections, interfaces, openings and design transitions.
2. Give each section a consistent local frame.
3. Align loop winding and start landmarks.
4. Resample with a verified method appropriate to the curve representation.
5. Check section spacing and curvature distribution.
6. Detect twist, collapse, self-crossing and sudden scale changes.
7. Evaluate intermediate sections, not only input stations.
8. Compare the generated surface against reference evidence.

Do not add arbitrary stations to hide an unstable interpolation method. If the available loft is linear, disclose its limitations, use a verified higher-order method, or construct a patch whose boundary conditions can be checked.

### 15.3 Continuity terminology
- G0: positions coincide along the shared boundary.
- G1: tangent directions/planes agree along the boundary.
- G2: curvature behaviour agrees along the boundary.
- C0/C1/C2: parametric derivatives agree; these are not interchangeable with geometric G-continuity.

A mesh made of flat polygons has piecewise planar normals. Subdivision may create a smooth limit surface, but continuity depends on cage topology and boundary conditions. Never infer G2 from polygon count, smooth shading or a visually soft render.

## 16. Architecture audit safeguards

The supplied MCP architecture audit identifies the following geometry-relevant risks. Treat each as a verification target against the installed build, not as proof that runtime code is unchanged.

| Audit item | Geometry-engineering response |
|---|---|
| `export_game_asset` accepts but reportedly does not enforce `triangle_budget` | Independently measure evaluated triangles; block export if over budget unless the user explicitly accepts. |
| `audit_mesh_object` reportedly omits `bm.free()` | Confirm cleanup before repeated audits; bound audit loops and report unresolved leak risk. |
| Curvature compiler reportedly uses a Python per-vertex loop | Benchmark actual runtime; do not promise sub-20ms for arbitrary mesh sizes. |
| CLAS loft reportedly uses `np.interp` | Do not claim G1/G2; inspect station tangent changes and use a verified alternative if needed. |
| Phase gate manager is in-memory singleton | Do not treat gate state as durable across server restart or independent assets. |
| Export transform application may affect other selected objects | Isolate intended selection and restore user context around context-sensitive operations. |
| SDF mask orientation is not validated | Confirm image dimensions, orientation and view convention before silhouette-mask use. |
| Root/bundled addon copies can drift | Record runtime addon/build identity; do not assume source and installed copies match. |
| Large addon/server files create a god-node | Keep geometry reasoning modular and prefer focused kernel operations. |
| Silent exception handling may hide failures | Require explicit structured result evidence; a swallowed exception is not success. |

This skill does not repair the MCP architecture itself. It adapts safely to verified capabilities and reports blockers to the maintainer.

### 16.1 Safe Blender context and mutation
- Snapshot active object, selected objects, mode, active collection and relevant view-layer state when possible.
- Isolate only the intended target before context-sensitive operations.
- Restore user context in cleanup code where supported.
- Verify unrelated objects and transforms were not changed.
- Prefer data API/BMesh operations for deterministic geometry changes when supported.
- Never assume a command success response proves the scene changed as intended.

### 16.2 Audit lifecycle
- Do not repeatedly invoke a potentially leaking auditor in an unbounded repair loop.
- Run targeted checks after local edits and a full audit at defined gates.
- Record audit duration, target object, mesh size and result.
- If cleanup is confirmed fixed, record the fixed version/commit in the report.

## 17. Geometry regression protocol

After every non-trivial operation, compare post-operation state with pre-operation state.

Minimum regression checks:
- Target object exists and retains expected data type.
- Object transform and dimensions remain expected.
- Vertex/edge/face/triangle counts are plausible.
- Expected components remain separate and named.
- No unrelated object changed.
- Critical landmarks remain within documented deviation.
- No new non-manifold edges, degenerates or unexpected intersections.
- Modifier stack and evaluated geometry remain valid.
- Required views retain intended silhouette.
- Geometry budget remains satisfied.

Record what changed, why, affected objects, before/after metrics, checks rerun, regressions, rollback point and final status. A repair is not accepted merely because the original symptom disappeared.

## 18. Handoff contracts

### Input from Pre-Production Intelligence
- Approved brief, intended use, scale, units and coordinate convention.
- Component scope, acceptance priorities and budget definition.

### Input from Visual Reference Intelligence
- Reference register and compatible view set.
- Evidence labels, confidence and landmark/proportion register.
- Component relationship map, surface hypotheses and hidden-geometry register.
- Conflicts and per-component readiness.

### Output to Artist Workflow
- Geometry specification and construction status.
- Components built/modified and source objects preserved.
- Validation evidence, unresolved defects and next task recommendations.
- Operations blocked by MCP capability or architecture issues.

### Output to future export/optimization skills
- Base/evaluated geometry counts and component-level geometry cost.
- Protected silhouette/curvature regions and known topology constraints.
- Verified collision/clearance facts only.
- Explicitly unverified UV, LOD, tangent, bake or export requirements.

Do not claim UV unwrap, LOD generation, tangent generation, collision proxy creation, FBX export or other delivery subsystems exist merely because the audit recommends them. They are outside this skill's core geometry remit unless a verified operation is available.

**Final rule:** construct deliberately, measure honestly, repair locally, and
never confuse a convincing image with verified geometry.
