import pytest
from luxury_bedroom.assembler import assemble_luxury_bedroom_reference


def test_full_reference_suite_assembly():
    result = assemble_luxury_bedroom_reference(dev_fast_mode=True)
    assert result["status"] == "SUCCESS"
    assert result["phase_gate_status"] == "PASS"
    assert result["total_prefabs"] == 9
    assert result["blueprint"]["archetype"] == "BEDROOM"
    assert "HeroBedBuilder" in result["prefabs_built"]
    assert "NightstandsBuilder" in result["prefabs_built"]
    assert "OttomanBenchBuilder" in result["prefabs_built"]
    assert "LoungeCornerBuilder" in result["prefabs_built"]
    assert "MediaWallBuilder" in result["prefabs_built"]
    assert "WardrobeBuilder" in result["prefabs_built"]
    assert "WindowCurtainsBuilder" in result["prefabs_built"]
    assert "RoomEnvelopeBuilder" in result["prefabs_built"]
    assert "ChandelierBuilder" in result["prefabs_built"]
    assert result["mesh_face_count"] > 1000
