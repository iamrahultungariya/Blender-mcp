---
name: blender-visual-reference-intelligence
description: Analyse user-provided or researched visual references for Blender assets. Use when an image, image set, screenshot, blueprint, drawing, photograph, render, or visual target must be interpreted into reliable 3D form evidence, component relationships, proportions, views, and a traceable reference plan before geometry construction.
---

# Blender Visual Reference Intelligence

## Mission

Convert visual references into a **traceable geometric understanding**, not an imaginative description.

This skill answers:
- What is actually visible?
- Which object, variant, generation, configuration, and components are supported by evidence?
- What shape, proportion, alignment, depth, and component relationships can be inferred?
- Which views agree or conflict?
- What is hidden, ambiguous, distorted, cropped, or absent?
- What can be modelled confidently, what needs more evidence, and what must remain explicitly unknown?

**Core rule:** A plausible-looking interpretation is not automatically a reference-supported interpretation.

## Position in the Blender skill system

Use this skill after `blender-preproduction-intelligence` has established the requested subject, scope, intended use, and constraints. Use it before `blender-artist-workflow` creates the component-level modelling plan and before `blender-geometry-engineering` defines construction and geometric verification.

Responsibilities:
- Pre-Production Intelligence: decides what the requested asset is and why it is being made.
- Visual Reference Intelligence (this skill): decides what the visual evidence actually supports.
- Artist Workflow: decides what components to build and in what modelling sequence.
- Geometry Engineering: decides how to construct and mathematically verify those forms.
- MCP execution layer: performs Blender operations and reports observed results.

Do not duplicate the other skills' responsibilities. Do not execute modelling or claim geometry has been verified from images alone.

## Non-negotiable principles

1. **Inspect before interpreting.** Review every supplied image at its available resolution. Do not infer unseen details from a thumbnail or filename.
2. **Identify before measuring.** Establish whether references show the same object, variant, year, body kit, configuration, and viewpoint.
3. **Separate observation from inference.** Never present an inferred feature as directly visible.
4. **Preserve uncertainty.** Unknown means unknown; it is not permission to invent.
5. **Use views together.** Do not treat a perspective image as an orthographic blueprint.
6. **Do not average contradictions blindly.** Resolve source quality, variant differences, camera distortion, and image mismatch first.
7. **Respect occlusion.** A hidden surface is not evidence of a particular shape.
8. **Track provenance.** Every important geometric claim must point to the image and region that supports it.
9. **Do not fake precision.** Measurements from photographs are estimates unless calibrated dimensions or orthographic references exist.
10. **Do not equate visual similarity with geometric accuracy.** A render can look convincing while its underlying form is wrong.

## Activation and inputs

Activate when:
- The user attaches one or more images and asks for a 3D model, reconstruction, analysis, or reference matching.
- The user provides front/side/rear/top/bottom views, blueprints, product photographs, screenshots, sketches, or renders.
- A modelling task depends on identifying components, proportions, silhouette, surface transitions, or hidden geometry.
- A previous modelling result must be compared against reference images.

Before analysis, establish what is available:
- User-supplied images and their order.
- Any written subject/variant description from the approved pre-production brief.
- Existing project screenshots or model views, if supplied.
- External reference material only when research is authorised or necessary.

If the user supplied images, analyse those first. Do not replace them with web images or assume the user wants a different reference. If image access or resolution is insufficient, state the limitation and request a clearer crop/view only when it materially blocks the task.

## Reference evidence model

Classify each claim using one label:

- `DIRECT`: clearly visible in a supplied reference.
- `CROSS_VIEW`: supported by two or more compatible views.
- `SOURCE_VERIFIED`: supported by an identified reliable external source.
- `INFERRED`: reasoned from visible geometry, perspective, symmetry, or component relationships.
- `ASSUMED`: a provisional modelling decision, explicitly marked.
- `UNKNOWN`: insufficient evidence.
- `CONFLICT`: references disagree or may depict different variants.
- `NOT_APPLICABLE`: not relevant to the requested asset.

Every high-impact claim must include:
- Claim ID.
- Description.
- Evidence label.
- Reference ID(s).
- Image region or component location.
- Confidence: High / Medium / Low.
- Reasoning.
- Impact if wrong.
- Required next action, if any.

Confidence is not a substitute for evidence. A high-confidence inference remains an inference.

## Workflow

### Phase 0 — Establish the analysis contract

Read the approved pre-production brief. Extract:
- Exact subject and variant.
- Intended output and camera/use context.
- Required components and exclusions.
- Scale or known dimensions.
- Polygon/triangle budget, if relevant.
- Required views and accuracy level.
- Any approved assumptions.

If the brief is missing, do not silently invent its contents. Ask only for the missing information that materially changes reference interpretation; otherwise proceed with clearly marked unknowns.

### Phase 1 — Reference inventory

Create a reference register. For every image record:
- Unique ID (`REF-01`, `REF-02`, ...).
- Source: user / official / manufacturer / technical document / reputable secondary / unknown.
- Image type: orthographic drawing / technical diagram / photograph / render / screenshot / scan / sketch.
- Apparent view: front / rear / left / right / top / bottom / three-quarter / detail / unknown.
- Subject/variant match status.
- Resolution and visible quality limitations.
- Cropping, obstruction, reflections, shadows, lens distortion, perspective, compression.
- What the image is useful for.
- What it cannot reliably establish.

Never infer the view solely from the file name.

### Phase 2 — Subject and variant consistency

Determine whether all references depict the same:
- Product or vehicle identity.
- Model generation and production year, where relevant.
- Trim, race class, body kit, facelift, regional configuration, or revision.
- Door count, wheelbase, roofline, attachments, accessories, and other variant-sensitive traits.

Use visible discriminators, not branding alone. A logo may identify a brand but not the exact model variant.

If identity is uncertain:
1. List the plausible candidates.
2. Identify visible discriminators.
3. Compare them with source evidence.
4. Mark unresolved identity as `CONFLICT` or `UNKNOWN`.
5. Do not choose a candidate merely because it looks familiar.

### Phase 3 — Image quality and camera assessment

For each reference, assess:
- Perspective vs orthographic projection.
- Camera elevation, azimuth, roll, and approximate focal-length distortion where discernible.
- Lens distortion and foreshortening.
- Subject orientation and image-plane alignment.
- Occluded or cropped areas.
- Lighting/reflection artifacts that may look like geometry.
- Whether straight edges, circles, and parallel lines appear distorted.

Rules:
- Perspective photographs are valid for appearance and component detail, but weak for exact dimensions without calibration.
- Orthographic drawings are strong for projected proportions, but may omit depth, curvature, or hidden features.
- Three-quarter views are useful for volume and transitions, but should not be treated as dimensional ground truth.
- Reflections and highlights are not topology.
- Dark regions are not automatically holes; bright regions are not automatically raised surfaces.

### Phase 4 — View classification and alignment

Map each image to a view and coordinate convention.

Default convention only when the project has not established one:
- Front = negative Y.
- Rear = positive Y.
- Left = negative X.
- Right = positive X.
- Top = positive Z.
- Bottom = negative Z.
- Ground plane = XY.
- Vertical axis = Z.

Do not silently apply this convention if the existing Blender project uses another orientation. Inspect the scene or ask.

For paired views:
- Check whether left/right are mirrored or labelled from the subject's perspective.
- Check wheel positions, door handles, lights, vents, and asymmetric features.
- Identify whether the view is rotated, mirrored, or flipped.
- Align views using stable landmarks only when justified.

Do not combine incompatible images into a synthetic orthographic set.

### Phase 5 — Landmark and proportion extraction

Identify stable landmarks before estimating dimensions.

Examples:
- Vehicle: wheel centres, axle lines, front/rear extremities, roof peak, windshield base, beltline, sill, wheel-arch apex, wing plane.
- Building: ground line, corners, floor levels, openings, roof ridge, eaves, structural grid.
- Furniture/product: bounding extents, support contact points, joints, openings, control locations, major transitions.
- Organic object: major mass centres, silhouette extrema, articulation points, symmetry axes where supported.

For each landmark record:
- ID and name.
- Reference ID and image coordinates or region.
- Whether directly visible or inferred.
- Repeatability across views.
- Confidence and limitations.

Proportion rules:
- Prefer ratios to guessed absolute dimensions when no known scale exists.
- State the denominator and measurement endpoints.
- Do not report false decimal precision.
- If perspective is significant, use qualitative proportions or calibrated reconstruction rather than raw pixel ratios.
- Treat dimensions from different images as comparable only after projection and scale differences are understood.

### Phase 6 — Silhouette and form analysis

Analyse the object in layers:

1. **Primary envelope:** overall length, width, height, mass distribution, dominant silhouette.
2. **Secondary forms:** cabin/body volumes, fenders, roof, wings, supports, housings, structural masses.
3. **Tertiary forms:** openings, seams, recesses, lips, bevels, vents, handles, trim.
4. **Micro details:** fasteners, badges, small grilles, textures, tiny hardware.

#### Multi-Domain Visual Decomposition & Anti-Boxy Screening
- **Architecture & Buildings**: Deconstruct references into foundation plinth $\to$ exterior cavity walls ($\ge 0.20\,\text{m}$ thickness) $\to$ window/door openings with visible reveal jambs and sloped sills ($\ge 0.15\,\text{m}$ depth) $\to$ architectural casing/trim $\to$ roof overhang eaves. Identify wall depth and shadow lines: flat painted window planes with zero reveals indicate invalid cartoon or low-effort geometry.
- **Furniture & Interiors**: Deconstruct references into frame/legs (tapered profiles, foot glides) $\to$ support structure $\to$ crowned cushion volumes (convex double-parabolic puff with seam piping, strictly screening out flat box cushions) $\to$ edge fillets ($2\text{--}6\,\text{mm}$ roundovers). Identify floor-to-wall baseboards and ceiling crown trims in room interior photos.


For each major view describe:
- Outer silhouette.
- Major contour changes.
- Convex/concave transitions.
- Character lines and crease paths.
- Surface break locations.
- Symmetry or asymmetry.
- Component boundaries.
- Areas with insufficient evidence.

Do not let tertiary detail distract from primary proportions and silhouette.

### Phase 7 — Component segmentation and relationships

Build a component map from visible evidence.

For each component capture:
- Component ID and name.
- Parent assembly.
- Function, if known.
- Approximate location and orientation.
- Shape/form description.
- Visible boundaries.
- Interfaces and attachments.
- Symmetry/instance relationship.
- Whether separate object, integrated surface, or uncertain.
- Evidence references.
- Confidence.
- Hidden or unresolved aspects.

Distinguish:
- A visible panel gap from a true separate mesh.
- A trim line from a physical seam.
- A shadow from a recess.
- A decal from a geometric feature.
- A transparent window from an absent surface.
- An aerodynamic appendage from a structural mounting system.

Do not force every visual boundary to become a separate Blender object. That is an artist-workflow decision informed by this evidence.

### Phase 8 — Surface and curvature interpretation

For each major surface identify:
- Surface class: planar / ruled / cylindrical / conical / freeform / blended / unknown.
- Approximate curvature behaviour: flat / single-direction / double-direction / changing / unknown.
- Convex or concave regions.
- Tangent direction and transition locations where visible.
- Whether the surface appears continuous across a component boundary.
- Evidence strength and camera/reflection limitations.

Do not claim G0, G1, G2, curvature continuity, exact radii, or mathematically smooth surfaces from a shaded photograph alone. Such properties require geometric construction data or later mesh/surface inspection.

Use visual cues carefully:
- Silhouette curvature is stronger evidence than a highlight streak.
- Multiple views improve confidence but do not prove continuity.
- Specular highlights depend on material, lighting, and environment.
- A smooth render can conceal poor topology.

Pass surface observations to Geometry Engineering as hypotheses with provenance, not as verified mathematical facts.

### Phase 9 — Occlusion and hidden-geometry policy

Create a hidden-geometry register.

For every hidden region record:
- What is hidden and why.
- Which views partially reveal it.
- Whether the shape is constrained by interfaces, symmetry, function, or known construction.
- Whether it affects visible silhouette, assembly, clearance, or function.
- Evidence status and confidence.

Allowed strategies:
1. Search for additional compatible references if authorised.
2. Request another view from the user.
3. Infer a conservative form from strong constraints and mark it `INFERRED`.
4. Leave it `UNKNOWN` and defer the modelling decision.

Forbidden:
- Inventing exact underside layouts from top views.
- Assuming left/right symmetry where asymmetry is possible.
- Filling occluded regions with arbitrary detail.
- Claiming hidden components are reference-accurate without evidence.

### Phase 10 — Cross-view consistency and conflict resolution

Check:
- Same component location across views.
- Landmark alignment.
- Silhouette compatibility.
- Wheelbase/axle spacing or equivalent structural spacing.
- Overall proportions.
- Component presence/absence.
- Variant-sensitive features.
- Left/right asymmetry.
- Scale consistency.

When views conflict:
1. Confirm they show the same variant.
2. Assess source authority and image quality.
3. Assess projection and camera angle.
4. Check whether the difference is a real configuration change.
5. Record the conflict and evidence.
6. Prefer the strongest compatible evidence; never silently average.
7. If unresolved and high impact, stop the affected decision and request clarification or research.

### Phase 11 — Reference-to-model requirement map

Translate evidence into modelling requirements without prescribing exact construction methods.

Each requirement must contain:
- Requirement ID.
- Component or region.
- Required visible form.
- Relevant views.
- Landmark/proportion constraints.
- Surface behaviour hypothesis.
- Required interfaces.
- Accuracy priority: Critical / High / Medium / Low.
- Evidence and confidence.
- Acceptance observation.
- Open questions.

This map is handed to Artist Workflow and Geometry Engineering.

### Phase 12 — Readiness decision

Assign one state per component:
- `READY`: enough evidence for a reliable modelling plan.
- `READY_WITH_ASSUMPTIONS`: proceed only with documented assumptions.
- `NEEDS_REFERENCE`: missing evidence materially affects the form.
- `CONFLICT_BLOCKED`: incompatible references prevent a safe decision.
- `OUT_OF_SCOPE`: not required.

Overall readiness:
- `READY`: critical components are supported.
- `CONDITIONAL`: limited assumptions remain and are disclosed.
- `BLOCKED`: critical identity, proportions, or component evidence is unresolved.

Do not block the entire asset for a low-priority unknown detail. Isolate the blocked component.

## Output contract

Produce a **Visual Reference Analysis Report** with these sections:

1. Analysis scope and brief inputs.
2. Reference register.
3. Subject/variant consistency.
4. Camera and image-quality assessment.
5. View coverage matrix.
6. Landmark and proportion register.
7. Silhouette/form analysis by view.
8. Component map and relationships.
9. Surface/curvature hypotheses.
10. Occlusion and hidden-geometry register.
11. Cross-view conflicts and resolutions.
12. Reference-to-model requirement map.
13. Confidence and risk summary.
14. Component readiness states.
15. Questions or additional references required.
16. Handoff notes for Artist Workflow and Geometry Engineering.

Use the templates in `templates/visual-reference-analysis-report.md` and the detailed procedures in `references/visual-reference-analysis-playbook.md`.

## Handoff protocol

### To Blender Artist Workflow
Provide:
- Confirmed subject and variant.
- Required components and hierarchy evidence.
- Primary/secondary/tertiary form priorities.
- Landmark and proportion constraints.
- View coverage and missing references.
- Component readiness.
- Explicit assumptions and exclusions.

Do not dictate the complete modelling sequence; Artist Workflow owns that.

### To Blender Geometry Engineering
Provide:
- Surface classes and curvature hypotheses.
- Cross-section/landmark locations where evidence supports them.
- Suspected continuity transitions.
- Interface and fit constraints.
- Regions requiring deviation checks.
- Unknowns that must not be treated as verified geometry.

Do not claim geometric continuity or topology is already validated.

### To Pre-Production Intelligence
Return:
- Identity conflicts.
- Scope changes.
- Research gaps.
- Unresolved requirements that affect feasibility or intended use.

## MCP and tool discipline

- Discover available MCP tools and their actual schemas before invoking them. Never invent tool names, parameters, or capabilities.
- Use image inspection capabilities only if actually available in the current environment.
- If an image cannot be opened, zoomed, cropped, or measured with available tools, state that limitation; do not claim that operation occurred.
- Do not run Blender modelling commands in this skill.
- Do not modify the `.blend` file.
- Do not claim scene geometry, mesh topology, dimensions, or evaluated polygon counts were inspected unless an actual Blender/MCP inspection produced that evidence.
- Keep reference analysis read-only.
- Record tool observations separately from visual interpretations.

## Quality gate

Before finalising, verify:
- Every supplied reference is inventoried.
- Subject/variant identity is supported or uncertainty is explicit.
- Perspective and orthographic evidence are not conflated.
- Important landmarks have traceable provenance.
- Major components and interfaces are mapped.
- Hidden geometry is explicitly handled.
- Conflicting views are documented.
- No unsupported precision or invented detail appears.
- Each critical component has a readiness state.
- Handoff notes are actionable and do not overlap other skills.

If any check fails, revise the report before handing it off.

## Final behaviour

Be precise, sceptical, and transparent. Think like a visual reconstruction specialist: observe first, compare second, infer carefully, and label uncertainty. The goal is not to sound certain; the goal is to make downstream geometry decisions more reliable.
