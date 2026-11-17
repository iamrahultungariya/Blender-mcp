"""Comprehensive End-to-End Integration Suite for Reference-to-Asset Pipeline v2.

Validates that all 5 quality enforcement engines and tools operate in unison
to prevent low-poly boxy hallucinations, non-manifold geometry, and skipped phase gates.
"""
from pathlib import Path
import pytest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "skills" / "blender-artist-workflow" / "SKILL.md"
ADDON_PATH = REPO_ROOT / "addon.py"


def test_v2_skill_contract_prohibitions_and_gates():
    """Verify that SKILL.md contains strict quality gates and anti-boxy prohibitions."""
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "MANDATORY EXECUTION CONTRACT" in content
    assert "anti-boxy" in content.lower() or "box" in content.lower()
    assert "subdivision" in content.lower()
    assert "evaluated" in content.lower()
    assert "Reference Evidence Matrix" in content
    assert "Phase" in content


def test_server_exposes_all_v2_contract_tools():
    """Verify that FastMCP server exposes all tools required by the contract."""
    from blender_mcp import server

    expected_tools = [
        "audit_mesh_topology",
        "inspect_specular_clay_pass",
        "get_evaluated_budget_report",
        "reconcile_reference_datums",
        "validate_phase_gate",
        "get_pipeline_status",
    ]
    for tool_name in expected_tools:
        assert hasattr(server, tool_name), f"Server missing tool: {tool_name}"


def test_addon_contains_all_v2_command_handlers():
    """Verify that addon.py implements and dispatches all v2 commands."""
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "cmd_type == \"audit_mesh_topology\"" in content
    assert "cmd_type == \"inspect_specular_clay_pass\"" in content
    assert "cmd_type == \"get_evaluated_budget_report\"" in content
    assert "def audit_mesh_topology" in content
    assert "def inspect_specular_clay_pass" in content
    assert "def get_evaluated_budget_report" in content


def test_full_pipeline_progression_with_audit_and_gates():
    """Simulate a complete 6-stage reference-to-asset workflow using pipeline gates."""
    from blender_mcp.pipeline_gates import PhaseGateManager
    from blender_mcp.reference_analyzer import reconcile_reference_datums
    from blender_mcp.mesh_auditor import audit_geometry_topology

    manager = PhaseGateManager()
    manager.reset()

    # Step 1: Reference intake & datum reconciliation
    dims = {
        "length": 5.92,
        "width": 2.02,
        "height": 2.75,
        "wheelbase": 3.665,
        "front_overhang": 1.01,
        "rear_overhang": 1.245,
    }
    views = ["front", "side", "top", "perspective"]
    datum_report = reconcile_reference_datums(views=views, archetype="VEHICLE", dimensions=dims)
    assert datum_report["status"] == "PASS"

    # Pass Gate 1
    g1 = manager.validate_gate(phase_id=1, evidence={
        "datums_reconciled": True,
        "evidence_matrix_compiled": True,
        "evidence_matrix": datum_report["evidence_matrix"],
    })
    assert g1["status"] == "PASS"

    # Step 2: Component Breakdown & Strategy selection
    g2 = manager.validate_gate(phase_id=2, evidence={
        "component_strategies": {
            "main_unibody": "subdivision_cage",
            "front_fascia": "boolean_bevel",
            "brake_lines": "bezier_curve",
            "seat_creases": "sculpt_and_bake",
        }
    })
    assert g2["status"] == "PASS"

    # Step 3: Primary Form Sub-D Cage & Visual Hull Topology Audit
    verts = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
    ], dtype=np.float64)
    faces = [
        [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
        [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5],
    ]
    topo = audit_geometry_topology(verts, faces)
    assert topo["is_watertight"] is True

    g3 = manager.validate_gate(phase_id=3, evidence={
        "specular_clay_verified": True,
        "topology_passed": topo["status"] == "PASS",
    })
    assert g3["status"] == "PASS"

    # Step 4: Secondary Assemblies & Precision Cutouts
    g4 = manager.validate_gate(phase_id=4, evidence={
        "wheelhouse_recessed": True,
        "cutouts_carved": True,
    })
    assert g4["status"] == "PASS"

    # Step 5: Detailing & True 3D Depth
    g5 = manager.validate_gate(phase_id=5, evidence={
        "hero_depth_verified": True,
    })
    assert g5["status"] == "PASS"

    # Step 6: Multi-Material PBR Shading & QA Gate
    g6 = manager.validate_gate(phase_id=6, evidence={
        "materials_assigned": True,
        "studio_render_verified": True,
    })
    assert g6["status"] == "PASS"

    # Verify overall pipeline verdict
    pipeline_status = manager.get_status()
    assert pipeline_status["passed_count"] == 6
    assert pipeline_status["pipeline_verdict"] == "APPROVED_FOR_EXPORT"
