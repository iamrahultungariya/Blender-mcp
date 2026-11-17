"""Unit tests for AAA Edge Conditioning Engine.

Verifies edge bevel weight assignment, crease tagging, Bevel modifier limit by weight,
and Weighted Normal modifier setup with keep_sharp=True (Pillar 3 of AAA furniture).
"""

import pytest
from blender_mcp.modifier_engine import apply_edge_conditioning, SUPPORTED_MODIFIERS


def test_edge_conditioning_headless():
    """Verify apply_edge_conditioning returns proper structured response in non-bpy test environment."""
    res = apply_edge_conditioning(
        object_name="Table_Top",
        mode="bevel_weight",
        angle_threshold_deg=35.0,
        bevel_weight=1.0,
        bevel_width=0.01,
        bevel_segments=2,
        add_weighted_normal=True,
        keep_sharp=True
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Table_Top"
    assert result["mode"] == "bevel_weight"
    assert result["bevel_weight"] == 1.0
    assert result["bevel_width"] == 0.01
    assert result["bevel_segments"] == 2
    assert result["weighted_normal_added"] is True
    assert result["keep_sharp"] is True


def test_edge_conditioning_crease_mode():
    """Verify edge conditioning in crease mode."""
    res = apply_edge_conditioning(
        object_name="Sofa_Base",
        mode="crease",
        crease_weight=0.8,
        add_weighted_normal=False
    )
    assert res["success"] is True
    assert res["result"]["mode"] == "crease"
    assert res["result"]["crease_weight"] == 0.8
    assert res["result"]["weighted_normal_added"] is False
