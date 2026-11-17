import pytest
from blender_mcp.server import mcp


def test_phases_4_to_7_tools_registered():
    """Verify that all Phase 4-7 MCP tools are registered on the FastMCP instance."""
    tools = list(mcp._tool_manager._tools.keys())

    expected_tools = [
        # Phase 4: Camera Framing & Composition
        "frame_camera_to_object",
        "setup_camera_dof",
        "create_turntable_camera",
        "inspect_camera_setup",

        # Phase 5: Automated Mesh Repair & Remeshing
        "repair_mesh_topology",
        "decimate_mesh",
        "quad_remesh",
        "generate_lod_chain",

        # Phase 6: Cloth Simulation & Surface Placement
        "setup_cloth_physics",
        "bake_cloth_drop",
        "inspect_cloth_simulation",
        "snap_to_surface",
        "align_object_to_surface",
        "scatter_instances",
        "inspect_scatter_result",

        # Phase 7: Modifier Stack Automation & Mechanical Rigging
        "apply_modifier_stack",
        "inspect_modifier_stack",
        "freeze_modifiers",
        "setup_vehicle_rig",
        "setup_hinge_constraint",
        "setup_mechanical_pivot",
        "inspect_rig_hierarchy",
    ]

    for tool in expected_tools:
        assert tool in tools, f"Tool '{tool}' is not registered on FastMCP server"
