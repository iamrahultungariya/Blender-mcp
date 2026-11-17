import pytest
from blender_mcp.lighting_engine import (
    setup_studio_lighting,
    setup_environment_hdri,
    inspect_lighting_setup,
    adjust_lighting_for_object,
    _kelvin_to_rgb
)


def test_kelvin_to_rgb_ranges():
    # Warm tungsten (3200K) -> higher red than blue
    r, g, b = _kelvin_to_rgb(3200)
    assert r > b
    assert r == 1.0

    # Cool daylight (7500K) -> noticeable blue component
    r2, g2, b2 = _kelvin_to_rgb(7500)
    assert b2 > 0.8


def test_setup_studio_lighting_all_10_presets():
    presets = [
        "three_point", "dramatic_rim", "soft_interior", "product_clean",
        "cinematic", "architectural", "horror_atmosphere", "daylight",
        "night_scene", "automotive_studio"
    ]
    for p in presets:
        res = setup_studio_lighting(preset=p, target_object=None)
        assert res["success"] is True, f"Preset {p} failed to setup"
        assert res["result"]["preset"] == p
        assert res["tool"] == "setup_studio_lighting"


def test_setup_studio_lighting_invalid_preset():
    res = setup_studio_lighting(preset="bogus_preset")
    assert res["success"] is False
    assert len(res["errors"]) > 0


def test_setup_environment_hdri_contract():
    res = setup_environment_hdri(hdri_path_or_preset="studio", strength=1.2, rotation=45.0)
    assert res["success"] is True
    assert res["tool"] == "setup_environment_hdri"
    assert res["result"]["strength"] == 1.2
    assert res["result"]["rotation"] == 45.0


def test_inspect_and_adjust_lighting_contract():
    insp = inspect_lighting_setup()
    assert insp["success"] is True
    assert insp["tool"] == "inspect_lighting_setup"

    adj = adjust_lighting_for_object("Cube")
    assert adj["success"] is True
    assert adj["tool"] == "adjust_lighting_for_object"
