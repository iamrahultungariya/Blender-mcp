# Geometry Engineering Playbook

## Purpose
Operational companion for `blender-geometry-engineering`. It focuses on robust, repeatable geometry construction and verification while remaining agnostic to unverified MCP tool implementations.

## A. Geometry-first sequence
1. Read the approved pre-production brief.
2. Read the visual-reference evidence package.
3. Select geometry class and construction candidate.
4. Define coordinate frame, datums, dimensions and constraints.
5. Define component interfaces and intended boundary continuity.
6. Build primary form before secondary detail.
7. Inspect cross-sections and silhouettes.
8. Validate topology, normals, thickness and intersections.
9. Measure base and evaluated geometry cost.
10. Repair locally and rerun regression checks.
11. Record evidence and hand off.

Do not begin by adding bevels, vents, bolts, badges or material details.

## B. Robust surface construction
### B1. Section stations
Place stations at leading/trailing boundaries, extrema, inflection regions, interfaces, openings and design transitions. Prefer intentional placement over dense arbitrary stations.
### B2. Section correspondence
Match winding, start point, landmarks, point counts or explicit correspondence. Resample by arc length only when supported. Compare local frames, scale, twist and foldover.
### B3. Loft limitations
Piecewise linear interpolation can have tangent discontinuities at section boundaries. It is not automatically G1 and is not G2. Actual continuity depends on interpolation, parameterization, correspondence and boundary conditions.
### B4. Patch boundaries
Match boundary position first, tangent direction for G1 where required, and curvature behaviour for G2 where required. Preserve deliberate hard edges. Test evaluated surfaces, not only input curves/cages.

## C. Topology inspection
Inspect boundary loops, non-manifold edges/vertices, duplicate/internal faces, degenerate faces, zero-length edges, loose geometry, face winding, normals, self-intersections, overlapping shells, disconnected islands, long thin faces, subdivision pinching, pole placement and n-gon triangulation. Document expected open surfaces separately from defects.

## D. Vehicle-specific geometry checks
Only apply when the asset is a vehicle and references support the feature.
- **Body shell:** wheelbase/axle datums, overall envelope, roof/greenhouse profile, hood/fender/door/quarter/bumper interfaces, wheel arches and reflective surface flow.
- **Aerodynamics:** splitter thickness, side skirt alignment, diffuser floor/tunnels/fins, wing plane/endplates/supports and attachment geometry.
- **Wheels:** wheel/tyre concentricity, tyre profile, rim depth, brake placement, tyre-to-arch clearance.
- **Cabin:** glazing fit, dashboard/seat envelope, roll-cage tube continuity and joints.

## E. Polygon budget
Report vertices, edges, faces and triangulated triangles separately. Blender polygon count is not necessarily triangle count. Measure evaluated geometry after modifiers/instances when the target is an exported asset. If over budget, identify expensive components, protect silhouette/high-curvature regions, reduce hidden/low-impact geometry first, then rerun silhouette, normals, manifoldness and fit checks. The audited export function reportedly accepts `triangle_budget` without enforcing it; verify installed code or use an independent pre-export gate.

## F. Failure diagnosis
| Symptom | Likely causes | First diagnostic |
|---|---|---|
| Wavy highlight | Poor sections, poles, uneven spacing | Cross-sections and curvature display |
| Loft twist | Loop winding/start mismatch, frame rotation | Compare section landmarks |
| Flat spot | Linear interpolation, poor station placement | Tangent/curvature comparison |
| Cracked seam | Boundary mismatch | G0 gap measurement |
| Pinched corner | Pole/support-loop placement | Subdivision cage inspection |
| Boolean spikes | Coplanar cutter, slivers | Cut boundary and face areas |
| Bevel artifacts | Scale, width, clamp overlap | Evaluated bevel geometry |
| Shell inversion | Offset direction, tight concavity | Normals and local thickness |
| Floating part | Bad datum or transform | Interface distance and transform check |
| Good render, bad mesh | Shading hides defects | Wireframe, normals, topology and sections |

## G. Audit performance safeguards
The supplied audit reports a possible missing `bm.free()` and a Python per-vertex curvature loop. Confirm these against installed code. Until confirmed fixed, avoid unbounded repeated audits, benchmark representative mesh sizes, use targeted checks during edits, and record timings. Never claim a performance bound from a small test mesh.

## H. Acceptance checklist
- [ ] Correct object and component scope.
- [ ] Coordinate frame, units and datums recorded.
- [ ] Dimensions and key landmarks measured.
- [ ] Profiles and sections correspond correctly.
- [ ] Silhouette checked in required views.
- [ ] G0/G1/G2 requirements classified per boundary.
- [ ] Continuity claims supported by actual checks.
- [ ] Topology defects checked and classified.
- [ ] Normals and evaluated modifiers inspected.
- [ ] Thickness and open boundaries understood.
- [ ] Intersections, gaps and clearances checked.
- [ ] Base and evaluated triangle counts recorded.
- [ ] No unrelated scene objects changed.
- [ ] Regression checks rerun after repair.
- [ ] Unverified checks clearly disclosed.
