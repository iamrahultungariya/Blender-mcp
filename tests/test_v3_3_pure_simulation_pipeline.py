"""Unit tests for Pure Simulation Pipeline & Assembly Settling.

Verifies cross-cutting support for simulation_mode ("parametric", "hybrid", "pure_simulation")
in soft goods tools, and multi-cloth assembly physics settling onto obstacle collision geometry.
"""

import pytest
from blender_mcp.soft_goods_engine import (
    create_pillow,
    create_curtains,
    create_duvet,
    create_blanket
)
from blender_mcp.cloth_engine import simulate_cloth_assembly


def test_soft_goods_simulation_mode_support():
    """Verify soft goods tools accept simulation_mode parameter and return it in result."""
    for mode in ["parametric", "hybrid", "pure_simulation"]:
        p_res = create_pillow(
            shape="classic",
            simulation_mode=mode,
            name=f"Pillow_{mode}"
        )
        assert p_res["success"] is True
        assert p_res["result"]["simulation_mode"] == mode

    d_res = create_duvet(
        bed_width=1.8,
        bed_length=2.0,
        simulation_mode="pure_simulation",
        name="Duvet_Sim"
    )
    assert d_res["success"] is True
    assert d_res["result"]["simulation_mode"] == "pure_simulation"

    c_res = create_curtains(
        width=1.5,
        height=2.4,
        simulation_mode="hybrid",
        name="Curtain_Sim"
    )
    assert c_res["success"] is True
    assert c_res["result"]["simulation_mode"] == "hybrid"

    b_res = create_blanket(
        width=1.4,
        length=1.8,
        simulation_mode="pure_simulation",
        name="Blanket_Sim"
    )
    assert b_res["success"] is True
    assert b_res["result"]["simulation_mode"] == "pure_simulation"


def test_simulate_cloth_assembly_headless():
    """Verify simulate_cloth_assembly executes multi-cloth settling and collision configuration."""
    res = simulate_cloth_assembly(
        assembly_root="Master_Bed_Root",
        target_obstacles=["Master_Bed_Frame", "Master_Bed_Mattress"],
        steps=50,
        apply_result=False
    )
    assert res["success"] is True
    result = res["result"]
    assert result["assembly_root"] == "Master_Bed_Root"
    assert "Master_Bed_Frame" in result["obstacles_configured"]
    assert "Master_Bed_Mattress" in result["obstacles_configured"]
    assert result["simulated_steps"] == 50
    assert result["applied_as_static_mesh"] is False
