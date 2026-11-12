"""Tests for Task 5 & 6: Pipeline Gate State Persistence and G0-G6 String Aliases."""
import json
from pathlib import Path
import pytest
from blender_mcp.pipeline_gates import (
    PhaseGateManager,
    validate_phase_gate,
    get_pipeline_status,
    reset_pipeline,
)


def test_gate_string_aliases_resolution():
    """Verify validate_gate resolves 'G1'-'G6', 'G0', and 'Phase N' aliases."""
    manager = PhaseGateManager(state_file=None)
    manager.reset()

    # Pass Gate 1 via string alias 'G1'
    res1 = manager.validate_gate("G1", evidence={"datums_reconciled": True, "evidence_matrix_compiled": True})
    assert res1["status"] == "PASS", f"G1 failed: {res1}"
    assert res1["phase_id"] == 1

    # Pass Gate 2 via string alias 'G2'
    res2 = manager.validate_gate("G2", evidence={"component_strategies": {"body": "subdivision_cage"}})
    assert res2["status"] == "PASS", f"G2 failed: {res2}"
    assert res2["phase_id"] == 2

    # Pass Gate 3 via string alias 'Phase 3'
    res3 = manager.validate_gate("Phase 3", evidence={"specular_clay_verified": True, "topology_passed": True})
    assert res3["status"] == "PASS", f"Phase 3 failed: {res3}"
    assert res3["phase_id"] == 3

    # Pass Gate 4 via 'G4'
    res4 = manager.validate_gate("G4", evidence={"wheelhouse_recessed": True, "cutouts_carved": True})
    assert res4["status"] == "PASS", f"G4 failed: {res4}"
    assert res4["phase_id"] == 4


def test_top_level_validate_phase_gate_supports_aliases():
    """Verify module-level validate_phase_gate accepts string aliases."""
    reset_pipeline()
    res = validate_phase_gate("G1", evidence={"datums_reconciled": True, "evidence_matrix_compiled": True})
    assert res["status"] == "PASS"
    assert res["phase_id"] == 1


def test_pipeline_state_disk_persistence(tmp_path):
    """Verify PhaseGateManager saves and restores state across separate instances."""
    state_file = tmp_path / ".pipeline_state.json"

    # Instance 1: advance phase 1
    m1 = PhaseGateManager(state_file=state_file)
    m1.reset()
    res = m1.validate_gate(1, evidence={"datums_reconciled": True, "evidence_matrix_compiled": True})
    assert res["status"] == "PASS"
    assert state_file.exists(), "State file must be written to disk on phase change"

    # Verify JSON structure
    saved_data = json.loads(state_file.read_text(encoding="utf-8"))
    assert saved_data["phases"]["1"]["status"] == "PASS"

    # Instance 2: new object pointing to same state file
    m2 = PhaseGateManager(state_file=state_file)
    assert m2.phases[1]["status"] == "PASS", "Instance 2 must restore Phase 1 PASS status from disk"

    # Instance 2 can immediately validate Gate 2 without re-doing Gate 1
    res2 = m2.validate_gate(2, evidence={"component_strategies": {"body": "subdivision_cage"}})
    assert res2["status"] == "PASS", f"Phase 2 should succeed because Phase 1 was loaded: {res2}"
