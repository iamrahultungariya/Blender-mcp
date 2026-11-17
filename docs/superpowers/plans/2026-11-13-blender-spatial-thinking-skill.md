# Blender Universal Spatial Thinking & Modular Planning Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a production-grade universal spatial thinking, reference deconstruction, tool mapping, and modular planning skill (`blender-spatial-thinking-planner`) for Blender MCP agents, preventing boxy hallucinations, geometry misallocation (walls vs soft goods), tool ignorance, and monolithic script generation.

**Architecture:** The skill defines a 6-phase cognitive contract (Deconstruct -> Classify & Allocate Geo -> Map to Live MCP Tools -> Socratic Clarification -> Modular Plan Creation -> Gate Approval) backed by 3 technical reference playbooks (Spatial Deconstruction & Geometry Allocation, Tool Selection Matrix, and Modular Code Architecture) and a standardized execution plan template. All principles synthesized from the 9 core Blender tutorials (passes workflow, CAD precision, pre-boolean grids, shrinkwrap artifact fixes, cloth/cushion anatomy, curve tapering, and modular asset hygiene) are codified into testable rules.

**Tech Stack:** Python 3.11+, Blender 4.x/5.x BMesh API, FastMCP Blender Tools, Pytest, Markdown / Frontmatter.

**Spec:** [docs/superpowers/specs/2026-11-13-blender-spatial-thinking-skill-design.md](file:///c:/Users/Rahul/OneDrive/Desktop/Blender%20MCP/docs/superpowers/specs/2026-11-13-blender-spatial-thinking-skill-design.md)

## Global Constraints

- **90/10 Hybrid Pipeline**: In-memory `bmesh` Zone A operations (90%) with sub-second execution; `bpy.ops` Zone B (10%) restricted to final I/O.
- **Strict Anti-Monolithic Architecture**: Banned from generating single giant script files (>250 lines); assets must be partitioned into `core/materials.py`, `prefabs/<feature>_kit.py`, and `main.py`.
- **Soft Goods Geometry Mandate**: Soft items (pillows, cushions, bedspreads, clothing) must never be modeled as flat beveled boxes; must include crowned parabolic lofts, perimeter seam lines, and subdivision cages.
- **Planar Geometry Discipline**: Architectural walls and planar surfaces must not use dense subdiv grids or wasteful Geometry Nodes; must use clean quads with perimeter bevels or `create_architectural_wall`.
- **Tool Mapping Justification**: Every planned component in the pre-execution plan must explicitly cite its assigned MCP tool or BMesh technique and provide a technical justification.

## Review Focus

1. Pillow/Cushion represented as a flat cube with bevel instead of parabolic crown loft with seam lines.
2. Architectural wall receiving heavy subdivision or complex procedural nodes instead of clean quad extrusion.
3. Plan omitting tool justification or inventing non-existent MCP tool signatures.
4. Generated 3D modeling code dumped into a single monolithic script instead of modular prefabs/kits.
5. Boolean operations executed without pre-boolean grid cuts or without checking normal orientation (`Shift+N`).

---

### Task 1: Test Suite Scaffolding

**Files:**
- Create: `tests/test_spatial_thinking_planner_skill.py`

**Interfaces:**
- Consumes: Python `pytest`, `pathlib`, `yaml` / regex frontmatter parser.
- Produces: Test harness validating skill directory structure, frontmatter metadata, heuristic rules, and tool mappings.

- [ ] **Step 1: Write the failing test**

```python
import os
import re
from pathlib import Path
import pytest

SKILL_DIR = Path("skills/blender-spatial-thinking-planner")

def test_skill_directory_and_frontmatter():
    skill_file = SKILL_DIR / "SKILL.md"
    assert skill_file.exists(), "SKILL.md must exist in blender-spatial-thinking-planner"
    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---"), "SKILL.md must have YAML frontmatter"
    assert "name: blender-spatial-thinking-planner" in content
    assert "description:" in content

def test_playbook_references_exist():
    refs = [
        "references/spatial-deconstruction-and-geometry-allocation-playbook.md",
        "references/mcp-and-blender-tool-selection-matrix.md",
        "references/modular-code-architecture-playbook.md",
        "templates/spatial-execution-plan-template.md",
    ]
    for rel_path in refs:
        target = SKILL_DIR / rel_path
        assert target.exists(), f"Reference file {rel_path} must exist"

def test_spatial_thinking_rules_content():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    # Check 6 phases
    assert "Phase 1: Multi-Angle Reference & Domain Deconstruction" in content
    assert "Phase 2: Physical & Material Classification" in content
    assert "Phase 3: Geometry & Budget Allocation Matrix" in content
    assert "Phase 4: Live MCP & Native Tool Selection Matrix" in content
    assert "Phase 5: Socratic Clarification & Inquiry Gate" in content
    assert "Phase 6: Modular Code Architecture Mandate" in content
    # Check 9 video principles codified
    assert "Primary -> Secondary -> Tertiary" in content
    assert "Shrinkwrap" in content
    assert "create_cushioned_profile" in content
    assert "create_architectural_wall" in content
    assert "create_profile_sweep_molding" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_spatial_thinking_planner_skill.py -v`  
Expected: FAIL with "SKILL.md must exist in blender-spatial-thinking-planner"

- [ ] **Step 3: Create directory structure `skills/blender-spatial-thinking-planner/{references,templates}`**

Run: `mkdir -p skills/blender-spatial-thinking-planner/references skills/blender-spatial-thinking-planner/templates`

- [ ] **Step 4: Run test to verify it still fails on missing files**

Run: `pytest tests/test_spatial_thinking_planner_skill.py -v`  
Expected: FAIL with "SKILL.md must exist"

- [ ] **Step 5: Commit scaffolding**

```bash
git add tests/test_spatial_thinking_planner_skill.py
git commit -m "test: scaffold spatial thinking planner skill test suite"
```

---

### Task 2: Core Skill Contract (`SKILL.md`)

**Files:**
- Create: `skills/blender-spatial-thinking-planner/SKILL.md`

**Interfaces:**
- Consumes: Design specification at `docs/superpowers/specs/2026-11-13-blender-spatial-thinking-skill-design.md`.
- Produces: The primary agent contract governing how an AI thinks, questions, maps tools, and plans 3D assets before writing code.

- [ ] **Step 1: Write `skills/blender-spatial-thinking-planner/SKILL.md`**

Implement full markdown skill containing:
- Frontmatter with name, description, and trigger instructions.
- The 6 Cognitive Phases.
- Explicit rules banning boxy defaults, monolithic scripts, and geometry misallocation.
- Soft goods anatomy standard (parabolic loft, perimeter seams, pinched corners).
- Architectural envelope standard (flat quads, bevels, sweep moldings, no wasteful subdiv).
- Socratic clarification guidelines (asking targeted questions with options).
- Hard gate: No code generation without user approval of the modular execution plan.

- [ ] **Step 2: Run test to verify SKILL.md assertions**

Run: `pytest tests/test_spatial_thinking_planner_skill.py::test_skill_directory_and_frontmatter tests/test_spatial_thinking_planner_skill.py::test_spatial_thinking_rules_content -v`  
Expected: PASS

- [ ] **Step 3: Commit `SKILL.md`**

```bash
git add skills/blender-spatial-thinking-planner/SKILL.md
git commit -m "feat(skill): author blender-spatial-thinking-planner master contract"
```

---

### Task 3: Spatial Deconstruction & Geometry Allocation Playbook

**Files:**
- Create: `skills/blender-spatial-thinking-planner/references/spatial-deconstruction-and-geometry-allocation-playbook.md`

**Interfaces:**
- Consumes: Tutorial principles (Passes, Real-world scale, Soft goods anatomy, Precision CAD).
- Produces: Definitive guide for breaking down multi-angle references and assigning geometry budgets based on physics and material nature.

- [ ] **Step 1: Author `references/spatial-deconstruction-and-geometry-allocation-playbook.md`**

Contents must include:
- Multi-Angle Reference Fusion (reconciling Front, Side, Top datums).
- The 4 Physical Surface Classes:
  1. Envelope / Planar Architecture (walls, ceilings, slabs): minimal topology.
  2. Precision Hard CAD / Mechanical: uniform grid prep, clean quads, chamfers.
  3. Soft Goods / Pliable Cloth (pillows, cushions, blankets, curtains): mathematical crown formula $Z(u,v) = Z_0 + h_{crown}(1-u^2)(1-v^2)$, perimeter welts, corner pinches, tension creases.
  4. Slender Curved Tubes (cables, pipes, stylized hair): Bezier paths + bevel object + `Alt+S` taper.
- Primary, Secondary, Tertiary passes breakdown.
- Metric scale discipline (real-world units, `Ctrl+A` scale).

- [ ] **Step 2: Verify playbook structure and formatting**

Check links, KaTeX math formulas, and code snippets.

- [ ] **Step 3: Commit playbook**

```bash
git add skills/blender-spatial-thinking-planner/references/spatial-deconstruction-and-geometry-allocation-playbook.md
git commit -m "docs(playbook): add spatial deconstruction and geometry allocation guide"
```

---

### Task 4: MCP & Blender Tool Selection Matrix Playbook

**Files:**
- Create: `skills/blender-spatial-thinking-planner/references/mcp-and-blender-tool-selection-matrix.md`

**Interfaces:**
- Consumes: Live FastMCP tools from `blender_mcp` and native BMesh / modifier techniques.
- Produces: Exhaustive directory mapping asset features to specific tools with rationales.

- [ ] **Step 1: Author `references/mcp-and-blender-tool-selection-matrix.md`**

Contents must detail:
- Live FastMCP Tools:
  - `create_architectural_wall`: Wall spans with precise cutouts.
  - `create_profile_sweep_molding`: Baseboards, cornices, wainscoting.
  - `create_cushioned_profile`: Domed cushions, headboards, mattress lofts.
  - `setup_subdivision_cage`: Sub-D smoothing with crease protection.
  - `create_bezier_tube`: Cables, stylized hair, pipes.
  - `clas_loft_splines`: Aerodynamic surfaces and organic lofting.
  - `audit_mesh_topology`: Non-manifold and topology inspection.
  - `apply_uv_unwrap`: Automatic unwrapping and packing.
  - `export_game_asset`: Final GLTF/FBX export with budget enforcement.
- Native Techniques from the 9 Videos:
  - Pre-Boolean uniform grid cuts + quad repair (`LoopTools Circle`, `Bridge Edge Loops`).
  - Shrinkwrap modifier shading fix for curved corners with vertex groups.
  - Solidify with vertex groups for hollow objects (bottles, mugs, panels).
  - Linked duplicates (`Alt+D`) with random object info variation.
  - Nishita Sky + 3-Point Lighting + Gobos and Light Linking.

- [ ] **Step 2: Verify playbook content**

Check that every live tool matches existing signatures in `blender_mcp/server.py` and `blender_mcp/bmesh_toolkit.py`.

- [ ] **Step 3: Commit playbook**

```bash
git add skills/blender-spatial-thinking-planner/references/mcp-and-blender-tool-selection-matrix.md
git commit -m "docs(playbook): add MCP and blender tool selection matrix"
```

---

### Task 5: Modular Code Architecture Playbook & Execution Template

**Files:**
- Create: `skills/blender-spatial-thinking-planner/references/modular-code-architecture-playbook.md`
- Create: `skills/blender-spatial-thinking-planner/templates/spatial-execution-plan-template.md`

**Interfaces:**
- Consumes: 90/10 Hybrid Pipeline rules and modular prefab design.
- Produces: Concrete architectural blueprint banning monolithic scripts and providing the standardized plan template.

- [ ] **Step 1: Author `references/modular-code-architecture-playbook.md`**

Contents must include:
- Strict ban on monolithic files (>250 lines).
- Four-tier modular directory blueprint:
  - `core/materials.py`: Material node graphs, PBR definitions.
  - `core/mesh_utils.py`: BMesh matrix helpers, clean transform utilities.
  - `prefabs/<feature>_kit.py`: Component generators.
  - `main.py`: Scene coordinator, assembly, instancing (`Alt+D`), camera & lighting.
- Single-Buffer BMesh Merging rules.
- Fast mesh evaluation (`depsgraph` vs `bpy.ops.object.convert`).

- [ ] **Step 2: Author `templates/spatial-execution-plan-template.md`**

Standardized template containing:
- Asset Overview & Reference Evidence Matrix.
- Component Decomposition Table (Component, Class, Geometry Budget, Tool Choice, Justification).
- Socratic Clarifications / User Choices.
- File Decomposition Architecture.
- Phase-by-Phase Execution Checklist.

- [ ] **Step 3: Commit playbook and template**

```bash
git add skills/blender-spatial-thinking-planner/references/modular-code-architecture-playbook.md skills/blender-spatial-thinking-planner/templates/spatial-execution-plan-template.md
git commit -m "feat(template): add modular code architecture playbook and plan template"
```

---

### Task 6: Comprehensive Verification & Pytest Execution

**Files:**
- Modify: `tests/test_spatial_thinking_planner_skill.py` (add deep validation of all playbooks and template tokens)

**Interfaces:**
- Consumes: All authored files in `skills/blender-spatial-thinking-planner/`.
- Produces: 100% green test execution.

- [ ] **Step 1: Add comprehensive checks in `tests/test_spatial_thinking_planner_skill.py`**

Test that:
- All 4 references exist and are non-empty.
- All 9 tutorial principles are documented.
- Mathematical parabolic loft formula is present.
- Every live FastMCP tool is documented in the matrix.
- Modular file structure pattern is defined.

- [ ] **Step 2: Run pytest across the entire test suite**

Run: `pytest tests/test_spatial_thinking_planner_skill.py tests/test_spatial_thinking_universal.py tests/test_spatial_geometry_generators.py -v`  
Expected: All tests PASS.

- [ ] **Step 3: Commit final verification**

```bash
git add tests/test_spatial_thinking_planner_skill.py
git commit -m "test: verify spatial thinking planner skill suite end-to-end"
```
