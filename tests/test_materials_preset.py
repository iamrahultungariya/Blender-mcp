import pytest

def test_materials_preset_imports():
    from blender_mcp import materials_preset
    assert hasattr(materials_preset, "setup_car_paint_material")
    assert hasattr(materials_preset, "setup_textured_plastic_material")
    assert hasattr(materials_preset, "setup_automotive_glass_material")
    assert hasattr(materials_preset, "setup_emergency_emissive_material")
    assert hasattr(materials_preset, "setup_radial_tire_material")
    assert hasattr(materials_preset, "setup_chrome_trim_material")
    assert hasattr(materials_preset, "MaterialPresetVault")

def test_material_specs_dictionary():
    from blender_mcp.materials_preset import MaterialPresetVault
    vault = MaterialPresetVault()
    spec = vault.get_material_spec("car_paint", color=(0.9, 0.1, 0.1, 1.0))
    assert spec["type"] == "car_paint"
    assert spec["clearcoat"] >= 0.8
    assert "base_color" in spec

def test_emissive_spec():
    from blender_mcp.materials_preset import MaterialPresetVault
    vault = MaterialPresetVault()
    spec = vault.get_material_spec("emergency_emissive", color=(1.0, 0.0, 0.0, 1.0), strength=45.0)
    assert spec["type"] == "emergency_emissive"
    assert spec["emission_strength"] == 45.0
