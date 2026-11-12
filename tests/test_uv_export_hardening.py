"""Tests for Task 3 & 4: apply_uv_unwrap tool and Iron Law 4 UV enforcement in export_game_asset."""
import inspect
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"
BUNDLED_ADDON_PATH = REPO_ROOT / "src" / "blender_mcp" / "bundled" / "addon.py"


def test_server_exposes_apply_uv_unwrap_tool():
    """Verify FastMCP server exposes apply_uv_unwrap tool with proper parameters."""
    from blender_mcp import server

    assert hasattr(server, "apply_uv_unwrap"), "server.py must expose apply_uv_unwrap tool"
    sig = inspect.signature(server.apply_uv_unwrap)
    assert "target_object" in sig.parameters
    assert "angle_limit_deg" in sig.parameters
    assert "island_margin" in sig.parameters


def test_server_export_game_asset_exposes_uv_parameters():
    """Verify export_game_asset in server.py exposes auto_uv and enforce_uv parameters."""
    from blender_mcp import server

    sig = inspect.signature(server.export_game_asset)
    assert "auto_uv" in sig.parameters
    assert "enforce_uv" in sig.parameters


def test_addon_contains_apply_uv_unwrap_handler():
    """Verify addon.py contains the apply_uv_unwrap command dispatcher and method."""
    content = ADDON_PATH.read_text(encoding="utf-8")
    assert 'cmd_type == "apply_uv_unwrap"' in content
    assert "def apply_uv_unwrap(" in content


def test_export_game_asset_isolates_selection_and_validates_uv():
    """Verify export_game_asset in addon.py deselects other objects and handles UV validation."""
    content = ADDON_PATH.read_text(encoding="utf-8")
    # Verify selection isolation
    assert "o.select_set(False)" in content or "select_all(action='DESELECT')" in content
    # Verify UV status reporting
    assert "uv_status" in content
    assert "auto_uv" in content
    assert "enforce_uv" in content
