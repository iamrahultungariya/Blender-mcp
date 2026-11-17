# Universal Spatial & Architectural Intelligence Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform Blender MCP from an automotive/gaming-biased tool into a Universal Spatial & Architectural Intelligence Engine that forces AI models to produce rich, filleted, crowned, and architecturally accurate 3D geometry (villas, houses, rooms, furniture) while eliminating "lazy boxy collapse".

**Architecture:** Implement a domain-agnostic `SpatialThinkingEngine` in `src/blender_mcp/spatial_thinking.py` defining architectural and ergonomic proportions and curvature equations; expand `bmesh_toolkit.py`'s `get_component_tree()` to replace vehicle fallbacks with structured systems for Architecture, Interiors, and Furniture; add high-performance C-RAM procedural BMesh generators (`create_cushioned_profile`, `create_architectural_wall_with_openings`, `create_profile_sweep_molding`); wire them into FastMCP server tools and `addon.py`; and enforce the Zero Unfilleted Primitives Law in the Intelligence Triad skills.

**Tech Stack:** Python 3.10+, BMesh (`bpy.data`, `bmesh`), NumPy, FastMCP, Pytest.

**Spec:** [docs/superpowers/specs/2026-11-13-universal-spatial-intelligence-design.md](file:///c:/Users/Rahul/OneDrive/Desktop/Blender%20MCP/docs/superpowers/specs/2026-11-13-universal-spatial-intelligence-design.md)

## Global Constraints
- **90/10 Hybrid Pipeline Standard**: 90% procedural geometry execution must run in memory via `bmesh` (`bmesh.new()`, `bmesh.ops.*`, `bm.to_mesh()`) without UI context. `bpy.ops` strictly restricted to I/O boundaries.
- **Zero Unfilleted Primitives Law**: No raw, sharp-edged 90-degree boxes for furniture or architecture; upholstered items require parabolic crowned cushion lofts, walls require minimum 0.2m thickness with reveals, and corners require bevels/fillets.
- **Backwards Compatibility**: Retain 100% compatibility with `VehicleThinkingEngine` and pass all 26+ core engine tests and 14 Apex GT-R test suites without regressions.
- **FastMCP Protocol Integrity**: Every server tool must handle disconnected Blender gracefully and return JSON-formatted diagnostic output.

## Review Focus
1. Non-vehicle query fallback: `get_component_tree("HOUSE")` previously returned `"main_chassis"` and `"body_shell"`; must now return architectural systems (`structural_walls`, `roof_structure`, `fenestration`).
2. Flat sofa cushion collapse: Passing dimensions to cushion creation should never generate flat planar caps; must adhere to $Z(u,v) = Z_0 + \text{crown} \cdot (1 - u^2)(1 - v^2)$.
3. Paper-thin walls: Wall generation must produce watertight manifold geometry with interior/exterior leaves, lintels, and reveal jambs for window/door cavities.
4. Scale & datum consistency: Floor heights (2.8m - 3.5m), door frames (0.9m x 2.1m), and seat heights (0.42m - 0.46m) must strictly adhere to architectural & ergonomic standards.
5. Skill compliance verification: Automated tests must ensure the Zero Unfilleted Primitives Law is permanently codified in the Intelligence Triad markdown files.

---

### Task 1: Universal Spatial Thinking Engine (`spatial_thinking.py`)

**Files:**
- Create: `src/blender_mcp/spatial_thinking.py`
- Test: `tests/test_spatial_thinking_universal.py`

**Interfaces:**
- Consumes: `VehicleThinkingEngine.ARCHETYPES` from `src/blender_mcp/vehicle_thinking.py`
- Produces: `SpatialThinkingEngine` class with `classify_domain`, `get_dimensions`, `calculate_cushion_loft`, `get_ergonomic_clearances`, and `generate_spatial_blueprint`.

- [ ] **Step 1: Write the failing tests in `tests/test_spatial_thinking_universal.py`**

```python
import pytest
from blender_mcp.spatial_thinking import SpatialThinkingEngine

def test_classify_domain_heuristics():
    engine = SpatialThinkingEngine()
    assert engine.classify_domain("modern luxury villa with swimming pool") == "ARCHITECTURE"
    assert engine.classify_domain("scandinavian minimalist bedroom interior") == "INTERIOR_SPACES"
    assert engine.classify_domain("leather Chesterfield sofa 3 seater") == "FURNITURE_PRODUCT"
    assert engine.classify_domain("supercar GT-R aerodynamic chassis") == "VEHICLE"

def test_architectural_dimensions_and_datums():
    engine = SpatialThinkingEngine()
    villa = engine.get_dimensions("MODERN_VILLA")
    assert villa["exterior_wall_thickness"] >= 0.20
    assert villa["floor_to_floor"] >= 2.80
    assert villa["door_height"] == 2.10

def test_cushion_loft_parabolic_curvature():
    engine = SpatialThinkingEngine()
    crown = 0.05
    z0 = 0.45
    # Center (u=0, v=0) must reach maximum crown height
    assert pytest.approx(engine.calculate_cushion_loft(0.0, 0.0, crown, z0), abs=1e-4) == z0 + crown
    # Edges (u=1 or v=1) must drop to baseline z0
    assert pytest.approx(engine.calculate_cushion_loft(1.0, 0.0, crown, z0), abs=1e-4) == z0
    assert pytest.approx(engine.calculate_cushion_loft(0.0, 1.0, crown, z0), abs=1e-4) == z0

def test_spatial_blueprint_generation():
    engine = SpatialThinkingEngine()
    blueprint = engine.generate_spatial_blueprint("velvet lounge armchair")
    assert blueprint["domain"] == "FURNITURE_PRODUCT"
    assert "dimensions" in blueprint
    assert blueprint["anti_boxy_mandate"]["zero_unfilleted_primitives"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_thinking_universal.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'blender_mcp.spatial_thinking'`

- [ ] **Step 3: Implement `SpatialThinkingEngine` in `src/blender_mcp/spatial_thinking.py`**

Implement domain classification keywords, architectural/interior/furniture archetypes dictionary (`MODERN_VILLA`, `RESIDENTIAL_HOUSE`, `LIVING_ROOM`, `BEDROOM`, `KITCHEN`, `SOFA_3_SEATER`, `ARMCHAIR_LOUNGE`, `DINING_TABLE`, `DINING_CHAIR`), double-parabolic cushion loft formula $Z(u,v) = z0 + \text{crown} \cdot (1 - u^2)(1 - v^2)$, ergonomic clearance lookups, and `generate_spatial_blueprint` with anti-boxy directives.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_thinking_universal.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add src/blender_mcp/spatial_thinking.py tests/test_spatial_thinking_universal.py
git commit -m "feat(spatial): implement Universal SpatialThinkingEngine with anti-boxy heuristics"
```

---

### Task 2: Multi-Domain Component Tree Expansion in `bmesh_toolkit.py`

**Files:**
- Modify: `src/blender_mcp/bmesh_toolkit.py:752-795`
- Test: `tests/test_spatial_thinking_universal.py`

**Interfaces:**
- Consumes: Archetype string from caller (`ARCHITECTURE`, `INTERIOR_SPACES`, `FURNITURE_PRODUCT`, `VEHICLE`, or specific aliases)
- Produces: 4-level component tree dictionary with `archetype`, `domain`, and `systems` containing `strategy`, `components`, and `datums`.

- [ ] **Step 1: Write the failing tests in `tests/test_spatial_thinking_universal.py`**

```python
from blender_mcp.bmesh_toolkit import get_component_tree

def test_component_tree_architecture_domain():
    tree = get_component_tree("HOUSE")
    assert "structural_walls" in tree["systems"]
    assert "roof_structure" in tree["systems"]
    assert "fenestration" in tree["systems"]
    assert "main_chassis" not in tree["systems"].get("primary_structure", {}).get("components", [])

def test_component_tree_interior_domain():
    tree = get_component_tree("LIVING_ROOM")
    assert "room_envelope" in tree["systems"]
    assert "trim_carpentry" in tree["systems"]

def test_component_tree_furniture_domain():
    tree = get_component_tree("SOFA")
    assert "cushion_assemblies" in tree["systems"]
    assert "frame_and_chassis" in tree["systems"]

def test_component_tree_vehicle_domain_preserved():
    tree = get_component_tree("VEHICLE")
    assert "body_shell" in tree["systems"]
    assert "wheel_assembly" in tree["systems"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_thinking_universal.py -k "test_component_tree" -v`
Expected: FAIL on `test_component_tree_architecture_domain` (`"structural_walls"` not in `tree["systems"]`)

- [ ] **Step 3: Update `get_component_tree()` in `src/blender_mcp/bmesh_toolkit.py`**

Replace the fallback block with domain-aware branches for `ARCHITECTURE` (villas, houses, buildings, facades), `INTERIOR_SPACES` (living rooms, bedrooms, kitchens), and `FURNITURE_PRODUCT` (sofas, armchairs, chairs, tables, beds). Each domain must provide structured systems, procedural strategies (`subdivision_cage`, `boolean_bevel`, `bezier_curve`, `procedural_loft`), components, and dimensional datums.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_thinking_universal.py -v`
Expected: PASS (8 passed)

- [ ] **Step 5: Commit**

```bash
git add src/blender_mcp/bmesh_toolkit.py tests/test_spatial_thinking_universal.py
git commit -m "feat(bmesh_toolkit): expand get_component_tree for architecture, interiors, and furniture"
```

---

### Task 3: Procedural BMesh Anti-Boxy Geometry Generators

**Files:**
- Modify: `src/blender_mcp/bmesh_toolkit.py`
- Create: `tests/test_spatial_geometry_generators.py`

**Interfaces:**
- Consumes: BMesh module or mock data structures
- Produces:
  - `create_cushioned_profile(width, depth, thickness, crown_height, segments, bm)`
  - `create_architectural_wall_with_openings(length, height, thickness, openings, bm)`
  - `create_profile_sweep_molding(path_points, profile_type, height, depth, bm)`

- [ ] **Step 1: Write the failing tests in `tests/test_spatial_geometry_generators.py`**

```python
import pytest
from blender_mcp.bmesh_toolkit import (
    create_cushioned_profile,
    create_architectural_wall_with_openings,
    create_profile_sweep_molding,
)

def test_create_cushioned_profile_geometry():
    res = create_cushioned_profile(width=0.8, depth=0.8, thickness=0.15, crown_height=0.04, segments=8)
    assert res["status"] == "success"
    assert res["vert_count"] > 30
    assert res["is_crowned"] is True
    assert res["max_z"] > (0.15 / 2.0)  # Has vertical crown dome

def test_create_architectural_wall_with_window_opening():
    openings = [{"type": "window", "x": 1.5, "z": 0.9, "width": 1.2, "height": 1.4}]
    res = create_architectural_wall_with_openings(length=4.0, height=3.0, thickness=0.25, openings=openings)
    assert res["status"] == "success"
    assert res["thickness"] == 0.25
    assert len(res["openings"]) == 1
    assert res["vert_count"] >= 16

def test_create_profile_sweep_molding():
    path = [(0.0, 0.0, 0.0), (4.0, 0.0, 0.0), (4.0, 3.0, 0.0)]
    res = create_profile_sweep_molding(path_points=path, profile_type="BASEBOARD", height=0.12, depth=0.02)
    assert res["status"] == "success"
    assert res["segments"] >= 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_geometry_generators.py -v`
Expected: FAIL with `ImportError: cannot import name 'create_cushioned_profile' from 'blender_mcp.bmesh_toolkit'`

- [ ] **Step 3: Implement the three procedural BMesh generators in `src/blender_mcp/bmesh_toolkit.py`**

1. Implement `create_cushioned_profile`: creates a 2.5D lofted quad surface grid where vertex positions are displaced by the double-parabolic crown equation $Z(u,v)$, mirrored for top and bottom cushions, and stitched together along the perimeter with quad side faces. If `HAS_BPY` is False, construct and return an evaluated geometry description dict with vertex coordinates and quad face indices.
2. Implement `create_architectural_wall_with_openings`: creates a solid manifold wall with exterior and interior wall faces, joined at the boundaries, and subtracts opening volumes using quad subdivisions forming reveal jambs, lintels, and sills with specified wall thickness ($\ge 0.2\text{m}$).
3. Implement `create_profile_sweep_molding`: extrudes a profiled cross-section (baseboard with top roundover or crown molding cove) along consecutive 3D path points with mitered corner transitions.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_geometry_generators.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add src/blender_mcp/bmesh_toolkit.py tests/test_spatial_geometry_generators.py
git commit -m "feat(bmesh_toolkit): implement procedural cushioned profile, architectural wall, and molding sweep"
```

---

### Task 4: Codify Anti-Boxy Spatial Law in Intelligence Triad Skills

**Files:**
- Modify: `skills/blender-geometry-engineering/SKILL.md`
- Modify: `skills/blender-preproduction-intelligence/SKILL.md`
- Modify: `skills/blender-visual-reference-intelligence/SKILL.md`
- Modify: `tests/test_intelligence_triad_skills.py`

**Interfaces:**
- Consumes: Existing Phase gates G0-G6 and skill standards
- Produces: Codified Zero Unfilleted Primitives Law, Architectural/Interior/Furniture datums, and anti-boxy inspection rules across all 3 skills.

- [ ] **Step 1: Write the failing tests in `tests/test_intelligence_triad_skills.py`**

```python
def test_zero_unfilleted_primitives_law_codified():
    geom_skill = Path("skills/blender-geometry-engineering/SKILL.md").read_text(encoding="utf-8")
    assert "Zero Unfilleted Primitives Law" in geom_skill
    assert "ANTI-BOXY" in geom_skill or "Anti-Boxy" in geom_skill
    assert "0.20m" in geom_skill or "0.2m" in geom_skill  # Exterior wall minimum thickness
    assert "cushion" in geom_skill.lower()

def test_spatial_domains_in_preproduction_skill():
    preprod_skill = Path("skills/blender-preproduction-intelligence/SKILL.md").read_text(encoding="utf-8")
    assert "ARCHITECTURE" in preprod_skill
    assert "INTERIOR_SPACES" in preprod_skill
    assert "FURNITURE_PRODUCT" in preprod_skill
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\pytest.exe tests/test_intelligence_triad_skills.py -k "test_zero_unfilleted_primitives_law_codified" -v`
Expected: FAIL with `AssertionError: assert 'Zero Unfilleted Primitives Law' in geom_skill`

- [ ] **Step 3: Update the 3 Intelligence Triad skills**

1. In `skills/blender-geometry-engineering/SKILL.md`:
   - Under Gate G2, add **The Zero Unfilleted Primitives Law**: Reject any raw, sharp 90-degree boxes for architecture or furniture.
   - Prescribe mandatory edge fillets (2-4mm for wood/tables, 15-30mm for upholstered chairs), crowned cushion math ($Z(u,v)$), minimum 0.2m exterior wall thickness, and window reveals $\ge 0.15\text{m}$.
2. In `skills/blender-preproduction-intelligence/SKILL.md`:
   - Add the 4 Spatial Domains (`ARCHITECTURE`, `INTERIOR_SPACES`, `FURNITURE_PRODUCT`, `VEHICLE`) to Phase 1 Understand & Blueprinting.
   - Enforce architectural scale rules (ceiling height 2.8m-3.5m, door 0.9m x 2.1m) and ergonomic clearances.
3. In `skills/blender-visual-reference-intelligence/SKILL.md`:
   - Add architectural facade layering (ground plane $\to$ foundation $\to$ cavity walls $\to$ trim/moldings $\to$ roof overhang).
   - Add furniture contour analysis (silhouette puffiness, seam piping, leg taper).

- [ ] **Step 4: Run test to verify it passes**

Run: `.\.venv\Scripts\pytest.exe tests/test_intelligence_triad_skills.py -v`
Expected: PASS (all tests pass)

- [ ] **Step 5: Commit**

```bash
git add skills/ tests/test_intelligence_triad_skills.py
git commit -m "docs(skills): codify Zero Unfilleted Primitives Law and 4 spatial domains in Intelligence Triad"
```

---

### Task 5: FastMCP Server Integration & Regression Suite Verification

**Files:**
- Modify: `src/blender_mcp/server.py`
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: All tests in `tests/`

**Interfaces:**
- Consumes: `bmesh_toolkit` generators
- Produces: MCP tools `create_cushioned_profile`, `create_architectural_wall`, `create_profile_sweep_molding` and addon command dispatchers.

- [ ] **Step 1: Write integration tests in `tests/test_spatial_geometry_generators.py`**

```python
def test_spatial_thinking_engine_imports_in_server():
    import blender_mcp.server as srv
    assert hasattr(srv, "get_component_tree")
```

- [ ] **Step 2: Run test to verify status**

Run: `.\.venv\Scripts\pytest.exe tests/test_spatial_geometry_generators.py -v`
Expected: PASS/FAIL depending on imports

- [ ] **Step 3: Register tools in `server.py` and command handlers in `addon.py`**

Expose `@mcp.tool() create_cushioned_profile(...)`, `@mcp.tool() create_architectural_wall(...)`, and `@mcp.tool() create_profile_sweep_molding(...)` in `src/blender_mcp/server.py` with full docstrings, typed arguments, and JSON returns. Add matching dispatchers in `addon.py` and `src/blender_mcp/bundled/addon.py`.

- [ ] **Step 4: Run full test suite & update knowledge graph**

Run:
```bash
.\.venv\Scripts\pytest.exe tests/test_spatial_thinking_universal.py tests/test_spatial_geometry_generators.py tests/test_intelligence_triad_skills.py tests/test_vehicle_thinking.py tests/test_bmesh_toolkit.py tests/test_pipeline_gates_persistence_and_aliases.py tests/test_uv_export_hardening.py tests/test_dxr_clas.py -v
```
Expected: PASS (100% green across all target test files)
Run: `npx graphify update .` (or python graphify update)

- [ ] **Step 5: Commit**

```bash
git add src/blender_mcp/server.py addon.py src/blender_mcp/bundled/addon.py tests/
git commit -m "feat(server): expose spatial procedural generators as FastMCP tools and update addon dispatch"
```
