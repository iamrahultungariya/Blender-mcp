import pytest
from blender_mcp.kernel.ptlas_partition_manager import (
    audit_script_ast,
    compute_mesh_hash,
    PTLASManager,
)

def test_ast_audit_safe_code():
    safe_code = """
import bpy
obj = bpy.data.objects.get("Room_ICU_Wall")
if obj:
    obj.location.x += 1.0
"""
    valid, reason = audit_script_ast(safe_code, allowed_partition="Room_ICU")
    assert valid is True
    assert reason == "OK"

def test_ast_audit_blocks_global_select_all_delete():
    destructive_code = """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
"""
    valid, reason = audit_script_ast(destructive_code, allowed_partition="Room_ICU")
    assert valid is False
    assert "select_all" in reason.lower() or "delete" in reason.lower()

def test_ast_audit_blocks_factory_reset():
    code = "bpy.ops.wm.read_factory_settings()"
    valid, reason = audit_script_ast(code, allowed_partition="Chassis")
    assert valid is False
    assert "read_factory_settings" in reason.lower()

def test_compute_mesh_hash_consistency():
    verts = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    loops = [0, 1, 2]
    matrix = [1.0 if i == j else 0.0 for i in range(4) for j in range(4)]
    
    hash1 = compute_mesh_hash({"vertices": verts, "loops": loops, "matrix": matrix})
    hash2 = compute_mesh_hash({"vertices": verts, "loops": loops, "matrix": matrix})
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 hex string

    # Slight perturbation should drastically change hash
    verts_mod = list(verts)
    verts_mod[0] += 0.0001
    hash3 = compute_mesh_hash({"vertices": verts_mod, "loops": loops, "matrix": matrix})
    assert hash1 != hash3

def test_ptlas_manager_transactions():
    manager = PTLASManager()
    manager.create_partition("Room_A")
    manager.create_partition("Room_B")
    
    # Register mock meshes
    mesh_a = {"name": "Bed_A", "vertices": [0.0, 0.0, 0.0], "loops": [0], "matrix": [1.0]*16}
    mesh_b = {"name": "Desk_B", "vertices": [5.0, 0.0, 0.0], "loops": [0], "matrix": [1.0]*16}
    manager.register_mesh("Room_A", mesh_a)
    manager.register_mesh("Room_B", mesh_b)
    
    # Begin transaction on Room_A
    tx = manager.begin_transaction("Room_A")
    assert tx["status"] == "active"
    
    # Mutate Room_A
    mesh_a["vertices"][0] = 1.0
    
    # Room_B is untouched, integrity check should pass
    ok, violations = manager.verify_integrity()
    assert ok is True
    assert len(violations) == 0
    
    # Illegal mutation in Room_B during Room_A transaction
    mesh_b["vertices"][0] = 99.0
    ok, violations = manager.verify_integrity()
    assert ok is False
    assert any("Room_B" in v for v in violations)
    
    # Rollback restores state
    rolled_back = manager.rollback_transaction("Room_A")
    assert rolled_back is True
    assert mesh_b["vertices"][0] == 5.0
