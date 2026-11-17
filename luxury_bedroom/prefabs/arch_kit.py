"""Architectural Shell Kit (Walls, Flooring, Window, Curtains, Skirting).

Tier 3 Modular Prefab: Constructs room boundary and window opening.
"""
from __future__ import annotations

import math
import bpy
import bmesh
from mathutils import Vector
from luxury_bedroom.core.mesh_utils import bmesh_to_object, create_beveled_box


def create_pleated_curtain_mesh(
    width: float = 0.55,
    height: float = 2.02,
    depth_pleat: float = 0.04,
    pleat_count: int = 6,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bmesh.types.BMesh:
    """Generate an elegant sheer pleated curtain panel hanging gracefully."""
    bm = bmesh.new()
    ox, oy, oz = offset
    subs_z = 10
    subs_y = pleat_count * 4

    grid = []
    for j in range(subs_y + 1):
        row = []
        v = j / subs_y
        y = v * width
        pleat_x = math.sin(v * pleat_count * 2.0 * math.pi) * depth_pleat

        for k in range(subs_z + 1):
            w = k / subs_z
            z = w * height
            row.append(bm.verts.new(Vector((ox + pleat_x, oy + y, oz + z))))
        grid.append(row)

    for j in range(subs_y):
        for k in range(subs_z):
            bm.faces.new((grid[j][k], grid[j + 1][k], grid[j + 1][k + 1], grid[j][k + 1]))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def build_architectural_shell(
    col: bpy.types.Collection, mats: dict[str, bpy.types.Material]
) -> dict[str, bpy.types.Object]:
    """Construct complete room envelope, floor, baseboards, window, and curtains."""
    objs = {}

    # 1. Floor (Wide-Plank Satin Oak)
    floor_bm = create_beveled_box(
        width=5.20, length=5.60, height=0.04, bevel_radius=0.005, segments=2, offset=(0.0, 0.0, -0.04)
    )
    objs["Floor"] = bmesh_to_object(floor_bm, "Floor_Oak_Hardwood", col, mats["OAK_FLOOR"])

    # 2. Plush Wool Area Rug
    rug_bm = create_beveled_box(
        width=2.50, length=3.10, height=0.016, bevel_radius=0.02, segments=2, offset=(0.0, 0.85, 0.0)
    )
    objs["Rug"] = bmesh_to_object(rug_bm, "Rug_Plush_Wool", col, mats["RUG"])

    # 3. Back Wall (Minimalist Off-White Plaster)
    back_bm = create_beveled_box(
        width=5.20, length=0.20, height=2.85, bevel_radius=0.005, segments=1, offset=(0.0, 2.60, 0.0)
    )
    objs["Wall_Back"] = bmesh_to_object(back_bm, "Wall_Back_Plaster", col, mats["WALL_PLASTER"])

    # 4. Right Wall
    right_bm = create_beveled_box(
        width=0.20, length=5.60, height=2.85, bevel_radius=0.005, segments=1, offset=(2.50, 0.0, 0.0)
    )
    objs["Wall_Right"] = bmesh_to_object(right_bm, "Wall_Right_Plaster", col, mats["WALL_PLASTER"])

    # 5. Left Wall Window Cutout (Sill, Header, Back & Front Jambs)
    sill_bm = create_beveled_box(
        width=0.20, length=5.60, height=0.45, bevel_radius=0.005, segments=1, offset=(-2.50, 0.0, 0.0)
    )
    objs["Wall_Sill"] = bmesh_to_object(sill_bm, "Wall_Left_Sill", col, mats["WALL_PLASTER"])

    header_bm = create_beveled_box(
        width=0.20, length=5.60, height=0.35, bevel_radius=0.005, segments=1, offset=(-2.50, 0.0, 2.50)
    )
    objs["Wall_Header"] = bmesh_to_object(header_bm, "Wall_Left_Header", col, mats["WALL_PLASTER"])

    jamb_b_bm = create_beveled_box(
        width=0.20, length=1.20, height=2.05, bevel_radius=0.005, segments=1, offset=(-2.50, 2.20, 0.45)
    )
    objs["Wall_Jamb_Back"] = bmesh_to_object(jamb_b_bm, "Wall_Left_Jamb_Back", col, mats["WALL_PLASTER"])

    jamb_f_bm = create_beveled_box(
        width=0.20, length=2.00, height=2.05, bevel_radius=0.005, segments=1, offset=(-2.50, -1.80, 0.45)
    )
    objs["Wall_Jamb_Front"] = bmesh_to_object(jamb_f_bm, "Wall_Left_Jamb_Front", col, mats["WALL_PLASTER"])

    # 6. Architectural Hollow Black Aluminum Window Frame
    win_f_bm = bmesh.new()
    bars = [
        # (width, length, height, offset)
        (0.08, 2.40, 0.05, (-2.50, 0.40, 2.45)),   # Top sill bar
        (0.08, 2.40, 0.05, (-2.50, 0.40, 0.45)),   # Bottom sill bar
        (0.08, 0.05, 1.95, (-2.50, 1.575, 0.50)),  # Back jamb bar
        (0.08, 0.05, 1.95, (-2.50, -0.775, 0.50)), # Front jamb bar
        (0.06, 0.04, 1.95, (-2.50, 0.40, 0.50)),   # Vertical center mullion bar
    ]
    for w, l, h, (ox, oy, oz) in bars:
        ret = bmesh.ops.create_cube(win_f_bm, size=1.0)
        bmesh.ops.scale(win_f_bm, vec=(w, l, h), verts=ret["verts"])
        bmesh.ops.translate(win_f_bm, vec=(ox, oy, oz + h / 2.0), verts=ret["verts"])

    bmesh.ops.recalc_face_normals(win_f_bm, faces=win_f_bm.faces)
    objs["Window_Frame"] = bmesh_to_object(win_f_bm, "Window_Frame_Exterior", col, mats["WINDOW_FRAME"])

    # 7. Architectural Window Glass (Clear transmission, no dark shadow)
    glass_bm = create_beveled_box(
        width=0.015, length=2.34, height=1.99, bevel_radius=0.001, segments=1, offset=(-2.50, 0.40, 0.48)
    )
    glass_obj = bmesh_to_object(glass_bm, "Window_Architectural_Glass", col, mats["WINDOW_GLASS"])
    glass_obj.visible_shadow = False
    objs["Window_Glass"] = glass_obj

    # 8. Glowing Morning Sky Exterior Plane (outside window)
    sky_bm = bmesh.new()
    v0 = sky_bm.verts.new(Vector((-2.75, -1.40, 0.20)))
    v1 = sky_bm.verts.new(Vector((-2.75, 2.20, 0.20)))
    v2 = sky_bm.verts.new(Vector((-2.75, 2.20, 2.75)))
    v3 = sky_bm.verts.new(Vector((-2.75, -1.40, 2.75)))
    sky_bm.faces.new((v0, v1, v2, v3))
    bmesh.ops.recalc_face_normals(sky_bm, faces=sky_bm.faces)
    sky_obj = bmesh_to_object(sky_bm, "Backdrop_Morning_Sky", col, mats["EXTERIOR_SKY"])
    sky_obj.visible_shadow = False
    objs["Morning_Sky"] = sky_obj

    # 9. Sheer Pleated Linen Curtains
    c_back_bm = create_pleated_curtain_mesh(offset=(-2.42, 1.05, 0.46))
    objs["Curtain_Back"] = bmesh_to_object(c_back_bm, "Curtain_Sheer_Back", col, mats["SHEER_CURTAIN"])

    c_front_bm = create_pleated_curtain_mesh(offset=(-2.42, -0.80, 0.46))
    objs["Curtain_Front"] = bmesh_to_object(c_front_bm, "Curtain_Sheer_Front", col, mats["SHEER_CURTAIN"])

    # 10. Baseboards & Ceiling
    bb_b_bm = create_beveled_box(
        width=4.95, length=0.02, height=0.12, bevel_radius=0.004, segments=1, offset=(0.0, 2.49, 0.0)
    )
    objs["Baseboard_Back"] = bmesh_to_object(bb_b_bm, "Baseboard_Back_Wall", col, mats["BASEBOARD"])

    bb_r_bm = create_beveled_box(
        width=0.02, length=5.35, height=0.12, bevel_radius=0.004, segments=1, offset=(2.39, 0.0, 0.0)
    )
    objs["Baseboard_Right"] = bmesh_to_object(bb_r_bm, "Baseboard_Right_Wall", col, mats["BASEBOARD"])

    ceil_bm = create_beveled_box(
        width=5.20, length=5.60, height=0.08, bevel_radius=0.005, segments=1, offset=(0.0, 0.0, 2.85)
    )
    objs["Ceiling"] = bmesh_to_object(ceil_bm, "Ceiling_Slab", col, mats["WALL_PLASTER"])

    return objs
