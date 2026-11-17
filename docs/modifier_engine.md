# Modifier Stack Automation Engine (System 08)
**Rahul 3D Engine — Phase 7 Documentation**

---

## 1. Overview
The Modifier Stack Engine provides a declarative, JSON-driven interface to construct, order, inspect, and safely collapse modifier stacks.

Supported modifier types:
- `BEVEL`, `SUBSURF`, `SOLIDIFY`, `ARRAY`, `MIRROR`, `DECIMATE`, `REMESH`, `WEIGHTED_NORMAL`, `SHRINKWRAP`, `DISPLACE`, `BOOLEAN`.

---

## 2. FastMCP Tool Interface

### `apply_modifier_stack`
Configures an ordered array of modifiers on a target object.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `stack` (list[dict]): List of modifier definitions (e.g. `[{"type": "BEVEL", "width": 0.02, "segments": 3, "harden_normals": True}, {"type": "SUBSURF", "levels": 2}]`).
  - `apply_immediately` (bool): If True, destructively applies modifiers to mesh data.
- **Risk**: `DESTRUCTIVE` if `apply_immediately=True`, else `REVERSIBLE`.

### `inspect_modifier_stack`
Returns structured inventory of all modifiers on an object with their visibility and primary settings.
- **Risk**: `READ_ONLY`.

### `freeze_modifiers`
Destructively collapses modifiers into static vertex/face geometry, with optional backup creation.
- **Parameters**:
  - `object_name` (str): Target mesh object.
  - `modifier_names` (list[str], optional): Specific modifiers to apply (applies all if omitted).
  - `create_backup` (bool): Duplicate mesh datablock before collapsing (default: True).
- **Risk**: `DESTRUCTIVE`.
