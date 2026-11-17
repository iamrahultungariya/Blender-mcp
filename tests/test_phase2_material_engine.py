import pytest
from blender_mcp.material_engine import (
    assign_pbr_material,
    inspect_material_nodes,
    create_procedural_shader,
    modify_material_property,
    validate_material_setup,
    PRINCIPLED_SOCKET_ALIASES
)


def test_material_presets_list_and_aliases():
    assert "base_color" in PRINCIPLED_SOCKET_ALIASES
    assert "metallic" in PRINCIPLED_SOCKET_ALIASES
    assert "roughness" in PRINCIPLED_SOCKET_ALIASES
    assert "clearcoat" in PRINCIPLED_SOCKET_ALIASES
    assert "transmission" in PRINCIPLED_SOCKET_ALIASES


def test_create_procedural_shader_all_15_presets():
    presets = [
        "wood", "brushed_metal", "polished_metal", "concrete", "marble",
        "leather", "fabric_weave", "plastic", "ceramic", "rubber",
        "painted_wall", "aged_wood", "rusted_metal", "stone", "glass"
    ]
    for p in presets:
        res = create_procedural_shader(material_name=f"M_Test_{p}", preset=p, scale=1.5)
        assert res["success"] is True, f"Preset {p} failed to generate"
        assert res["result"]["preset"] == p
        assert res["tool"] == "create_procedural_shader"


def test_create_procedural_shader_invalid_preset():
    res = create_procedural_shader(material_name="M_Invalid", preset="non_existent_preset")
    assert res["success"] is False
    assert len(res["errors"]) > 0


def test_assign_pbr_material_unit_contract():
    res = assign_pbr_material(
        object_name="Cube",
        material_name="M_Standard_PBR",
        base_color=(0.9, 0.2, 0.2, 1.0),
        metallic=0.8,
        roughness=0.25
    )
    assert res["success"] is True
    assert res["tool"] == "assign_pbr_material"


def test_inspect_and_validate_material_contract():
    inspect_res = inspect_material_nodes("M_Standard_PBR")
    assert inspect_res["success"] is True
    assert inspect_res["tool"] == "inspect_material_nodes"

    val_res = validate_material_setup("M_Standard_PBR")
    assert val_res["success"] is True
    assert val_res["tool"] == "validate_material_setup"
