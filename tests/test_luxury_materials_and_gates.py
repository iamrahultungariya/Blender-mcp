import pytest
from luxury_bedroom.core.materials import MaterialLibrary
from blender_mcp.pipeline_gates import validate_phase_gate
from blender_mcp.spatial_thinking import SpatialThinkingEngine


def test_spatial_blueprint_resolution():
    engine = SpatialThinkingEngine()
    bp = engine.generate_spatial_blueprint("luxury bedroom with king bed and pillows")
    assert bp["domain"] == "INTERIOR_SPACES"
    assert bp["archetype"] == "BEDROOM"
    assert bp["dimensions"]["length"] >= 4.0
    assert bp["anti_boxy_mandate"]["zero_unfilleted_primitives"] is True


def test_phase_gate_g2_bedroom_strategies():
    strategies = {
        "bed_frame": "boolean_bevel",
        "fluted_headboard": "subdivision_cage",
        "mattress_cushion": "subdivision_cage",
        "pillows_layered": "subdivision_cage",
        "chadar_duvet": "subdivision_cage",
        "nightstands": "boolean_bevel",
        "pendant_lighting": "bezier_curve",
        "room_envelope": "boolean_bevel",
    }
    result = validate_phase_gate(phase_id=2, evidence={"component_strategies": strategies})
    assert result["status"] == "PASS"


def test_material_library_definitions():
    mat_lib = MaterialLibrary()
    keys = mat_lib.get_material_names()
    expected = [
        "WALNUT_WOOD",
        "UPHOLSTERY_VELVET",
        "LINEN_WHITE",
        "LINEN_ACCENT",
        "BRUSHED_BRASS",
        "PARQUET_OAK",
        "WARM_PLASTER",
        "LED_WARM_COVE",
    ]
    for k in expected:
        assert k in keys
    # Verify index mapping
    for k in expected:
        idx = mat_lib.get_index(k)
        assert isinstance(idx, int)
        assert idx >= 0
