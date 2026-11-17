"""
Bedroom Suites Prefab Kit:
- Master Bedroom Suite (SW / Nairutya - Earth Element)
  * Fluted Channel-Tufted Velvet King Bed (13 High-Poly Curved Channels)
  * Lathe-Turned Spindle Nightstands & Urn Lamps
  * Fluted 4-Door Wardrobe & Tambour Vanity Desk
- Guest Bedroom & Study Suite (NW / Vayu - Air Element)
  * Queen Bed with Sage Upholstery
  * Ergonomic Study Desk & 5-Star Swivel Task Chair with Casters & Armrests
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math
from ..core.mesh_utils import add_beveled_box, add_lathe_mesh, add_cylinder, add_fluted_panel, build_object_from_bmesh

def generate_master_bedroom(mats, col):
    bm = bmesh.new()
    m_teak = mats["Mat_Teak_Wood"]
    m_navy = mats["Mat_Bed_Master_Navy"]
    m_white = mats["Mat_Bed_Linen_White"]
    m_mustard = mats["Mat_Fabric_Mustard"]
    m_brass = mats["Mat_Brass_Gold"]
    m_light = mats["Mat_Warm_Light"]
    m_rug = mats["Mat_Rug_Bedroom"]
    m_mirror = mats["Mat_Mirror"]
    
    mat_list = [m_teak, m_navy, m_white, m_mustard, m_brass, m_light, m_rug, m_mirror]
    
    # 1. Bedroom Area Rug (Plush beveled)
    add_beveled_box(bm, -4.8, -5.1, 0.021, 2.8, 3.2, 0.018, bevel_r=0.04, segs=3, mat_idx=6)
    
    # 2. Luxury King Bed (Headboard against South Wall: Center X = -3.4, Y = -5.2)
    add_beveled_box(bm, -4.55, -5.26, 0.02, 2.30, 0.12, 1.25, bevel_r=0.02, segs=3, mat_idx=0)
    # Fluted Velvet Headboard (13 High-Poly Channels)
    add_fluted_panel(bm, -4.48, -5.22, 0.25, 2.16, 0.06, 0.95, num_flutes=13, axis='X', segs_per_flute=16, mat_idx=1)
    
    # Bed Frame with Beveled Chamfers
    add_beveled_box(bm, -4.42, -5.16, 0.02, 2.04, 2.12, 0.32, bevel_r=0.03, segs=3, mat_idx=0)
    for bx, by in [(-4.40, -5.14), (-2.40, -5.14), (-4.40, -3.06), (-2.40, -3.06)]:
        add_cylinder(bm, bx, by, 0.02, 0.03, 0.08, segs=16, mat_idx=4)
        
    # Deep Mattress with Rounded Bullnose Corners
    add_beveled_box(bm, -4.36, -5.10, 0.34, 1.92, 2.02, 0.26, bevel_r=0.05, segs=4, mat_idx=2)
    # Draped Navy Duvet Quilt
    add_beveled_box(bm, -4.38, -4.60, 0.36, 1.96, 1.48, 0.26, bevel_r=0.06, segs=4, mat_idx=1)
    add_beveled_box(bm, -4.39, -3.80, 0.63, 1.98, 0.45, 0.025, bevel_r=0.015, segs=2, mat_idx=3)
    
    # 4 Plush Pillows with Soft Piping
    add_beveled_box(bm, -4.26, -4.96, 0.61, 0.76, 0.46, 0.14, bevel_r=0.06, segs=4, mat_idx=2)
    add_beveled_box(bm, -3.32, -4.96, 0.61, 0.76, 0.46, 0.14, bevel_r=0.06, segs=4, mat_idx=2)
    add_beveled_box(bm, -4.20, -4.86, 0.66, 0.66, 0.36, 0.12, bevel_r=0.05, segs=3, mat_idx=1)
    add_beveled_box(bm, -3.26, -4.86, 0.66, 0.66, 0.36, 0.12, bevel_r=0.05, segs=3, mat_idx=3)
    
    # 3. Nightstands with Lathe Spindle Legs & Urn Lamps
    for nx in [-5.15, -2.15]:
        add_beveled_box(bm, nx, -5.20, 0.30, 0.55, 0.45, 0.24, bevel_r=0.02, segs=3, mat_idx=0)
        for lx, ly in [(nx + 0.06, -5.14), (nx + 0.49, -5.14), (nx + 0.06, -4.81), (nx + 0.49, -4.81)]:
            leg_prof = [(0.022, 0.0), (0.018, 0.08), (0.014, 0.22), (0.020, 0.30)]
            add_lathe_mesh(bm, lx, ly, 0.02, leg_prof, segs=16, mat_idx=0)
            add_cylinder(bm, lx, ly, 0.02, 0.023, 0.06, segs=16, mat_idx=4)
        add_cylinder(bm, nx + 0.275, -4.74, 0.42, 0.012, 0.02, segs=12, mat_idx=4)
        
        lamp_x, lamp_y = nx + 0.275, -4.95
        lamp_prof = [
            (0.08, 0.0), (0.09, 0.02), (0.05, 0.06), (0.09, 0.14), (0.07, 0.20),
            (0.04, 0.24), (0.05, 0.26), (0.02, 0.28), (0.02, 0.32)
        ]
        add_lathe_mesh(bm, lamp_x, lamp_y, 0.54, lamp_prof, segs=24, mat_idx=4)
        shade_prof = [(0.14, 0.30), (0.09, 0.48)]
        add_lathe_mesh(bm, lamp_x, lamp_y, 0.54, shade_prof, segs=24, mat_idx=5)
        
    # 4. Master Wardrobe (West Wall)
    add_beveled_box(bm, -5.72, -3.85, 0.02, 0.68, 2.30, 1.42, bevel_r=0.02, segs=3, mat_idx=0)
    for i in range(4):
        dy = -3.85 + i * 0.575
        add_fluted_panel(bm, -5.03, dy + 0.03, 0.06, 0.02, 0.51, 1.30, num_flutes=8, axis='Y', segs_per_flute=12, mat_idx=0)
        add_cylinder(bm, -5.01, dy + 0.48, 0.55, 0.012, 0.35, segs=12, mat_idx=4)
        
    # 5. Tambour Vanity Console
    add_beveled_box(bm, -1.50, -3.65, 0.02, 0.46, 1.05, 0.76, bevel_r=0.03, segs=3, mat_idx=0)
    add_fluted_panel(bm, -1.48, -3.60, 0.15, 0.02, 0.95, 0.55, num_flutes=14, axis='Y', segs_per_flute=12, mat_idx=0)
    # Oval Backlit Mirror
    mirror_x, mirror_y = -1.12, -3.12
    add_cylinder(bm, mirror_x, mirror_y, 0.90, 0.32, 0.03, segs=32, mat_idx=4)
    add_cylinder(bm, mirror_x - 0.01, mirror_y, 0.90, 0.30, 0.02, segs=32, mat_idx=7)
    
    # Cylindrical Velvet Pouf with Brass Ring
    add_cylinder(bm, -1.90, -3.12, 0.02, 0.22, 0.06, segs=24, mat_idx=4)
    add_cylinder(bm, -1.90, -3.12, 0.08, 0.20, 0.38, segs=24, mat_idx=3)
    
    return build_object_from_bmesh("Furn_Master_Bedroom_SW", bm, mat_list, col)

def generate_guest_bedroom(mats, col):
    bm = bmesh.new()
    m_light_wood = mats["Mat_Light_Wood"]
    m_teak = mats["Mat_Teak_Wood"]
    m_sage = mats["Mat_Bed_Guest_Sage"]
    m_white = mats["Mat_Bed_Linen_White"]
    m_teal = mats["Mat_Fabric_Teal"]
    m_chrome = mats["Mat_Chrome"]
    m_light = mats["Mat_Warm_Light"]
    m_screen = mats["Mat_TV_Display"]
    m_rug = mats["Mat_Rug_Bedroom"]
    
    mat_list = [m_light_wood, m_teak, m_sage, m_white, m_teal, m_chrome, m_light, m_screen, m_rug]
    
    # 1. Floor Rug
    add_beveled_box(bm, -5.2, 2.0, 0.021, 2.4, 2.6, 0.018, bevel_r=0.04, segs=3, mat_idx=8)
    
    # 2. Queen Bed
    add_beveled_box(bm, -5.76, 2.30, 0.02, 0.12, 1.84, 1.10, bevel_r=0.02, segs=3, mat_idx=1)
    add_fluted_panel(bm, -5.72, 2.40, 0.25, 0.05, 1.64, 0.80, num_flutes=11, axis='Y', segs_per_flute=14, mat_idx=2)
    add_beveled_box(bm, -5.64, 2.38, 0.02, 2.06, 1.68, 0.30, bevel_r=0.03, segs=3, mat_idx=0)
    add_beveled_box(bm, -5.58, 2.44, 0.32, 1.96, 1.56, 0.24, bevel_r=0.05, segs=4, mat_idx=3)
    add_beveled_box(bm, -5.10, 2.42, 0.34, 1.46, 1.60, 0.24, bevel_r=0.06, segs=4, mat_idx=2)
    add_beveled_box(bm, -4.10, 2.40, 0.59, 0.40, 1.62, 0.025, bevel_r=0.015, segs=2, mat_idx=4)
    
    # Pillows
    add_beveled_box(bm, -5.50, 2.54, 0.56, 0.46, 0.62, 0.13, bevel_r=0.05, segs=3, mat_idx=3)
    add_beveled_box(bm, -5.50, 3.24, 0.56, 0.46, 0.62, 0.13, bevel_r=0.05, segs=3, mat_idx=3)
    add_beveled_box(bm, -5.34, 2.66, 0.61, 0.36, 0.46, 0.11, bevel_r=0.04, segs=3, mat_idx=4)
    
    # Nightstand
    add_beveled_box(bm, -5.72, 4.22, 0.02, 0.52, 0.46, 0.52, bevel_r=0.02, segs=3, mat_idx=0)
    lamp_prof = [(0.06, 0.0), (0.08, 0.03), (0.03, 0.15), (0.02, 0.24)]
    add_lathe_mesh(bm, -5.46, 4.45, 0.54, lamp_prof, segs=20, mat_idx=5)
    shade_prof = [(0.12, 0.22), (0.08, 0.38)]
    add_lathe_mesh(bm, -5.46, 4.45, 0.54, shade_prof, segs=20, mat_idx=6)
    
    # 3. Work-From-Home Study Station
    add_beveled_box(bm, -3.00, 4.80, 0.02, 1.55, 0.50, 0.74, bevel_r=0.02, segs=3, mat_idx=0)
    add_beveled_box(bm, -2.95, 4.82, 0.06, 0.38, 0.45, 0.64, bevel_r=0.015, segs=2, mat_idx=1)
    
    # 5-Star Swivel Task Chair with Casters & Armrests
    cx, cy = -2.20, 4.40
    for i in range(5):
        ang = 2 * math.pi * i / 5.0
        bx = cx + 0.26 * math.cos(ang)
        by = cy + 0.26 * math.sin(ang)
        add_cylinder(bm, (cx + bx)/2, (cy + by)/2, 0.04, 0.015, 0.03, segs=12, mat_idx=5)
        add_cylinder(bm, bx, by, 0.02, 0.025, 0.04, segs=12, mat_idx=5)
    add_cylinder(bm, cx, cy, 0.06, 0.025, 0.38, segs=16, mat_idx=5)
    add_beveled_box(bm, cx - 0.22, cy - 0.20, 0.44, 0.44, 0.42, 0.08, bevel_r=0.03, segs=3, mat_idx=4)
    add_beveled_box(bm, cx - 0.20, cy - 0.22, 0.52, 0.40, 0.06, 0.42, bevel_r=0.03, segs=3, mat_idx=4)
    # Armrests
    add_cylinder(bm, cx - 0.20, cy, 0.46, 0.012, 0.18, segs=8, mat_idx=5)
    add_cylinder(bm, cx + 0.20, cy, 0.46, 0.012, 0.18, segs=8, mat_idx=5)
    add_beveled_box(bm, cx - 0.22, cy - 0.12, 0.64, 0.04, 0.24, 0.02, bevel_r=0.005, mat_idx=4)
    add_beveled_box(bm, cx + 0.18, cy - 0.12, 0.64, 0.04, 0.24, 0.02, bevel_r=0.005, mat_idx=4)
    
    # Open Laptop
    add_beveled_box(bm, -2.32, 4.88, 0.76, 0.34, 0.23, 0.015, bevel_r=0.005, segs=2, mat_idx=5)
    add_beveled_box(bm, -2.32, 5.10, 0.77, 0.34, 0.015, 0.22, bevel_r=0.005, segs=2, mat_idx=7)
    
    # 4. Wardrobe
    add_beveled_box(bm, -1.50, 2.00, 0.02, 0.46, 1.45, 1.40, bevel_r=0.02, segs=3, mat_idx=0)
    add_fluted_panel(bm, -1.48, 2.05, 0.06, 0.02, 0.64, 1.30, num_flutes=7, axis='Y', segs_per_flute=12, mat_idx=1)
    add_fluted_panel(bm, -1.48, 2.75, 0.06, 0.02, 0.64, 1.30, num_flutes=7, axis='Y', segs_per_flute=12, mat_idx=1)
    
    return build_object_from_bmesh("Furn_Guest_Bedroom_NW", bm, mat_list, col)
