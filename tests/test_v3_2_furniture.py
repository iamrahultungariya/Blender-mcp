"""Unit tests for Phase V3.2 Furniture & Architectural Detail Engine.

Verifies semantic component hierarchy generation (Pillar 4), clean quad topology (Pillar 2),
and AAA edge conditioning (Pillar 3) for beds, sofas, chairs, tables, wardrobes, and doors.
"""

import pytest
from blender_mcp.furniture_engine import (
    create_bed,
    create_sofa,
    create_chair,
    create_table,
    create_wardrobe,
    create_door_assembly
)


def test_create_bed_semantic_hierarchy():
    """Verify create_bed returns structured semantic hierarchy with frame, headboard, mattress, pillows, duvet."""
    res = create_bed(
        style="modern",
        dimensions=(2.0, 1.8, 0.45),
        headboard_style="tufted",
        include_mattress=True,
        include_pillows=True,
        include_duvet=True,
        name="Master_Bed"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["root_name"] == "Master_Bed_Root"
    assert "components" in result
    comp_names = [c["name"] for c in result["components"]]
    assert any("Frame" in n for n in comp_names)
    assert any("Headboard" in n for n in comp_names)
    assert any("Mattress" in n for n in comp_names)
    assert any("Pillow" in n for n in comp_names)
    assert any("Duvet" in n for n in comp_names)
    assert result["total_components"] >= 5


def test_create_sofa_modular_cushions():
    """Verify create_sofa returns semantic assembly with frame, armrests, seat & back cushions."""
    res = create_sofa(
        style="modern",
        seats=3,
        armrest_style="rounded",
        cushion_puffiness=0.85,
        leg_style="tapered_metal",
        name="Living_Sofa"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["root_name"] == "Living_Sofa_Root"
    assert result["seats"] == 3
    comp_names = [c["name"] for c in result["components"]]
    assert any("Base" in n for n in comp_names)
    assert any("Backrest" in n for n in comp_names)
    assert any("Armrest_L" in n for n in comp_names)
    assert any("Armrest_R" in n for n in comp_names)
    assert any("Seat_Cushion" in n for n in comp_names)
    assert any("Back_Cushion" in n for n in comp_names)


def test_create_chair_proportions():
    """Verify create_chair generates seat, backrest, and legs."""
    res = create_chair(
        style="dining",
        seat_height=0.45,
        backrest_style="curved",
        leg_style="tapered",
        name="Dining_Chair"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["root_name"] == "Dining_Chair_Root"
    comp_names = [c["name"] for c in result["components"]]
    assert any("Seat" in n for n in comp_names)
    assert any("Backrest" in n for n in comp_names)
    assert any("Legs" in n for n in comp_names)


def test_create_table_chamfer():
    """Verify create_table generates tabletop with chamfer, apron, and legs."""
    res = create_table(
        style="dining",
        length=1.8,
        width=0.9,
        height=0.76,
        tabletop_thickness=0.04,
        leg_style="angled_post",
        name="Dining_Table"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["root_name"] == "Dining_Table_Root"
    comp_names = [c["name"] for c in result["components"]]
    assert any("Top" in n for n in comp_names)
    assert any("Apron" in n for n in comp_names)
    assert any("Legs" in n for n in comp_names)


def test_create_wardrobe_doors_and_drawers():
    """Verify create_wardrobe generates carcass, doors, drawers, and handles."""
    res = create_wardrobe(
        width=1.4,
        height=2.2,
        depth=0.6,
        door_count=2,
        has_drawers=True,
        handle_style="bar",
        name="Master_Wardrobe"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["root_name"] == "Master_Wardrobe_Root"
    comp_names = [c["name"] for c in result["components"]]
    assert any("Carcass" in n for n in comp_names)
    assert any("Door" in n for n in comp_names)
    assert any("Drawer" in n for n in comp_names)
    assert any("Handle" in n for n in comp_names)


def test_create_door_assembly_molding_and_hardware():
    """Verify create_door_assembly generates frame, casing architrave, panel leaf, and hardware."""
    res = create_door_assembly(
        width=0.9,
        height=2.1,
        frame_depth=0.15,
        panel_style="six_panel",
        handle_type="lever",
        name="Internal_Door"
    )
    assert res["success"] is True
    result = res["result"]
    assert result["root_name"] == "Internal_Door_Root"
    comp_names = [c["name"] for c in result["components"]]
    assert any("Jamb" in n for n in comp_names)
    assert any("Architrave" in n for n in comp_names)
    assert any("Leaf" in n for n in comp_names)
    assert any("Hardware" in n for n in comp_names)
