# Phase V3.3 & Phase V4: Nature & Organic Environment Engine, Pure Simulation Pipeline, and Layered Thinking Critic

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Phase V3.3 (Nature & Organic Environment Engine with Geometry Nodes scattering and translucent foliage), the Pure Physical Simulation Pipeline (multi-cloth assembly settling and collision draping), and Phase V4 (Layered Thinking Architecture, Intent Decomposition, and Independent Critic Gate) in Rahul 3D Engine.

**Architecture:**
- **Pure Simulation Mode & Assembly Physics**: Cross-cutting support across soft goods for `"pure_simulation"` alongside `"hybrid"` and `"parametric"`. Multi-object cloth settling tool (`simulate_cloth_assembly`) that assigns collision boundaries to furniture and bakes real draping.
- **Nature Engine (Zone A/B)**: Procedural grass blade cluster modeling in BMesh with natural curve/twist and dead stalk variations, coupled with procedural Geometry Nodes scattering (`create_grass_field`, `scatter_foliage`) with Musgrave patchiness masks and slope cutoffs.
- **Layered Thinking & Independent Critic**: Intent decomposition tool (`decompose_scene_intent`) generating ordered execution DAGs with simulation mode decisions, and the Independent Critic gate (`validate_aesthetic_quality`, `audit_production_readiness`) auditing topology, edge conditioning, materials, and lighting.
- **MCP & Addon Layer**: FastMCP tool registrations in `server.py`, command routing in `addon.py` (keeping byte-identical parity with `src/blender_mcp/bundled/addon.py`), and pure-Python testability in standard environments without live bpy.

**Tech Stack:** Python 3.11, Blender 3.0-5.2 bpy/bmesh/Geometry Nodes, FastMCP, Pytest.

**Spec / Master Directive Reference:** Rahul 3D Engine Master Engineering Directive, CG Geek Nature Tutorial 1, and Layered Intelligence Standard.

## Global Constraints
- Preserve TCP Port 9876 and Protocol Version 15 for Blender communication.
- Every new engine module must be importable and testable without live `bpy` (using `HAS_BPY` fallback pattern).
- Keep `addon.py`, `src/blender_mcp/bundled/addon.py`, and Blender 5.2 user addons folder byte-identical (identical SHA256).
- Follow the 90/10 Hybrid Standard: Geometry built in BMesh/Geometry Nodes; no `bpy.ops` inside scattering loops.
- Support both Pure Simulation Mode and Fast Hybrid Mode across all soft goods tools without excluding either.

## Review Focus
1. Pure Simulation Mode integration: soft goods tools accept `simulation_mode` ("parametric", "hybrid", "pure_simulation") without breaking existing callers.
2. Geometry Nodes tree generation: grass field generation in Blender creates valid node tree links without GUI dependencies.
3. Non-bpy environments: all newly added tools return structured mock responses with `success=True` in pytest test suites.
4. Addon protocol parity: every newly registered FastMCP tool in `server.py` has an exact matching handler in `addon.py`.
5. Critic audit rigor: `validate_aesthetic_quality` reliably checks edge conditioning, quad topology, material setup, and soft goods crowns.

---

### Task 1: Implement Pure Simulation Pipeline & Assembly Settling (`simulate_cloth_assembly`)

**Files:**
- Modify: `src/blender_mcp/cloth_engine.py`
- Modify: `src/blender_mcp/soft_goods_engine.py`
- Test: `tests/test_v3_3_pure_simulation_pipeline.py`

- [x] Step 1: Write failing unit tests in `tests/test_v3_3_pure_simulation_pipeline.py` verifying:
  - `simulation_mode` parameter in `create_pillow`, `create_curtains`, `create_duvet`, `create_blanket` ("parametric", "hybrid", "pure_simulation").
  - `simulate_cloth_assembly` configuring obstacle collisions on furniture and baking multi-cloth physics.
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `simulation_mode` handling in `src/blender_mcp/soft_goods_engine.py`.
- [x] Step 4: Implement `simulate_cloth_assembly` in `src/blender_mcp/cloth_engine.py`.
- [x] Step 5: Run tests and verify all pass.

---

### Task 2: Implement Nature & Organic Environment Engine (`src/blender_mcp/nature_engine.py`)

**Files:**
- Create: `src/blender_mcp/nature_engine.py`
- Test: `tests/test_v3_3_nature_engine.py`

- [x] Step 1: Write failing unit tests in `tests/test_v3_3_nature_engine.py` covering:
  - `create_grass_blade_cluster` (curved blades, dead stalk variation, translucent material tag)
  - `create_grass_field` (Geometry Nodes procedural scattering with Musgrave density mask)
  - `create_terrain_ground` (displaced rolling ground mesh)
  - `scatter_foliage` (multi-asset foliage distribution with slope cutoff)
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `src/blender_mcp/nature_engine.py` with pure BMesh math generation for clusters and procedural Geometry Nodes setups for fields/foliage.
- [x] Step 4: Run tests and verify all pass.

---

### Task 3: Implement Layered Thinking & Independent Critic Engine (`src/blender_mcp/critic_engine.py`)

**Files:**
- Create: `src/blender_mcp/critic_engine.py`
- Test: `tests/test_v4_layered_thinking_critic.py`

- [x] Step 1: Write failing unit tests in `tests/test_v4_layered_thinking_critic.py` covering:
  - `decompose_scene_intent` (intent parsing, DAG generation, simulation mode prompt/choice)
  - `validate_aesthetic_quality` (topology, edge conditioning, soft goods crowns, score 0-100)
  - `audit_production_readiness` (transforms, materials, budgets, manifold geometry)
- [x] Step 2: Run test and verify failure.
- [x] Step 3: Implement `src/blender_mcp/critic_engine.py`.
- [x] Step 4: Run tests and verify all pass.

---

### Task 4: FastMCP Registration & Addon Sync for V3.3 & V4

**Files:**
- Modify: `src/blender_mcp/server.py`
- Modify: `addon.py`
- Modify: `src/blender_mcp/bundled/addon.py`
- Test: `tests/test_v3_3_v4_server_registration.py`

- [x] Step 1: Register all new V3.3 & V4 tools on FastMCP in `src/blender_mcp/server.py`:
  - `simulate_cloth_assembly`
  - `create_grass_blade_cluster`
  - `create_grass_field`
  - `create_terrain_ground`
  - `scatter_foliage`
  - `decompose_scene_intent`
  - `validate_aesthetic_quality`
  - `audit_production_readiness`
- [x] Step 2: Add dispatch handlers in `addon.py`.
- [x] Step 3: Mirror changes to `src/blender_mcp/bundled/addon.py` (verifying exact SHA256 parity).
- [x] Step 4: Sync `addon.py` to Blender 5.2 user addons folder (`C:\Users\Rahul\AppData\Roaming\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py`).
- [x] Step 5: Write and run `tests/test_v3_3_v4_server_registration.py`.

---

### Task 5: Full Regression Verification, Documentation & Knowledge Graph Update

**Files:**
- Modify: `docs/production_capability_audit.md`
- Modify: `README.md`
- Graph: `graphify-out/`

- [x] Step 1: Execute all test suites across the entire repository to confirm zero regressions.
- [x] Step 2: Update `docs/production_capability_audit.md` with V3.3 and V4 capabilities.
- [x] Step 3: Update `README.md` tool directory.
- [x] Step 4: Run `graphify update .`.
