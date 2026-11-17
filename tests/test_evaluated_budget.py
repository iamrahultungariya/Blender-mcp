import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"

def test_addon_evaluated_budget_contract():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert "def get_evaluated_budget_report" in content
    assert '"get_evaluated_budget_report":' in content or "cmd_type == \"get_evaluated_budget_report\"" in content
    assert "evaluated_depsgraph_get" in content
    assert "evaluated_tris" in content

def test_server_evaluated_budget_tool_exposed():
    from blender_mcp import server
    assert hasattr(server, "get_evaluated_budget_report")
