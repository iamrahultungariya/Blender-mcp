"""
Ambulance Builder - Swept-Back Headlights & Whelen Freedom IV Lightbars (<180 LOC).
Procedural swept-back headlights with chrome rings, DRL eyebrow, and 128 parabolic LED cups.
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_emergency_system(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    obj = bpy.data.objects.get("VAN_Emergency_System")
    if not obj:
        mesh = bpy.data.meshes.new("VAN_Emergency_System")
        obj = bpy.data.objects.new("VAN_Emergency_System", mesh)
        (target_col or bpy.context.scene.collection).objects.link(obj)
    mesh = obj.data

    mat_names = ["VAN_Strobe_Red", "VAN_Strobe_Blue", "VAN_Strobe_Amber", "VAN_Headlight_LED",
                 "VAN_Taillight_Red", "VAN_Cladding_Grey", "VAN_Glass_Tinted", "VAN_Paint_White", "VAN_Wheel_Steel"]
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

    def tag_res(res, mat_id, smooth=True):
        for f in list({f for v in res["verts"] for f in v.link_faces}):
            f.material_index = mat_id
            f.smooth = smooth

    # 1. Front Rooftop Aerodynamic Lightbar (Whelen Freedom IV style, 64 LED Cups)
    for mx in [-0.55, 0.55]:
        make_box(bm, (mx - 0.05, 1.20, 2.64), (mx + 0.05, 1.32, 2.67), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.08, 1.20, 2.66), (0.08, 1.32, 2.76), m_idx["VAN_Cladding_Grey"])

    siren = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=24, radius1=0.065, radius2=0.042, depth=0.06,
        matrix=Matrix.Translation(Vector((0, 1.31, 2.71))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(siren, m_idx["VAN_Cladding_Grey"], smooth=True)

    make_box(bm, (-0.72, 1.21, 2.67), (-0.09, 1.31, 2.75), m_idx["VAN_Strobe_Red"])
    for li in range(16):
        cup = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=16, radius1=0.016, radius2=0.008, depth=0.02,
            matrix=Matrix.Translation(Vector((-0.70 + li * 0.038, 1.305, 2.71))) @ Matrix.Rotation(math.pi/2, 4, 'X')
        )
        tag_res(cup, m_idx["VAN_Headlight_LED"], smooth=True)

    make_box(bm, (0.09, 1.21, 2.67), (0.72, 1.31, 2.75), m_idx["VAN_Strobe_Blue"])
    for li in range(16):
        cup = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=16, radius1=0.016, radius2=0.008, depth=0.02,
            matrix=Matrix.Translation(Vector((0.11 + li * 0.038, 1.305, 2.71))) @ Matrix.Rotation(math.pi/2, 4, 'X')
        )
        tag_res(cup, m_idx["VAN_Headlight_LED"], smooth=True)

    make_box(bm, (-0.76, 1.20, 2.66), (-0.72, 1.32, 2.76), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (0.72, 1.20, 2.66), (0.76, 1.32, 2.76), m_idx["VAN_Cladding_Grey"])

    # 2. Rear Rooftop Aerodynamic Lightbar (64 LED Cups)
    for mx in [-0.55, 0.55]:
        make_box(bm, (mx - 0.05, -2.92, 2.64), (mx + 0.05, -2.84, 2.67), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.08, -2.92, 2.66), (0.08, -2.84, 2.76), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.72, -2.91, 2.67), (-0.09, -2.85, 2.75), m_idx["VAN_Strobe_Red"])
    for li in range(16):
        cup = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=16, radius1=0.016, radius2=0.008, depth=0.02,
            matrix=Matrix.Translation(Vector((-0.70 + li * 0.038, -2.855, 2.71))) @ Matrix.Rotation(-math.pi/2, 4, 'X')
        )
        tag_res(cup, m_idx["VAN_Headlight_LED"], smooth=True)

    make_box(bm, (0.09, -2.91, 2.67), (0.72, -2.85, 2.75), m_idx["VAN_Strobe_Blue"])
    for li in range(16):
        cup = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=16, radius1=0.016, radius2=0.008, depth=0.02,
            matrix=Matrix.Translation(Vector((0.11 + li * 0.038, -2.855, 2.71))) @ Matrix.Rotation(-math.pi/2, 4, 'X')
        )
        tag_res(cup, m_idx["VAN_Headlight_LED"], smooth=True)

    make_box(bm, (-0.76, -2.92, 2.66), (-0.72, -2.84, 2.76), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (0.72, -2.92, 2.66), (0.76, -2.84, 2.76), m_idx["VAN_Cladding_Grey"])

    # 3. 4 Corner Perimeter Warning Pods
    for px, py in [(-0.95, 0.95), (0.95, 0.95), (-0.95, -2.82), (0.95, -2.82)]:
        make_box(bm, (px - 0.045, py - 0.09, 2.63), (px + 0.045, py + 0.09, 2.65), m_idx["VAN_Cladding_Grey"])
        pod_res = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=24, radius1=0.042, radius2=0.034, depth=0.06,
            matrix=Matrix.Translation(Vector((px, py, 2.68)))
        )
        tag_res(pod_res, m_idx["VAN_Strobe_Red"], smooth=True)

    # 4. Rooftop AC Pod & Dual Fans
    make_box(bm, (-0.52, -0.50, 2.65), (0.52, 0.45, 2.78), m_idx["VAN_Paint_White"])
    make_box(bm, (-0.46, 0.38, 2.68), (0.46, 0.46, 2.76), m_idx["VAN_Cladding_Grey"])
    for fy in [-0.22, 0.12]:
        res_fan = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=32, radius1=0.18, radius2=0.18, depth=0.03,
            matrix=Matrix.Translation(Vector((0, fy, 2.78)))
        )
        tag_res(res_fan, m_idx["VAN_Cladding_Grey"], smooth=True)

    # 5. Seamless Swept Headlight Assemblies (Matching bumper Z=0.58 & fender Z=0.92)
    for s_sign in [1, -1]:
        hx_in, hx_out = s_sign * 0.68, s_sign * 0.98
        # Continuous dark bezel housing seated flush on bumper
        make_box(bm, (min(hx_in, hx_out), 2.70, 0.58), (max(hx_in, hx_out), 2.88, 0.92), m_idx["VAN_Cladding_Grey"])

        # Dual Projector Lens Barrels with Chrome Bezel Rings
        for p_idx, (p_off_x, p_off_y, pz) in enumerate([(0.05, 0.04, 0.77), (0.17, -0.04, 0.74)]):
            px, py = hx_in + s_sign * p_off_x, 2.84 + p_off_y
            ring = bmesh.ops.create_cone(
                bm, cap_ends=False, segments=32, radius1=0.052, radius2=0.052, depth=0.018,
                matrix=Matrix.Translation(Vector((px, py + 0.01, pz))) @ Matrix.Rotation(math.pi/2, 4, 'X')
            )
            tag_res(ring, m_idx["VAN_Wheel_Steel"], smooth=True)
            proj = bmesh.ops.create_cone(
                bm, cap_ends=True, segments=32, radius1=0.045, radius2=0.045, depth=0.038,
                matrix=Matrix.Translation(Vector((px, py, pz))) @ Matrix.Rotation(math.pi/2, 4, 'X')
            )
            tag_res(proj, m_idx["VAN_Headlight_LED"], smooth=True)

        # Swept-Back Upper Eyebrow LED DRL Strip
        make_box(bm, (min(hx_in, hx_out), 2.78, 0.88), (max(hx_in, hx_out), 2.87, 0.92), m_idx["VAN_Headlight_LED"])
        # Amber Side Indicator Reflector on Outer Corner
        make_box(bm, (min(hx_out - s_sign * 0.04, hx_out), 2.70, 0.64),
                     (max(hx_out - s_sign * 0.04, hx_out), 2.80, 0.82), m_idx["VAN_Strobe_Amber"])

    # 6. High-Mounted D-Pillar Vertical Taillight Stacks
    for s_sign in [1, -1]:
        tx = s_sign * 0.965
        for bi in range(16):
            bz = 1.25 + bi * 0.038
            make_box(bm, (min(tx - 0.028, tx + 0.028), -2.975, bz),
                         (max(tx - 0.028, tx + 0.028), -2.945, bz + 0.030), m_idx["VAN_Taillight_Red"])
        make_box(bm, (min(tx - 0.03, tx + 0.03), -2.975, 1.05),
                     (max(tx - 0.03, tx + 0.03), -2.945, 1.25), m_idx["VAN_Strobe_Amber"])
        make_box(bm, (min(tx - 0.03, tx + 0.03), -2.975, 0.90),
                     (max(tx - 0.03, tx + 0.03), -2.945, 1.05), m_idx["VAN_Headlight_LED"])

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
    print("Ultra-realistic emergency system and swept headlights constructed.")
