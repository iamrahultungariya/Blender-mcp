"""
Architectural Shell Prefab Kit:
- Stepped Plinth & Travertine Patio
- Multi-Layered Room Floors with Inlaid Concentric Mandala Medallion (Brahmasthan)
- Beveled Cutaway Walls with 75mm Skirting & LED Cove Capping Trim
- Modular Door Casings & Clean Thin Hinged Door Leaves (Zero Blockage)
- Multi-Pane Casement Windows with Beveled Sills and Mullions
- Semicircular Carved Indian Archway between Foyer and Living
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math
from ..core.mesh_utils import add_beveled_box, add_lathe_mesh, add_cylinder, add_fluted_panel, build_object_from_bmesh

def add_clean_door_leaf(bm, hinge_x, hinge_y, z, width, height, thickness=0.038, angle_deg=45, mat_wood=0, mat_handle=1):
    """
    Creates a realistic 38mm thin 4-panel door leaf swung ajar on its hinge.
    Uses pure matrix rotation around the hinge axis to ensure zero walkway obstruction.
    """
    rad = math.radians(angle_deg)
    rot_mat = Matrix.Rotation(rad, 4, 'Z')
    trans_mat = Matrix.Translation(Vector((hinge_x, hinge_y, z + height/2.0)))
    
    # 1. Main door leaf slab
    res = bmesh.ops.create_cube(bm, size=1.0)
    cube_verts = res['verts']
    
    local_mat = Matrix.Translation(Vector((width/2.0, 0, 0))) @ Matrix.Diagonal((width, thickness, height, 1.0))
    full_mat = trans_mat @ rot_mat @ local_mat
    bmesh.ops.transform(bm, verts=cube_verts, matrix=full_mat)
    
    cube_faces = [f for f in bm.faces if all(v in cube_verts for v in f.verts)]
    for f in cube_faces:
        f.material_index = mat_wood
        
    edges = [e for e in bm.edges if all(v in cube_verts for v in e.verts)]
    if edges:
        bmesh.ops.bevel(bm, geom=edges, offset=0.005, segments=2, profile=0.5, affect='EDGES')
            
    # 2. Brass Lever Handle & Backplate
    hx_local = width - 0.10
    hy_local = thickness/2.0 + 0.015
    hz_local = 0.95 - height/2.0
    
    handle_pos = trans_mat @ rot_mat @ Vector((hx_local, hy_local, hz_local))
    add_cylinder(bm, handle_pos.x, handle_pos.y, z + 0.95, 0.028, 0.015, segs=16, mat_idx=mat_handle)
    add_cylinder(bm, handle_pos.x, handle_pos.y, z + 0.965, 0.010, 0.035, segs=12, mat_idx=mat_handle)
    add_beveled_box(bm, handle_pos.x - 0.01, handle_pos.y - 0.01, z + 0.99, 0.02, 0.02, 0.015, bevel_r=0.003, segs=2, mat_idx=mat_handle)

def add_door_casing_and_leaf(bm, x1, y1, x2, y2, z, wall_t, open_angle=50, mat_casing=6, mat_leaf=6, mat_handle=7, mat_thresh=3):
    dx = x2 - x1
    dy = y2 - y1
    door_w = math.sqrt(dx*dx + dy*dy)
    door_h = 1.38
    
    if abs(dy) < 0.01:
        add_beveled_box(bm, x1 - 0.04, y1 - 0.01, z, 0.05, wall_t + 0.02, 1.45, bevel_r=0.008, segs=2, mat_idx=mat_casing)
        add_beveled_box(bm, x2 - 0.01, y1 - 0.01, z, 0.05, wall_t + 0.02, 1.45, bevel_r=0.008, segs=2, mat_idx=mat_casing)
        add_beveled_box(bm, x1, y1, z, door_w, wall_t, 0.03, bevel_r=0.004, segs=2, mat_idx=mat_thresh)
        add_clean_door_leaf(bm, x1 + 0.02, y1 + wall_t/2.0, z + 0.03, door_w - 0.04, door_h, thickness=0.038, angle_deg=open_angle, mat_wood=mat_leaf, mat_handle=mat_handle)
    else:
        add_beveled_box(bm, x1 - 0.01, y1 - 0.04, z, wall_t + 0.02, 0.05, 1.45, bevel_r=0.008, segs=2, mat_idx=mat_casing)
        add_beveled_box(bm, x1 - 0.01, y2 - 0.01, z, wall_t + 0.02, 0.05, 1.45, bevel_r=0.008, segs=2, mat_idx=mat_casing)
        add_beveled_box(bm, x1, y1, z, wall_t, door_w, 0.03, bevel_r=0.004, segs=2, mat_idx=mat_thresh)
        add_clean_door_leaf(bm, x1 + wall_t/2.0, y1 + 0.02, z + 0.03, door_w - 0.04, door_h, thickness=0.038, angle_deg=open_angle + 90, mat_wood=mat_leaf, mat_handle=mat_handle)

def generate_floors_and_plinth(mats, col):
    bm = bmesh.new()
    m_plinth = mats["Mat_Plinth"]
    m_marble = mats["Mat_Floor_Marble"]
    m_inlay = mats["Mat_Floor_Inlay"]
    m_wood_m = mats["Mat_Floor_Wood_Master"]
    m_wood_g = mats["Mat_Floor_Wood_Guest"]
    m_kitchen = mats["Mat_Floor_Kitchen"]
    m_bath = mats["Mat_Floor_Bath"]
    m_grass = mats["Mat_Lawn_Grass"]
    m_brass = mats["Mat_Brass_Gold"]
    
    mat_list = [m_plinth, m_marble, m_inlay, m_wood_m, m_wood_g, m_kitchen, m_bath, m_grass, m_brass]
    
    # 1. Outdoor Lawn Ground
    add_beveled_box(bm, -8.4, -8.0, -0.25, 16.8, 16.0, 0.08, bevel_r=0.04, segs=3, mat_idx=7)
    
    # 2. Main Plinth Platform
    add_beveled_box(bm, -6.6, -6.1, -0.17, 13.2, 12.2, 0.17, bevel_r=0.03, segs=3, mat_idx=0)
    
    # 3. Entrance Steps
    add_beveled_box(bm, 2.0, 5.5, -0.16, 2.0, 0.8, 0.08, bevel_r=0.02, segs=2, mat_idx=0)
    add_beveled_box(bm, 2.2, 5.5, -0.08, 1.6, 0.4, 0.08, bevel_r=0.02, segs=2, mat_idx=1)
    
    # 4. Room Floor Slabs
    # Master Bedroom (SW): Walnut parquet
    add_beveled_box(bm, -5.8, -5.3, 0.0, 4.8, 4.1, 0.02, bevel_r=0.005, segs=2, mat_idx=3)
    add_beveled_box(bm, -5.75, -5.25, 0.021, 4.7, 4.0, 0.003, bevel_r=0.002, segs=1, mat_idx=2)
    add_beveled_box(bm, -5.65, -5.15, 0.023, 4.5, 3.8, 0.002, bevel_r=0.002, segs=1, mat_idx=3)
    
    # Bathroom (West)
    add_beveled_box(bm, -5.8, -1.0, 0.0, 2.6, 2.2, 0.02, bevel_r=0.005, segs=2, mat_idx=6)
    
    # 2nd Bedroom (NW)
    add_beveled_box(bm, -5.8, 1.4, 0.0, 4.8, 3.9, 0.02, bevel_r=0.005, segs=2, mat_idx=4)
    
    # Kitchen & Dining (SE)
    add_beveled_box(bm, 1.0, -5.3, 0.0, 4.8, 5.1, 0.02, bevel_r=0.005, segs=2, mat_idx=5)
    
    # Living Room (NE)
    add_beveled_box(bm, 1.0, 0.0, 0.0, 4.8, 5.3, 0.02, bevel_r=0.005, segs=2, mat_idx=1)
    
    # Central Corridor & Foyer
    add_beveled_box(bm, -1.0, -5.3, 0.0, 2.0, 10.6, 0.02, bevel_r=0.005, segs=2, mat_idx=1)
    add_beveled_box(bm, -3.2, -1.2, 0.0, 2.2, 2.6, 0.02, bevel_r=0.005, segs=2, mat_idx=1)
    
    # 5. BRAHMASTHAN (Cosmic Center) Royal Mandala Medallion (High-Poly 16-Petal Inlay)
    add_cylinder(bm, 0.0, 0.0, 0.021, 1.20, 0.004, segs=48, mat_idx=2)
    add_cylinder(bm, 0.0, 0.0, 0.023, 1.00, 0.003, segs=48, mat_idx=1)
    add_cylinder(bm, 0.0, 0.0, 0.024, 0.75, 0.003, segs=48, mat_idx=2)
    add_cylinder(bm, 0.0, 0.0, 0.025, 0.55, 0.003, segs=48, mat_idx=1)
    
    for a in range(16):
        ang = 2 * math.pi * a / 16.0
        sx = 0.65 * math.cos(ang)
        sy = 0.65 * math.sin(ang)
        add_cylinder(bm, sx, sy, 0.026, 0.045, 0.003, segs=12, mat_idx=8)
    add_cylinder(bm, 0.0, 0.0, 0.027, 0.18, 0.005, segs=24, mat_idx=8)
    
    return build_object_from_bmesh("Arch_Floors_Plinth", bm, mat_list, col)

def generate_walls_and_openings(mats, col):
    bm = bmesh.new()
    m_ext = mats["Mat_Wall_Ext"]
    m_int = mats["Mat_Wall_Int"]
    m_accent = mats["Mat_Wall_Accent"]
    m_cap = mats["Mat_Wall_Cap"]
    m_skirting = mats["Mat_Skirting"]
    m_glass = mats["Mat_Glass_Clear"]
    m_teak = mats["Mat_Teak_Wood"]
    m_brass = mats["Mat_Brass_Gold"]
    
    mat_list = [m_ext, m_int, m_accent, m_cap, m_skirting, m_glass, m_teak, m_brass]
    
    wall_h = 1.45
    cap_h = 0.04
    t_ext = 0.22
    t_int = 0.15
    
    def wall_segment(x, y, z, sx, sy, sz, mat_idx=0, add_skirt=True):
        add_beveled_box(bm, x, y, z, sx, sy, sz, bevel_r=0.015, segs=3, mat_idx=mat_idx)
        add_beveled_box(bm, x - 0.025, y - 0.025, z + sz, sx + 0.05, sy + 0.05, cap_h, bevel_r=0.01, segs=2, mat_idx=3)
        add_beveled_box(bm, x - 0.015, y - 0.015, z + sz - 0.02, sx + 0.03, sy + 0.03, 0.015, bevel_r=0.003, segs=1, mat_idx=7)
        if add_skirt:
            add_beveled_box(bm, x - 0.008, y - 0.008, z, sx + 0.016, sy + 0.016, 0.08, bevel_r=0.004, segs=2, mat_idx=4)
            
    def window_assembly_x(x, y, length, sill_h=0.55, win_w=1.6):
        p1 = (length - win_w) / 2
        wall_segment(x, y, 0.0, p1, t_ext, wall_h, mat_idx=0)
        wall_segment(x + p1 + win_w, y, 0.0, p1, t_ext, wall_h, mat_idx=0)
        add_beveled_box(bm, x + p1, y, 0.0, win_w, t_ext, sill_h, bevel_r=0.01, segs=2, mat_idx=0)
        add_beveled_box(bm, x + p1 - 0.04, y - 0.03, sill_h, win_w + 0.08, t_ext + 0.06, 0.04, bevel_r=0.01, segs=2, mat_idx=3)
        add_beveled_box(bm, x + p1, y + t_ext/2 - 0.03, sill_h + 0.04, win_w, 0.06, wall_h - sill_h - 0.04, bevel_r=0.005, segs=2, mat_idx=6)
        add_beveled_box(bm, x + p1 + win_w/2 - 0.025, y + t_ext/2 - 0.035, sill_h + 0.04, 0.05, 0.07, wall_h - sill_h - 0.04, bevel_r=0.004, segs=2, mat_idx=6)
        add_beveled_box(bm, x + p1 + 0.03, y + t_ext/2 - 0.008, sill_h + 0.06, win_w/2 - 0.05, 0.016, wall_h - sill_h - 0.08, bevel_r=0.002, segs=1, mat_idx=5)
        add_beveled_box(bm, x + p1 + win_w/2 + 0.02, y + t_ext/2 - 0.008, sill_h + 0.06, win_w/2 - 0.05, 0.016, wall_h - sill_h - 0.08, bevel_r=0.002, segs=1, mat_idx=5)

    def window_assembly_y(x, y, length, sill_h=0.55, win_w=1.6):
        p1 = (length - win_w) / 2
        wall_segment(x, y, 0.0, t_ext, p1, wall_h, mat_idx=0)
        wall_segment(x, y + p1 + win_w, 0.0, t_ext, p1, wall_h, mat_idx=0)
        add_beveled_box(bm, x, y + p1, 0.0, t_ext, win_w, sill_h, bevel_r=0.01, segs=2, mat_idx=0)
        add_beveled_box(bm, x - 0.03, y + p1 - 0.04, sill_h, t_ext + 0.06, win_w + 0.08, 0.04, bevel_r=0.01, segs=2, mat_idx=3)
        add_beveled_box(bm, x + t_ext/2 - 0.03, y + p1, sill_h + 0.04, 0.06, win_w, wall_h - sill_h - 0.04, bevel_r=0.005, segs=2, mat_idx=6)
        add_beveled_box(bm, x + t_ext/2 - 0.035, y + p1 + win_w/2 - 0.025, sill_h + 0.04, 0.07, 0.05, wall_h - sill_h - 0.04, bevel_r=0.004, segs=2, mat_idx=6)
        add_beveled_box(bm, x + t_ext/2 - 0.008, y + p1 + 0.03, sill_h + 0.06, 0.016, win_w/2 - 0.05, wall_h - sill_h - 0.08, bevel_r=0.002, segs=1, mat_idx=5)
        add_beveled_box(bm, x + t_ext/2 - 0.008, y + p1 + win_w/2 + 0.02, sill_h + 0.06, 0.016, win_w/2 - 0.05, wall_h - sill_h - 0.08, bevel_r=0.002, segs=1, mat_idx=5)

    # 1. EXTERIOR PERIMETER
    # South Wall
    window_assembly_x(-6.0, -5.5, 5.0, sill_h=0.6, win_w=1.6)
    wall_segment(-1.0, -5.5, 0.0, 2.0, t_ext, wall_h, mat_idx=0)
    window_assembly_x(1.0, -5.5, 5.0, sill_h=0.7, win_w=1.4)
    
    # North Wall & Main Entrance
    window_assembly_x(-6.0, 5.3, 5.0, sill_h=0.6, win_w=1.6)
    wall_segment(-1.0, 5.3, 0.0, 2.0, t_ext, wall_h, mat_idx=0)
    wall_segment(1.0, 5.3, 0.0, 1.4, t_ext, wall_h, mat_idx=0)
    # Main Entrance Modular Door
    add_door_casing_and_leaf(bm, 2.4, 5.3, 3.4, 5.3, 0.0, t_ext, open_angle=55, mat_casing=6, mat_leaf=6, mat_handle=7, mat_thresh=3)
    window_assembly_x(3.4, 5.3, 2.6, sill_h=0.55, win_w=1.2)
    
    # West Wall
    window_assembly_y(-6.0, -5.3, 4.3, sill_h=0.6, win_w=1.4)
    wall_segment(-6.0, -1.0, 0.0, t_ext, 0.6, wall_h, mat_idx=0)
    add_beveled_box(bm, -6.0, -0.4, 0.9, t_ext, 0.8, 0.04, bevel_r=0.008, segs=2, mat_idx=3)
    add_beveled_box(bm, -6.0 + t_ext/2 - 0.01, -0.4, 0.94, 0.02, 0.8, wall_h - 0.94, bevel_r=0.002, segs=1, mat_idx=5)
    wall_segment(-6.0, 0.4, 0.0, t_ext, 0.8, wall_h, mat_idx=0)
    window_assembly_y(-6.0, 1.2, 4.1, sill_h=0.6, win_w=1.4)
    
    # East Wall
    window_assembly_y(5.8, -5.3, 5.1, sill_h=0.7, win_w=1.5)
    window_assembly_y(5.8, -0.2, 5.5, sill_h=0.5, win_w=2.0)
    
    # 2. INTERIOR PARTITIONS & MODULAR DOORS
    # Master Bedroom North Partition & Door
    wall_segment(-5.8, -1.2, 0.0, 3.8, t_int, wall_h, mat_idx=1)
    add_door_casing_and_leaf(bm, -2.0, -1.2, -1.1, -1.2, 0.0, t_int, open_angle=-50, mat_casing=6, mat_leaf=6, mat_handle=7, mat_thresh=3)
    wall_segment(-1.1, -1.2, 0.0, 0.1, t_int, wall_h, mat_idx=1)
    
    # Master Bedroom East Partition
    wall_segment(-1.0, -5.3, 0.0, t_int, 4.1, wall_h, mat_idx=1)
    
    # Bathroom East Partition & Door
    wall_segment(-3.2, -1.0, 0.0, t_int, 1.0, wall_h, mat_idx=1)
    add_door_casing_and_leaf(bm, -3.2, 0.0, -3.2, 0.9, 0.0, t_int, open_angle=45, mat_casing=6, mat_leaf=6, mat_handle=7, mat_thresh=3)
    wall_segment(-3.2, 0.9, 0.0, t_int, 0.3, wall_h, mat_idx=1)
    
    # Bathroom North Partition
    wall_segment(-5.8, 1.2, 0.0, 2.75, t_int, wall_h, mat_idx=1)
    
    # 2nd Bedroom South Partition
    wall_segment(-3.05, 1.25, 0.0, 2.05, t_int, wall_h, mat_idx=1)
    
    # 2nd Bedroom East Partition & Door
    add_door_casing_and_leaf(bm, -1.0, 1.4, -1.0, 2.3, 0.0, t_int, open_angle=45, mat_casing=6, mat_leaf=6, mat_handle=7, mat_thresh=3)
    wall_segment(-1.0, 2.3, 0.0, t_int, 3.0, wall_h, mat_idx=1)
    
    # Kitchen & Living Dividing Wall & Breakfast Pass
    wall_segment(4.0, -0.2, 0.0, 1.8, t_int, wall_h, mat_idx=1)
    add_beveled_box(bm, 2.0, -0.2, 0.0, 2.0, t_int, 0.88, bevel_r=0.015, segs=3, mat_idx=1)
    add_beveled_box(bm, 1.94, -0.24, 0.88, 2.12, t_int + 0.08, 0.05, bevel_r=0.015, segs=3, mat_idx=3)
    add_beveled_box(bm, 1.0, -0.2, 0.0, 1.0, t_int, 0.03, bevel_r=0.005, segs=2, mat_idx=3)
    
    # GRAND INDIAN ARCHWAY (Between Brahmasthan & Living)
    wall_segment(0.85, -5.3, 0.0, t_int, 2.3, wall_h, mat_idx=1)
    add_beveled_box(bm, 0.85, -3.0, 0.0, t_int, 1.0, 0.03, bevel_r=0.005, segs=2, mat_idx=3)
    wall_segment(0.85, -2.0, 0.0, t_int, 1.95, wall_h, mat_idx=1)
    
    add_fluted_panel(bm, 0.84, 0.50, 0.0, t_int + 0.02, 0.18, wall_h, num_flutes=5, axis='Y', segs_per_flute=12, mat_idx=6)
    add_fluted_panel(bm, 0.84, 2.32, 0.0, t_int + 0.02, 0.18, wall_h, num_flutes=5, axis='Y', segs_per_flute=12, mat_idx=6)
    add_beveled_box(bm, 0.85, 0.5, 0.0, t_int, 2.0, 0.03, bevel_r=0.005, segs=2, mat_idx=3)
    wall_segment(0.85, 2.5, 0.0, t_int, 2.8, wall_h, mat_idx=1)
    
    # Feature Accent Walls
    add_beveled_box(bm, 3.4, 5.22, 0.0, 1.2, 0.06, wall_h, bevel_r=0.01, segs=2, mat_idx=2)
    add_beveled_box(bm, -4.8, -5.28, 0.0, 2.8, 0.06, wall_h, bevel_r=0.01, segs=2, mat_idx=2)

    return build_object_from_bmesh("Arch_Walls_Cutaway", bm, mat_list, col)
