import pytest
from blender_mcp.spatial_thinking import SpatialThinkingEngine

def test_classify_domain_heuristics():
    engine = SpatialThinkingEngine()
    assert engine.classify_domain("modern luxury villa with swimming pool") == "ARCHITECTURE"
    assert engine.classify_domain("scandinavian minimalist bedroom interior") == "INTERIOR_SPACES"
    assert engine.classify_domain("leather Chesterfield sofa 3 seater") == "FURNITURE_PRODUCT"
    assert engine.classify_domain("supercar GT-R aerodynamic chassis") == "VEHICLE"

def test_architectural_dimensions_and_datums():
    engine = SpatialThinkingEngine()
    villa = engine.get_dimensions("MODERN_VILLA")
    assert villa["exterior_wall_thickness"] >= 0.20
    assert villa["floor_to_floor"] >= 2.80
    assert villa["door_height"] == 2.10

def test_cushion_loft_parabolic_curvature():
    engine = SpatialThinkingEngine()
    crown = 0.05
    z0 = 0.45
    # Center (u=0, v=0) must reach maximum crown height
    assert pytest.approx(engine.calculate_cushion_loft(0.0, 0.0, crown, z0), abs=1e-4) == z0 + crown
    # Edges (u=1 or v=1) must drop to baseline z0
    assert pytest.approx(engine.calculate_cushion_loft(1.0, 0.0, crown, z0), abs=1e-4) == z0
    assert pytest.approx(engine.calculate_cushion_loft(0.0, 1.0, crown, z0), abs=1e-4) == z0

def test_spatial_blueprint_generation():
    engine = SpatialThinkingEngine()
    blueprint = engine.generate_spatial_blueprint("velvet lounge armchair")
    assert blueprint["domain"] == "FURNITURE_PRODUCT"
    assert "dimensions" in blueprint
    assert blueprint["anti_boxy_mandate"]["zero_unfilleted_primitives"] is True


def test_component_tree_architecture_domain():
    from blender_mcp.bmesh_toolkit import get_component_tree
    tree = get_component_tree("HOUSE")
    assert "structural_walls" in tree["systems"]
    assert "roof_structure" in tree["systems"]
    assert "fenestration" in tree["systems"]
    assert "main_chassis" not in tree["systems"].get("primary_structure", {}).get("components", [])

def test_component_tree_interior_domain():
    from blender_mcp.bmesh_toolkit import get_component_tree
    tree = get_component_tree("LIVING_ROOM")
    assert "room_envelope" in tree["systems"]
    assert "trim_carpentry" in tree["systems"]

def test_component_tree_furniture_domain():
    from blender_mcp.bmesh_toolkit import get_component_tree
    tree = get_component_tree("SOFA")
    assert "cushion_assemblies" in tree["systems"]
    assert "frame_and_chassis" in tree["systems"]

def test_component_tree_vehicle_domain_preserved():
    from blender_mcp.bmesh_toolkit import get_component_tree
    tree = get_component_tree("VEHICLE")
    assert "body_shell" in tree["systems"]
    assert "wheel_assembly" in tree["systems"]

