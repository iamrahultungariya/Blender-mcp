"""Verification test for Phase V3.3 & V4 FastMCP Tool Registration & Addon Sync.

Verifies that all Phase V3.3 (Nature Engine & Cloth Assembly Physics) and
Phase V4 (Layered Thinking & Independent Critic) tools are registered on FastMCP server
and their corresponding handlers exist in addon.py.
"""

import pytest
from blender_mcp import server


@pytest.mark.asyncio
async def test_v3_3_v4_tools_registered_on_server():
    """Verify that all V3.3 and V4 tools exist on the MCP server."""
    tools = await server.mcp.list_tools()
    tool_names = {t.name for t in tools}

    expected_tools = [
        # Phase V3.3: Nature & Cloth Assembly Physics
        "simulate_cloth_assembly",
        "create_grass_blade_cluster",
        "create_grass_field",
        "create_terrain_ground",
        "scatter_foliage",

        # Phase V4: Layered Thinking Architecture & Independent Critic
        "decompose_scene_intent",
        "validate_aesthetic_quality",
        "audit_production_readiness",
    ]

    for tool in expected_tools:
        assert tool in tool_names, f"Tool '{tool}' is not registered on FastMCP server."


def test_v3_3_v4_addon_parity():
    """Verify that addon.py defines handler methods and command routing for all V3.3 and V4 tools."""
    with open("addon.py", "r", encoding="utf-8") as f:
        content = f.read()

    expected_methods = [
        "simulate_cloth_assembly",
        "create_grass_blade_cluster",
        "create_grass_field",
        "create_terrain_ground",
        "scatter_foliage",
        "decompose_scene_intent",
        "validate_aesthetic_quality",
        "audit_production_readiness",
    ]

    for method in expected_methods:
        assert f'def {method}(' in content, f"addon.py missing definition for 'def {method}('"
        assert f'if cmd_type == "{method}":' in content, f"addon.py missing dispatcher for '{method}'"
