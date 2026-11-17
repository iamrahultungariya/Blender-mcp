import pytest
from blender_mcp.camera_engine import (
    frame_camera_to_object,
    setup_camera_dof,
    create_turntable_camera,
    inspect_camera_setup,
    _compute_framing_distance
)


def test_compute_framing_distance_math():
    # 50mm lens, 36mm sensor, radius 1.0m, margin 1.0
    dist = _compute_framing_distance(radius=1.0, lens_mm=50.0, sensor_width=36.0, margin=1.0)
    assert dist > 1.5
    assert dist < 6.0


def test_frame_camera_all_angles():
    angles = [
        "front", "back", "left", "right", "top", "bottom",
        "three_quarters", "isometric", "hero", "low_angle", "high_angle"
    ]
    for a in angles:
        res = frame_camera_to_object("Cube", lens_mm=85.0, angle=a, composition="rule_of_thirds")
        assert res["success"] is True, f"Angle {a} failed"
        assert res["result"]["angle"] == a
        assert res["tool"] == "frame_camera_to_object"


def test_frame_camera_invalid_angle():
    res = frame_camera_to_object("Cube", angle="invalid_perspective")
    assert res["success"] is False
    assert len(res["errors"]) > 0


def test_setup_camera_dof_contract():
    res = setup_camera_dof(target_object="Cube", f_stop=1.8, enabled=True)
    assert res["success"] is True
    assert res["tool"] == "setup_camera_dof"


def test_create_turntable_and_inspect_camera():
    tt = create_turntable_camera("Cube", frames=180, height=2.0)
    assert tt["success"] is True
    assert tt["result"]["total_frames"] == 180

    insp = inspect_camera_setup()
    assert insp["success"] is True
    assert insp["tool"] == "inspect_camera_setup"
