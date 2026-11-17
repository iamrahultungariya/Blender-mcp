"""Soft Goods Kit (Puffy Sleeping Pillows with Welt Piping & Folded Draped Duvet).

Tier 3 Modular Prefab: Anti-Boxy soft goods with organic curves and fabric tension.
"""
from __future__ import annotations

import math
import bpy
import bmesh
from mathutils import Vector
from luxury_bedroom.core.mesh_utils import bmesh_to_object


def create_puffy_sleeping_pillow_mesh(
    width: float = 0.78,
    length: float = 0.52,
    thickness: float = 0.20,
    crown_height: float = 0.085,
    piping_radius: float = 0.008,
    subdivisions_u: int = 16,
    subdivisions_v: int = 12,
    tilt_deg_x: float = 26.0,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bmesh.types.BMesh:
    """Generate an authentic puffy sleeping pillow with authentic fabric seam welt line and pinched corners."""
    bm = bmesh.new()
    ox, oy, oz = offset
    rad_tilt = math.radians(tilt_deg_x)
    cos_t, sin_t = math.cos(rad_tilt), math.sin(rad_tilt)

    top_grid = []
    bot_grid = []
    mid_grid = []

    for i in range(subdivisions_u + 1):
        top_row = []
        bot_row = []
        mid_row = []
        u = -1.0 + 2.0 * (i / subdivisions_u)
        x = u * (width / 2.0)

        for j in range(subdivisions_v + 1):
            v = -1.0 + 2.0 * (j / subdivisions_v)
            y = v * (length / 2.0)

            crown_factor = max(0.0, (1.0 - u * u) * (1.0 - v * v))
            center_hollow = 0.015 * math.exp(-6.0 * (u * u + v * v))

            zt = (thickness / 2.0) + (crown_height * crown_factor) - center_hollow
            zb = -(thickness / 2.0) - (crown_height * 0.40 * crown_factor)

            corner_pinch = (u * u) * (v * v)
            zt -= 0.024 * corner_pinch
            zb += 0.024 * corner_pinch

            xm = x
            ym = y
            zm = 0.0
            if abs(u) > 0.95 or abs(v) > 0.95:
                x_sign = math.copysign(1.0, u) if abs(u) > 0.1 else 0.0
                y_sign = math.copysign(1.0, v) if abs(v) > 0.1 else 0.0
                if abs(u) > 0.95:
                    xm += x_sign * piping_radius
                if abs(v) > 0.95:
                    ym += y_sign * piping_radius

            y_rel = y - (length / 2.0)
            yt_rot = y_rel * cos_t - zt * sin_t + (length / 2.0)
            zt_rot = y_rel * sin_t + zt * cos_t

            yb_rot = y_rel * cos_t - zb * sin_t + (length / 2.0)
            zb_rot = y_rel * sin_t + zb * cos_t

            ym_rel = ym - (length / 2.0)
            ym_rot = ym_rel * cos_t - zm * sin_t + (length / 2.0)
            zm_rot = ym_rel * sin_t + zm * cos_t

            vt = bm.verts.new(Vector((ox + x, oy + yt_rot, oz + zt_rot)))
            vb = bm.verts.new(Vector((ox + x, oy + yb_rot, oz + zb_rot)))
            vm = bm.verts.new(Vector((ox + xm, oy + ym_rot, oz + zm_rot)))

            top_row.append(vt)
            bot_row.append(vb)
            mid_row.append(vm)

        top_grid.append(top_row)
        bot_grid.append(bot_row)
        mid_grid.append(mid_row)

    for i in range(subdivisions_u):
        for j in range(subdivisions_v):
            bm.faces.new((top_grid[i][j], top_grid[i + 1][j], top_grid[i + 1][j + 1], top_grid[i][j + 1]))
            bm.faces.new((bot_grid[i][j], bot_grid[i][j + 1], bot_grid[i + 1][j + 1], bot_grid[i + 1][j]))

    for i in range(subdivisions_u):
        bm.faces.new((top_grid[i][0], top_grid[i + 1][0], mid_grid[i + 1][0], mid_grid[i][0]))
        bm.faces.new((mid_grid[i][0], mid_grid[i + 1][0], bot_grid[i + 1][0], bot_grid[i][0]))
    for j in range(subdivisions_v):
        bm.faces.new((top_grid[subdivisions_u][j], top_grid[subdivisions_u][j + 1], mid_grid[subdivisions_u][j + 1], mid_grid[subdivisions_u][j]))
        bm.faces.new((mid_grid[subdivisions_u][j], mid_grid[subdivisions_u][j + 1], bot_grid[subdivisions_u][j + 1], bot_grid[subdivisions_u][j]))
    for i in range(subdivisions_u - 1, -1, -1):
        bm.faces.new((top_grid[i + 1][subdivisions_v], top_grid[i][subdivisions_v], mid_grid[i][subdivisions_v], mid_grid[i + 1][subdivisions_v]))
        bm.faces.new((mid_grid[i + 1][subdivisions_v], mid_grid[i][subdivisions_v], bot_grid[i][subdivisions_v], bot_grid[i + 1][subdivisions_v]))
    for j in range(subdivisions_v - 1, -1, -1):
        bm.faces.new((top_grid[0][j + 1], top_grid[0][j], mid_grid[0][j], mid_grid[0][j + 1]))
        bm.faces.new((mid_grid[0][j + 1], mid_grid[0][j], bot_grid[0][j], bot_grid[0][j + 1]))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def create_luxury_folded_duvet_mesh(
    width: float = 2.06,
    length: float = 1.45,
    drape_drop: float = 0.24,
    cuff_length: float = 0.28,
    loft_thickness: float = 0.035,
    subdivisions_x: int = 28,
    subdivisions_y: int = 24,
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bmesh.types.BMesh:
    """Generate an authentic draped, folded duvet blanket with turned-down cuff fold."""
    bm = bmesh.new()
    ox, oy, oz = offset

    grid = []
    cuff_y_threshold = (length / 2.0) - cuff_length

    for i in range(subdivisions_x + 1):
        row = []
        u = -1.0 + 2.0 * (i / subdivisions_x)
        x = u * (width / 2.0)

        flank_dist = max(0.0, abs(u) - 0.72) / 0.28
        flank_drop = (flank_dist ** 2) * drape_drop

        for j in range(subdivisions_y + 1):
            v = -1.0 + 2.0 * (j / subdivisions_y)
            y = v * (length / 2.0)

            foot_dist = max(0.0, (-v) - 0.68) / 0.32
            foot_drop = (foot_dist ** 2) * (drape_drop * 1.1)

            center_loft = loft_thickness * max(0.0, (1.0 - (u * 0.9) ** 2) * (1.0 - (v * 0.9) ** 2))
            cloth_ripple = 0.008 * math.sin(2.5 * math.pi * u) * math.cos(2.0 * math.pi * v)

            z_cuff_offset = 0.0
            if y > cuff_y_threshold:
                cuff_progress = (y - cuff_y_threshold) / max(0.01, cuff_length)
                z_cuff_offset = math.sin(cuff_progress * math.pi) * 0.055 - (cuff_progress * 0.03)

            z = oz + center_loft + cloth_ripple - flank_drop - foot_drop + z_cuff_offset
            row.append(bm.verts.new(Vector((ox + x, oy + y, z))))
        grid.append(row)

    for i in range(subdivisions_x):
        for j in range(subdivisions_y):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def build_soft_goods(
    col: bpy.types.Collection, mats: dict[str, bpy.types.Material]
) -> dict[str, bpy.types.Object]:
    """Construct 2 puffy sleeping pillows with welt seams and folded draped duvet blanket."""
    objs = {}

    # 1. Left Puffy Sleeping Pillow (with welt piping & deep parabolic crown)
    p_left_bm = create_puffy_sleeping_pillow_mesh(offset=(-0.48, 1.76, 0.54))
    p_left_obj = bmesh_to_object(p_left_bm, "Pillow_Sleeping_Left", col, mats["PILLOW_COTTON"])
    mod = p_left_obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = 2
    mod.render_levels = 2
    objs["Pillow_Left"] = p_left_obj

    # 2. Right Puffy Sleeping Pillow
    p_right_bm = create_puffy_sleeping_pillow_mesh(offset=(0.48, 1.76, 0.54))
    p_right_obj = bmesh_to_object(p_right_bm, "Pillow_Sleeping_Right", col, mats["PILLOW_COTTON"])
    mod = p_right_obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = 2
    mod.render_levels = 2
    objs["Pillow_Right"] = p_right_obj

    # 3. Folded Duvet Blanket with Turned-Down Cuff & Draped Flanks
    duvet_bm = create_luxury_folded_duvet_mesh(offset=(0.0, 0.65, 0.51))
    duvet_obj = bmesh_to_object(duvet_bm, "Duvet_Blanket_Folded", col, mats["DUVET_FABRIC"])
    sol = duvet_obj.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.016
    sol.offset = 0.0
    mod = duvet_obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = 2
    mod.render_levels = 2
    objs["Duvet"] = duvet_obj

    return objs
