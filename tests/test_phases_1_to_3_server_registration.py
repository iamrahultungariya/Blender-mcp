import pytest
from blender_mcp.server import mcp


def test_phases_1_to_3_tools_registered():
    """Verify that all Phase 1-3 MCP tools are registered on the FastMCP instance."""
    tools = list(mcp._tool_manager._tools.keys())

    expected_tools = [
        # Phase 1: Checkpoint & Safety Engine
        "create_scene_checkpoint",
        "restore_scene_checkpoint",
        "list_scene_checkpoints",
        "delete_scene_checkpoint",

        # Phase 2: PBR Material & Procedural Shader Engine
        "assign_pbr_material",
        "inspect_material_nodes",
        "create_procedural_shader",
        "modify_material_property",
        "validate_material_setup",

        # Phase 3: Cinematic Studio Lighting & HDRI Engine
        "setup_studio_lighting",
        "setup_environment_hdri",
        "inspect_lighting_setup",
        "adjust_lighting_for_object",
    ]

    for tool in expected_tools:
        assert tool in tools, f"Tool '{tool}' is not registered on FastMCP server"


def test_existing_tools_preserved():
    """Verify that existing tools remain registered and were not broken."""
    tools = list(mcp._tool_manager._tools.keys())
    existing = [
        "execute_blender_code",
        "get_scene_info",
        "look",
        "inspect_asset",
        "ptlas_create_partition",
        "clas_loft_splines",
        "export_game_asset",
        "create_cushioned_profile",
        "create_architectural_wall",
        "create_profile_sweep_molding",
        "audit_mesh_topology",
        "validate_phase_gate",
    ]
    for tool in existing:
        assert tool in tools, f"Existing tool '{tool}' must remain registered"
