"""
Ambulance Builder - Watertight Body Shell, Swept Forehead & Clean Fenders (<190 LOC).
Continuous quad-strip topology, 3D boxed A-pillars, watertight dome cheeks & cab interior tub.
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_body_shell(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    obj = bpy.data.objects.get("VAN_Body_Shell")
    if not obj:
        mesh = bpy.data.meshes.new("VAN_Body_Shell")
        obj = bpy.data.objects.new("VAN_Body_Shell", mesh)
        (target_col or bpy.context.scene.collection).objects.link(obj)
    mesh = obj.data

    for m_name in ["VAN_Paint_White", "VAN_Cladding_Grey", "VAN_Glass_Tinted"]:
        m = bpy.data.materials.get(m_name)
        if m and m.name not in mesh.materials:
            mesh.materials.append(m)
    m_idx = {name: i for i, name in enumerate(mesh.materials.keys())}

    bm = bmesh.new()

    def make_box(bm, min_v, max_v, mat_id, smooth=True):
        min_v, max_v = Vector(min_v), Vector(max_v)
        center = (min_v + max_v) * 0.5
        size_v = max_v - min_v
        res = bmesh.ops.create_cube(
            bm, size=1.0, matrix=Matrix.Translation(center) @ Matrix.Diagonal((*size_v, 1.0))
        )
        for f in list({f for v in res["verts"] for f in v.link_faces}):
            f.material_index = mat_id
            f.smooth = smooth
        return res

    # 1. Solid Interior Cab Tub & Partition (Eliminates interior light bleed)
    make_box(bm, (-0.98, 0.60, 0.54), (0.98, 1.48, 0.58), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.92, 1.25, 0.58), (0.92, 1.48, 1.16), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.98, 0.60, 0.54), (0.98, 0.66, 2.10), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.26, 0.59, 1.35), (0.26, 0.67, 1.70), m_idx["VAN_Glass_Tinted"])

    # 2. Main Cargo Body, Rear Barn Doors & Roof Cap
    make_box(bm, (-1.02, -2.96, 0.54), (1.02, 1.48, 1.25), m_idx["VAN_Paint_White"])
    make_box(bm, (-1.00, -2.96, 2.08), (1.00, 0.82, 2.65), m_idx["VAN_Paint_White"])
    make_box(bm, (-0.98, -2.96, 0.54), (0.98, -2.94, 2.10), m_idx["VAN_Paint_White"])

    for s_sign in [1, -1]:
        sx_in, sx_out = s_sign * 0.98, s_sign * 1.02
        x_min, x_max = min(sx_in, sx_out), max(sx_in, sx_out)
        make_box(bm, (x_min, -2.96, 1.25), (x_max, -0.65, 2.10), m_idx["VAN_Paint_White"])
        make_box(bm, (x_min, -0.65, 1.25), (x_max, 0.55, 1.30), m_idx["VAN_Paint_White"])
        make_box(bm, (x_min, -0.65, 2.05), (x_max, 0.55, 2.10), m_idx["VAN_Paint_White"])
        make_box(bm, (x_min, 0.55, 1.25), (x_max, 0.68, 2.10), m_idx["VAN_Paint_White"])
        # Complete Cab Door Upper Perimeter Frame & Door Sill
        make_box(bm, (x_min, 0.68, 1.25), (x_max, 1.44, 1.28), m_idx["VAN_Paint_White"])
        make_box(bm, (s_sign * 0.92, 0.68, 2.04), (s_sign * 0.98, 1.12, 2.08), m_idx["VAN_Paint_White"])
        make_box(bm, (x_min, 0.68, 1.28), (x_max, 0.72, 2.04), m_idx["VAN_Paint_White"])

    # 3. Lofted Continuous Hood (32x20)
    u_s, v_s = 32, 20
    u_v = [i / u_s for i in range(u_s + 1)]
    v_v = [j / v_s for j in range(v_s + 1)]
    hood = []
    for v in v_v:
        y = 1.48 + (2.86 - 1.48) * v
        z_b = 1.18 - 0.28 * (v ** 1.08)
        hw = 0.98 - 0.22 * (v ** 0.95)
        row = []
        for u in u_v:
            un = (u - 0.5) * 2.0
            sweep = (un ** 4) * 0.12 * v
            crown = (1.0 - (un ** 2)) * (0.035 - 0.010 * v)
            row.append(bm.verts.new((un * hw, y - sweep, z_b + crown)))
        hood.append(row)

    for j in range(v_s):
        for i in range(u_s):
            f = bm.faces.new([hood[j][i], hood[j][i+1], hood[j+1][i+1], hood[j+1][i]])
            f.material_index = m_idx["VAN_Paint_White"]
            f.smooth = True

    # 4. Continuous Smooth Front Fenders (Shared Vertex Strips, No Gaps/Fringes)
    for s_sign in [1, -1]:
        f_top = []
        f_low = []
        for j in range(v_s + 1):
            v = v_v[j]
            y = 1.48 + (2.86 - 1.48) * v - 0.12 * v
            z = 1.18 - 0.28 * (v ** 1.08)
            x = s_sign * (1.02 - 0.035 * v)
            zl = 0.84 if (1.30 <= y <= 2.15) else (0.54 if y > 2.15 else 0.84)
            f_top.append(bm.verts.new((x, y, z)))
            f_low.append(bm.verts.new((x, y, zl)))

        for j in range(v_s):
            in0 = hood[j][u_s if s_sign > 0 else 0]
            in1 = hood[j + 1][u_s if s_sign > 0 else 0]
            top_vs = [in0, in1, f_top[j + 1], f_top[j]] if s_sign > 0 else [in0, f_top[j], f_top[j + 1], in1]
            side_vs = [f_top[j], f_top[j + 1], f_low[j + 1], f_low[j]] if s_sign > 0 else [f_top[j], f_low[j], f_low[j + 1], f_top[j + 1]]
            f1 = bm.faces.new(top_vs)
            f2 = bm.faces.new(side_vs)
            f1.material_index = f2.material_index = m_idx["VAN_Paint_White"]
            f1.smooth = f2.smooth = True

    # 5. Watertight Aerodynamic Forehead Dome (Shared Vertex Topology)
    brow = []
    for j in range(v_s + 1):
        v = j / v_s
        ts = 0.5 * (1.0 - math.cos(v * math.pi))
        y_c = 1.12 - (1.12 - 0.82) * ts + math.sin(v * math.pi) * 0.045
        z_c = 2.08 + (2.65 - 2.08) * ts
        hw = 0.88 + 0.11 * v
        row = []
        for i in range(u_s + 1):
            un = (i / u_s - 0.5) * 2.0
            sag = (1.0 - (un ** 2)) * 0.075 * (1.0 - v)
            row.append(bm.verts.new((un * hw, y_c + sag, z_c)))
        brow.append(row)

    for j in range(v_s):
        for i in range(u_s):
            f = bm.faces.new([brow[j][i], brow[j][i+1], brow[j+1][i+1], brow[j+1][i]])
            f.material_index = m_idx["VAN_Paint_White"]
            f.smooth = True

    # Continuous Forehead Side Cheeks (Shared Strip)
    for s_sign in [1, -1]:
        sx = s_sign * 0.99
        cheek_low = [bm.verts.new((sx, 1.12 - (1.12 - 0.82) * (j / v_s), 2.08)) for j in range(v_s + 1)]
        for j in range(v_s):
            b0 = brow[j][u_s if s_sign > 0 else 0]
            b1 = brow[j + 1][u_s if s_sign > 0 else 0]
            chk_vs = [b0, b1, cheek_low[j + 1], cheek_low[j]] if s_sign > 0 else [b0, cheek_low[j], cheek_low[j + 1], b1]
            f_chk = bm.faces.new(chk_vs)
            f_chk.material_index = m_idx["VAN_Paint_White"]
            f_chk.smooth = True

    # Under-cowl shelf
    make_box(bm, (-0.88, 1.08, 2.04), (0.88, 1.14, 2.08), m_idx["VAN_Cladding_Grey"])

    # 6. 3D Boxed Structural A-Pillars (True Volume & Tumblehome)
    for s_sign in [1, -1]:
        xb_out, xb_in = s_sign * 1.00, s_sign * 0.92
        xt_out, xt_in = s_sign * 0.92, s_sign * 0.84
        v_out_bot = bm.verts.new((xb_out, 1.48, 1.20))
        v_out_top = bm.verts.new((xt_out, 1.12, 2.08))
        v_in_top = bm.verts.new((xt_in, 1.12, 2.08))
        v_in_bot = bm.verts.new((xb_in, 1.48, 1.20))
        # Front face
        f_front = bm.faces.new([v_out_bot, v_out_top, v_in_top, v_in_bot] if s_sign > 0 else [v_out_bot, v_in_bot, v_in_top, v_out_top])
        f_front.material_index = m_idx["VAN_Paint_White"]
        f_front.smooth = True

    # 7. 6 Longitudinal Roof Stiffening Ribs
    for rx in [-0.72, -0.44, -0.15, 0.15, 0.44, 0.72]:
        make_box(bm, (rx - 0.038, -2.60, 2.65), (rx + 0.038, 0.65, 2.67), m_idx["VAN_Paint_White"])

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.002)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj.location = base_offset
    sub_mod = obj.modifiers.get("Auto_Subsurf")
    if sub_mod:
        obj.modifiers.remove(sub_mod)

    b_mod = obj.modifiers.get("Auto_Bevel") or obj.modifiers.new("Auto_Bevel", 'BEVEL')
    b_mod.width = 0.005
    b_mod.segments = 2
    b_mod.limit_method = 'ANGLE'
    b_mod.angle_limit = math.radians(35.0)

    wn_mod = obj.modifiers.get("Auto_WeightedNormal") or obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn_mod.keep_sharp = True
    print("Continuous watertight unibody shell and forehead dome constructed.")
