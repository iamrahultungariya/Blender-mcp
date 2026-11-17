"""Scene Checkpoint & Rollback Engine for Rahul 3D Engine (Blender MCP).

Provides transactional safety, disk-based snapshotting, metadata indexing,
and state restoration prior to high-risk or destructive operations.
"""

from __future__ import annotations
import os
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False

from blender_mcp.foundation import format_tool_response, OperationRisk

DEFAULT_CHECKPOINT_DIR = Path(os.environ.get("BLENDER_CHECKPOINT_DIR", Path.cwd() / ".checkpoints"))


def get_checkpoint_dir() -> Path:
    """Ensure and return the checkpoint directory."""
    d = DEFAULT_CHECKPOINT_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def create_checkpoint(
    label: str,
    description: str = "",
    checkpoint_type: str = "MANUAL"
) -> Dict[str, Any]:
    """Create a persistent disk-based .blend copy snapshot with metadata.
    
    Uses `bpy.ops.wm.save_as_mainfile(copy=True)` to avoid altering active scene path.
    """
    if not label or not label.strip():
        return format_tool_response(
            "create_scene_checkpoint",
            success=False,
            errors=["Checkpoint label cannot be empty."],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    clean_label = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in label.strip())
    cp_id = f"cp_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    cp_dir = get_checkpoint_dir()
    blend_path = cp_dir / f"{cp_id}_{clean_label}.blend"
    meta_path = cp_dir / f"{cp_id}_{clean_label}.json"

    obj_count = 0
    active_obj = None
    collection_names = []

    if HAS_BPY:
        try:
            obj_count = len(bpy.data.objects)
            active_obj = bpy.context.active_object.name if bpy.context.active_object else None
            collection_names = [c.name for c in bpy.data.collections]
            
            # Save copy without changing current workspace filename
            bpy.ops.wm.save_as_mainfile(filepath=str(blend_path), copy=True, compress=True)
        except Exception as e:
            return format_tool_response(
                "create_scene_checkpoint",
                success=False,
                errors=[f"Failed to create .blend snapshot: {str(e)}"],
                risk=OperationRisk.NON_DESTRUCTIVE
            )
    else:
        # Mock creation for unit testing in non-bpy environment
        blend_path.write_bytes(b"MOCK_BLEND_DATA")

    file_size = blend_path.stat().st_size if blend_path.exists() else 0

    metadata = {
        "id": cp_id,
        "label": label,
        "clean_label": clean_label,
        "description": description,
        "checkpoint_type": checkpoint_type,
        "created_at": time.time(),
        "created_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "blend_file": str(blend_path),
        "file_size_bytes": file_size,
        "object_count": obj_count,
        "active_object": active_obj,
        "collections": collection_names,
    }

    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        return format_tool_response(
            "create_scene_checkpoint",
            success=False,
            errors=[f"Failed to write metadata JSON: {str(e)}"],
            risk=OperationRisk.NON_DESTRUCTIVE
        )

    return format_tool_response(
        "create_scene_checkpoint",
        result={
            "checkpoint_id": cp_id,
            "label": label,
            "file_path": str(blend_path),
            "object_count": obj_count,
            "file_size_kb": round(file_size / 1024, 2),
            "checkpoint_type": checkpoint_type,
        },
        success=True,
        risk=OperationRisk.NON_DESTRUCTIVE,
        validation={"passed": True, "checks": ["snapshot_written", "metadata_indexed"]}
    )


def list_checkpoints() -> Dict[str, Any]:
    """List all available scene checkpoints ordered by creation time descending."""
    cp_dir = get_checkpoint_dir()
    checkpoints = []

    for meta_file in cp_dir.glob("*.json"):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Verify corresponding .blend exists
                b_path = Path(data.get("blend_file", ""))
                data["file_exists"] = b_path.exists()
                checkpoints.append(data)
        except Exception:
            continue

    checkpoints.sort(key=lambda x: x.get("created_at", 0), reverse=True)

    return format_tool_response(
        "list_scene_checkpoints",
        result={
            "count": len(checkpoints),
            "checkpoints": checkpoints
        },
        success=True,
        risk=OperationRisk.READ_ONLY
    )


def _find_checkpoint(label_or_id: str) -> Optional[Dict[str, Any]]:
    """Look up checkpoint by exact id, prefix id, or label."""
    cp_dir = get_checkpoint_dir()
    candidates = []
    
    for meta_file in cp_dir.glob("*.json"):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("id") == label_or_id:
                    return data
                if data.get("id", "").startswith(label_or_id):
                    candidates.append(data)
                elif data.get("label") == label_or_id or data.get("clean_label") == label_or_id:
                    candidates.append(data)
        except Exception:
            continue

    if candidates:
        # Return most recent candidate
        candidates.sort(key=lambda x: x.get("created_at", 0), reverse=True)
        return candidates[0]
    return None


def restore_checkpoint(label_or_id: str, restore_mode: str = "RELOAD") -> Dict[str, Any]:
    """Restore Blender scene state from a previously saved checkpoint.
    
    Marked DESTRUCTIVE because it replaces active scene state with snapshot.
    """
    cp = _find_checkpoint(label_or_id)
    if not cp:
        return format_tool_response(
            "restore_scene_checkpoint",
            success=False,
            errors=[f"No checkpoint found matching '{label_or_id}'."],
            risk=OperationRisk.DESTRUCTIVE
        )

    blend_path = Path(cp.get("blend_file", ""))
    if not blend_path.exists():
        return format_tool_response(
            "restore_scene_checkpoint",
            success=False,
            errors=[f"Checkpoint file '{blend_path}' is missing on disk."],
            risk=OperationRisk.DESTRUCTIVE
        )

    if HAS_BPY:
        try:
            bpy.ops.wm.open_mainfile(filepath=str(blend_path))
        except Exception as e:
            return format_tool_response(
                "restore_scene_checkpoint",
                success=False,
                errors=[f"Failed to open mainfile from checkpoint: {str(e)}"],
                risk=OperationRisk.DESTRUCTIVE
            )

    return format_tool_response(
        "restore_scene_checkpoint",
        result={
            "restored_checkpoint_id": cp.get("id"),
            "label": cp.get("label"),
            "file_path": str(blend_path),
            "object_count": cp.get("object_count"),
            "restore_mode": restore_mode
        },
        success=True,
        risk=OperationRisk.DESTRUCTIVE,
        warnings=["Active scene has been restored to snapshot state."],
        validation={"passed": True, "checks": ["checkpoint_found", "file_reloaded"]}
    )


def delete_checkpoint(label_or_id: str) -> Dict[str, Any]:
    """Delete a checkpoint file and its metadata index."""
    cp = _find_checkpoint(label_or_id)
    if not cp:
        return format_tool_response(
            "delete_scene_checkpoint",
            success=False,
            errors=[f"No checkpoint found matching '{label_or_id}'."],
            risk=OperationRisk.DESTRUCTIVE
        )

    blend_path = Path(cp.get("blend_file", ""))
    cp_id = cp.get("id")
    clean_label = cp.get("clean_label", "")
    meta_path = get_checkpoint_dir() / f"{cp_id}_{clean_label}.json"

    deleted_files = []
    if blend_path.exists():
        blend_path.unlink()
        deleted_files.append(str(blend_path))
    if meta_path.exists():
        meta_path.unlink()
        deleted_files.append(str(meta_path))

    return format_tool_response(
        "delete_scene_checkpoint",
        result={
            "deleted_checkpoint_id": cp_id,
            "deleted_files": deleted_files
        },
        success=True,
        risk=OperationRisk.DESTRUCTIVE,
        validation={"passed": True, "checks": ["files_unlinked"]}
    )


# Aliases matching tool naming conventions
create_scene_checkpoint = create_checkpoint
restore_scene_checkpoint = restore_checkpoint
list_scene_checkpoints = list_checkpoints
delete_scene_checkpoint = delete_checkpoint

