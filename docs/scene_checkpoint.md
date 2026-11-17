# Scene Checkpoint & Safety Engine (System 07)
**Rahul 3D Engine — Phase 1 Documentation**

---

## 1. Overview
The Scene Checkpoint & Safety Engine provides a reliable recovery mechanism for high-risk operations (e.g. destructive booleans, quad remeshing, modifier collapsing, and batch script modifications).

Instead of brittle in-memory representations, checkpoints are stored as **genuine `.blend` copy snapshots** alongside JSON metadata files in a designated `.checkpoints/` directory.

---

## 2. FastMCP Tool Interface

### `create_scene_checkpoint`
Creates a timestamped snapshot of the current Blender scene without altering the active workspace file path.
- **Parameters**:
  - `label` (str, required): Descriptive tag (e.g., `pre_boolean_cutout`, `blockout_verified`).
  - `description` (str, optional): Additional context about what is being preserved.
  - `checkpoint_type` (str): `MANUAL` or `AUTO`.
- **Risk Classification**: `NON_DESTRUCTIVE`.
- **Returns**: Checkpoint ID, file path, object count, and file size in KB.

### `restore_scene_checkpoint`
Restores Blender to an exact previous snapshot.
- **Parameters**:
  - `label_or_id` (str, required): Full checkpoint ID (e.g., `cp_1731760000_a1b2c3`) or label.
  - `restore_mode` (str): `RELOAD`.
- **Risk Classification**: `DESTRUCTIVE` (Replaces active scene data).

### `list_scene_checkpoints`
Lists all available checkpoints ordered chronologically (newest first).
- **Risk Classification**: `READ_ONLY`.
- **Returns**: List of metadata dictionaries containing IDs, labels, timestamps, object counts, and disk status.

### `delete_scene_checkpoint`
Permanently deletes a checkpoint `.blend` file and its metadata index to reclaim disk storage.
- **Parameters**:
  - `label_or_id` (str, required): Target checkpoint ID or label.
- **Risk Classification**: `DESTRUCTIVE`.

---

## 3. Best Practices & Gating
- **Always checkpoint before high-risk actions**: Call `create_scene_checkpoint` before executing boolean differences, remeshing, or applying irreversible modifiers.
- **Clean up old checkpoints**: Call `delete_scene_checkpoint` after verifying successful asset export to prevent disk bloat.
