import ast
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PATH = REPO_ROOT / "addon.py"
BUNDLED_PATH = REPO_ROOT / "src" / "blender_mcp" / "bundled" / "addon.py"

def test_addon_syntax_valid():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        code = f.read()
    # Must compile cleanly as valid Python
    tree = ast.parse(code)
    assert tree is not None

def test_addon_contains_dxr_commands():
    with open(ADDON_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    expected_command_handlers = [
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
    for cmd in expected_command_handlers:
        assert f'cmd_type == "{cmd}"' in content or f"cmd_type == '{cmd}'" in content, f"Command {cmd} missing from addon.py dispatch table"

def test_bundled_addon_in_sync():
    with open(ADDON_PATH, "rb") as f1, open(BUNDLED_PATH, "rb") as f2:
        assert f1.read() == f2.read(), "bundled/addon.py must be 100% identical to root addon.py"
