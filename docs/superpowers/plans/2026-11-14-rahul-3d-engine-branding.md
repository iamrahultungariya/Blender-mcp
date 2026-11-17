# Rahul 3D Engine Branding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand the Blender MCP addon, server handshake, and N-panel sidebar to "Rahul 3D Engine" authored by "Rahul" without breaking internal operator dispatch or socket stability.

**Architecture:** Update user-facing metadata in `addon.py` (`bl_info`, `bl_category`, `bl_label`), configure FastMCP server name in `server.py`, adjust discovery regexes in `addon_manager.py` to recognize `Rahul 3D Engine`, mirror to `bundled/addon.py`, and deploy into Blender's user addons folder.

**Tech Stack:** Python 3.11+, Blender Python API (`bpy`), FastMCP / MCP SDK.

**Spec:** `docs/superpowers/specs/2026-11-14-rahul-3d-engine-branding-design.md`

## Global Constraints

- Keep internal operator IDs (`bpy.ops.wm.blender_mcp_*`) intact to avoid breaking scene scripts.
- Preserve communication socket port `9876` and protocol version `15`.
- Ensure `addon_manager.py` continues to discover and manage existing and updated addon files.
- Ensure `bundled/addon.py` is identical to root `addon.py`.

## Review Focus

- Addon discovery failure if `_BL_INFO_NAME_RE` is too strict: Ensure regex matches `Rahul 3D Engine`.
- Self-update integrity check failure in `addon.py:8297`: Ensure check validates `Rahul 3D Engine`.
- Viewport sidebar tab missing or misnamed: Ensure `bl_category = 'Rahul 3D'` is properly registered.
- FastMCP handshake reporting old server title: Ensure `FastMCP("Rahul 3D Engine", ...)` is initialized.
- Addon deployment file missing in Blender 5.2 roaming directory: Ensure `install_addon()` succeeds and file hash matches.

---

### Task 1: Rebrand Addon Metadata and Viewport UI in addon.py

**Files:**
- Modify: `c:/Users/Rahul/OneDrive/Desktop/Blender MCP/addon.py:33-43, 8033-8037, 8295-8300`

**Interfaces:**
- Consumes: `bl_info` dict, `BLENDERMCP_PT_Panel`
- Produces: Addon metadata with name `"Rahul 3D Engine"`, author `"Rahul"`, `bl_category = 'Rahul 3D'`

- [ ] **Step 1: Update `bl_info` in `addon.py`**
  Set `name` to `"Rahul 3D Engine"`, `author` to `"Rahul"`, `location` to `"View3D > Sidebar > Rahul 3D"`, `description` to `"Rahul 3D Engine MCP integration for autonomous 3D creation"`.

- [ ] **Step 2: Update Viewport Panel in `addon.py`**
  In `BLENDERMCP_PT_Panel`, set `bl_label = "Rahul 3D Engine"` and `bl_category = 'Rahul 3D'`.

- [ ] **Step 3: Update integrity self-check in `addon.py`**
  In line ~8297, update the check to verify `"Rahul 3D Engine"` in addition to `"MCP for Blender"`.

- [ ] **Step 4: Verify syntax**
  Run: `& .venv/Scripts/python.exe -m py_compile addon.py`
  Expected: PASS with exit code 0.

---

### Task 2: Update FastMCP Server Name, Addon Manager Regex, and pyproject.toml

**Files:**
- Modify: `c:/Users/Rahul/OneDrive/Desktop/Blender MCP/src/blender_mcp/server.py:358-362`
- Modify: `c:/Users/Rahul/OneDrive/Desktop/Blender MCP/src/blender_mcp/addon_manager.py:25-34`
- Modify: `c:/Users/Rahul/OneDrive/Desktop/Blender MCP/pyproject.toml:7-9`

**Interfaces:**
- Consumes: FastMCP initialization, `_BL_INFO_NAME_RE` in `addon_manager.py`
- Produces: MCP server named `"Rahul 3D Engine"`, regex recognizing `"Rahul 3D Engine"`

- [ ] **Step 1: Update FastMCP server initialization in `src/blender_mcp/server.py`**
  Set `mcp = FastMCP("Rahul 3D Engine", lifespan=server_lifespan, instructions=SERVER_INSTRUCTIONS)`.

- [ ] **Step 2: Update `_BL_INFO_NAME_RE` in `src/blender_mcp/addon_manager.py`**
  Update regex to `r"""["']name["']\s*:\s*["'](?:Rahul 3D Engine|MCP for Blender|Blender MCP)["']"""` and update `_ADDON_MARKER` to match `Rahul 3D Engine`.

- [ ] **Step 3: Update author in `pyproject.toml`**
  Set `authors = [{name = "Rahul"}]`.

- [ ] **Step 4: Verify syntax of server and addon_manager**
  Run: `& .venv/Scripts/python.exe -m py_compile src/blender_mcp/server.py src/blender_mcp/addon_manager.py`
  Expected: PASS with exit code 0.

---

### Task 3: Bundle, Install, and Verify in Blender 5.2 Addons Directory

**Files:**
- Modify: `c:/Users/Rahul/OneDrive/Desktop/Blender MCP/src/blender_mcp/bundled/addon.py`
- Target: `C:/Users/Rahul/AppData/Roaming/Blender Foundation/Blender/5.2/scripts/addons/blender_mcp.py`

**Interfaces:**
- Consumes: `addon.py`
- Produces: Synchronized `bundled/addon.py` and deployed `blender_mcp.py` in Blender 5.2

- [ ] **Step 1: Sync `bundled/addon.py`**
  Copy `addon.py` to `src/blender_mcp/bundled/addon.py`.

- [ ] **Step 2: Deploy addon to Blender 5.2**
  Run: `& .venv/Scripts/python.exe -c "from blender_mcp.addon_manager import install_addon; print(install_addon())"`
  Expected: Output `AddonInstallResult(success=True, ... target_path=...blender_mcp.py...)`.

- [ ] **Step 3: Verify addon status and discovery**
  Run: `& .venv/Scripts/python.exe -c "from blender_mcp.addon_manager import check_addon_status_on_startup; print(check_addon_status_on_startup())"`
  Expected: `reason='already_current'`, `missing=False`.

- [ ] **Step 4: Verify deployed addon content**
  Check that `C:/Users/Rahul/AppData/Roaming/Blender Foundation/Blender/5.2/scripts/addons/blender_mcp.py` contains `"Rahul 3D Engine"` and `bl_category = 'Rahul 3D'`.
