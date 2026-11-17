# Design Document: Rahul 3D Engine Custom Branding & Rebranding

**Date:** 2026-11-14  
**Author:** Rahul  
**Status:** Approved  

## 1. Intent & Goals
The goal is to customize and rebrand the local Blender MCP addon and server components to reflect Rahul's custom identity ("Rahul 3D Engine"), removing references to "Siddharth Ahuja" and "MCP for Blender" in user-facing surfaces.

### Goals
- Update Blender Add-on metadata (`bl_info`) to Display Name: `Rahul 3D Engine`, Author: `Rahul`.
- Set Viewport 3D sidebar tab (N-panel `bl_category`) to `Rahul 3D`, with panel title `Rahul 3D Engine`.
- Update FastMCP server name in `server.py` to `Rahul 3D Engine` for handshake.
- Update `addon_manager.py` discovery regexes and messages so it seamlessly detects, verifies, and installs `Rahul 3D Engine` without breaking backward/forward compatibility.
- Synchronize root `addon.py`, `src/blender_mcp/bundled/addon.py`, and install directly to Blender's user addons directory (`blender_mcp.py`).

### Non-Goals
- Altering internal operator identifiers (`bpy.ops.wm.blender_mcp_*`) or socket communication ports (`9876`) to prevent breaking existing scene scripts or internal handlers.

## 2. Approaches Considered
1. **Full Namespace & Identifier Rename:**
   - *Pros:* Complete white-labeling down to variable names.
   - *Cons:* High risk of breaking internal dispatch table, operator callbacks, and socket protocol.
2. **Targeted Branding & Interface Layer (Recommended & Approved):**
   - *Pros:* Updates all visible surfaces (`bl_info`, N-panel category, panel labels, FastMCP server title, package authors, addon manager detection regex) cleanly with zero breakage risk.
   - *Cons:* None.
