# Phase V3.1 & V3.2: Soft Goods & Furniture Engineering Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Phase V3.1 (Soft Goods & Existing Tools Overhaul) and Phase V3.2 (Furniture & Architectural Detail Engine) in Rahul 3D Engine, providing high-level semantic generators, cloth pressure puffing, AAA hard-surface edge conditioning (bevel weights + weighted normals), and modular component hierarchies inspired by the 6 Blender modeling masterclasses.

**Architecture:**
- **Zone A (90% execution)**: In-memory C RAM BMesh procedural generators for pillows, curtains, duvets, blankets, tufted surfaces, beds, sofas, chairs, tables, wardrobes, and doors with clean quad flow and semantic parented hierarchies.
- **Zone B (10% execution)**: Non-modal headless Blender physics simulation hooks (cloth pressure puffing, shape key pleating, collision drape) and modifier automation (weighted normal + bevel).
- **MCP & Addon Layer**: FastMCP tool registrations in `server.py`, command routing in `addon.py` (keeping byte-identical parity with `src/blender_mcp/bundled/addon.py`), and pure-Python testability in standard environments without live bpy.

**Tech Stack:** Python 3.11, Blender 3.0-5.2 bpy/bmesh, FastMCP, Pytest.

**Spec / Master Directive Reference:** Rahul 3D Engine Master Engineering Directive (Sections 1.1–1.5, 90/10 Hybrid Pipeline Standard, and 6 Video Masterclass Analyses).

## Global Constraints
- Preserve TCP Port 9876 and Protocol Version 15 for Blender communication.
- Every new engine module must be importable and testable without live `bpy` (using `HAS_BPY` fallback pattern).
- Keep `addon.py` and `src/blender_mcp/bundled/addon.py` exactly byte-identical (identical SHA256).
- Follow the 90/10 Hybrid Standard: Procedural geometry built in BMesh memory; no `bpy.ops` in tight loops.
- Semantic Assemblies: Complex furniture must be parented hierarchies of distinct parts, never single monolithic merged blobs.

## Review Focus
1. `setup_cloth_physics` backwards compatibility: callers omitting `pressure` or `gravity_scale` must get identical default behavior.
2. Non-bpy environments: all newly added tools must return structured mock responses with `success=True` when running in test suites without Blender.
3. Addon protocol parity: every newly registered FastMCP tool in `server.py` must have an exact matching handler in `addon.py`.
4. Topology quality: all parametric soft-goods and furniture components must generate manifold quad-dominant meshes without degenerate faces or loose vertices.
5. Auto-smooth and normals: edge conditioning must handle Blender 4.x/5.x normal modifier standards (`keep_sharp=True`).

---

### Task 1: Overhaul Existing Tools (Cloth Pressure, Translucent Foliage & Velvet Presets, Cushioned Profile Upgrade)

**Files:**
- Modify: `src/blender_mcp/cloth_engine.py`
- Modify: `src/blender_mcp/material_engine.py`
- Modify: `src/blender_mcp/bmesh_toolkit.py`
- Test: `tests/test_v3_1_existing_tools_overhaul.py`

- [x] Step 1: Write failing unit test in `tests/test_v3_1_existing_tools_overhaul.py` verifying new parameters (`pressure`, `gravity_scale`, `shrink_factor`) in `setup_cloth_physics`, new shader presets (`"translucent_foliage"`, `"velvet_fabric"`) in `create_procedural_shader`, and enhanced options (`pinch_corners`, `welt_depth`, `tufting_grid`) in `create_cushioned_profile`.
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `pressure`, `pressure_factor`, `gravity_scale`, and `shrink_factor` in `src/blender_mcp/cloth_engine.py`.
- [x] Step 4: Implement `"translucent_foliage"` and `"velvet_fabric"` presets in `src/blender_mcp/material_engine.py`.
- [x] Step 5: Implement `pinch_corners`, `welt_depth`, and `tufting_grid` in `create_cushioned_profile` in `src/blender_mcp/bmesh_toolkit.py`.
- [x] Step 6: Run tests and ensure all pass.

---

### Task 2: Implement AAA Edge Conditioning Engine

**Files:**
- Modify: `src/blender_mcp/modifier_engine.py`
- Test: `tests/test_v3_1_edge_conditioning.py`

- [x] Step 1: Write failing unit test in `tests/test_v3_1_edge_conditioning.py` for `apply_edge_conditioning(object_name, mode, angle_threshold, bevel_weight, crease_weight, add_weighted_normal, keep_sharp)`.
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `apply_edge_conditioning` in `src/blender_mcp/modifier_engine.py` supporting both headless non-bpy fallback and live BMesh edge marking with Bevel + Weighted Normal modifier pairing.
- [x] Step 4: Run test and verify pass.

---

### Task 3: Implement Soft Goods Engine (`src/blender_mcp/soft_goods_engine.py`)

**Files:**
- Create: `src/blender_mcp/soft_goods_engine.py`
- Test: `tests/test_v3_1_soft_goods.py`

- [x] Step 1: Write failing unit tests in `tests/test_v3_1_soft_goods.py` covering:
  - `create_pillow` (shapes: `"classic"`, `"diamond"`, `"bolster"`, `"square"`)
  - `create_curtains` (pleated drapery with bunching)
  - `create_duvet` (baffle-box quilted bedding)
  - `create_blanket` (folded/draped throw blanket)
  - `create_tufted_surface` (chesterfield diamond tufting)
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `src/blender_mcp/soft_goods_engine.py` with pure BMesh math generation for all 5 tools, plus optional non-modal cloth pressure inflation when `use_physics=True`.
- [x] Step 4: Run tests and verify all pass.

---

### Task 4: FastMCP Registration & Addon Sync for V3.1 Soft Goods

**Files:**
- Modify: `src/blender_mcp/server.py`
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_v3_1_server_registration.py`

- [x] Step 1: Register `create_pillow`, `create_curtains`, `create_duvet`, `create_blanket`, `create_tufted_surface`, and `apply_edge_conditioning` in `src/blender_mcp/server.py`.
- [x] Step 2: Update `setup_cloth_physics` FastMCP tool signature with `pressure`, `pressure_factor`, and `gravity_scale`.
- [x] Step 3: Add dispatch handlers in `addon.py` for the new tools.
- [x] Step 4: Mirror all changes to `src/blender_mcp/bundled/addon.py` ensuring exact SHA256 match.
- [x] Step 5: Write and run `tests/test_v3_1_server_registration.py` to verify all tool schemas and addon handlers.

---

### Task 5: Implement Furniture & Architectural Detail Engine (`src/blender_mcp/furniture_engine.py`)

**Files:**
- Create: `src/blender_mcp/furniture_engine.py`
- Test: `tests/test_v3_2_furniture.py`

- [x] Step 1: Write failing unit tests in `tests/test_v3_2_furniture.py` covering:
  - `create_bed` (hierarchy with Frame, Headboard, Mattress, Pillows, Duvet, Legs)
  - `create_sofa` (hierarchy with Base Frame, Backrest, Armrests, Seat/Back Cushions, Legs)
  - `create_chair` (hierarchy with Seat, Backrest, Legs)
  - `create_table` (hierarchy with Tabletop, Apron, Legs)
  - `create_wardrobe` (hierarchy with Carcass, Doors, Drawers, Handles)
  - `create_door_assembly` (hierarchy with Jamb, Architrave Molding, Door Leaf, Hardware)
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `src/blender_mcp/furniture_engine.py` adhering to the 4-Pillar AAA workflow (modular blockout, quad topology, edge conditioning, semantic parented hierarchy).
- [x] Step 4: Run tests and verify all pass.

---

### Task 6: FastMCP Registration & Addon Sync for V3.2 Furniture

**Files:**
- Modify: `src/blender_mcp/server.py`
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_v3_2_server_registration.py`

- [x] Step 1: Register `create_bed`, `create_sofa`, `create_chair`, `create_table`, `create_wardrobe`, and `create_door_assembly` in `src/blender_mcp/server.py`.
- [x] Step 2: Add dispatch handlers in `addon.py` for all 6 furniture tools.
- [x] Step 3: Mirror changes to `src/blender_mcp/bundled/addon.py` (verifying exact SHA256 parity).
- [x] Step 4: Sync `addon.py` to Blender 5.2 user addons folder (`C:\Users\Rahul\AppData\Roaming\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py`).
- [x] Step 5: Write and run `tests/test_v3_2_server_registration.py`.

---

### Task 7: Full Regression Verification, Documentation & Knowledge Graph Update

**Files:**
- Modify: `docs/production_capability_audit.md`
- Modify: `README.md`
- Graph: `graphify-out/`

- [x] Step 1: Execute all test suites (`test_phase*.py`, `test_v3_*.py`) to confirm zero regressions.
- [x] Step 2: Update `docs/production_capability_audit.md` with complete Phase V3.1 and V3.2 capabilities, tools, and technical benchmarks.
- [x] Step 3: Update `README.md` tool catalog reflecting all new soft goods and furniture tools.
- [x] Step 4: Run `graphify update .` to update the codebase knowledge graph.
