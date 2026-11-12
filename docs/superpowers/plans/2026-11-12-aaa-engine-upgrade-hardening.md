# Implementation Plan: Blender MCP AAA Engine Upgrade Hardening & Guardrails

**Date**: 2026-11-12  
**Target File**: `docs/superpowers/plans/2026-11-12-aaa-engine-upgrade-hardening.md`  
**Status**: Completed  
**Priority**: High  

---

## Verification Summary
- [x] Task 1: `pyproject.toml` pythonpath configured; 31 apex_gtr tests collect and pass.
- [x] Task 2: Blender 5.3 & 5.3+ auto-smooth "Smooth by Angle" NODES modifier & polygon smooth shading implemented.
- [x] Task 3: `apply_uv_unwrap` tool exposed in `server.py` and dispatched in `addon.py`.
- [x] Task 4: `export_game_asset` selection isolation (BUG-03) and Iron Law 4 UV inspection/auto_uv/enforce_uv.
- [x] Task 5: 6-Phase pipeline state persisted to `.pipeline_state.json` with auto-save on status changes.
- [x] Task 6: Skill G0-G6 string aliases bridged to Phase 1-6 in `validate_phase_gate()`.
- [x] All 26 core quality and robustness tests passing (100% green).

---

## 1. Goal

Harden the Blender MCP engine post-v2.2 upgrade by resolving newly discovered compatibility and pipeline flaws:
1. Fix `pyproject.toml` test configuration.
2. Fix Blender 4.1+ auto-smooth normal handling in `clas_tensor_shaper.py`.
3. Expose `apply_uv_unwrap` as an MCP tool and enforce Iron Law 4 (Mandatory UV) in `export_game_asset`.
4. Ensure `export_game_asset` isolates selection before applying transforms.
5. Persist `pipeline_gates.py` progress to disk (`.pipeline_state.json`).
6. Bridge Skill G0-G6 quality gates with Python Phase 1-6 validator.

---

## 2. Architecture & Tech Stack

- **Server**: FastMCP (Python 3.10+, `mcp>=1.26.0`)
- **Addon Engine**: Blender 4.x/5.x Python API (`bpy`, `bmesh`, `mathutils`)
- **Testing**: `pytest`, `pytest-asyncio`
- **Rule Set**: 90/10 Hybrid Pipeline Standard (Zone A: `bmesh` 90%, Zone B: `bpy.ops` 10%)

---

## 3. Step-by-Step Execution Plan

### Task 1: Fix `pyproject.toml` Test Environment
- **File**: `pyproject.toml`
- **Changes**: Add `pythonpath = ["."]` under `[tool.pytest.ini_options]` so root packages/scripts can be imported without manual path overrides.
- **Verification**: Run `uv run pytest tests/test_geometry_engineering_robustness.py` and verify collection works cleanly.

### Task 2: Fix Blender 4.1+ Auto-Smooth Compatibility
- **File**: `src/blender_mcp/kernel/clas_tensor_shaper.py`
- **Changes**:
  In `apply_blender_version_compatibility(node_or_mesh)`:
  - For Blender 4.1+, if target is a Mesh Object, ensure smooth shading is enabled and add the `NODES` modifier (`GeometryNodeSmoothByAngle` or "Smooth by Angle") if not already present.
  - Return clear status instead of silently swallowing with `pass`.
- **Verification**: Run unit test verifying Blender 4.1+ object normal handling.

### Task 3: Expose `apply_uv_unwrap` Tool in FastMCP Server & Addon
- **Files**:
  - `src/blender_mcp/server.py`
  - `src/blender_mcp/bundled/addon.py`
  - `addon.py`
- **Changes**:
  - Expose `@mcp.tool() async def apply_uv_unwrap(target_object: str, angle_limit_deg: float = 66.0, island_margin: float = 0.02) -> dict` in `server.py`.
  - Dispatch command `apply_uv_unwrap` in `addon.py` invoking `bmesh_toolkit.apply_smart_uv_unwrapping`.
- **Verification**: Create a mock test ensuring `apply_uv_unwrap` is exposed in `server.py` and callable via JSON-RPC.

### Task 4: Enforce UV Validation & Selection Isolation in `export_game_asset`
- **Files**:
  - `src/blender_mcp/bundled/addon.py`
  - `addon.py`
- **Changes**:
  In `export_game_asset`:
  1. Call `bpy.ops.object.select_all(action='DESELECT')` before setting `obj.select_set(True)`.
  2. Inspect `obj.data.uv_layers`. If empty and `auto_uv=True` (or by default), call `apply_smart_uv_unwrapping(obj)`.
  3. If mesh has no UVs and `enforce_uv=True`, return `{"status": "error", "error": "Iron Law 4 Violation: Asset has no UV coordinates"}`.
- **Verification**: Add test verifying export fails on non-UV mesh when `enforce_uv=True`, or automatically generates UVs when `auto_uv=True`.

### Task 5: Persist 6-Phase Pipeline State to Disk
- **File**: `src/blender_mcp/pipeline_gates.py`
- **Changes**:
  - In `PhaseGateManager`, add `save_state(filepath)` and `load_state(filepath)`.
  - By default, load from `.pipeline_state.json` in the current workspace if present.
  - On every gate status change (`validate_gate`, `reset`), persist state to file.
- **Verification**: Test that resetting/advancing gates survives recreating `PhaseGateManager` instance when pointing to the same state file.

### Task 6: Bridge Skill G0-G6 Gates with Pipeline Validator
- **File**: `src/blender_mcp/pipeline_gates.py`
- **Changes**:
  - Add string alias mapping:
    ```python
    GATE_ALIAS_MAP = {
        "G1": 1, "G0": 1,
        "G2": 2, "G3": 3,
        "G4": 4, "G5": 5, "G6": 6
    }
    ```
  - Allow `validate_gate(phase_id: int | str, evidence=...)` to accept strings like `"G3"` or `"Phase 3"`.
- **Verification**: Test passing `"G3"` into `validate_phase_gate()` and ensuring it maps to Phase 3.

---

## 4. Verification Checklist & Success Criteria

- [ ] All 21 core geometry/contract tests continue to pass (`uv run pytest tests/test_geometry_engineering_robustness.py tests/test_full_artist_contract_v2.py ...`)
- [ ] `uv run pytest` runs without collection crashes across all files.
- [ ] `server.py` exposes `apply_uv_unwrap`.
- [ ] `export_game_asset` reports UV status and enforces Iron Law 4.
- [ ] Blender 4.1+ modifier-based auto-smooth path is robust.
