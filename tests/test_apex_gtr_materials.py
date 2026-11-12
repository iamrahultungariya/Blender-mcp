"""Unit tests for Apex GT-R PBR Automotive Shader Vault."""
import pytest
from scripts.generate_apex_gtr import GTR_MATERIAL_SPECS, setup_gtr_materials


def test_gtr_material_specs_completeness():
    """Verify all 9 required production materials are specified."""
    required_keys = [
        "MAT_GTR_Paint_Gunmetal",
        "MAT_GTR_Carbon_Satin",
        "MAT_GTR_Crimson_Accent",
        "MAT_GTR_Automotive_Glass",
        "MAT_GTR_Tire_Rubber",
        "MAT_GTR_Brake_Steel",
        "MAT_GTR_Caliper_Red",
        "MAT_GTR_LED_Emissive",
        "MAT_GTR_Tail_Emissive",
    ]
    for key in required_keys:
        assert key in GTR_MATERIAL_SPECS, f"Missing material spec: {key}"


def test_paint_material_spec():
    """Verify dark metallic gunmetal paint parameters."""
    paint = GTR_MATERIAL_SPECS["MAT_GTR_Paint_Gunmetal"]
    assert paint["metallic"] >= 0.90
    assert paint["roughness"] <= 0.30
    assert paint["clearcoat"] == 1.0


def test_glass_material_spec():
    """Verify automotive glass parameters."""
    glass = GTR_MATERIAL_SPECS["MAT_GTR_Automotive_Glass"]
    assert glass["transmission"] == 1.0
    assert pytest.approx(glass["ior"], 0.01) == 1.52


def test_emissive_material_specs():
    """Verify LED headlights and tail light emissive intensities."""
    led = GTR_MATERIAL_SPECS["MAT_GTR_LED_Emissive"]
    assert led["emission_strength"] >= 10.0
    tail = GTR_MATERIAL_SPECS["MAT_GTR_Tail_Emissive"]
    assert tail["emission_strength"] >= 10.0
