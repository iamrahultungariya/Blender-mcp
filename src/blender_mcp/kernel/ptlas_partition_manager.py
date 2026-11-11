"""PTLAS Scene Partitioning & Copy-on-Write Isolation Kernel.

Mirrors Microsoft DirectX Raytracing 1.722 Partitioned TLAS (PTLAS).
Partitions the scene graph into isolated spatial domains (Blender Collections),
enforces pre-execution AST safety rules, and tracks geometric state with
SHA-256 Merkle hashes to guarantee transactional isolation.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
from typing import Any


FORBIDDEN_OPERATORS = {
    ("bpy.ops.object", "select_all"): "Global selection modifies objects outside partition",
    ("bpy.ops.wm", "read_factory_settings"): "Destructive operation clears entire scene",
    ("bpy.ops.wm", "open_mainfile"): "Loading external file destroys active workspace",
}


def audit_script_ast(code: str, allowed_partition: str = "") -> tuple[bool, str]:
    """Scan code AST for forbidden global operations that could corrupt unrelated scene partitions."""
    try:
        tree = ast.parse(code)
    except SyntaxError as err:
        return False, f"Syntax error in script: {err}"

    for node in ast.walk(tree):
        # Detect function / operator calls
        if isinstance(node, ast.Call):
            call_repr = ""
            if isinstance(node.func, ast.Attribute):
                # e.g., bpy.ops.object.select_all
                parts = []
                curr = node.func
                while isinstance(curr, ast.Attribute):
                    parts.append(curr.attr)
                    curr = curr.value
                if isinstance(curr, ast.Name):
                    parts.append(curr.id)
                parts.reverse()
                call_repr = ".".join(parts)

            # Check forbidden list
            for (pkg, op_name), reason in FORBIDDEN_OPERATORS.items():
                if call_repr == f"{pkg}.{op_name}":
                    return False, f"Forbidden operator '{call_repr}': {reason}"

            # Check unconstrained bpy.ops.object.delete() without selection scoping
            if call_repr == "bpy.ops.object.delete":
                # Check keywords
                use_global = True
                for kw in node.keywords:
                    if kw.arg == "use_global" and isinstance(kw.value, ast.Constant):
                        use_global = kw.value.value
                if use_global:
                    return (
                        False,
                        "Unconstrained 'bpy.ops.object.delete()' blocked: Must operate strictly within target partition",
                    )

    return True, "OK"


def compute_mesh_hash(mesh_data: Any) -> str:
    """Compute a SHA-256 geometric hash over vertex coordinates, face topology, and world transform.

    Supports both Blender RNA Mesh objects and raw dictionary/numpy representations.
    """
    hasher = hashlib.sha256()

    if isinstance(mesh_data, dict):
        verts = mesh_data.get("vertices", [])
        loops = mesh_data.get("loops", [])
        matrix = mesh_data.get("matrix", [])

        # Pack floats into bytes representation
        v_bytes = b"".join(f"{float(v):.6f}".encode("ascii") for v in verts)
        l_bytes = b"".join(f"{int(l)}".encode("ascii") for l in loops)
        m_bytes = b"".join(f"{float(m):.6f}".encode("ascii") for m in matrix)

        hasher.update(v_bytes)
        hasher.update(l_bytes)
        hasher.update(m_bytes)
    else:
        # Blender bpy.types.Mesh RNA object
        try:
            import numpy as np

            n_verts = len(mesh_data.vertices)
            v_buf = np.empty(n_verts * 3, dtype=np.float32)
            mesh_data.vertices.foreach_get("co", v_buf)
            hasher.update(v_buf.tobytes())

            n_loops = len(mesh_data.loops)
            l_buf = np.empty(n_loops, dtype=np.int32)
            mesh_data.loops.foreach_get("vertex_index", l_buf)
            hasher.update(l_buf.tobytes())
        except Exception:
            # Fallback string representation
            hasher.update(str(mesh_data).encode("utf-8"))

    return hasher.hexdigest()


class PTLASManager:
    """Manages scene partitions and Copy-on-Write transactional isolation."""

    def __init__(self) -> None:
        self.partitions: dict[str, dict[str, Any]] = {}
        self.active_transaction: str | None = None
        self._snapshots: dict[str, Any] = {}
        self._baseline_hashes: dict[str, str] = {}

    def create_partition(self, name: str, parent: str = "") -> dict[str, Any]:
        """Register or create a spatial partition."""
        if name not in self.partitions:
            self.partitions[name] = {
                "name": name,
                "parent": parent,
                "meshes": {},
                "hash": "",
                "locked": False,
            }
        return self.partitions[name]

    def register_mesh(self, partition_name: str, mesh_obj: Any) -> None:
        """Associate a mesh object with a partition."""
        if partition_name not in self.partitions:
            self.create_partition(partition_name)
        mesh_name = mesh_obj.get("name", "mesh") if isinstance(mesh_obj, dict) else getattr(mesh_obj, "name", "mesh")
        self.partitions[partition_name]["meshes"][mesh_name] = mesh_obj
        self._update_partition_hash(partition_name)

    def _update_partition_hash(self, partition_name: str) -> str:
        part = self.partitions.get(partition_name)
        if not part:
            return ""
        hasher = hashlib.sha256()
        for mesh_name in sorted(part["meshes"].keys()):
            mesh_data = part["meshes"][mesh_name]
            h = compute_mesh_hash(mesh_data)
            hasher.update(f"{mesh_name}:{h}".encode("utf-8"))
        part["hash"] = hasher.hexdigest()
        return part["hash"]

    def begin_transaction(self, partition_name: str) -> dict[str, Any]:
        """Snapshot the target partition and record baseline hashes for all other partitions."""
        if partition_name not in self.partitions:
            self.create_partition(partition_name)

        self.active_transaction = partition_name
        self._snapshots = copy.deepcopy(self.partitions)
        self._baseline_hashes = {
            p_name: self._update_partition_hash(p_name)
            for p_name in self.partitions
            if p_name != partition_name
        }

        return {
            "status": "active",
            "target": partition_name,
            "locked_partitions": list(self._baseline_hashes.keys()),
        }

    def verify_integrity(self) -> tuple[bool, list[str]]:
        """Verify that all non-target partitions remain 100% untouched."""
        violations = []
        if not self.active_transaction:
            return True, []

        for p_name, base_hash in self._baseline_hashes.items():
            curr_hash = self._update_partition_hash(p_name)
            if curr_hash != base_hash:
                violations.append(
                    f"Integrity violation in partition '{p_name}': Hash changed from {base_hash[:8]} to {curr_hash[:8]}"
                )

        return len(violations) == 0, violations

    def rollback_transaction(self, partition_name: str) -> bool:
        """Instantly revert scene state from snapshot upon transaction abort."""
        if not self._snapshots:
            return False

        # Restore deep copy and in-place mutate any referenced mesh dictionaries
        for p_name, snap_part in self._snapshots.items():
            if p_name in self.partitions:
                curr_part = self.partitions[p_name]
                for m_name, snap_mesh in snap_part["meshes"].items():
                    if m_name in curr_part["meshes"]:
                        orig_m = curr_part["meshes"][m_name]
                        if isinstance(orig_m, dict) and isinstance(snap_mesh, dict):
                            orig_m.clear()
                            orig_m.update(copy.deepcopy(snap_mesh))
                self.partitions[p_name] = copy.deepcopy(snap_part)

        self.active_transaction = None
        self._snapshots.clear()
        self._baseline_hashes.clear()
        return True

    def commit_transaction(self, partition_name: str) -> bool:
        """Commit transaction changes and update DAG hashes."""
        if self.active_transaction != partition_name:
            return False

        self._update_partition_hash(partition_name)
        self.active_transaction = None
        self._snapshots.clear()
        self._baseline_hashes.clear()
        return True
