# Design Specification: Blender MCP Intelligence Triad Skills Integration

**Date**: 2026-11-13  
**Status**: Pending Review  
**Target Path**: `docs/superpowers/specs/2026-11-13-blender-intelligence-triad-skills-design.md`  

---

## 1. Intent & Purpose

With the completion of engine hardening (Blender 5.3+ auto-smooth modifier support, `apply_uv_unwrap` tool exposure, selection isolation, `.pipeline_state.json` persistence, and Iron Law 4 UV enforcement), the Blender MCP platform requires an intelligent, production-grade agent skill system.

To prevent low-poly boxy hallucinations, unverified geometric guesses, and unstructured modeling, every asset iteration will strictly follow the **3-Stage Intelligence Triad**:
- **Skill 01 — Pre-Production Intelligence** (*Understand · Research · Plan*): Decides *what* is being built, resolves real-world identity, analyzes constraints, and compiles the Pre-Production Brief (PPB).
- **Skill 02 — Visual Reference Intelligence** (*Observe · Analyse · Interpret*): Converts imagery/blueprints into a traceable Evidence Matrix, establishes datum planes, and classifies features into OBSERVED vs INFERRED.
- **Skill 03 — Geometry Engineering (v2)** (*Construct · Validate · Repair*): Enforces pure `bmesh` Zone A modeling, G0–G6 quality gates, watertight manifold auditing, Catmull-Rom lofting, UV unwrapping, and game export.

---

## 2. Goals & Non-Goals

### Goals
1. Install all 3 unpacked skills into `skills/` with complete reference playbooks and report templates:
   - `skills/blender-preproduction-intelligence/`
   - `skills/blender-visual-reference-intelligence/`
   - `skills/blender-geometry-engineering/` (upgraded from v1 to v2)
2. Synchronize all tool signatures, code examples, and gate criteria with latest engine upgrades:
   - `@mcp.tool() apply_uv_unwrap(target_object, angle_limit_deg, island_margin)`
   - `@mcp.tool() validate_phase_gate(phase_id="G0"..."G6", evidence=...)`
   - `@mcp.tool() export_game_asset(..., auto_uv=True, auto_decimate=True)`
   - Blender 5.3 & 5.3+ modern "Smooth by Angle" `NODES` modifier standard.
3. Validate that all markdown links, template paths, and test suites are consistent.

### Non-Goals
- Modifying the underlying Python server or addon logic (already completed in Tasks 1-6).
- Deleting existing foundational skills (`blender-computational-geometry`, `blender-dxr-kernel-architect`, `blender-artist-workflow`).

---

## 3. Directory Layout

```
skills/
├── blender-preproduction-intelligence/
│   ├── SKILL.md
│   ├── references/
│   │   ├── preproduction-research-and-decision-playbook.md
│   │   └── research-and-evidence-protocol.md
│   └── templates/
│       └── pre-production-brief.md
│
├── blender-visual-reference-intelligence/
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   │   └── visual-reference-analysis-playbook.md
│   └── templates/
│       └── visual-reference-analysis-report.md
│
├── blender-geometry-engineering/
│   ├── SKILL.md (v2 updated with live FastMCP tools & Blender 5.3+ rules)
│   ├── README.md
│   ├── references/
│   │   └── geometry-engineering-playbook.md
│   └── templates/
│       └── geometry-engineering-report.md
│
├── blender-artist-workflow/
│   └── SKILL.md (Master orchestrator referencing the Triad)
├── blender-computational-geometry/
│   └── SKILL.md (4 Iron Laws)
└── blender-dxr-kernel-architect/
    └── SKILL.md (C-RNA kernel reference)
```

---

## 4. Live Engine Tool Synchronization Matrix

| Skill | Subsystem / Section | Synchronized FastMCP Tool / Capability |
| :--- | :--- | :--- |
| **Skill 01 (Pre-Production)** | Component Strategy & Breakdown | `get_component_tree(archetype)` + evaluated triangle budget estimation |
| **Skill 02 (Visual Reference)** | Datum Reconciliation & Projection | `reconcile_reference_datums` + `gbuffer_quad_capture` + `gbuffer_project_uv` |
| **Skill 03 (Geometry Engineering)** | Gate Validation & Persistence | `validate_phase_gate(phase_id="G0"..."G6")` storing to `.pipeline_state.json` |
| **Skill 03 (Geometry Engineering)** | Surface Lofting & Smoothing | `clas_loft_splines(..., longitudinal_samples=4)` + Blender 5.3+ "Smooth by Angle" modifier |
| **Skill 03 (Geometry Engineering)** | Topology & Manifold QA | `audit_mesh_topology(target_object)` with `try/finally: bm.free()` safety |
| **Skill 03 (Geometry Engineering)** | Curvature & Cavity Shading | `pbr_compile_curvature_ao` (sub-millisecond NumPy `np.add.at` vectorization) |
| **Skill 03 (Geometry Engineering)** | UV Unwrapping & Packaging | `apply_uv_unwrap` + `export_game_asset(auto_uv=True, auto_decimate=True)` |

---

## 5. Verification Plan

1. Verify all files exist in their target directories with intact markdown syntax and frontmatter.
2. Run test suite:
   ```bash
   pytest tests/test_geometry_engineering_robustness.py tests/test_full_artist_contract_v2.py
   ```
3. Add a unit test verifying that all 3 skills are discoverable, possess valid YAML frontmatter, and mention the newly added engine tools.
