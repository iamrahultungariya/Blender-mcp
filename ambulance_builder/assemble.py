"""
Ambulance Builder - Master Coordinator & Assembly Orchestrator.
Assembles the complete Type II Sprinter Ambulance beside the bedroom in collection 07_AMBULANCE_BAY.
"""
import bpy
from mathutils import Vector

from ambulance_builder.materials import setup_ambulance_materials
from ambulance_builder.chassis import build_chassis_and_interior
from ambulance_builder.body import build_body_shell
from ambulance_builder.cladding import build_cladding_and_bumpers
from ambulance_builder.glass import build_glass_and_doors
from ambulance_builder.emergency import build_emergency_system
from ambulance_builder.wheels import spawn_wheel_instances
from ambulance_builder.decals import build_livery_decals
from ambulance_builder.staging import build_ambulance_staging, evaluate_ambulance_budget

def get_or_create_collection(name: str) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col

def assemble_ambulance(base_offset=Vector((6.0, 0.0, 0.0)), save_scene=True):
    col = get_or_create_collection("07_AMBULANCE_BAY")

    print(f"Starting Modular Ambulance Construction at {base_offset}...")
    setup_ambulance_materials()

    build_chassis_and_interior(base_offset, col)
    build_body_shell(base_offset, col)
    build_cladding_and_bumpers(base_offset, col)
    build_glass_and_doors(base_offset, col)
    build_emergency_system(base_offset, col)
    spawn_wheel_instances(base_offset, col)
    build_livery_decals(base_offset, col)
    build_ambulance_staging(base_offset, col)

    total_tris = evaluate_ambulance_budget()

    if save_scene:
        current_path = bpy.data.filepath or r"c:\Users\Rahul\OneDrive\Desktop\Blender MCP\Luxury_Master_Bedroom_Aesthetic.blend"
        bpy.ops.wm.save_as_mainfile(filepath=current_path)
        print(f"Scene cleanly saved to {current_path}")

    return total_tris

if __name__ == "__main__":
    assemble_ambulance()
