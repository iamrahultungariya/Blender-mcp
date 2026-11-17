"""Furniture & Decor Kit (Floating Nightstands, Brass Reveals, Ceramic Vase, Art Books).

Tier 3 Modular Prefab: Constructs bedside tables and tabletop styling accessories.
"""
from __future__ import annotations

import bpy
from luxury_bedroom.core.mesh_utils import (
    bmesh_to_object,
    create_beveled_box,
    create_cylinder,
)


def build_furniture(
    col: bpy.types.Collection, mats: dict[str, bpy.types.Material]
) -> dict[str, bpy.types.Object]:
    """Construct floating oak nightstands, brass drawer accents, and tabletop decor."""
    objs = {}

    for side, pos_x in [("Left", -1.48), ("Right", 1.48)]:
        # Floating Oak Console Body
        ns_bm = create_beveled_box(
            width=0.55, length=0.42, height=0.30, bevel_radius=0.020, segments=3, offset=(pos_x, 1.88, 0.16)
        )
        objs[f"Nightstand_{side}"] = bmesh_to_object(
            ns_bm, f"Nightstand_{side}_Oak", col, mats["OAK_WOOD"]
        )

        # Brushed Brass Drawer Reveal Trim
        reveal_bm = create_beveled_box(
            width=0.51, length=0.015, height=0.015, bevel_radius=0.002, segments=1, offset=(pos_x, 1.66, 0.31)
        )
        objs[f"Nightstand_Trim_{side}"] = bmesh_to_object(
            reveal_bm, f"Nightstand_{side}_Brass_Trim", col, mats["BRUSHED_BRASS"]
        )

    # Left Nightstand Decor: Ceramic Artisanal Vase with botanical branch
    vase_bm = create_cylinder(radius=0.055, height=0.17, segments=24, offset=(-1.48, 1.88, 0.46))
    objs["Vase"] = bmesh_to_object(vase_bm, "Decor_Ceramic_Vase", col, mats["CERAMIC"])

    branch_bm = create_cylinder(radius=0.004, height=0.28, segments=8, offset=(-1.48, 1.88, 0.55))
    objs["Branch"] = bmesh_to_object(branch_bm, "Decor_Botanical_Branch", col, mats["MATTE_BLACK"])

    # Right Nightstand Decor: Stack of 2 Hardcover Art Books
    b1_bm = create_beveled_box(
        width=0.22, length=0.28, height=0.03, bevel_radius=0.004, segments=1, offset=(1.48, 1.88, 0.46)
    )
    objs["Book_Bottom"] = bmesh_to_object(b1_bm, "Decor_Book_Bottom", col, mats["BOOK"])

    b2_bm = create_beveled_box(
        width=0.20, length=0.26, height=0.025, bevel_radius=0.004, segments=1, offset=(1.49, 1.87, 0.49)
    )
    objs["Book_Top"] = bmesh_to_object(b2_bm, "Decor_Book_Top", col, mats["HEADBOARD_BOUCLE"])

    return objs
