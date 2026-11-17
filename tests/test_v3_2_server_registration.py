"""Verification test for Phase V3.2 FastMCP Tool Registration & Addon Sync.

Verifies that all Phase V3.2 furniture tools are registered on FastMCP server and their
corresponding handlers exist in addon.py.
"""

import pytest
from blender_mcp import server


@pytest.mark.asyncio
async def test_v3_2_tools_registered_on_server():
    """Verify that all V3.2 furniture tools exist on the MCP server."""
    tools = await server.mcp.list_tools()
    tool_names = {t.name for t in tools}

    expected_v3_2_tools = [
        "create_bed",
        "create_sofa",
        "create_chair",
        "create_table",
        "create_wardrobe",
        "create_door_assembly",
    ]

    for tool in expected_v3_2_tools:
        assert tool in tool_names, f"Tool '{tool}' is not registered on FastMCP server."


def test_v3_2_addon_parity():
    """Verify that addon.py defines handler methods and command routing for all V3.2 tools."""
    with open("addon.py", "r", encoding="utf-8") as f:
        content = f.read()

    v3_2_methods = [
        "create_bed",
        "create_sofa",
        "create_chair",
        "create_table",
        "create_wardrobe",
        "create_door_assembly",
    ]

    for method in v3_2_methods:
        assert f'def {method}(' in content, f"addon.py missing definition for 'def {method}('"
        assert f'if cmd_type == "{method}":' in content, f"addon.py missing dispatcher for '{method}'"
