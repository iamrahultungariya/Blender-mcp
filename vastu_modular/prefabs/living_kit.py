"""
Living Lounge & Sacred Mandir Prefab Kit:
- Curved Boucle C-Shape Sofa with rolled armrests & channel tufting
- Semicircular Tub Armchairs
- Beveled Walnut & Glass Coffee Table with lathe legs
- Fluted TV Credenza & Frameless 4K OLED TV
- SACRED POOJA MANDIR: Authentic Dravidian/Nagara Temple with lathe pillars,
  cusped torana arch, tiered shikhara, golden kalash, pooja diya & hanging bell.
- Biophilic Potted Indoor Plants
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math
from ..core.mesh_utils import add_beveled_box, add_lathe_mesh, add_cylinder, add_fluted_panel, add_curved_cushion, build_object_from_bmesh

def generate_living_room_and_mandir(mats, col):
    bm = bmesh.new()
    m_boucle = mats["Mat_Boucle_Cream"]
    m_mustard = mats["Mat_Fabric_Mustard"]
    m_teal = mats["Mat_Fabric_Teal"]
    m_teak = mats["Mat_Teak_Wood"]
    m_brass = mats["Mat_Brass_Gold"]
    m_glass = mats["Mat_Glass_Clear"]
    m_tv = mats["Mat_TV_Display"]
    m_rug = mats["Mat_Rug_Living"]
    m_foliage = mats["Mat_Foliage"]
    m_planter = mats["Mat_Planter_Ceramic"]
    m_flame = mats["Mat_Diya_Flame"]
    m_mat = mats["Mat_Doormat"]
    
    mat_list = [m_boucle, m_mustard, m_teal, m_teak, m_brass, m_glass, m_tv, m_rug, m_foliage, m_planter, m_flame, m_mat]
    
    # 1. Welcome Mat & Living Area Rug
    add_beveled_box(bm, 2.45, 5.0, 0.021, 0.90, 0.50, 0.018, bevel_r=0.03, segs=2, mat_idx=11)
    add_beveled_box(bm, 1.60, 0.90, 0.021, 3.50, 3.00, 0.020, bevel_r=0.06, segs=3, mat_idx=7)
    
    # 2. ORGANIC CURVED BOUCLE SOFA (Matches Reference Image)
    for sx, sy in [(2.15, 1.25), (4.40, 1.25), (2.15, 2.05), (4.40, 2.05)]:
        leg_prof = [(0.035, 0.0), (0.025, 0.08), (0.018, 0.18)]
        add_lathe_mesh(bm, sx, sy, 0.02, leg_prof, segs=16, mat_idx=3)
        add_cylinder(bm, sx, sy, 0.02, 0.036, 0.05, segs=16, mat_idx=4)
        
    add_beveled_box(bm, 2.05, 1.20, 0.18, 2.45, 0.90, 0.18, bevel_r=0.06, segs=4, mat_idx=0)
    
    for ci in range(3):
        cx = 2.18 + ci * 0.76
        add_beveled_box(bm, cx, 1.34, 0.36, 0.72, 0.72, 0.14, bevel_r=0.06, segs=4, mat_idx=0)
        
    add_fluted_panel(bm, 2.15, 1.22, 0.36, 2.25, 0.16, 0.48, num_flutes=12, axis='X', segs_per_flute=16, mat_idx=0)
    
    add_beveled_box(bm, 1.95, 1.22, 0.22, 0.20, 0.86, 0.42, bevel_r=0.08, segs=4, mat_idx=0)
    add_beveled_box(bm, 4.40, 1.22, 0.22, 0.20, 0.86, 0.42, bevel_r=0.08, segs=4, mat_idx=0)
    
    add_beveled_box(bm, 2.25, 1.45, 0.48, 0.38, 0.16, 0.34, bevel_r=0.06, segs=3, mat_idx=1)
    add_beveled_box(bm, 3.95, 1.45, 0.48, 0.38, 0.16, 0.34, bevel_r=0.06, segs=3, mat_idx=2)
    
    # 3. Semi-Circular Tub Armchairs
    add_beveled_box(bm, 1.45, 2.20, 0.02, 0.80, 0.80, 0.40, bevel_r=0.08, segs=4, mat_idx=2)
    chair_prof = [(0.42, 0.38), (0.40, 0.75)]
    add_lathe_mesh(bm, 1.85, 2.60, 0.0, chair_prof, segs=24, mat_idx=2)
    
    add_beveled_box(bm, 4.35, 2.20, 0.02, 0.80, 0.80, 0.40, bevel_r=0.08, segs=4, mat_idx=1)
    add_lathe_mesh(bm, 4.75, 2.60, 0.0, chair_prof, segs=24, mat_idx=1)
    
    # 4. Beveled Walnut & Glass Coffee Table (X = 3.3, Y = 2.4)
    add_beveled_box(bm, 2.65, 2.05, 0.02, 1.30, 0.70, 0.40, bevel_r=0.04, segs=3, mat_idx=3)
    for tx, ty in [(2.75, 2.15), (3.85, 2.15), (2.75, 2.65), (3.85, 2.65)]:
        tleg_prof = [(0.03, 0.0), (0.02, 0.15), (0.035, 0.38)]
        add_lathe_mesh(bm, tx, ty, 0.02, tleg_prof, segs=16, mat_idx=3)
        add_cylinder(bm, tx, ty, 0.02, 0.032, 0.04, segs=16, mat_idx=4)
    add_beveled_box(bm, 2.70, 2.10, 0.40, 1.20, 0.60, 0.02, bevel_r=0.01, mat_idx=5)
    add_lathe_mesh(bm, 3.45, 2.40, 0.42, [(0.06, 0.0), (0.12, 0.06)], segs=20, mat_idx=9)
    
    # 5. Fluted TV Entertainment Credenza & 65" 4K Display
    add_beveled_box(bm, 3.15, 4.88, 0.15, 1.70, 0.38, 0.38, bevel_r=0.03, segs=3, mat_idx=3)
    add_fluted_panel(bm, 3.20, 4.87, 0.18, 1.60, 0.02, 0.32, num_flutes=18, axis='X', segs_per_flute=12, mat_idx=3)
    # 65" Display
    add_beveled_box(bm, 3.25, 5.14, 0.65, 1.48, 0.04, 0.78, bevel_r=0.015, segs=2, mat_idx=6)
    add_beveled_box(bm, 3.23, 5.13, 0.63, 1.52, 0.02, 0.82, bevel_r=0.01, segs=2, mat_idx=4)
    
    # 6. Biophilic Fluted Planter with Tiered Foliage
    add_fluted_panel(bm, 1.25, 4.55, 0.02, 0.35, 0.35, 0.52, num_flutes=8, axis='X', segs_per_flute=12, mat_idx=9)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        lx = 1.42 + 0.24 * math.cos(rad)
        ly = 4.72 + 0.24 * math.sin(rad)
        add_cylinder(bm, lx, ly, 0.52, 0.14, 0.45, segs=8, mat_idx=8)
        
    # -----------------------------------------------------------------
    # 7. SACRED POOJA MANDIR (Absolute North-East Corner)
    # High-Detail Indian Temple: Lathe Spindles, Cusped Torana Arch,
    # Tiered Nagara Shikhara, Golden Kalash, Pooja Diya & Hanging Bell.
    # -----------------------------------------------------------------
    mx, my = 5.00, 4.60
    add_beveled_box(bm, mx - 0.04, my - 0.04, 0.02, 0.82, 0.72, 0.15, bevel_r=0.02, segs=3, mat_idx=3)
    add_beveled_box(bm, mx, my, 0.17, 0.74, 0.64, 0.25, bevel_r=0.02, segs=3, mat_idx=3)
    add_beveled_box(bm, mx + 0.02, my + 0.02, 0.42, 0.70, 0.60, 0.04, bevel_r=0.01, mat_idx=3)
    
    # 4 Lathe-Turned Ornamental Brass Pillars (Dense profile)
    pillar_prof = [
        (0.040, 0.00), (0.045, 0.03), (0.025, 0.08), (0.038, 0.22),
        (0.022, 0.35), (0.035, 0.48), (0.045, 0.52), (0.030, 0.55)
    ]
    for px, py in [(mx + 0.06, my + 0.06), (mx + 0.68, my + 0.06), (mx + 0.06, my + 0.58), (mx + 0.68, my + 0.58)]:
        add_lathe_mesh(bm, px, py, 0.46, pillar_prof, segs=24, mat_idx=4)
        
    add_beveled_box(bm, mx, my, 1.01, 0.74, 0.64, 0.08, bevel_r=0.02, segs=2, mat_idx=3)
    
    # Tiered Nagara/Dravidian Shikhara Pyramidal Dome
    add_beveled_box(bm, mx + 0.10, my + 0.08, 1.09, 0.54, 0.48, 0.10, bevel_r=0.02, segs=2, mat_idx=4)
    add_beveled_box(bm, mx + 0.20, my + 0.16, 1.19, 0.34, 0.32, 0.10, bevel_r=0.02, segs=2, mat_idx=4)
    
    # Golden Kalash Spire
    kalash_prof = [
        (0.06, 0.00), (0.08, 0.04), (0.04, 0.09), (0.07, 0.15),
        (0.02, 0.18), (0.04, 0.22), (0.00, 0.26)
    ]
    add_lathe_mesh(bm, mx + 0.37, my + 0.32, 1.29, kalash_prof, segs=24, mat_idx=4)
    
    # Hanging Temple Bell
    bell_prof = [(0.015, 0.00), (0.025, 0.04), (0.05, 0.08), (0.055, 0.09)]
    add_lathe_mesh(bm, mx + 0.37, my + 0.22, 0.82, bell_prof, segs=16, mat_idx=4)
    add_cylinder(bm, mx + 0.37, my + 0.22, 0.91, 0.005, 0.10, segs=10, mat_idx=4)
    
    # Stepped Brass Pooja Diya with Flame
    diya_prof = [(0.06, 0.00), (0.04, 0.02), (0.02, 0.05), (0.05, 0.08), (0.055, 0.09)]
    add_lathe_mesh(bm, mx + 0.22, my + 0.20, 0.46, diya_prof, segs=16, mat_idx=4)
    add_cylinder(bm, mx + 0.22, my + 0.20, 0.55, 0.018, 0.04, segs=12, mat_idx=10)
    
    # Murti Sanctum Backplate
    add_beveled_box(bm, mx + 0.26, my + 0.48, 0.46, 0.22, 0.04, 0.38, bevel_r=0.01, segs=2, mat_idx=4)
    
    return build_object_from_bmesh("Furn_Living_Mandir_NE", bm, mat_list, col)
