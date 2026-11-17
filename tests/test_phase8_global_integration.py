"""Phase 8: Global End-to-End Integration Suite for Rahul 3D Engine.

Tests the complete multi-system pipeline combining:
1. Scene Checkpoints & Safe Mode (System 07)
2. PBR Materials & Procedural Shaders (System 01)
3. Cinematic Studio Lighting & HDRI (System 02)
4. Camera Framing, Composition & DoF (System 03)
5. Automated Mesh Repair, Remeshing & LOD (System 04)
6. Cloth Physics & Draping (System 05)
7. Surface Raycast Placement & Instancing (System 06)
8. Declarative Modifier Stack (System 08)
9. Mechanical & Vehicle Rigging (System 09)
10. G0-G6 Pipeline Gates validation with expanded tool evidence
"""
import pytest
import shutil
from pathlib import Path
from blender_mcp.checkpoint_manager import (
    create_scene_checkpoint,
    list_scene_checkpoints,
    restore_scene_checkpoint,
    delete_scene_checkpoint,
)
import blender_mcp.checkpoint_manager as cm
from blender_mcp.material_engine import (
    assign_pbr_material,
    inspect_material_nodes,
    create_procedural_shader,
    modify_material_property,
    validate_material_setup,
)
from blender_mcp.lighting_engine import (
    setup_studio_lighting,
    setup_environment_hdri,
    inspect_lighting_setup,
    adjust_lighting_for_object,
)
from blender_mcp.camera_engine import (
    frame_camera_to_object,
    setup_camera_dof,
    create_turntable_camera,
    inspect_camera_setup,
)
from blender_mcp.topology_engine import (
    repair_mesh_topology,
    decimate_mesh,
    quad_remesh,
    generate_lod_chain,
)
from blender_mcp.cloth_engine import (
    setup_cloth_physics,
    bake_cloth_drop,
    inspect_cloth_simulation,
)
from blender_mcp.placement_engine import (
    snap_to_surface,
    align_object_to_surface,
    scatter_instances,
    inspect_scatter_result,
)
from blender_mcp.modifier_engine import (
    apply_modifier_stack,
    inspect_modifier_stack,
    freeze_modifiers,
)
from blender_mcp.rigging_engine import (
    setup_vehicle_rig,
    setup_hinge_constraint,
    setup_mechanical_pivot,
    inspect_rig_hierarchy,
)
from blender_mcp.pipeline_gates import PhaseGateManager


@pytest.fixture(autouse=True)
def clean_checkpoints_dir(tmp_path, monkeypatch):
    test_dir = tmp_path / "test_checkpoints"
    monkeypatch.setenv("BLENDER_CHECKPOINT_DIR", str(test_dir))
    cm.DEFAULT_CHECKPOINT_DIR = test_dir
    yield
    if test_dir.exists():
        shutil.rmtree(test_dir, ignore_errors=True)


def test_full_pipeline_checkpoint_lifecycle():
    """Test checkpoint creation, listing, restoration, and deletion."""
    cp = create_scene_checkpoint(
        label="integration_baseline",
        description="E2E test checkpoint",
    )
    assert cp["success"] is True
    cp_id = cp["result"]["checkpoint_id"]
    assert cp_id is not None
    assert cp_id.startswith("cp_")

    cp_list = list_scene_checkpoints()
    assert cp_list["success"] is True
    assert cp_list["result"]["count"] >= 1

    restored = restore_scene_checkpoint("integration_baseline")
    assert restored["success"] is True

    deleted = delete_scene_checkpoint(cp_id)
    assert deleted["success"] is True
    assert deleted["result"]["deleted_checkpoint_id"] == cp_id


def test_material_and_shader_suite():
    """Test procedural shader creation, PBR assignment, inspection, and validation."""
    proc = create_procedural_shader(
        material_name="Oak_Wood",
        preset="wood",
        object_name="Desk",
        scale=3.0,
        roughness_multiplier=1.2,
    )
    assert proc["success"] is True
    assert proc["result"]["preset"] == "wood"

    pbr = assign_pbr_material(
        object_name="Desk",
        material_name="Metal_Legs",
        base_color=[0.1, 0.1, 0.1, 1.0],
        metallic=0.9,
        roughness=0.2,
    )
    assert pbr["success"] is True

    mod = modify_material_property(
        material_name="Metal_Legs",
        property_name="Roughness",
        value=0.15,
    )
    assert mod["success"] is True

    nodes = inspect_material_nodes(material_name="Metal_Legs")
    assert nodes["success"] is True

    val = validate_material_setup(material_name="Metal_Legs")
    assert val["success"] is True
    assert val["result"]["valid"] is True


def test_lighting_and_hdri_suite():
    """Test studio lighting presets, HDRI setup, inspection, and object adjustment."""
    studio = setup_studio_lighting(
        preset="automotive_studio",
        target_object="HeroCar",
        energy_multiplier=1.5,
        color_temperature=5500,
    )
    assert studio["success"] is True
    assert studio["result"]["preset"] == "automotive_studio"

    hdri = setup_environment_hdri(
        hdri_path_or_preset="studio_warm",
        strength=0.8,
        rotation=45.0,
    )
    assert hdri["success"] is True

    insp = inspect_lighting_setup()
    assert insp["success"] is True

    adj = adjust_lighting_for_object(target_object="HeroCar")
    assert adj["success"] is True


def test_camera_framing_and_dof_suite():
    """Test camera framing angles, compositions, DoF bokeh, and turntable creation."""
    frame = frame_camera_to_object(
        object_name="HeroCar",
        lens_mm=50.0,
        angle="hero",
        composition="rule_of_thirds",
    )
    assert frame["success"] is True
    assert frame["result"]["angle"] == "hero"

    dof = setup_camera_dof(
        target_object="HeroCar",
        f_stop=2.8,
        enabled=True,
    )
    assert dof["success"] is True

    turntable = create_turntable_camera(
        target_object="HeroCar",
        frames=120,
    )
    assert turntable["success"] is True
    assert turntable["result"]["total_frames"] == 120

    cam_insp = inspect_camera_setup()
    assert cam_insp["success"] is True


def test_topology_repair_and_lod_suite():
    """Test mesh repair, quad remeshing, decimation, and LOD chain generation."""
    rep = repair_mesh_topology(
        object_name="HeroCar",
        remove_doubles=True,
        fix_normals=True,
    )
    assert rep["success"] is True

    remesh = quad_remesh(
        object_name="HeroCar",
        target_quads=2500,
    )
    assert remesh["success"] is True
    assert remesh["result"]["target_quads"] == 2500

    dec = decimate_mesh(
        object_name="HeroCar",
        target_ratio=0.5,
        preserve_uvs=True,
    )
    assert dec["success"] is True
    assert dec["result"]["target_ratio"] == 0.5

    lods = generate_lod_chain(
        object_name="HeroCar",
        lod_ratios=[1.0, 0.5, 0.25],
    )
    assert lods["success"] is True
    assert lods["result"]["total_lods"] == 3


def test_cloth_and_surface_placement_suite():
    """Test cloth physics, simulation bake, raycast snapping, and instancing."""
    cloth = setup_cloth_physics(
        cloth_object="Blanket",
        preset="cotton",
        mass=0.2,
    )
    assert cloth["success"] is True

    bake = bake_cloth_drop(
        cloth_object="Blanket",
        collision_objects=["BedFrame"],
        steps=10,
    )
    assert bake["success"] is True

    cloth_insp = inspect_cloth_simulation(cloth_object="Blanket")
    assert cloth_insp["success"] is True

    snap = snap_to_surface(
        object_name="Pillow",
        target_surface_name="BedFrame",
        offset=0.002,
    )
    assert snap["success"] is True

    align = align_object_to_surface(
        object_name="Pillow",
        target_surface_name="BedFrame",
    )
    assert align["success"] is True

    scat = scatter_instances(
        collection_name="ScatterBooks",
        target_surface="Desk",
        count=10,
    )
    assert scat["success"] is True

    scat_insp = inspect_scatter_result(target_surface="Desk")
    assert scat_insp["success"] is True


def test_modifier_and_rigging_suite():
    """Test modifier stack declarative builder, freeze, hinge constraint, and vehicle rig."""
    stack = apply_modifier_stack(
        object_name="Cabinet",
        stack=[
            {"type": "BEVEL", "width": 0.015, "segments": 3},
            {"type": "SUBSURF", "levels": 1},
        ],
    )
    assert stack["success"] is True

    mod_insp = inspect_modifier_stack(object_name="Cabinet")
    assert mod_insp["success"] is True

    frz = freeze_modifiers(
        object_name="Cabinet",
        modifier_names=["Bevel"],
    )
    assert frz["success"] is True

    rig = setup_vehicle_rig(
        chassis_obj="Car_Chassis",
        wheel_objs=["Car_Wheel_FL", "Car_Wheel_FR", "Car_Wheel_RL", "Car_Wheel_RR"],
        steering_wheels=["Car_Wheel_FL", "Car_Wheel_FR"],
    )
    assert rig["success"] is True

    hinge = setup_hinge_constraint(
        door_obj="Cabinet_Door",
        frame_obj="Cabinet",
        axis="Z",
        limits=(-90.0, 0.0),
    )
    assert hinge["success"] is True

    pivot = setup_mechanical_pivot(
        object_name="Cabinet_Door",
        pivot_location=[0.0, 0.5, 0.0],
    )
    assert pivot["success"] is True

    rig_insp = inspect_rig_hierarchy(root_obj="Car_Chassis")
    assert rig_insp["success"] is True


def test_pipeline_gates_with_expanded_evidence(tmp_path):
    """Test sequential G0-G6 pipeline gates validation with newly integrated tool evidence keys."""
    state_file = tmp_path / ".pipeline_state.json"
    mgr = PhaseGateManager(state_file=state_file)

    # Phase 1
    g1 = mgr.validate_gate(1, evidence={"datums_reconciled": True})
    assert g1["status"] == "PASS"

    # Phase 2
    g2 = mgr.validate_gate(2, evidence={"component_strategies": {"body": "subdivision_cage", "wheels": "boolean_bevel"}})
    assert g2["status"] == "PASS"

    # Phase 3 with topology_repaired from repair_mesh_topology
    g3 = mgr.validate_gate(3, evidence={"specular_clay_verified": True, "topology_repaired": True})
    assert g3["status"] == "PASS"

    # Phase 4 with modifier_stack_applied
    g4 = mgr.validate_gate(4, evidence={"wheelhouse_recessed": True, "modifier_stack_applied": True})
    assert g4["status"] == "PASS"

    # Phase 5 with rig_hierarchy_verified
    g5 = mgr.validate_gate(5, evidence={"hero_depth_verified": True, "rig_hierarchy_verified": True})
    assert g5["status"] == "PASS"

    # Phase 6 with pbr_material_assigned, studio_lighting_configured, camera_framed
    g6 = mgr.validate_gate(
        6,
        evidence={
            "pbr_material_assigned": True,
            "studio_lighting_configured": True,
            "camera_framed": True,
        },
    )
    assert g6["status"] == "PASS"
    assert g6["next_phase"] == "COMPLETE"

    status = mgr.get_status()
    assert status["passed_count"] == 6
    assert status["pipeline_verdict"] == "APPROVED_FOR_EXPORT"
