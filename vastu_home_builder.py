"""
Indian Vastu Shastra Compliant 2BHK Architectural Home Design
Procedural Blender 3D Engine (90/10 Hybrid BMesh Pipeline)

Vastu Directional Matrix:
- North (+Y): Kubera (Wealth, Prosperity)
- East (+X): Surya & Indra (Vitality, Health, Clarity)
- South (-Y): Yama (Stability, Strength)
- West (-X): Varuna (Water, Balance)
- South-West (SW / Nairutya): Master Bedroom (Stability, Heavy Earth Element)
- South-East (SE / Agni): Modular Kitchen & Dining (Fire Element, Cook facing East)
- North-East (NE / Ishanya): Living / Guest Lounge & Sacred Mandir (Divine Space & Water Element)
- North-West (NW / Vayu): 2nd Bedroom / Guest / Study Room (Movement & Air Element)
- West / North-West: Restroom & Bathroom (Waste elimination, Water drainage)
- Center (Brahmasthan): Open Cosmic Foyer (Akasha / Space, Zero Obstructions)
"""

import bpy
import bmesh
from mathutils import Matrix, Vector
import math

# ==========================================
# 1. SCENE CLEANUP
# ==========================================
def cleanup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for collection in [bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights]:
        for block in collection:
            if block.users == 0:
                collection.remove(block)

# ==========================================
# 2. MATERIAL FACTORY
# ==========================================
MATS = {}

def get_or_create_material(name, color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0, alpha=1.0, transmission=0.0, emission_color=(0,0,0,1), emission_strength=0.0, ior=1.45):
    if name in MATS:
        return MATS[name]
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
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
    get_or_create_material("Mat_Plinth", (0.32, 0.33, 0.35, 1.0), roughness=0.65)
    get_or_create_material("Mat_Wall_Ext", (0.94, 0.92, 0.88, 1.0), roughness=0.8)
    get_or_create_material("Mat_Wall_Int", (0.97, 0.96, 0.94, 1.0), roughness=0.8)
    get_or_create_material("Mat_Wall_Accent", (0.24, 0.36, 0.40, 1.0), roughness=0.55) # Modern slate-teal
    get_or_create_material("Mat_Wall_Cap", (0.22, 0.16, 0.12, 1.0), roughness=0.35) # Dark mahogany coping
    
    # Floors
    get_or_create_material("Mat_Floor_Marble", (0.93, 0.91, 0.86, 1.0), roughness=0.12) # Italian Botticino
    get_or_create_material("Mat_Floor_Inlay", (0.46, 0.28, 0.14, 1.0), roughness=0.2) # Brahmasthan Medallion
    get_or_create_material("Mat_Floor_Wood_Master", (0.38, 0.23, 0.13, 1.0), roughness=0.32) # Dark Walnut
    get_or_create_material("Mat_Floor_Wood_Guest", (0.76, 0.62, 0.44, 1.0), roughness=0.35) # Scandinavian Oak
    get_or_create_material("Mat_Floor_Kitchen", (0.84, 0.82, 0.79, 1.0), roughness=0.20) # Vitrified tile
    get_or_create_material("Mat_Floor_Bath", (0.32, 0.34, 0.38, 1.0), roughness=0.35) # Charcoal anti-skid
    get_or_create_material("Mat_Wall_Bath_Tile", (0.90, 0.90, 0.92, 1.0), roughness=0.15) # Ceramic gloss
    
    # Furniture Woods & Surfaces
    get_or_create_material("Mat_Teak_Wood", (0.36, 0.20, 0.10, 1.0), roughness=0.3)
    get_or_create_material("Mat_Light_Wood", (0.82, 0.68, 0.50, 1.0), roughness=0.38)
    get_or_create_material("Mat_Granite_Black", (0.05, 0.05, 0.06, 1.0), roughness=0.06) # Polished Black Granite
    get_or_create_material("Mat_Cabinet_Offwhite", (0.94, 0.93, 0.90, 1.0), roughness=0.25)
    
    # Fabrics & Soft Furnishings
    get_or_create_material("Mat_Fabric_Sofa", (0.70, 0.68, 0.64, 1.0), roughness=0.88) # Warm grey linen
    get_or_create_material("Mat_Fabric_Mustard", (0.88, 0.60, 0.14, 1.0), roughness=0.85) # Saffron/Mustard
    get_or_create_material("Mat_Fabric_Teal", (0.10, 0.40, 0.46, 1.0), roughness=0.85) # Peacock Teal
    get_or_create_material("Mat_Bed_Master_Navy", (0.08, 0.14, 0.22, 1.0), roughness=0.75) # Royal Navy
    get_or_create_material("Mat_Bed_Guest_Sage", (0.32, 0.46, 0.35, 1.0), roughness=0.75) # Sage Green
    get_or_create_material("Mat_Bed_Linen_White", (0.96, 0.96, 0.95, 1.0), roughness=0.8)
    get_or_create_material("Mat_Rug_Living", (0.84, 0.79, 0.72, 1.0), roughness=0.9)
    get_or_create_material("Mat_Rug_Bedroom", (0.76, 0.73, 0.69, 1.0), roughness=0.9)
    get_or_create_material("Mat_Doormat", (0.50, 0.32, 0.18, 1.0), roughness=0.95) # Coir welcome mat
    
    # Metals, Glass & Ceramics
    get_or_create_material("Mat_Brass_Gold", (0.96, 0.80, 0.26, 1.0), roughness=0.18, metallic=1.0) # Mandir, trims
    get_or_create_material("Mat_Chrome", (0.92, 0.92, 0.94, 1.0), roughness=0.06, metallic=1.0) # Fixtures
    get_or_create_material("Mat_Glass_Clear", (0.92, 0.96, 1.0, 1.0), roughness=0.03, alpha=0.35) # Clear architectural glass
    get_or_create_material("Mat_Ceramic_White", (0.97, 0.97, 0.98, 1.0), roughness=0.05) # Sanitaryware
    get_or_create_material("Mat_Mirror", (0.95, 0.95, 0.96, 1.0), roughness=0.02, metallic=1.0)
    
    # TV Screen & Lighting
    get_or_create_material("Mat_TV_Display", (0.12, 0.28, 0.45, 1.0), roughness=0.08, emission_color=(0.15, 0.35, 0.55, 1.0), emission_strength=1.5)
    get_or_create_material("Mat_Warm_Light", (1.0, 0.92, 0.75, 1.0), roughness=0.2, emission_color=(1.0, 0.88, 0.55, 1.0), emission_strength=5.0)
    get_or_create_material("Mat_Diya_Flame", (1.0, 0.45, 0.05, 1.0), roughness=0.1, emission_color=(1.0, 0.40, 0.02, 1.0), emission_strength=12.0)
    
    # Nature & Grounds
    get_or_create_material("Mat_Foliage", (0.14, 0.44, 0.12, 1.0), roughness=0.55)
    get_or_create_material("Mat_Planter_Ceramic", (0.90, 0.89, 0.87, 1.0), roughness=0.2)
    get_or_create_material("Mat_Lawn_Grass", (0.22, 0.38, 0.16, 1.0), roughness=0.8)
    get_or_create_material("Mat_Text_Label", (0.15, 0.15, 0.18, 1.0), roughness=0.2, metallic=0.5)

# ==========================================
# 3. BMESH PRIMITIVE HELPERS
# ==========================================
def add_box(bm, x, y, z, sx, sy, sz, mat_idx=0):
    verts = [
        bm.verts.new((x, y, z)),
        bm.verts.new((x + sx, y, z)),
        bm.verts.new((x + sx, y + sy, z)),
        bm.verts.new((x, y + sy, z)),
        bm.verts.new((x, y, z + sz)),
        bm.verts.new((x + sx, y, z + sz)),
        bm.verts.new((x + sx, y + sy, z + sz)),
        bm.verts.new((x, y + sy, z + sz))
    ]
    faces = [
        (0, 1, 2, 3), # Bottom
        (4, 7, 6, 5), # Top
        (0, 4, 5, 1), # Front (-Y)
        (1, 5, 6, 2), # Right (+X)
        (2, 6, 7, 3), # Back (+Y)
        (3, 7, 4, 0)  # Left (-X)
    ]
    created = []
    for f_idx in faces:
        try:
            f = bm.faces.new([verts[i] for i in f_idx])
            f.material_index = mat_idx
            created.append(f)
        except Exception:
            pass
    return created

def add_cylinder(bm, cx, cy, cz, radius, height, segs=16, mat_idx=0):
    bottom_verts = []
    top_verts = []
    for i in range(segs):
        angle = 2 * math.pi * i / segs
        vx = cx + radius * math.cos(angle)
        vy = cy + radius * math.sin(angle)
        bottom_verts.append(bm.verts.new((vx, vy, cz)))
        top_verts.append(bm.verts.new((vx, vy, cz + height)))
        
    created = []
    for i in range(segs):
        next_i = (i + 1) % segs
        f = bm.faces.new([bottom_verts[i], bottom_verts[next_i], top_verts[next_i], top_verts[i]])
        f.material_index = mat_idx
        created.append(f)
        
    try:
        fb = bm.faces.new(reversed(bottom_verts))
        fb.material_index = mat_idx
        created.append(fb)
        ft = bm.faces.new(top_verts)
        ft.material_index = mat_idx
        created.append(ft)
    except Exception:
        pass
    return created

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

# ==========================================
# 4. ARCHITECTURE GENERATION
# ==========================================
def generate_floors_and_plinth(col):
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
    # Indices: 0: Plinth, 1: Marble, 2: Inlay, 3: Wood Master, 4: Wood Guest, 5: Kitchen, 6: Bath, 7: Grass, 8: Brass
    
    # Outdoor Lawn Garden
    add_box(bm, -8.2, -7.8, -0.22, 16.4, 15.6, 0.06, mat_idx=7)
    
    # Plinth Platform
    add_box(bm, -6.5, -6.0, -0.16, 13.0, 12.0, 0.16, mat_idx=0)
    
    # Entrance Steps at East/North-East (X: 2.2 to 3.8, Y: 5.5 to 6.3)
    add_box(bm, 2.0, 5.5, -0.16, 2.0, 0.8, 0.08, mat_idx=0)
    add_box(bm, 2.2, 5.5, -0.08, 1.6, 0.4, 0.08, mat_idx=1)
    
    # Room Floors (Z: 0.0 to 0.02)
    # 1. Master Bedroom (SW)
    add_box(bm, -5.8, -5.3, 0.0, 4.8, 4.1, 0.02, mat_idx=3)
    # 2. Bathroom & Toilet (West)
    add_box(bm, -5.8, -1.0, 0.0, 2.6, 2.2, 0.02, mat_idx=6)
    # 3. 2nd Bedroom (NW)
    add_box(bm, -5.8, 1.4, 0.0, 4.8, 3.9, 0.02, mat_idx=4)
    # 4. Kitchen & Dining (SE)
    add_box(bm, 1.0, -5.3, 0.0, 4.8, 5.1, 0.02, mat_idx=5)
    # 5. Living Room / Guest Area (NE)
    add_box(bm, 1.0, 0.0, 0.0, 4.8, 5.3, 0.02, mat_idx=1)
    # 6. Central Corridor & Hallway
    add_box(bm, -1.0, -5.3, 0.0, 2.0, 10.6, 0.02, mat_idx=1)
    add_box(bm, -3.2, -1.2, 0.0, 2.2, 2.6, 0.02, mat_idx=1)
    
    # 7. Brahmasthan Sacred Center Medallion (Center X=0, Y=0)
    add_box(bm, -0.9, -0.9, 0.021, 1.8, 1.8, 0.005, mat_idx=2)
    add_box(bm, -0.7, -0.7, 0.023, 1.4, 1.4, 0.005, mat_idx=1)
    add_box(bm, -0.25, -0.25, 0.025, 0.5, 0.5, 0.005, mat_idx=8) # Brass center
    
    return build_object_from_bmesh("Arch_Floors_Plinth", bm, mat_list, col)

def generate_walls_and_doorways(col):
    bm = bmesh.new()
    m_ext = MATS["Mat_Wall_Ext"]
    m_int = MATS["Mat_Wall_Int"]
    m_accent = MATS["Mat_Wall_Accent"]
    m_cap = MATS["Mat_Wall_Cap"]
    m_glass = MATS["Mat_Glass_Clear"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_brass = MATS["Mat_Brass_Gold"]
    
    mat_list = [m_ext, m_int, m_accent, m_cap, m_glass, m_teak, m_brass]
    # 0: Ext, 1: Int, 2: Accent, 3: Cap, 4: Glass, 5: Teak, 6: Brass
    
    wall_h = 1.45
    cap_h = 0.04
    t_ext = 0.20
    t_int = 0.15
    
    def wall_segment(x, y, z, sx, sy, sz, mat_idx=0, has_cap=True):
        add_box(bm, x, y, z, sx, sy, sz, mat_idx=mat_idx)
        if has_cap:
            add_box(bm, x - 0.02, y - 0.02, z + sz, sx + 0.04, sy + 0.04, cap_h, mat_idx=3)
            
    def window_wall_x(x, y, length, sill_h=0.55, win_w=1.6):
        p1 = (length - win_w) / 2
        wall_segment(x, y, 0.0, p1, t_ext, wall_h, mat_idx=0)
        wall_segment(x + p1 + win_w, y, 0.0, p1, t_ext, wall_h, mat_idx=0)
        add_box(bm, x + p1, y, 0.0, win_w, t_ext, sill_h, mat_idx=0) # Sill
        add_box(bm, x + p1 - 0.02, y - 0.02, sill_h, win_w + 0.04, t_ext + 0.04, 0.03, mat_idx=3)
        # Window Frame & Glass
        add_box(bm, x + p1 + 0.02, y + t_ext/2 - 0.015, sill_h + 0.03, win_w - 0.04, 0.03, wall_h - sill_h - 0.03, mat_idx=4)
        # Teak Frame border
        add_box(bm, x + p1, y + t_ext/2 - 0.02, sill_h + 0.03, 0.04, 0.04, wall_h - sill_h - 0.03, mat_idx=3)
        add_box(bm, x + p1 + win_w - 0.04, y + t_ext/2 - 0.02, sill_h + 0.03, 0.04, 0.04, wall_h - sill_h - 0.03, mat_idx=3)
        
    def window_wall_y(x, y, length, sill_h=0.55, win_w=1.6):
        p1 = (length - win_w) / 2
        wall_segment(x, y, 0.0, t_ext, p1, wall_h, mat_idx=0)
        wall_segment(x, y + p1 + win_w, 0.0, t_ext, p1, wall_h, mat_idx=0)
        add_box(bm, x, y + p1, 0.0, t_ext, win_w, sill_h, mat_idx=0) # Sill
        add_box(bm, x - 0.02, y + p1 - 0.02, sill_h, t_ext + 0.04, win_w + 0.04, 0.03, mat_idx=3)
        # Window Frame & Glass
        add_box(bm, x + t_ext/2 - 0.015, y + p1 + 0.02, sill_h + 0.03, 0.03, win_w - 0.04, wall_h - sill_h - 0.03, mat_idx=4)
        add_box(bm, x + t_ext/2 - 0.02, y + p1, sill_h + 0.03, 0.04, 0.04, wall_h - sill_h - 0.03, mat_idx=3)
        add_box(bm, x + t_ext/2 - 0.02, y + p1 + win_w - 0.04, sill_h + 0.03, 0.04, 0.04, wall_h - sill_h - 0.03, mat_idx=3)

    # 1. EXTERIOR PERIMETER
    # South Wall
    window_wall_x(-6.0, -5.5, 5.0, sill_h=0.6, win_w=1.6)
    wall_segment(-1.0, -5.5, 0.0, 2.0, t_ext, wall_h, mat_idx=0)
    window_wall_x(1.0, -5.5, 5.0, sill_h=0.7, win_w=1.4)
    
    # North Wall
    window_wall_x(-6.0, 5.3, 5.0, sill_h=0.6, win_w=1.6)
    wall_segment(-1.0, 5.3, 0.0, 2.0, t_ext, wall_h, mat_idx=0)
    wall_segment(1.0, 5.3, 0.0, 1.4, t_ext, wall_h, mat_idx=0)
    # Main Entrance Opening at X: 2.4 to 3.4
    add_box(bm, 2.4, 5.3, 0.0, 1.0, t_ext, 0.04, mat_idx=3) # Threshold
    # Welcoming Half-Open Main Entrance Door
    add_box(bm, 2.42, 5.32, 0.04, 0.05, 0.85, 1.38, mat_idx=5) # Door panel swung inward
    add_cylinder(bm, 2.47, 5.45, 0.70, 0.015, 0.12, segs=8, mat_idx=6) # Brass handle
    window_wall_x(3.4, 5.3, 2.6, sill_h=0.55, win_w=1.2)
    
    # West Wall
    window_wall_y(-6.0, -5.3, 4.3, sill_h=0.6, win_w=1.4)
    wall_segment(-6.0, -1.0, 0.0, t_ext, 0.6, wall_h, mat_idx=0)
    add_box(bm, -6.0, -0.4, 0.9, t_ext, 0.8, 0.03, mat_idx=3)
    add_box(bm, -6.0 + t_ext/2 - 0.01, -0.4, 0.93, 0.02, 0.8, wall_h - 0.93, mat_idx=4)
    wall_segment(-6.0, 0.4, 0.0, t_ext, 0.8, wall_h, mat_idx=0)
    window_wall_y(-6.0, 1.2, 4.1, sill_h=0.6, win_w=1.4)
    
    # East Wall
    window_wall_y(5.8, -5.3, 5.1, sill_h=0.7, win_w=1.5)
    window_wall_y(5.8, -0.2, 5.5, sill_h=0.5, win_w=2.0)
    
    # 2. INTERIOR PARTITIONS & DOORS
    # Master Bedroom North Wall
    wall_segment(-5.8, -1.2, 0.0, 3.8, t_int, wall_h, mat_idx=1)
    add_box(bm, -2.0, -1.2, 0.0, 0.9, t_int, 0.03, mat_idx=3) # Doorway threshold
    # Master Bedroom Door (swung ajar into bedroom)
    add_box(bm, -1.98, -1.75, 0.03, 0.04, 0.82, 1.38, mat_idx=5)
    wall_segment(-1.1, -1.2, 0.0, 0.1, t_int, wall_h, mat_idx=1)
    
    # Master Bedroom East Wall
    wall_segment(-1.0, -5.3, 0.0, t_int, 4.1, wall_h, mat_idx=1)
    
    # Bathroom East Wall
    wall_segment(-3.2, -1.0, 0.0, t_int, 1.0, wall_h, mat_idx=1)
    add_box(bm, -3.2, 0.0, 0.0, t_int, 0.9, 0.03, mat_idx=3) # Threshold
    # Bathroom Door (swung inward)
    add_box(bm, -3.75, 0.02, 0.03, 0.78, 0.04, 1.38, mat_idx=5)
    wall_segment(-3.2, 0.9, 0.0, t_int, 0.3, wall_h, mat_idx=1)
    
    # Bathroom North Wall
    wall_segment(-5.8, 1.2, 0.0, 2.75, t_int, wall_h, mat_idx=1)
    
    # 2nd Bedroom South Wall
    wall_segment(-3.05, 1.25, 0.0, 2.05, t_int, wall_h, mat_idx=1)
    
    # 2nd Bedroom East Wall
    add_box(bm, -1.0, 1.4, 0.0, t_int, 0.9, 0.03, mat_idx=3) # Threshold
    # 2nd Bed Door (swung inward)
    add_box(bm, -1.65, 1.42, 0.03, 0.78, 0.04, 1.38, mat_idx=5)
    wall_segment(-1.0, 2.3, 0.0, t_int, 3.0, wall_h, mat_idx=1)
    
    # Kitchen & Living Dividing Wall
    wall_segment(4.0, -0.2, 0.0, 1.8, t_int, wall_h, mat_idx=1)
    add_box(bm, 2.0, -0.2, 0.0, 2.0, t_int, 0.85, mat_idx=1) # Low counter
    add_box(bm, 1.95, -0.22, 0.85, 2.1, t_int + 0.04, 0.04, mat_idx=3)
    add_box(bm, 1.0, -0.2, 0.0, 1.0, t_int, 0.03, mat_idx=3) # Threshold
    
    # East Wall of Central Corridor
    wall_segment(0.85, -5.3, 0.0, t_int, 2.3, wall_h, mat_idx=1)
    add_box(bm, 0.85, -3.0, 0.0, t_int, 1.0, 0.03, mat_idx=3)
    wall_segment(0.85, -2.0, 0.0, t_int, 1.95, wall_h, mat_idx=1)
    add_box(bm, 0.85, 0.5, 0.0, t_int, 2.0, 0.03, mat_idx=3)
    wall_segment(0.85, 2.5, 0.0, t_int, 2.8, wall_h, mat_idx=1)
    
    # Feature Accent Walls
    add_box(bm, 3.4, 5.22, 0.0, 1.2, 0.06, wall_h, mat_idx=2) # TV Wall
    add_box(bm, -4.8, -5.28, 0.0, 2.8, 0.06, wall_h, mat_idx=2) # Master Bed Accent

    return build_object_from_bmesh("Arch_Walls_Cutaway", bm, mat_list, col)

# ==========================================
# 5. FURNITURE GENERATORS
# ==========================================
def generate_master_bedroom(col):
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
    
    # Area Rug
    add_box(bm, -4.8, -5.1, 0.021, 2.8, 3.2, 0.015, mat_idx=6)
    
    # King Bed (South Wall: Center X = -3.4, Y = -5.2)
    add_box(bm, -4.5, -5.25, 0.02, 2.2, 0.12, 1.15, mat_idx=0) # Wooden headboard
    add_box(bm, -4.4, -5.23, 0.25, 2.0, 0.08, 0.85, mat_idx=1) # Navy padded insert
    add_box(bm, -4.4, -5.15, 0.02, 2.0, 2.1, 0.32, mat_idx=0) # Frame
    add_box(bm, -4.35, -5.1, 0.34, 1.9, 2.0, 0.25, mat_idx=2) # Mattress
    add_box(bm, -4.37, -4.6, 0.35, 1.94, 1.45, 0.26, mat_idx=1) # Duvet
    add_box(bm, -4.38, -3.8, 0.62, 1.96, 0.45, 0.02, mat_idx=3) # Mustard runner
    
    # Pillows
    add_box(bm, -4.25, -4.95, 0.60, 0.75, 0.45, 0.12, mat_idx=2)
    add_box(bm, -3.30, -4.95, 0.60, 0.75, 0.45, 0.12, mat_idx=2)
    add_box(bm, -4.20, -4.85, 0.65, 0.65, 0.35, 0.10, mat_idx=1)
    add_box(bm, -3.25, -4.85, 0.65, 0.65, 0.35, 0.10, mat_idx=3)
    
    # Nightstands
    for nx in [-5.05, -2.25]:
        add_box(bm, nx, -5.2, 0.02, 0.55, 0.45, 0.52, mat_idx=0)
        add_box(bm, nx + 0.05, -5.18, 0.28, 0.45, 0.02, 0.18, mat_idx=4)
        add_cylinder(bm, nx + 0.27, -4.97, 0.54, 0.10, 0.03, segs=12, mat_idx=4)
        add_cylinder(bm, nx + 0.27, -4.97, 0.57, 0.02, 0.22, segs=8, mat_idx=4)
        add_cylinder(bm, nx + 0.27, -4.97, 0.75, 0.14, 0.20, segs=16, mat_idx=5)
        
    # Master Wardrobe (West Wall)
    add_box(bm, -5.7, -3.8, 0.02, 0.65, 2.2, 1.40, mat_idx=0)
    for i in range(4):
        dy = -3.8 + i * 0.55
        add_box(bm, -5.04, dy + 0.02, 0.06, 0.02, 0.51, 1.32, mat_idx=0)
        add_box(bm, -5.02, dy + 0.45, 0.60, 0.02, 0.03, 0.20, mat_idx=4)
        
    # Dressing Vanity
    add_box(bm, -1.5, -3.6, 0.02, 0.45, 1.0, 0.75, mat_idx=0)
    add_box(bm, -1.48, -3.55, 0.55, 0.02, 0.90, 0.15, mat_idx=4)
    add_box(bm, -1.12, -3.5, 0.85, 0.04, 0.80, 0.55, mat_idx=0)
    add_box(bm, -1.13, -3.46, 0.89, 0.02, 0.72, 0.47, mat_idx=7)
    add_box(bm, -1.9, -3.3, 0.02, 0.35, 0.40, 0.45, mat_idx=0)
    add_box(bm, -1.92, -3.32, 0.45, 0.39, 0.44, 0.08, mat_idx=3)
    
    return build_object_from_bmesh("Furn_Master_Bedroom_SW", bm, mat_list, col)

def generate_guest_bedroom(col):
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
    
    # Floor Rug
    add_box(bm, -5.2, 2.0, 0.021, 2.4, 2.6, 0.015, mat_idx=8)
    
    # Queen Bed
    add_box(bm, -5.75, 2.3, 0.02, 0.12, 1.8, 1.05, mat_idx=1)
    add_box(bm, -5.72, 2.4, 0.25, 0.08, 1.6, 0.75, mat_idx=2)
    add_box(bm, -5.63, 2.4, 0.02, 2.05, 1.6, 0.30, mat_idx=0)
    add_box(bm, -5.58, 2.45, 0.32, 1.95, 1.5, 0.22, mat_idx=3)
    add_box(bm, -5.1, 2.43, 0.33, 1.45, 1.54, 0.24, mat_idx=2)
    add_box(bm, -4.1, 2.42, 0.58, 0.40, 1.56, 0.02, mat_idx=4)
    
    # Pillows
    add_box(bm, -5.5, 2.55, 0.55, 0.45, 0.60, 0.12, mat_idx=3)
    add_box(bm, -5.5, 3.25, 0.55, 0.45, 0.60, 0.12, mat_idx=3)
    add_box(bm, -5.35, 2.65, 0.60, 0.35, 0.45, 0.10, mat_idx=4)
    
    # Nightstand
    add_box(bm, -5.7, 4.2, 0.02, 0.50, 0.45, 0.50, mat_idx=0)
    add_cylinder(bm, -5.45, 4.42, 0.52, 0.08, 0.02, segs=12, mat_idx=5)
    add_cylinder(bm, -5.45, 4.42, 0.54, 0.015, 0.20, segs=8, mat_idx=5)
    add_cylinder(bm, -5.45, 4.42, 0.70, 0.12, 0.16, segs=16, mat_idx=6)
    
    # Study Desk & Workstation
    add_box(bm, -3.0, 4.8, 0.02, 1.5, 0.48, 0.74, mat_idx=0)
    add_box(bm, -2.95, 4.82, 0.05, 0.35, 0.44, 0.65, mat_idx=1)
    add_box(bm, -2.3, 4.9, 0.76, 0.32, 0.22, 0.015, mat_idx=5)
    add_box(bm, -2.3, 5.11, 0.77, 0.32, 0.015, 0.20, mat_idx=7)
    add_box(bm, -1.8, 4.95, 0.76, 0.20, 0.25, 0.08, mat_idx=4)
    add_cylinder(bm, -2.2, 4.4, 0.02, 0.24, 0.45, segs=12, mat_idx=5)
    add_box(bm, -2.38, 4.25, 0.47, 0.40, 0.40, 0.08, mat_idx=4)
    add_box(bm, -2.38, 4.23, 0.55, 0.40, 0.06, 0.38, mat_idx=4)
    
    # Wardrobe
    add_box(bm, -1.5, 2.0, 0.02, 0.45, 1.4, 1.40, mat_idx=0)
    add_box(bm, -1.48, 2.05, 0.06, 0.02, 0.62, 1.30, mat_idx=1)
    add_box(bm, -1.48, 2.73, 0.06, 0.02, 0.62, 1.30, mat_idx=1)
    
    return build_object_from_bmesh("Furn_Guest_Bedroom_NW", bm, mat_list, col)

def generate_living_room_and_mandir(col):
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
    
    # Entrance Welcome Mat
    add_box(bm, 2.5, 5.0, 0.021, 0.8, 0.45, 0.015, mat_idx=11)
    
    # Living Room Area Rug
    add_box(bm, 1.6, 1.0, 0.021, 3.4, 2.8, 0.015, mat_idx=7)
    
    # 3-Seater Sofa
    add_box(bm, 2.1, 1.2, 0.02, 2.4, 0.85, 0.42, mat_idx=0)
    add_box(bm, 2.1, 1.2, 0.42, 2.4, 0.22, 0.40, mat_idx=0)
    add_box(bm, 2.0, 1.2, 0.02, 0.15, 0.85, 0.60, mat_idx=0)
    add_box(bm, 4.45, 1.2, 0.02, 0.15, 0.85, 0.60, mat_idx=0)
    add_box(bm, 2.3, 1.42, 0.44, 0.40, 0.15, 0.35, mat_idx=1)
    add_box(bm, 3.8, 1.42, 0.44, 0.40, 0.15, 0.35, mat_idx=2)
    
    # Armchairs
    add_box(bm, 1.5, 2.2, 0.02, 0.75, 0.75, 0.40, mat_idx=2)
    add_box(bm, 1.5, 2.2, 0.40, 0.20, 0.75, 0.38, mat_idx=2)
    add_box(bm, 1.7, 2.35, 0.42, 0.35, 0.35, 0.12, mat_idx=1)
    
    add_box(bm, 4.4, 2.2, 0.02, 0.75, 0.75, 0.40, mat_idx=1)
    add_box(bm, 4.95, 2.2, 0.40, 0.20, 0.75, 0.38, mat_idx=1)
    add_box(bm, 4.6, 2.35, 0.42, 0.35, 0.35, 0.12, mat_idx=2)
    
    # Coffee Table
    add_box(bm, 2.7, 2.1, 0.02, 1.2, 0.65, 0.38, mat_idx=3)
    add_box(bm, 2.65, 2.05, 0.40, 1.3, 0.75, 0.02, mat_idx=5)
    add_box(bm, 2.9, 2.3, 0.42, 0.25, 0.20, 0.03, mat_idx=2)
    add_cylinder(bm, 3.5, 2.4, 0.42, 0.10, 0.05, segs=12, mat_idx=4)
    
    # Entertainment Media Console & TV
    add_box(bm, 3.2, 4.9, 0.15, 1.6, 0.35, 0.35, mat_idx=3)
    add_box(bm, 3.55, 4.95, 0.52, 0.90, 0.10, 0.06, mat_idx=6)
    add_box(bm, 3.3, 5.15, 0.65, 1.4, 0.04, 0.75, mat_idx=6) # Colorful TV display
    add_box(bm, 3.28, 5.14, 0.63, 1.44, 0.02, 0.79, mat_idx=4)
    
    # Planter
    add_cylinder(bm, 1.4, 4.7, 0.02, 0.25, 0.50, segs=16, mat_idx=9)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle)
        lx = 1.4 + 0.22 * math.cos(rad)
        ly = 4.7 + 0.22 * math.sin(rad)
        add_cylinder(bm, lx, ly, 0.52, 0.12, 0.45, segs=6, mat_idx=8)
        
    # Entrance Console
    add_box(bm, 1.2, 5.0, 0.02, 1.0, 0.28, 0.78, mat_idx=3)
    add_cylinder(bm, 1.5, 5.14, 0.80, 0.08, 0.25, segs=12, mat_idx=9)
    
    # SACRED POOJA MANDIR (North-East Corner: +5.0, +4.6)
    mx, my = 5.0, 4.6
    add_box(bm, mx, my, 0.02, 0.75, 0.65, 0.40, mat_idx=3) # Pedestal
    add_box(bm, mx + 0.05, my - 0.01, 0.10, 0.65, 0.02, 0.25, mat_idx=4)
    add_box(bm, mx + 0.02, my + 0.02, 0.42, 0.71, 0.61, 0.04, mat_idx=3)
    for px, py in [(mx + 0.06, my + 0.06), (mx + 0.65, my + 0.06), (mx + 0.06, my + 0.55), (mx + 0.65, my + 0.55)]:
        add_cylinder(bm, px, py, 0.46, 0.025, 0.55, segs=12, mat_idx=4)
    add_box(bm, mx, my, 1.01, 0.75, 0.65, 0.08, mat_idx=3) # Canopy
    add_box(bm, mx + 0.12, my + 0.10, 1.09, 0.51, 0.45, 0.10, mat_idx=4) # Shikhara
    add_box(bm, mx + 0.25, my + 0.20, 1.19, 0.25, 0.25, 0.10, mat_idx=4)
    add_cylinder(bm, mx + 0.375, my + 0.325, 1.29, 0.06, 0.12, segs=12, mat_idx=4) # Kalash
    add_cylinder(bm, mx + 0.375, my + 0.25, 0.85, 0.04, 0.08, segs=10, mat_idx=4) # Bell
    add_cylinder(bm, mx + 0.22, my + 0.20, 0.46, 0.05, 0.06, segs=12, mat_idx=4) # Diya
    add_cylinder(bm, mx + 0.22, my + 0.20, 0.52, 0.02, 0.04, segs=8, mat_idx=10) # Flame
    add_box(bm, mx + 0.30, my + 0.45, 0.46, 0.25, 0.04, 0.35, mat_idx=4)
    
    return build_object_from_bmesh("Furn_Living_Mandir_NE", bm, mat_list, col)

def generate_kitchen_and_dining(col):
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
    
    # Lower Modular Cabinets (L-Shape)
    add_box(bm, 2.0, -5.25, 0.02, 3.7, counter_d, counter_h - 0.04, mat_idx=1)
    add_box(bm, 5.7 - counter_d, -4.60, 0.02, counter_d, 3.8, counter_h - 0.04, mat_idx=1)
    
    for cx in [2.3, 3.0, 3.7, 4.4]:
        add_box(bm, cx, -4.58, counter_h * 0.6, 0.35, 0.02, 0.03, mat_idx=3)
    for cy in [-4.0, -3.2, -2.4, -1.6]:
        add_box(bm, 5.03, cy, counter_h * 0.6, 0.02, 0.35, 0.03, mat_idx=3)
        
    # Granite Tops
    add_box(bm, 1.95, -5.28, counter_h - 0.04, 3.8, counter_d + 0.04, 0.04, mat_idx=0)
    add_box(bm, 5.7 - counter_d - 0.04, -4.60, counter_h - 0.04, counter_d + 0.04, 3.85, 0.04, mat_idx=0)
    
    # 4-Burner Gas Stove (SE Corner: Cook faces East)
    add_box(bm, 4.5, -5.1, counter_h, 0.75, 0.50, 0.03, mat_idx=0)
    for bx, by in [(4.65, -4.98), (4.65, -4.72), (5.05, -4.98), (5.05, -4.72)]:
        add_cylinder(bm, bx, by, counter_h + 0.03, 0.07, 0.02, segs=12, mat_idx=3)
        add_cylinder(bm, bx, by, counter_h + 0.05, 0.04, 0.01, segs=8, mat_idx=4)
    for ki in range(4):
        add_cylinder(bm, 4.6 + ki * 0.15, -5.12, counter_h + 0.015, 0.018, 0.02, segs=8, mat_idx=3)
        
    # Chimney Hood
    add_box(bm, 4.45, -5.1, 1.25, 0.85, 0.48, 0.08, mat_idx=3)
    add_box(bm, 4.65, -5.2, 1.33, 0.45, 0.28, 0.15, mat_idx=3)
    
    # Kitchen Sink (NE of kitchen)
    add_box(bm, 5.15, -1.8, counter_h, 0.48, 0.70, 0.01, mat_idx=3)
    add_box(bm, 5.20, -1.75, counter_h - 0.20, 0.40, 0.60, 0.20, mat_idx=3)
    add_cylinder(bm, 5.58, -1.45, counter_h + 0.01, 0.02, 0.25, segs=8, mat_idx=3)
    add_box(bm, 5.42, -1.46, counter_h + 0.25, 0.18, 0.03, 0.03, mat_idx=3)
    
    # Refrigerator (SW of kitchen)
    add_box(bm, 1.2, -5.2, 0.02, 0.70, 0.65, 1.45, mat_idx=3)
    add_box(bm, 1.22, -4.54, 0.06, 0.66, 0.02, 1.38, mat_idx=3)
    add_box(bm, 1.52, -4.52, 0.60, 0.04, 0.02, 0.45, mat_idx=4)
    
    # Overhead Cabinets
    add_box(bm, 2.2, -5.25, 1.15, 2.0, 0.35, 0.32, mat_idx=1)
    add_box(bm, 5.35, -4.4, 1.15, 0.35, 2.4, 0.32, mat_idx=1)
    
    # Dining Table & Chairs
    add_box(bm, 2.2, -2.9, 0.02, 1.3, 0.90, 0.72, mat_idx=2)
    add_box(bm, 2.15, -2.95, 0.72, 1.4, 1.0, 0.04, mat_idx=2)
    add_cylinder(bm, 2.85, -2.45, 0.76, 0.14, 0.06, segs=12, mat_idx=4)
    add_cylinder(bm, 2.5, -2.45, 0.76, 0.12, 0.015, segs=12, mat_idx=6)
    add_cylinder(bm, 3.2, -2.45, 0.76, 0.12, 0.015, segs=12, mat_idx=6)
    
    for cx in [2.4, 3.0]:
        add_box(bm, cx, -3.35, 0.02, 0.38, 0.38, 0.44, mat_idx=2)
        add_box(bm, cx - 0.01, -3.36, 0.44, 0.40, 0.40, 0.05, mat_idx=1)
        add_box(bm, cx, -3.42, 0.49, 0.38, 0.06, 0.38, mat_idx=2)
    for cx in [2.4, 3.0]:
        add_box(bm, cx, -1.95, 0.02, 0.38, 0.38, 0.44, mat_idx=2)
        add_box(bm, cx - 0.01, -1.96, 0.44, 0.40, 0.40, 0.05, mat_idx=1)
        add_box(bm, cx, -1.60, 0.49, 0.38, 0.06, 0.38, mat_idx=2)
        
    return build_object_from_bmesh("Furn_Kitchen_Dining_SE", bm, mat_list, col)

def generate_bathroom_sanitary(col):
    bm = bmesh.new()
    m_ceramic = MATS["Mat_Ceramic_White"]
    m_chrome = MATS["Mat_Chrome"]
    m_glass = MATS["Mat_Glass_Clear"]
    m_mirror = MATS["Mat_Mirror"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_tile = MATS["Mat_Wall_Bath_Tile"]
    
    mat_list = [m_ceramic, m_chrome, m_glass, m_mirror, m_teak, m_tile]
    
    # Wall-hung WC (Facing North-South)
    add_box(bm, -5.75, 0.05, 0.15, 0.20, 0.45, 0.70, mat_idx=0)
    add_box(bm, -5.54, 0.18, 0.60, 0.02, 0.18, 0.12, mat_idx=1)
    add_box(bm, -5.55, 0.08, 0.20, 0.50, 0.38, 0.24, mat_idx=0)
    add_box(bm, -5.52, 0.09, 0.44, 0.45, 0.36, 0.03, mat_idx=0)
    
    # Vanity Basin & Mirror
    add_box(bm, -4.4, 0.70, 0.02, 1.0, 0.48, 0.78, mat_idx=4)
    add_box(bm, -4.2, 0.72, 0.80, 0.60, 0.42, 0.08, mat_idx=0)
    add_cylinder(bm, -3.9, 1.10, 0.82, 0.02, 0.18, segs=8, mat_idx=1)
    add_box(bm, -3.92, 0.96, 0.98, 0.04, 0.14, 0.03, mat_idx=1)
    add_box(bm, -4.3, 1.18, 1.0, 0.80, 0.02, 0.42, mat_idx=3)
    
    # Walk-in Shower Enclosure
    add_box(bm, -4.25, -0.95, 0.02, 0.03, 0.80, 1.40, mat_idx=2)
    add_cylinder(bm, -4.23, -0.55, 0.60, 0.015, 0.35, segs=8, mat_idx=1)
    add_box(bm, -5.6, -0.85, 1.35, 0.35, 0.03, 0.03, mat_idx=1)
    add_cylinder(bm, -5.25, -0.85, 1.32, 0.12, 0.02, segs=12, mat_idx=1)
    add_cylinder(bm, -5.65, -0.55, 0.90, 0.05, 0.03, segs=8, mat_idx=1)
    
    # Towel Rail
    add_box(bm, -3.35, -0.4, 0.85, 0.04, 0.50, 0.02, mat_idx=1)
    add_box(bm, -3.34, -0.35, 0.55, 0.02, 0.40, 0.32, mat_idx=0)
    
    return build_object_from_bmesh("Sanitary_Bathroom_W", bm, mat_list, col)

def generate_vastu_compass(col):
    bm = bmesh.new()
    m_brass = MATS["Mat_Brass_Gold"]
    m_marble = MATS["Mat_Floor_Marble"]
    m_teak = MATS["Mat_Teak_Wood"]
    m_light = MATS["Mat_Warm_Light"]
    
    mat_list = [m_brass, m_marble, m_teak, m_light]
    
    cx, cy, cz = 6.4, 5.8, 0.02
    radius = 1.0
    
    add_cylinder(bm, cx, cy, cz, radius, 0.03, segs=32, mat_idx=1)
    add_cylinder(bm, cx, cy, cz + 0.03, radius * 0.95, 0.01, segs=32, mat_idx=0)
    add_cylinder(bm, cx, cy, cz + 0.04, radius * 0.85, 0.01, segs=32, mat_idx=2)
    
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        px = cx + 0.75 * math.cos(rad)
        py = cy + 0.75 * math.sin(rad)
        add_box(bm, px - 0.04, py - 0.04, cz + 0.05, 0.08, 0.08, 0.02, mat_idx=0)
        
    nx, ny = cx, cy + 0.72
    add_box(bm, nx - 0.03, ny, cz + 0.06, 0.06, 0.22, 0.04, mat_idx=0)
    
    return build_object_from_bmesh("Vastu_Compass_Indicator", bm, mat_list, col)

# ==========================================
# 6. 3D VASTU LABELS
# ==========================================
def add_vastu_labels(col):
    """Adds clear, readable 3D text labels for all Vastu zones"""
    label_mat = MATS["Mat_Text_Label"]
    brass_mat = MATS["Mat_Brass_Gold"]
    
    labels = [
        ("Label_Master", "MASTER BEDROOM (SW / NAIRUTYA)", (-5.2, -3.2, 1.62), 0.22, brass_mat),
        ("Label_Living", "LIVING & GUEST LOUNGE (NE / ISHANYA)", (1.4, 2.6, 1.62), 0.22, brass_mat),
        ("Label_Mandir", "POOJA MANDIR (NE)", (4.8, 4.3, 1.62), 0.18, brass_mat),
        ("Label_Kitchen", "KITCHEN & DINING (SE / AGNI)", (1.8, -3.8, 1.62), 0.22, brass_mat),
        ("Label_Guest", "2ND BEDROOM / STUDY (NW / VAYU)", (-5.2, 3.8, 1.62), 0.22, brass_mat),
        ("Label_Bath", "RESTROOM & BATH (WEST / VARUNA)", (-5.4, 0.1, 1.62), 0.18, brass_mat),
        ("Label_Center", "BRAHMASTHAN (OPEN CENTER)", (-0.9, 0.2, 1.62), 0.20, brass_mat),
        ("Label_Entrance", "MAIN ENTRANCE (NORTH-EAST)", (1.8, 5.65, 0.10), 0.22, brass_mat),
    ]
    
    for name, text, loc, size, mat in labels:
        font_curve = bpy.data.curves.new(type="FONT", name=name + "_data")
        font_curve.body = text
        font_curve.size = size
        font_curve.extrude = 0.02
        font_curve.bevel_depth = 0.003
        font_obj = bpy.data.objects.new(name, font_curve)
        font_obj.location = loc
        # Align flat facing slightly tilted towards isometric camera
        font_obj.rotation_euler = (math.radians(35.0), 0.0, math.radians(-15.0))
        if mat:
            font_obj.data.materials.append(mat)
        col.objects.link(font_obj)

# ==========================================
# 7. CAMERAS & LIGHTING
# ==========================================
def setup_lighting_and_cameras():
    col_light = get_or_create_collection("04_Lighting_Cameras")
    
    # Sun Light (Warm morning sun from East/North-East)
    sun_data = bpy.data.lights.new(name="Sun_Vastu", type='SUN')
    sun_data.energy = 5.0
    sun_data.color = (1.0, 0.96, 0.90)
    sun_data.angle = math.radians(8.0)
    sun_obj = bpy.data.objects.new(name="Sun_Vastu", object_data=sun_data)
    sun_obj.location = (10.0, 8.0, 14.0)
    sun_obj.rotation_euler = (math.radians(35.0), math.radians(-25.0), math.radians(45.0))
    col_light.objects.link(sun_obj)
    
    # Area Fill Lights for each room
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
    # 1. Main Isometric 3/4 Camera (Southeast view)
    cam1_data = bpy.data.cameras.new(name="Cam_Isometric_Southeast")
    cam1_data.lens = 42.0
    cam1_obj = bpy.data.objects.new(name="Cam_Isometric_Southeast", object_data=cam1_data)
    cam1_obj.location = (14.0, -13.0, 13.5)
    cam1_obj.rotation_euler = (math.radians(52.0), 0.0, math.radians(45.0))
    col_light.objects.link(cam1_obj)
    
    # 2. Southwest Isometric Camera (Master Bedroom & Bathroom focus)
    cam2_data = bpy.data.cameras.new(name="Cam_Isometric_Southwest")
    cam2_data.lens = 42.0
    cam2_obj = bpy.data.objects.new(name="Cam_Isometric_Southwest", object_data=cam2_data)
    cam2_obj.location = (-13.5, -13.5, 13.5)
    cam2_obj.rotation_euler = (math.radians(52.0), 0.0, math.radians(-45.0))
    col_light.objects.link(cam2_obj)
    
    # 3. Top-Down Floorplan Camera (Orthographic)
    cam3_data = bpy.data.cameras.new(name="Cam_TopDown_Floorplan")
    cam3_data.type = 'ORTHO'
    cam3_data.ortho_scale = 16.5
    cam3_obj = bpy.data.objects.new(name="Cam_TopDown_Floorplan", object_data=cam3_data)
    cam3_obj.location = (0.0, 0.0, 18.0)
    cam3_obj.rotation_euler = (0.0, 0.0, 0.0)
    col_light.objects.link(cam3_obj)
    
    # Set default camera
    bpy.context.scene.camera = cam1_obj

# ==========================================
# 8. MAIN DISPATCHER
# ==========================================
def build_vastu_home():
    print("=========================================================")
    print("STARTING COMPLETE VASTU 2BHK ARCHITECTURAL MASTER GENERATION")
    print("=========================================================")
    
    cleanup_scene()
    init_palette()
    
    col_arch = get_or_create_collection("01_Architecture")
    col_furn = get_or_create_collection("02_Furnishings")
    col_labels = get_or_create_collection("03_Vastu_Labels")
    
    print("1. Generating Foundation, Plinth & Floors...")
    generate_floors_and_plinth(col_arch)
    
    print("2. Generating Walls, Cutaways & Doors...")
    generate_walls_and_doorways(col_arch)
    
    print("3. Furnishing Master Bedroom (SW / Nairutya)...")
    generate_master_bedroom(col_furn)
    
    print("4. Furnishing Guest Bedroom / Study (NW / Vayu)...")
    generate_guest_bedroom(col_furn)
    
    print("5. Furnishing Living Lounge & Sacred Mandir (NE / Ishanya)...")
    generate_living_room_and_mandir(col_furn)
    
    print("6. Furnishing Kitchen & Dining (SE / Agni)...")
    generate_kitchen_and_dining(col_furn)
    
    print("7. Generating Restroom & Bathroom (West / Varuna)...")
    generate_bathroom_sanitary(col_furn)
    
    print("8. Generating 3D Vastu Compass...")
    generate_vastu_compass(col_arch)
    
    print("9. Generating 3D Vastu Room Labels...")
    add_vastu_labels(col_labels)
    
    print("10. Setting up Cinematic Lights & Multi-Angle Cameras...")
    setup_lighting_and_cameras()
    
    print("=========================================================")
    print("SUCCESS: INDIAN VASTU 2BHK HOME GENERATED IN BLENDER!")
    print("=========================================================")

build_vastu_home()
