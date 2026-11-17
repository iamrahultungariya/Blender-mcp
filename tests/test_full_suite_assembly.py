import pytest
from luxury_bedroom.assembler import assemble_luxury_bedroom


def test_full_assembly_pipeline():
    result = assemble_luxury_bedroom(dev_fast_mode=True)
    assert result["status"] == "SUCCESS"
    assert result["phase_gate_status"] == "PASS"
    assert result["total_components"] >= 6
    assert result["mesh_face_count"] > 1000
    assert result["blueprint"]["archetype"] == "BEDROOM"
    assert result["blueprint"]["domain"] == "INTERIOR_SPACES"
    assert "components" in result
    assert "bed_platform" in result["components"]
    assert "fluted_headboard" in result["components"]
    assert "pillows_cluster" in result["components"]
    assert "chadar_duvet" in result["components"]
    assert "floating_nightstands" in result["components"]
    assert "pendant_lighting" in result["components"]
    assert "acoustic_slat_wall" in result["components"]
    assert "room_envelope" in result["components"]
