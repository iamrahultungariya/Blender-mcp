"""
PBR Material Factory for Vastu 2BHK Luxury Residence.
Compatible with Blender 4.x / 5.x Principled BSDF socket definitions.
"""

import bpy

MATS = {}

def get_or_create_material(name, color=(0.8, 0.8, 0.8, 1.0), roughness=0.5, metallic=0.0, alpha=1.0, transmission=0.0, emission_color=(0,0,0,1), emission_strength=0.0, ior=1.45):
    mat = bpy.data.materials.get(name)
    if not mat:
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
    global MATS
    MATS.clear()
    
    # Architecture
    get_or_create_material("Mat_Plinth", (0.28, 0.29, 0.31, 1.0), roughness=0.60)
    get_or_create_material("Mat_Wall_Ext", (0.94, 0.92, 0.88, 1.0), roughness=0.82)
    get_or_create_material("Mat_Wall_Int", (0.97, 0.96, 0.94, 1.0), roughness=0.78)
    get_or_create_material("Mat_Wall_Accent", (0.20, 0.32, 0.36, 1.0), roughness=0.50) # Designer slate-teal
    get_or_create_material("Mat_Wall_Cap", (0.18, 0.12, 0.08, 1.0), roughness=0.32) # Dark mahogany coping
    get_or_create_material("Mat_Skirting", (0.22, 0.14, 0.10, 1.0), roughness=0.35) # Wood skirting
    
    # Floors
    get_or_create_material("Mat_Floor_Marble", (0.93, 0.91, 0.86, 1.0), roughness=0.10) # Botticino glossy marble
    get_or_create_material("Mat_Floor_Inlay", (0.45, 0.26, 0.12, 1.0), roughness=0.18) # Inlaid medallion border
    get_or_create_material("Mat_Floor_Wood_Master", (0.34, 0.20, 0.10, 1.0), roughness=0.28) # Walnut parquet
    get_or_create_material("Mat_Floor_Wood_Guest", (0.76, 0.60, 0.42, 1.0), roughness=0.32) # Scandinavian Oak
    get_or_create_material("Mat_Floor_Kitchen", (0.86, 0.84, 0.81, 1.0), roughness=0.16) # Vitrified stone
    get_or_create_material("Mat_Floor_Bath", (0.26, 0.28, 0.32, 1.0), roughness=0.32) # Charcoal slate anti-skid
    get_or_create_material("Mat_Wall_Bath_Tile", (0.92, 0.92, 0.94, 1.0), roughness=0.12) # Glossy subway tile
    
    # Woods & Solids
    get_or_create_material("Mat_Teak_Wood", (0.34, 0.18, 0.08, 1.0), roughness=0.26) # Polished Teak
    get_or_create_material("Mat_Light_Wood", (0.82, 0.68, 0.50, 1.0), roughness=0.35) # Ash/Birch
    get_or_create_material("Mat_Granite_Black", (0.04, 0.04, 0.05, 1.0), roughness=0.04) # Jet Black Bullnose Granite
    get_or_create_material("Mat_Cabinet_Offwhite", (0.95, 0.94, 0.91, 1.0), roughness=0.20)
    
    # Fabrics & Soft Goods (Matching Visual Reference)
    get_or_create_material("Mat_Boucle_Cream", (0.92, 0.90, 0.86, 1.0), roughness=0.88) # Curved boucle sofa
    get_or_create_material("Mat_Fabric_Mustard", (0.88, 0.58, 0.12, 1.0), roughness=0.82) # Accent saffron
    get_or_create_material("Mat_Fabric_Teal", (0.08, 0.38, 0.44, 1.0), roughness=0.82) # Peacock teal
    get_or_create_material("Mat_Bed_Master_Navy", (0.05, 0.10, 0.18, 1.0), roughness=0.68) # Deep Navy Velvet
    get_or_create_material("Mat_Bed_Guest_Sage", (0.30, 0.45, 0.33, 1.0), roughness=0.70) # Sage
    get_or_create_material("Mat_Bed_Linen_White", (0.97, 0.97, 0.96, 1.0), roughness=0.76)
    get_or_create_material("Mat_Rug_Living", (0.86, 0.82, 0.76, 1.0), roughness=0.92)
    get_or_create_material("Mat_Rug_Bedroom", (0.76, 0.73, 0.69, 1.0), roughness=0.92)
    get_or_create_material("Mat_Doormat", (0.48, 0.30, 0.16, 1.0), roughness=0.95)
    
    # Metals, Glass & Ceramics
    get_or_create_material("Mat_Brass_Gold", (0.97, 0.82, 0.28, 1.0), roughness=0.16, metallic=1.0) # Temple brass
    get_or_create_material("Mat_Chrome", (0.92, 0.92, 0.94, 1.0), roughness=0.04, metallic=1.0) # Faucets & hardware
    get_or_create_material("Mat_Glass_Clear", (0.94, 0.97, 1.0, 1.0), roughness=0.02, alpha=0.30)
    get_or_create_material("Mat_Ceramic_White", (0.98, 0.98, 0.99, 1.0), roughness=0.04) # Sanitaryware
    get_or_create_material("Mat_Mirror", (0.96, 0.96, 0.96, 1.0), roughness=0.02, metallic=1.0)
    
    # Lighting & Displays
    get_or_create_material("Mat_TV_Display", (0.10, 0.25, 0.42, 1.0), roughness=0.08, emission_color=(0.15, 0.35, 0.55, 1.0), emission_strength=1.8)
    get_or_create_material("Mat_Warm_Light", (1.0, 0.92, 0.75, 1.0), roughness=0.2, emission_color=(1.0, 0.88, 0.55, 1.0), emission_strength=5.0)
    get_or_create_material("Mat_Diya_Flame", (1.0, 0.45, 0.05, 1.0), roughness=0.1, emission_color=(1.0, 0.40, 0.02, 1.0), emission_strength=14.0)
    
    # Nature & Grounds
    get_or_create_material("Mat_Foliage", (0.12, 0.44, 0.10, 1.0), roughness=0.52)
    get_or_create_material("Mat_Planter_Ceramic", (0.92, 0.91, 0.88, 1.0), roughness=0.18)
    get_or_create_material("Mat_Lawn_Grass", (0.20, 0.36, 0.14, 1.0), roughness=0.82)
    get_or_create_material("Mat_Text_Label", (0.15, 0.15, 0.18, 1.0), roughness=0.2, metallic=0.5)
    
    return MATS
