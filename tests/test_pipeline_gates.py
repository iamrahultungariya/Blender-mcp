import pytest

def test_pipeline_gates_module_exists():
    from blender_mcp import pipeline_gates
    assert hasattr(pipeline_gates, "PhaseGateManager")
    assert hasattr(pipeline_gates, "validate_phase_gate")
    assert hasattr(pipeline_gates, "get_pipeline_status")

def test_phase_gate_sequential_enforcement():
    from blender_mcp.pipeline_gates import PhaseGateManager

    manager = PhaseGateManager()
    manager.reset()

    # Attempting Phase 3 before Phase 1 and 2 pass must be BLOCKED
    res = manager.validate_gate(phase_id=3, evidence={"specular_clay_verified": True})
    assert res["status"] == "BLOCKED"
    assert "Prerequisite Phase" in res["error"]

def test_phase_gate_full_progression():
    from blender_mcp.pipeline_gates import PhaseGateManager

    manager = PhaseGateManager()
    manager.reset()

    # Phase 1: Reference Intake
    p1 = manager.validate_gate(phase_id=1, evidence={"datums_reconciled": True, "evidence_matrix_compiled": True})
    assert p1["status"] == "PASS"

    # Phase 2: Component Breakdown
    p2 = manager.validate_gate(phase_id=2, evidence={"component_strategies": {"chassis": "subdivision_cage", "fascia": "boolean_bevel"}})
    assert p2["status"] == "PASS"

    # Phase 3: Primary Form Sub-D Cage
    p3 = manager.validate_gate(phase_id=3, evidence={"specular_clay_verified": True, "topology_passed": True})
    assert p3["status"] == "PASS"

    status = manager.get_status()
    assert status["phases"][1]["status"] == "PASS"
    assert status["phases"][2]["status"] == "PASS"
    assert status["phases"][3]["status"] == "PASS"
    assert status["phases"][4]["status"] == "NOT_STARTED"

def test_server_phase_gate_tool_exposed():
    from blender_mcp import server
    assert hasattr(server, "validate_phase_gate")
    assert hasattr(server, "get_pipeline_status")
