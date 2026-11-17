"""Verification test for Phase V3.1 FastMCP Tool Registration & Addon Sync.

Verifies that all Phase V3.1 tools are registered on FastMCP server and their
corresponding handlers exist in addon.py.
"""

import pytest
import inspect
from blender_mcp import server


@pytest.mark.asyncio
async def test_v3_1_tools_registered_on_server():
    """Verify that all V3.1 soft goods and edge conditioning tools exist on the MCP server."""
    tools = await server.mcp.list_tools()
    tool_names = {t.name for t in tools}

    expected_v3_1_tools = [
        "apply_edge_conditioning",
        "create_pillow",
        "create_curtains",
        "create_duvet",
        "create_blanket",
        "create_tufted_surface",
    ]

    for tool in expected_v3_1_tools:
        assert tool in tool_names, f"Tool '{tool}' is not registered on FastMCP server."


def test_v3_1_setup_cloth_physics_signature():
    """Verify setup_cloth_physics on server exposes pressure and gravity parameters."""
    sig = inspect.signature(server.setup_cloth_physics)
    params = sig.parameters
    assert "pressure" in params
    assert "pressure_factor" in params
    assert "gravity_scale" in params
    assert "shrink_factor" in params


def test_v3_1_addon_parity():
    """Verify that addon.py defines handler methods and command routing for all V3.1 tools."""
    with open("addon.py", "r", encoding="utf-8") as f:
        content = f.read()

    v3_1_methods = [
        "apply_edge_conditioning",
        "create_pillow",
        "create_curtains",
        "create_duvet",
        "create_blanket",
        "create_tufted_surface",
    ]

    for method in v3_1_methods:
        assert f'def {method}(' in content, f"addon.py missing definition for 'def {method}('"
        assert f'if cmd_type == "{method}":' in content, f"addon.py missing dispatcher for '{method}'"
