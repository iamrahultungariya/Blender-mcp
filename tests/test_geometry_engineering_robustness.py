"""Tests verifying the Geometry Engineering engine and MCP robustness hardening."""
import numpy as np
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GEOM_SKILL_PATH = REPO_ROOT / "skills" / "blender-geometry-engineering" / "SKILL.md"
ADDON_PATH = REPO_ROOT / "addon.py"


def test_geometry_engineering_skill_exists_and_valid():
    """Verify blender-geometry-engineering skill is registered with complete gates."""
    assert GEOM_SKILL_PATH.exists(), "blender-geometry-engineering skill file missing"
    content = GEOM_SKILL_PATH.read_text(encoding="utf-8")
    assert "name: blender-geometry-engineering" in content
    assert "Core principle:" in content
    assert "G0 / positional continuity" in content
    assert "G1 / tangent continuity" in content
    assert "G2 / curvature continuity" in content
    assert "Gate G0" in content
    assert "Gate G6" in content


def test_catmull_rom_smooth_spline_lofting():
    """Verify that loft_spline_sections supports smooth Catmull-Rom longitudinal interpolation."""
    from blender_mcp.kernel.clas_tensor_shaper import loft_spline_sections

    K = 4
    res = 16
    sections = []
    for k in range(K):
        # Create circular cross-sections along Z axis
        theta = np.linspace(0, 2 * np.pi, res, endpoint=False)
        radius = 1.0 + 0.5 * np.sin(k)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = np.full(res, k * 5.0)
        sections.append(np.column_stack([x, y, z]))

    # Test with longitudinal_samples = 4
    verts, quads, normals = loft_spline_sections(
        sections, resolution=res, closed=True, longitudinal_samples=4
    )

    expected_sections = (K - 1) * 4 + 1  # 3 * 4 + 1 = 13 sections
    assert len(verts) == expected_sections * res
    assert len(quads) == (expected_sections - 1) * res
    assert np.isclose(verts[0, 2], 0.0)
    assert np.isclose(verts[-1, 2], 15.0)


def test_addon_contains_vectorized_curvature_and_budget_export():
    """Verify addon.py contains the vectorized np.add.at math and budget enforcement."""
    content = ADDON_PATH.read_text(encoding="utf-8")

    # Vectorized curvature check
    assert "np.add.at(deg" in content
    assert "np.add.at(nbr_sum" in content

    # Budget enforcement in export
    assert "eval_tris > budget" in content or "triangle_budget and" in content
    assert "auto_decimate" in content
    assert "longitudinal_samples" in content


def test_server_exposes_geometry_robustness_parameters():
    """Verify server.py exposes longitudinal_samples and auto_decimate."""
    from blender_mcp import server
    import inspect

    loft_sig = inspect.signature(server.clas_loft_splines)
    assert "longitudinal_samples" in loft_sig.parameters

    export_sig = inspect.signature(server.export_game_asset)
    assert "auto_decimate" in export_sig.parameters
