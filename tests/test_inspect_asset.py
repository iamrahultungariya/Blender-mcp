import pytest
import inspect
from blender_mcp import server

def test_inspect_asset_tool_registered():
    assert hasattr(server, "inspect_asset")
    sig = inspect.signature(server.inspect_asset)
    params = sig.parameters
    assert "target" in params
    assert "shading" in params
    assert "max_size" in params
    assert params["shading"].default == "rendered"
    assert params["max_size"].default == 1024

def test_inspect_asset_docstring():
    doc = server.inspect_asset.__doc__
    assert doc is not None
    assert "contact sheet" in doc.lower() or "4-quadrant" in doc.lower() or "angles" in doc.lower()
