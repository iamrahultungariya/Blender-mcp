import pytest
from mcp.server.fastmcp import FastMCP
from blender_mcp.server import mcp

def test_dxr_tools_registered():
    # Check that new DXR kernel tools are registered on the FastMCP instance
    tool_names = list(mcp._tool_manager._tools.keys())
    
    expected_dxr_tools = [
        "ptlas_create_partition",
        "ptlas_mutate_partition",
        "ptlas_verify_integrity",
        "sdf_space_carve",
        "clas_eval_bezier_patch",
        "clas_loft_splines",
        "clas_boolean_carve",
        "gbuffer_quad_capture",
        "gbuffer_project_uv",
        "pbr_compile_curvature_ao",
        "export_game_asset",
    ]
    for expected in expected_dxr_tools:
        assert expected in tool_names, f"Tool {expected} missing from registered tools"

def test_legacy_tools_preserved():
    tool_names = list(mcp._tool_manager._tools.keys())
    for legacy in ["execute_blender_code", "get_scene_info", "search_assets", "import_asset"]:
        assert legacy in tool_names, f"Legacy tool {legacy} must be preserved"
