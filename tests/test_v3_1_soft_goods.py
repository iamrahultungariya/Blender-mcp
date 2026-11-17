"""Unit tests for Phase V3.1 Soft Goods Engine.

Verifies parametric generation of pillows (classic, diamond, bolster, square),
curtains (pleated accordion drape), baffle-box duvets, accent throw blankets,
and chesterfield tufted surfaces.
"""

import pytest
from blender_mcp.soft_goods_engine import (
    create_pillow,
    create_curtains,
    create_duvet,
    create_blanket,
    create_tufted_surface,
    PILLOW_SHAPES
)


def test_create_pillow_shapes():
    """Verify create_pillow generates valid quad mesh for all supported shapes."""
    for shape in ["classic", "diamond", "bolster", "square"]:
        res = create_pillow(
            shape=shape,
            width=0.6,
            length=0.4,
            thickness=0.18,
            puffiness=1.2,
            seam_piping=True,
            name=f"Pillow_{shape}"
        )
        assert res["success"] is True
        result = res["result"]
        assert result["shape"] == shape
        assert result["object_name"] == f"Pillow_{shape}"
        assert result["vertex_count"] > 10
        assert result["face_count"] > 5


def test_create_pillow_tufted():
    """Verify create_pillow with tufting enabled."""
    res = create_pillow(
        shape="classic",
        width=0.5,
        length=0.5,
        thickness=0.2,
        tufting=True,
        name="Tufted_Pillow"
    )
    assert res["success"] is True
    assert res["result"]["tufting"] is True


def test_create_curtains_pleats():
    """Verify create_curtains generates pleated drapery with top pin group and bunching."""
    res = create_curtains(
        width=1.6,
        height=2.5,
        pleat_count=10,
        bunch_factor=0.55,
        rod_offset=0.06,
        name="Sheer_Curtains"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Sheer_Curtains"
    assert result["pleat_count"] == 10
    assert result["bunch_factor"] == 0.55
    assert result["has_pin_group"] is True
    assert result["vertex_count"] > 20


def test_create_duvet_baffle_box():
    """Verify create_duvet generates baffle-box bedding with rounded drape overhang."""
    res = create_duvet(
        bed_width=1.8,
        bed_length=2.0,
        overhang=0.3,
        thickness=0.05,
        baffle_box=True,
        name="Master_Duvet"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Master_Duvet"
    assert result["baffle_box"] is True
    assert result["overhang"] == 0.3
    assert result["vertex_count"] > 30


def test_create_blanket_folded():
    """Verify create_blanket generates accent throw blanket with folded edge."""
    res = create_blanket(
        width=1.3,
        length=1.7,
        drape_angle=20.0,
        thickness=0.012,
        fold_back=0.25,
        name="Throw_Blanket"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Throw_Blanket"
    assert result["fold_back"] == 0.25
    assert result["vertex_count"] > 20


def test_create_tufted_surface():
    """Verify create_tufted_surface generates quilted chesterfield pattern with buttons."""
    res = create_tufted_surface(
        width=1.2,
        height=0.9,
        rows=4,
        cols=4,
        button_depth=0.035,
        diamond_pattern=True,
        name="Headboard_Tuft"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["object_name"] == "Headboard_Tuft"
    assert result["rows"] == 4
    assert result["cols"] == 4
    assert result["button_count"] == 16
    assert result["diamond_pattern"] is True
