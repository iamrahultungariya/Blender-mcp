# Visual Reference Analysis Playbook

This document expands the operational method for `blender-visual-reference-intelligence`.

## 1. Evidence hierarchy

Use the hierarchy as a guide, not an absolute ranking. A source is only useful if it depicts the correct subject and variant.

Typical order for identity and specifications:
1. Official manufacturer technical documentation for the exact variant.
2. Official homologation, service, parts, or engineering documentation.
3. Official press/media imagery with clear variant identification.
4. Reputable specialist publications with traceable identification.
5. High-resolution photographs with known provenance.
6. Community images, forum posts, marketplace photos.
7. Unattributed renders, AI images, mood boards, and visual guesses.

For visible appearance, a high-resolution real photograph may be more useful than a low-resolution official brochure. Record why a source was selected.

Never infer source reliability from visual polish.

## 2. Image inspection procedure

For every image:
1. Inspect the entire image.
2. Identify the subject boundaries.
3. Identify camera/view direction.
4. Locate visible landmarks.
5. Identify occlusions and crop boundaries.
6. Separate geometry cues from lighting/material cues.
7. Record useful regions and limitations.
8. Compare with other views only after identity compatibility is checked.

If the environment exposes only a small preview, do not pretend to inspect details outside that preview. Ask for a higher-resolution image or a crop when necessary.

## 3. Orthographic, perspective, and technical drawing interpretation

### Orthographic-like views
Evidence:
- Parallel edges remain parallel.
- No obvious convergence toward vanishing points.
- Circular features retain near-circular projection when viewed normal to their plane.

Potential limitations:
- Drawing may be stylised or simplified.
- Different views may not share a scale.
- Hidden edges may be omitted.
- Dimensions may be rounded.
- A line drawing may not encode surface curvature.

### Perspective photographs
Evidence:
- Strong for visual appearance, material boundaries, relative depth, and visible component detail.
- Weak for raw pixel-based dimension comparison without camera calibration.

Potential limitations:
- Foreshortening.
- Lens distortion.
- Camera tilt and roll.
- Wide-angle exaggeration.
- Occlusion.

### Technical diagrams
Check:
- Units.
- Scale.
- Projection convention.
- Revision/version.
- Whether dimensions refer to overall extents or local features.
- Whether a diagram depicts a prototype, production model, or modified configuration.

Do not treat a dimensionless illustration as a scaled drawing.

## 4. View coverage matrix

Use a matrix to expose missing evidence. Example:

| Region | Front | Rear | Left | Right | Top | Bottom | Detail |
|---|---|---|---|---|---|---|---|
| Primary silhouette | Strong | Strong | Strong | Weak | Medium | None | N/A |
| Wheel/fender interface | Medium | Medium | Strong | Weak | Low | None | Strong |
| Underside | None | None | None | None | None | Weak | None |
| Lighting assembly | Strong | Strong | None | None | None | None | Strong |

Coverage labels:
- `STRONG`: clear and useful.
- `MEDIUM`: partially visible or distorted.
- `WEAK`: ambiguous, cropped, small, or obstructed.
- `NONE`: absent.
- `N/A`: not relevant.

A missing view is not automatically a blocker. Determine whether the missing view affects a critical component or visible silhouette.

## 5. Landmark strategy

Choose landmarks that are:
- Visually stable.
- Repeated across views.
- Easy to define unambiguously.
- Connected to structural proportions.
- Less affected by removable accessories.

Avoid using:
- Reflections.
- Shadows.
- Decals.
- Flexible parts.
- Perspective-distorted extrema without correction.

For a vehicle, useful landmarks may include:
- Front-most and rear-most body points.
- Front and rear axle centres.
- Wheelbase endpoints.
- Wheel outer diameters.
- Roof highest point.
- Windshield base and top.
- Beltline.
- Sill line.
- Wheel-arch apex.
- Wing leading/trailing edge.
- Overall ground clearance.

Do not assume a car is symmetric just because the front view appears symmetric. Verify with additional evidence where possible.

## 6. Proportion confidence

Use confidence based on evidence quality:

**High**
- Dimensioned technical drawing or calibrated orthographic view.
- Multiple compatible views support the same relationship.
- Landmarks are clear and unambiguous.

**Medium**
- One clear view, or multiple views with mild perspective/scale uncertainty.
- Relationship is visible but not calibrated.

**Low**
- Strong perspective, occlusion, crop, low resolution, uncertain variant, or ambiguous landmark.

Use ratio descriptions where absolute scale is unavailable:
- Wheelbase / overall length.
- Height / width.
- Cabin length / overall length.
- Opening width / parent panel width.

Always name the exact endpoints. Never present a ratio as exact if its endpoints are uncertain.

## 7. Component segmentation

Use a hierarchy:
- Assembly
  - Major component
    - Subcomponent
      - Detail

Example vehicle:
- Exterior body
  - Front body
    - Hood
    - Front bumper
    - Grille opening
    - Splitter
    - Headlamp housings
  - Side body
    - Front fender
    - Door skin
    - Side skirt
    - Rear quarter
  - Rear body
    - Rear bumper
    - Diffuser
    - Tail lamps
    - Wing assembly
      - Main plane
      - Endplates
      - Supports
- Running gear
  - Wheel
  - Tyre
  - Brake assembly
- Cabin
  - Glass
  - Dashboard
  - Seats
  - Roll structure

This is an evidence map, not a mandatory Blender object hierarchy. Some visible regions may be one continuous surface; some assemblies may be split into many objects.

## 8. Surface interpretation cues

### Silhouette
A reliable cue for the outer boundary in that view. It does not reveal the full surface between boundaries.

### Cross-section
Can be inferred when several views expose the same station or section. Do not invent section profiles from a single oblique view.

### Highlight flow
Can suggest broad curvature, but is highly dependent on lighting and material. Treat as supporting evidence only.

### Reflections
May reveal surface smoothness or broad shape changes, but can also create false edges. Never trace every reflection as a crease.

### Panel gaps
Can indicate separation, but may be painted, shadowed, decal-based, or artificially enhanced in renders.

### Occlusion boundaries
Show which object is in front, not necessarily how the hidden object continues.

## 9. Cross-view consistency checks

Use a stable set of checks:
- Do wheel centres align consistently with the side view?
- Does the roof peak occupy a compatible longitudinal position?
- Do front/rear extremities agree with overall length?
- Do top and front views support the same width distribution?
- Are left/right features genuinely symmetric?
- Are mirrors, intakes, vents, wing supports, and exhausts variant-specific?
- Are apparent component changes explained by camera angle or occlusion?
- Do dimensions and ratios use the same endpoints?

When a conflict remains, create a conflict record. Never quietly pick the most convenient image.

## 10. Hidden geometry decision tree

1. Is the region visible in another supplied view?
   - Yes: compare that view.
   - No: continue.
2. Is there a compatible reliable external reference and is research permitted?
   - Yes: research and cite it in the report.
   - No: continue.
3. Is the form strongly constrained by known interfaces, symmetry, or function?
   - Yes: mark as `INFERRED`, describe constraints, assign confidence.
   - No: mark `UNKNOWN`.
4. Does the unknown affect silhouette, fit, assembly, or intended camera?
   - Yes: mark `NEEDS_REFERENCE` or ask the user.
   - No: defer as low-priority unknown.

## 11. Common failure patterns

| Failure | Why it fails | Correct response |
|---|---|---|
| Treating a three-quarter image as a blueprint | Perspective distorts proportions | Use view-aware interpretation |
| Assuming all photos show the same variant | Body kits and revisions differ | Verify discriminators |
| Inventing the unseen underside | No supporting evidence | Mark unknown or research |
| Reading reflections as creases | Lighting creates false edges | Cross-check silhouette and other views |
| Treating every panel line as a separate mesh | Visual seam does not prove object separation | Record boundary evidence only |
| Reporting exact dimensions from pixels | No calibration | Use approximate ratios and confidence |
| Ignoring mirrored images | Left/right can reverse | Verify asymmetric landmarks |
| Overweighting logos | Brand identity is not variant identity | Use geometry and technical identifiers |
| Filling every missing view with AI imagination | Creates false certainty | Request evidence or label assumptions |
| Calling smooth shading proof of good topology | Shading can hide mesh defects | Defer topology QA to geometry skill |

## 12. Report quality scoring

Score the analysis, not the model:
- Reference inventory completeness: 0–5
- Subject/variant confidence: 0–5
- View coverage: 0–5
- Landmark/proportion traceability: 0–5
- Component relationship clarity: 0–5
- Hidden geometry honesty: 0–5
- Conflict handling: 0–5
- Handoff usefulness: 0–5

Maximum: 40.

Interpretation:
- 35–40: strong evidence package.
- 28–34: usable with disclosed limitations.
- 20–27: conditional; critical gaps likely.
- Below 20: weak evidence; do not claim reliable reconstruction readiness.

A high score cannot override a critical unresolved identity or proportion conflict.
