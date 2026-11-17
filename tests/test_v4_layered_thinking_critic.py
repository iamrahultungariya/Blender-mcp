"""Unit tests for Phase V4 Layered Thinking Architecture & Independent Critic Engine.

Verifies scene intent decomposition into execution DAGs with simulation mode decisions,
aesthetic quality scorecards, and production readiness gates.
"""

import pytest
from blender_mcp.critic_engine import (
    decompose_scene_intent,
    validate_aesthetic_quality,
    audit_production_readiness
)


def test_decompose_scene_intent_with_simulation_decision():
    """Verify decompose_scene_intent parses prompt and provides simulation mode recommendation."""
    prompt = "Create a luxury master bedroom with tufted king bed, pillows, silk curtains, and warm sunlight"
    res = decompose_scene_intent(user_prompt=prompt, target_style="photorealistic")
    assert res["success"] is True
    result = res["result"]
    assert "execution_stages" in result
    assert len(result["execution_stages"]) >= 4
    assert "simulation_mode_recommendation" in result
    sim_rec = result["simulation_mode_recommendation"]
    assert "recommended_mode" in sim_rec
    assert "user_prompt_required" in sim_rec
    assert "options" in sim_rec
    assert "pure_simulation" in sim_rec["options"]
    assert "hybrid" in sim_rec["options"]


def test_validate_aesthetic_quality_scorecard():
    """Verify validate_aesthetic_quality generates 0-100 score and critique checklist."""
    res = validate_aesthetic_quality(root_object="Master_Bed_Root", scene_check=True)
    assert res["success"] is True
    result = res["result"]
    assert "aesthetic_score" in result
    assert 0 <= result["aesthetic_score"] <= 100
    assert "verdict" in result
    assert "criteria_breakdown" in result
    breakdown = result["criteria_breakdown"]
    assert "topology_quad_flow" in breakdown
    assert "edge_conditioning" in breakdown
    assert "soft_goods_crown" in breakdown
    assert "material_pbr_completeness" in breakdown


def test_audit_production_readiness_gate():
    """Verify audit_production_readiness checks transforms, scale, and manifold geometry."""
    res = audit_production_readiness(asset_name="Dining_Table", target_engine="blender_cycles")
    assert res["success"] is True
    result = res["result"]
    assert result["asset_name"] == "Dining_Table"
    assert "is_production_ready" in result
    assert "checks" in result
