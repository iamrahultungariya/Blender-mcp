---
name: blender-artist-workflow
description: >
  Professional Blender modeling skill for AI agents and Blender MCP. Use for
  vehicles, hard-surface props, mechanical assets, organic forms, cables, pipes,
  architecture, game assets, product visualization, and scene assembly. Enforces
  reference-first planning, natural curvature, deliberate topology, non-destructive
  workflows, staged execution, visual QA, and anti-boxy modeling standards.
---

# MANDATORY EXECUTION CONTRACT — REFERENCE-TO-ASSET PIPELINE (v2)

> This contract overrides any older, looser workflow below whenever instructions conflict. Follow it for every new asset request. Do not skip gates to save time. Do not claim a gate passed without evidence from Blender/MCP inspection.

## A. Input classification: understand what the user actually asked to build

Before creating or modifying geometry, classify the request as one of:
- **Image-led:** one or more reference images are attached.
- **Text-led:** the object is described in text, with no visual reference.
- **Hybrid:** text and images are both supplied.
- **Existing-scene edit:** the user asks to modify an already-open or supplied `.blend` scene.

Identify the requested asset category and exact subject first: vehicle, building, furniture, character, machine, weapon-like fictional prop, product, environment, organic object, etc. Never infer a different asset just because it is easier to model.

### A1. Image-led and hybrid requests

1. Inspect every supplied image, not just the first or most attractive one. Record image dimensions, visible view, camera angle, and what regions are occluded.
2. Identify whether each image is a front/rear/left/right/top/bottom orthographic view, a perspective view, a close-up, an exploded diagram, a wireframe, or a dimension sheet. Do not label a perspective image as orthographic.
3. Create a **Reference Evidence Matrix** with columns: feature/component, source image and region, observed dimensions/shape, confidence (high/medium/low), and unresolved ambiguity.
4. If multiple sides are supplied, reconcile them into one consistent 3D interpretation. Use shared centerlines, wheel/door/window positions, floor levels, symmetry planes, and other datums. Never model each view independently and allow contradictory proportions.
5. If the reference shows components separately, in an exploded view, or with clearly distinct physical/material/moving boundaries, represent them as separate objects or assemblies. If all sides of a vehicle/building/product are shown, decompose visible systems into a component tree. Examples:
   - Vehicle: body shell, hood/bonnet, hood underside reinforcement, doors, trunk/tailgate, bumpers, grille and ducts, headlamp housings/lenses, glass, seals, mirrors/stalks, fenders, wheel/tire/rim/brake assemblies, suspension visible through openings, side skirts, splitter, diffuser, wing/mounts, exhaust, undertray and interior.
   - Building: foundation/plinth, structural frame, floors, walls, roof layers, façade panels, doors, windows/glazing, frames, balconies, stairs, railings, columns, gutters, downpipes, service equipment and site elements.
   - Product/machine: main housing, covers, panels, controls, displays, connectors, fasteners, vents, internal visible assemblies, feet/mounts and cable routes.
6. Separate parts based on physical boundaries, material changes, motion, assembly logic, visibility, or editability—not by arbitrarily splitting every surface. A single continuous body panel should remain continuous unless the design shows a seam or separate panel.
7. Explicitly inspect **undersides, backsides, inner faces, cavities, thickness, panel backs and hidden structures** when references reveal them or the object type requires them. Do not invent hidden detail as observed fact. Label inferred construction as inferred and use plausible real-world construction only where the user expects a complete asset.
8. If a critical side/view is missing, proceed only if proportions can be responsibly inferred. Mark the view as inferred and lower confidence. Ask one focused question only if the missing view would materially change the asset.
9. Never treat text, labels, dimensions, arrows, UI panels, or presentation-board decorations inside a reference image as geometry unless they are explicitly part of the requested asset.

### A2. Text-led requests: build a concrete visual specification before modeling

Do not jump from a short phrase straight into primitive creation. First translate the request into a **Real-World Visual Brief**:
- Exact object identity and intended variant/model/type.
- Real-world purpose and how the object is constructed.
- Primary silhouette and proportions.
- Primary, secondary and tertiary forms.
- Material families and plausible thicknesses/joins.
- Moving, detachable and separately manufactured parts.
- Hidden/internal areas that should be present for the requested level of completeness.
- Required views and final use (game, realtime, cinematic, product render, animation, 3D print, education, or preview).

Create an internal visual concept in words: describe what a knowledgeable observer should see from front, rear, left, right, top, bottom and three-quarter views as relevant. Use real-world reference knowledge only as a design hypothesis; do not claim exact manufacturer dimensions unless sourced or supplied.

If web/reference research or image generation tools are available and the user asks for research or concept imagery, use them appropriately. Otherwise do not pretend an image was generated. The visual brief and component tree are mandatory even without external images.

### A3. Component tree and dependency map

Before geometry, create a hierarchical component tree. Each component entry must state:
- Component ID and clear object/collection name.
- Purpose and visual role.
- Parent/assembly relationship.
- Geometry method (mesh cage, curve, bevel/boolean, sculpt, Geometry Nodes, etc.).
- Approximate dimensions or datum references.
- Required material/slot where relevant.
- Whether separate, joined, instanced, or procedural—and why.
- Which phase/task creates it and which verification checks it.

Also record shared datums, symmetry planes, pivots, attachment surfaces, clearances, and dependencies. Model dependencies before dependent components (e.g. wheel centers before arches; building grid/floor levels before façade modules; housing before fitted covers).

## B. Feasibility and geometry-budget gate — before any modeling

A requested polygon/triangle budget is a constraint to evaluate, not a target to blindly satisfy. First establish intended output and quality level. Distinguish **vertices, edges, faces/polygons, and evaluated triangles**. Do not use these terms interchangeably. Report both base-mesh and evaluated counts when modifiers change the result.

### B1. Build a budget estimate

Create a component-level estimate with columns: component, required detail, estimated triangle range, geometry method, priority, and confidence. Include hidden components and details when required. Reserve headroom for modifiers, bevels, subdivision, curves converted to meshes, repeated instances, and final export.

Estimate based on visible curvature, silhouette importance, close-up distance, mechanical detail, output platform, and whether details can be represented by textures/normal maps instead of geometry. A smooth curved silhouette needs enough actual geometry; a normal map cannot repair a faceted outline.

### B2. Feasibility decision

Before building, compare the user's requested budget with the estimate:
- **Feasible:** the full required asset can meet the quality brief within budget. State the planned allocation and proceed.
- **Feasible with trade-offs:** state exactly which details must be simplified, instanced, baked, or omitted. Do not silently downgrade quality.
- **Not feasible:** stop before modeling. Explain why the requested count/format cannot support the requested silhouette, curvature, component separation, or detail. Recommend a minimum viable triangle count/range and an alternative (e.g. separate high-poly render asset and optimized game asset). Ask permission to use the revised budget if it changes the user's explicit constraint.
- **No budget supplied:** recommend a budget based on asset category and target use; explain that it is an estimate, not a universal industry standard. Do not impose a generic 600K target on every object.

Never promise an exact triangle count before the final evaluated mesh exists. A minimum triangle count is not a quality guarantee. Do not add useless subdivisions just to hit a number. Spend geometry where it changes silhouette, curvature, openings, mechanical forms, or visible close-up detail.

### B3. Budget profiles (starting estimates, not rigid standards)

Use these only as planning starting points and revise after the component estimate:
- **Realtime/game asset:** choose a platform-specific budget; preserve silhouette and bake high-frequency detail where appropriate.
- **Mid-poly product/prop:** enough geometry for clean bevels and the expected camera distance; use materials/normal maps for tiny surface detail.
- **Hero cinematic/product-render asset:** substantially denser geometry may be justified for close-ups, smooth reflections, tires, machined details and visible underside. A complex hero car may reasonably start around 600K evaluated triangles or higher, but this is not mandatory for every car and must be justified by the actual design.
- **Architecture/environment:** budget by repeated modules, silhouette, visible façade complexity, interior access and camera distance; use instancing and modular reuse rather than duplicating identical detail.
- **Organic/sculpted asset:** budget according to silhouette, deformation, sculpt resolution and bake strategy.

## C. Phase-and-task execution: one task at a time, hard gates

The project must be split into ordered **phases**, and every phase into explicit **tasks**. Each task must contain:
1. Task ID and single objective.
2. Exact components/objects it may change.
3. Required operations and modeling method.
4. Expected measurable result.
5. Verification procedure using the actual available Blender MCP tools/API.
6. Evidence to capture (object data, mesh statistics, orthographic view, close-up, wireframe, section, render, or screenshot).
7. Pass criteria and failure/rollback action.
8. Dependencies and the next allowed task.

### C1. Mandatory execution loop

For each task, do this exact loop:
1. Read current scene/object state; confirm the intended target objects and dependencies.
2. Execute only the current task. Do not bundle unrelated future tasks into one giant script or command batch.
3. Query Blender again after the write. Confirm object existence, dimensions, transforms, mesh/curve data, modifiers, materials, and relevant statistics.
4. Capture the view/evidence that can actually verify this task.
5. Compare the result against the requirement and reference evidence, including close-up crops where relevant.
6. If any pass criterion fails, repair only the smallest affected scope and repeat verification.
7. Save a checkpoint after a successful task or phase, using a versioned file or safe checkpoint strategy that does not overwrite the user's original.
8. Mark the task PASS only when evidence supports it. Otherwise mark FAIL or BLOCKED with the reason.
9. Start the next task only after the current task is PASS. Start the next phase only after every mandatory task and phase gate in the current phase is PASS.

**No silent skipping:** if a required MCP operation, screenshot, mesh query, or verification capability is unavailable, mark the check UNVERIFIED/BLOCKED. Do not infer success from a command returning without an exception. Discover the connected MCP tool list and use only operations actually supported by that server. Use Blender Python/BMesh for a check only when the connected route can execute it and return evidence.

### C2. Default phase template (adapt to asset category)

- **Phase 0 — Intake & scene safety:** classify input; inspect existing scene; preserve user work; confirm Blender version and MCP capabilities; create safe working copy/checkpoint.
- **Phase 1 — Reference intelligence:** inspect all images/views; establish dimensions/datums; record confidence; identify missing views; create reference matrix.
- **Phase 2 — Concept, component tree & feasibility:** write the real-world visual brief; decompose assemblies; choose modeling methods; estimate triangle budget; resolve infeasible constraints before geometry.
- **Phase 3 — Primary blockout:** build datums, bounding envelope, major masses and silhouette only. Verify all required orthographic views and proportions before detail.
- **Phase 4 — Primary surfaces and curvature:** construct continuous shells, compound curves, rooflines, fenders, walls/roof forms or equivalent. Verify highlight flow, cross-sections, silhouette and surface continuity.
- **Phase 5 — Secondary components and openings:** create distinct panels, housings, doors/windows, recesses, wheel arches, façade systems, mechanical assemblies and attachment geometry.
- **Phase 6 — Hidden geometry and underside:** add inner faces, thickness, hood/bonnet underside, wheel wells, undertray, structural backs, interior cavities or building internals as required by the brief.
- **Phase 7 — Tertiary detail:** add fasteners, vents, seals, trim, labels, small hardware and surface details. Only add details visible or required for the target use.
- **Phase 8 — Materials, UVs and shading:** assign real material separation, UVs, normals and shader response; inspect neutral clay and material passes.
- **Phase 9 — Integration and full QA:** inspect assembly fit, clearances, intersections, topology, triangle budget, symmetry, all views and reference fidelity.
- **Phase 10 — Presentation and delivery:** final renders/turntable if requested, organized Outliner, save/export, reopen or re-query deliverables, and evidence-backed report.

A task can be split into smaller tasks whenever it changes multiple independent systems. For example, hood top surface, hood underside reinforcement, hood hinges and hood latch should not be one unverifiable task.

## D. Verification must test the actual requirement, not just mesh statistics

Use a requirement-to-evidence map. Polygon count is only one metric and must never dominate visual/structural correctness.

### D1. Visual fidelity and shape
- Compare front/rear/left/right/top/bottom and three-quarter views against corresponding references.
- Compare silhouette, proportions, negative spaces, wheelbase/track, roofline, overhangs, façade rhythm, opening positions and major component placement.
- Use orthographic overlays or measured landmark comparisons when references permit.
- Inspect critical regions as close-up crops; do not rely on one overall perspective screenshot.

### D2. Curvature and surface quality
- Inspect broad specular highlight flow using neutral glossy/clay material and consistent lighting.
- Inspect cross-sections/curvature through hood, bonnet, fenders, roof, doors, quarter panels, product shells, curved roofs and other designed surfaces.
- Look for flat patches, lumpy reflections, pinching, unintended facets, abrupt tangent breaks, warped transitions and box-like approximations.
- Distinguish intentional creases/sharp transitions from accidental G0/G1/G2 discontinuities. Do not demand G2 continuity at a deliberately sharp panel break.
- Use curvature/normal analysis or surface sampling when available; otherwise mark the check as visual-only rather than claiming a numeric curvature test.

### D3. Completeness and real-world construction
- Check the component tree against the reference matrix: every required part exists, is correctly positioned, and has the correct relationship to adjacent parts.
- Inspect backsides, underside, thickness, inner walls, cavities and visible structural details.
- For vehicles, explicitly check hood/bonnet top and underside separately, inner fender liners, wheel wells, door/trunk inner faces, glass thickness/seals, bumper ducts and visible chassis/undertray details as required.
- For buildings, inspect roof layers, wall thickness, openings, structural supports, interior/exterior transitions, stairs, railings and service connections as required.
- Do not give credit for a named object that is only a flat placeholder when the reference requires a shaped component.

### D4. Geometry and technical integrity
- Check evaluated and base triangle counts separately, plus vertex/edge/face counts.
- Check normals, manifold status, duplicate geometry, degenerates, self-intersections, non-planar/ngon risks, modifier results, object scale/origins and material assignment.
- Check physical clearances and attachment contact; use measurements when possible. Do not invent exact tolerances if none were supplied.
- Check curve splines, bevel depth, resolution, tilt, caps and conversion results for actual curve-based components.

### D5. Evidence-based statuses
Every check must be marked exactly one of:
- **PASS:** directly verified and evidence captured.
- **FAIL:** evidence shows the requirement is not met.
- **UNVERIFIED:** evidence/tooling is insufficient.
- **NOT APPLICABLE:** requirement genuinely does not apply, with a short reason.

Never convert UNVERIFIED into PASS. Never mark an entire phase complete while any mandatory task is FAIL or UNVERIFIED.

## E. Example: vehicle task card format

### Phase 4 / Task VEH-04.02 — Hood/bonnet primary surface
- **Objective:** create a continuous hood outer surface matching the supplied front/top/side references.
- **Scope:** `Hood_Outer` and its source cage only; do not modify fenders, windshield or bumper.
- **Actions:** align hood boundary to shared datums; create controlled surface cage; establish center crown and lateral falloff; preserve designed creases; add thickness only in its own later task.
- **Verify:** front/top/side orthographic overlays; glossy clay highlight pass; cross-section at front/middle/rear stations; inspect evaluated topology and dimensions.
- **Pass:** silhouette and boundary align with references; curvature is continuous where intended; no visible lumps/pinching; object remains editable; measurements recorded.
- **Evidence:** 3 orthographic screenshots, 3 highlight/cross-section checks, mesh statistics.
- **Failure action:** adjust the hood cage only, re-run the same checks, save checkpoint after PASS.
- **Next allowed task:** hood underside reinforcement; do not proceed to vents or badges first.

This card format is mandatory for every task, not just vehicles. Adapt its checks to the object category.

## F. Final reporting contract

At completion, report:
- What was requested and how the input was interpreted.
- Which references/views were available and which assumptions were inferred.
- Component tree and separate assemblies created.
- Requested vs estimated vs actual evaluated triangle counts (and base counts).
- Phase/task ledger with PASS/FAIL/UNVERIFIED/BLOCKED statuses.
- Visual fidelity, curvature, completeness, hidden-geometry and technical findings.
- Known limitations and omitted features.
- Exact saved file/export paths only after confirming they exist.

Never summarize a failed or partially verified model as complete. A beautiful render does not prove correct underside geometry; a high triangle count does not prove realism; a clean manifold mesh does not prove the reference was matched.

---

# Blender Artist Workflow Skill
**Purpose:** Make an AI-controlled Blender session behave like a thoughtful 3D artist, not a primitive-placement script.

This skill is written for Blender MCP / Blender automation agents. It is intentionally implementation-agnostic: inspect the tools exposed by the connected MCP server and use the best available operation. Do not assume every Blender MCP server exposes the same tools.

## 0. Core operating principle

Do not equate "model created" with "asset completed."

A successful asset must satisfy:
1. **Silhouette:** recognizable and proportionally convincing from the intended views.
2. **Form:** large, medium, and small forms are deliberately layered.
3. **Curvature:** curved surfaces transition smoothly and naturally; they are not approximated by obvious stacks of boxes.
4. **Construction logic:** parts, seams, openings, joints, thickness, and attachments make physical sense.
5. **Topology and shading:** no accidental pinching, broken normals, self-intersections, stretched faces, or ugly bevels.
6. **Presentation:** materials, lighting, camera, and scale communicate the quality of the model.
7. **Deliverable integrity:** correct object organization, names, transforms, saved file, and requested export format.

**Never stop at a primitive blockout** unless the user explicitly requested a blockout, low-poly/blocky style, or a fast prototype.

---

# 1. Source material distilled from the supplied videos

The following points are derived from the seven video summaries supplied with this task. They are not claims that every technique is appropriate for every asset.

## 1.1 Curves and natural tubes — Ryan King Art
Source: [Blender Curves tutorial](https://www.youtube.com/watch?v=gxzWCH1Q4fM)

- Add Bézier, Circle, Path, or NURBS curves for cables, pipes, ropes, vines, and flowing lines.
- Edit control points with `G`, `R`, and `S`; extend splines with `E` or `Ctrl-click`; connect endpoints with `F`; subdivide to add control points; separate selected spline parts with `P`.
- Use handle types intentionally:
  - `Automatic`: smooth transitions.
  - `Vector`: sharp, linear corners.
  - `Aligned`: handles remain aligned.
  - `Free`: independent handle control.
- Use `Alt+S` to vary local curve radius along the spline.
- Use curve Geometry settings:
  - Bevel Depth for tube thickness.
  - Bevel Resolution for roundness.
  - Fill Caps for closed ends.
  - Object/Profile bevel for custom cross-sections.
  - Taper Object for changing thickness along a path.
  - Extrude/Offset for ribbon-like geometry.
  - Start/End mapping for partial curve visibility and growth effects.
- Use 3D curves for paths in space and 2D curves for flat shapes.
- Convert to mesh only when mesh-specific editing, sculpting, or UV work is required.
- Curve Draw tools can sketch paths directly; surface snapping is useful for wires that follow an existing object.

## 1.2 Sculpting, wear, and high-to-low baking — Grant Abbitt
Source: [Multiresolution sculpting and baking tutorial](https://www.youtube.com/watch?v=LvFilHJfinU)

- Prepare even topology before detailed sculpting; apply object scale first.
- Use Multiresolution when a low-resolution base must retain a sculptable subdivision stack.
- Use X/Y symmetry for symmetrical wear, then deliberately break symmetry for believable variation.
- Scrape/Fill creates worn planes; Crease creates sharp cracks; Trim removes larger chunks; alpha brushes add repeatable surface texture.
- UV unwrap the low-resolution mesh before baking.
- Bake high-frequency normal/displacement detail from higher Multires levels onto the lower level.
- Treat normal/displacement maps as data, not color: set image color space to Non-Color.
- Use a Normal Map node for tangent-space normal maps; use ramps and roughness variation carefully.
- Preserve a clean low-poly silhouette. A normal map cannot repair a bad silhouette.

## 1.3 Universal modeling workflow — On Mars 3D
Source: [Universal 7-step modeling workflow](https://www.youtube.com/watch?v=p5N5oikFWE8)

- Gather references before modeling.
- Decide the output target first: real-time game, cinematic/render, animation, or 3D print.
- Separate primary, secondary, and tertiary forms.
- Block out the silhouette and proportions before bevels and micro-detail.
- Choose the fastest suitable method for each part: polygon modeling, curves/NURBS, sculpting, CAD-like construction, or procedural geometry.
- Refine large transitions and secondary shapes after the blockout is approved.
- Add small details last; keep form design distinct from topology cleanup.
- Validate with test materials, viewport inspection, and renders before calling the asset finished.

## 1.4 Vehicle body modeling and panel flow — Aryan 3D
Source: [Car modeling tutorial](https://www.youtube.com/watch?v=NDPeZ7YZgrc)

- Set up aligned front, side, and top orthographic blueprints.
- Trace the major body contour with a small number of well-placed vertices.
- Use Subdivision Surface to preview smooth body curvature.
- Use LoopTools Space/Relax to even and smooth edge flows.
- Match edge counts before filling between boundaries.
- Use Grid Fill where the boundary topology supports it; manually rebuild difficult areas instead of forcing a bad fill.
- Use dissolve rather than deleting when an edge must be removed without opening a hole.
- Create controlled body creases with bevels and carefully fade them into the surrounding surface.
- Use viewport statistics to monitor edge counts and symmetry.

## 1.5 Image-based architectural assets — BlenderVitals
Source: [Low-poly building from a photo](https://www.youtube.com/watch?v=j-WegUytMA8)

- Use an image plane as a visual and texturing reference.
- Add loop cuts to isolate architectural zones such as walls, balconies, pillars, and windows.
- Extrude selected regions to establish depth.
- Assign separate glass materials to windows; tune metallic and roughness for the intended look.
- Fix UVs on newly created side faces rather than accepting stretched textures.
- Model repeated façade props separately, then duplicate and place them.
- Use Bézier curves for cables and pipes.
- Duplicate and rotate modular façade sections to assemble larger structures.

## 1.6 Hard-surface prop workflow — Isto Inc. Glock modeling challenge
Source: [Three artists model a Glock 19](https://www.youtube.com/watch?v=XEaoHoH4qf0)

- Establish real-world scale and proportions before adding details.
- Keep a rough blockout/reference mesh separate from the refined asset.
- Save incremental versions during complex work.
- Use axis-constrained transforms for precise mechanical parts.
- Use Subdivision for smooth forms with controlled low-poly cages; use bevels for machined edges.
- Use LoopTools Circle for clean circular openings where appropriate.
- Use Boolean Difference for designed cuts and recesses, then inspect and repair shading/topology.
- Prefer deliberate quad flow in deforming or subdivision-critical regions; do not force all surfaces into quads when a clean planar n-gon is more suitable.
- UV unwrap before painting or texture authoring.
- Build distinct material responses for metal, polymer, rubber, and painted surfaces.
- Use camera alignment and a deliberate key/fill/rim lighting setup for presentation.

**Safety and scope:** For firearm-shaped assets, model only the requested visual/game/film prop. Do not add functional construction guidance, operational mechanisms, or instructions that make a real weapon more usable.

## 1.7 Efficient hard-surface construction and cable/kitbash tricks — CG Boost
Source: [CG Boost hard-surface workflow](https://www.youtube.com/watch?v=Ml2t8uxPAQU)

- Use Inset and Bridge Faces for hollow low-poly forms.
- Use Subdivision with edge creases or support loops when a smooth cage-based result is needed.
- Use bevel weights and a Bevel modifier for controllable edge highlights.
- Use the modifier stack deliberately; modifier order changes the result.
- Draw curves in Cursor or Surface placement modes for cables.
- Bridge edge loops to connect pipe/handle sections and create smooth transitions.
- Use face snapping with rotation alignment to place kitbash details on curved surfaces.
- Use Shrinkwrap on a controlled vertex group to fit an attachment boundary to a host surface.
- Transfer custom normals when separate attached parts need compatible shading.
- Copy a proven modifier setup to repeated details rather than rebuilding it manually.

---

# 2. Additional professional guidance

These practices extend the supplied videos. Treat them as general production guidance, not as techniques demonstrated in those videos.

## 2.1 Choose the correct modeling strategy

Do not use one method for every object.

| Strategy | Best for | Typical tools | Main risk |
|---|---|---|---|
| Subdivision cage | Organic hard-surface shells, vehicle body panels, product forms | Quads, support loops, creases, Subdivision Surface | Pinching and uneven curvature |
| Bevel + weighted normals (mid-poly) | Machined props, modular assets, many planar surfaces | Bevel modifier, bevel weights, Auto Smooth/Smooth by Angle workflow, Weighted Normal | Bad shading if bevel widths/topology are inconsistent |
| Boolean + bevel | Complex cutouts, vents, recesses, mechanical panel details | Boolean Difference, bevel, cleanup, weighted normals | N-gons, thin slivers, shading artifacts |
| Curves | Cables, hoses, pipes, trim, seams, organic paths | Bézier/NURBS, bevel, taper, custom profile | Twists, uneven radius, poor junctions |
| Sculpt / Multires | Organic damage, stone, terrain, soft forms, surface wear | Sculpt brushes, Multires, remesh | Dense geometry and difficult game topology |
| High-to-low | Hero game assets needing sculpted surface detail | High-poly sculpt, low-poly retopo, UVs, baking | Projection errors and poor UVs |
| Geometry Nodes | Repeated procedural structures and configurable assets | Instances, curves, fields, node groups | Overengineering simple one-off assets |

**Decision rule:** select the method based on the surface and intended output, not on habit. A vehicle body usually needs controlled continuous surfaces; a bolted mechanical bracket may be faster and cleaner with booleans and bevels; a flexible hose should usually be a curve.

## 2.2 Natural curvature: the anti-boxy standard

A model looks boxy when the agent substitutes rectangular primitives for designed forms, uses too few silhouette segments, or makes abrupt transitions where the reference shows continuous curvature.

For every curved object:

1. Identify the curvature family: cylindrical, spherical, elliptical, compound, spline-like, or freeform.
2. Establish the silhouette in at least two orthographic views and one perspective view.
3. Use a small number of well-spaced control points. Add points only where curvature changes.
4. Keep control-point spacing reasonably even through smooth regions; concentrate points around intentional transitions.
5. Use Bézier handles or a Subdivision cage to control tangency. Avoid tiny zig-zag segments.
6. Inspect highlight flow with a glossy neutral test material. Broken highlights reveal bumps and pinching.
7. Check the silhouette against the reference from front, side, top, and three-quarter views.
8. Add thickness, seams, and details only after the primary surface is convincing.

**Curve-specific rules**
- Use `Automatic` handles for smooth continuous paths, `Vector` for intentionally sharp corners, and `Aligned`/`Free` when tangent direction needs explicit control.
- Avoid abrupt radius changes. Use `Alt+S` or a taper object to create gradual hose/cable thickness transitions.
- For a pipe with a hard elbow, use a curve with a smooth bend or a deliberately constructed tube junction; do not intersect two cylinders and leave the overlap visible.
- Use a custom bevel profile for trim, weather seals, rails, and non-circular extrusions.
- Check curve tilt to prevent unexpected twisting of rectangular or custom-profile cross-sections.
- Cap open ends when the tube should be closed; leave them open only when the design calls for a visible hollow opening.
- Convert curves to mesh only when needed; keep editable source curves where possible.

## 2.3 Vehicle modeling rules

Vehicles are silhouette-sensitive. A car cannot be made convincing by attaching four wheels to a rectangular body.

**Reference package**
- Obtain front, rear, side, top, and three-quarter references when possible.
- Align orthographic references to a shared scale and centerline.
- Confirm wheelbase, track width, overall length/width/height, wheel diameter, cabin height, hood length, and overhangs.
- If exact blueprints are unavailable, use multiple photos of the same model and clearly mark inferred dimensions.

**Build order**
0. Inspect the complete reference, create named zoom crops for the nose, hood, fenders, wheels, side details, and rear, and record which features are observed versus inferred.
1. Create a component tree for the car. Keep the body shell, bumper/fascia, splitter, grille/ducts, headlamps, wheels/tires, rims, brakes, mirrors, glass, skirts, wing/diffuser, and trim logically separate when their physical boundaries or material/assembly roles justify it.
2. Centerline, wheel centers, tire envelopes, and overall bounding box.
3. Main body volume: hood, cabin, rear deck/trunk, and continuous body shell.
4. Wheel arches and major cutlines.
5. Glasshouse: windshield, side windows, rear glass, pillars.
6. Fender volumes and shoulder/character lines.
7. Front/rear fascia as a system of individually reasoned components: bumper cover, splitter, grille, ducts, lamp housings, lenses, and visible inner walls.
8. Panel gaps, trim, badges, fasteners, and small details.
9. Render matching views/crops and compare each high-priority region against its reference crop before final detailing.

**Surface design**
- Build the body as continuous surfaces where possible; avoid disconnected flat plates masquerading as a shell.
- Use a low-control-point Subdivision cage for flowing body panels.
- Maintain smooth tangent transitions across hood, fenders, doors, roof, and quarter panels.
- Keep wheel arches consistently circular/elliptical and centered on wheel hubs.
- Use separate objects for glass, lights, tires, rims, mirrors, and trim when that improves editability.
- Use curves or carefully modeled geometry for window seals, trim strips, and panel lines.
- Panel gaps should have consistent width and believable depth. Avoid black painted lines as a substitute for every physical gap.
- Model tire sidewalls with a rounded profile; avoid flat cylinders with no shoulder curvature.
- Ensure wheels are correctly oriented, centered, and visibly grounded.
- Inspect front/side/rear/three-quarter views before adding details.

**Topology**
- Keep loops flowing around wheel arches, openings, and major body transitions.
- Match edge counts before bridging surfaces.
- Use Grid Fill only when the boundary loop is suitable; manually redirect edge flow when it is not.
- Fade crease lines into the surface instead of ending them abruptly in the middle of a panel.
- Avoid poles or dense topology in highly reflective curvature zones when they create visible pinching.

## 2.4 Hard-surface props and mechanical assets

- Start with the primary silhouette and functional visual zones, not screws and grooves.
- Separate parts when they have different materials, movement, assembly logic, or shading requirements.
- Use bevels to catch light: a perfectly sharp real-world edge often looks CG-flat.
- Keep bevel width proportional to object scale. Tiny objects need smaller bevels; hero props may need larger visible edge radii.
- Use multi-segment bevels for rounded edges and one segment for a crisp chamfer.
- Apply scale before beveling or sculpting when non-uniform scale would distort the result.
- Use Boolean cutters for designed holes, slots, vents, and recesses. Keep cutters separate and named until the design is stable.
- Inspect Boolean results for sliver faces, overlapping geometry, flipped normals, and thin bevels.
- Use support loops or creases for subdivision-controlled rounded housings.
- Use weighted normals/hardened bevel normals for flat machined surfaces, but do not use shading modifiers to hide broken geometry.
- Use circular loops for ports, barrels, sockets, and holes; maintain consistent radial segment counts where connected.
- Build repeated screws, vents, ribs, buttons, and grooves as reusable details or linked duplicates.
- Use floating geometry only when the seam is hidden by design or shading is intentionally managed. Do not assume intersecting parts will automatically look welded.


## 2.5 Organic and damaged surfaces

- Use sculpting for irregular, non-mechanical forms; do not try to create every rock, dent, or torn edge from cubes.
- Use Multires when you need to preserve the base mesh and move between sculpt levels.
- Use voxel remesh/Dyntopo only when appropriate; they can change topology and may require retopology afterward.
- Build damage at multiple scales: large missing chunks, medium cracks/chips, small surface breakup.
- Avoid evenly distributed noise. Real wear is directional and concentrated at exposed edges, contact points, corners, and high-use areas.
- Break symmetry after establishing the main form.
- Use alpha brushes as accents, not as a substitute for sculpted structure.
- For game assets, bake high-frequency sculpt detail onto a clean low-poly mesh where appropriate.

## 2.6 Architecture and modular environments

- Establish floor heights, wall thickness, door/window dimensions, and a modular grid before detailing.
- Use modular wall/facade pieces with consistent pivots and dimensions.
- Use image planes as reference or texture projection aids, not as a replacement for all geometry.
- Extrude balconies, ledges, frames, pillars, and recesses to create real depth.
- Fix UVs on side faces created by extrusion.
- Separate glass, frames, doors, vents, AC units, cables, and pipes into logically named objects.
- Use curves for overhead wires and pipes; use bevel/taper to vary thickness.
- Duplicate and rotate modules only after checking corner joins, scale, and texture continuity.
- Avoid repeating identical damage, props, and window patterns too uniformly; add controlled variation.

---


## 2.7 AI design reasoning mode: think before modeling

For every complex asset, perform a design-reasoning pass before creating geometry. Treat the asset as a system of components, surfaces, interfaces, and details—not as one giant shape.

### Required thinking sequence
1. Understand the object, intended use, style, visible views, and reference limitations.
2. Decompose it into systems, components, and subcomponents; create a component tree.
3. Define interfaces: attachment points, seams, overlaps, movement, contact surfaces, and clearances.
4. Choose a modeling method per component: curves, subdivision cages, bevel/boolean meshes, sculpting, profile/loft construction, or Geometry Nodes.
5. Establish shared datums and dependencies before modeling dependent parts.
6. Build in dependency order, keeping components editable.
7. Verify each important component against its reference crop and neighboring geometry.
8. Verify the complete assembled asset from all required views.

### Component separation rules
Create a separate object when a part has a distinct physical boundary, material, movement, assembly role, topology/UV requirement, or needs independent editing/export. Keep geometry continuous when the reference shows one uninterrupted surface and splitting it would create an inaccurate seam or shading break. Do not create an object for every tiny polygon. Use the hierarchy **asset → system → component → detail** and organize it with collections and clear names.

### Example: racing-car front-end decomposition
Do not model the nose as one rounded block. Reason about it as separate visual/physical components:
- **Body shell:** hood/bonnet, left/right fenders, bumper cover, front-quarter transitions.
- **Aerodynamics:** splitter, end plates, canards/dive planes, grille opening, brake ducts, visible inner duct walls.
- **Lighting:** left/right headlamp housings, lens covers, internal lamp elements.
- **Wheel assembly:** tire, rim/barrel, spokes, center cap, brake disc, caliper, wheel arch/liner.
- **Secondary parts:** tow hook, fasteners, badges, panel gaps, seals, and trim.
Apply the same decomposition at the rear for bumper, diffuser, exhaust outlets, wing, end plates, taillights, and vents when supported by the reference. This is a reasoning template, not a mandatory parts list. Never invent a feature and claim it came from the image.

For every important component, define: name/parent system; governing crop; main shape and proportions; material; neighboring parts and attachment method; gap/overlap requirements; modeling method; verification view; and evidence confidence (**observed**, **partially observed**, or **inferred**). Keep low-confidence inferred components simple and editable.

## 2.8 Reference-image zoom, crop, and verification protocol

Treat a reference image as a set of measurable visual regions, not a picture to glance at once.

### Image inspection workflow
1. Preserve the original image and record resolution/aspect ratio.
2. Inspect the full image for camera angle, perspective, lighting, occlusion, and visible surfaces.
3. Create named zoom crops when tools/runtime allow. For a car, inspect: overall silhouette/roofline; nose/bumper/splitter; hood/fender/headlamp; front wheel/arch; side skirt/door/mirror/intake; rear quarter/rear wheel; rear bumper/diffuser/wing/taillights; glass/pillars/panel seams.
4. Maintain a crop index: crop name, source-image coordinates, purpose, and confidence.
5. Zoom enough to inspect contours, seams, curvature, vents, lamps, and attachments, while retaining surrounding context.
6. If cropping/zooming is unavailable, do not pretend it happened. Use an available image viewer or local image-processing route if the source is accessible; otherwise request higher-resolution close-ups or state the limitation.

### Evidence versus inference
- **Observed:** directly visible in the reference.
- **Partially observed:** visible but occluded, blurred, or too small to resolve.
- **Inferred:** hidden or not represented by the available view.
- **Designed addition:** intentionally added, not claimed to be reference-accurate.

A single left-side image can constrain the side silhouette and visible side details. It cannot uniquely determine front/rear width, roof cross-section, opposite side, underside, or hidden depth. Use additional views when all-side fidelity matters; otherwise make conservative assumptions and label them inferred.

### Crop-to-render verification
For each high-priority crop: identify contours, landmarks, panel boundaries, and ratios; model the relevant component; render a matching view; crop the render to the same region/aspect ratio; compare side-by-side or with an opacity overlay; check silhouette, landmark positions, curvature, gaps, and detail placement; fix the largest mismatch first; repeat. Do not refine tiny vents while wheel placement, body contour, or roofline is still wrong. Overlays are diagnostic aids, not proof of correct 3D depth.

## 2.9 Architectural and engineering thinking methods

These methods improve visual modeling discipline; they do not certify mechanical function or safety.

### A. Systems engineering and functional decomposition
Treat the asset as subsystems with interfaces. Trace important features through **reference evidence → design requirement → component → geometry → verification view**. Track dependencies so a change to a parent form triggers inspection of attached parts.

### B. Datum-based construction
Set a global origin, unit scale, axes, center planes, ground plane, and key reference planes. Use empties, curves, planes, and helper meshes as datums. Derive dependent dimensions from shared references rather than eyeballing each component independently. Preserve symmetry unless the reference proves otherwise. For a car, wheel centers, axle planes, longitudinal centerline, and ground plane are critical datums.

### C. Feature-based and parametric design intent
Expose key parameters such as wheelbase, wheel radius, track width, body width, ground clearance, panel gap, bevel radius, and vent spacing. Keep source curves, Boolean cutters, profile sketches, reference meshes, and source cages editable until approval. When a key parameter changes, re-check dependent parts and clearances. Use procedural graphs only when they add real editability or repeatability.

### D. Cross-section stations and loft thinking
For long compound surfaces—car bodies, aircraft fuselages, hulls, product housings, architectural shells—define cross-section stations along the main length. At each station, set width, height, crown, shoulder, and lower contour. Keep point order consistent, loft/interpolate with controlled continuity, add stations only where shape changes, and inspect transverse sections plus longitudinal highlights for waviness. A side view alone cannot define these cross-sections.

### E. Surface continuity: G0 / G1 / G2
- **G0 positional:** surfaces meet without a gap.
- **G1 tangent:** tangent directions align for a smooth directional transition.
- **G2 curvature:** curvature changes smoothly across the transition, important for premium reflective surfaces.
Use G0 at intentional seams, G1 for smooth adjoining surfaces, and G2-like highlight flow on hero bodywork. Preserve intentional creases. Inspect with a glossy neutral material and broad studio reflections.

### F. Assembly, clearance, and tolerance thinking
Define consistent gaps and overlaps. Check tire/fender clearance, door/arch relationships, lamp/housing fit, trim-to-body contact, and motion envelopes when animation is requested. Prevent coplanar z-fighting and add thickness where openings reveal the interior. Do not invent manufacturing tolerances or claim mechanical fit from visual estimates; preserve exact tolerances if supplied by the user.

### G. Design for assembly and maintainability
Organize by system/component; give moving parts useful pivots; name parts by function and side (e.g. `Wheel_Front_Left`, `Headlamp_Front_Right`). Use collections such as `00_References`, `01_Datums`, `10_Body`, `20_Aero`, `30_Wheels`, `40_Lighting`, `50_Details`, and `90_Cutters`. Keep references, cutters, high-poly sources, and presentation geometry separated. Do not join the entire asset merely to tidy the Outliner.

### H. Verification-driven development (mini V-model)
Give every requirement a test view: side silhouette → side orthographic overlay; symmetry/track width → front/rear orthographic; hood/roof curvature → three-quarter highlight render; wheel fit → wheel-arch close-up; panel gaps → macro crop; complete assembly → turntable/multi-view sheet. A stage is complete only after inspection against its requirement, not merely because a script ran.

# 3. Asset planning and task decomposition

The agent must plan the work in small, verifiable stages. Never attempt a complex asset in one giant operation.

## 3.1 Before touching geometry

Create an internal asset brief:

- Asset name and category.
- Intended use: game, cinematic, product render, animation, 3D print, or preview.
- Style: realistic, stylized, low-poly, mid-poly, or high-poly.
- Reference images and required views.
- Approximate real-world dimensions and units.
- Required parts and moving/separate components.
- Detail priority: hero areas versus hidden areas.
- Polycount/performance target if supplied.
- Required materials, textures, UVs, and export format.
- Deliverable location and naming rules.

If critical information is missing, make conservative assumptions and state them. Ask a question only when the missing information would materially change the asset.

## 3.2 Standard staged workflow

### Stage A — Scene inspection and preparation
- Inspect current scene, active collection, units, existing objects, materials, and render settings.
- Do not delete or overwrite user content without permission.
- Create a dedicated collection for the asset.
- Set units and a sensible origin/pivot.
- Save an initial version.

### Stage B — Reference and blockout
- Load and align references.
- Create only the major volumes and silhouette.
- Use temporary materials with clear contrast if needed.
- Check front, side, top, and three-quarter views.
- Do not add small bevels, screws, labels, or textures yet.

**Gate:** do not proceed until proportions and silhouette are acceptable.

### Stage C — Primary form refinement
- Replace crude primitives with the correct modeling method.
- Establish compound curvature, wheel arches, openings, transitions, and major cuts.
- Keep geometry editable and modifiers non-destructive where practical.
- Check symmetry and dimensions.

**Gate:** the asset should already be recognizable without small details.

### Stage D — Secondary forms
- Add panels, housings, windows, ribs, handles, vents, seams, and major attachments.
- Separate objects when material, assembly, or editability requires it.
- Check intersections and attachment surfaces.

### Stage E — Tertiary detail
- Add fasteners, grooves, labels, surface wear, small bevels, and texture details.
- Use instances/linked duplicates for repeated details.
- Do not add detail that cannot be seen at the final camera distance.

### Stage F — Materials and UVs
- Apply physically plausible material values.
- Unwrap deliberately; inspect UV stretching and overlaps.
- Use texture maps only when they add visible value.
- Set data maps (normal, roughness, metallic, displacement) to Non-Color.
- Keep material naming consistent.

### Stage G — Lighting and presentation
- Choose a camera that communicates the silhouette and key details.
- Use a simple key/fill/rim or studio setup as appropriate.
- Use reflections to reveal surface quality.
- Render a neutral clay pass and a material pass.
- Avoid using glow/bloom to disguise poor modeling.

### Stage H — Quality assurance and delivery
- Inspect all requested views.
- Check normals, shading, non-manifold edges where relevant, intersections, modifiers, UVs, and object names.
- Save the final `.blend` and export only the requested formats.
- Report what was completed and any known limitations.

## 3.3 Task breakdown example: vehicle

Do not ask the agent to "make a complete realistic car" in one step. Break it down:

1. Reference alignment and dimensions.
2. Wheel centers, tire envelopes, wheelbase, track width.
3. Main body silhouette blockout.
4. Hood, cabin, roof, trunk and bumper volumes.
5. Fender and wheel-arch curvature.
6. Glasshouse and pillars.
7. Front/rear fascia.
8. Wheels, tires, rims and brakes.
9. Lamps, mirrors, handles, grille and vents.
10. Panel gaps, seals and trim.
11. Materials, UVs and decals.
12. Studio lighting, camera and multi-view QA.

## 3.4 Task breakdown example: complex hard-surface prop

1. Reference and dimension study.
2. Major silhouette blockout.
3. Main housing and large separate components.
4. Openings, ports, slots and recesses.
5. Bevel and shading setup.
6. Secondary attachments and controls.
7. UV layout and material separation.
8. Surface details and wear.
9. Camera, lighting and render checks.
10. Cleanup and save/export.

---

# 4. Blender MCP execution protocol

MCP implementations differ. First inspect available tools and their descriptions. Prefer explicit typed tools for common operations; use Python/BMesh scripting only when the exposed tools cannot express the required geometry or modifier setup.

## 4.1 Read before write

Before editing:
- Build a component tree and identify shared datums for complex reference-driven assets.
- Build a reference crop index for high-priority regions when image tools permit.
- Query scene/object state.
- Inspect object names, types, transforms, dimensions, modifiers, materials, collections, and selection.
- Capture a viewport screenshot or render if supported.
- Identify what already exists and what must be preserved.

After every meaningful modeling pass:
- Query the changed object data.
- Capture a screenshot/render.
- Compare it against the intended reference and current stage.
- For reference-driven hero assets, compare the relevant render crop against the corresponding source crop, not only the full image.
- Fix visible problems before continuing.

For complex assets, create the component tree and reference-crop index before issuing geometry commands. If the connected MCP tools cannot inspect/crop images, use an available local image-processing route only when the source image is accessible; otherwise ask for close-up references or state the limitation. Never fabricate crop inspection.

Do not blindly issue long sequences of geometry commands without checking the result.

## 4.2 Use the right operation

- Prefer curves for flexible paths, cables, hoses, trim, and continuous tubes.
- Prefer mesh topology for surfaces that need precise openings, panels, and edge flow.
- Prefer modifiers for reversible bevels, mirrors, arrays, solidify, subdivision, and shrinkwrap.
- Prefer Geometry Nodes for repeated or parameterized systems.
- Prefer sculpting for organic surface form and irregular damage.
- Use Boolean operations for designed cuts, not as an excuse to skip cleanup.
- Use image references and orthographic alignment for proportion-critical assets.

## 4.3 Script quality rules

When using Blender Python:
- Use `bpy` for scene/object/material/modifier operations and `bmesh` for mesh construction/editing where suitable.
- Use descriptive variables and object names.
- Use functions for repeated operations; avoid giant monolithic scripts.
- Make scripts idempotent where possible: rerunning should update known objects rather than create endless duplicates.
- Check whether objects/materials/collections already exist before creating them.
- Apply transforms intentionally, not automatically to everything.
- Keep source curves, cutters, and high-poly meshes in clearly named collections when they are useful for future edits.
- Validate object existence and operation results after writes.
- Handle exceptions and report the exact failing step; do not silently continue after a failed operation.
- Avoid hard-coded assumptions about active object, selection, mode, or collection.
- Use Blender-version-aware API properties. If a property/operator is unavailable, inspect the current API or use an equivalent supported operation.

## 4.4 Modifier order and non-destructive design

Modifier order is part of the model design. Typical examples (not universal):

- Mirror → primary shape operations → bevel → normal correction.
- Subdivision after the base cage and support-loop/crease design.
- Shrinkwrap on a limited vertex group for fitted borders.
- Data Transfer after the host surface and target attachment are stable.
- Solidify after defining a clean surface when thickness is required.

Always inspect the evaluated result. Do not blindly copy a modifier stack from one object to another if scale, topology, or target objects differ.

## 4.5 Visual feedback loop

Use this loop repeatedly:

**Plan → Build one stage → Inspect screenshot/render → Compare → Correct → Save checkpoint.**

For complex assets, use at least:
- Front orthographic.
- Side orthographic.
- Top orthographic.
- Rear orthographic when relevant.
- Three-quarter perspective.
- Close-up of the most difficult transition.

A single perspective screenshot is not enough to validate a vehicle, symmetric prop, or multi-sided asset.

---

# 5. Quality assurance checklist

## Reference reasoning and component architecture
- [ ] Component tree created before detailed modeling.
- [ ] Components separated by physical boundary, material, movement, or editability—not arbitrarily.
- [ ] Shared datums and dependency relationships are defined.
- [ ] Reference crops inspected for all high-priority regions where tools permit.
- [ ] Observed versus inferred features are distinguished.
- [ ] High-priority render crops compared with source crops.

## Reference reasoning and component architecture
- [ ] Component tree created before detailed modeling.
- [ ] Parts separated by physical boundary, material, movement, or editability—not arbitrarily.
- [ ] Shared datums and component dependencies are defined.
- [ ] High-priority reference regions zoomed/cropped where tools permit.
- [ ] Observed, partially observed, and inferred features are distinguished.
- [ ] Important render crops compared against their source crops.

## Silhouette and proportions
- [ ] Recognizable from the required views.
- [ ] Major dimensions and ratios match references or stated assumptions.
- [ ] Curves are smooth and intentional.
- [ ] No accidental box-like substitution for designed forms.
- [ ] Negative spaces and openings have believable proportions.

## Geometry and topology
- [ ] No unintended holes, duplicate faces, or overlapping geometry.
- [ ] No obvious self-intersections.
- [ ] Edge flow supports the intended curvature.
- [ ] Bevel widths are consistent and scale-appropriate.
- [ ] Boolean artifacts and thin sliver faces are corrected.
- [ ] Subdivision surfaces do not pinch.
- [ ] Curve radius and tilt are controlled.
- [ ] Normals and smoothing behave correctly.

## Materials and UVs
- [ ] Material response matches the intended material (metal, rubber, glass, paint, plastic, stone, etc.).
- [ ] UVs are not visibly stretched.
- [ ] Data textures use Non-Color.
- [ ] Texture resolution is appropriate to camera distance.
- [ ] Material slots and names are organized.

## Presentation
- [ ] Camera shows the important silhouette and design details.
- [ ] Lighting reveals curvature rather than flattening it.
- [ ] Neutral/clay render has been inspected.
- [ ] No clipping, accidental crop, or distracting background.
- [ ] Render quality is adequate for the requested output.

## Project hygiene
- [ ] Collections are organized.
- [ ] Objects have meaningful names.
- [ ] Origins and transforms are intentional.
- [ ] Modifiers are named/ordered sensibly.
- [ ] High-poly, low-poly, references, and cutters are separated when applicable.
- [ ] Final project is saved and requested exports exist.

---

# 6. Common failure patterns and corrections

| Failure | Likely cause | Required correction |
|---|---|---|
| Everything looks like cubes | Primitive-only construction; no silhouette study | Rebuild primary forms using curves, Subdivision cages, bevels, or sculpting |
| Vehicle looks like a toy block | Incorrect body proportions; no compound curvature | Recheck orthographic references, wheel placement, cabin, hood, fenders and highlight flow |
| Curves look kinked | Too many control points or wrong handle types | Reduce points, adjust tangents, use aligned/automatic handles where suitable |
| Hose thickness is uniform and artificial | No radius/taper variation | Use per-point radius or taper curve |
| Pipe joints look intersected | Two tubes overlap without a designed junction | Build a continuous curve, bridge loops, or create a proper junction |
| Subdivision pinches | Poor pole placement, uneven loops, abrupt edge flow | Redirect topology and move poles away from reflective curvature |
| Bevels look melted | Width too large, overlapping edges, wrong modifier order | Reduce width, enable clamp overlap, inspect scale and topology |
| Smooth shading makes hard edges look soft | No bevel/support edges or incorrect normals | Add controlled bevels, mark sharp boundaries, use weighted normals appropriately |
| Boolean leaves ugly shading | Sliver faces, bad topology, insufficient bevel clearance | Adjust cutter, clean topology, bevel selectively, inspect normals |
| Floating detail looks pasted on | Poor fit or normal mismatch | Use face snapping, shrinkwrap a controlled border, transfer normals if appropriate |
| Sculpt detail disappears in game mesh | No high-to-low bake or bad bake setup | UV unwrap low mesh, bake normal/displacement, verify tangent space and ray distances |
| Asset is detailed but unreadable | Tertiary details added before primary forms | Return to silhouette and primary/secondary forms; remove noise |
| Scene becomes chaotic | No collections, naming, checkpoints | Organize by asset/component and save incremental versions |

---

# 7. Blender version and feature awareness

This skill references modern Blender workflows. Always inspect the installed Blender version before using a feature or Python API property.

As of this skill's research date (2026-11-12), the official Blender release page lists **Blender 5.2.4 LTS (2026-11-10)**. Blender 5.2 LTS includes:
- A Geometry Nodes **Mesh Bevel** node for procedurally beveling selected edges or vertices.
- Native modeling improvements including LoopTools operators such as Circle, Space Edge Loops, and Flatten.
- New node-based cloth and hair simulation workflows.
- Improved sculpting tools and remesh attribute preservation.
- Online Asset Library improvements.

Do not assume a feature exists in Blender 4.x or earlier merely because it is documented for 5.2. If the user’s installed version is older, use the closest supported equivalent.

---

# 8. Recommended response and execution behavior

When the user asks for an asset, follow the MANDATORY EXECUTION CONTRACT at the beginning of this file. The following legacy summary is subordinate: interpret the brief, plan, build one task, verify it, checkpoint it, and only then advance. Never keep phases merely internal when the user needs a plan or task ledger.

When a stage fails:
- State what failed and why, if known.
- Do not pretend the asset is complete.
- Roll back or repair the smallest affected stage.
- Re-inspect after the correction.

**Do not:**
- Use boxes for every part by default.
- Add random bevels to make a primitive look "detailed."
- add micro-details before proportions are approved.
- use Shade Smooth to hide bad topology.
- apply every modifier prematurely.
- create dozens of objects without naming or collections.
- claim realism without inspecting multiple views.
- claim a successful save/export unless the operation confirms it.

**Definition of done:** the asset has a correct silhouette, intentional form transitions, clean visible shading, appropriate detail density, organized scene structure, and has been inspected from the views required by the brief.

---

# 9. References

## Supplied video sources
1. [Ryan King Art — Blender Curves](https://www.youtube.com/watch?v=gxzWCH1Q4fM)
2. [Grant Abbitt — Multiresolution Sculpting and Baking](https://www.youtube.com/watch?v=LvFilHJfinU)
3. [On Mars 3D — Universal Modeling Workflow](https://www.youtube.com/watch?v=p5N5oikFWE8)
4. [Aryan 3D — Car Modeling](https://www.youtube.com/watch?v=NDPeZ7YZgrc)
5. [BlenderVitals — Low-poly Building from Photo](https://www.youtube.com/watch?v=j-WegUytMA8)
6. [Isto Inc. — Glock Modeling Challenge](https://www.youtube.com/watch?v=XEaoHoH4qf0)
7. [CG Boost — Hard-surface Modeling Tricks](https://www.youtube.com/watch?v=Ml2t8uxPAQU)

## Additional Blender documentation and research
- [Blender 5.2 LTS release notes](https://www.blender.org/download/releases/5-2/)
- [Blender 5.2 LTS manual](https://docs.blender.org/manual/en/5.2/)
- [Curves manual](https://docs.blender.org/manual/en/5.2/modeling/curves/index.html)
- [Curve geometry: bevel, taper, extrusion](https://docs.blender.org/manual/pt/5.2/modeling/curves/properties/geometry.html)
- [Geometry Nodes introduction](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/introduction.html)
- [Geometry Nodes Mesh Bevel node](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/mesh/operations/mesh_bevel.html)
- [Weighted Normal modifier](https://docs.blender.org/manual/en/5.2/modeling/modifiers/normals/weighted_normal.html)
- [Render baking](https://docs.blender.org/manual/en/5.2/render/cycles/baking.html)
- [Mesh structure and custom normals](https://docs.blender.org/manual/en/5.2/modeling/meshes/structure.html)
- [Bevel modifier](https://docs.blender.org/manual/pt/5.2/modeling/modifiers/generate/bevel.html)
- [Blender MCP example architecture](https://github.com/ageless-h/blender-mcp)

**Research note:** Blender MCP is a community integration category, not one universal official tool contract. Inspect the connected server's actual tool list and capabilities before planning operations.


## 10. Advanced reasoning rule

**Think in systems, construct from datums, model by component, shape by cross-section, and verify by evidence.** The agent must use this sequence on complex reference-driven assets. It must not jump directly from a single image to a monolithic mesh. A professional result comes from correct decomposition, controlled interfaces, deliberate surface continuity, and repeated visual verification—not from adding more polygons.

---

# 11. Mandatory request interpretation and reference intake (highest-priority rules)

This section overrides any weaker or conflicting guidance above. Apply it before creating, editing, or repairing geometry.

## 11.1 Determine what the user actually asked to build

Classify the request before touching Blender:
- **Image-led:** one or more images are attached and are intended as visual references.
- **Text-led:** the user describes an object or scene without a reference image.
- **Hybrid:** text and images jointly define the target; explicit text constraints take precedence over visual inference.
- **Edit/repair:** the user asks to modify an existing `.blend` scene or selected objects.

Identify the target category explicitly: vehicle, building, room/interior, environment, character/creature, furniture, product, mechanical prop, organic asset, or other. Do not assume every image depicts a vehicle. Read labels, captions, callouts, dimensions, view names, and component annotations. If multiple objects are shown, identify which is the requested target and which are supporting references.

Before modeling, write a compact **Interpretation Record**:
1. Requested asset and category.
2. Intended use and quality style (game-ready, cinematic/hero, product visualization, 3D print, architectural visualization, blockout, etc.).
3. Explicit constraints from the user (dimensions, triangle/vertex budget, style, views, separate parts, file format).
4. Reference coverage and confidence.
5. Assumptions and unknowns.
6. Feasibility decision: feasible, feasible with trade-offs, or infeasible as specified.

If the target object is genuinely ambiguous and choosing incorrectly would waste substantial work, ask one concise clarification. Otherwise state a reasonable assumption and proceed.

## 11.2 Image reference analysis — mandatory when images are attached

Inspect every supplied image at useful zoom. Do not merely describe the overall picture. Build a **Reference View Matrix**:

| View/evidence | What to extract |
|---|---|
| Front / rear / left / right orthographic | Width, height, symmetry, silhouette, openings, placement |
| Top / bottom | Planform, footprint, roof/hood/deck layout, underside structures |
| Three-quarter / perspective | Surface transitions, depth, assembly relationships |
| Close-ups / exploded views | Small parts, joints, internal layers, mounting logic |
| Dimensions / scale bars | Real-world dimensions and ratios |
| Labels / callouts | Exact part names and intended separation |

Rules:
- If all sides are supplied, use them together as a multi-view specification. Do not model only the most attractive perspective view.
- Align views to a shared coordinate system and common scale where possible. Record view disagreement instead of silently averaging incompatible references.
- Extract the silhouette and landmarks first: corners, axes, wheel centers, roofline, window boundaries, door/window openings, floor levels, roof edges, façade bays, etc., according to the asset category.
- Create a **Component Breakdown** from visible seams, material boundaries, labels, physical joints, openings, separate moving parts, and assembly logic.
- Separate subcomponents when they are physically distinct, independently movable, differently shaded/materialled, replaceable, or need independent editing. Do not split every visual region into arbitrary objects; continuous body surfaces should remain continuous where appropriate.
- For a vehicle, investigate body shell, hood, trunk, doors, fenders, bumpers, grille, headlamp housings/lenses, glass, seals, mirrors, wheels, tires, rims, brakes, wheel-well liners, undertray, exhaust, interior, aero parts, and hood underside where shown or implied by the requested fidelity.
- For buildings, investigate foundation, structural frame, floor slabs, walls, roof, façade layers, doors, windows, frames, balconies, stairs, railings, parapets, roof equipment, interior partitions, and site/landscape only when requested or visible.
- For rooms/interiors, identify shell, floor/ceiling, openings, trim, built-in furniture, movable furniture, fixtures, lighting, and repeated props.
- For products/mechanical props, identify housing, covers, panels, fasteners, ports, joints, controls, inserts, lenses, gaskets, and internal/underside details when visible or required.
- Mark each feature as **Observed**, **Partially observed**, or **Inferred**. Never present inferred details as facts from the reference.
- If a view is missing, do not invent precise unseen geometry. Use a conservative, physically plausible completion and label it inferred, or ask for a missing view when it materially affects the result.
- If the image is a concept sheet, use the actual design shown; do not substitute a generic or more familiar design.
- Reference images are design evidence, not permission to ignore written constraints.

## 11.3 Text-only prompt: create a mental reference before modeling

When the user gives only text, do not jump directly into primitive creation. First construct an internal **Visual Design Brief** as if preparing a real-world reference board:
1. Identify the exact named object/category and intended variant.
2. Determine its real-world function, typical construction, proportions, materials, and major subassemblies from reliable knowledge. For unfamiliar or contemporary named objects, research if available; otherwise state uncertainty.
3. Define a coherent design language (era, style, manufacturer/model only if specified, environment, wear, manufacturing logic).
4. Establish plausible dimensions and ratios. If dimensions are not supplied, choose documented/typical proportions only when sufficiently grounded; otherwise label them assumptions.
5. Describe the object in front, rear, left, right, top, bottom, and three-quarter views as relevant.
6. Identify components, seams, openings, thickness, internal/underside features, and assembly order.
7. Identify what must be actual geometry versus material/texture/normal-map detail.
8. If image generation/reference lookup is available and useful, create or retrieve a **planning reference** before modeling. Treat generated imagery as a design aid, not authoritative engineering evidence. Do not pretend a generated image is a verified photograph or blueprint.
9. Convert the brief into a Component Breakdown and Phase Plan.

Do not create an image if the user did not request one and the tool is unavailable; the essential requirement is to reason through a concrete multi-view visual specification before building.

## 11.4 Real-world plausibility and honest feasibility gate

Before execution, check whether the requested design can be built within the supplied constraints and the available Blender MCP capabilities.

Check:
- Are the dimensions and proportions mutually consistent?
- Can required shapes, openings, undercuts, curves, thicknesses, and separate parts be represented with the selected technique?
- Is the requested polygon/triangle budget sufficient for the requested silhouette and visible detail at the target camera distance?
- Are texture resolution, UVs, material count, rigging, animation, simulation, or printability requirements compatible with the target?
- Can the connected MCP tools actually perform and inspect the necessary operations?

If the request is infeasible as written:
- **Stop before destructive or expensive modeling.**
- Explain exactly which requirement conflicts with which constraint.
- Give the minimum practical triangle/vertex/texture/part budget estimate or a range, and explain the quality trade-off.
- Offer the closest feasible alternative (for example, bake detail into normal maps, reduce hidden geometry, use LODs, split hero and game-ready versions, or relax the target).
- Ask the user to approve the changed target when it materially changes their request.

Never silently exceed a hard budget. Never promise that an arbitrary triangle count guarantees realism. Never reject a request merely because it is ambitious if a feasible staged or multi-resolution approach exists.

## 11.5 Polygon and performance budgeting — define what is being counted

A polycount requirement is incomplete until the agent clarifies or states:
- Triangles, quads, or vertices?
- Evaluated mesh or base mesh?
- Whole scene or asset only?
- Include hidden geometry, interior, fasteners, cables, and duplicates?
- Include modifier-evaluated subdivision/instances?
- Target platform and camera distance?

Use **evaluated triangle count** as the default for a whole asset unless the user specifies otherwise. Report both base and evaluated counts when modifiers materially change the result. Distinguish unique mesh data from instances and distinguish render-time geometry from exported geometry.

Budget is a constraint and diagnostic, not a quality score. Allocate triangles according to silhouette curvature, screen-space visibility, deformation, and detail needs. Curved hero surfaces, wheels, openings, and close-up parts need more geometry than hidden flat panels. Do not inflate counts with useless subdivisions, hidden duplicate meshes, or triangulation that adds no visible quality.

Use these starting estimates only as planning heuristics, never universal facts:
- Simple low-poly prop: roughly 500–5,000 triangles.
- Medium game prop: roughly 5,000–30,000 triangles.
- Detailed hero prop: roughly 30,000–150,000+ triangles.
- Detailed hero vehicle: roughly 150,000–800,000+ triangles depending on interior, underside, wheel detail, and close-up requirements.
- Architectural hero asset/building: highly variable; plan by façade complexity, interiors, repeated modules, and camera coverage rather than a single fixed number.

If the user specifies a hard target (e.g. 600K triangles), determine whether the complete requested asset can reasonably meet it. If it is excessive for a game target, explain and propose LODs; if insufficient for a close-up hero asset, explain and suggest a minimum range. Never confuse a 600K target with a universal minimum for every vehicle.

---

# 12. Phase-and-task execution contract (mandatory MCP workflow)

Complex assets must be built as **Phases**, each containing small named **Tasks**. Every task must include: objective, affected objects/components, exact operations, acceptance criteria, verification method, evidence to capture, and status.

## 12.1 Plan before geometry

Create a **Model Execution Plan** before modeling:

```text
Asset:
Target use / quality:
Reference source:
Dimensions / assumptions:
Triangle budget (base and evaluated):
Component hierarchy:
MCP capabilities confirmed:

PHASE 01 — Reference interpretation and scene setup
  TASK 01.1 — ...
    Objective:
    Components:
    Operations:
    Acceptance criteria:
    MCP verification:
    Evidence:
    Status: NOT STARTED

PHASE 02 — Primary silhouette and proportions
  TASK 02.1 — ...
  ...

PHASE 03 — Primary surface construction
PHASE 04 — Secondary components and openings
PHASE 05 — Underside / interior / hidden geometry
PHASE 06 — Tertiary details and materials
PHASE 07 — UVs / optimization / LODs (if applicable)
PHASE 08 — Presentation and final QA
```

Adapt phase names to the asset. Do not force vehicle-specific phases onto a building or organic asset. Every phase should have a clear exit gate.

## 12.2 One task at a time — no blind batch modeling

For each task:
1. Read current scene state and confirm the intended target objects.
2. Execute only the operations needed for that task. Use small, reversible changes where possible.
3. Query Blender through MCP after the operation. Do not infer success merely because the tool returned without an exception.
4. Verify the task's acceptance criteria using the strongest available evidence: object data, dimensions, mesh statistics, modifier state, material slots, transforms, geometry checks, and/or screenshots/renders.
5. Compare the relevant view/crop to the reference or visual design brief.
6. If failed, repair the task or roll back the smallest affected change. Re-run the verification.
7. Save a checkpoint after a verified task or a meaningful group of low-risk tasks.
8. Mark the task **VERIFIED** only when evidence supports every required criterion. Otherwise mark **PARTIAL**, **BLOCKED**, or **FAILED** and explain.
9. Only then start the next dependent task.

Do not continue to the next phase while a critical task in the current phase is failed or unverified. Independent non-blocking tasks may proceed only if dependencies are explicit and no failed task contaminates them.

## 12.3 MCP verification is task-specific

Use the connected MCP tools, not assumptions about a universal server API. At the start, enumerate available tools and capabilities. If a required inspection or edit operation is unavailable, report the limitation and use a safe alternative only if it preserves the acceptance criteria.

Examples:
- A proportions task requires measured dimensions and orthographic comparison, not only a successful object creation call.
- A curvature task requires silhouette/highlight inspection and, where possible, surface deviation or cross-section checks; polygon count alone is insufficient.
- A component separation task requires object/collection inspection and proof that intended components are independently editable.
- A normals task requires actual face-orientation/normal checks.
- A material task requires material-slot and assignment checks plus a render/viewport evidence pass.
- A clearance task requires measured distance/intersection checks, not a visual guess alone.
- A hidden-geometry task requires underside/interior views or direct geometry inspection.
- A save/export task requires checking the file operation result and verifying the output exists where the tool supports it.

If screenshot/render capture is unavailable, state that visual verification is unavailable; do not claim visual fidelity was verified. If mesh analysis is unavailable, state that technical verification is incomplete.

## 12.4 Phase gates

Each phase ends with a gate:
- **PASS:** all critical tasks verified; proceed.
- **PASS WITH LIMITATIONS:** only non-critical items remain and user-approved trade-offs are recorded.
- **BLOCKED:** required evidence, reference, MCP capability, or user decision is missing.
- **FAIL:** acceptance criteria are not met; repair before proceeding.

The agent must not mark an entire asset complete while any critical phase is blocked, failed, or unverified.

## 12.5 Progress reporting

Keep reports compact and structured, not scattered. Maintain one progress ledger:

| Phase / task | Status | Verification evidence | Remaining issue |
|---|---|---|---|

Use statuses: NOT STARTED, IN PROGRESS, VERIFIED, PARTIAL, BLOCKED, FAILED. Do not use a checkmark without evidence. At each user-facing update, report only the current phase, verified work, blockers, and next task.

---

# 13. Visual fidelity and geometric QA — not just technical hygiene

Technical validity does not prove that the model resembles the requested object. Evaluate these separately.

## 13.1 Visual fidelity checks

- Overall silhouette and negative spaces from all available reference views.
- Major proportion ratios and landmarks.
- Curvature families and surface transitions: convex, concave, compound, rolled edges, fillets, and intentional creases.
- Highlight flow under a broad neutral studio light; look for waviness, pinching, flat spots, abrupt tangent breaks, and lumpy reflections.
- Cross-sections at critical stations (e.g. vehicle hood/fender/roof, building wall/roof junction, product housing transitions).
- Panel thickness, edge radius, recess depth, openings, and realistic attachment relationships.
- Front/side/rear/top/bottom view consistency.
- Hidden geometry and underside completeness to the fidelity level requested.
- Component presence and correct separation based on the Component Breakdown.
- Material response only after geometry is credible. Do not use dark materials, reflections, shadows, or camera angles to conceal missing geometry.

## 13.2 Geometry evidence

For reflective hero assets, capture:
- Neutral clay render with broad softbox reflections.
- Silhouette renders against a contrasting background.
- Orthographic front/rear/left/right/top/bottom views as relevant.
- Wireframe or topology views for critical surfaces.
- Close-ups of difficult transitions, openings, and assemblies.
- Underside/interior views when required.

Use the same camera framing and scale for reference comparisons. A beauty render alone is not a geometry audit.

## 13.3 Separate score dimensions

Never combine all quality into polygon count. Report independent scores or pass/fail findings for:
1. Reference interpretation and component completeness.
2. Silhouette and proportions.
3. Surface curvature and highlight continuity.
4. Primary/secondary/tertiary form quality.
5. Hidden geometry and assembly logic.
6. Topology, shading, and mesh integrity.
7. Materials/UVs.
8. Performance/budget compliance.
9. Scene organization and deliverables.

A high triangle count cannot compensate for a wrong silhouette, missing hood underside, flat fenders, absent interior, or incorrect part decomposition.

---

# 14. Final delivery contract

The final response/report must contain one consolidated summary:
- What was requested and what was actually built.
- Reference interpretation and assumptions.
- Phase/task completion ledger.
- Visual fidelity findings (including curvature and hidden geometry).
- Base and evaluated triangle counts, with scope clearly defined.
- Technical QA results and unresolved defects.
- Which checks were actually run through MCP and which could not be run.
- Saved `.blend` and exports, with confirmed paths only.
- Known limitations and recommended next actions.

Never claim a feature, part, verification, save, export, or reference comparison happened unless the tool evidence confirms it.

**Highest-priority rule:** Interpret the object correctly, plan its real construction, verify every task, and only then proceed. A successful Blender command is not a successful model.
