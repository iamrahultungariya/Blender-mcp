"""
Ambulance Builder - Ultra-Realistic Cladding, Grille, Tubular Push Bar & Wheel Arches (<170 LOC).
Procedural front bumper, anchored push bar, honeycomb grille, 32-seg arches, and diamond step.
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_cladding_and_bumpers(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    obj = bpy.data.objects.get("VAN_Cladding_Bumpers")
    if not obj:
        mesh = bpy.data.meshes.new("VAN_Cladding_Bumpers")
        obj = bpy.data.objects.new("VAN_Cladding_Bumpers", mesh)
        (target_col or bpy.context.scene.collection).objects.link(obj)
    mesh = obj.data

    for m_name in ["VAN_Cladding_Grey", "VAN_Paint_White", "VAN_Wheel_Steel", "VAN_Headlight_LED"]:
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

    # 1. Lower Side Protective Cladding (Z = 0.22 to 0.54)
    for s_sign in [1, -1]:
        cx = s_sign * 1.025
        x_min, x_max = min(cx - 0.02, cx + 0.02), max(cx - 0.02, cx + 0.02)
        make_box(bm, (x_min, 2.18, 0.22), (x_max, 2.70, 0.54), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (x_min, -1.48, 0.22), (x_max, 1.28, 0.54), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (x_min, -2.96, 0.22), (x_max, -2.38, 0.54), m_idx["VAN_Cladding_Grey"])
        make_box(bm, (x_min - 0.005, -2.94, 0.42), (x_max + 0.005, 2.68, 0.45), m_idx["VAN_Cladding_Grey"])

    # 2. Semicircular Molded Wheel Arch Trims (32 segments)
    arch_specs = [(1, 1.73), (-1, 1.73), (1, -1.93), (-1, -1.93)]
    for s_sign, y_pos in arch_specs:
        cx = s_sign * 1.025
        n_s = 32
        angles = [math.pi * i / n_s for i in range(n_s + 1)]
        v_out = [bm.verts.new((cx + s_sign * 0.025, y_pos + math.cos(a) * 0.44, 0.375 + math.sin(a) * 0.44)) for a in angles]
        v_in = [bm.verts.new((cx - s_sign * 0.05, y_pos + math.cos(a) * 0.41, 0.375 + math.sin(a) * 0.41)) for a in angles]
        for i in range(n_s):
            f = bm.faces.new([v_out[i], v_out[i+1], v_in[i+1], v_in[i]] if s_sign > 0 else
                             [v_out[i+1], v_out[i], v_in[i], v_in[i+1]])
            f.material_index = m_idx["VAN_Cladding_Grey"]
            f.smooth = True

    # 3. Sculpted Front Bumper, Grille & Honeycomb Mesh
    make_box(bm, (-1.02, 2.70, 0.24), (1.02, 2.96, 0.58), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.68, 2.82, 0.58), (0.68, 2.95, 0.94), m_idx["VAN_Cladding_Grey"])

    for gz in [0.66, 0.76, 0.86]:
        make_box(bm, (-0.65, 2.92, gz - 0.018), (0.65, 2.97, gz + 0.018), m_idx["VAN_Paint_White"])

    # Center Grille Logo Emblem Badge (48 segments)
    res_badge = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=48, radius1=0.082, radius2=0.082, depth=0.02,
        matrix=Matrix.Translation(Vector((0, 2.97, 0.76))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(res_badge, m_idx["VAN_Wheel_Steel"], smooth=True)

    # 36 Hexagonal Honeycomb Lower Intake Cells
    for hx in [-0.55, -0.44, -0.33, -0.22, -0.11, 0.0, 0.11, 0.22, 0.33, 0.44, 0.55]:
        for hz in [0.32, 0.38, 0.44]:
            cell = bmesh.ops.create_cone(
                bm, cap_ends=False, segments=6, radius1=0.038, radius2=0.038, depth=0.025,
                matrix=Matrix.Translation(Vector((hx, 2.955, hz))) @ Matrix.Rotation(math.pi/2, 4, 'X')
            )
            tag_res(cell, m_idx["VAN_Cladding_Grey"])

    # Front License Plate
    make_box(bm, (-0.26, 2.965, 0.32), (0.26, 2.975, 0.45), m_idx["VAN_Paint_White"])

    # Fog Lamp Housings & Projector lenses (32 segments)
    for s_sign in [1, -1]:
        make_box(bm, (min(s_sign * 0.74, s_sign * 0.90), 2.88, 0.32),
                     (max(s_sign * 0.74, s_sign * 0.90), 2.96, 0.45), m_idx["VAN_Cladding_Grey"])
        res_fog = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=32, radius1=0.042, radius2=0.042, depth=0.02,
            matrix=Matrix.Translation(Vector((s_sign * 0.82, 2.96, 0.385))) @ Matrix.Rotation(math.pi/2, 4, 'X')
        )
        tag_res(res_fog, m_idx["VAN_Headlight_LED"], smooth=True)

    # 4. Realistic Cylindrical Push Bar Anchored to Bumper (radius 28mm, 24 segs)
    tube_r = 0.028
    for s_sign in [1, -1]:
        upright = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=24, radius1=tube_r, radius2=tube_r, depth=0.52,
            matrix=Matrix.Translation(Vector((s_sign * 0.38, 2.99, 0.46)))
        )
        tag_res(upright, m_idx["VAN_Cladding_Grey"], smooth=True)
        # Heavy-Duty Steel Chassis Anchoring Bracket Flange
        make_box(bm, (s_sign * 0.38 - 0.03, 2.92, 0.36), (s_sign * 0.38 + 0.03, 2.99, 0.42), m_idx["VAN_Cladding_Grey"])

    # Lower Horizontal Tubular Crossbar
    bar_low = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=24, radius1=tube_r, radius2=tube_r, depth=0.82,
        matrix=Matrix.Translation(Vector((0.0, 2.99, 0.24))) @ Matrix.Rotation(math.pi/2, 4, 'Y')
    )
    tag_res(bar_low, m_idx["VAN_Cladding_Grey"], smooth=True)

    # Upper Horizontal Tubular Loop
    bar_high = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=24, radius1=tube_r, radius2=tube_r, depth=0.82,
        matrix=Matrix.Translation(Vector((0.0, 2.99, 0.68))) @ Matrix.Rotation(math.pi/2, 4, 'Y')
    )
    tag_res(bar_high, m_idx["VAN_Cladding_Grey"], smooth=True)

    # 5. Rear Step Bumper with 48 Non-Slip Diamond Plate Tread Studs
    make_box(bm, (-1.02, -3.12, 0.26), (1.02, -2.96, 0.52), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.75, -3.14, 0.48), (0.75, -2.98, 0.52), m_idx["VAN_Cladding_Grey"])
    make_box(bm, (-0.26, -3.00, 0.60), (0.26, -2.98, 0.72), m_idx["VAN_Paint_White"])

    for si in range(48):
        sx = -0.70 + si * 0.029
        stud = bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((sx, -3.06, 0.522))) @ Matrix.Diagonal((0.016, 0.042, 0.005, 1.0))
        )
        tag_res(stud, m_idx["VAN_Cladding_Grey"])

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
    print("Ultra-realistic cladding and bumper system constructed.")
