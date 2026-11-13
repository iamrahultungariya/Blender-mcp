# Pre-Production Research and Decision Playbook

Load this reference when performing Standard or Deep mode, researching a named subject, resolving conflicting references, or assessing feasibility/uncertainty.

## 5. Research policy: browse intelligently, not automatically

Research is allowed when search tools are available. It is not mandatory for every
asset. First decide whether current or subject-specific information could change
the design.

### 5.1 When research is strongly recommended

Research when the user names:
- A real vehicle, exact generation/trim, aircraft, train, ship or motorcycle.
- A specific building, architectural style, landmark or historical structure.
- A machine, industrial product, consumer device or technical instrument.
- A real weapon/tool, sports equipment or manufactured object.
- A historical period, culture-specific artifact or named design movement.
- A subject whose proportions, components or construction are unfamiliar.
- A product/asset whose current revision differs from earlier versions.

Also research when:
- The user explicitly asks for accuracy, authenticity or "real-world correct".
- Several references disagree.
- Critical hidden construction must be inferred.
- A named standard, format, API or technical requirement may have changed.
- A feasibility decision depends on current platform or software capabilities.

### 5.2 When research is optional or unnecessary

Usually do not browse for:
- An original fictional design with sufficient user direction.
- A simple generic primitive or common object.
- A stylized concept where factual fidelity is not required.
- Purely aesthetic ideation where research would constrain creativity.
- Details already clearly established by user-provided source material.

If research is skipped, state `Research: not required` and why. Do not imply that
the design is verified against real-world references.

### 5.3 Search workflow

When search is available:

1. Search the exact subject plus its exact variant/generation/year.
2. Search for official specifications, dimension drawings, manufacturer press
   kits, manuals, technical documents, museum/catalogue records or architect/
   manufacturer publications.
3. Search for orthographic views, technical drawings, exploded views and
   close-ups when visual references are needed.
4. Search specialist sources for construction details that official marketing
   pages omit.
5. Cross-check critical facts with a second independent source when practical.
6. Verify dates, model variants, units and regional differences.
7. Open the most useful sources; do not rely only on search snippets.
8. Record source title, publisher, URL, date/version if available, what it
   supports, and confidence.
9. Stop when the important decisions are sufficiently supported. Do not collect
   dozens of redundant images.

### 5.4 Source hierarchy

Prefer, in order:
1. Official manufacturer/developer/architect documentation.
2. Official manuals, specification sheets, press kits, technical drawings,
   standards or public institutional archives.
3. Museums, universities, government records and professional institutions.
4. Reputable technical publications and specialist reference databases.
5. Expert teardown/review/engineering analysis.
6. Community posts and forums as leads or corroboration, not sole support for
   critical dimensions.

Community sources can reveal useful practical details, but label anecdotal claims
and verify critical facts elsewhere.

### 5.5 Research integrity

For every important claim, mark one:
- `SOURCE-VERIFIED`: supported by a source actually opened or inspected.
- `USER-SUPPLIED`: directly stated or shown in supplied material.
- `CROSS-CHECKED`: supported by multiple independent sources.
- `INFERRED`: reasoned from available evidence but not directly stated.
- `ASSUMED`: selected because evidence is unavailable or unnecessary.
- `UNKNOWN`: unresolved.

Do not invent citations, URLs, publication dates, dimensions or source contents.
If a source is inaccessible, say so and do not claim to have inspected it.

When dimensions are reported:
- Preserve source units and convert carefully.
- Distinguish overall length/width/height from wheelbase, track, ground clearance,
  body-only dimensions and component dimensions.
- Record whether mirrors, spoilers, roof rails, attachments or protrusions are
  included.
- Do not use a specification from a different model year/trim without flagging it.

### 5.6 Search budget

Use a proportional research budget:
- **Quick:** one or two targeted searches for a low-risk named subject.
- **Standard:** several focused searches and source checks for a complex real
  subject or reference-led hero asset.
- **Deep:** broader research for historically/technically accurate assets,
  conflicting sources or high-consequence dimensions.

Stop researching when:
- Identity and variant are established.
- Critical dimensions/proportions have reliable support or explicit assumptions.
- Major design features are understood.
- Conflicts and unknowns are recorded.
- Additional searches are unlikely to change the plan.

---

## 6. Understand the subject before deciding how it should look

Create a concise **Subject Understanding** for the specified asset:

1. What is it?
2. What is its real-world purpose or fictional role?
3. What are its defining silhouette features?
4. What are its major functional systems or visual assemblies?
5. What are its characteristic proportions?
6. Which details make this variant recognizable?
7. What must be visible for the requested use?
8. What can be simplified without damaging identity?
9. What must not be invented?
10. What are the major unknowns?

For real manufactured objects, distinguish:
- External styling.
- Functional/structural parts.
- Serviceable or removable panels.
- Moving assemblies.
- Decorative details.
- Hidden structures.
- Presentation-only elements.

For architecture, distinguish:
- Building type and style.
- Structural system versus façade language.
- Massing and floor organization.
- Openings and circulation.
- Roof and foundation logic.
- Site/context elements.
- Historical authenticity versus contemporary interpretation.

For original fictional assets, define the design rules consistently rather than
pretending the object has a real manufacturer or established specifications.

---

## 7. Visual direction and design intent

Write a short design direction that can guide downstream modeling.

It must define:

- **Identity:** what makes this subject recognizable.
- **Silhouette:** the dominant large-scale shape.
- **Proportion language:** long/low, tall/compact, wide/narrow, heavy/light, etc.
- **Form language:** angular, faceted, compound-curved, organic, modular,
  machined, layered, soft or hybrid.
- **Detail language:** restrained, dense, exposed, integrated, rugged, precise.
- **Construction language:** monolithic shell, assembled panels, frame-and-skin,
  cast housing, layered façade, etc., only where supported or deliberately chosen.
- **Visual hierarchy:** hero forms, secondary forms and details.
- **Fidelity target:** exact reference match, evidence-based reconstruction,
  plausible interpretation or original concept.

Do not prescribe materials, thicknesses or internal construction as factual if
the evidence does not support them. You may propose them as design decisions.

---

## 8. Reference and evidence strategy

This skill sets the evidence strategy; `blender-artist-workflow` performs detailed
image inspection and builds the full Reference Evidence Matrix.

Define:
- Which views are available.
- Which views are missing.
- Which views are essential for this asset.
- Which features are obscured or cropped.
- Which source is authoritative when views disagree.
- Whether scale and camera perspective can be calibrated.
- Which close-ups or technical drawings would materially reduce uncertainty.

### 8.1 View coverage

For a complex object, consider the relevant set:
- Front and rear.
- Left and right.
- Top and bottom.
- Three-quarter perspective.
- Detail close-ups.
- Exploded/section views.
- Dimension drawings.
- Interior/underside/hidden structure views.

Do not demand every view for every asset. Select views according to the geometry
and intended deliverable.

### 8.2 Perspective caution

A perspective photograph is not an orthographic dimension drawing. Lens distortion,
camera angle, occlusion, lighting and reflections can alter apparent proportions.

Do not infer exact width/height ratios from a perspective image unless there is
a defensible calibration method. Use multiple landmarks and corroborating views.

### 8.3 Reference conflict

If two views conflict:
1. Confirm they depict the same variant and revision.
2. Check if one is mirrored, perspective, cropped or edited.
3. Check whether the feature changes between trims/years/configurations.
4. Prefer dimensioned/official sources for dimensions and the best-matched
   visual reference for styling.
5. Record unresolved conflict. Ask the user only if it changes the design.

---

## 9. Requirements, priorities and trade-offs

Sort requirements into:

- **Must-have:** explicit and essential.
- **Should-have:** important to fidelity or intended use.
- **Could-have:** optional detail.
- **Must-not:** prohibited elements or unwanted changes.

Assign priority:
- `P0`: identity, silhouette, dimensions, core constraints, critical exclusions.
- `P1`: major forms, primary components, functional/structural relationships.
- `P2`: secondary forms and visible construction details.
- `P3`: tertiary details and presentation polish.

Resolve conflicts in this order:
1. Safety and platform constraints.
2. Explicit user requirements and exclusions.
3. Subject identity and reference fidelity.
4. Intended use/performance constraints.
5. Structural plausibility.
6. Aesthetic preferences.
7. Optional decoration.

If two P0 requirements conflict, do not choose silently. Explain the conflict
and request a decision or propose clearly labeled alternatives.

---

## 10. Feasibility before modeling

Assess whether the brief can be built with the available evidence, tools and
constraints.

Evaluate:
- Is the subject sufficiently identified?
- Are critical views/dimensions available or inferable?
- Does the requested use fit the requested geometry/detail level?
- Is the triangle budget plausible for the silhouette and components?
- Are separate/moving parts feasible?
- Are hidden areas required but unsupported by references?
- Are required outputs supported by the connected environment?
- Are there conflicting constraints?
- Is external research needed before a reliable estimate?

Use one verdict:

- `FEASIBLE`: requirements are sufficiently clear and compatible.
- `FEASIBLE WITH TRADE-OFFS`: achievable if specified details or constraints
  are adjusted.
- `BLOCKED — CLARIFICATION`: a critical decision is missing.
- `BLOCKED — CAPABILITY`: required tool, reference or environment capability
  is unavailable.
- `NOT FEASIBLE AS SPECIFIED`: requirements conflict materially.

A feasibility verdict is a planning assessment, not proof of execution success.

### 10.1 Budget discipline

Do not invent a universal polygon target. A budget estimate must depend on:
- Intended platform and camera distance.
- Silhouette curvature.
- Component count and separation.
- Interior/underside visibility.
- Deformation and LOD needs.
- Modifier/evaluated geometry.
- Whether high-frequency details can be baked.

If no budget is supplied, ask downstream `blender-artist-workflow` to estimate
using its component-level budgeting rules. Do not duplicate or replace its
numerical budget process here.

### 10.2 Risk register

Record high-impact risks, likelihood, impact and mitigation. Examples:
- Missing underside references may force assumptions.
- Conflicting variants may produce wrong body proportions.
- Strict triangle budget may compromise wheel arches or silhouette.
- Unknown MCP capability may block a planned operation.
- Perspective-only references may not constrain exact dimensions.
- An exact real-world match may require licensed or inaccessible references.

---

## 11. Decision quality and anti-hallucination controls

Before approving the brief, run these checks:

### 11.1 Evidence audit

- Is every factual claim linked to user material or a source?
- Are exact dimensions actually sourced?
- Are model year, trim, revision and regional differences correct?
- Are hidden details labeled as inferred/unknown?
- Are reference images classified correctly?
- Are perspective images being mistaken for orthographic views?
- Are source conflicts visible in the brief?

### 11.2 Assumption audit

For each assumption:
- Why is it necessary?
- What evidence supports it?
- What is the confidence?
- What changes if it is wrong?
- Can it be deferred until a later stage?
- Does it require user approval?

Prefer reversible assumptions. Never let an assumption silently define a critical
silhouette or named model identity.

### 11.3 Feasibility audit

- Are the user's explicit constraints preserved?
- Are target use and quality compatible?
- Are requested views and hidden areas accounted for?
- Are unsupported tool requirements called out?
- Is any trade-off disclosed before work begins?

### 11.4 Stop conditions

Stop and ask or report BLOCKED when:
- The named subject has multiple materially different variants and the intended
  one cannot be determined.
- A required dimension or view changes the primary silhouette substantially.
- User constraints conflict and no priority rule resolves them.
- The user requests exact fidelity but only contradictory/insufficient evidence
  exists.
- Required capabilities are unavailable and no valid alternative preserves the
  acceptance criteria.

Do not stop for low-impact cosmetic unknowns. Record them and let downstream work
continue with a conservative assumption.

---


## 14. Worked example: a named GT racing car

User request: "Create a realistic [named GT racing car] from these images."

Correct pre-production behavior:

1. Confirm exact model, generation, race specification and year if the name covers
   multiple variants.
2. If identifiable, research official press material and technical/specification
   sources. Do not assume road-car bodywork matches the race version.
3. Determine whether the references show the same race season and aero package.
4. Establish intended use: game asset, close-up hero render, animation or preview.
5. Record available front/rear/side/top/three-quarter views and missing underside
   or interior evidence.
6. Identify signature identity features: roofline, greenhouse, wheelbase, track,
   overhangs, fender volume, bumper openings, wing and diffuser layout.
7. Distinguish sourced dimensions from ratios estimated from images.
8. Flag any hidden construction that cannot be seen.
9. Assess whether requested geometry budget and close-up quality are compatible.
10. Produce the PPB and hand it to `blender-artist-workflow`.

Incorrect behavior:
- Immediately create a generic sports-car mesh.
- Guess a specific GT variant from a vague name.
- Copy proportions from a perspective image as exact dimensions.
- Invent underside details and describe them as reference-accurate.
- Promise "production-ready" before geometry and output validation.
- Generate dozens of decorative parts before the silhouette is approved.

---

