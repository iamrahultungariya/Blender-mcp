"""
Master Scene Assembler & Vastu Orchestration Engine.
Assembles all modular architectural and furniture prefabs into the live Blender scene.
"""

import bpy
import bmesh
import math
from mathutils import Matrix, Vector

from .core.materials import init_palette
from .core.mesh_utils import add_cylinder, add_beveled_box, build_object_from_bmesh, get_or_create_collection
from .prefabs.arch_kit import generate_floors_and_plinth, generate_walls_and_openings
from .prefabs.living_kit import generate_living_room_and_mandir
from .prefabs.bedroom_kit import generate_master_bedroom, generate_guest_bedroom
from .prefabs.kitchen_kit import generate_kitchen_and_dining
from .prefabs.bath_kit import generate_bathroom_sanitary

def cleanup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for collection in [bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights]:
        for block in collection:
            if block.users == 0:
                collection.remove(block)

def generate_vastu_compass(mats, col):
    bm = bmesh.new()
    m_brass = mats["Mat_Brass_Gold"]
    m_marble = mats["Mat_Floor_Marble"]
    m_teak = mats["Mat_Teak_Wood"]
    m_light = mats["Mat_Warm_Light"]
    
    mat_list = [m_brass, m_marble, m_teak, m_light]
    
    cx, cy, cz = 6.40, 5.80, 0.02
    radius = 1.05
    
    add_cylinder(bm, cx, cy, cz, radius, 0.03, segs=32, mat_idx=1)
    add_cylinder(bm, cx, cy, cz + 0.03, radius * 0.94, 0.012, segs=32, mat_idx=0)
    add_cylinder(bm, cx, cy, cz + 0.042, radius * 0.84, 0.012, segs=32, mat_idx=2)
    
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        px = cx + 0.78 * math.cos(rad)
        py = cy + 0.78 * math.sin(rad)
        add_beveled_box(bm, px - 0.04, py - 0.04, cz + 0.054, 0.08, 0.08, 0.025, bevel_r=0.01, mat_idx=0)
        
    nx, ny = cx, cy + 0.74
    add_beveled_box(bm, nx - 0.03, ny, cz + 0.065, 0.06, 0.22, 0.04, bevel_r=0.008, mat_idx=0)
    
    return build_object_from_bmesh("Vastu_Compass_Indicator", bm, mat_list, col)

def add_vastu_labels(mats, col):
    brass_mat = mats["Mat_Brass_Gold"]
    
    labels = [
        ("Label_Master", "✦ MASTER BEDROOM (SW / NAIRUTYA)", (-5.2, -3.2, 1.62), 0.22, brass_mat),
        ("Label_Living", "✦ LIVING & GUEST LOUNGE (NE / ISHANYA)", (1.4, 2.6, 1.62), 0.22, brass_mat),
        ("Label_Mandir", "✦ SACRED POOJA MANDIR (NE)", (4.8, 4.3, 1.62), 0.18, brass_mat),
        ("Label_Kitchen", "✦ KITCHEN & DINING (SE / AGNI)", (1.8, -3.8, 1.62), 0.22, brass_mat),
        ("Label_Guest", "✦ 2ND BEDROOM / STUDY (NW / VAYU)", (-5.2, 3.8, 1.62), 0.22, brass_mat),
        ("Label_Bath", "✦ RESTROOM & BATH (WEST / VARUNA)", (-5.4, 0.1, 1.62), 0.18, brass_mat),
        ("Label_Center", "✦ BRAHMASTHAN (OPEN HARMONY)", (-0.9, 0.2, 1.62), 0.20, brass_mat),
        ("Label_Entrance", "✦ MAIN ENTRANCE (NORTH-EAST)", (1.8, 5.65, 0.10), 0.22, brass_mat),
    ]
    
    for name, text, loc, size, mat in labels:
        font_curve = bpy.data.curves.new(type="FONT", name=name + "_data")
        font_curve.body = text
        font_curve.size = size
        font_curve.extrude = 0.02
        font_curve.bevel_depth = 0.003
        font_obj = bpy.data.objects.new(name, font_curve)
        font_obj.location = loc
        font_obj.rotation_euler = (math.radians(35.0), 0.0, math.radians(-15.0))
        if mat:
            font_obj.data.materials.append(mat)
        col.objects.link(font_obj)

def setup_lighting_and_cameras():
    col_light = get_or_create_collection("04_Lighting_Cameras")
    
    # Sun light (East / NE morning sun)
    sun_data = bpy.data.lights.new(name="Sun_Vastu", type='SUN')
    sun_data.energy = 5.5
    sun_data.color = (1.0, 0.96, 0.90)
    sun_data.angle = math.radians(8.0)
    sun_obj = bpy.data.objects.new(name="Sun_Vastu", object_data=sun_data)
    sun_obj.location = (10.0, 8.0, 14.0)
    sun_obj.rotation_euler = (math.radians(35.0), math.radians(-25.0), math.radians(45.0))
    col_light.objects.link(sun_obj)
    
    # Ambient fill lights
    room_lights = [
        ("Light_Living_NE", (3.4, 2.6, 3.2), (3.0, 3.0), 130.0, (1.0, 0.96, 0.92)),
        ("Light_Mandir_Ishanya", (5.1, 4.7, 1.8), (0.8, 0.8), 55.0, (1.0, 0.80, 0.45)),
        ("Light_Kitchen_SE", (3.4, -2.8, 3.0), (3.0, 3.0), 110.0, (1.0, 0.98, 0.95)),
        ("Light_Master_SW", (-3.4, -3.2, 3.0), (2.8, 2.8), 100.0, (1.0, 0.94, 0.86)),
        ("Light_Guest_NW", (-3.4, 3.3, 3.0), (2.8, 2.8), 100.0, (1.0, 0.96, 0.90)),
        ("Light_Bath_W", (-4.5, 0.1, 2.5), (1.5, 1.5), 70.0, (0.95, 0.98, 1.0)),
        ("Light_Brahmasthan_Center", (0.0, 0.0, 3.5), (2.0, 2.0), 90.0, (1.0, 0.97, 0.92))
    ]
    
    for name, loc, size, energy, color in room_lights:
        light_data = bpy.data.lights.new(name=name, type='AREA')
        light_data.energy = energy
        light_data.size = size[0]
        light_data.size_y = size[1]
        light_data.color = color
        light_obj = bpy.data.objects.new(name=name, object_data=light_data)
        light_obj.location = loc
        col_light.objects.link(light_obj)
        
    # Cameras
    cam1_data = bpy.data.cameras.new(name="Cam_Isometric_Southeast")
    cam1_data.lens = 42.0
    cam1_obj = bpy.data.objects.new(name="Cam_Isometric_Southeast", object_data=cam1_data)
    cam1_obj.location = (14.0, -13.0, 13.5)
    cam1_obj.rotation_euler = (math.radians(52.0), 0.0, math.radians(45.0))
    col_light.objects.link(cam1_obj)
    
    cam2_data = bpy.data.cameras.new(name="Cam_Isometric_Southwest")
    cam2_data.lens = 42.0
    cam2_obj = bpy.data.objects.new(name="Cam_Isometric_Southwest", object_data=cam2_data)
    cam2_obj.location = (-13.5, -13.5, 13.5)
    cam2_obj.rotation_euler = (math.radians(52.0), 0.0, math.radians(-45.0))
    col_light.objects.link(cam2_obj)
    
    cam3_data = bpy.data.cameras.new(name="Cam_TopDown_Floorplan")
    cam3_data.type = 'ORTHO'
    cam3_data.ortho_scale = 16.5
    cam3_obj = bpy.data.objects.new(name="Cam_TopDown_Floorplan", object_data=cam3_data)
    cam3_obj.location = (0.0, 0.0, 18.0)
    cam3_obj.rotation_euler = (0.0, 0.0, 0.0)
    col_light.objects.link(cam3_obj)
    
    bpy.context.scene.camera = cam1_obj

def assemble_scene():
    print("=========================================================")
    print("ASSEMBLING MODULAR VASTU 2BHK RESIDENCE (400k TRI TARGET)")
    print("=========================================================")
    
    cleanup_scene()
    mats = init_palette()
    
    col_arch = get_or_create_collection("01_Architecture")
    col_furn = get_or_create_collection("02_Furnishings")
    col_labels = get_or_create_collection("03_Vastu_Labels")
    
    print("-> 1. Instantiating Architectural Foundations & Mandala...")
    generate_floors_and_plinth(mats, col_arch)
    
    print("-> 2. Instantiating Walls, Windows, Architraves & Clean Doors...")
    generate_walls_and_openings(mats, col_arch)
    
    print("-> 3. Instantiating Living Lounge & Sacred Mandir Prefabs...")
    generate_living_room_and_mandir(mats, col_furn)
    
    print("-> 4. Instantiating Master Bedroom Suite Prefab (SW / Nairutya)...")
    generate_master_bedroom(mats, col_furn)
    
    print("-> 5. Instantiating Guest Bedroom & Study Workstation Prefabs (NW / Vayu)...")
    generate_guest_bedroom(mats, col_furn)
    
    print("-> 6. Instantiating Kitchen & Dining Suite Prefabs (SE / Agni)...")
    generate_kitchen_and_dining(mats, col_furn)
    
    print("-> 7. Instantiating Luxury Restroom & Sanitary Prefabs (West / Varuna)...")
    generate_bathroom_sanitary(mats, col_furn)
    
    print("-> 8. Instantiating Vastu Compass Rose...")
    generate_vastu_compass(mats, col_arch)
    
    print("-> 9. Adding Floating 3D Vastu Room Labels...")
    add_vastu_labels(mats, col_labels)
    
    print("-> 10. Setting up Lighting & Multi-Angle Cinematic Cameras...")
    setup_lighting_and_cameras()
    
    # Polygon / Triangle Audit
    total_polys = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    total_tris = sum(len(o.data.polygons)*2 for o in bpy.data.objects if o.type == 'MESH')
    print("---------------------------------------------------------")
    print(f"ASSEMBLY COMPLETE! Total Quads: {total_polys:,} | Total Triangles: {total_tris:,}")
    print("=========================================================")

if __name__ == "__main__":
    assemble_scene()
