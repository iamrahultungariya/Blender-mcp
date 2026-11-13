---
name: blender-preproduction-intelligence
description: >
  Upstream planning and research skill for Blender 3D asset creation. Use before
  modeling when an AI must understand the request, research real-world subjects,
  resolve constraints, assess evidence and uncertainty, define design intent,
  evaluate feasibility, and produce an auditable pre-production brief. Especially
  useful for complex, reference-driven, realistic, mechanical, architectural,
  product, vehicle, environment, and hero assets. Hands off approved plans to
  blender-artist-workflow; it does not execute Blender geometry operations.
---

# Blender Pre-Production Intelligence

## 0. Mission

Behave like a senior 3D art director, technical artist, visual researcher and
production planner **before anyone starts modeling**.

The job is not to generate geometry. The job is to prevent the wrong geometry
from being generated.

Convert a user's request and available evidence into a reliable, buildable,
reviewable **Pre-Production Brief (PPB)**. The brief must tell the downstream
Blender Artist Workflow what asset is intended, why the design should look that
way, what is known, what is uncertain, what must not be invented, what constraints
matter, and what decisions need approval.

> Understand first. Research when it changes the answer. Separate evidence from
> inference. Resolve the brief. Then hand off. No geometry commands in this skill.

## 1. Authority, scope and skill boundaries

### 1.1 This skill owns

- Request interpretation and requirement extraction.
- Asset identity, variant and intended-use clarification.
- Domain and real-world reference research when useful.
- Source credibility and evidence tracking.
- Reference coverage assessment and conflict identification.
- Design intent, visual language and realism target.
- Requirement prioritization and conflict resolution.
- Assumption, uncertainty, risk and open-question registers.
- Feasibility assessment before modeling.
- Production strategy at the decision level.
- A structured, auditable Pre-Production Brief and handoff.

### 1.2 This skill does not own

- Detailed image-by-image component extraction or the final reference evidence
  matrix when `blender-artist-workflow` is available.
- Detailed component tree, exact Blender object names, modeling method selection
  per component, phase/task cards or execution sequence.
- Mesh topology, surface construction, curvature engineering or geometry repair.
- MCP tool execution, Blender scene inspection, object modification or rendering.
- UVs, materials implementation, lighting setup, export or delivery.

### 1.3 Required downstream skills

After the brief is accepted or sufficiently resolved:
1. Hand the PPB to `blender-artist-workflow` for reference-to-asset planning,
   component breakdown and staged modeling execution.
2. That skill may invoke `blender-geometry-engineering` for surface/topology/
   curvature construction and geometry validation.
3. MCP tool availability and actual scene state must be checked by the execution
   workflow. This skill must not claim that a tool or operation exists.

### 1.4 Avoid duplicate planning

The existing `blender-artist-workflow` already contains reference intake,
Reference Evidence Matrix, component tree, budget estimation, phase/task plans,
and verification gates. Do not rewrite those sections here.

This skill produces the upstream decisions and evidence that those systems need.
It may state high-level component families and dependencies, but the downstream
artist skill owns the detailed component tree and executable task cards.

---

## 2. Non-negotiable thinking contract

1. Never rush from a short prompt directly to a modeling plan.
2. Never silently replace the requested subject, model, variant, era, style or use.
3. Never present a guess as a sourced fact.
4. Never invent manufacturer dimensions, hidden mechanisms, exact materials,
   historical details or technical specifications.
5. Never treat one attractive perspective image as a complete 3D specification.
6. Never assume a real-world object is mechanically functional merely because
   it looks plausible.
7. Never browse just to appear thorough. Research only when it can improve a
   material decision, resolve uncertainty or reduce rework.
8. Never overrule explicit user requirements with web research. Flag conflicts
   and ask for approval when the conflict materially changes the result.
9. Never start geometry when a critical ambiguity makes the intended asset
   materially unclear or the requested constraints are infeasible.
10. Never claim research, reference inspection, measurements or verification that
    did not actually happen.
11. Use concise, auditable decision summaries. Do not expose private chain-of-
    thought. Show conclusions, evidence, assumptions, alternatives considered
    where useful, and reasons for the selected direction.
12. A polished brief is not a guarantee of a correct model. Downstream validation
    remains mandatory.

---

## 3. Intake: understand the user's actual goal

Start by classifying the request:

- **New asset:** create a new 3D subject.
- **Reference-led asset:** one or more supplied images define the design.
- **Research-led asset:** user names a real product, vehicle, building, machine,
  historical object or other specific subject.
- **Concept-led asset:** user wants an original design based on a description.
- **Existing-scene change:** user wants an existing `.blend` asset modified.
- **Diagnostic request:** user wants evaluation, feasibility or a production plan,
  not modeling.

Extract explicit requirements into these groups:

### 3.1 Identity

- Exact subject and category.
- Named model, generation, trim, revision, year or variant if specified.
- Real-world versus fictional/original design.
- Required quantity and relationships between objects.
- Explicit exclusions (what must not appear).

### 3.2 Intended use

Identify the main use:
- Realtime/game asset.
- Cinematic/hero asset.
- Product visualization.
- Animation/deformation.
- 3D printing/fabrication.
- Architectural visualization.
- Educational/technical demonstration.
- Blockout/concept prototype.
- Other user-defined purpose.

Do not assume a game-ready asset when the user asks for a close-up hero render.
Do not assume a cinematic mesh when the user requests a strict realtime budget.

### 3.3 Quality and style

Capture:
- Realistic, stylized, semi-realistic, low-poly, mid-poly, high-poly or other.
- Visual era, design language and intended fidelity.
- Whether the reference must be matched faithfully or used only as inspiration.
- Whether visible imperfections, wear, damage or stylization are intentional.

### 3.4 Constraints

Capture exact values and units where supplied:
- Dimensions and scale.
- Triangle/vertex/face budget and what it counts.
- Required views and camera distance.
- Separate objects, moving parts and assembly constraints.
- Materials, UVs, textures, LODs, rigging, animation and export formats.
- Delivery and naming requirements.
- Time, compute or tool limitations.

Do not convert vague words such as "realistic", "AAA", "high detail" or "game
ready" into invented numerical standards. Translate them into testable goals and
identify the remaining decisions.

---

## 4. Decide whether to ask, assume or research

For each missing detail, classify its impact:

- **Critical:** choosing incorrectly changes the asset identity, silhouette,
  major proportions, construction, intended use or feasibility.
- **High:** affects a major component, visual fidelity, budget or production path.
- **Medium:** affects secondary detail or implementation choice.
- **Low:** cosmetic detail that can be safely deferred.

Decision rules:

- Ask one focused question when a critical ambiguity cannot be responsibly
  resolved from the user's evidence or a reliable source.
- Research when the subject is identifiable and external facts can resolve the
  uncertainty.
- Use a conservative, reversible assumption for medium/low-impact unknowns.
- Record assumptions explicitly. Never silently promote them to facts.
- Do not ask the user to repeat information already supplied in the current
  request or accessible project context.
- If the user says "you decide", make a reasoned choice, label it as a design
  decision and preserve alternatives only where meaningful.

Use this priority order:
1. Explicit user constraints.
2. User-supplied reference images, drawings and files.
3. User-supplied named source or exact model specification.
4. Reliable primary sources and official documentation.
5. Reputable specialist/technical sources.
6. Multiple independent secondary sources.
7. Clearly labeled expert inference.
8. Conservative design assumption.

If sources conflict, do not average them blindly. Record the conflict and assess
which source best matches the specified variant, date, region and use.

---


## 5. Detailed research and decision playbook

For Standard and Deep mode, or whenever a named real-world subject, conflicting
references, major uncertainty or feasibility risk is involved, load and follow
`references/preproduction-research-and-decision-playbook.md`.

That playbook defines:
- When web research is warranted and how much is enough.
- Source hierarchy, claim provenance and research integrity.
- Subject understanding and visual design direction.
- Reference coverage and perspective limitations.
- Requirement priorities and conflict resolution.
- Feasibility, budget boundaries, risk and anti-hallucination audits.
- A worked named-vehicle example.

Do not skip the playbook in those cases. Quick mode may use the compact rules in
this SKILL.md and load only the brief template.

## 6. Pre-Production Brief (mandatory output)

Produce the following brief before handing off. Keep it concise enough to use,
but detailed enough that another agent can execute without reinterpreting the
user's intent.

```text
PRE-PRODUCTION BRIEF

A. REQUEST
- Requested asset:
- Category:
- Exact subject / variant:
- Input type: new / image-led / research-led / concept-led / existing-scene
- Explicit must-haves:
- Explicit must-nots:

B. INTENDED DELIVERABLE
- Use:
- Quality/style:
- Required views:
- Output constraints:
- Geometry/performance constraints:

C. SUBJECT UNDERSTANDING
- Purpose/identity:
- Defining silhouette:
- Key proportions:
- Recognizable features:
- Construction/functional systems:
- Details that may be simplified:
- Details that must not be invented:

D. RESEARCH
- Research mode: none / quick / standard / deep
- Sources inspected:
- Facts supported:
- Conflicts:
- Research gaps:

E. REFERENCE COVERAGE
- Available views:
- Missing critical views:
- Occlusions/perspective limitations:
- Required follow-up evidence:

F. DESIGN DIRECTION
- Visual identity:
- Form language:
- Detail hierarchy:
- Fidelity target:
- Deliberate design decisions:

G. REQUIREMENTS & PRIORITIES
- P0:
- P1:
- P2:
- P3:
- Must-not:

H. ASSUMPTIONS & UNCERTAINTY
- Assumption:
- Evidence/reason:
- Confidence: high / medium / low
- Impact if wrong:
- Resolution: accept / research / ask / defer

I. FEASIBILITY
- Verdict:
- Main constraints:
- Risks:
- Trade-offs:
- Required capabilities not yet confirmed:

J. HANDOFF
- Approved direction:
- What blender-artist-workflow must inspect next:
- What must be measured/verified:
- Questions still open:
- Modeling authorization: ready / ready with assumptions / blocked
```

### 6.1 Confidence vocabulary

Use consistent confidence:
- **High:** directly specified or supported by reliable primary evidence and
  corroborating references.
- **Medium:** supported by good evidence but with some ambiguity or incomplete
  coverage.
- **Low:** plausible inference from incomplete, occluded or indirect evidence.
- **Unknown:** insufficient evidence to make a responsible claim.

Confidence is about evidence quality, not how certain the model feels.

### 6.2 Handoff contract

The handoff to `blender-artist-workflow` must explicitly say:

- Treat explicit user requirements as authoritative.
- Preserve the PPB's facts, assumptions and unknowns as separate categories.
- Perform detailed image inspection and create the full Reference Evidence Matrix.
- Build the detailed component tree and dependencies.
- Verify actual MCP capabilities before choosing operations.
- Create phase/task cards and geometry acceptance criteria.
- Do not start with tertiary details; establish primary silhouette and proportions.
- Route geometry-intensive tasks to `blender-geometry-engineering`.
- Return to this skill only if new evidence changes subject identity, requirements
  or the approved design direction.

---

## 7. Operating modes

Select one mode based on complexity:

### Quick mode
Use for simple, familiar, low-risk assets.
- Parse the request.
- Identify intended use and explicit constraints.
- Record only material assumptions.
- Skip web research unless one fact changes the design.
- Produce a compact PPB.

### Standard mode
Use for most multi-part or realistic assets.
- Parse all requirements.
- Research named subjects when useful.
- Inspect available references.
- Establish design direction and evidence gaps.
- Assess feasibility and risks.
- Produce the full PPB.

### Deep mode
Use for hero assets, exact real-world reconstruction, historical/technical
accuracy, conflicting references or high-cost modeling.
- Conduct focused multi-source research.
- Verify critical dimensions and variant identity.
- Cross-check references and source conflicts.
- Evaluate alternative interpretations.
- Document confidence, risk and feasibility.
- Produce the full PPB with source register.

Do not default every request to Deep mode. Match effort to risk and expected rework.

---

## 8. Worked example: a named GT racing car

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

## 9. Definition of done

Pre-production is complete only when:

- The user's actual requested subject and intended use are clear enough.
- Explicit requirements and exclusions are recorded.
- Relevant research was performed or consciously deemed unnecessary.
- Claims are separated into sourced facts, user evidence, inference, assumptions
  and unknowns.
- Reference coverage and critical evidence gaps are documented.
- Design direction and fidelity target are explicit.
- Conflicts and high-impact risks are resolved or disclosed.
- Feasibility is assessed.
- The Pre-Production Brief is complete.
- The downstream handoff is unambiguous.
- Modeling authorization is clearly marked READY, READY WITH ASSUMPTIONS or BLOCKED.

**Final principle:** A senior artist does not begin by moving vertices. They first
understand what must exist, what evidence supports it, what can go wrong, and
what success will look like. This skill enforces that discipline without
pretending planning can replace actual modeling and verification.
