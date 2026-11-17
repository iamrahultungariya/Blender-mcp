"""
Bathroom & Sanitary Prefab Kit (West / Varuna - Water Drainage & Waste Removal):
- Smooth D-Shaped Curved Ceramic Wall-Hung WC (Facing North-South per Vastu)
- Floating Vanity with Fluted Drawer Face & Curved Oval Ceramic Basin
- Walk-in Shower with Frameless Glass & Curved Rain Shower Head
- Tubular Chrome Towel Rail
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math
from ..core.mesh_utils import add_beveled_box, add_lathe_mesh, add_cylinder, add_fluted_panel, build_object_from_bmesh

def generate_bathroom_sanitary(mats, col):
    bm = bmesh.new()
    m_ceramic = mats["Mat_Ceramic_White"]
    m_chrome = mats["Mat_Chrome"]
    m_glass = mats["Mat_Glass_Clear"]
    m_mirror = mats["Mat_Mirror"]
    m_teak = mats["Mat_Teak_Wood"]
    m_tile = mats["Mat_Wall_Bath_Tile"]
    
    mat_list = [m_ceramic, m_chrome, m_glass, m_mirror, m_teak, m_tile]
    # 0: Ceramic, 1: Chrome, 2: Glass, 3: Mirror, 4: Teak, 5: Tile
    
    # 1. Wall-Hung D-Shaped Curved WC (West Wall: X = -5.5, Y = 0.2, Facing North-South)
    add_beveled_box(bm, -5.76, 0.04, 0.12, 0.22, 0.48, 0.74, bevel_r=0.015, segs=2, mat_idx=0)
    add_beveled_box(bm, -5.53, 0.18, 0.62, 0.02, 0.20, 0.14, bevel_r=0.005, mat_idx=1)
    wc_prof = [
        (0.18, 0.00), (0.21, 0.08), (0.22, 0.20), (0.21, 0.24)
    ]
    add_lathe_mesh(bm, -5.32, 0.28, 0.20, wc_prof, segs=16, mat_idx=0)
    add_cylinder(bm, -5.32, 0.28, 0.44, 0.22, 0.03, segs=16, mat_idx=0)
    
    # 2. Floating Vanity & Oval Ceramic Washbasin
    add_beveled_box(bm, -4.42, 0.70, 0.02, 1.04, 0.50, 0.78, bevel_r=0.02, segs=2, mat_idx=4)
    add_fluted_panel(bm, -4.40, 0.69, 0.15, 1.00, 0.02, 0.55, num_flutes=10, axis='X', mat_idx=4)
    
    # Oval Ceramic Vessel Basin
    add_lathe_mesh(bm, -3.90, 0.95, 0.80, [(0.14, 0.0), (0.24, 0.12)], segs=20, mat_idx=0)
    # Swept Chrome Faucet
    faucet_prof = [(0.018, 0.0), (0.015, 0.16), (0.012, 0.22), (0.012, 0.18)]
    add_lathe_mesh(bm, -3.90, 1.12, 0.80, faucet_prof, segs=12, mat_idx=1)
    
    # Backlit LED Rounded Mirror
    add_beveled_box(bm, -4.32, 1.18, 0.98, 0.84, 0.025, 0.44, bevel_r=0.04, segs=2, mat_idx=3)
    
    # 3. Walk-in Shower Enclosure
    add_beveled_box(bm, -4.26, -0.96, 0.02, 0.025, 0.82, 1.40, bevel_r=0.005, mat_idx=2)
    add_cylinder(bm, -4.25, -0.95, 0.30, 0.02, 0.04, segs=8, mat_idx=1)
    add_cylinder(bm, -4.25, -0.95, 1.10, 0.02, 0.04, segs=8, mat_idx=1)
    add_cylinder(bm, -5.60, -0.85, 1.36, 0.015, 0.38, segs=8, mat_idx=1)
    add_lathe_mesh(bm, -5.25, -0.85, 1.34, [(0.12, 0.0), (0.13, 0.02)], segs=16, mat_idx=1)
    
    # 4. Chrome Tubular Towel Rail with Folded Towel
    add_cylinder(bm, -3.36, -0.40, 0.85, 0.012, 0.52, segs=8, mat_idx=1)
    add_beveled_box(bm, -3.34, -0.36, 0.54, 0.025, 0.42, 0.34, bevel_r=0.015, segs=2, mat_idx=0)
    
    return build_object_from_bmesh("Sanitary_Bathroom_W", bm, mat_list, col)
