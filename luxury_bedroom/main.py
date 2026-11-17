"""Master Coordinator for Aesthetic Modern Luxury Master Bedroom Suite.

Tier 4 Coordinator: Assembles all modular kits into the live Blender scene.
Strictly decoupled modular architecture (<250 lines per module).
"""
from __future__ import annotations

import math
import bpy
from mathutils import Vector

from luxury_bedroom.core.mesh_utils import (
    get_or_create_collection,
    clear_collection_objects,
)
from luxury_bedroom.core.materials import setup_all_materials
from luxury_bedroom.prefabs.arch_kit import build_architectural_shell
from luxury_bedroom.prefabs.bed_kit import build_bed_assembly
from luxury_bedroom.prefabs.soft_goods_kit import build_soft_goods
from luxury_bedroom.prefabs.furniture_kit import build_furniture
from luxury_bedroom.prefabs.lighting_kit import build_lighting


def assemble_luxury_bedroom() -> dict[str, any]:
    """Execute complete modular assembly of the 5-star master bedroom suite."""
    print(">>> Assembling Modular Aesthetic Luxury Master Bedroom Suite...")

    # 1. Prepare clean collections
    col_names = [
        "01_Architecture",
        "02_Bed_Assembly",
        "03_Bedding",
        "04_Furniture",
        "05_Lighting",
        "06_Camera",
    ]
    cols: dict[str, bpy.types.Collection] = {}
    for cname in col_names:
        col = get_or_create_collection(cname)
        clear_collection_objects(col)
        cols[cname] = col

    # 2. Materials
    mats = setup_all_materials()

    # 3. Build Prefab Kits
    print("--> 1/5 Building Architecture...")
    arch_objs = build_architectural_shell(cols["01_Architecture"], mats)

    print("--> 2/5 Building Bed Assembly...")
    bed_objs = build_bed_assembly(cols["02_Bed_Assembly"], mats)

    print("--> 3/5 Building Bedding & Soft Goods...")
    soft_objs = build_soft_goods(cols["03_Bedding"], mats)

    print("--> 4/5 Building Nightstands & Furniture...")
    furn_objs = build_furniture(cols["04_Furniture"], mats)

    print("--> 5/5 Setting up Lighting...")
    light_objs = build_lighting(cols["05_Lighting"], mats)

    # 4. Camera Setup
    print("--> Configuring Perspective Hero Camera...")
    cam_col = cols["06_Camera"]
    cam_name = "Camera_Hero_Perspective"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        cam_col.objects.link(cam_obj)

    cam_obj.location = (2.25, -1.60, 1.25)
    cam_obj.data.lens = 32.0  # 32mm architectural wide-normal
    cam_obj.data.clip_start = 0.1
    cam_obj.data.clip_end = 50.0

    target = Vector((0.0, 1.10, 0.65))
    direction = target - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam_obj

    # 5. Viewport & Render Settings
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.shading.type = "MATERIAL"
                        space.region_3d.view_perspective = "CAMERA"

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        try:
            scene.eevee.use_gtao = True
        except AttributeError:
            pass
        try:
            scene.eevee.use_bloom = True
        except AttributeError:
            pass

    total_objs = (
        len(arch_objs) + len(bed_objs) + len(soft_objs) + len(furn_objs) + len(light_objs) + 1
    )
    print(f">>> Complete Suite Successfully Assembled ({total_objs} Modular Props in 6 Collections)!")
    return {
        "status": "SUCCESS",
        "objects_created": total_objs,
        "collections": list(cols.keys()),
        "camera": cam_name,
    }


if __name__ == "__main__":
    assemble_luxury_bedroom()
