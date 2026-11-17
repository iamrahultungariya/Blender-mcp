import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_specular_clay_contract():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "def inspect_specular_clay_pass" in content
    assert '"inspect_specular_clay_pass":' in content or "cmd_type == \"inspect_specular_clay_pass\"" in content
    # Non-destructive requirement: must preserve and restore original materials
    assert "orig_materials" in content or "material_override" in content
    assert "STUDIO_CLAY" in content

def test_server_specular_clay_tool_exposed():
    from blender_mcp import server
    assert hasattr(server, "inspect_specular_clay_pass")

def test_specular_clay_material_preset():
    from blender_mcp.materials_preset import MaterialPresetVault
    spec = MaterialPresetVault.get_material_spec("specular_clay")
    assert spec["type"] == "specular_clay"
    assert spec["roughness"] <= 0.12
    assert "clearcoat" in spec
