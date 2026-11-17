"""
Kitchen & Dining Suite Prefab Kit (SE / Agni - Fire Element):
- L-Shaped Modular Kitchen with Continuous 40mm Polished Black Granite Bullnose Edge
- 4-Burner Glass Hob with Cast-Iron Trivets (SE Corner, Cook faces East per Vastu)
- Sloped Stainless Chimney Hood
- Undermount Stainless Sink with Radiused Corners & Swept Chrome Faucet
- Dining Suite with Tapered Turned Legs & Ergonomic Curved Chairs
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math
from ..core.mesh_utils import add_beveled_box, add_lathe_mesh, add_cylinder, build_object_from_bmesh

def generate_kitchen_and_dining(mats, col):
    bm = bmesh.new()
    m_granite = mats["Mat_Granite_Black"]
    m_cabinet = mats["Mat_Cabinet_Offwhite"]
    m_teak = mats["Mat_Teak_Wood"]
    m_chrome = mats["Mat_Chrome"]
    m_brass = mats["Mat_Brass_Gold"]
    m_flame = mats["Mat_Diya_Flame"]
    m_ceramic = mats["Mat_Ceramic_White"]
    
    mat_list = [m_granite, m_cabinet, m_teak, m_chrome, m_brass, m_flame, m_ceramic]
    # 0: Granite, 1: Cabinet, 2: Teak, 3: Chrome, 4: Brass, 5: Flame, 6: Ceramic
    
    counter_h = 0.86
    counter_d = 0.65
    
    # 1. Lower Modular Cabinets (L-Shape) with Beveled Inset Doors
    add_beveled_box(bm, 2.00, -5.25, 0.02, 3.70, counter_d, counter_h - 0.04, bevel_r=0.015, segs=2, mat_idx=1)
    add_beveled_box(bm, 5.70 - counter_d, -4.60, 0.02, counter_d, 3.80, counter_h - 0.04, bevel_r=0.015, segs=2, mat_idx=1)
    
    for cx in [2.3, 3.0, 3.7, 4.4]:
        add_cylinder(bm, cx + 0.18, -4.58, counter_h * 0.6, 0.012, 0.32, segs=8, mat_idx=3)
    for cy in [-4.0, -3.2, -2.4, -1.6]:
        add_cylinder(bm, 5.03, cy + 0.18, counter_h * 0.6, 0.012, 0.32, segs=8, mat_idx=3)
        
    # 2. Continuous 40mm Polished Jet Black Granite Countertop with Bullnose Fillet
    add_beveled_box(bm, 1.95, -5.28, counter_h - 0.04, 3.80, counter_d + 0.05, 0.04, bevel_r=0.018, segs=3, mat_idx=0)
    add_beveled_box(bm, 5.70 - counter_d - 0.05, -4.60, counter_h - 0.04, counter_d + 0.05, 3.85, 0.04, bevel_r=0.018, segs=3, mat_idx=0)
    
    # 3. 4-Burner Tempered Glass Hob (SE Corner: X = 4.8, Y = -4.9, Cook faces East)
    add_beveled_box(bm, 4.48, -5.12, counter_h, 0.78, 0.52, 0.025, bevel_r=0.012, segs=2, mat_idx=0)
    for bx, by in [(4.65, -4.98), (4.65, -4.72), (5.05, -4.98), (5.05, -4.72)]:
        add_cylinder(bm, bx, by, counter_h + 0.025, 0.075, 0.018, segs=16, mat_idx=3)
        add_cylinder(bm, bx, by, counter_h + 0.043, 0.045, 0.010, segs=12, mat_idx=4)
        for a in range(4):
            ang = math.pi * a / 2.0
            px = bx + 0.06 * math.cos(ang)
            py = by + 0.06 * math.sin(ang)
            add_beveled_box(bm, px - 0.01, py - 0.01, counter_h + 0.04, 0.02, 0.02, 0.015, bevel_r=0.003, mat_idx=0)
    for ki in range(4):
        add_cylinder(bm, 4.60 + ki * 0.15, -5.14, counter_h + 0.012, 0.016, 0.02, segs=12, mat_idx=3)
        
    # 4. Sloped Stainless Chimney Hood
    add_beveled_box(bm, 4.42, -5.12, 1.25, 0.88, 0.50, 0.09, bevel_r=0.02, segs=2, mat_idx=3)
    add_cylinder(bm, 4.86, -5.02, 1.34, 0.12, 0.16, segs=16, mat_idx=3)
    
    # 5. Undermount Double Sink with Radiused Corners (NE of Kitchen)
    add_beveled_box(bm, 5.12, -1.85, counter_h - 0.18, 0.52, 0.74, 0.18, bevel_r=0.04, segs=2, mat_idx=3)
    faucet_prof = [
        (0.020, 0.00), (0.018, 0.18), (0.015, 0.26), (0.014, 0.32),
        (0.012, 0.34), (0.012, 0.28)
    ]
    add_lathe_mesh(bm, 5.58, -1.48, counter_h + 0.01, faucet_prof, segs=12, mat_idx=3)
    
    # 6. Refrigerator (SW of Kitchen)
    add_beveled_box(bm, 1.18, -5.22, 0.02, 0.74, 0.68, 1.48, bevel_r=0.03, segs=2, mat_idx=3)
    add_cylinder(bm, 1.54, -4.51, 0.60, 0.015, 0.48, segs=8, mat_idx=4)
    
    # 7. Dining Suite (Beveled Table with Tapered Lathe Legs & 4 Ergonomic Chairs)
    add_beveled_box(bm, 2.15, -2.95, 0.72, 1.42, 1.02, 0.045, bevel_r=0.015, segs=2, mat_idx=2)
    add_beveled_box(bm, 2.22, -2.88, 0.64, 1.28, 0.88, 0.08, bevel_r=0.01, mat_idx=2)
    for dx, dy in [(2.26, -2.84), (3.44, -2.84), (2.26, -2.04), (3.44, -2.04)]:
        dleg_prof = [(0.035, 0.0), (0.024, 0.25), (0.032, 0.64)]
        add_lathe_mesh(bm, dx, dy, 0.02, dleg_prof, segs=12, mat_idx=2)
        add_cylinder(bm, dx, dy, 0.02, 0.036, 0.06, segs=12, mat_idx=4)
        
    add_lathe_mesh(bm, 2.86, -2.44, 0.765, [(0.06, 0.0), (0.15, 0.08)], segs=16, mat_idx=4)
    add_cylinder(bm, 2.50, -2.44, 0.765, 0.12, 0.015, segs=16, mat_idx=6)
    add_cylinder(bm, 3.22, -2.44, 0.765, 0.12, 0.015, segs=16, mat_idx=6)
    
    # 4 Dining Chairs with Curved Ergonomic Backrests & Tapered Legs
    for cx in [2.45, 3.10]:
        add_beveled_box(bm, cx, -3.38, 0.44, 0.42, 0.42, 0.06, bevel_r=0.02, mat_idx=1)
        add_beveled_box(bm, cx + 0.02, -3.44, 0.50, 0.38, 0.05, 0.38, bevel_r=0.02, mat_idx=2)
        for legx, legy in [(cx + 0.04, -3.34), (cx + 0.38, -3.34), (cx + 0.04, -3.00), (cx + 0.38, -3.00)]:
            add_cylinder(bm, legx, legy, 0.02, 0.018, 0.42, segs=8, mat_idx=2)
    for cx in [2.45, 3.10]:
        add_beveled_box(bm, cx, -1.94, 0.44, 0.42, 0.42, 0.06, bevel_r=0.02, mat_idx=1)
        add_beveled_box(bm, cx + 0.02, -1.58, 0.50, 0.38, 0.05, 0.38, bevel_r=0.02, mat_idx=2)
        for legx, legy in [(cx + 0.04, -1.90), (cx + 0.38, -1.90), (cx + 0.04, -1.56), (cx + 0.38, -1.56)]:
            add_cylinder(bm, legx, legy, 0.02, 0.018, 0.42, segs=8, mat_idx=2)
            
    return build_object_from_bmesh("Furn_Kitchen_Dining_SE", bm, mat_list, col)
