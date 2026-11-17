# Phases 1–3: Foundation, PBR Materials & Cinematic Lighting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Phases 1–3 of the Rahul 3D Engine Master Engineering Directive: Scene Checkpointing & Safety Architecture (System 07), PBR Material & Procedural Shader Engine (System 01), and Cinematic Studio Lighting & HDRI Engine (System 02), fully integrated across the FastMCP server, Blender addon, and test suites.

**Architecture:** 
- Modular engine design: Core logic resides in dedicated modules (`foundation.py`, `checkpoint_manager.py`, `material_engine.py`, `lighting_engine.py`) under `src/blender_mcp/`.
- Blender execution: `addon.py` imports these engines and dispatches requests received over the TCP socket (`127.0.0.1:9876`, Protocol v15).
- Server orchestration: `server.py` exposes strongly typed FastMCP tools with structured result schemas (`success`, `tool`, `operation_id`, `result`, `warnings`, `errors`, `validation`) and risk classifications (`READ_ONLY`, `NON_DESTRUCTIVE`, `REVERSIBLE`, `DESTRUCTIVE`).
- Fallback & safety: Pure Python/numpy fallback execution paths allow unit tests to pass without `bpy` present.

**Tech Stack:** Python 3.11+, Blender Python API (`bpy`, `bmesh`, `mathutils`), FastMCP / MCP SDK, Pytest.

**Spec:** `docs/production_capability_audit.md` and Master Engineering Directive.

## Global Constraints

- Do not alter or break TCP port `9876` or Protocol version `15`.
- Do not modify or break any of the 41 existing MCP tools.
- Keep `src/blender_mcp/bundled/addon.py` 100% byte-identical to `addon.py`.
- Handle multi-version socket aliases for Blender 3.x, 4.x, and 5.x LTS (`Clearcoat` vs `Coat Weight`, `Specular` vs `Specular IOR Level`, `Transmission` vs `Transmission Weight`, `Emission` vs `Emission Color`).
- Safe execution: destructive operations (like checkpoint restoration or material overwrite) must be marked `DESTRUCTIVE` and report explicit validation warnings.

## Review Focus

1. *Principled BSDF socket compatibility across versions*: Ensure `material_engine.py` uses fallback alias dictionaries so it never crashes on Blender 3.6 LTS, 4.2 LTS, or 5.x.
2. *Non-destructive checkpointing*: Ensure `create_scene_checkpoint()` uses `bpy.ops.wm.save_as_mainfile(copy=True)` so it does not hijack Blender's active file path.
3. *Headless / CI test resilience*: Modules must cleanly guard `import bpy` with `try/except ImportError: HAS_BPY = False` so pytest passes in standard virtual environments.
4. *Light energy calibration*: Ensure studio lighting presets calculate appropriate wattages/lumens based on object bounding dimensions rather than static blind values.
5. *Addon deployment parity*: Ensure `install_addon()` copies the updated `addon.py` to the local Blender user directory so live testing succeeds.

---

### Task 1: Phase 1 — Foundation, Structured Result Schema & Checkpoint Engine

**Files:**
- Create: `src/blender_mcp/foundation.py`
- Create: `src/blender_mcp/checkpoint_manager.py`
- Modify: `addon.py` (Command routing lines 1950-2050 + implementation methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase1_foundation_safety.py`

**Interfaces:**
- Consumes: `bpy.ops.wm.save_as_mainfile`, `bpy.ops.wm.open_mainfile`
- Produces: MCP tools `create_scene_checkpoint`, `restore_scene_checkpoint`, `list_scene_checkpoints`, `delete_scene_checkpoint`

- [x] **Step 1: Create `src/blender_mcp/foundation.py`**
  Implement:
  - `OperationRisk(Enum)`: `READ_ONLY`, `NON_DESTRUCTIVE`, `REVERSIBLE`, `DESTRUCTIVE`.
  - `format_tool_response(tool_name: str, result: Any, success: bool = True, warnings: list = None, errors: list = None, validation: dict = None, risk: OperationRisk = OperationRisk.NON_DESTRUCTIVE) -> dict`.
  - Input validation helpers: `validate_object_exists(name)`, `validate_positive_float(val, name)`.

- [x] **Step 2: Create `src/blender_mcp/checkpoint_manager.py`**
  Implement:
  - Checkpoint storage directory: `.checkpoints/` inside active project or system temp directory.
  - `create_checkpoint(label: str, description: str = "", checkpoint_type: str = "MANUAL") -> dict`: Generates timestamped `.blend` copy snapshot and writes metadata JSON (`id`, `label`, `timestamp`, `path`, `object_count`, `active_object`).
  - `restore_checkpoint(label_or_id: str) -> dict`: Safely reloads or verifies checkpoint file.
  - `list_checkpoints() -> list[dict]`: Returns sorted list of available checkpoints.
  - `delete_checkpoint(label_or_id: str) -> dict`: Removes specific checkpoint and cleans up disk storage.

- [x] **Step 3: Update `addon.py` with Checkpoint Dispatchers**
  Add command handlers:
  - `"create_scene_checkpoint"` -> `self.create_scene_checkpoint(**params)`
  - `"restore_scene_checkpoint"` -> `self.restore_scene_checkpoint(**params)`
  - `"list_scene_checkpoints"` -> `self.list_scene_checkpoints(**params)`
  - `"delete_scene_checkpoint"` -> `self.delete_scene_checkpoint(**params)`

- [x] **Step 4: Expose Checkpoint Tools in `server.py`**
  Register FastMCP tools with docstrings, parameter types, and risk tags.

- [x] **Step 5: Write and run Phase 1 unit tests**
  Create `tests/test_phase1_foundation_safety.py` and run:
  `& .venv/Scripts/python.exe -m pytest tests/test_phase1_foundation_safety.py`
  Expected: PASS.

---

### Task 2: Phase 2 — PBR Material & Procedural Shader Engine

**Files:**
- Create: `src/blender_mcp/material_engine.py`
- Modify: `addon.py` (Command routing + dispatch methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase2_material_engine.py`

**Interfaces:**
- Consumes: `bpy.data.materials`, `ShaderNodeBsdfPrincipled`, `ShaderNodeTexNoise`, `ShaderNodeTexVoronoi`, etc.
- Produces: MCP tools:
  - `assign_pbr_material(object_name, material_name, base_color, metallic, roughness, alpha, emission_color, emission_strength, normal_strength, assign_mode)`
  - `inspect_material_nodes(material_name, include_links, include_node_properties)`
  - `create_procedural_shader(material_name, preset, object_name, scale, color_tint, roughness_multiplier)`
  - `modify_material_property(material_name, property_name, value)`
  - `validate_material_setup(material_name)`

- [x] **Step 1: Create `src/blender_mcp/material_engine.py`**
  Implement:
  - Version-aware Principled BSDF socket resolver: `find_principled_bsdf()`, `set_socket_value()`, `get_socket_value()`.
  - `assign_pbr_material(...)`: Creates/reuses material, configures Principled BSDF, assigns to object material slots (or active slot).
  - `inspect_material_nodes(...)`: Traverses node tree and returns structured graph (nodes, inputs, outputs, links, missing links).
  - `create_procedural_shader(...)`: 15 physically-calibrated procedural presets:
    1. `wood`: Musgrave/Noise waves, subtle bump, natural grain roughness.
    2. `brushed_metal`: Anisotropic/stretched noise, metallic 1.0, fine micro-scratches.
    3. `polished_metal`: Ultra-low roughness (0.05), metallic 1.0.
    4. `concrete`: Aggregate voronoi + layered noise bump.
    5. `marble`: Veined noise wave distortion + low roughness subsurface scattering.
    6. `leather`: Voronoi cell boundaries, organic bump, flexible roughness.
    7. `fabric_weave`: Micro-crosshatch pattern, velvet sheen/fuzz.
    8. `plastic`: Pure dielectric, configurable color and specular.
    9. `ceramic`: Clean glazed dielectric with high clearcoat.
    10. `rubber`: High roughness (0.65), low specular, pure dielectric.
    11. `painted_wall`: Subtle plaster orange-peel micro-stipple bump.
    12. `aged_wood`: Darkened grain ridges, weathered desaturation.
    13. `rusted_metal`: Masked metallic/roughness blend simulating oxidized iron.
    14. `stone`: Multi-frequency noise displacement and mineral variation.
    15. `glass`: Transmission 1.0, IOR 1.52, roughness 0.02.
  - `modify_material_property(...)`: Safe targeted property tweak on Principled BSDF.
  - `validate_material_setup(...)`: Checks for missing output nodes, broken links, disconnected BSDFs.

- [x] **Step 2: Update `addon.py` with Material Engine Handlers**
  Add command handlers:
  - `"assign_pbr_material"`
  - `"inspect_material_nodes"`
  - `"create_procedural_shader"`
  - `"modify_material_property"`
  - `"validate_material_setup"`

- [x] **Step 3: Expose Material Engine Tools in `server.py`**
  Register FastMCP tools with rich docstrings and validation.

- [x] **Step 4: Write and run Phase 2 unit tests**
  Create `tests/test_phase2_material_engine.py` and run:
  `& .venv/Scripts/python.exe -m pytest tests/test_phase2_material_engine.py`
  Expected: PASS.

---

### Task 3: Phase 3 — Cinematic Studio Lighting & HDRI Engine

**Files:**
- Create: `src/blender_mcp/lighting_engine.py`
- Modify: `addon.py` (Command routing + dispatch methods)
- Modify: `src/blender_mcp/bundled/addon.py` (Mirrored copy)
- Modify: `src/blender_mcp/server.py` (FastMCP tool registrations)
- Create: `tests/test_phase3_lighting_engine.py`

**Interfaces:**
- Consumes: `bpy.data.lights`, `bpy.data.worlds`, `bpy.data.collections`
- Produces: MCP tools:
  - `setup_studio_lighting(preset, target_object, energy_multiplier, color_temperature, shadow_quality, world_strength, collection_name)`
  - `setup_environment_hdri(hdri_path_or_preset, strength, rotation, background_visibility)`
  - `inspect_lighting_setup()`
  - `adjust_lighting_for_object(target_object, key_fill_ratio)`

- [x] **Step 1: Create `src/blender_mcp/lighting_engine.py`**
  Implement 10 distinct, mathematically calibrated lighting presets:
  1. `three_point`: Classic key (45°), fill (opposing 45°, half intensity), rim (backlight).
  2. `dramatic_rim`: High-contrast dual rear edge kickers with minimal frontal fill.
  3. `soft_interior`: Large overhead softboxes + warm cove light fill.
  4. `product_clean`: High-key 4-point studio cyclorama lighting with white floor bounce.
  5. `cinematic`: Moody warm key (3200K) + cool complementary fill (6500K) + sharp edge rim.
  6. `architectural`: Balanced daylight sun angle + ambient sky fill.
  7. `horror_atmosphere`: Low-angle harsh green/cool single-source key + deep dark shadows.
  8. `daylight`: Direct sun (5000W) + ambient world sky.
  9. `night_scene`: Cool moonlight + warm point/spot accents.
  10. `automotive_studio`: Elongated overhead strip softboxes to create continuous reflection streaks on body panels.
  Implement:
  - `setup_environment_hdri(...)`: Configures World shader node tree (`Background` + `Environment Texture` + `Mapping` + `Texture Coordinate`).
  - `inspect_lighting_setup(...)`: Returns structured report of all scene lights (type, energy, color, location, size) and world environment settings.
  - `adjust_lighting_for_object(...)`: Measures object bounding box and scales light distances and sizes dynamically.

- [x] **Step 2: Update `addon.py` with Lighting Engine Handlers**
  Add command handlers:
  - `"setup_studio_lighting"`
  - `"setup_environment_hdri"`
  - `"inspect_lighting_setup"`
  - `"adjust_lighting_for_object"`

- [x] **Step 3: Expose Lighting Engine Tools in `server.py`**
  Register FastMCP tools with rich docstrings and validation.

- [x] **Step 4: Write and run Phase 3 unit tests**
  Create `tests/test_phase3_lighting_engine.py` and run:
  `& .venv/Scripts/python.exe -m pytest tests/test_phase3_lighting_engine.py`
  Expected: PASS.

---

### Task 4: Addon Synchronization, Deployment & Regression Suite Verification

**Files:**
- Modify: `src/blender_mcp/bundled/addon.py` (Ensure byte parity with `addon.py`)
- Deploy to: `C:/Users/Rahul/AppData/Roaming/Blender Foundation/Blender/5.2/scripts/addons/blender_mcp.py`
- Create docs:
  - `docs/scene_checkpoint.md`
  - `docs/material_engine.md`
  - `docs/lighting_engine.md`

- [x] **Step 1: Mirror `addon.py` to `src/blender_mcp/bundled/addon.py`**
- [x] **Step 2: Deploy addon to local Blender user addons folder**
  Run: `& .venv/Scripts/python.exe -c "from blender_mcp.addon_manager import install_addon; print(install_addon())"`
- [x] **Step 3: Run comprehensive pytest regression suite**
  Verify all Phase 1, Phase 2, Phase 3 tests pass alongside existing DXR and spatial tool tests.
- [x] **Step 4: Author feature documentation**
  Write detailed reference docs in `docs/scene_checkpoint.md`, `docs/material_engine.md`, and `docs/lighting_engine.md`.
