# Reference-to-Asset Pipeline v2 Implementation Plan (Quality Over Quantity)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform Blender MCP from a raw script execution engine into an automated, quality-first 3D artist pipeline fully compliant with the Reference-to-Asset Pipeline v2 Contract—implementing automated mesh topology auditing, specular reflection highlight QA, reference evidence matrices, evaluated vs base triangle budgeting, and strict staged execution gates.

**Architecture:**
1. `src/blender_mcp/mesh_auditor.py` & `addon.py`: Implement non-manifold, normal-orientation, and topology defect auditor (`audit_mesh_topology`).
2. `src/blender_mcp/reference_analyzer.py`: Implement structured reference evidence matrix and multi-view landmark reconciliation (`reconcile_reference_datums`).
3. `addon.py` & `src/blender_mcp/bundled/addon.py`: Embed studio clay specular inspection passes (`inspect_specular_clay_pass`) and evaluated vs base triangle budgeting (`get_evaluated_budget_report`).
4. `src/blender_mcp/pipeline_gates.py`: Implement strict phase-gate validator and task execution tracker enforcing the 6-stage artist workflow.
5. `src/blender_mcp/server.py`: Expose high-level FastMCP tools for pipeline gates, topology audits, reflection inspection, and budget reports.

**Tech Stack:** Python 3.10+, Blender 5.2.2 LTS C-API (`bpy`, `bmesh`, `mathutils`, `gpu`), FastMCP, numpy, pytest.

**Spec:** `skills/blender-artist-workflow/SKILL.md` (MANDATORY EXECUTION CONTRACT — REFERENCE-TO-ASSET PIPELINE v2).

## Global Constraints

1. Quality Over Quantity: Spend geometry strictly on silhouette curvature, openings, and visible mechanics; never inflate polycount with useless flat subdivisions.
2. Dual Addon Sync: `addon.py` and `src/blender_mcp/bundled/addon.py` must remain 100% byte-for-byte identical and synchronized to `%APPDATA%\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py`.
3. 90/10 Hybrid Standard: 90% procedural execution via `bmesh` + `bpy.data` in memory; `bpy.ops` strictly restricted to I/O boundaries.
4. Mandatory Gate Evidence: No task or phase may be marked PASS without verified numerical/visual evidence from Blender/MCP inspection.
5. Non-Destructive Modifiers: Base meshes must remain clean, editable low-poly cages with modifiers (Subsurf, Bevel, WeightedNormal) handling evaluated fidelity.

## Review Focus

1. `audit_mesh_topology` detecting non-manifold edges, flipped normals, duplicate vertices, and self-intersections.
2. `inspect_specular_clay_pass` rendering broad specular reflection lines without altering existing scene materials.
3. `get_evaluated_budget_report` accurately distinguishing base mesh faces from modifier-evaluated triangles.
4. `reconcile_reference_datums` preventing contradictory proportions between front, side, and top orthographics.
5. All new tools passing 100% automated unit tests without network or external UI dependencies.

---

### Task 1: Real-Time Topology & Manifold Auditor (`audit_mesh_topology`)

**Files:**
- Create: `src/blender_mcp/mesh_auditor.py`
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Modify: `src/blender_mcp/server.py`
- Test: `tests/test_mesh_auditor.py`

**Interfaces:**
- Produces: `audit_mesh_topology(object_name, auto_repair=False) -> dict`
- Reports: `{ "object": str, "non_manifold_edges": int, "loose_verts": int, "flipped_normals": int, "interior_faces": int, "is_watertight": bool, "status": "PASS"|"FAIL" }`

- [x] **Step 1: Write failing test in `tests/test_mesh_auditor.py` testing non-manifold edge and normal detection**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `MeshAuditor` in `src/blender_mcp/mesh_auditor.py` and `addon.py`**
- [x] **Step 4: Expose tool `audit_mesh_topology` in `server.py` and dispatch in `addon.py`**
- [x] **Step 5: Run test to verify it passes**
- [x] **Step 6: Sync `addon.py` to `bundled/addon.py` and Blender Roaming directory**

---

### Task 2: Specular Clay & Reflection Highlight QA Tool (`inspect_specular_clay_pass`)

**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Modify: `src/blender_mcp/server.py`
- Test: `tests/test_specular_clay_inspection.py`

**Interfaces:**
- Produces: `inspect_specular_clay_pass(object_name=None, filepath=None, mode="STUDIO_CLAY") -> dict`
- Verifies: Temporarily overrides viewport with high-gloss neutral reflection shader, renders 4 orthographic quadrants, and safely restores original materials.

- [x] **Step 1: Write failing test in `tests/test_specular_clay_inspection.py`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `inspect_specular_clay_pass` in `addon.py` using non-destructive material slot override**
- [x] **Step 4: Expose tool `inspect_specular_clay_pass` in `server.py`**
- [x] **Step 5: Run test to verify it passes**
- [x] **Step 6: Sync `addon.py` to `bundled/addon.py` and Blender Roaming directory**

---

### Task 3: Evaluated vs Base Triangle Budget Reporter (`get_evaluated_budget_report`)

**Files:**
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Modify: `src/blender_mcp/server.py`
- Test: `tests/test_evaluated_budget.py`

**Interfaces:**
- Produces: `get_evaluated_budget_report(target_collection=None) -> dict`
- Reports: Component-by-component breakdown:
  `{ "components": [{ "name": str, "base_verts": int, "base_faces": int, "evaluated_tris": int, "modifiers": list }], "total_base_faces": int, "total_evaluated_tris": int }`

- [x] **Step 1: Write failing test in `tests/test_evaluated_budget.py`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `get_evaluated_budget_report` using `evaluated_depsgraph_get()` in `addon.py`**
- [x] **Step 4: Expose tool `get_evaluated_budget_report` in `server.py`**
- [x] **Step 5: Run test to verify it passes**
- [x] **Step 6: Sync `addon.py` to `bundled/addon.py` and Blender Roaming directory**

---

### Task 4: Reference Evidence Matrix & Datum Reconciler (`reference_analyzer.py`)

**Files:**
- Create: `src/blender_mcp/reference_analyzer.py`
- Modify: `src/blender_mcp/server.py`
- Test: `tests/test_reference_analyzer.py`

**Interfaces:**
- Produces: `reconcile_reference_datums(image_paths, archetype="VEHICLE") -> dict`
- Features: Cross-checks front width vs top width, side wheelbase vs wheel placement, builds `ReferenceEvidenceMatrix` with confidence levels (Observed, Inferred, Designed).

- [x] **Step 1: Write failing test in `tests/test_reference_analyzer.py`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `reconcile_reference_datums` in `src/blender_mcp/reference_analyzer.py`**
- [x] **Step 4: Expose tool `reconcile_reference_datums` in `server.py`**
- [x] **Step 5: Run test to verify it passes**

---

### Task 5: Phase-Gate & Execution Validator (`pipeline_gates.py`)

**Files:**
- Create: `src/blender_mcp/pipeline_gates.py`
- Modify: `src/blender_mcp/server.py`
- Test: `tests/test_pipeline_gates.py`

**Interfaces:**
- Produces: `validate_phase_gate(phase_id, gate_evidence) -> dict`
- Tracks: `NOT STARTED` -> `IN PROGRESS` -> `VERIFIED` -> `PASS` / `FAIL`. Prohibits advancing to detailing (Phase 4) if Primary Silhouette (Phase 3) is FAIL or UNVERIFIED.

- [x] **Step 1: Write failing test in `tests/test_pipeline_gates.py`**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement `PhaseGateManager` in `src/blender_mcp/pipeline_gates.py`**
- [x] **Step 4: Expose tool `validate_phase_gate` in `server.py`**
- [x] **Step 5: Run test to verify it passes**

---

### Task 6: Comprehensive Verification & Integration Test

**Files:**
- Test: `tests/test_full_artist_contract_v2.py`

- [x] **Step 1: Write end-to-end integration test validating the entire Reference-to-Asset Pipeline v2 contract**
- [x] **Step 2: Run full pytest suite across all test files (`uv run pytest`)**
- [x] **Step 3: Ensure 100% test pass rate with zero regressions**
