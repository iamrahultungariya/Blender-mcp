"""Multi-material PBR Shaders for Aesthetic Modern Luxury Bedroom.

Defines decoupled PBR materials with physical roughness, sheen, and transmission.
"""
from __future__ import annotations

import bpy


def get_or_create_material(name: str) -> bpy.types.Material:
    """Create or reset material with clean node tree."""
    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
    else:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new(type="ShaderNodeOutputMaterial")
    out.location = (600, 0)
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (200, 0)
    mat.node_tree.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def set_bsdf(bsdf: bpy.types.ShaderNodeBsdfPrincipled, key_candidates: list[str], val: any) -> None:
    for k in key_candidates:
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = val
            return


def setup_all_materials() -> dict[str, bpy.types.Material]:
    """Build and return all materials dictionary."""
    mats: dict[str, bpy.types.Material] = {}

    # 1. Warm Natural American Oak Wood (Bed, Nightstands)
    mat = get_or_create_material("M_Warm_Oak_Wood")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.46, 0.30, 0.17, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.34)
    set_bsdf(bsdf, ["Specular IOR Level", "Specular"], 0.52)
    mats["OAK_WOOD"] = mat

    # 2. Wide-Plank Satin Oak Flooring
    mat = get_or_create_material("M_Oak_Floor_Planks")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.42, 0.28, 0.16, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.25)
    set_bsdf(bsdf, ["Specular IOR Level", "Specular"], 0.60)
    mats["OAK_FLOOR"] = mat

    # 3. Padded Headboard Cream Bouclé Linen
    mat = get_or_create_material("M_Padded_Headboard_Boucle")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.76, 0.71, 0.64, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.88)
    set_bsdf(bsdf, ["Sheen Weight", "Sheen"], 0.85)
    set_bsdf(bsdf, ["Sheen Tint"], (0.92, 0.88, 0.82, 1.0))
    mats["HEADBOARD_BOUCLE"] = mat

    # 4. Pure Crisp White Cotton (Sleeping Pillows)
    mat = get_or_create_material("M_Pillow_Crisp_Cotton")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.96, 0.95, 0.94, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.70)
    set_bsdf(bsdf, ["Sheen Weight", "Sheen"], 0.75)
    set_bsdf(bsdf, ["Subsurface Weight", "Subsurface"], 0.05)
    mats["PILLOW_COTTON"] = mat

    # 5. Pillow Seam Welt Piping (Crisp ivory accent)
    mat = get_or_create_material("M_Pillow_Welt_Piping")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.82, 0.78, 0.72, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.75)
    mats["PILLOW_PIPING"] = mat

    # 6. Folded Duvet Cozy Greige Blanket
    mat = get_or_create_material("M_Duvet_Cozy_Greige")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.54, 0.47, 0.39, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.84)
    set_bsdf(bsdf, ["Sheen Weight", "Sheen"], 0.80)
    mats["DUVET_FABRIC"] = mat

    # 7. Mattress Quilted Textile
    mat = get_or_create_material("M_Mattress_Fabric")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.91, 0.90, 0.89, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.80)
    mats["MATTRESS"] = mat

    # 8. Minimalist Off-White Plaster Wall
    mat = get_or_create_material("M_Wall_Minimalist_Plaster")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.88, 0.86, 0.82, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.92)
    mats["WALL_PLASTER"] = mat

    # 9. Baseboard Skirting
    mat = get_or_create_material("M_Baseboard_Skirting")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.86, 0.84, 0.80, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.40)
    mats["BASEBOARD"] = mat

    # 10. Window Frame Dark Bronze / Black Metal
    mat = get_or_create_material("M_Window_Frame_Metal")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.05, 0.05, 0.05, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.35)
    set_bsdf(bsdf, ["Metallic"], 0.85)
    mats["WINDOW_FRAME"] = mat

    # 11. Sheer White Pleated Curtains
    mat = get_or_create_material("M_Sheer_Curtain")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.96, 0.96, 0.96, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.80)
    set_bsdf(bsdf, ["Transmission Weight", "Transmission"], 0.70)
    set_bsdf(bsdf, ["Sheen Weight", "Sheen"], 0.90)
    mats["SHEER_CURTAIN"] = mat

    # 12. Architectural Clear Glass
    mat = get_or_create_material("M_Window_Glass")
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new(type="ShaderNodeOutputMaterial")
    transp = nodes.new(type="ShaderNodeBsdfTransparent")
    transp.inputs["Color"].default_value = (0.95, 0.98, 1.0, 1.0)
    gloss = nodes.new(type="ShaderNodeBsdfGlossy")
    gloss.inputs["Roughness"].default_value = 0.02
    mix = nodes.new(type="ShaderNodeMixShader")
    mix.inputs["Fac"].default_value = 0.08
    mat.node_tree.links.new(transp.outputs["BSDF"], mix.inputs[1])
    mat.node_tree.links.new(gloss.outputs["BSDF"], mix.inputs[2])
    mat.node_tree.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    mats["WINDOW_GLASS"] = mat

    # 13. Brushed Champagne Brass
    mat = get_or_create_material("M_Brushed_Brass")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.92, 0.78, 0.46, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.25)
    set_bsdf(bsdf, ["Metallic"], 1.0)
    set_bsdf(bsdf, ["Specular IOR Level", "Specular"], 0.70)
    mats["BRUSHED_BRASS"] = mat

    # 14. Matte Black Metal
    mat = get_or_create_material("M_Matte_Black")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.03, 0.03, 0.03, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.50)
    mats["MATTE_BLACK"] = mat

    # 15. Warm 2700K LED
    mat = get_or_create_material("M_Warm_LED_2700K")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (1.0, 0.90, 0.74, 1.0))
    set_bsdf(bsdf, ["Emission Color"], (1.0, 0.86, 0.64, 1.0))
    set_bsdf(bsdf, ["Emission Strength"], 16.0)
    mats["WARM_LED"] = mat

    # 16. Ceramic Vase Decor
    mat = get_or_create_material("M_Ceramic_Vase")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.76, 0.68, 0.60, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.45)
    mats["CERAMIC"] = mat

    # 17. Hardcover Art Book
    mat = get_or_create_material("M_Book_Cover")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.24, 0.25, 0.27, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.75)
    mats["BOOK"] = mat

    # 18. Plush Wool Area Rug
    mat = get_or_create_material("M_Plush_Wool_Rug")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_bsdf(bsdf, ["Base Color"], (0.84, 0.80, 0.74, 1.0))
    set_bsdf(bsdf, ["Roughness"], 0.92)
    set_bsdf(bsdf, ["Sheen Weight", "Sheen"], 0.60)
    mats["RUG"] = mat

    # 19. Glowing Morning Sky Exterior Plane
    mat = get_or_create_material("M_Exterior_Morning_Sky")
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new(type="ShaderNodeOutputMaterial")
    em = nodes.new(type="ShaderNodeEmission")
    em.inputs["Color"].default_value = (0.88, 0.94, 1.0, 1.0)
    em.inputs["Strength"].default_value = 5.0
    mat.node_tree.links.new(em.outputs["Emission"], out.inputs["Surface"])
    mats["EXTERIOR_SKY"] = mat

    return mats
