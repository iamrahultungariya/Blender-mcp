"""
Ambulance Builder - Undercarriage Running Gear Silhouette (~8k tris).
Procedural ladder frame, 6 crossmembers, exhaust, differential, leaf springs, and shock bellows (Exterior Only).
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_chassis_and_interior(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    obj = bpy.data.objects.get("VAN_Chassis_Undercarriage")
    if not obj:
        mesh = bpy.data.meshes.new("VAN_Chassis_Undercarriage")
        obj = bpy.data.objects.new("VAN_Chassis_Undercarriage", mesh)
        if target_col:
            target_col.objects.link(obj)
        else:
            bpy.context.scene.collection.objects.link(obj)
    mesh = obj.data

    mat_names = ["VAN_Cladding_Grey", "VAN_Wheel_Steel", "VAN_Tire_Rubber"]
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

    def tag_res(res, m_idx, smooth=True):
        for f in list({f for v in res["verts"] for f in v.link_faces}):
            f.material_index = m_idx
            f.smooth = smooth

    # 1. Dual Ladder Frame Rails (Length Y = -2.85 to +2.70, Z = 0.28 to 0.40)
    for x_c in [-0.48, 0.48]:
        make_box(bm, (x_c - 0.05, -2.85, 0.28), (x_c + 0.05, 2.70, 0.40), mat_idx["VAN_Cladding_Grey"])

    # 2. 6 Structural Crossmembers
    for y_c in [-2.75, -1.93, -1.0, 0.20, 1.40, 2.60]:
        make_box(bm, (-0.48, y_c - 0.04, 0.30), (0.48, y_c + 0.04, 0.38), mat_idx["VAN_Cladding_Grey"])

    # 3. Fuel Tank with Metal Mounting Straps
    make_box(bm, (-0.88, -0.70, 0.24), (-0.44, 0.65, 0.42), mat_idx["VAN_Cladding_Grey"])
    for y_strap in [-0.45, 0.0, 0.45]:
        make_box(bm, (-0.89, y_strap - 0.02, 0.23), (-0.43, y_strap + 0.02, 0.43), mat_idx["VAN_Wheel_Steel"])

    # 4. Exhaust System & Drive Shaft
    res_muffler = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=32, radius1=0.11, radius2=0.11, depth=0.72,
        matrix=Matrix.Translation(Vector((0.22, -0.15, 0.29))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(res_muffler, mat_idx["VAN_Wheel_Steel"], smooth=True)

    res_fpipe = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=24, radius1=0.035, radius2=0.035, depth=1.85,
        matrix=Matrix.Translation(Vector((0.22, 1.10, 0.32))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(res_fpipe, mat_idx["VAN_Wheel_Steel"], smooth=True)

    res_tpipe = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=24, radius1=0.032, radius2=0.032, depth=1.25,
        matrix=Matrix.Translation(Vector((0.26, -1.10, 0.33))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(res_tpipe, mat_idx["VAN_Wheel_Steel"], smooth=True)

    res_shaft = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=24, radius1=0.042, radius2=0.042, depth=2.85,
        matrix=Matrix.Translation(Vector((0.0, -0.25, 0.35))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(res_shaft, mat_idx["VAN_Wheel_Steel"], smooth=True)

    # 5. Rear Drive Axle Tube & Differential Pumpkin
    res_axle = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=32, radius1=0.045, radius2=0.045, depth=1.52,
        matrix=Matrix.Translation(Vector((0, -1.93, 0.375))) @ Matrix.Rotation(math.pi/2, 4, 'Y')
    )
    tag_res(res_axle, mat_idx["VAN_Cladding_Grey"], smooth=True)

    res_diff = bmesh.ops.create_cone(
        bm, cap_ends=True, segments=32, radius1=0.135, radius2=0.135, depth=0.22,
        matrix=Matrix.Translation(Vector((0, -1.93, 0.375))) @ Matrix.Rotation(math.pi/2, 4, 'X')
    )
    tag_res(res_diff, mat_idx["VAN_Cladding_Grey"], smooth=True)

    # Dual 5-Leaf Spring Stacks
    for sx in [-0.58, 0.58]:
        for li in range(5):
            lz = 0.30 - li * 0.016
            l_len = 1.05 - li * 0.14
            make_box(bm, (sx - 0.035, -1.93 - l_len * 0.5, lz), (sx + 0.035, -1.93 + l_len * 0.5, lz + 0.014), mat_idx["VAN_Wheel_Steel"])

    # 6. 4 Telescopic Shock Absorbers with Ribbed Accordion Dust Boots
    for sx, sy in [(-0.52, 1.73), (0.52, 1.73), (-0.52, -1.93), (0.52, -1.93)]:
        # Shock body cylinder
        shock = bmesh.ops.create_cone(
            bm, cap_ends=True, segments=16, radius1=0.026, radius2=0.026, depth=0.32,
            matrix=Matrix.Translation(Vector((sx, sy + 0.08, 0.45)))
        )
        tag_res(shock, mat_idx["VAN_Cladding_Grey"], smooth=True)
        # 6 Bellows rings
        for ri in range(6):
            ring = bmesh.ops.create_cone(
                bm, cap_ends=True, segments=16, radius1=0.034, radius2=0.034, depth=0.018,
                matrix=Matrix.Translation(Vector((sx, sy + 0.08, 0.36 + ri * 0.028)))
            )
            tag_res(ring, mat_idx["VAN_Tire_Rubber"], smooth=True)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj.location = base_offset
    print("Undercarriage running gear constructed (Exterior Only).")
