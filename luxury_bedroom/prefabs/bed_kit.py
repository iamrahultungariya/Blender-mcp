"""Bed Assembly Kit (Low-Profile Platform Bed, Padded Headboard, Mattress).

Tier 3 Modular Prefab: Constructs hero bed architecture.
"""
from __future__ import annotations

import bpy
import bmesh
from mathutils import Vector
from luxury_bedroom.core.mesh_utils import bmesh_to_object, create_beveled_box


def create_padded_headboard_mesh(
    width: float = 2.26,
    height: float = 1.12,
    depth: float = 0.15,
    channel_count: int = 3,
    crown_height: float = 0.038,
    offset_y: float = 2.22,
    base_z: float = 0.18,
) -> bmesh.types.BMesh:
    """Generate a 3-channel padded/cushioned headboard with parabolic softness and horizontal seam grooves."""
    bm = bmesh.new()
    chan_h = (height - 0.04) / channel_count

    for c in range(channel_count):
        cz = base_z + 0.02 + (c * chan_h)
        subs_u = 18
        subs_v = 6
        top_grid = []
        bot_grid = []

        for i in range(subs_u + 1):
            top_row = []
            bot_row = []
            u = -1.0 + 2.0 * (i / subs_u)
            x = u * (width / 2.0)

            for j in range(subs_v + 1):
                v = -1.0 + 2.0 * (j / subs_v)
                z_rel = v * (chan_h * 0.46)
                crown = max(0.0, (1.0 - u * u) * (1.0 - v * v)) * crown_height
                front_y = offset_y - (depth / 2.0) - crown
                back_y = offset_y + (depth / 2.0)

                vf = bm.verts.new(Vector((x, front_y, cz + (chan_h / 2.0) + z_rel)))
                vb = bm.verts.new(Vector((x, back_y, cz + (chan_h / 2.0) + z_rel)))
                top_row.append(vf)
                bot_row.append(vb)
            top_grid.append(top_row)
            bot_grid.append(bot_row)

        for i in range(subs_u):
            for j in range(subs_v):
                bm.faces.new((top_grid[i][j], top_grid[i + 1][j], top_grid[i + 1][j + 1], top_grid[i][j + 1]))
                bm.faces.new((bot_grid[i][j], bot_grid[i][j + 1], bot_grid[i + 1][j + 1], bot_grid[i + 1][j]))

        for i in range(subs_u):
            bm.faces.new((top_grid[i][0], bot_grid[i][0], bot_grid[i + 1][0], top_grid[i + 1][0]))
            bm.faces.new((top_grid[i + 1][subs_v], bot_grid[i + 1][subs_v], bot_grid[i][subs_v], top_grid[i][subs_v]))
        for j in range(subs_v):
            bm.faces.new((top_grid[0][j + 1], bot_grid[0][j + 1], bot_grid[0][j], top_grid[0][j]))
            bm.faces.new((top_grid[subs_u][j], bot_grid[subs_u][j], bot_grid[subs_u][j + 1], top_grid[subs_u][j + 1]))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def build_bed_assembly(
    col: bpy.types.Collection, mats: dict[str, bpy.types.Material]
) -> dict[str, bpy.types.Object]:
    """Construct low-profile wooden platform bed, floating plinth, padded headboard, and mattress."""
    objs = {}

    # 1. Recessed Floating Plinth (Shadow gap)
    plinth_bm = create_beveled_box(
        width=1.84, length=2.00, height=0.09, bevel_radius=0.01, segments=2, offset=(0.0, 1.15, 0.0)
    )
    objs["Plinth"] = bmesh_to_object(plinth_bm, "Bed_Floating_Plinth", col, mats["MATTE_BLACK"])

    # 2. Main Platform Bed Frame (Warm American Oak with 30mm roundovers)
    platform_bm = create_beveled_box(
        width=2.10, length=2.24, height=0.18, bevel_radius=0.030, segments=3, offset=(0.0, 1.15, 0.09)
    )
    objs["Platform"] = bmesh_to_object(platform_bm, "Bed_Wooden_Platform_Frame", col, mats["OAK_WOOD"])

    # 3. Padded Cushioned Headboard (3 Soft Horizontal Channeled Bouclé Cushions)
    headboard_bm = create_padded_headboard_mesh()
    hb_obj = bmesh_to_object(headboard_bm, "Headboard_Padded_Cushioned", col, mats["HEADBOARD_BOUCLE"])
    mod = hb_obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = 1
    mod.render_levels = 2
    objs["Headboard"] = hb_obj

    # 4. Ergonomic Mattress Core
    mattress_bm = create_beveled_box(
        width=1.92, length=2.06, height=0.25, bevel_radius=0.045, segments=4, offset=(0.0, 1.10, 0.25)
    )
    mattress_obj = bmesh_to_object(mattress_bm, "Mattress_Ergonomic", col, mats["MATTRESS"])
    mod = mattress_obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = 1
    objs["Mattress"] = mattress_obj

    return objs
