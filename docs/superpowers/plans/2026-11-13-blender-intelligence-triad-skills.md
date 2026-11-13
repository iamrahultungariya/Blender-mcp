# Blender MCP Intelligence Triad Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install and synchronize the 3-Stage Intelligence Triad skills (Pre-Production, Visual Reference, and Geometry Engineering v2) into the project with complete playbooks and templates, aligned with latest Blender 5.3+ and FastMCP tools.

**Status:** Completed  
**Execution Mode:** Native Inline Execution (superpowers:executing-plans)  
**Verification:** 29/29 tests passed (100% green).  

**Architecture:** The skills are organized into `skills/blender-preproduction-intelligence/`, `skills/blender-visual-reference-intelligence/`, and `skills/blender-geometry-engineering/`. Each directory contains a primary `SKILL.md`, supporting playbooks in `references/`, and standardized deliverables in `templates/`. Skill 03 is updated with live FastMCP signatures (`apply_uv_unwrap`, `validate_phase_gate` G0-G6 aliases, `.pipeline_state.json` persistence, Blender 5.3+ "Smooth by Angle" modifier, and Iron Law 4 UV export checks).

**Tech Stack:** Markdown, YAML frontmatter, Python 3.11, pytest, Blender 5.3+ Python API / FastMCP.

**Spec:** `docs/superpowers/specs/2026-11-13-blender-intelligence-triad-skills-design.md`

## Global Constraints

- Every skill directory MUST have a root `SKILL.md` with valid YAML frontmatter (`name`, `description`).
- Skill references must accurately reflect the live FastMCP server tools in `src/blender_mcp/server.py`.
- Blender 5.3+ normal rules must mandate the "Smooth by Angle" `NODES` modifier over deprecated `use_auto_smooth`.
- Existing core tests (26 tests) must remain 100% green without regressions.

## Review Focus

- Missing tool references: ensure `apply_uv_unwrap` and `auto_uv` are explicitly documented in Skill 03.
- Broken template paths: ensure relative paths to `references/` and `templates/` exist and match filesystem.
- Dual-gate clarity: ensure G0-G6 gate descriptions clarify that strings `"G0"` through `"G6"` can be passed directly to `validate_phase_gate()`.
- Backward compatibility: ensure `tests/test_geometry_engineering_robustness.py` continues to pass with v2 skill.

---

### Task 1: Install & Synchronize Skill 01 — Pre-Production Intelligence

**Files:**
- Create: `skills/blender-preproduction-intelligence/SKILL.md`
- Create: `skills/blender-preproduction-intelligence/references/preproduction-research-and-decision-playbook.md`
- Create: `skills/blender-preproduction-intelligence/references/research-and-evidence-protocol.md`
- Create: `skills/blender-preproduction-intelligence/templates/pre-production-brief.md`
- Test: `tests/test_intelligence_triad_skills.py`

**Interfaces:**
- Consumes: Pre-production brief schema from unpacked scratch bundle
- Produces: `blender-preproduction-intelligence` skill discoverable by agent harness

- [x] **Step 1: Write the failing test**
Create `tests/test_intelligence_triad_skills.py` asserting `skills/blender-preproduction-intelligence/SKILL.md` exists and contains valid frontmatter.
- [x] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_intelligence_triad_skills.py::test_preproduction_intelligence_skill_exists -v`
Expected: FAIL (file not found).
- [x] **Step 3: Copy and synchronize Skill 01 files**
Copy `scratch/skills_unpacked/skill1/blender-preproduction-intelligence/` into `skills/blender-preproduction-intelligence/`.
- [x] **Step 4: Run test to verify it passes**
Run: `pytest tests/test_intelligence_triad_skills.py::test_preproduction_intelligence_skill_exists -v`
Expected: PASS.
- [x] **Step 5: Commit**
`git add skills/blender-preproduction-intelligence tests/test_intelligence_triad_skills.py`
`git commit -m "feat(skills): install Skill 01 blender-preproduction-intelligence"`

---

### Task 2: Install & Synchronize Skill 02 — Visual Reference Intelligence

**Files:**
- Create: `skills/blender-visual-reference-intelligence/SKILL.md`
- Create: `skills/blender-visual-reference-intelligence/README.md`
- Create: `skills/blender-visual-reference-intelligence/references/visual-reference-analysis-playbook.md`
- Create: `skills/blender-visual-reference-intelligence/templates/visual-reference-analysis-report.md`
- Test: `tests/test_intelligence_triad_skills.py`

**Interfaces:**
- Consumes: Evidence matrix schema and visual reference analysis playbook
- Produces: `blender-visual-reference-intelligence` skill discoverable by agent harness

- [x] **Step 1: Write the failing test**
Add `test_visual_reference_intelligence_skill_exists` to `tests/test_intelligence_triad_skills.py`.
- [x] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_intelligence_triad_skills.py::test_visual_reference_intelligence_skill_exists -v`
Expected: FAIL.
- [x] **Step 3: Copy and synchronize Skill 02 files**
Copy `scratch/skills_unpacked/skill2/blender-visual-reference-intelligence/` into `skills/blender-visual-reference-intelligence/`.
- [x] **Step 4: Run test to verify it passes**
Run: `pytest tests/test_intelligence_triad_skills.py::test_visual_reference_intelligence_skill_exists -v`
Expected: PASS.
- [x] **Step 5: Commit**
`git add skills/blender-visual-reference-intelligence tests/test_intelligence_triad_skills.py`
`git commit -m "feat(skills): install Skill 02 blender-visual-reference-intelligence"`

---

### Task 3: Upgrade & Synchronize Skill 03 — Geometry Engineering v2

**Files:**
- Modify: `skills/blender-geometry-engineering/SKILL.md`
- Create: `skills/blender-geometry-engineering/README.md`
- Create: `skills/blender-geometry-engineering/references/geometry-engineering-playbook.md`
- Create: `skills/blender-geometry-engineering/templates/geometry-engineering-report.md`
- Test: `tests/test_intelligence_triad_skills.py`

**Interfaces:**
- Consumes: `apply_uv_unwrap`, `validate_phase_gate`, `export_game_asset` signatures from `server.py`
- Produces: Updated `blender-geometry-engineering` v2 skill with live FastMCP tool documentation and Blender 5.3+ rules

- [x] **Step 1: Write the failing test**
Add `test_geometry_engineering_v2_and_mcp_sync` to `tests/test_intelligence_triad_skills.py` asserting that `SKILL.md` contains v2 features, `apply_uv_unwrap`, and Blender 5.3+ modifier rules.
- [x] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_intelligence_triad_skills.py::test_geometry_engineering_v2_and_mcp_sync -v`
Expected: FAIL.
- [x] **Step 3: Install v2 and synchronize engine tools**
Copy v2 files from `scratch/skills_unpacked/skill3/blender-geometry-engineering-v2/` into `skills/blender-geometry-engineering/`. Update `SKILL.md` to document the new `apply_uv_unwrap` tool, G0-G6 string alias validation, and Blender 5.3+ "Smooth by Angle" modifier standard.
- [x] **Step 4: Run test to verify it passes**
Run: `pytest tests/test_intelligence_triad_skills.py::test_geometry_engineering_v2_and_mcp_sync -v`
Expected: PASS.
- [x] **Step 5: Commit**
`git add skills/blender-geometry-engineering tests/test_intelligence_triad_skills.py`
`git commit -m "feat(skills): upgrade Skill 03 blender-geometry-engineering to v2 with live MCP tool sync"`

---

### Task 4: Complete Triad Suite Verification & Regression Check

**Files:**
- Test: `tests/test_intelligence_triad_skills.py`
- Test: `tests/test_geometry_engineering_robustness.py`
- Test: `tests/test_full_artist_contract_v2.py`
- Test: `tests/test_uv_export_hardening.py`
- Test: `tests/test_pipeline_gates_persistence_and_aliases.py`

- [x] **Step 1: Run comprehensive test suite**
Run: `pytest tests/test_intelligence_triad_skills.py tests/test_geometry_engineering_robustness.py tests/test_full_artist_contract_v2.py tests/test_uv_export_hardening.py tests/test_pipeline_gates_persistence_and_aliases.py -v`
Expected: All tests PASS (100% green).
- [x] **Step 2: Update progress ledger and finalize**
Update `.superpowers/sdd/2026-11-13-blender-intelligence-triad-skills/progress.md` with Triad skills installation record.
- [x] **Step 3: Final Commit**
`git commit -m "chore(skills): finalize intelligence triad skills integration and verification"`
