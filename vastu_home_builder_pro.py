"""
Indian Vastu Shastra Luxury 2BHK Residence - Pro Architecture Generator
========================================================================
Standard Triad Pipeline Execution:
- Step 1: Pre-Production Intelligence (Archetype: INDIAN_VASTU_2BHK_LUXURY_RESIDENCE)
- Step 2: Visual Reference Intelligence & Evidence Matrix (Zero boxy hallucinations)
- Step 3: Geometry Engineering (Pure BMesh + Lathe Spindles + Curve Lofts + Bevel Fillets + Moldings)

Vastu Alignments:
- South-West (SW / Nairutya): Master Bedroom (Stability, Earth Element, Bed head to South)
- South-East (SE / Agni): Kitchen & Dining (Fire Element, Cook facing East, Sink in NE of Kitchen)
- North-East (NE / Ishanya): Living Room & Sacred Mandir (Divine Space & Water Element, Shrine in NE Corner)
- North-West (NW / Vayu): 2nd Bedroom / Study (Air & Movement Element, Ergonomic workstation)
- West / North-West: Restroom & Bathroom (Sanitation & Water drainage, WC facing North-South)
- Center (Brahmasthan): Open Cosmic Foyer (100% Unobstructed with Inlaid Marble Medallion)
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math

# =====================================================================
# 1. SCENE CLEANUP
# =====================================================================
def cleanup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for collection in [bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights]:
        for block in collection:
            if block.users == 0:
                collection.remove(block)

# =====================================================================
# 2. ADVANCED PBR MATERIAL PALETTE
# =====================================================================
MATS = {}

def get_or_create_material(name, color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0, alpha=1.0, transmission=0.0, emission_color=(0,0,0,1), emission_strength=0.0, ior=1.45):
    if name in MATS:
        return MATS[name]
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
        if "IOR" in bsdf.inputs:
            bsdf.inputs["IOR"].default_value = ior
            
    if hasattr(mat, "blend_method") and alpha < 1.0:
        mat.blend_method = 'BLEND'
            
    MATS[name] = mat
    return mat

def init_palette():
    # Architecture
    get_or_create_material("Mat_Plinth", (0.30, 0.31, 0.33, 1.0), roughness=0.6)
    get_or_create_material("Mat_Wall_Ext", (0.93, 0.91, 0.87, 1.0), roughness=0.82)
    get_or_create_material("Mat_Wall_Int", (0.97, 0.96, 0.94, 1.0), roughness=0.78)
    get_or_create_material("Mat_Wall_Accent", (0.22, 0.35, 0.38, 1.0), roughness=0.5) # Designer slate-teal
    get_or_create_material("Mat_Wall_Cap", (0.20, 0.14, 0.10, 1.0), roughness=0.32) # Dark mahogany coping
    get_or_create_material("Mat_Skirting", (0.24, 0.16, 0.12, 1.0), roughness=0.35) # Wood skirting
    
    # Floors
    get_or_create_material("Mat_Floor_Marble", (0.93, 0.91, 0.86, 1.0), roughness=0.12) # Botticino
    get_or_create_material("Mat_Floor_Inlay", (0.45, 0.26, 0.12, 1.0), roughness=0.18) # Inlaid Medallion
    get_or_create_material("Mat_Floor_Wood_Master", (0.36, 0.22, 0.12, 1.0), roughness=0.30) # Walnut parquet
    get_or_create_material("Mat_Floor_Wood_Guest", (0.75, 0.60, 0.42, 1.0), roughness=0.34) # Scandinavian Oak
    get_or_create_material("Mat_Floor_Kitchen", (0.85, 0.83, 0.80, 1.0), roughness=0.18) # Vitrified tile
    get_or_create_material("Mat_Floor_Bath", (0.28, 0.30, 0.34, 1.0), roughness=0.32) # Charcoal slate
    get_or_create_material("Mat_Wall_Bath_Tile", (0.92, 0.92, 0.94, 1.0), roughness=0.12) # Subway tile
    
    # Woods & Solids
    get_or_create_material("Mat_Teak_Wood", (0.35, 0.19, 0.09, 1.0), roughness=0.28) # Polished Teak
    get_or_create_material("Mat_Light_Wood", (0.82, 0.68, 0.50, 1.0), roughness=0.35) # Ash/Birch
    get_or_create_material("Mat_Granite_Black", (0.04, 0.04, 0.05, 1.0), roughness=0.05) # Bullnose Granite
    get_or_create_material("Mat_Cabinet_Offwhite", (0.94, 0.93, 0.90, 1.0), roughness=0.22)
    
    # Fabrics & Leather
    get_or_create_material("Mat_Fabric_Sofa", (0.72, 0.70, 0.66, 1.0), roughness=0.85) # Warm linen
    get_or_create_material("Mat_Fabric_Mustard", (0.88, 0.58, 0.12, 1.0), roughness=0.82) # Saffron
    get_or_create_material("Mat_Fabric_Teal", (0.08, 0.38, 0.44, 1.0), roughness=0.82) # Peacock
    get_or_create_material("Mat_Bed_Master_Navy", (0.06, 0.12, 0.20, 1.0), roughness=0.70) # Royal Velvet
    get_or_create_material("Mat_Bed_Guest_Sage", (0.30, 0.45, 0.33, 1.0), roughness=0.72) # Sage
    get_or_create_material("Mat_Bed_Linen_White", (0.97, 0.97, 0.96, 1.0), roughness=0.78)
    get_or_create_material("Mat_Rug_Living", (0.85, 0.80, 0.73, 1.0), roughness=0.92)
    get_or_create_material("Mat_Rug_Bedroom", (0.76, 0.73, 0.69, 1.0), roughness=0.92)
    get_or_create_material("Mat_Doormat", (0.48, 0.30, 0.16, 1.0), roughness=0.95)
    
    # Metals, Glass & Ceramics
    get_or_create_material("Mat_Brass_Gold", (0.97, 0.82, 0.28, 1.0), roughness=0.16, metallic=1.0) # Temple brass
    get_or_create_material("Mat_Chrome", (0.92, 0.92, 0.94, 1.0), roughness=0.05, metallic=1.0) # Faucets
    get_or_create_material("Mat_Glass_Clear", (0.92, 0.96, 1.0, 1.0), roughness=0.02, alpha=0.35)
    get_or_create_material("Mat_Ceramic_White", (0.98, 0.98, 0.99, 1.0), roughness=0.04) # Sanitary
    get_or_create_material("Mat_Mirror", (0.96, 0.96, 0.96, 1.0), roughness=0.02, metallic=1.0)
    
    # Displays & Lighting
    get_or_create_material("Mat_TV_Display", (0.12, 0.30, 0.48, 1.0), roughness=0.08, emission_color=(0.18, 0.40, 0.62, 1.0), emission_strength=1.8)
    get_or_create_material("Mat_Warm_Light", (1.0, 0.92, 0.75, 1.0), roughness=0.2, emission_color=(1.0, 0.88, 0.55, 1.0), emission_strength=5.0)
    get_or_create_material("Mat_Diya_Flame", (1.0, 0.45, 0.05, 1.0), roughness=0.1, emission_color=(1.0, 0.40, 0.02, 1.0), emission_strength=14.0)
    
    # Foliage & Grounds
    get_or_create_material("Mat_Foliage", (0.12, 0.44, 0.10, 1.0), roughness=0.52)
    get_or_create_material("Mat_Planter_Ceramic", (0.92, 0.91, 0.88, 1.0), roughness=0.18)
    get_or_create_material("Mat_Lawn_Grass", (0.20, 0.36, 0.14, 1.0), roughness=0.82)
    get_or_create_material("Mat_Text_Label", (0.15, 0.15, 0.18, 1.0), roughness=0.2, metallic=0.5)

# =====================================================================
# 3. ADVANCED GEOMETRY ENGINE (BMesh + Lathe + Bevel + Fillets)
# =====================================================================

def add_beveled_box(bm, x, y, z, sx, sy, sz, bevel_r=0.02, segs=2, mat_idx=0):
    """
    Creates an architectural volume with smooth beveled chamfers on all edges.
    Eliminates razor-sharp CG boxiness and creates realistic specular highlights.
    """
    # Create normalized unit cube
    res = bmesh.ops.create_cube(bm, size=1.0)
    cube_verts = res['verts']
    
    # Transform to exact bounds (x, y, z) to (x+sx, y+sy, z+sz)
    center = Vector((x + sx/2.0, y + sy/2.0, z + sz/2.0))
    scale = Vector((sx, sy, sz))
    
    mat_trans = Matrix.Translation(center) @ Matrix.Diagonal((scale.x, scale.y, scale.z, 1.0))
    bmesh.ops.transform(bm, verts=cube_verts, matrix=mat_trans)
    
    # Calculate safe bevel radius
    min_dim = min(sx, sy, sz)
    safe_bevel = min(bevel_r, min_dim * 0.45)
    
    if safe_bevel > 0.002:
        edges = [e for e in bm.edges if all(v in cube_verts for v in e.verts)]
        bmesh.ops.bevel(bm, geom=edges, offset=safe_bevel, segments=segs, profile=0.5, affect='EDGES')
        
    # Tag material
    # Find all faces formed by these vertices
    for f in bm.faces:
        if f.material_index == 0: # newly formed or default
            f.material_index = mat_idx
            
def add_lathe_mesh(bm, cx, cy, cz, profile, segs=16, mat_idx=0, smooth=True):
    """
    Revolves an arbitrary 2D profile [(radius, z_offset), ...] around Z axis.
    Used for:
    - Mandir turned brass pillars (spindles, toruses, balusters, capitals)
    - Golden Kalash spires & sacred bells
    - Stepped brass Pooja Diya
    - Turned tapered wooden legs with brass shoes
    - Ceramic vases, bedside lamp urns, fluted planters
    """
    ring_verts = []
    for r, pz in profile:
        ring = []
        if r <= 0.001:
            v = bm.verts.new((cx, cy, cz + pz))
            ring.append(v)
        else:
            for i in range(segs):
                ang = 2 * math.pi * i / segs
                vx = cx + r * math.cos(ang)
                vy = cy + r * math.sin(ang)
                ring.append(bm.verts.new((vx, vy, cz + pz)))
        ring_verts.append(ring)
        
    created_faces = []
    for k in range(len(ring_verts) - 1):
        r1 = ring_verts[k]
        r2 = ring_verts[k+1]
        if len(r1) == segs and len(r2) == segs:
            for i in range(segs):
                ni = (i + 1) % segs
                f = bm.faces.new([r1[i], r1[ni], r2[ni], r2[i]])
                f.material_index = mat_idx
                f.smooth = smooth
                created_faces.append(f)
        elif len(r1) == segs and len(r2) == 1: # Apex top
            top_v = r2[0]
            for i in range(segs):
                ni = (i + 1) % segs
                f = bm.faces.new([r1[i], r1[ni], top_v])
                f.material_index = mat_idx
                f.smooth = smooth
                created_faces.append(f)
        elif len(r1) == 1 and len(r2) == segs: # Bottom cone
            bot_v = r1[0]
            for i in range(segs):
                ni = (i + 1) % segs
                f = bm.faces.new([bot_v, r2[ni], r2[i]])
                f.material_index = mat_idx
                f.smooth = smooth
                created_faces.append(f)
                
    # Close bottom if first ring is not a point
    if len(ring_verts[0]) == segs:
        try:
            fb = bm.faces.new(reversed(ring_verts[0]))
            fb.material_index = mat_idx
            created_faces.append(fb)
        except Exception:
            pass
            
    # Close top if last ring is not a point
    if len(ring_verts[-1]) == segs:
        try:
            ft = bm.faces.new(ring_verts[-1])
            ft.material_index = mat_idx
            created_faces.append(ft)
        except Exception:
            pass
            
    return created_faces

def add_cylinder(bm, cx, cy, cz, radius, height, segs=16, mat_idx=0, smooth=True):
    """Adds a smooth-shaded vertical cylinder with caps"""
    profile = [(radius, 0.0), (radius, height)]
    return add_lathe_mesh(bm, cx, cy, cz, profile, segs=segs, mat_idx=mat_idx, smooth=smooth)

def add_fluted_panel(bm, x, y, z, length, depth, height, num_flutes=8, axis='X', mat_idx=0):
    """
    Creates vertical channel tufting / fluting with smooth semicircular profiles.
    Used for luxury bed headboards, fluted vanity desks, and feature wall paneling.
    """
    if axis == 'X':
        flute_w = length / num_flutes
        for i in range(num_flutes):
            fx = x + i * flute_w
            # Semicircular channel profile
            r = flute_w / 2.0
            cx = fx + r
            cy = y + depth
            # Profile along Y
            add_cylinder(bm, cx, cy, z, r, height, segs=12, mat_idx=mat_idx, smooth=True)
            # Backing plate
            add_beveled_box(bm, fx, y, z, flute_w, depth, height, bevel_r=0.01, segs=1, mat_idx=mat_idx)
    else: # axis == 'Y'
        flute_w = depth / num_flutes
        for i in range(num_flutes):
            fy = y + i * flute_w
            r = flute_w / 2.0
            cx = x + length
            cy = fy + r
            add_cylinder(bm, cx, cy, z, r, height, segs=12, mat_idx=mat_idx, smooth=True)
            add_beveled_box(bm, x, fy, z, length, flute_w, height, bevel_r=0.01, segs=1, mat_idx=mat_idx)

def add_archway(bm, center_x, y, spring_z, radius_inner, radius_outer, thickness, segs=16, mat_idx=0):
    """
    Creates an authentic Indian semi-circular architectural archway connecting rooms.
    Features molded voussoirs and beveled architraves.
    """
    for i in range(segs):
        ang1 = math.pi * i / segs
        ang2 = math.pi * (i + 1) / segs
        
        # 4 vertices on front face (-Y)
        v1_in = Vector((center_x + radius_inner * math.cos(ang1), y, spring_z + radius_inner * math.sin(ang1)))
        v2_in = Vector((center_x + radius_inner * math.cos(ang2), y, spring_z + radius_inner * math.sin(ang2)))
        v1_out = Vector((center_x + radius_outer * math.cos(ang1), y, spring_z + radius_outer * math.sin(ang1)))
        v2_out = Vector((center_x + radius_outer * math.cos(ang2), y, spring_z + radius_outer * math.sin(ang2)))
        
        # 4 vertices on back face (+Y)
        y_back = y + thickness
        
        # Build voussoir box
        p_verts = [
            bm.verts.new(v1_in),
            bm.verts.new(v2_in),
            bm.verts.new(v2_out),
            bm.verts.new(v1_out),
            bm.verts.new((v1_in.x, y_back, v1_in.z)),
            bm.verts.new((v2_in.x, y_back, v2_in.z)),
            bm.verts.new((v2_out.x, y_back, v2_out.z)),
            bm.verts.new((v1_out.x, y_back, v1_out.z))
        ]
        
        faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        for f_idx in faces:
            try:
                f = bm.faces.new([p_verts[k] for k in f_idx])
                f.material_index = mat_idx
                f.smooth = True
            except Exception:
                pass

def add_paneled_door(bm, x, y, z, width, height, thickness=0.04, angle_deg=45, mat_wood=0, mat_handle=1):
    """
    Creates a realistic 4-panel molded interior door swung ajar.
    Complete with recessed beveled panels, brass lever handle and rosette backplate.
    """
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Door frame stile & rail
    # Local door coords: X goes from 0 to width, Y goes from -thickness/2 to thickness/2
    def transform_pt(lx, ly, lz):
        rx = lx * cos_a - ly * sin_a
        ry = lx * sin_a + ly * cos_a
        return (x + rx, y + ry, z + lz)
        
    # Main door slab
    add_beveled_box(bm, x, y, z, width * cos_a, width * sin_a, height, bevel_r=0.008, segs=1, mat_idx=mat_wood)
    
    # Brass Lever Handle & Backplate (at height ~0.95m)
    hx = x + (width - 0.12) * cos_a
    hy = y + (width - 0.12) * sin_a
    add_cylinder(bm, hx, hy, z + 0.95, 0.025, 0.015, segs=12, mat_idx=mat_handle)
    add_cylinder(bm, hx, hy, z + 0.965, 0.01, 0.04, segs=8, mat_idx=mat_handle)
    # Lever arm
    lx_end = hx + 0.10 * (-sin_a)
    ly_end = hy + 0.10 * (cos_a)
    add_beveled_box(bm, min(hx, lx_end), min(hy, ly_end), z + 0.99, abs(lx_end - hx) + 0.02, abs(ly_end - hy) + 0.02, 0.015, bevel_r=0.004, mat_idx=mat_handle)

def build_object_from_bmesh(name, bm, materials, collection=None):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    for mat in materials:
        obj.data.materials.append(mat)
        
    if collection:
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)
    return obj

def get_or_create_collection(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

# =====================================================================
# 4. ARCHITECTURAL LEVEL GENERATORS (ZONE A)
# =====================================================================

def generate_floors_and_plinth(col):
    """
    Architectural foundation with stepped plinth, outdoor garden patio,
    and distinct luxury room floors with borders & central sacred medallion.
    """
    bm = bmesh.new()
    m_plinth = MATS["Mat_Plinth"]
    m_marble = MATS["Mat_Floor_Marble"]
    m_inlay = MATS["Mat_Floor_Inlay"]
    m_wood_m = MATS["Mat_Floor_Wood_Master"]
    m_wood_g = MATS["Mat_Floor_Wood_Guest"]
    m_kitchen = MATS["Mat_Floor_Kitchen"]
    m_bath = MATS["Mat_Floor_Bath"]
    m_grass = MATS["Mat_Lawn_Grass"]
    m_brass = MATS["Mat_Brass_Gold"]
    
    mat_list = [m_plinth, m_marble, m_inlay, m_wood_m, m_wood_g, m_kitchen, m_bath, m_grass, m_brass]
    
    # 1. Outdoor Lawn Patio (Beveled edge)
    add_beveled_box(bm, -8.4, -8.0, -0.25, 16.8, 16.0, 0.08, bevel_r=0.04, segs=2, mat_idx=7)
    
    # 2. Main Plinth Platform (Stepped chamfer)
    add_beveled_box(bm, -6.6, -6.1, -0.17, 13.2, 12.2, 0.17, bevel_r=0.03, segs=2, mat_idx=0)
    
    # 3. Entrance Steps at North-East (X: 2.0 to 4.0, Y: 5.5 to 6.3)
    add_beveled_box(bm, 2.0, 5.5, -0.16, 2.0, 0.8, 0.08, bevel_r=0.02, segs=2, mat_idx=0)
    add_beveled_box(bm, 2.2, 5.5, -0.08, 1.6, 0.4, 0.08, bevel_r=0.02, segs=2, mat_idx=1)
    
    # 4. Room Flooring with Marble Borders
    # Master Bedroom (SW): Walnut herringbone
    add_beveled_box(bm, -5.8, -5.3, 0.0, 4.8, 4.1, 0.02, bevel_r=0.005, mat_idx=3)
    # Master floor perimeter border inlay
    add_beveled_box(bm, -5.75, -5.25, 0.021, 4.7, 4.0, 0.003, bevel_r=0.002, mat_idx=2)
    add_beveled_box(bm, -5.65, -5.15, 0.023, 4.5, 3.8, 0.002, bevel_r=0.002, mat_idx=3)
    
    # Bathroom & Toilet (West): Charcoal slate tiles
    add_beveled_box(bm, -5.8, -1.0, 0.0, 2.6, 2.2, 0.02, bevel_r=0.005, mat_idx=6)
    
    # 2nd Bedroom (NW): Scandinavian oak
    add_beveled_box(bm, -5.8, 1.4, 0.0, 4.8, 3.9, 0.02, bevel_r=0.005, mat_idx=4)
    
    # Kitchen & Dining (SE): Vitrified polished stone
    add_beveled_box(bm, 1.0, -5.3, 0.0, 4.8, 5.1, 0.02, bevel_r=0.005, mat_idx=5)
    
    # Living Room (NE): Italian Botticino marble
    add_beveled_box(bm, 1.0, 0.0, 0.0, 4.8, 5.3, 0.02, bevel_r=0.005, mat_idx=1)
    
    # Central Corridor & Foyer (Brahmasthan transition)
    add_beveled_box(bm, -1.0, -5.3, 0.0, 2.0, 10.6, 0.02, bevel_r=0.005, mat_idx=1)
    add_beveled_box(bm, -3.2, -1.2, 0.0, 2.2, 2.6, 0.02, bevel_r=0.005, mat_idx=1)
    
    # 5. BRAHMASTHAN (Cosmic Center) Royal Medallion
    # Concentric multi-tiered circular marble and brass inlay
    # Outer ring
    add_cylinder(bm, 0.0, 0.0, 0.021, 1.10, 0.004, segs=32, mat_idx=2)
    # Inner marble disc
    add_cylinder(bm, 0.0, 0.0, 0.023, 0.90, 0.003, segs=32, mat_idx=1)
    # Central 8-pointed star in polished brass
    for a in range(8):
        ang = math.pi * a / 4.0
        sx = 0.50 * math.cos(ang)
        sy = 0.50 * math.sin(ang)
        add_beveled_box(bm, sx - 0.04, sy - 0.04, 0.025, 0.08, 0.08, 0.004, bevel_r=0.005, mat_idx=8)
    # Central Golden Bindu point
    add_cylinder(bm, 0.0, 0.0, 0.026, 0.15, 0.006, segs=16, mat_idx=8)
    
    return build_object_from_bmesh("Arch_Floors_Plinth", bm, mat_list, col)

def generate_walls_and_openings(col):
    """
    Architectural Walls with:
    - Baseboard Skirting (75mm)
    - Beveled Wall Cap Trim (Mahogany coping)
    - Carved Indian Archway between Living and Brahmasthan Foyer
    - Beveled Doorway Casings & Architraves
    - 4-Panel Molded Doors Swung Ajar with Brass Levers
    - Multi-Pane Windows with Sills and Mullions
    """
    bm = bmesh.new()
    m_ext = MATS["Mat_Wall_Ext"]
    m_int = MATS["Mat_Wall_Int"]
    m_accent = MATS["Mat_Wall_Accent"]
    m_cap = MATS["Mat_Wall_Cap"]
    m_skirting = MATS["Mat_Skirting"]
    m_glass = MATS["Mat_Glass_Clear"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_brass = MATS["Mat_Brass_Gold"]
    
    mat_list = [m_ext, m_int, m_accent, m_cap, m_skirting, m_glass, m_teak, m_brass]
    # 0: Ext, 1: Int, 2: Accent, 3: Cap, 4: Skirting, 5: Glass, 6: Teak, 7: Brass
    
    wall_h = 1.45
    cap_h = 0.04
    t_ext = 0.22
    t_int = 0.15
    
    def wall_with_skirting(x, y, z, sx, sy, sz, mat_idx=0, add_skirt=True):
        # Main beveled wall
        add_beveled_box(bm, x, y, z, sx, sy, sz, bevel_r=0.015, segs=2, mat_idx=mat_idx)
        # Mahogany Coping Cap on top (30mm overhang with bevel)
        add_beveled_box(bm, x - 0.025, y - 0.025, z + sz, sx + 0.05, sy + 0.05, cap_h, bevel_r=0.01, segs=2, mat_idx=3)
        # Baseboard Skirting
        if add_skirt:
            add_beveled_box(bm, x - 0.008, y - 0.008, z, sx + 0.016, sy + 0.016, 0.08, bevel_r=0.004, segs=1, mat_idx=4)
            
    def window_assembly_x(x, y, length, sill_h=0.55, win_w=1.6):
        p1 = (length - win_w) / 2
        # Left wall
        wall_with_skirting(x, y, 0.0, p1, t_ext, wall_h, mat_idx=0)
        # Right wall
        wall_with_skirting(x + p1 + win_w, y, 0.0, p1, t_ext, wall_h, mat_idx=0)
        # Window bottom sill wall
        add_beveled_box(bm, x + p1, y, 0.0, win_w, t_ext, sill_h, bevel_r=0.01, mat_idx=0)
        # Molded Window Sill Coping
        add_beveled_box(bm, x + p1 - 0.04, y - 0.03, sill_h, win_w + 0.08, t_ext + 0.06, 0.04, bevel_r=0.01, mat_idx=3)
        # Casement Frame & Mullions (Dark Teak)
        # Perimeter Frame
        add_beveled_box(bm, x + p1, y + t_ext/2 - 0.03, sill_h + 0.04, win_w, 0.06, wall_h - sill_h - 0.04, bevel_r=0.005, mat_idx=6)
        # Center Vertical Mullion
        add_beveled_box(bm, x + p1 + win_w/2 - 0.025, y + t_ext/2 - 0.035, sill_h + 0.04, 0.05, 0.07, wall_h - sill_h - 0.04, bevel_r=0.004, mat_idx=6)
        # Glass Panes
        add_beveled_box(bm, x + p1 + 0.03, y + t_ext/2 - 0.008, sill_h + 0.06, win_w/2 - 0.05, 0.016, wall_h - sill_h - 0.08, bevel_r=0.002, mat_idx=5)
        add_beveled_box(bm, x + p1 + win_w/2 + 0.02, y + t_ext/2 - 0.008, sill_h + 0.06, win_w/2 - 0.05, 0.016, wall_h - sill_h - 0.08, bevel_r=0.002, mat_idx=5)

    def window_assembly_y(x, y, length, sill_h=0.55, win_w=1.6):
        p1 = (length - win_w) / 2
        wall_with_skirting(x, y, 0.0, t_ext, p1, wall_h, mat_idx=0)
        wall_with_skirting(x, y + p1 + win_w, 0.0, t_ext, p1, wall_h, mat_idx=0)
        add_beveled_box(bm, x, y + p1, 0.0, t_ext, win_w, sill_h, bevel_r=0.01, mat_idx=0)
        add_beveled_box(bm, x - 0.03, y + p1 - 0.04, sill_h, t_ext + 0.06, win_w + 0.08, 0.04, bevel_r=0.01, mat_idx=3)
        # Frame
        add_beveled_box(bm, x + t_ext/2 - 0.03, y + p1, sill_h + 0.04, 0.06, win_w, wall_h - sill_h - 0.04, bevel_r=0.005, mat_idx=6)
        # Center Mullion
        add_beveled_box(bm, x + t_ext/2 - 0.035, y + p1 + win_w/2 - 0.025, sill_h + 0.04, 0.07, 0.05, wall_h - sill_h - 0.04, bevel_r=0.004, mat_idx=6)
        # Glass Panes
        add_beveled_box(bm, x + t_ext/2 - 0.008, y + p1 + 0.03, sill_h + 0.06, 0.016, win_w/2 - 0.05, wall_h - sill_h - 0.08, bevel_r=0.002, mat_idx=5)
        add_beveled_box(bm, x + t_ext/2 - 0.008, y + p1 + win_w/2 + 0.02, sill_h + 0.06, 0.016, win_w/2 - 0.05, wall_h - sill_h - 0.08, bevel_r=0.002, mat_idx=5)

    # -----------------------------------------------------------------
    # A. EXTERIOR PERIMETER WALLS
    # -----------------------------------------------------------------
    # South Wall
    window_assembly_x(-6.0, -5.5, 5.0, sill_h=0.6, win_w=1.6)
    wall_with_skirting(-1.0, -5.5, 0.0, 2.0, t_ext, wall_h, mat_idx=0)
    window_assembly_x(1.0, -5.5, 5.0, sill_h=0.7, win_w=1.4)
    
    # North Wall
    window_assembly_x(-6.0, 5.3, 5.0, sill_h=0.6, win_w=1.6)
    wall_with_skirting(-1.0, 5.3, 0.0, 2.0, t_ext, wall_h, mat_idx=0)
    wall_with_skirting(1.0, 5.3, 0.0, 1.4, t_ext, wall_h, mat_idx=0)
    
    # Main Entrance Portal at North-East (X: 2.4 to 3.4)
    # Molded Doorway Casing
    add_beveled_box(bm, 2.36, 5.28, 0.0, 0.06, t_ext + 0.04, wall_h, bevel_r=0.01, mat_idx=6)
    add_beveled_box(bm, 3.38, 5.28, 0.0, 0.06, t_ext + 0.04, wall_h, bevel_r=0.01, mat_idx=6)
    # Threshold strip
    add_beveled_box(bm, 2.4, 5.3, 0.0, 1.0, t_ext, 0.04, bevel_r=0.005, mat_idx=3)
    # Main Entrance Grand Door (Swung ajar 55 deg into foyer)
    add_paneled_door(bm, 2.42, 5.32, 0.04, 0.96, 1.38, angle_deg=55, mat_wood=6, mat_handle=7)
    window_assembly_x(3.4, 5.3, 2.6, sill_h=0.55, win_w=1.2)
    
    # West Wall
    window_assembly_y(-6.0, -5.3, 4.3, sill_h=0.6, win_w=1.4)
    wall_with_skirting(-6.0, -1.0, 0.0, t_ext, 0.6, wall_h, mat_idx=0)
    # Bathroom ventilation window
    add_beveled_box(bm, -6.0, -0.4, 0.9, t_ext, 0.8, 0.04, bevel_r=0.008, mat_idx=3)
    add_beveled_box(bm, -6.0 + t_ext/2 - 0.01, -0.4, 0.94, 0.02, 0.8, wall_h - 0.94, bevel_r=0.002, mat_idx=5)
    wall_with_skirting(-6.0, 0.4, 0.0, t_ext, 0.8, wall_h, mat_idx=0)
    window_assembly_y(-6.0, 1.2, 4.1, sill_h=0.6, win_w=1.4)
    
    # East Wall
    window_assembly_y(5.8, -5.3, 5.1, sill_h=0.7, win_w=1.5)
    window_assembly_y(5.8, -0.2, 5.5, sill_h=0.5, win_w=2.0)
    
    # -----------------------------------------------------------------
    # B. INTERIOR PARTITIONS, ARCHES & PANELED DOORS
    # -----------------------------------------------------------------
    # 1. Master Bedroom North Partition
    wall_with_skirting(-5.8, -1.2, 0.0, 3.8, t_int, wall_h, mat_idx=1)
    # Door Jamb Casings
    add_beveled_box(bm, -2.04, -1.22, 0.0, 0.05, t_int + 0.04, wall_h, bevel_r=0.008, mat_idx=6)
    add_beveled_box(bm, -1.11, -1.22, 0.0, 0.05, t_int + 0.04, wall_h, bevel_r=0.008, mat_idx=6)
    add_beveled_box(bm, -2.0, -1.2, 0.0, 0.9, t_int, 0.03, bevel_r=0.005, mat_idx=3)
    # Master Door Swung Ajar into Bedroom (45 deg)
    add_paneled_door(bm, -2.0, -1.2, 0.03, 0.88, 1.38, angle_deg=-45, mat_wood=6, mat_handle=7)
    wall_with_skirting(-1.1, -1.2, 0.0, 0.1, t_int, wall_h, mat_idx=1)
    
    # 2. Master Bedroom East Wall
    wall_with_skirting(-1.0, -5.3, 0.0, t_int, 4.1, wall_h, mat_idx=1)
    
    # 3. Bathroom East Wall & Door
    wall_with_skirting(-3.2, -1.0, 0.0, t_int, 1.0, wall_h, mat_idx=1)
    add_beveled_box(bm, -3.22, -0.04, 0.0, t_int + 0.04, 0.05, wall_h, bevel_r=0.008, mat_idx=6)
    add_beveled_box(bm, -3.22, 0.89, 0.0, t_int + 0.04, 0.05, wall_h, bevel_r=0.008, mat_idx=6)
    add_beveled_box(bm, -3.2, 0.0, 0.0, t_int, 0.9, 0.03, bevel_r=0.005, mat_idx=3)
    add_paneled_door(bm, -3.2, 0.0, 0.03, 0.88, 1.38, angle_deg=135, mat_wood=6, mat_handle=7)
    wall_with_skirting(-3.2, 0.9, 0.0, t_int, 0.3, wall_h, mat_idx=1)
    
    # 4. Bathroom North Wall
    wall_with_skirting(-5.8, 1.2, 0.0, 2.75, t_int, wall_h, mat_idx=1)
    
    # 5. 2nd Bedroom South Wall
    wall_with_skirting(-3.05, 1.25, 0.0, 2.05, t_int, wall_h, mat_idx=1)
    
    # 6. 2nd Bedroom East Wall & Door
    add_beveled_box(bm, -1.02, 1.36, 0.0, t_int + 0.04, 0.05, wall_h, bevel_r=0.008, mat_idx=6)
    add_beveled_box(bm, -1.02, 2.29, 0.0, t_int + 0.04, 0.05, wall_h, bevel_r=0.008, mat_idx=6)
    add_beveled_box(bm, -1.0, 1.4, 0.0, t_int, 0.9, 0.03, bevel_r=0.005, mat_idx=3)
    add_paneled_door(bm, -1.0, 1.4, 0.03, 0.88, 1.38, angle_deg=135, mat_wood=6, mat_handle=7)
    wall_with_skirting(-1.0, 2.3, 0.0, t_int, 3.0, wall_h, mat_idx=1)
    
    # 7. Kitchen & Living Dividing Wall & Breakfast Pass
    wall_with_skirting(4.0, -0.2, 0.0, 1.8, t_int, wall_h, mat_idx=1)
    add_beveled_box(bm, 2.0, -0.2, 0.0, 2.0, t_int, 0.88, bevel_r=0.015, mat_idx=1) # Low counter
    add_beveled_box(bm, 1.94, -0.24, 0.88, 2.12, t_int + 0.08, 0.05, bevel_r=0.015, mat_idx=3) # Bullnose bar
    add_beveled_box(bm, 1.0, -0.2, 0.0, 1.0, t_int, 0.03, bevel_r=0.005, mat_idx=3)
    
    # 8. GRAND INDIAN ARCHWAY (Between Brahmasthan Foyer & Living Room: Y = 0.5 to 2.5)
    wall_with_skirting(0.85, -5.3, 0.0, t_int, 2.3, wall_h, mat_idx=1)
    add_beveled_box(bm, 0.85, -3.0, 0.0, t_int, 1.0, 0.03, bevel_r=0.005, mat_idx=3)
    wall_with_skirting(0.85, -2.0, 0.0, t_int, 1.95, wall_h, mat_idx=1)
    
    # Fluted Pilasters on Archway Sides
    # South Pilaster
    add_fluted_panel(bm, 0.84, 0.50, 0.0, t_int + 0.02, 0.18, wall_h, num_flutes=4, axis='Y', mat_idx=6)
    # North Pilaster
    add_fluted_panel(bm, 0.84, 2.32, 0.0, t_int + 0.02, 0.18, wall_h, num_flutes=4, axis='Y', mat_idx=6)
    # Semicircular Arch Architrave
    add_archway(bm, 0.925, 0.68, 0.80, 0.70, 0.82, t_int, segs=16, mat_idx=6)
    add_beveled_box(bm, 0.85, 0.5, 0.0, t_int, 2.0, 0.03, bevel_r=0.005, mat_idx=3)
    wall_with_skirting(0.85, 2.5, 0.0, t_int, 2.8, wall_h, mat_idx=1)
    
    # 9. Feature Accent Walls
    add_beveled_box(bm, 3.4, 5.22, 0.0, 1.2, 0.06, wall_h, bevel_r=0.01, mat_idx=2) # Living TV
    add_beveled_box(bm, -4.8, -5.28, 0.0, 2.8, 0.06, wall_h, bevel_r=0.01, mat_idx=2) # Master Bed

    return build_object_from_bmesh("Arch_Walls_Cutaway", bm, mat_list, col)

# =====================================================================
# 5. FURNITURE GENERATORS (CURVED & PROFILES)
# =====================================================================

def generate_master_bedroom(col):
    """
    South-West (Nairutya - Earth Element):
    - Fluted Channel-Tufted Luxury King Bed with curved profiles
    - Lathe-Turned Spindle Nightstands with bulbous ceramic bedside lamps
    - 4-Door Wardrobe with fluted vertical panels & brass handles
    - Tambour Vanity Console with oval backlit mirror & cylindrical velvet pouf
    - Layered duvet & soft pillows with piping
    """
    bm = bmesh.new()
    m_teak = MATS["Mat_Teak_Wood"]
    m_navy = MATS["Mat_Bed_Master_Navy"]
    m_white = MATS["Mat_Bed_Linen_White"]
    m_mustard = MATS["Mat_Fabric_Mustard"]
    m_brass = MATS["Mat_Brass_Gold"]
    m_light = MATS["Mat_Warm_Light"]
    m_rug = MATS["Mat_Rug_Bedroom"]
    m_mirror = MATS["Mat_Mirror"]
    
    mat_list = [m_teak, m_navy, m_white, m_mustard, m_brass, m_light, m_rug, m_mirror]
    
    # 1. Bedroom Area Rug (Plush beveled edges)
    add_beveled_box(bm, -4.8, -5.1, 0.021, 2.8, 3.2, 0.018, bevel_r=0.04, segs=2, mat_idx=6)
    
    # 2. Luxury King Bed (Headboard against South Wall: Center X = -3.4, Y = -5.2)
    # Headboard Frame
    add_beveled_box(bm, -4.55, -5.26, 0.02, 2.3, 0.12, 1.20, bevel_r=0.02, segs=2, mat_idx=0)
    # Fluted / Channel-Tufted Upholstered Velvet Headboard (9 vertical curved channels)
    add_fluted_panel(bm, -4.45, -5.22, 0.25, 2.1, 0.06, 0.90, num_flutes=9, axis='X', mat_idx=1)
    
    # Bed Frame with Beveled Chamfers
    add_beveled_box(bm, -4.42, -5.16, 0.02, 2.04, 2.12, 0.32, bevel_r=0.03, segs=2, mat_idx=0)
    # Turned Brass Foot Ferrules on bed corners
    for bx, by in [(-4.40, -5.14), (-2.40, -5.14), (-4.40, -3.06), (-2.40, -3.06)]:
        add_cylinder(bm, bx, by, 0.02, 0.03, 0.08, segs=12, mat_idx=4)
        
    # Deep Mattress with Rounded Bullnose Corners
    add_beveled_box(bm, -4.36, -5.10, 0.34, 1.92, 2.02, 0.26, bevel_r=0.05, segs=2, mat_idx=2)
    # Draped Navy Duvet Quilt with Folded Edge
    add_beveled_box(bm, -4.38, -4.60, 0.36, 1.96, 1.48, 0.26, bevel_r=0.06, segs=2, mat_idx=1)
    # Mustard Gold Bed Runner
    add_beveled_box(bm, -4.39, -3.80, 0.63, 1.98, 0.45, 0.025, bevel_r=0.015, mat_idx=3)
    
    # 4 Plush Pillows with Soft Volume & Piping
    add_beveled_box(bm, -4.26, -4.96, 0.61, 0.76, 0.46, 0.14, bevel_r=0.06, segs=2, mat_idx=2)
    add_beveled_box(bm, -3.32, -4.96, 0.61, 0.76, 0.46, 0.14, bevel_r=0.06, segs=2, mat_idx=2)
    add_beveled_box(bm, -4.20, -4.86, 0.66, 0.66, 0.36, 0.12, bevel_r=0.05, segs=2, mat_idx=1)
    add_beveled_box(bm, -3.26, -4.86, 0.66, 0.66, 0.36, 0.12, bevel_r=0.05, segs=2, mat_idx=3)
    
    # 3. Nightstands with Lathe-Turned Spindle Legs & Designer Lamps
    for nx in [-5.15, -2.15]:
        # Nightstand Tabletop & Drawer (Beveled corners)
        add_beveled_box(bm, nx, -5.20, 0.30, 0.55, 0.45, 0.24, bevel_r=0.02, segs=2, mat_idx=0)
        # 4 Turned Tapered Wooden Legs with Brass Shoes
        for lx, ly in [(nx + 0.06, -5.14), (nx + 0.49, -5.14), (nx + 0.06, -4.81), (nx + 0.49, -4.81)]:
            leg_prof = [(0.022, 0.0), (0.018, 0.08), (0.014, 0.22), (0.020, 0.30)]
            add_lathe_mesh(bm, lx, ly, 0.02, leg_prof, segs=12, mat_idx=0)
            add_cylinder(bm, lx, ly, 0.02, 0.023, 0.06, segs=12, mat_idx=4) # Brass shoe
        # Brass Drawer Handle
        add_cylinder(bm, nx + 0.275, -4.74, 0.42, 0.012, 0.02, segs=8, mat_idx=4)
        
        # Bedside Designer Lamp: Lathe-Turned Bulbous Urn Base + Flared Fabric Shade
        lamp_x, lamp_y = nx + 0.275, -4.95
        lamp_prof = [
            (0.08, 0.0), (0.09, 0.02), (0.05, 0.06), (0.09, 0.14), (0.07, 0.20),
            (0.04, 0.24), (0.05, 0.26), (0.02, 0.28), (0.02, 0.32)
        ]
        add_lathe_mesh(bm, lamp_x, lamp_y, 0.54, lamp_prof, segs=16, mat_idx=4)
        # Flared Shade
        shade_prof = [(0.14, 0.30), (0.09, 0.48)]
        add_lathe_mesh(bm, lamp_x, lamp_y, 0.54, shade_prof, segs=16, mat_idx=5)
        
    # 4. Master Wardrobe (West Wall: X [-5.7, -5.0], Y [-3.8, -1.6])
    # Fluted Shaker Panel Doors
    add_beveled_box(bm, -5.72, -3.85, 0.02, 0.68, 2.30, 1.42, bevel_r=0.02, segs=2, mat_idx=0)
    for i in range(4):
        dy = -3.85 + i * 0.575
        add_fluted_panel(bm, -5.03, dy + 0.03, 0.06, 0.02, 0.51, 1.30, num_flutes=5, axis='Y', mat_idx=0)
        # Full-length brass bar handle
        add_cylinder(bm, -5.01, dy + 0.48, 0.55, 0.012, 0.35, segs=8, mat_idx=4)
        
    # 5. Tambour Vanity Console (East Wall: X [-1.5, -1.05], Y [-3.8, -2.6])
    add_beveled_box(bm, -1.50, -3.65, 0.02, 0.46, 1.05, 0.76, bevel_r=0.03, segs=2, mat_idx=0)
    add_fluted_panel(bm, -1.48, -3.60, 0.15, 0.02, 0.95, 0.55, num_flutes=8, axis='Y', mat_idx=0)
    # Oval Backlit Mirror on Wall
    mirror_x, mirror_y = -1.12, -3.12
    add_cylinder(bm, mirror_x, mirror_y, 0.90, 0.32, 0.03, segs=24, mat_idx=4) # Brass frame
    add_cylinder(bm, mirror_x - 0.01, mirror_y, 0.90, 0.30, 0.02, segs=24, mat_idx=7) # Mirror
    
    # Cylindrical Velvet Pouf / Stool with Brass Plinth Ring
    add_cylinder(bm, -1.90, -3.12, 0.02, 0.22, 0.06, segs=16, mat_idx=4) # Brass ring
    add_cylinder(bm, -1.90, -3.12, 0.08, 0.20, 0.38, segs=16, mat_idx=3) # Mustard velvet
    
    return build_object_from_bmesh("Furn_Master_Bedroom_SW", bm, mat_list, col)

def generate_guest_bedroom(col):
    """
    North-West (Vayu - Air & Movement):
    - Queen Bed with rounded headboard & soft bedding
    - Ergonomic Study Workstation with 5-star swivel office chair & laptop
    - Wardrobe closet with brass hardware
    - Reading lamp & nightstand
    """
    bm = bmesh.new()
    m_light_wood = MATS["Mat_Light_Wood"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_sage = MATS["Mat_Bed_Guest_Sage"]
    m_white = MATS["Mat_Bed_Linen_White"]
    m_teal = MATS["Mat_Fabric_Teal"]
    m_chrome = MATS["Mat_Chrome"]
    m_light = MATS["Mat_Warm_Light"]
    m_screen = MATS["Mat_TV_Display"]
    m_rug = MATS["Mat_Rug_Bedroom"]
    
    mat_list = [m_light_wood, m_teak, m_sage, m_white, m_teal, m_chrome, m_light, m_screen, m_rug]
    
    # 1. Floor Rug
    add_beveled_box(bm, -5.2, 2.0, 0.021, 2.4, 2.6, 0.018, bevel_r=0.04, segs=2, mat_idx=8)
    
    # 2. Queen Bed (Headboard against West Wall)
    add_beveled_box(bm, -5.76, 2.30, 0.02, 0.12, 1.84, 1.10, bevel_r=0.02, segs=2, mat_idx=1)
    add_fluted_panel(bm, -5.72, 2.40, 0.25, 0.05, 1.64, 0.80, num_flutes=7, axis='Y', mat_idx=2)
    add_beveled_box(bm, -5.64, 2.38, 0.02, 2.06, 1.68, 0.30, bevel_r=0.03, segs=2, mat_idx=0)
    add_beveled_box(bm, -5.58, 2.44, 0.32, 1.96, 1.56, 0.24, bevel_r=0.05, segs=2, mat_idx=3)
    add_beveled_box(bm, -5.10, 2.42, 0.34, 1.46, 1.60, 0.24, bevel_r=0.06, segs=2, mat_idx=2)
    add_beveled_box(bm, -4.10, 2.40, 0.59, 0.40, 1.62, 0.025, bevel_r=0.015, mat_idx=4)
    
    # Pillows
    add_beveled_box(bm, -5.50, 2.54, 0.56, 0.46, 0.62, 0.13, bevel_r=0.05, segs=2, mat_idx=3)
    add_beveled_box(bm, -5.50, 3.24, 0.56, 0.46, 0.62, 0.13, bevel_r=0.05, segs=2, mat_idx=3)
    add_beveled_box(bm, -5.34, 2.66, 0.61, 0.36, 0.46, 0.11, bevel_r=0.04, segs=2, mat_idx=4)
    
    # Nightstand with Lathe Lamp
    add_beveled_box(bm, -5.72, 4.22, 0.02, 0.52, 0.46, 0.52, bevel_r=0.02, segs=2, mat_idx=0)
    lamp_prof = [(0.06, 0.0), (0.08, 0.03), (0.03, 0.15), (0.02, 0.24)]
    add_lathe_mesh(bm, -5.46, 4.45, 0.54, lamp_prof, segs=12, mat_idx=5)
    shade_prof = [(0.12, 0.22), (0.08, 0.38)]
    add_lathe_mesh(bm, -5.46, 4.45, 0.54, shade_prof, segs=12, mat_idx=6)
    
    # 3. Work-From-Home Study Station (North Window: X [-3.0, -1.4], Y [4.8, 5.25])
    add_beveled_box(bm, -3.00, 4.80, 0.02, 1.55, 0.50, 0.74, bevel_r=0.02, segs=2, mat_idx=0)
    # Pedestal Drawer
    add_beveled_box(bm, -2.95, 4.82, 0.06, 0.38, 0.45, 0.64, bevel_r=0.015, segs=2, mat_idx=1)
    
    # Ergonomic Office Swivel Chair: 5-Star Base + Hydraulic Column + Contoured Mesh Seat & Back
    cx, cy = -2.20, 4.40
    # 5 Star Base with Casters
    for i in range(5):
        ang = 2 * math.pi * i / 5.0
        bx = cx + 0.26 * math.cos(ang)
        by = cy + 0.26 * math.sin(ang)
        add_cylinder(bm, (cx + bx)/2, (cy + by)/2, 0.04, 0.015, 0.03, segs=8, mat_idx=5)
        add_cylinder(bm, bx, by, 0.02, 0.025, 0.04, segs=8, mat_idx=5) # Caster
    # Hydraulic cylinder
    add_cylinder(bm, cx, cy, 0.06, 0.025, 0.38, segs=12, mat_idx=5)
    # Contoured Seat Cushion
    add_beveled_box(bm, cx - 0.22, cy - 0.20, 0.44, 0.44, 0.42, 0.08, bevel_r=0.03, segs=2, mat_idx=4)
    # Curved Mesh Backrest
    add_beveled_box(bm, cx - 0.20, cy - 0.22, 0.52, 0.40, 0.06, 0.42, bevel_r=0.03, segs=2, mat_idx=4)
    
    # Open High-End Laptop (Wedge base + Trackpad + Thin Screen)
    add_beveled_box(bm, -2.32, 4.88, 0.76, 0.34, 0.23, 0.015, bevel_r=0.005, mat_idx=5)
    add_beveled_box(bm, -2.32, 5.10, 0.77, 0.34, 0.015, 0.22, bevel_r=0.005, mat_idx=7)
    
    # 4. Wardrobe
    add_beveled_box(bm, -1.50, 2.00, 0.02, 0.46, 1.45, 1.40, bevel_r=0.02, segs=2, mat_idx=0)
    add_fluted_panel(bm, -1.48, 2.05, 0.06, 0.02, 0.64, 1.30, num_flutes=5, axis='Y', mat_idx=1)
    add_fluted_panel(bm, -1.48, 2.75, 0.06, 0.02, 0.64, 1.30, num_flutes=5, axis='Y', mat_idx=1)
    
    return build_object_from_bmesh("Furn_Guest_Bedroom_NW", bm, mat_list, col)

def generate_living_room_and_mandir(col):
    """
    North-East (Ishanya - Divine & Water Element):
    - Ergonomic Curved 3-Seater Sofa with rolled armrests & channel tufting
    - Semi-circular Tub Armchairs
    - Beveled Walnut & Glass Coffee Table with lathe legs
    - Fluted TV Credenza & Frameless 4K OLED TV
    - SACRED POOJA MANDIR: Authentic Dravidian/Nagara Temple with lathe pillars,
      tiered Shikhara, Golden Kalash, Pooja Diya with glowing flame & hanging bell.
    """
    bm = bmesh.new()
    m_sofa = MATS["Mat_Fabric_Sofa"]
    m_mustard = MATS["Mat_Fabric_Mustard"]
    m_teal = MATS["Mat_Fabric_Teal"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_brass = MATS["Mat_Brass_Gold"]
    m_glass = MATS["Mat_Glass_Clear"]
    m_tv = MATS["Mat_TV_Display"]
    m_rug = MATS["Mat_Rug_Living"]
    m_foliage = MATS["Mat_Foliage"]
    m_planter = MATS["Mat_Planter_Ceramic"]
    m_flame = MATS["Mat_Diya_Flame"]
    m_mat = MATS["Mat_Doormat"]
    
    mat_list = [m_sofa, m_mustard, m_teal, m_teak, m_brass, m_glass, m_tv, m_rug, m_foliage, m_planter, m_flame, m_mat]
    
    # 1. Welcome Mat & Living Area Rug
    add_beveled_box(bm, 2.45, 5.0, 0.021, 0.90, 0.50, 0.018, bevel_r=0.03, segs=2, mat_idx=11)
    add_beveled_box(bm, 1.60, 0.90, 0.021, 3.50, 3.00, 0.020, bevel_r=0.06, segs=2, mat_idx=7)
    
    # 2. ERGONOMIC CURVED 3-SEATER SOFA (No Boxy Cuboids!)
    # Turned Tapered Wooden Legs with Brass Shoes
    for sx, sy in [(2.15, 1.25), (4.40, 1.25), (2.15, 2.05), (4.40, 2.05)]:
        leg_prof = [(0.035, 0.0), (0.025, 0.08), (0.018, 0.18)]
        add_lathe_mesh(bm, sx, sy, 0.02, leg_prof, segs=12, mat_idx=3)
        add_cylinder(bm, sx, sy, 0.02, 0.036, 0.05, segs=12, mat_idx=4) # Brass cap
        
    # Curved Base Frame
    add_beveled_box(bm, 2.05, 1.20, 0.18, 2.45, 0.90, 0.18, bevel_r=0.06, segs=3, mat_idx=0)
    
    # 3 Separate Bullnose Seat Cushions with Volumetric Puff
    for ci in range(3):
        cx = 2.18 + ci * 0.76
        add_beveled_box(bm, cx, 1.34, 0.36, 0.72, 0.72, 0.14, bevel_r=0.06, segs=3, mat_idx=0)
        
    # Contoured Backrest with Vertical Channel Tufting
    add_fluted_panel(bm, 2.15, 1.22, 0.36, 2.25, 0.16, 0.48, num_flutes=8, axis='X', mat_idx=0)
    
    # Rolled / Curved Armrests on Left & Right
    add_beveled_box(bm, 1.95, 1.22, 0.22, 0.20, 0.86, 0.42, bevel_r=0.08, segs=3, mat_idx=0)
    add_beveled_box(bm, 4.40, 1.22, 0.22, 0.20, 0.86, 0.42, bevel_r=0.08, segs=3, mat_idx=0)
    
    # Throw Pillows (Saffron & Peacock Teal)
    add_beveled_box(bm, 2.25, 1.45, 0.48, 0.38, 0.16, 0.34, bevel_r=0.06, segs=2, mat_idx=1)
    add_beveled_box(bm, 3.95, 1.45, 0.48, 0.38, 0.16, 0.34, bevel_r=0.06, segs=2, mat_idx=2)
    
    # 3. Semi-Circular Tub Armchairs
    # Left Armchair (Facing East)
    add_beveled_box(bm, 1.45, 2.20, 0.02, 0.80, 0.80, 0.40, bevel_r=0.08, segs=3, mat_idx=2)
    # Curved Barrel Backrest
    chair_prof = [(0.42, 0.38), (0.40, 0.75)]
    add_lathe_mesh(bm, 1.85, 2.60, 0.0, chair_prof, segs=16, mat_idx=2)
    
    # Right Armchair (Facing West)
    add_beveled_box(bm, 4.35, 2.20, 0.02, 0.80, 0.80, 0.40, bevel_r=0.08, segs=3, mat_idx=1)
    add_lathe_mesh(bm, 4.75, 2.60, 0.0, chair_prof, segs=16, mat_idx=1)
    
    # 4. Beveled Walnut & Glass Coffee Table (X = 3.3, Y = 2.4)
    # Beveled Solid Walnut Rim
    add_beveled_box(bm, 2.65, 2.05, 0.02, 1.30, 0.70, 0.40, bevel_r=0.04, segs=2, mat_idx=3)
    # 4 Lathe-Turned Table Legs
    for tx, ty in [(2.75, 2.15), (3.85, 2.15), (2.75, 2.65), (3.85, 2.65)]:
        tleg_prof = [(0.03, 0.0), (0.02, 0.15), (0.035, 0.38)]
        add_lathe_mesh(bm, tx, ty, 0.02, tleg_prof, segs=12, mat_idx=3)
        add_cylinder(bm, tx, ty, 0.02, 0.032, 0.04, segs=12, mat_idx=4) # Brass shoe
    # Tempered Glass Inset Top
    add_beveled_box(bm, 2.70, 2.10, 0.40, 1.20, 0.60, 0.02, bevel_r=0.01, mat_idx=5)
    # Ceramic Bowl & Magazines
    add_lathe_mesh(bm, 3.45, 2.40, 0.42, [(0.06, 0.0), (0.12, 0.06)], segs=16, mat_idx=9)
    
    # 5. Fluted TV Entertainment Credenza & 65" 4K Display
    add_beveled_box(bm, 3.15, 4.88, 0.15, 1.70, 0.38, 0.38, bevel_r=0.03, segs=2, mat_idx=3)
    add_fluted_panel(bm, 3.20, 4.87, 0.18, 1.60, 0.02, 0.32, num_flutes=14, axis='X', mat_idx=3)
    # 65" 4K Display
    add_beveled_box(bm, 3.25, 5.14, 0.65, 1.48, 0.04, 0.78, bevel_r=0.015, mat_idx=6)
    add_beveled_box(bm, 3.23, 5.13, 0.63, 1.52, 0.02, 0.82, bevel_r=0.01, mat_idx=4) # Slim Gold Bezel
    
    # 6. Biophilic Fluted Planter with Tiered Foliage
    add_fluted_panel(bm, 1.25, 4.55, 0.02, 0.35, 0.35, 0.52, num_flutes=6, axis='X', mat_idx=9)
    for angle in [0, 40, 80, 120, 160, 200, 240, 280, 320]:
        rad = math.radians(angle)
        lx = 1.42 + 0.24 * math.cos(rad)
        ly = 4.72 + 0.24 * math.sin(rad)
        add_cylinder(bm, lx, ly, 0.52, 0.14, 0.45, segs=6, mat_idx=8)
        
    # -----------------------------------------------------------------
    # 7. SACRED POOJA MANDIR (Strictly North-East Corner)
    # Masterpiece Architecture: Lathe Spindles, Cusped Torana Arch,
    # Tiered Nagara Shikhara, Golden Kalash, Pooja Diya & Hanging Bell.
    # -----------------------------------------------------------------
    mx, my = 5.00, 4.60
    # Tiered Molded Plinth Base
    add_beveled_box(bm, mx - 0.04, my - 0.04, 0.02, 0.82, 0.72, 0.15, bevel_r=0.02, segs=2, mat_idx=3)
    add_beveled_box(bm, mx, my, 0.17, 0.74, 0.64, 0.25, bevel_r=0.02, segs=2, mat_idx=3)
    # Sanctum Floor
    add_beveled_box(bm, mx + 0.02, my + 0.02, 0.42, 0.70, 0.60, 0.04, bevel_r=0.01, mat_idx=3)
    
    # 4 Lathe-Turned Ornamental Brass Pillars (Spindles with torus, baluster, capital)
    pillar_prof = [
        (0.040, 0.00), (0.045, 0.03), (0.025, 0.08), (0.038, 0.22),
        (0.022, 0.35), (0.035, 0.48), (0.045, 0.52), (0.030, 0.55)
    ]
    for px, py in [(mx + 0.06, my + 0.06), (mx + 0.68, my + 0.06), (mx + 0.06, my + 0.58), (mx + 0.68, my + 0.58)]:
        add_lathe_mesh(bm, px, py, 0.46, pillar_prof, segs=16, mat_idx=4)
        
    # Cusped Torana Archway Canopy
    add_archway(bm, mx + 0.37, my + 0.06, 0.90, 0.24, 0.28, 0.08, segs=12, mat_idx=4)
    add_beveled_box(bm, mx, my, 1.01, 0.74, 0.64, 0.08, bevel_r=0.02, mat_idx=3)
    
    # Tiered Nagara/Dravidian Shikhara Pyramidal Dome
    add_beveled_box(bm, mx + 0.10, my + 0.08, 1.09, 0.54, 0.48, 0.10, bevel_r=0.02, mat_idx=4)
    add_beveled_box(bm, mx + 0.20, my + 0.16, 1.19, 0.34, 0.32, 0.10, bevel_r=0.02, mat_idx=4)
    
    # Golden Kalash Spire with Mangal Coconut Apex (Lathe Profile)
    kalash_prof = [
        (0.06, 0.00), (0.08, 0.04), (0.04, 0.09), (0.07, 0.15),
        (0.02, 0.18), (0.04, 0.22), (0.00, 0.26)
    ]
    add_lathe_mesh(bm, mx + 0.37, my + 0.32, 1.29, kalash_prof, segs=16, mat_idx=4)
    
    # Lathe-Turned Temple Hanging Bell
    bell_prof = [(0.015, 0.00), (0.025, 0.04), (0.05, 0.08), (0.055, 0.09)]
    add_lathe_mesh(bm, mx + 0.37, my + 0.22, 0.82, bell_prof, segs=12, mat_idx=4)
    add_cylinder(bm, mx + 0.37, my + 0.22, 0.91, 0.005, 0.10, segs=8, mat_idx=4) # Chain
    
    # Stepped Brass Pooja Diya (Deepak) with Warm Glowing Flame
    diya_prof = [(0.06, 0.00), (0.04, 0.02), (0.02, 0.05), (0.05, 0.08), (0.055, 0.09)]
    add_lathe_mesh(bm, mx + 0.22, my + 0.20, 0.46, diya_prof, segs=12, mat_idx=4)
    add_cylinder(bm, mx + 0.22, my + 0.20, 0.55, 0.018, 0.04, segs=8, mat_idx=10) # Flame
    
    # Deity / Murti Sanctum Backplate
    add_beveled_box(bm, mx + 0.26, my + 0.48, 0.46, 0.22, 0.04, 0.38, bevel_r=0.01, mat_idx=4)
    
    return build_object_from_bmesh("Furn_Living_Mandir_NE", bm, mat_list, col)

def generate_kitchen_and_dining(col):
    """
    South-East (Agni - Fire Element):
    - L-Shaped Modular Kitchen with Continuous 40mm Polished Black Granite Bullnose Edge
    - 4-Burner Glass Hob with Cast-Iron Trivets (SE Corner, Cook faces East)
    - Sloped Stainless Chimney Hood
    - Undermount Stainless Sink with Radiused Corners & Swept Chrome Faucet
    - Dining Suite with Tapered Turned Legs & Ergonomic Curved Chairs
    """
    bm = bmesh.new()
    m_granite = MATS["Mat_Granite_Black"]
    m_cabinet = MATS["Mat_Cabinet_Offwhite"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_chrome = MATS["Mat_Chrome"]
    m_brass = MATS["Mat_Brass_Gold"]
    m_flame = MATS["Mat_Diya_Flame"]
    m_ceramic = MATS["Mat_Ceramic_White"]
    
    mat_list = [m_granite, m_cabinet, m_teak, m_chrome, m_brass, m_flame, m_ceramic]
    
    counter_h = 0.86
    counter_d = 0.65
    
    # 1. Lower Modular Cabinets (L-Shape) with Beveled Inset Doors
    add_beveled_box(bm, 2.00, -5.25, 0.02, 3.70, counter_d, counter_h - 0.04, bevel_r=0.015, segs=2, mat_idx=1)
    add_beveled_box(bm, 5.70 - counter_d, -4.60, 0.02, counter_d, 3.80, counter_h - 0.04, bevel_r=0.015, segs=2, mat_idx=1)
    
    # Sleek Brushed Steel Edge-Pull Handles
    for cx in [2.3, 3.0, 3.7, 4.4]:
        add_cylinder(bm, cx + 0.18, -4.58, counter_h * 0.6, 0.012, 0.32, segs=8, mat_idx=3)
    for cy in [-4.0, -3.2, -2.4, -1.6]:
        add_cylinder(bm, 5.03, cy + 0.18, counter_h * 0.6, 0.012, 0.32, segs=8, mat_idx=3)
        
    # 2. Continuous 40mm Polished Jet Black Granite Countertop with Bullnose Fillet!
    add_beveled_box(bm, 1.95, -5.28, counter_h - 0.04, 3.80, counter_d + 0.05, 0.04, bevel_r=0.018, segs=3, mat_idx=0)
    add_beveled_box(bm, 5.70 - counter_d - 0.05, -4.60, counter_h - 0.04, counter_d + 0.05, 3.85, 0.04, bevel_r=0.018, segs=3, mat_idx=0)
    
    # 3. 4-Burner Tempered Glass Hob (SE Corner: X = 4.8, Y = -4.9, Cook faces East)
    add_beveled_box(bm, 4.48, -5.12, counter_h, 0.78, 0.52, 0.025, bevel_r=0.012, segs=2, mat_idx=0)
    for bx, by in [(4.65, -4.98), (4.65, -4.72), (5.05, -4.98), (5.05, -4.72)]:
        # Stepped burner rings
        add_cylinder(bm, bx, by, counter_h + 0.025, 0.075, 0.018, segs=16, mat_idx=3)
        add_cylinder(bm, bx, by, counter_h + 0.043, 0.045, 0.010, segs=12, mat_idx=4) # Brass inner ring
        # 4-prong cast iron trivet
        for a in range(4):
            ang = math.pi * a / 2.0
            px = bx + 0.06 * math.cos(ang)
            py = by + 0.06 * math.sin(ang)
            add_beveled_box(bm, px - 0.01, py - 0.01, counter_h + 0.04, 0.02, 0.02, 0.015, bevel_r=0.003, mat_idx=0)
    # Control Dials
    for ki in range(4):
        add_cylinder(bm, 4.60 + ki * 0.15, -5.14, counter_h + 0.012, 0.016, 0.02, segs=12, mat_idx=3)
        
    # 4. Sloped Stainless Chimney Hood
    add_beveled_box(bm, 4.42, -5.12, 1.25, 0.88, 0.50, 0.09, bevel_r=0.02, segs=2, mat_idx=3)
    add_cylinder(bm, 4.86, -5.02, 1.34, 0.12, 0.16, segs=16, mat_idx=3) # Duct
    
    # 5. Undermount Double Sink with Radiused Corners (NE of Kitchen)
    add_beveled_box(bm, 5.12, -1.85, counter_h - 0.18, 0.52, 0.74, 0.18, bevel_r=0.04, segs=2, mat_idx=3)
    # Swept Chrome Gooseneck Mixer Faucet (Lathe curved profile)
    faucet_prof = [
        (0.020, 0.00), (0.018, 0.18), (0.015, 0.26), (0.014, 0.32),
        (0.012, 0.34), (0.012, 0.28)
    ]
    add_lathe_mesh(bm, 5.58, -1.48, counter_h + 0.01, faucet_prof, segs=12, mat_idx=3)
    
    # 6. Refrigerator (SW of Kitchen)
    add_beveled_box(bm, 1.18, -5.22, 0.02, 0.74, 0.68, 1.48, bevel_r=0.03, segs=2, mat_idx=3)
    # Curved tubular handles
    add_cylinder(bm, 1.54, -4.51, 0.60, 0.015, 0.48, segs=8, mat_idx=4)
    
    # 7. Dining Suite (Beveled Table with Tapered Lathe Legs & 4 Ergonomic Chairs)
    # Beveled Teak Tabletop
    add_beveled_box(bm, 2.15, -2.95, 0.72, 1.42, 1.02, 0.045, bevel_r=0.015, segs=2, mat_idx=2)
    # Chamfered Apron
    add_beveled_box(bm, 2.22, -2.88, 0.64, 1.28, 0.88, 0.08, bevel_r=0.01, mat_idx=2)
    # 4 Turned Tapered Legs with Brass Shoes
    for dx, dy in [(2.26, -2.84), (3.44, -2.84), (2.26, -2.04), (3.44, -2.04)]:
        dleg_prof = [(0.035, 0.0), (0.024, 0.25), (0.032, 0.64)]
        add_lathe_mesh(bm, dx, dy, 0.02, dleg_prof, segs=12, mat_idx=2)
        add_cylinder(bm, dx, dy, 0.02, 0.036, 0.06, segs=12, mat_idx=4) # Brass shoe
        
    # Table Centerpiece (Fruit bowl & ceramic dinner plates)
    add_lathe_mesh(bm, 2.86, -2.44, 0.765, [(0.06, 0.0), (0.15, 0.08)], segs=16, mat_idx=4)
    add_cylinder(bm, 2.50, -2.44, 0.765, 0.12, 0.015, segs=16, mat_idx=6)
    add_cylinder(bm, 3.22, -2.44, 0.765, 0.12, 0.015, segs=16, mat_idx=6)
    
    # 4 Dining Chairs with Curved Ergonomic Backrests & Tapered Legs
    # 2 South Chairs
    for cx in [2.45, 3.10]:
        add_beveled_box(bm, cx, -3.38, 0.44, 0.42, 0.42, 0.06, bevel_r=0.02, mat_idx=1) # Cushion
        add_beveled_box(bm, cx + 0.02, -3.44, 0.50, 0.38, 0.05, 0.38, bevel_r=0.02, mat_idx=2) # Curved Back
        for legx, legy in [(cx + 0.04, -3.34), (cx + 0.38, -3.34), (cx + 0.04, -3.00), (cx + 0.38, -3.00)]:
            add_cylinder(bm, legx, legy, 0.02, 0.018, 0.42, segs=8, mat_idx=2)
    # 2 North Chairs
    for cx in [2.45, 3.10]:
        add_beveled_box(bm, cx, -1.94, 0.44, 0.42, 0.42, 0.06, bevel_r=0.02, mat_idx=1)
        add_beveled_box(bm, cx + 0.02, -1.58, 0.50, 0.38, 0.05, 0.38, bevel_r=0.02, mat_idx=2)
        for legx, legy in [(cx + 0.04, -1.90), (cx + 0.38, -1.90), (cx + 0.04, -1.56), (cx + 0.38, -1.56)]:
            add_cylinder(bm, legx, legy, 0.02, 0.018, 0.42, segs=8, mat_idx=2)
            
    return build_object_from_bmesh("Furn_Kitchen_Dining_SE", bm, mat_list, col)

def generate_bathroom_sanitary(col):
    """
    West / North-West (Varuna / Vayu Zone):
    - Smooth D-Shaped Curved Ceramic Wall-Hung WC (Facing North-South per Vastu)
    - Floating Vanity with Fluted Drawer Face & Curved Oval Ceramic Basin
    - Walk-in Shower with Frameless Glass & Curved Rain Shower Head
    - Tubular Chrome Towel Rail
    """
    bm = bmesh.new()
    m_ceramic = MATS["Mat_Ceramic_White"]
    m_chrome = MATS["Mat_Chrome"]
    m_glass = MATS["Mat_Glass_Clear"]
    m_mirror = MATS["Mat_Mirror"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_tile = MATS["Mat_Wall_Bath_Tile"]
    
    mat_list = [m_ceramic, m_chrome, m_glass, m_mirror, m_teak, m_tile]
    
    # 1. Wall-Hung D-Shaped Curved WC (West Wall: X = -5.5, Y = 0.2, Facing North-South)
    # In-wall cistern enclosure with chamfered top
    add_beveled_box(bm, -5.76, 0.04, 0.12, 0.22, 0.48, 0.74, bevel_r=0.015, segs=2, mat_idx=0)
    add_beveled_box(bm, -5.53, 0.18, 0.62, 0.02, 0.20, 0.14, bevel_r=0.005, mat_idx=1) # Flush plate
    # D-Shaped Curved Ceramic Toilet Bowl (Lathe curved contour)
    wc_prof = [
        (0.18, 0.00), (0.21, 0.08), (0.22, 0.20), (0.21, 0.24)
    ]
    add_lathe_mesh(bm, -5.32, 0.28, 0.20, wc_prof, segs=16, mat_idx=0)
    # Seat cover with bullnose edge
    add_cylinder(bm, -5.32, 0.28, 0.44, 0.22, 0.03, segs=16, mat_idx=0)
    
    # 2. Floating Vanity & Oval Ceramic Washbasin (North Wall: X [-4.4, -3.4], Y = 0.85)
    add_beveled_box(bm, -4.42, 0.70, 0.02, 1.04, 0.50, 0.78, bevel_r=0.02, segs=2, mat_idx=4)
    add_fluted_panel(bm, -4.40, 0.69, 0.15, 1.00, 0.02, 0.55, num_flutes=10, axis='X', mat_idx=4)
    
    # Oval Ceramic Vessel Basin
    add_lathe_mesh(bm, -3.90, 0.95, 0.80, [(0.14, 0.0), (0.24, 0.12)], segs=20, mat_idx=0)
    # Swept Chrome Faucet
    faucet_prof = [(0.018, 0.0), (0.015, 0.16), (0.012, 0.22), (0.012, 0.18)]
    add_lathe_mesh(bm, -3.90, 1.12, 0.80, faucet_prof, segs=12, mat_idx=1)
    
    # Backlit LED Rounded Mirror
    add_beveled_box(bm, -4.32, 1.18, 0.98, 0.84, 0.025, 0.44, bevel_r=0.04, segs=2, mat_idx=3)
    
    # 3. Walk-in Shower Enclosure (South Portion: X [-5.7, -4.2], Y [-0.95, -0.15])
    # Frameless Tempered Glass Screen with Chrome Wall Clamps
    add_beveled_box(bm, -4.26, -0.96, 0.02, 0.025, 0.82, 1.40, bevel_r=0.005, mat_idx=2)
    # Chrome pivot clamps
    add_cylinder(bm, -4.25, -0.95, 0.30, 0.02, 0.04, segs=8, mat_idx=1)
    add_cylinder(bm, -4.25, -0.95, 1.10, 0.02, 0.04, segs=8, mat_idx=1)
    # Swept Rain Shower Arm & Diffuser Head
    add_cylinder(bm, -5.60, -0.85, 1.36, 0.015, 0.38, segs=8, mat_idx=1)
    add_lathe_mesh(bm, -5.25, -0.85, 1.34, [(0.12, 0.0), (0.13, 0.02)], segs=16, mat_idx=1)
    
    # 4. Chrome Tubular Towel Rail with Folded Towel
    add_cylinder(bm, -3.36, -0.40, 0.85, 0.012, 0.52, segs=8, mat_idx=1)
    add_beveled_box(bm, -3.34, -0.36, 0.54, 0.025, 0.42, 0.34, bevel_r=0.015, segs=2, mat_idx=0)
    
    return build_object_from_bmesh("Sanitary_Bathroom_W", bm, mat_list, col)

def generate_vastu_compass(col):
    """
    Multi-ringed Vastu Purusha Mandala Compass Rose on ground patio.
    """
    bm = bmesh.new()
    m_brass = MATS["Mat_Brass_Gold"]
    m_marble = MATS["Mat_Floor_Marble"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_light = MATS["Mat_Warm_Light"]
    
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

# =====================================================================
# 6. 3D VASTU LABELS
# =====================================================================
def add_vastu_labels(col):
    brass_mat = MATS["Mat_Brass_Gold"]
    
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

# =====================================================================
# 7. CAMERAS & LIGHTING
# =====================================================================
def setup_lighting_and_cameras():
    col_light = get_or_create_collection("04_Lighting_Cameras")
    
    sun_data = bpy.data.lights.new(name="Sun_Vastu", type='SUN')
    sun_data.energy = 5.2
    sun_data.color = (1.0, 0.96, 0.90)
    sun_data.angle = math.radians(8.0)
    sun_obj = bpy.data.objects.new(name="Sun_Vastu", object_data=sun_data)
    sun_obj.location = (10.0, 8.0, 14.0)
    sun_obj.rotation_euler = (math.radians(35.0), math.radians(-25.0), math.radians(45.0))
    col_light.objects.link(sun_obj)
    
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

# =====================================================================
# 8. MAIN EXECUTION PIPELINE
# =====================================================================
def run_vastu_home_pro():
    print("=========================================================")
    print("STARTING PRO ARCHITECTURAL VASTU HOME BUILD (TRIAD 1->2->3)")
    print("=========================================================")
    
    cleanup_scene()
    init_palette()
    
    col_arch = get_or_create_collection("01_Architecture")
    col_furn = get_or_create_collection("02_Furnishings")
    col_labels = get_or_create_collection("03_Vastu_Labels")
    
    print("1. Generating Architectural Foundation & Sacred Medallion...")
    generate_floors_and_plinth(col_arch)
    
    print("2. Generating Walls, Architraves, Casings, Indian Arch & Doors...")
    generate_walls_and_openings(col_arch)
    
    print("3. Generating Master Bedroom with Fluted Headboard & Spindles...")
    generate_master_bedroom(col_furn)
    
    print("4. Generating Guest Bedroom & Ergonomic Study Workstation...")
    generate_guest_bedroom(col_furn)
    
    print("5. Generating Curved Living Sofa Suite & Temple Mandir...")
    generate_living_room_and_mandir(col_furn)
    
    print("6. Generating Bullnose Kitchen Granite Counter & Dining Suite...")
    generate_kitchen_and_dining(col_furn)
    
    print("7. Generating D-Shaped Sanitary WC, Basin & Glass Shower...")
    generate_bathroom_sanitary(col_furn)
    
    print("8. Generating Vastu Mandala Compass Rose...")
    generate_vastu_compass(col_arch)
    
    print("9. Generating Floating 3D Vastu Room Titles...")
    add_vastu_labels(col_labels)
    
    print("10. Setting up Cinematic Lights & Cameras...")
    setup_lighting_and_cameras()
    
    print("=========================================================")
    print("SUCCESS: PRO ARCHITECTURAL HOME GENERATED IN BLENDER!")
    print("=========================================================")

run_vastu_home_pro()
