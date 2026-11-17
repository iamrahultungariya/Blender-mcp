"""
Ambulance Builder - 3D Livery Decals, Battenburg Chevrons & Star of Life (~15k tris).
Procedural 1mm-offset geometric decals with red/yellow chevrons, Star of Life, and typography.
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_livery_decals(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    obj = bpy.data.objects.get("VAN_Livery_Decals")
    if not obj:
        mesh = bpy.data.meshes.new("VAN_Livery_Decals")
        obj = bpy.data.objects.new("VAN_Livery_Decals", mesh)
        if target_col:
            target_col.objects.link(obj)
        else:
            bpy.context.scene.collection.objects.link(obj)
    mesh = obj.data

    mat_names = ["VAN_Decal_Red", "VAN_Decal_Blue", "VAN_Decal_Yellow", "VAN_Decal_White"]
    for m_name in mat_names:
        m = bpy.data.materials.get(m_name)
        if m and m.name not in mesh.materials:
            mesh.materials.append(m)
    mat_idx = {name: i for i, name in enumerate(mesh.materials.keys())}

    bm = bmesh.new()

    def make_box(bm, min_v, max_v, m_idx, smooth=False):
        min_v = Vector(min_v)
        max_v = Vector(max_v)
        center = (min_v + max_v) * 0.5
        size_v = max_v - min_v
        res = bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(center) @ Matrix.Diagonal((*size_v, 1.0))
        )
        for f in list({f for v in res["verts"] for f in v.link_faces}):
            f.material_index = m_idx
            f.smooth = smooth
        return res

    def tag_res(res, m_idx, smooth=False):
        for f in list({f for v in res["verts"] for f in v.link_faces}):
            f.material_index = m_idx
            f.smooth = smooth

    # 1. High-Visibility Fluorescent Yellow & Red Side Chevrons (Battenburg Pattern)
    for side_sign in [1, -1]:
        dx_in = side_sign * 1.026
        dx_out = side_sign * 1.030
        x_min, x_max = min(dx_in, dx_out), max(dx_in, dx_out)

        # Main Fluorescent Yellow Waistline Band (Y = -2.75 to 1.65, Z = 0.96 to 1.18)
        make_box(bm, (x_min, -2.75, 0.96), (x_max, 1.65, 1.18), mat_idx["VAN_Decal_Yellow"])

        # Upper Narrow Blue Accent Stripe
        make_box(bm, (x_min, -2.75, 1.18), (x_max, 1.65, 1.21), mat_idx["VAN_Decal_Blue"])

        # Repeating 45-degree Forward Red Chevrons along the yellow band
        for cy in [-2.5, -2.1, -1.7, -1.3, -0.9, -0.5, -0.1, 0.3, 0.7, 1.1]:
            # Upper slash
            make_box(bm, (x_min - 0.001, cy - 0.08, 1.07), (x_max + 0.001, cy + 0.08, 1.17), mat_idx["VAN_Decal_Red"])
            # Lower slash (chevron fold)
            make_box(bm, (x_min - 0.001, cy - 0.02, 0.97), (x_max + 0.001, cy + 0.14, 1.07), mat_idx["VAN_Decal_Red"])

        # Roof-edge Fluorescent Yellow High-Vis Accent Line
        make_box(bm, (x_min, -2.70, 2.45), (x_max, 0.85, 2.52), mat_idx["VAN_Decal_Yellow"])
        # Three red angled hash marks at rear roof edge
        for hy in [-2.65, -2.55, -2.45]:
            make_box(bm, (x_min - 0.001, hy - 0.03, 2.46), (x_max + 0.001, hy + 0.03, 2.51), mat_idx["VAN_Decal_Red"])

    # 2. 6-Pointed Blue Star of Life with White Rod of Asclepius
    def add_star_of_life(bm, center_v, normal_axis, scale_s=0.36):
        for ang_deg in [0, 60, 120]:
            rad = math.radians(ang_deg)
            mat_rot = Matrix.Rotation(rad, 4, normal_axis)
            if normal_axis == 'X':
                s_mat = Matrix.Translation(center_v) @ mat_rot @ Matrix.Scale(0.003, 4, (1,0,0)) @ Matrix.Scale(scale_s*0.28, 4, (0,1,0)) @ Matrix.Scale(scale_s, 4, (0,0,1))
            else:
                s_mat = Matrix.Translation(center_v) @ mat_rot @ Matrix.Scale(scale_s*0.28, 4, (1,0,0)) @ Matrix.Scale(0.003, 4, (0,1,0)) @ Matrix.Scale(scale_s, 4, (0,0,1))
            res = bmesh.ops.create_cube(bm, size=1.0, matrix=s_mat)
            tag_res(res, mat_idx["VAN_Decal_Blue"])

        # White Rod of Asclepius staff
        staff = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=8, radius1=scale_s*0.038, radius2=scale_s*0.028, depth=scale_s*1.12,
            matrix=Matrix.Translation(center_v + (Vector((0.002, 0, 0)) if normal_axis == 'X' else Vector((0, -0.002, 0))))
        )
        tag_res(staff, mat_idx["VAN_Decal_White"])

    # Side Quarter Panels Star of Life
    add_star_of_life(bm, Vector((1.031, -1.35, 1.62)), 'X', scale_s=0.38)
    add_star_of_life(bm, Vector((-1.031, -1.35, 1.62)), 'X', scale_s=0.38)

    # Dual Rear Door Glass Star of Life
    add_star_of_life(bm, Vector((-0.46, -2.975, 1.74)), 'Y', scale_s=0.22)
    add_star_of_life(bm, Vector((0.46, -2.975, 1.74)), 'Y', scale_s=0.22)

    # Front Roof Brow Star of Life
    add_star_of_life(bm, Vector((0.0, 0.96, 2.38)), 'Y', scale_s=0.24)

    # 3. 3D Bold "AMBULANCE" Typography Graphic Blocks
    # Hood text (forward sloped)
    make_box(bm, (-0.45, 2.15, 1.10), (0.45, 2.32, 1.11), mat_idx["VAN_Decal_Red"])
    # Side door texts
    for side_sign in [1, -1]:
        sx = side_sign * 1.031
        make_box(bm, (min(sx, sx+0.002), -0.30, 0.90), (max(sx, sx+0.002), 0.70, 0.95), mat_idx["VAN_Decal_Blue"])

    # 4. Rear Lower Barn Doors 45° Diagonal Safety Hazard Chevrons (Red & White)
    for chi in range(6):
        cz = 0.52 + chi * 0.08
        c_mat = mat_idx["VAN_Decal_Red"] if chi % 2 == 0 else mat_idx["VAN_Decal_White"]
        # Left door
        make_box(bm, (-0.88, -2.975, cz), (-0.08, -2.970, cz + 0.075), c_mat)
        # Right door
        make_box(bm, (0.08, -2.975, cz), (0.88, -2.970, cz + 0.075), c_mat)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj.location = base_offset
    print("Livery decals constructed.")
