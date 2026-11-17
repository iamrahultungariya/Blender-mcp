"""
Ambulance Builder - Material Library
Configures all PBR shaders with strictly non-metallic finishes (metallic=0.0).
Features high-gloss automotive clearcoat white paint and dark privacy safety glass.
"""
import bpy

def get_or_create_material(name: str) -> bpy.types.Material:
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    return mat

def setup_ambulance_materials():
    # 1. Non-Metallic Gloss White Clearcoat Automotive Paint
    mat = get_or_create_material("VAN_Paint_White")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.94, 0.95, 0.96, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.14
        bsdf.inputs["Metallic"].default_value = 0.0  # STRICT NON-METALLIC
        if "Coat Weight" in bsdf.inputs:
            bsdf.inputs["Coat Weight"].default_value = 1.0
            bsdf.inputs["Coat Roughness"].default_value = 0.025

    # 2. Textured Dark Matte Grey Cladding, Grille & Moldings
    mat = get_or_create_material("VAN_Cladding_Grey")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.08, 0.08, 0.09, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.72
        bsdf.inputs["Metallic"].default_value = 0.0

    # 3. Tinted Automotive Privacy Safety Glass (Dark High-Gloss Glazing)
    mat = get_or_create_material("VAN_Glass_Tinted")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.015, 0.02, 0.025, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.035
        bsdf.inputs["Metallic"].default_value = 0.0
        bsdf.inputs["IOR"].default_value = 1.52
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.95
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = 0.04
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = 0.04

    # 4. Emergency Red Emissive Strobe
    mat = get_or_create_material("VAN_Strobe_Red")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (1.0, 0.02, 0.02, 1.0)
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.02, 0.02, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 35.0
        bsdf.inputs["Metallic"].default_value = 0.0

    # 5. Emergency Blue Emissive Strobe
    mat = get_or_create_material("VAN_Strobe_Blue")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.02, 0.25, 1.0, 1.0)
        bsdf.inputs["Emission Color"].default_value = (0.02, 0.25, 1.0, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 35.0
        bsdf.inputs["Metallic"].default_value = 0.0

    # 6. Emergency Amber Indicator Strobe
    mat = get_or_create_material("VAN_Strobe_Amber")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (1.0, 0.45, 0.02, 1.0)
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.45, 0.02, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 25.0
        bsdf.inputs["Metallic"].default_value = 0.0

    # 7. Xenon / LED Headlight Projector Emissive
    mat = get_or_create_material("VAN_Headlight_LED")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.95, 0.98, 1.0, 1.0)
        bsdf.inputs["Emission Color"].default_value = (0.95, 0.98, 1.0, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 40.0
        bsdf.inputs["Metallic"].default_value = 0.0

    # 8. Rear LED Taillight Emissive
    mat = get_or_create_material("VAN_Taillight_Red")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.9, 0.02, 0.02, 1.0)
        bsdf.inputs["Emission Color"].default_value = (0.9, 0.02, 0.02, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 20.0
        bsdf.inputs["Metallic"].default_value = 0.0

    # 9. Non-Metallic Painted Wheel Rim (Satin Grey Alloy)
    mat = get_or_create_material("VAN_Wheel_Steel")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.40, 0.42, 0.45, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.30
        bsdf.inputs["Metallic"].default_value = 0.0  # STRICT NON-METALLIC

    # 10. Vulcanized Road Tire Rubber
    mat = get_or_create_material("VAN_Tire_Rubber")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.035, 0.035, 0.04, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.82
        bsdf.inputs["Metallic"].default_value = 0.0

    # 11. Livery Decals & Ground Staging
    for name, col in [
        ("VAN_Decal_Red", (0.85, 0.04, 0.04, 1.0)),
        ("VAN_Decal_Blue", (0.03, 0.22, 0.72, 1.0)),
        ("VAN_Decal_Yellow", (0.88, 0.92, 0.05, 1.0)),
        ("VAN_Decal_White", (0.95, 0.95, 0.95, 1.0)),
        ("AMB_Asphalt_Slab", (0.08, 0.08, 0.09, 1.0)),
        ("AMB_Bay_Line_Yellow", (0.92, 0.78, 0.08, 1.0))
    ]:
        m = get_or_create_material(name)
        b = m.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = col
            b.inputs["Roughness"].default_value = 0.35
            b.inputs["Metallic"].default_value = 0.0

    print("All 15 ambulance materials configured (STRICT NON-METALLIC, PRIVACY GLASS).")
