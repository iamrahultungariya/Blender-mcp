import pytest
from blender_mcp.modifier_engine import (
    apply_modifier_stack,
    inspect_modifier_stack,
    freeze_modifiers,
    SUPPORTED_MODIFIERS
)
from blender_mcp.rigging_engine import (
    setup_vehicle_rig,
    setup_hinge_constraint,
    setup_mechanical_pivot,
    inspect_rig_hierarchy
)


def test_supported_modifiers_list():
    assert "BEVEL" in SUPPORTED_MODIFIERS
    assert "SUBSURF" in SUPPORTED_MODIFIERS
    assert "SOLIDIFY" in SUPPORTED_MODIFIERS
    assert "DECIMATE" in SUPPORTED_MODIFIERS


def test_apply_modifier_stack_contract():
    stack = [
        {"type": "BEVEL", "width": 0.02, "segments": 3},
        {"type": "SUBSURF", "levels": 2}
    ]
    res = apply_modifier_stack("Cube", stack, apply_immediately=False)
    assert res["success"] is True
    assert res["tool"] == "apply_modifier_stack"
    assert res["result"]["modifiers_configured"] == 2


def test_apply_modifier_stack_unsupported():
    res = apply_modifier_stack("Cube", [{"type": "INVALID_MOD"}])
    assert res["success"] is False
    assert len(res["errors"]) > 0


def test_setup_vehicle_rig_contract():
    wheels = ["Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR"]
    res = setup_vehicle_rig("Chassis", wheels, steering_wheels=["Wheel_FL", "Wheel_FR"])
    assert res["success"] is True
    assert res["tool"] == "setup_vehicle_rig"
    assert res["result"]["chassis"] == "Chassis"
    assert len(res["result"]["wheels"]) == 4


def test_setup_hinge_constraint_contract():
    res = setup_hinge_constraint("Door_Panel", "Door_Frame", axis="Z", limits=[-90.0, 0.0])
    assert res["success"] is True
    assert res["tool"] == "setup_hinge_constraint"
    assert res["result"]["axis"] == "Z"
