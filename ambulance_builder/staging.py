"""
Ambulance Builder - Staging, Ground Slab, Dedicated Camera Rig & Polycount Evaluator.
Creates the ambulance bay ground slab beside the bedroom and provides verification tools for 200k-350k budget.
"""
import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def build_ambulance_staging(base_offset=Vector((6.0, 0.0, 0.0)), target_col=None):
    # 1. Asphalt Ground Slab
    obj_slab = bpy.data.objects.get("AMB_Bay_Asphalt_Slab")
    if not obj_slab:
        mesh_slab = bpy.data.meshes.new("AMB_Bay_Asphalt_Slab")
        obj_slab = bpy.data.objects.new("AMB_Bay_Asphalt_Slab", mesh_slab)
        if target_col:
            target_col.objects.link(obj_slab)
        else:
            bpy.context.scene.collection.objects.link(obj_slab)
    mesh = obj_slab.data

    mat_asphalt = bpy.data.materials.get("AMB_Asphalt_Slab")
    mat_line = bpy.data.materials.get("AMB_Bay_Line_Yellow")
    for m in [mat_asphalt, mat_line]:
        if m and m.name not in mesh.materials:
            mesh.materials.append(m)
    mat_idx = {name: i for i, name in enumerate(mesh.materials.keys())}

    bm = bmesh.new()

    # Ground slab: 5.2m wide x 8.4m long x 0.06m thick
    min_v = (-2.6, -4.2, -0.06)
    max_v = (2.6, 4.2, 0.0)
    center = (Vector(min_v) + Vector(max_v)) * 0.5
    size_v = Vector(max_v) - Vector(min_v)
    res_slab = bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(center) @ Matrix.Diagonal((*size_v, 1.0))
    )
    for f in list({f for v in res_slab["verts"] for f in v.link_faces}):
        f.material_index = mat_idx.get("AMB_Asphalt_Slab", 0)
        f.smooth = False

    # Yellow Bay Parking Guide Lines
    for lx in [-2.2, 2.2]:
        line = bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((lx, 0.0, 0.002))) @ Matrix.Diagonal((0.14, 7.8, 0.004, 1.0))
        )
        for f in list({f for v in line["verts"] for f in v.link_faces}):
            f.material_index = mat_idx.get("AMB_Bay_Line_Yellow", 0)

    # Front Stop Bar
    bar = bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0.0, 3.8, 0.002))) @ Matrix.Diagonal((4.2, 0.18, 0.004, 1.0))
    )
    for f in list({f for v in bar["verts"] for f in v.link_faces}):
        f.material_index = mat_idx.get("AMB_Bay_Line_Yellow", 0)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    obj_slab.location = base_offset

    # 2. Camera Rig: Hero Front 3/4 & Rear 3/4
    cam_hero = bpy.data.objects.get("Camera_Ambulance_Hero")
    if not cam_hero:
        cam_data = bpy.data.cameras.new("Camera_Ambulance_Hero")
        cam_hero = bpy.data.objects.new("Camera_Ambulance_Hero", cam_data)
        if target_col:
            target_col.objects.link(cam_hero)
        else:
            bpy.context.scene.collection.objects.link(cam_hero)
    cam_hero.data.lens = 50.0
    cam_hero.location = base_offset + Vector((4.8, 5.0, 1.75))
    look_target = base_offset + Vector((0.0, 0.3, 1.25))
    cam_hero.rotation_euler = (look_target - cam_hero.location).to_track_quat('-Z', 'Y').to_euler()

    # Rear Camera
    cam_rear = bpy.data.objects.get("Camera_Ambulance_Rear")
    if not cam_rear:
        cam_data_r = bpy.data.cameras.new("Camera_Ambulance_Rear")
        cam_rear = bpy.data.objects.new("Camera_Ambulance_Rear", cam_data_r)
        if target_col:
            target_col.objects.link(cam_rear)
        else:
            bpy.context.scene.collection.objects.link(cam_rear)
    cam_rear.data.lens = 45.0
    cam_rear.location = base_offset + Vector((4.8, -5.6, 2.1))
    cam_rear.rotation_euler = ((base_offset + Vector((0.0, -1.0, 1.25))) - cam_rear.location).to_track_quat('-Z', 'Y').to_euler()

    # 3. Dedicated Lighting for Ambulance Bay
    for l_name, l_type, l_energy, l_loc, l_color in [
        ("Light_AMB_Key_Soft", 'AREA', 320.0, base_offset + Vector((4.0, 4.0, 4.5)), (1.0, 0.98, 0.95)),
        ("Light_AMB_Fill_Cool", 'AREA', 160.0, base_offset + Vector((-3.5, 2.5, 3.8)), (0.92, 0.96, 1.0)),
        ("Light_AMB_Rim_High", 'SUN', 2.8, base_offset + Vector((-4.0, -5.0, 6.0)), (1.0, 0.97, 0.92))
    ]:
        l_obj = bpy.data.objects.get(l_name)
        if not l_obj:
            light_data = bpy.data.lights.new(l_name, l_type)
            l_obj = bpy.data.objects.new(l_name, light_data)
            if target_col:
                target_col.objects.link(l_obj)
            else:
                bpy.context.scene.collection.objects.link(l_obj)
        l_obj.data.energy = l_energy
        l_obj.data.color = l_color
        l_obj.location = l_loc
        if hasattr(l_obj.data, "size"):
            l_obj.data.size = 2.8

    print("Staging, parking slab, lighting and camera rig configured.")

def evaluate_ambulance_budget():
    depsgraph = bpy.context.evaluated_depsgraph_get()
    amb_objects = [o for o in bpy.data.objects if o.name.startswith("VAN_")]
    print("\n--- AMBULANCE EVALUATED BUDGET REPORT ---")
    total_polys = 0
    total_tris = 0
    for obj in amb_objects:
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        polys = len(mesh.polygons)
        tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
        print(f"  {obj.name}: {polys} polygons, {tris} triangles")
        total_polys += polys
        total_tris += tris
        eval_obj.to_mesh_clear()

    print(f"\nTOTAL EVALUATED POLYGONS:  {total_polys}")
    print(f"TOTAL EVALUATED TRIANGLES: {total_tris}")
    print(f"BUDGET TARGET: 200,000 (Maximum allowable: 350,000)")
    return total_tris
