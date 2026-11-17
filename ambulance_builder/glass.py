"""
Ambulance Builder - Ultra-Realistic Glazing, Raked Cab Glass & Towing Mirrors (<170 LOC).
Compound curved windshield, tumblehome raked cab glass matching A-pillar, dark privacy glass & towing mirrors.
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_glass_and_doors(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    obj = bpy.data.objects.get("VAN_Glass_and_Doors")
    if not obj:
        mesh = bpy.data.meshes.new("VAN_Glass_and_Doors")
        obj = bpy.data.objects.new("VAN_Glass_and_Doors", mesh)
        (target_col or bpy.context.scene.collection).objects.link(obj)
    mesh = obj.data

    mat_names = ["VAN_Glass_Tinted", "VAN_Cladding_Grey", "VAN_Wheel_Steel", "VAN_Strobe_Amber", "VAN_Paint_White"]
    for m_name in mat_names:
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

    # 1. Compound Curved Windshield (32x20 Quad Loft)
    u_s, v_s = 32, 20
    w_grid = []
    for j in range(v_s + 1):
        v = j / v_s
        y_w = 1.48 - 0.36 * v
        z_w = 1.20 + 0.88 * v
        hw = 0.91 - 0.085 * v
        row = []
        for i in range(u_s + 1):
            un = (i / u_s - 0.5) * 2.0
            sag = (1.0 - (un ** 2)) * 0.075 * (1.0 - 0.2 * v)
            row.append(bm.verts.new((un * hw, y_w + sag, z_w)))
        w_grid.append(row)

    for j in range(v_s):
        for i in range(u_s):
            f = bm.faces.new([w_grid[j][i], w_grid[j][i+1], w_grid[j+1][i+1], w_grid[j+1][i]])
            f.material_index = m_idx["VAN_Glass_Tinted"]
            f.smooth = True

    # Ceramic Frit Border
    make_box(bm, (-0.92, 1.45, 1.18), (0.92, 1.50, 1.22), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.84, 1.10, 2.06), (0.84, 1.14, 2.10), m_idx["VAN_Cladding_Grey"])

    # 2. Tumblehome Raked Cab Door Windows Matching A-Pillars (No gaps)
    for s_sign in [1, -1]:
        wx_bot = s_sign * 1.002
        wx_top = s_sign * 0.918
        v_bl = bm.verts.new((wx_bot, 0.72, 1.30))
        v_br = bm.verts.new((wx_bot, 1.42, 1.30))
        v_tr = bm.verts.new((wx_top, 1.14, 2.04))
        v_tl = bm.verts.new((wx_top, 0.72, 2.04))
        f_glass = bm.faces.new([v_bl, v_br, v_tr, v_tl] if s_sign > 0 else [v_bl, v_tl, v_tr, v_br])
        f_glass.material_index = m_idx["VAN_Glass_Tinted"]
        f_glass.smooth = True

        # Black molded rubber perimeter gasket frame
        f_bl = bm.verts.new((wx_bot + s_sign * 0.005, 0.70, 1.28))
        f_br = bm.verts.new((wx_bot + s_sign * 0.005, 1.44, 1.28))
        f_tr = bm.verts.new((wx_top + s_sign * 0.005, 1.12, 2.06))
        f_tl = bm.verts.new((wx_top + s_sign * 0.005, 0.70, 2.06))
        for p0, p1, g0, g1 in [(f_bl, f_br, v_bl, v_br), (f_br, f_tr, v_br, v_tr),
                               (f_tr, f_tl, v_tr, v_tl), (f_tl, f_bl, v_tl, v_bl)]:
            fg = bm.faces.new([p0, p1, g1, g0] if s_sign > 0 else [p0, g0, g1, p1])
            fg.material_index = m_idx["VAN_Cladding_Grey"]
            fg.smooth = True

        # Vertical Divider Bar for Vent Quarter Window
        make_box(bm, (wx_bot - 0.006, 1.20, 1.29), (wx_bot + 0.006, 1.22, 1.85), m_idx["VAN_Cladding_Grey"])

    # 3. Recessed Dark Privacy Side Windows (Curbside & Streetside)
    for s_sign in [1, -1]:
        wx = s_sign * 1.005
        make_box(bm, (wx - 0.004, -0.55, 1.32), (wx + 0.004, 0.55, 2.03), m_idx["VAN_Glass_Tinted"])
        make_box(bm, (wx - 0.006, -0.56, 1.30), (wx + 0.006, 0.56, 1.32), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (wx - 0.006, -0.56, 2.03), (wx + 0.006, 0.56, 2.05), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (wx - 0.006, -0.57, 1.30), (wx + 0.006, -0.55, 2.05), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (wx - 0.006, 0.55, 1.30), (wx + 0.006, 0.57, 2.05), m_idx["VAN_Cladding_Grey"])

    # Dual Rear Barn Door Windows (recessed)
    for s_sign in [1, -1]:
        rx = s_sign * 0.46
        make_box(bm, (rx - 0.36, -2.965, 1.44), (rx + 0.36, -2.955, 2.00), m_idx["VAN_Glass_Tinted"])
        make_box(bm, (rx - 0.38, -2.970, 1.42), (rx + 0.38, -2.950, 1.44), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (rx - 0.38, -2.970, 2.00), (rx + 0.38, -2.950, 2.02), m_idx["VAN_Cladding_Grey"])

    # 4. Commercial Dual-Glass Towing Mirrors with Amber Turn Indicators
    for s_sign in [1, -1]:
        mx_b, mx_o = s_sign * 1.02, s_sign * 1.25
        make_box(bm, (min(mx_b, mx_o), 1.24, 1.54), (max(mx_b, mx_o), 1.30, 1.58), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (min(mx_b, mx_o), 1.24, 1.36), (max(mx_b, mx_o), 1.30, 1.40), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (mx_o - 0.05, 1.20, 1.30), (mx_o + 0.05, 1.32, 1.66), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (mx_o - 0.045, 1.195, 1.44), (mx_o + 0.045, 1.205, 1.64), m_idx["VAN_Glass_Tinted"])
        make_box(bm, (mx_o - 0.045, 1.195, 1.32), (mx_o + 0.045, 1.205, 1.42), m_idx["VAN_Glass_Tinted"])
        make_box(bm, (mx_o + s_sign * 0.048, 1.24, 1.42), (mx_o + s_sign * 0.054, 1.31, 1.58), m_idx["VAN_Strobe_Amber"])

    # 5. Flush-Fit Modern Door Handles
    for s_sign in [1, -1]:
        hx = s_sign * 1.025
        make_box(bm, (hx - 0.008, 0.88, 1.12), (hx + 0.008, 1.04, 1.16), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (1.025 - 0.008, 0.45, 1.12), (1.025 + 0.008, 0.61, 1.16), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.12, -2.975, 1.08), (-0.02, -2.965, 1.20), m_idx["VAN_Cladding_Grey"])

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj.location = base_offset
    b_mod = obj.modifiers.get("Auto_Bevel") or obj.modifiers.new("Auto_Bevel", 'BEVEL')
    b_mod.width = 0.005
    b_mod.segments = 2
    b_mod.limit_method = 'ANGLE'
    b_mod.angle_limit = math.radians(35.0)

    wn_mod = obj.modifiers.get("Auto_WeightedNormal") or obj.modifiers.new("Auto_WeightedNormal", 'WEIGHTED_NORMAL')
    wn_mod.keep_sharp = True
    print("Glazing with tumblehome raked cab glass and rubber weatherstripping created.")
